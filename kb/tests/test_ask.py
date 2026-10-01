import contextlib, io, os, sys, unittest

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, HERE)
import ask


def run(q, *extra):
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        rc = ask.main([q, *extra])
    return rc, buf.getvalue()


class Entities(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rc = ask.cache()

    def test_model_fc_and_keywords(self):
        m, fcs, words, labels = ask.entities("why does 4x B2PB 3m LC-LC OM4 error on the SR635 V3?", self.rc, None, None)
        self.assertIn("7D9GCTO1WW", [x[0] for x in m])
        self.assertEqual(fcs, ["B2PB"])
        self.assertIn("OM4", words)
        self.assertIn("3m", words)

    def test_acronyms_are_not_feature_codes(self):
        _, fcs, _, _ = ask.entities("is RAID TCE on the SR630 V4 with NVME", self.rc, None, None)
        self.assertEqual(fcs, [])

    def test_sizes_survive_as_keywords(self):
        _, _, words, _ = ask.entities("is the 16GB DIMM TCE on HX650 V4?", self.rc, None, None)
        self.assertIn("16GB", words)


class Router(unittest.TestCase):
    def test_intents(self):
        r = lambda q: ask.route(q, [], [])
        self.assertIn("aix", r("what are the AI Express options on the SR675 V3?"))
        self.assertIn("error", r("why does it give me an error when I add B2PB"))
        self.assertIn("price", r("how much is C0TQ?"))
        self.assertIn("lifecycle", r("is the SR650 V3 still available?"))
        self.assertIn("compete", r("Dell R760 equivalent?"))
        self.assertIn("spec", r("how many drive bays does the SR635 V3 have?"))
        self.assertEqual(r("what is the difference between iSCSI and SAS?"), ["concept"])
        self.assertNotIn("compete", r("is C287 TCE on the SR675 V3?"))

    def test_brief_reports_route_gaps_next(self):
        _, out = run("why does it give me an error when i add B2PB to the SR635 V3?")
        self.assertIn("ROUTE: error", out)
        self.assertIn("paste it", out)
        self.assertIn("NEXT: ask the user first", out)

    def test_ai_express_swaps_to_the_ai_cto(self):
        _, out = run("what are the AI Express options on the SR675 V3?")
        if "tce=Y/AIX" not in out:
            self.skipTest("snapshot predates the tceAudience field")
        self.assertIn("7D9RCTO1WW", out)


class Brief(unittest.TestCase):
    def test_fc_rules_on_the_named_model(self):
        rc, out = run("is B2PB TCE on the SR635 V3?")
        self.assertEqual(rc, 0)
        self.assertIn("B2PB on 7D9GCTO1WW", out)
        self.assertIn("EXTERNAL_CABLES", out)

    def test_synonyms_reach_dcsc_vocabulary(self):
        _, out = run("which 16GB DIMM can the HX650 V4 take?")
        self.assertRegex(out, r"RDIMM")

    def test_external_hba_found_by_section_name(self):
        _, out = run("which SAS adapter does the SR635 V3 need for external storage?")
        self.assertIn("440-16e", out)


if __name__ == "__main__":
    unittest.main()
