import os, sys, tempfile, unittest

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, HERE)
import match


def tmp(text, ext=".txt"):
    f = tempfile.NamedTemporaryFile("w", suffix=ext, delete=False, encoding="utf-8")
    f.write(text); f.close()
    return f.name


class Classify(unittest.TestCase):
    def test_categories(self):
        c = match.classify
        self.assertEqual(c("Intel Xeon Gold 6526Y 2.8G, 16C/32T"), "cpu")
        self.assertEqual(c("32GB RDIMM, 5600MT/s, Dual Rank"), "memory")
        self.assertEqual(c("PERC H755 SAS Front 8GB cache"), "controller")
        self.assertEqual(c("BOSS-N1 controller card + with 2 M.2 480GB (RAID 1)"), "boot")
        self.assertEqual(c("Broadcom 57414 Dual Port 10/25GbE SFP28, OCP NIC 3.0"), "nic")
        self.assertEqual(c("1.92TB SSD SAS Mixed Use 24Gbps 512e 2.5in Hot-Plug"), "drive")
        self.assertEqual(c("HPE 1600W Flex Slot Platinum Hot Plug Power Supply Kit"), "psu")
        self.assertEqual(c("NVIDIA L4 24GB PCIe Accelerator"), "gpu")
        self.assertEqual(c("ProSupport and Next Business Day Onsite Service, 60 Month(s)"), "service")
        self.assertEqual(c("HPE ProLiant DL360 Gen12 8SFF Configure-to-order Server"), "platform")


class Spec(unittest.TestCase):
    def test_ns204_is_a_480gb_mirrored_pair(self):
        s = match.spec("boot", "HPE NS204i-u v2 Gen11 NVMe Hot Plug Boot Optimized Storage Device")
        self.assertEqual(s["drives"], 2); self.assertEqual(s["tb"], 0.48); self.assertEqual(s["iface"], "nvme")

    def test_digit_inside_a_word_is_not_a_drive_count(self):
        s = match.spec("boot", "Boot device Gen11 NVMe 480GB")
        self.assertNotEqual(s.get("drives"), 1)

    def test_ocp3_is_ocp(self):
        self.assertTrue(match.spec("nic", "Broadcom BCM57414 10/25Gb 2-port SFP28 OCP3 Adapter")["ocp"])

    def test_nic_ports_and_media(self):
        s = match.spec("nic", "Intel E810-XXV Dual Port 10/25GbE SFP28 Adapter")
        self.assertEqual(s["ports"], 2); self.assertEqual(s["media"], "sfp"); self.assertIn(25, s["speeds"])


class Load(unittest.TestCase):
    def test_csv_prefers_description_over_part_number_column(self):
        p = tmp("Product #,Description,Qty\nP60640-B21,HPE ProLiant DL360 Gen12 Server,10\n", ".csv")
        rows = match.load(p)
        self.assertEqual(rows[0]["text"], "HPE ProLiant DL360 Gen12 Server"); self.assertEqual(rows[0]["qty"], 10)

    def test_text_qty_prefix(self):
        rows = match.load(tmp("2 x Intel Xeon Gold 6526Y 16C\n16 x 32GB RDIMM 5600\n"))
        self.assertEqual([r["qty"] for r in rows], [2, 16])


class Run(unittest.TestCase):
    def test_order_totals_are_divided_by_server_count(self):
        p = tmp("Product #,Description,Qty\nX,HPE ProLiant DL360 Gen12 8SFF Server,10\nY,INT Xeon-G 6724P CPU,10\n"
                "Z,HPE 64GB Dual Rank x4 DDR5-6400 Registered Memory,160\n", ".csv")
        r = match.run(p)
        self.assertEqual(r["nodes"], 10)
        mem = next(x for x in r["rows"] if x["cat"] == "memory")
        self.assertEqual(mem["qty"], 16)
        self.assertEqual(mem["candidates"][0]["fc"], "C0TQ")

    def test_only_real_feature_codes_are_proposed(self):
        r = match.run(tmp("1 x PowerEdge R760 Server\n2 x Intel Xeon Gold 6526Y 2.8G, 16C/32T (195W)\n"))
        import dcsc_rules
        codes = {o[3] for o in dcsc_rules.options(dcsc_rules.load(), r["target"])}
        for row in r["rows"]:
            for c in row["candidates"]:
                self.assertIn(c["fc"], codes)

    def test_ties_go_to_tce(self):
        r = match.run(tmp("1 x PowerEdge R760 Server\n1 x PERC H755 SAS Front 8GB cache\n"))
        ctl = next(x for x in r["rows"] if x["cat"] == "controller")
        self.assertTrue(ctl["candidates"][0]["tce"])


if __name__ == "__main__":
    unittest.main()
