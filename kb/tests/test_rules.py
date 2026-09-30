"""Tests for kb/rules.py and kb/specs.py.   python -m unittest discover -s kb/tests"""
import os, sys, tempfile, unittest

KB = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if KB not in sys.path:
    sys.path.insert(0, KB)
import rules, specs

L = lambda fc, descr, qty=1: dict(fc=fc, descr=descr, qty=qty)
run = lambda lines, **kw: rules.validate(lines, **kw)
ids = lambda fs: {f["rule"] for f in fs}
hit = lambda fs, rid: [f for f in fs if f["rule"] == rid]

CPU = L("C5QV", "Intel Xeon 6517P 16C 190W 3.2GHz Processor", 2)
DIMM = L("C0TQ", "ThinkSystem 64GB TruDDR5 6400MHz (2Rx4) RDIMM", 8)
PSU = L("C2Y9", "ThinkSystem 1300W Titanium CRPS Hot-Swap Power Supply", 2)
HX = dict(mtm="7DG4CTO1WW", family="ThinkAgile HX650 V4", nodes=3)


class Loaders(unittest.TestCase):
    def test_text_qty_x_format(self):
        b = rules.parse_text("2 x BN2T ThinkSystem Broadcom 57414 10/25GbE SFP28 2-Port OCP Ethernet Adapter\n8x C0TQ 64GB RDIMM")
        self.assertEqual([(l["fc"], l["qty"]) for l in b], [("BN2T", 2), ("C0TQ", 8)])

    def test_text_tab_format_and_directives(self):
        t = "# mtm: 7DG4CTO1WW\n# nodes: 3\n# workload: nutanix\n# tce: yes\nBN2T\tBroadcom 57414 OCP Ethernet Adapter\t2\n"
        b = rules.parse_text(t)
        self.assertEqual(b[0]["fc"], "BN2T"); self.assertEqual(b[0]["qty"], 2)
        self.assertEqual((b.meta["mtm"], b.meta["nodes"], b.meta["workload"], b.meta["tce"]), ("7DG4CTO1WW", 3, "nutanix", True))

    def test_unparsed_lines_are_reported_not_dropped_silently(self):
        b = rules.parse_text("2 x BN2T adapter\nthis is prose\n")
        self.assertEqual(len(b), 1)
        self.assertTrue(any("not parsed" in n for n in b.meta["notes"]))

    def test_cluster_totals_are_divided_by_nodes(self):
        b = rules.parse_text("# cluster_totals: yes\n3 x 7DG4CTO1WW ThinkAgile HX650 V4\n6 x C5QV Intel Xeon 6517P 16C Processor\n24 x C0TQ 64GB RDIMM\n")
        self.assertEqual(b.meta["nodes"], 3)
        self.assertEqual({l["fc"]: l["qty"] for l in b}, {"7DG4CTO1WW": 1, "C5QV": 2, "C0TQ": 8})

    def test_xlsx_quote_sheet(self):
        import openpyxl
        wb = openpyxl.Workbook(); ws = wb.active; ws.title = "Quote"
        ws.append(["Feature", "Part", "Description", "x", "Qty", "Unit"])
        ws.append(["7DG4CTO1WW", "", "Server : ThinkAgile HX650 V4", "", 3, 1.0])
        ws.append(["C5QV", "", "Intel Xeon 6517P 16C 190W 3.2GHz Processor", "", 6, 1.0])
        ws.append(["C0TQ", "", "ThinkSystem 64GB TruDDR5 6400MHz (2Rx4) RDIMM", "", 24, 1.0])
        fd, p = tempfile.mkstemp(suffix=".xlsx"); os.close(fd)
        try:
            wb.save(p)
            b = rules.load_bom(p)
        finally:
            os.remove(p)
        self.assertEqual(b.meta["mtm"], "7DG4CTO1WW"); self.assertEqual(b.meta["nodes"], 3)
        self.assertEqual({l["fc"]: l["qty"] for l in b}["C5QV"], 2)

    def test_load_bom_text_file(self):
        fd, p = tempfile.mkstemp(suffix=".txt"); os.close(fd)
        try:
            with open(p, "w", encoding="utf-8") as f: f.write("2 x C5QV Intel Xeon 6517P Processor\n")
            self.assertEqual(rules.load_bom(p)[0]["fc"], "C5QV")
        finally:
            os.remove(p)


class Overrides(unittest.TestCase):
    def test_eleven_verdicts_with_required_fields(self):
        self.assertEqual(len(rules.TCE_OVERRIDES), 11)
        for o in rules.TCE_OVERRIDES:
            self.assertEqual(set(o), {"fc", "mtm", "tce", "verified_on", "basis", "note"})
            self.assertIn(o["basis"], ("panel", "doc", "rep"))

    def test_exact_mtm_beats_wildcard_and_unknown_is_none(self):
        self.assertIs(rules.tce_verdict("C5QQ", "7DG4CTO1WW"), False)
        self.assertIsNone(rules.tce_verdict("C5QQ", "7DG3CTO1WW"))
        self.assertIs(rules.tce_verdict("C1X9", "7DGDCTO1WW"), False)
        self.assertIs(rules.tce_verdict("C520", "anything"), True)


class Nics(unittest.TestCase):
    def test_hx_nic_single_vendor_fails_on_mix(self):
        fs = run([L("BPPW", "ThinkSystem Broadcom 57504 10/25GbE SFP28 4-Port OCP Ethernet Adapter"),
                  L("BE4U", "ThinkSystem Mellanox ConnectX-6 Lx 10/25GbE SFP28 2-port PCIe Ethernet Adapter")], **HX)
        self.assertEqual(len(hit(fs, "hx-nic-single-vendor")), 1)

    def test_hx_nic_single_vendor_passes_same_vendor_and_skips_thinksystem(self):
        ok = [L("BPPW", "Broadcom 57504 OCP Ethernet Adapter"), L("BNWM", "Broadcom 57504 PCIe Ethernet Adapter")]
        self.assertNotIn("hx-nic-single-vendor", ids(run(ok, **HX)))
        mix = [L("A", "Intel E810 Ethernet Adapter"), L("B", "Mellanox ConnectX-6 Ethernet Adapter")]
        self.assertNotIn("hx-nic-single-vendor", ids(run(mix, mtm="7DG9CTO1WW")))

    def test_thinksystem_nic_mix_warns_same_speed(self):
        fs = run([L("A", "Intel E810-XXV 10/25GbE SFP28 Ethernet Adapter"), L("B", "Broadcom 57414 10/25GbE SFP28 Ethernet Adapter")], mtm="7DG9CTO1WW")
        self.assertEqual(len(hit(fs, "thinksystem-nic-mix-role")), 1)

    def test_thinksystem_nic_mix_silent_across_roles(self):
        fs = run([L("A", "Mellanox ConnectX-6 Lx 10/25GbE SFP28 Ethernet Adapter"), L("B", "Intel I350-T4 PCIe 1GbE RJ45 Ethernet Adapter")], mtm="7DG9CTO1WW")
        self.assertNotIn("thinksystem-nic-mix-role", ids(fs))


class HxPlatform(unittest.TestCase):
    H630 = dict(mtm="7DG3CTO1WW", family="ThinkAgile HX630 V4", nodes=3)

    def test_hx630_dual_socket(self):
        one = L("C5QQ", "Intel Xeon 6505P 12C 150W 2.2GHz Processor", 1)
        two = L("C5QQ", "Intel Xeon 6505P 12C 150W 2.2GHz Processor", 2)
        self.assertEqual(len(hit(run([one], **self.H630), "hx630-dual-socket")), 1)
        self.assertEqual(len(hit(run([two], **self.H630), "hx630-dual-socket")), 0)

    def test_hx630_384gb(self):
        d = lambda gb, q: [L("X", f"ThinkSystem {gb}GB TruDDR5 6400MHz RDIMM", q)]
        self.assertEqual(len(hit(run(d(64, 6), **self.H630), "hx630-384gb-unbuildable")), 1)
        self.assertEqual(len(hit(run(d(64, 8), **self.H630), "hx630-384gb-unbuildable")), 0)

    def test_hx_nvme_single_sku(self):
        mix = [L("CCVZ", 'ThinkAgile HX 2.5" U.2 VA 3.2TB Mixed Use NVMe PCIe 4.0 SSD', 2),
               L("C3Q9", 'ThinkAgile HX 2.5" U.2 VA 3.84TB Read Intensive NVMe PCIe 4.0 SSD', 8)]
        self.assertEqual(len(hit(run(mix, **HX), "hx-nvme-single-sku")), 1)
        self.assertEqual(len(hit(run(mix[1:], **HX), "hx-nvme-single-sku")), 0)
        self.assertEqual(len(hit(run(mix, mtm="7DG4CTO2WW", nodes=3), "hx-nvme-single-sku")), 0)  # hybrid exempt

    def test_hx650_storage_hybrid_floor(self):
        hdd = lambda n: [L("C4DA", 'ThinkSystem 3.5" 12TB 7.2K SAS 12Gb Hot Swap 512e HDD v2', n)]
        kw = dict(mtm="7DG4CTO2WW", nodes=3)
        self.assertEqual(len(hit(run(hdd(4), **kw), "hx650-storage-hybrid-floor")), 1)
        self.assertEqual(len(hit(run(hdd(10), **kw), "hx650-storage-hybrid-floor")), 0)
        self.assertEqual(len(hit(run(hdd(12), **kw), "hx650-storage-hybrid-floor")), 0)

    def test_hx650_bays_socket_min_warns_and_admits_unsettled(self):
        n9 = [L("C5QV", "Intel Xeon 6517P Processor", 1), L("C3Q9", "3.84TB NVMe SSD", 9)]
        f = hit(run(n9, **HX), "hx650-bays-socket-min")
        self.assertEqual(len(f), 1); self.assertIn("UNSETTLED", f[0]["message"])
        self.assertEqual(len(hit(run([L("C5QV", "Xeon 6517P Processor", 1), L("C3Q9", "3.84TB NVMe SSD", 8)], **HX), "hx650-bays-socket-min")), 0)
        self.assertEqual(len(hit(run([L("C5QV", "Xeon 6517P Processor", 2), L("C3Q9", "3.84TB NVMe SSD", 9)], **HX), "hx650-bays-socket-min")), 0)


class Nutanix(unittest.TestCase):
    def test_min_3_policy_and_platform_note_at_2_nodes(self):
        fs = run([CPU], mtm="7DG4CTO1WW", family="ThinkAgile HX650 V4", nodes=2)
        self.assertEqual(len(hit(fs, "nutanix-min-3-policy")), 1)
        self.assertEqual(hit(fs, "nutanix-min-3-policy")[0]["severity"], "warn")
        self.assertEqual(hit(fs, "nutanix-2node-platform-truth")[0]["severity"], "info")

    def test_min_3_policy_silent_at_3_nodes_and_with_allow_flag(self):
        self.assertNotIn("nutanix-min-3-policy", ids(run([CPU], **HX)))
        self.assertNotIn("nutanix-min-3-policy", ids(run([CPU], mtm="7DG4CTO1WW", nodes=2, allow_2node=True)))
        self.assertNotIn("nutanix-min-3-policy", ids(run([CPU], mtm="7DG9CTO1WW", nodes=2)))  # not Nutanix

    def test_workload_nutanix_turns_on_hci_rules_for_thinksystem(self):
        fs = run([CPU], mtm="7DG9CTO1WW", nodes=2, workload="nutanix")
        self.assertEqual(len(hit(fs, "nutanix-min-3-policy")), 1)

    def test_2node_capacity_cap(self):
        big = [L("C3Q9", 'ThinkAgile HX 2.5" U.2 VA 3.84TB Read Intensive NVMe PCIe 4.0 SSD', 8)]   # 30.7TB
        self.assertEqual(len(hit(run(big, mtm="7DG4CTO1WW", nodes=2), "nutanix-2node-capacity-cap")), 1)
        self.assertEqual(len(hit(run(big, **HX), "nutanix-2node-capacity-cap")), 0)

    def test_capacity_gate_silent_on_normal_node_and_warns_past_307tb(self):
        norm = [L("C3Q9", 'ThinkAgile HX 2.5" U.2 VA 3.84TB Read Intensive NVMe PCIe 4.0 SSD', 9)]
        self.assertEqual(len(hit(run(norm, **HX), "nutanix-capacity-gate")), 0)
        big = [L("C3QG", 'ThinkAgile HX 2.5" U.2 VA 15.36TB Read Intensive NVMe PCIe 4.0 SSD', 24)]
        f = hit(run(big, **HX), "nutanix-capacity-gate")
        self.assertEqual(len(f), 1); self.assertIn("Unified Storage", f[0]["message"])


class Tce(unittest.TestCase):
    def test_all_or_nothing_fails_override_false_and_rack(self):
        fs = run([L("C1X9", "7.68TB NVMe SSD", 4), L("9363RC4", "42U Rack Cabinet", 1)], tce=True, mtm="7DG4CTO1WW")
        self.assertEqual(len(hit(fs, "tce-all-or-nothing")), 2)

    def test_all_or_nothing_uses_explicit_tce_flag(self):
        fs = run([dict(fc="Z999", descr="Some part", qty=1, tce=False)], tce=True, mtm="7DG9CTO1WW")
        self.assertEqual(len(hit(fs, "tce-all-or-nothing")), 1)

    def test_all_or_nothing_silent_when_clean(self):
        self.assertEqual(hit(run([L("C3Q9", "3.84TB NVMe SSD", 9)], tce=True, mtm="7DG4CTO1WW"), "tce-all-or-nothing"), [])

    def test_service_lines_never_fail_tce(self):
        svc = [dict(fc="5WS7C00907", descr="3Yr Premier NBD Resp SR645 V3", qty=1, tce=False),
               dict(fc="5PS7C20483", descr="3Yr KYD Add-On SR650 V4", qty=1, tce=False),
               dict(fc="QA18", descr="Premier", qty=1, tce=False),
               dict(fc="7Q01CTS2WW", descr="SERVER PREMIER NBD RESP", qty=1, tce=False),
               dict(fc="7D9CCTO1WW", descr="Server : ThinkSystem SR645 V3-3yr Base Warranty", qty=1, tce=False),
               dict(fc="00TU999", descr="RTS for Tape Devices- 1yr", qty=1, tce=False, section="Services")]
        self.assertEqual(hit(run(svc, tce=True, mtm="7D9CCTO1WW"), "tce-all-or-nothing"), [])

    def test_hardware_that_mentions_warranty_still_counts(self):
        hw = dict(fc="BLAC", descr="Lenovo ThinkSystem DB610S, 8 ports licensed, 8x 16Gb SWL SFPs, 1 PS, Rail Kit, Lifetime Warranty", qty=1, tce=False)
        f = hit(run([hw], tce=True, mtm="7D9CCTO1WW"), "tce-all-or-nothing")
        self.assertEqual(len(f), 1); self.assertIn("BLAC", f[0]["message"])

    def test_laser_service_indicator_is_hardware(self):
        c = rules.norm_line(dict(fc="CB2P", descr="SR650 V4 Laser service indicator", qty=1, tce=False))
        self.assertFalse(rules.is_service(c))

    def test_warranty_plus_hardware_names_only_hardware(self):
        fs = run([dict(fc="5WS7C00907", descr="3Yr Premier NBD Resp SR645 V3", qty=1, tce=False),
                  dict(fc="C5QQ", descr="Intel Xeon 6527P 12C 225W Processor", qty=2, tce=False)], tce=True, mtm="7D9CCTO1WW")
        f = hit(fs, "tce-all-or-nothing")
        self.assertEqual(len(f), 1); self.assertIn("C5QQ", f[0]["message"]); self.assertNotIn("5WS7C00907", f[0]["message"])

    def test_bu1e_in_bom_turns_tce_on(self):
        fs = run([L("BU1E", "Lenovo Top Choice Express Flag", 1), L("C1X9", "7.68TB NVMe SSD", 4)], mtm="7DG4CTO1WW")
        self.assertIn("tce-all-or-nothing", ids(fs))

    def test_tce_rules_off_without_tce(self):
        fs = run([L("C1X9", "7.68TB NVMe SSD", 4)], mtm="7DG4CTO1WW")
        self.assertFalse(ids(fs) & {"tce-all-or-nothing", "tce-platform-support", "tce-platform-unproven", "tce-dimm-max-64", "tce-needs-panel-check"})

    def test_dimm_max_64(self):
        self.assertEqual(len(hit(run([L("BZ7D", "ThinkSystem 96GB TruDDR5 6400MHz (2Rx4) RDIMM", 8)], tce=True, mtm="7DG4CTO1WW"), "tce-dimm-max-64")), 1)
        self.assertEqual(len(hit(run([DIMM], tce=True, mtm="7DG4CTO1WW"), "tce-dimm-max-64")), 0)

    def test_platform_support_fails_absent_families_from_family_or_mtm(self):
        for fam, mtm in [("ThinkSystem SR630 V3", "7D73CTO1WW"), ("ThinkSystem SR650 V3", "7D76CTO1WW"), ("ThinkSystem ST650 V3", "7D7ACTO1WW"),
                         ("ThinkAgile HX665 V3", "7D9NCTO3WW"), ("ThinkAgile HX630 V3", "7D6MCTO3WW"), ("ThinkAgile HX630", "7D6MCTO4WW"),
                         ("ThinkAgile HX650", "7D6NCTO4WW")]:
            self.assertEqual(len(hit(run([CPU], tce=True, family=fam, mtm=mtm), "tce-platform-support")), 1, fam)
            self.assertEqual(len(hit(run([CPU], tce=True, family="", mtm=mtm), "tce-platform-support")), 1, mtm)

    def test_platform_support_lookahead_keeps_hx_v4_clean(self):
        for fam, mtm in [("ThinkAgile HX630 V4", "7DG3CTO1WW"), ("ThinkAgile HX650 V4", "7DG4CTO1WW"), ("ThinkAgile HX650 V4", "7DG4CTO2WW")]:
            fs = run([CPU], tce=True, family=fam, mtm=mtm)
            self.assertEqual(hit(fs, "tce-platform-support"), [], fam)
            self.assertEqual(hit(fs, "tce-platform-unproven"), [], fam)

    def test_platform_support_passes_proven_families(self):
        for fam in ["ThinkSystem ST250 V3", "ThinkSystem SR250 V3", "ThinkSystem SR635 V3", "ThinkSystem SR645 V3", "ThinkSystem SR655 V3",
                    "ThinkSystem SR665 V3", "ThinkSystem SR630 V4", "ThinkSystem SR650 V4", "ThinkSystem SR650a V4", "ThinkAgile FX630 V4"]:
            fs = run([CPU], tce=True, family=fam)
            self.assertEqual(hit(fs, "tce-platform-support"), [], fam)
            self.assertEqual(hit(fs, "tce-platform-unproven"), [], fam)

    def test_platform_support_fails_v1_v2(self):
        self.assertEqual(len(hit(run([CPU], tce=True, family="ThinkSystem SR650 V2"), "tce-platform-support")), 1)
        self.assertEqual(len(hit(run([CPU], tce=True, family="ThinkSystem SR630 V1"), "tce-platform-support")), 1)

    def test_platform_unproven_warns_not_fails(self):
        fs = run([CPU], tce=True, family="ThinkAgile MX630 V4", mtm="7DFGCTO1WW")
        self.assertEqual(len(hit(fs, "tce-platform-unproven")), 1)
        self.assertEqual(hit(fs, "tce-platform-unproven")[0]["severity"], "warn")
        self.assertEqual(hit(fs, "tce-platform-support"), [])

    def test_needs_panel_check_is_info(self):
        f = hit(run([CPU], tce=True, mtm="7DG4CTO1WW"), "tce-needs-panel-check")
        self.assertEqual(len(f), 1); self.assertEqual(f[0]["severity"], "info")


class Storage(unittest.TestCase):
    def test_raid545_no_raid5(self):
        c = L("C0TU", "ThinkSystem RAID 545-8i PCIe Gen4 12Gb Adapter")
        self.assertEqual(len(hit(run([c], raid=5), "raid545-capability")), 1)
        self.assertEqual(len(hit(run([c], raid=6), "raid545-capability")), 1)
        self.assertEqual(len(hit(run([c], raid=1), "raid545-capability")), 0)
        self.assertEqual(len(hit(run([L("B8NY", "ThinkSystem RAID 940-8i 4GB Flash PCIe Gen4 12Gb Adapter")], raid=5), "raid545-capability")), 0)

    def test_nvme_behind_sas_raid_warns(self):
        fs = run([L("X", '2.5" U.2 VA 3.84TB Read Intensive NVMe SSD', 4), L("C0TU", "ThinkSystem RAID 545-8i SAS/SATA 12Gb Adapter")])
        self.assertEqual(len(hit(fs, "nvme-behind-sas-raid")), 1)
        ok = run([L("X", '2.5" U.2 VA 3.84TB Read Intensive NVMe SSD', 4), L("C0TU", "ThinkSystem RAID 940-8i Tri-Mode 12Gb Adapter")])
        self.assertEqual(len(hit(ok, "nvme-behind-sas-raid")), 0)

    def test_controller_ports_vs_bays(self):
        sas = L("C4DA", '3.5" 12TB 7.2K SAS HDD', 12)
        self.assertEqual(len(hit(run([sas, L("C0TU", "ThinkSystem RAID 545-8i Adapter")]), "controller-ports-vs-bays")), 1)
        self.assertEqual(len(hit(run([sas, L("B8NZ", "ThinkSystem RAID 940-16i Adapter")]), "controller-ports-vs-bays")), 0)
        self.assertEqual(len(hit(run([L("C3Q9", "3.84TB NVMe SSD", 9)]), "controller-ports-vs-bays")), 0)

    def test_boot_mirror_single_drive(self):
        kit = L("CCCZ", "ThinkSystem M.2 RAID B550p-2HS SATA/NVMe Enablement Kit")
        one = L("C286", "ThinkSystem M.2 VA 480GB Read Intensive NVMe NHS SSD", 1)
        f = hit(run([kit, one]), "boot-mirror")
        self.assertEqual(len(f), 1); self.assertIn("Single M.2 boot drive", f[0]["message"])

    def test_boot_mirror_pair_ok_and_heatsink_ignored(self):
        kit = L("CCCZ", "ThinkSystem M.2 RAID B550p-2HS SATA/NVMe Enablement Kit")
        two = L("C286", "ThinkSystem M.2 VA 480GB Read Intensive NVMe NHS SSD", 2)
        hs = L("C2RD", "ThinkSystem Hot Swap M.2 2280 SSD HeatSink", 2)
        self.assertEqual(hit(run([kit, two, hs]), "boot-mirror"), [])

    def test_boot_mirror_cluster_total_hint(self):
        f = hit(run([L("C286", "ThinkSystem M.2 VA 480GB Read Intensive NVMe NHS SSD", 6)]), "boot-mirror")
        self.assertIn("cluster total", f[0]["message"])

    def test_m2_kit_without_drives(self):
        kit = L("CCCZ", "ThinkSystem M.2 RAID B550p-2HS SATA/NVMe Enablement Kit")
        self.assertEqual(len(hit(run([kit]), "m2-kit-without-drives")), 1)

    def test_backplane_presence(self):
        self.assertEqual(len(hit(run([L("C3Q9", "ThinkAgile HX 3.84TB NVMe SSD", 9)]), "backplane-presence")), 1)
        ok = [L("C3Q9", "3.84TB NVMe SSD", 9), L("C46P", 'ThinkSystem 2U V4 8x2.5" NVMe Backplane', 1)]
        self.assertEqual(len(hit(run(ok), "backplane-presence")), 0)

    def test_drives_vs_backplane_bays(self):
        drives = L("C3Q9", '2.5" 3.84TB NVMe SSD', 10)
        bp8 = L("C46P", 'ThinkSystem 2U V4 8x2.5" NVMe Backplane', 1)
        self.assertEqual(len(hit(run([drives, bp8]), "drives-vs-backplane-bays")), 1)
        bp2 = L("C46Q", 'ThinkSystem 2U V4 8x2.5" NVMe Backplane', 2)
        self.assertEqual(len(hit(run([drives, bp2]), "drives-vs-backplane-bays")), 0)
        mixed = L("C3RV", 'ThinkSystem 2U V4 8x3.5" SAS/SATA+4x 3.5" AnyBay Backplane', 1)   # 12 bays
        self.assertEqual(len(hit(run([L("C4DA", '3.5" 12TB SAS HDD', 12), mixed]), "drives-vs-backplane-bays")), 0)
        self.assertEqual(rules.bp_bays('ThinkSystem 4x2.5" NVMe Backplane with 4x2.5" Chassis'), 4)

    def test_35in_drives_on_25in_platform(self):
        hdd = L("C4DA", '3.5" 12TB 7.2K SAS HDD', 4)
        self.assertEqual(len(hit(run([hdd], mtm="7DG9CTO1WW"), "35in-drives-on-25in-platform")), 1)
        self.assertEqual(len(hit(run([hdd], mtm="7DGDCTO1WW"), "35in-drives-on-25in-platform")), 0)  # SR650 V4 has 3.5"


class Compute(unittest.TestCase):
    SR630V4 = dict(mtm="7DG9CTO1WW")

    def test_cpu_sockets_max(self):
        self.assertEqual(len(hit(run([L("C5QV", "Intel Xeon 6517P Processor", 3)], **self.SR630V4), "cpu-sockets-max")), 1)
        self.assertEqual(len(hit(run([CPU], **self.SR630V4), "cpu-sockets-max")), 0)
        self.assertEqual(len(hit(run([L("X", "AMD EPYC 9354 32C Processor", 2)], mtm="7D9GCTO1WW"), "cpu-sockets-max")), 1)  # SR635 V3 is 1S

    def test_cpu_sockets_min(self):
        one = L("X", "Intel Xeon Gold 6430 Processor", 1)
        self.assertEqual(len(hit(run([one], mtm="7D93CTO1WW"), "cpu-sockets-min")), 1)  # SR860 V3 needs 2
        self.assertEqual(len(hit(run([one], **self.SR630V4), "cpu-sockets-min")), 0)

    def test_hci_min_cpus_only_fires_when_guide_says_more_than_socket_min(self):
        one = L("C5QV", "Intel Xeon 6517P Processor", 1)
        self.assertEqual(hit(run([one], mtm="7DG5CTO1WW"), "hci-min-cpus"), [])       # VX630 V4: min 1
        self.assertEqual(hit(run([one], **HX), "hci-min-cpus"), [])                    # HX650 V4: guide says 1 or 2

    def test_heatsink_cpu_pairing(self):
        hs = lambda q: L("C3QR", "ThinkSystem 2U V4 Performance Heatsink", q)
        self.assertEqual(len(hit(run([CPU, hs(1)]), "heatsink-cpu-pairing")), 1)
        self.assertEqual(len(hit(run([CPU, hs(2)]), "heatsink-cpu-pairing")), 0)

    def test_dimm_slots_exceeded(self):
        self.assertEqual(len(hit(run([CPU, L("C0TQ", "64GB TruDDR5 RDIMM", 34)], **self.SR630V4), "dimm-slots-exceeded")), 1)
        self.assertEqual(len(hit(run([CPU, DIMM], **self.SR630V4), "dimm-slots-exceeded")), 0)

    def test_dimm_slots_exceeded_per_populated_socket(self):
        one = L("C5QV", "Intel Xeon 6517P Processor", 1)
        self.assertEqual(len(hit(run([one, L("C0TQ", "64GB TruDDR5 RDIMM", 20)], **self.SR630V4), "dimm-slots-exceeded")), 1)

    def test_dimm_cpu_balance(self):
        self.assertEqual(len(hit(run([CPU, L("C0TQ", "64GB TruDDR5 RDIMM", 7)]), "dimm-cpu-balance")), 1)
        self.assertEqual(len(hit(run([CPU, DIMM]), "dimm-cpu-balance")), 0)

    def test_winserver_16core(self):
        self.assertEqual(len(hit(run([L("X", "Windows Server 2025 Standard 8-Core License")]), "winserver-16core-min")), 1)
        self.assertEqual(len(hit(run([L("X", "Windows Server 2025 Standard 16-Core License")]), "winserver-16core-min")), 0)


class Power(unittest.TestCase):
    BLKH = L("BLKH", "ThinkSystem 1100W 230V Titanium Hot-Swap Gen2 Power Supply", 2)
    BNFH = L("BNFH", "ThinkSystem 1100W 230V/115V Platinum Hot-Swap Gen2 Power Supply v3", 2)
    C07V = L("C07V", "ThinkSystem 750W 230V Titanium Hot-Swap Gen2 Power Supply v4", 2)
    CCTL = L("CCTL", "ThinkSystem 1100W -48V DC Hot-Swap Gen2 Power Supply v2", 2)
    AX8A = L("AX8A", "4.3m, 13A/120V, C13 to NEMA 5-15P (US) Line Cord", 2)
    C6313 = L("6313", "2.8m, 10A/120V, C13 to NEMA 5-15P (US) Line Cord", 2)
    C6370 = L("6370", "4.3m, 10A/125V, C13 to NEMA 5-15P (US) Line Cord", 2)
    C6373 = L("6373", "4.3m, 10A/250V, C13 to NEMA 6-15P (US) Line Cord", 2)
    JUMPER = L("6400", "2.8m, 13A/100-250V, C13 to C14 Jumper Cord", 2)
    RACKC20 = L("6204", "2.8m, 10A/100-250V, C13 to IEC 320-C20 Rack Power Cable", 2)

    def test_230v_only_psu_on_120v_cord_fails_and_names_fix(self):
        f = hit(run([self.BLKH, self.AX8A]), "psu-cord-voltage")
        self.assertEqual(len(f), 1)
        for s in ("BLKH", "AX8A", "BNFH", "will not power on"): self.assertIn(s, f[0]["message"])

    def test_every_120v_cord_fails_and_750w_names_bnfg(self):
        for cord in (self.AX8A, self.C6313, self.C6370):
            self.assertEqual(len(hit(run([self.BLKH, cord]), "psu-cord-voltage")), 1, cord["fc"])
        self.assertIn("BNFG", hit(run([self.C07V, self.AX8A]), "psu-cord-voltage")[0]["message"])

    def test_mixed_mode_psu_and_250v_cords_pass(self):
        self.assertEqual(hit(run([self.BNFH, self.AX8A]), "psu-cord-voltage"), [])
        self.assertEqual(hit(run([self.BLKH, self.C6373]), "psu-cord-voltage"), [])

    def test_rack_jumpers_and_dc_supplies_never_fire(self):
        self.assertEqual(hit(run([self.BLKH, self.JUMPER]), "psu-cord-voltage"), [])
        self.assertEqual(hit(run([self.BLKH, self.RACKC20]), "psu-cord-voltage"), [])
        self.assertEqual(hit(run([self.CCTL, self.AX8A]), "psu-cord-voltage"), [])

    def test_needs_both_psu_and_cord(self):
        self.assertEqual(hit(run([self.BLKH]), "psu-cord-voltage"), [])
        self.assertEqual(hit(run([self.AX8A]), "psu-cord-voltage"), [])

    def test_site_voltage_warning_only_for_230v_only_plus_agnostic_jumpers(self):
        self.assertEqual(len(hit(run([self.BLKH, self.JUMPER]), "psu-high-line-site-check")), 1)
        self.assertEqual(hit(run([self.BLKH, self.C6373]), "psu-high-line-site-check"), [])
        self.assertEqual(hit(run([self.BLKH, self.AX8A]), "psu-high-line-site-check"), [])
        self.assertEqual(hit(run([self.BNFH, self.JUMPER]), "psu-high-line-site-check"), [])

    def test_d4390_pdu_gate(self):
        d = L("7DAH", "ThinkSystem D4390 JBOD")
        self.assertEqual(len(hit(run([d, L("X", "v1 0U 60A delta PDU", 2)]), "d4390-pdu-gate")), 1)
        cur = L("C0D5", "0U 36 C13/C15 and 12 C13/C15/C19/C21 Switched and Monitored 60A PDU", 2)
        self.assertEqual(hit(run([d, cur]), "d4390-pdu-gate"), [])


class Ocp(unittest.TestCase):
    V4 = dict(family="ThinkSystem SR650 V4", mtm="7DGDCTO1WW")
    P4 = L("BPPW", "ThinkSystem Broadcom 57504 10/25GbE SFP28 4-Port OCP Ethernet Adapter")

    def test_v4_four_port_ocp_without_kit_warns(self):
        self.assertEqual(len(hit(run([self.P4], **self.V4), "ocp-x16-upgrade")), 1)

    def test_never_fires_on_v3_or_two_port_or_with_kit(self):
        self.assertEqual(hit(run([self.P4], family="ThinkSystem SR635 V3", mtm="7D9GCTO1WW"), "ocp-x16-upgrade"), [])
        self.assertEqual(hit(run([L("BN2T", "Broadcom 57414 10/25GbE SFP28 2-Port OCP Ethernet Adapter")], **self.V4), "ocp-x16-upgrade"), [])
        kit = L("C1YK", "ThinkSystem SR650 V4/SR630 V4 x16 OCP Cable Kit")
        self.assertEqual(hit(run([self.P4, kit], **self.V4), "ocp-x16-upgrade"), [])


class Hygiene(unittest.TestCase):
    def test_completeness_flags_missing_power_and_memory(self):
        fs = run([CPU, L("X", "3.84TB NVMe SSD", 4), L("Y", "Ethernet Adapter", 1), L("Z", "filler", 1)])
        f = hit(fs, "config-completeness")
        self.assertEqual(len(f), 1); self.assertIn("no memory", f[0]["message"]); self.assertIn("power supply", f[0]["message"])

    def test_completeness_passes_full_node_and_flags_lone_psu(self):
        self.assertEqual(hit(run([CPU, DIMM, PSU, L("Z", "filler", 1)]), "config-completeness"), [])
        one = hit(run([CPU, DIMM, L("C2Y9", "1300W Titanium Power Supply", 1), L("Z", "f", 1)]), "config-completeness")
        self.assertTrue(any("Only 1 power supply" in f["message"] for f in one))

    def test_completeness_counts_udimm(self):
        udimm = L("C527", "ThinkSystem 16GB TruDDR5 4800MHz (1Rx8) UDIMM", 2)
        self.assertEqual(hit(run([CPU, udimm, PSU, L("Z", "filler", 1)]), "config-completeness"), [])

    def test_placeholder_junk(self):
        fs = run([L("Lenovo-SSD-NONE", "Do not quote this SKU. No SSD Included"), L("C-GPU-NONE_Lenovo", "Do not quote this SKU. No GPU"), CPU])
        f = hit(fs, "placeholder-junk")
        self.assertEqual(len(f), 1); self.assertIn("LENOVO-SSD-NONE", f[0]["message"])

    def test_no_publications_selected_is_not_junk(self):
        self.assertEqual(hit(run([L("8086", "No Publications Selected")]), "placeholder-junk"), [])

    def test_duplicate_codes_hardware_only(self):
        hw = run([L("C3Q9", "3.84TB NVMe SSD", 4), L("C3Q9", "3.84TB NVMe SSD", 4)])
        self.assertEqual(len(hit(hw, "duplicate-codes")), 1)
        svc = run([L("QA0Y", "Months", 60), L("QA0Y", "Months", 60)])
        self.assertEqual(hit(svc, "duplicate-codes"), [])
        self.assertEqual(hit(run([L("X", "a", 1), L("Y", "b", 1)]), "duplicate-codes"), [])

    def test_platform_unresolved_info(self):
        self.assertEqual(len(hit(run([CPU]), "platform-unresolved")), 1)
        self.assertEqual(hit(run([CPU], mtm="7DG9CTO1WW"), "platform-unresolved"), [])

    def test_bom_load_note_surfaces_loader_notes(self):
        b = rules.parse_text("2 x C5QV Intel Xeon 6517P Processor\nsome prose line\n")
        self.assertEqual(len(hit(run(b), "bom-load-note")), 1)

    def test_a_crashing_rule_is_reported_not_swallowed(self):
        rules.RULES.append(dict(id="_boom", severity="block", applies=lambda c: True, fn=lambda c: 1 / 0, doc=""))
        try:
            f = hit(run([CPU]), "_boom")
        finally:
            rules.RULES.pop()
        self.assertEqual(len(f), 1); self.assertIn("unchecked", f[0]["message"]); self.assertEqual(f[0]["severity"], "warn")


class Helpers(unittest.TestCase):
    def test_to_tb_converts_only_tagged_tib(self):
        self.assertEqual(rules.to_tb(12, "TB"), 12)
        self.assertAlmostEqual(rules.to_tb(21, "TiB"), 23.0897, places=3)
        self.assertAlmostEqual(rules.to_tb(1000, "GB"), 1.0)
        with self.assertRaises(ValueError): rules.to_tb(12, "")

    def test_fixups_drop_junk_merge_dupes_mirror_boot(self):
        lines, notes = rules.apply_fixups([
            L("C5RD", "Intel Xeon 6515P 16C 150W 2.3GHz Processor", 2),
            L("CCCZ", "ThinkSystem M.2 RAID B550p-2HS SATA/NVMe Enablement Kit"),
            L("C286", "ThinkSystem M.2 VA 480GB Read Intensive NVMe NHS SSD", 1),
            L("Lenovo-SSD-NONE", "Do not quote this SKU. No SSD Included"),
            L("C-GPU-NONE_Lenovo", "Do not quote this SKU. No GPU"),
            L("C-GPU-NONE_Lenovo", "Do not quote this SKU. No GPU")])
        self.assertFalse(any("Do not quote" in l["descr"] for l in lines))
        self.assertEqual({l["fc"]: l["qty"] for l in lines}["C286"], 2)
        self.assertEqual((len(lines), len(notes)), (3, 2))

    def test_fixups_leave_correct_config_alone_and_merge_real_dupes(self):
        src = [L("CCCZ", "ThinkSystem M.2 RAID B550p-2HS Enablement Kit"), L("C287", "ThinkSystem M.2 VA 960GB Read Intensive NVMe NHS SSD", 2)]
        lines, notes = rules.apply_fixups(src)
        self.assertEqual((lines[1]["qty"], notes), (2, []))
        merged, _ = rules.apply_fixups([L("C0TQ", "64GB RDIMM", 4), L("C0TQ", "64GB RDIMM", 4)])
        self.assertEqual((len(merged), merged[0]["qty"]), (1, 8))

    def test_diff_clean_tolerates_derived_lines(self):
        intent = [L("C5QV", "Intel Xeon 6517P 16C Processor", 2), L("C0TQ", "64GB RDIMM", 8), L("C3Q9", "3.84TB NVMe SSD", 2)]
        rows = [L("C5QV", "cpu", 6), L("C0TQ", "dimm", 24), L("C3Q9", "ssd", 6),
                L("AVJ3", 'ThinkSystem 1x1 3.5" HDD Filler', 24), L("BU1E", "Lenovo Top Choice Express Flag", 3)]
        d = rules.diff_boms([rules.norm_line(x) for x in intent], [rules.norm_line(x) for x in rows], 3)
        self.assertEqual(d["verdict"], "CLEAN"); self.assertTrue(d["tce_flag_present"]); self.assertGreaterEqual(d["derived_count"], 1)

    def test_diff_drift_on_missing_qty_and_wrong_part(self):
        intent = [L("C5QV", "cpu", 2), L("C0TQ", "dimm", 8), L("C3Q9", "3.84TB NVMe SSD", 2)]
        rows = [L("C5QV", "cpu", 6), L("C0TQ", "dimm", 12), L("C1X9", "7.68TB NVMe SSD", 6)]
        d = rules.diff_boms([rules.norm_line(x) for x in intent], [rules.norm_line(x) for x in rows], 3)
        self.assertEqual((d["verdict"], len(d["missing"]), len(d["unexpected"]), len(d["qty_drift"])), ("DRIFT", 1, 1, 1))


class Cli(unittest.TestCase):
    def _run(self, text, *args):
        import io, contextlib
        fd, p = tempfile.mkstemp(suffix=".txt"); os.close(fd)
        with open(p, "w", encoding="utf-8") as f: f.write(text)
        buf = io.StringIO()
        try:
            with contextlib.redirect_stdout(buf):
                code = rules.main(["check", p, *args])
        finally:
            os.remove(p)
        return code, buf.getvalue()

    def test_exit_1_on_block_and_groups_by_severity(self):
        code, out = self._run("2 x BLKH ThinkSystem 1100W 230V Titanium Hot-Swap Gen2 Power Supply\n2 x AX8A 4.3m, 13A/120V, C13 to NEMA 5-15P (US) Line Cord\n")
        self.assertEqual(code, 1); self.assertIn("== BLOCK", out); self.assertIn("[psu-cord-voltage]", out)

    def test_exit_0_when_no_block(self):
        code, out = self._run("2 x C5QV Intel Xeon 6517P 16C Processor\n8 x C0TQ 64GB TruDDR5 6400MHz (2Rx4) RDIMM\n2 x C2Y9 ThinkSystem 1300W Titanium CRPS Hot-Swap Power Supply\n1 x C286 filler\n",
                              "--mtm", "7DG9CTO1WW")
        self.assertEqual(code, 0, out)

    def test_list_and_bad_args(self):
        import io, contextlib
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            self.assertEqual(rules.main(["list"]), 0)
        self.assertIn("psu-cord-voltage", buf.getvalue())
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(rules.main(["check"]), 2)


class Specs(unittest.TestCase):
    def test_sixteen_platforms_with_source_and_as_of(self):
        ps = specs.platforms()
        self.assertEqual(len(ps), 16)
        for p in ps:
            self.assertRegex(p["source"], r"^lp\d{4}$"); self.assertRegex(p["as_of"], r"^\d{4}-\d{2}$")

    def test_no_forbidden_fields(self):
        with open(specs.DATA, encoding="utf-8") as f:
            blob = f.read().lower()
        for bad in ("price", "$", "catalog" + ".json", "derived", "cra" + "wl"):
            self.assertNotIn(bad, blob)

    def test_find_by_fuzzy_name_and_mtm(self):
        self.assertEqual(specs.find("sr630 v4")[0]["name"], "ThinkSystem SR630 V4")
        self.assertEqual(specs.find("7DG9CTO1WW")[0]["name"], "ThinkSystem SR630 V4")
        self.assertEqual(specs.find("HX650 V4 Storage")[0]["name"], "ThinkAgile HX650 V4")
        self.assertEqual(specs.find("sr630 v44")[0]["name"], "ThinkSystem SR630 V4")    # typo, closest match first
        self.assertEqual(specs.find("nonsense"), [])

    def test_shared_machine_type_is_ambiguous_for_resolve(self):
        self.assertEqual(len(specs.find("7DGD")), 2)
        self.assertIsNone(specs.resolve(mtm="7DGD"))
        self.assertEqual(specs.resolve(mtm="7DGDCTO2WW")["name"], "ThinkSystem SR650a V4")

    def test_cli(self):
        import io, contextlib
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            self.assertEqual(specs.main(["spec", "sr630", "v4"]), 0)
            self.assertEqual(specs.main(["spec", "--list"]), 0)
        self.assertIn("lp1971", buf.getvalue())
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(specs.main(["spec", "zzzz"]), 1)


class Coverage(unittest.TestCase):
    def test_every_rule_id_is_named_in_this_file(self):
        with open(__file__, encoding="utf-8") as f:
            src = f.read()
        missing = [r["id"] for r in rules.RULES if f'"{r["id"]}"' not in src and r["id"] != "_boom"]
        self.assertEqual(missing, [])


if __name__ == "__main__":
    unittest.main()
