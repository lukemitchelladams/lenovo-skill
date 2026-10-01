# Platform, TCE, licensing and support rules for the /lenovo skill. Loaded by kb_facts.py.
# Same schema as kb_facts.py.
# Tuple order: topic, scope, status, title, body, source, verified
# status: proven | flagged | unknown
#
# All customer, partner and person names, quote numbers and prices have been removed.
# Price insights are kept only as ratios or directions. TCE membership ROTATES per MTM
# and per date: every TCE statement below carries its date, treat it as a lead to
# re-check on the live DCSC panel (feature code BU1E present in the built config), not
# as proof for today.

FACTS = [

("dcsc-crawl-2026-09-30-tce-changes",
 "SR630 V4|SR650 V4|SR650a V4|HX630 V4|HX650 V4|HX650 V4 Storage|FX630 V4|SR635 V3|SR645 V3|SR655 V3|SR665 V3|SR250 V3|ST250 V3|ST50 V3", "proven",
 "DCSC rules crawl 2026-09-30 vs 2026-07-28: Intel V4 16C TCE is now C5R5 6724P only, 940-16i adapters B8NZ/BM35 became TCE, EPYC 9535/9135 became TCE, BYLV 7.68TB SATA and C4D6 20TB SAS dropped out",
 "Per-section Top Choice flags in the DCSC static catalogue, compared between the two crawls (880 TCE gains, 95 losses, 9,213 options added, 894 removed across 225 live MTMs). "
 "INTEL V4: C5RD 6515P and C5QV 6517P lost TCE on SR630 V4, SR650 V4 and SR650a V4, and C5QQ 6505P 12C lost it everywhere, so the only TCE 16-core Xeon on those three is C5R5 6724P (matches the live panels of 2026-09-23). "
 "On HX630 V4 and HX650 V4 C5RD lost TCE while C5R6 6507P 8C gained it; FX630 V4 gained C5R7, C5R6 and C5R4. "
 "CONTROLLERS: the 940-16i PCIe adapters B8NZ (8GB) and BM35 (4GB) became TCE on SR630 V4, SR650 V4, SR650a V4 and the AMD V3 1U/2U servers. This may reopen a TCE path for 12x 3.5in on SR650 V4 (C3RW + a 16i), which the July evidence ruled out; build it and check BU1E before promising it. C3RV 8x3.5 SAS/SATA + 4x3.5 AnyBay lost TCE on SR650 V4. "
 "AMD V3: C2AL EPYC 9535 64C 300W and C2AK EPYC 9135 16C 200W became TCE on SR635/645/655/665 V3. "
 "DRIVES: BYLV 2.5in 7.68TB RI SATA lost TCE on most platforms and C4D6 3.5in 20TB SAS lost it on AMD V3, SR650 V4 and the entry servers; BYLZ 3.5in 1.92TB RI SATA gained it. "
 "ENTRY: C521 6333P 6C lost TCE on SR250 V3, ST250 V3 and ST50 V3 (matches the live panels), BMFT 540-8i gained it. "
 "GPU: CHWT RTX PRO 6000 Server Edition 96GB and CHWU GPU-Ready became TCE on SR650a V4. HX650 V4 Storage gained 231 TCE options (the whole model joined the program). "
 "The catalogue flag is per section and is a snapshot; the live panel and a BU1E export remain the proof.",
 "DCSC static and launch rules crawls 2026-07-28 and 2026-09-30", "2026-09-30"),

("dcsc-retired-ctos-2026-09-30",
 "HX630 V3|HX650 V3|MX630 V3|MX650 V3|VX630 V3|VX650 V3|ST650 V3|SR685a V3|D1224|Scale Computing|Cornelis", "proven",
 "43 CTOs no longer open in DCSC as of 2026-09-30: every ThinkAgile V3 (HX630/650 V3 incl. ROBO and Storage, MX630/650 V3, VX630/650 V3), ST650 V3, SR685a V3, D1224 and the Scale Computing V3/SE100 variants",
 "On the 2026-09-30 crawl DCSC answered 'Not found CTO with code ...' when opening a configuration for these, with every solution-mode and slice setting tried, and they are gone from the product menus; a live check in the DCSC UI confirmed HX650 V3 is gone. "
 "ThinkAgile HX630 V3 (7D6M: IS, CN, ROBO IS/CN, SAP HANA, for AI), HX650 V3 (7D6N: IS, CN, Storage IS/CN, SAP HANA, for AI), MX650 V3 (7D6S) and MX650 V3 PR (7DKB), MX630 V3 (7D6U), VX650 V3 (7D6W), VX630 V3 (7D6X); "
 "ST650 V3 (7D7A); SR685a V3 for AI (7DHCCTO1WW); D1224 SFF JBOD (4587HC2); Scale Computing Platform SR630 V3 (7D73CTO3WW) and SR650 V3 (7D76CTO5WW); Scale Computing SE100 (7DGRCTO2WW) and its 1U2N/1U3N enclosures (7DGV CTO3/CTO4); one Cornelis CN5000 switch variant (7DMQCTO4WW). "
 "The plain ThinkSystem SR630 V3 and SR650 V3 CTOs are still live. So a V3 ThinkAgile refresh or add-node request now maps to V4 (HX630 V4, HX650 V4, HX650 V4 Storage), and a mixed-generation Nutanix cluster expansion must use V4 nodes. "
 "An older Lenovo Press page that still shows these as available is stale on orderability. List them with: kb.py models --retired.",
 "DCSC launch endpoint and product menus 2026-09-30; DCSC UI check 2026-09-30", "2026-09-30"),

("amd-v3-cpu-generation-dictates-dimm-speed",
 "SR645 V3|SR665 V3|SR635 V3|SR655 V3|AMD EPYC 9004|AMD EPYC 9005", "proven",
 "AMD V3: EPYC 9004 Genoa pairs ONLY with 4800MHz DIMMs and EPYC 9005 Turin ONLY with 6400MHz; the DIMM speed picks the CPU generation",
 "Across all 48 AMD V3 configs in the source corpus (SR645 V3, SR665 V3, SR635 V3, SR655 V3) there are zero exceptions. "
 "Genoa 9004 CPUs (BREE 9124 16C, BREC 9334 32C, BPVJ 9554 64C, BPVK 9654, BR31 9474F) carry 4800MHz DIMMs BQ37 or BQ3D. "
 "Turin 9005 CPUs (C2AQ 9335 32C, C2AL 9535 64C, C2AN 9645, C2AU 9655, C2AX 9655P) carry 6400MHz DIMMs CBNC, CBNB, CBND, CBN9, CBFR or CA1N. "
 "So the memory choice drives the CPU generation, not the other way round: a spec that needs DDR5-6400 rules out every 9004 part regardless of core count. "
 "DCSC shows no gating message for a mismatched pair in the exports, the evidence is the co-occurrence pattern, so check the pairing by hand every time. "
 "Two structural parts follow the CPU generation and DCSC auto-pulls them on SR645 V3 (7D9CCTO1WW): board BQ2A (Genoa) becomes C2BD 'SR645 V3 MB W/IO, Turin', and RoT module BQ2P becomes C257 'Absolut-RoW RoT Module for Turin MLK'. "
 "Both Turin parts are BU1E-proven on that MTM; they are structural auto-adds, so their absence from a part-level catalog listing means nothing. "
 "Rank matters when matching a competitor line: CBNC 32GB 6400 is 2Rx8 dual rank and CBNB is 1Rx4 single rank, priced identically but not interchangeable. "
 "A competitor quote for '32GB RDIMM 6400 dual rank' maps to CBNC. "
 "COMPETITIVE: a Dell or HPE configuration that pairs 6400MT/s RDIMMs with an EPYC 9004 part is selling memory the CPU cannot run; those DIMMs clock down to 4800. "
 "The configurator may allow it, the silicon does not honour it. Related topic: tce-ceilings-amd-v3-vs-intel-v4-and-catalog-flag-corrections.",
 "DCSC exports (48 AMD V3 configs); DCSC auto-add behaviour on 7D9CCTO1WW", "2026-09-03"),

("d4390-blocked-with-0u-60a-delta-pdu-in-7d6e-rack",
 "D4390|7DAHCTO1WW|7D6E rack|Lenovo PDUs", "proven",
 "DCSC blocks the D4390 JBOD (BT4J) inside a 7D6E rack CTO when the 0U 60A 3-phase Delta PDU C0D5 is selected; it is a validation-matrix gate, not a hardware limit",
 "The DCSC rack-CTO error reads 'BT4J is not allowed when 7DAHCTO1WW is placed in 7D6ECTO1WW ... PDU (C0D5)'. "
 "7DAH is the ThinkSystem D4390 high-density SAS JBOD, and BT4J is its component feature code inside rack CTOs (a rack cross-reference, not a cable). Two CTO flavours exist: 7DAHCTO1WW General Purpose and 7DAHCTOLWW HPC and AI. "
 "7D6E is the ThinkSystem 48U Onyx/Pearl Heavy Duty Rack Cabinet, which has General Purpose and HPC and AI hardware modes. "
 "C0D5 is the 0U 21 C13/C15 + 21 C13/C15/C19 Switched and Monitored 60A 3-Phase Delta PDU, generation v1 (option PN 4PU7A93174; the v2 is 4PU7A93181). "
 "D4390 power: 4x 1300W 80PLUS Titanium PSUs (feature code BTLH, auto-derived) with C14 inlets, so it needs 4 C13-C14 jumpers (FC 6400 2.8m 13A). Redundancy is N+N at 200-240V and N+1 at 110V. "
 "Every C0D5 outlet accepts a C14 and Lenovo Press LP1681's PDU table lists both v1 and v2, so the block is purely DCSC's validation matrix on the v1 feature code. "
 "DCSC QUIRK: it keeps the SAME feature code across PDU generations and revs only the part number under it (for example 4PU7A93182, a v2, shows as C0CS, the v1 feature code), so 'just pick C0QN' is not possible because C0QN never appears in the picker. "
 "FIX ORDER from the 7D6E PDU picker: (1) C0DB 1U 12 C19/C13 S&M 60A 3P Delta PDU V2 (4PU7A90812), which has the identical IEC 60309 460P9 60A input plug and 17.2kW as C0D5 but only 12 outlets per PDU; "
 "(2) C0DD 1U 18 C19/C13 S&M 80A 3P Delta V2 (4PU7A90810, 23kW), but its input is IEC 60309 3P+E 100A, which needs different site whips; "
 "(3) the gate is scoped to the rack, so keeping C0D5 means moving every D4390 into racks or configs that do not carry C0D5. "
 "OUTLET MATH template (dual source, one PDU per feed): a D4390 with 4 PSUs uses 2 cords per feed and a 2-PSU server uses 1 cord per feed. 4 JBODs plus 4 servers is exactly 12 outlets per feed, so C0DB qty 2 fits with zero spare and any extra switch tips it to C0DD qty 2 or C0DB qty 4.",
 "DCSC rack-CTO error message and live PDU picker 2026-07-29; Lenovo Press LP1681 PDU table", "2026-07-29"),

("dcsc-supply-status-column-vs-tce-badge",
 "ALL", "flagged",
 "DCSC Supply Status is a separate column from the TCE badge; treat an X as a lead-time warning and confirm with the distributor whether it means unbuyable",
 "TWO READINGS FROM LIVE PANELS DISAGREE. (a) 2026-07-29 PDU picker: the Supply Status column shows green for fast ship and X for a longer lead, and X was NOT withdrawn or unorderable. "
 "(b) 2026-09-02 optics panel: BYBJ (Finisar 10G/25G SR SFP28) carried the Top Choice Express badge but supply status X, while BF10 (4TC7A69045, the same class of part) showed G, so the cheapest TCE-badged part looked unbuyable; "
 "likewise the 400GbE QSFP112 optic CFUD showed X and the 200G optic BQJZ showed G. An export-derived list showed BYBJ as non-TCE on 7DGDCTO2WW while the live panel badged it TCE, so exports and the panel can disagree on the badge too. "
 "WORKING RULE: a TCE badge is not a supply status and a supply status is not a TCE flag. Read both columns. Treat X as 'longer lead, possibly constrained' and confirm with the distributor before either promising the part or dismissing it. "
 "Whether X ever means truly unorderable is UNCONFIRMED.",
 "DCSC panels 2026-07-29 and 2026-09-02", "2026-09-02"),

("export-price-aggregation-and-scraped-price-traps",
 "ALL", "proven",
 "Scraped street prices are exact on structural parts but far too low on DIMMs and drives, and aggregating export prices by feature code with MAX picks up rolled-up whole-server prices",
 "TRAP 1, scraped or stored street-price lists. Measured 2026-09 against real DCSC list prices: structural and low-value parts matched to the cent (chassis, board, CPU, backplane, HBA, NIC, PSU, risers, fans, rails, XCC upgrade, Premier service). "
 "Memory and hot-swap drives did not: the real DCSC list was about 1.8x the scraped figure on the 32GB TruDDR5 6400 2Rx8 RDIMM (CBNC), about 1.4x on a 960GB read-intensive SATA SSD (BYLS), about 1.2x on a 2.4TB 10K SAS HDD (BRG7). "
 "Because memory is usually the largest single line, a whole-config estimate built from the scraped list came in about 32 percent under the real export total and inverted a competitive headline: it showed Lenovo roughly 19 percent under the competitor's net when at list it was roughly 19 percent over. "
 "RULE: use a scraped list for structure and for relative deltas between two CPUs or two NICs only. Never publish a config total from it and never price memory from it. "
 "A number that goes in front of a customer comes from a built and exported DCSC config: sum of qty x unit. If a figure must be given before the export exists, label it indicative, structure only, and do not compute a competitive delta from it. "
 "TRAP 2, aggregating unit price by feature code across exports. MAX(unit) is contaminated by rolled-up CTO rows that carry a whole-server price from the Summary sheet. Observed spreads on identical feature codes: C5RD 6515P about 2.1x, C286 M.2 480GB about 2.9x, C527 16GB UDIMM about 3.4x between exports. "
 "Rolled-up CTO SKUs (for example 7DGDCTO1WW, 7S0XCTO*, 7S1SCTO*) hold whole-server totals as their line price, and one such row inflated a spec-sheet total roughly 4x. "
 "Use MIN(unit), force roll-up SKUs to nominal, and sanity-check any computed total by repricing a known validated export: the fix was proven when a repriced export landed within a few dollars of its real total. "
 "So an export set proves a part is TCE-buildable and nothing more about price. Related topic: reading-dcsc-exports.",
 "Measured comparison of scraped price lists and export-derived prices against real DCSC exports, 2026-09-03 and 2026-09-11", "2026-09-11"),

("dm3010h-drives-sold-in-6-packs-dcsc-forces-qty-2",
 "DM3010H|DM120S", "proven",
 "DM3010H 2U12 LFF drives are sold only in 6-drive packs and DCSC forces qty 2 (all 12 bays); only the DM120S expansion shelf allows 6 drives",
 "ThinkSystem DM3010H 2U12 LFF (ONTAP unified hybrid array, Lenovo Press LP1793) ordering: drives are never ordered individually, every option is a 6-drive pack (for example '60TB (6x 10TB)', '144TB (6x 24TB)'). "
 "The base enclosure has 12 LFF bays so DCSC forces qty 2 (2 packs x 6 = 12 drives) and qty 1 is not selectable on the base chassis. The DM120S 2U12 LFF expansion shelf is the one that supports partial population of 6 or 12 drives. "
 "Confirmed from DCSC pack descriptions and the 12-bay spec; the verbatim 'must be fully populated' sentence could not be located in LP1793, so quote the DCSC validation message if a customer challenges it. "
 "TCE: all four NL-SAS packs seen carry Top Choice Express (B90V 24TB = 6x4TB, B90Y 60TB = 6x10TB, BXQE 132TB = 6x22TB, CASW 144TB = 6x24TB Non-SED), so changing drive size does not break TCE. "
 "COST PER TB (Aug 2026 DCSC list): the 22TB pack (BXQE) is cheapest per TB at about half the per-TB cost of the 6x4TB pack, the 6x24TB pack is about 0.55x and the 6x10TB pack about 0.63x of it. Going from 10TB to 22TB drives on a full 12 bays costs roughly two thirds of the 10TB pack's average per TB. Never default to small packs to save money; price the capacity actually needed. "
 "USABLE CAPACITY (12 bays, RAID-DP, ONTAP): 12 minus 2 parity minus 1 spare = 9 data drives, then about 10 percent WAFL and an optional 5 percent snapshot reserve gives roughly 60 percent of raw; 12x 10TB = 120TB raw is about 70-75TB usable. "
 "RAID-TEC (triple parity, best practice on very large NL-SAS because of rebuild time) takes a third parity drive and leaves 8 data drives. Pull the real number from the DM Capacity Estimator or the ONTAP Hardware Universe before quoting. "
 "GOTCHA: the 22TB and 24TB packs are Non-SED. If encryption at rest is required, find an SED pack or plan on ONTAP NVE (software volume encryption), which does not need SED drives. Units are TB.",
 "Lenovo Press LP1793; DCSC pack descriptions Aug 2026", "2026-08-13"),

("fx630-v4-is-all-nvme-only-no-hdd-or-raid",
 "FX630 V4|7DPLCTO1WW|ThinkAgile FX", "proven",
 "ThinkAgile FX630 V4 (7DPLCTO1WW) is 1U all-NVMe ONLY: no 3.5in, no SAS, no HDD and no RAID controller, so an HDD plus RAID config can never be 'converted' to FX",
 "FX630 V4 is the ThinkAgile any-to-any line (VMware, Nutanix or Azure Local on one SKU). Checked 2026-09-10 against 4 TCE-validated exports. "
 "The only backplane ever seen is C21X 10x 2.5in NVMe Gen5. A part search on the MTM for 3.5in, SAS, HDD or chassis returns one hit, a 2.5in filler. The only controller line is 5977 'no configured RAID required', so there is no RAID or HBA option at all. "
 "WHY IT IS NOT ARBITRARY: the FX spec is the intersection of what all three stacks demand. vSAN ESA wants all-NVMe TLC, Nutanix wants pass-through, and Azure Local (S2D) will not accept a RAID abstraction. "
 "Any config built on 3.5in SAS HDDs behind a RAID card is therefore a ground-up re-spec of the storage tier, not a modification. "
 "TCE-validated parts on 2026-09-10: base CDY4; the only TCE CPU was C5QV 6517P 16C 190W 3.2GHz (pricier and hotter than the SR650 V4's C5RD 6515P 150W; C5QV has since left the TCE list on some MTMs, so re-check); "
 "PSU C0U3 2000W Titanium is 230V-ONLY, so a 115V site kills FX outright; NVMe C0BA 3.84TB; boot M.2 C287 960GB x2 with CC7G RAID kit; NIC BE4T OCP or BE4U PCIe (ConnectX-6 Lx); memory C0TQ 64GB, C0U9 32GB 1Rx4, BYTJ 32GB 2Rx8. "
 "The service family is 7Q04CTS4WW 'SW DEFINED PREMIER', not the SR650 V4's 7Q01 family. "
 "TWO OPEN UNKNOWNS, assert neither: (1) single socket is UNPROVEN on FX630 V4, all 4 validated configs use 2 CPUs, and if 2 is the minimum the per-node core count and per-core VMware or Nutanix licensing double (contrast HX650 V4, where single socket is proven); "
 "(2) no 2U FX650 V4 appears anywhere in the source corpus, so ask for an export before answering anything about it. All-NVMe capacity is expensive per TB, so FX suits modest-capacity clusters.",
 "DCSC exports (4 TCE-validated 7DPLCTO1WW configs) 2026-09-10", "2026-09-10"),

("hx-integrated-system-vs-certified-node-and-7dg4-suffixes",
 "ThinkAgile HX|HX650 V4|HX650a V4|HX630 V4|Nutanix", "proven",
 "HX Integrated System vs Certified Node is a licence and support-contract difference, not hardware; V4 has no separate IS and CN part numbers, but machine type 7DG4 has three model suffixes",
 "Integrated System (Appliance) and Certified Node (CN) are the same box with the same components and both ship factory-imaged with Nutanix software preloaded. The difference is the Nutanix licence and software support. "
 "INTEGRATED SYSTEM: ships with licensed Nutanix software bundled (bought through Lenovo) plus the ThinkAgile Premier single point of contact for hardware and software. "
 "CERTIFIED NODE: ships without the Nutanix licence or Nutanix software support; software is preloaded but unlicensed, and the customer reuses an existing Nutanix term licence or ELA or buys licence and support direct from Nutanix. Support is split: Lenovo owns hardware, Nutanix owns software. "
 "V3 AND EARLIER: Appliance and CN were distinct orderable products with their own machine types (for example HX630 V3 ROBO Integrated System 7D6MCTO2WW versus Certified Node 7D6MCTO4WW). "
 "V4: the guide lp2133 lists no separate Appliance and CN part numbers; software licences are 'optional and recommended to be purchased from Lenovo' with flexibility to use existing Nutanix contracts, so whether the order behaves as an Integrated System or a CN is driven by whether Nutanix licences are added inside the config. "
 "CORRECTION: that does NOT make 7DG4 a single CTO. Machine type 7DG4 has three model suffixes: 7DG4CTO1WW HX650 V4, 7DG4CTO2WW HX650 V4 Storage, 7DG4CTO3WW HX650a V4 (guide lp2229). Read a 7DG4 quote to the suffix before assuming which box it is. "
 "SUPPORT: the ThinkAgile single point of support applies to CN as well as Appliances. Appliance gives one contact AND one contract; CN gives one contact but two entitlements underneath (Lenovo hardware plus Nutanix software direct) and needs an active Nutanix support contract for Lenovo to escalate. Quote Integrated System only if the customer wants everything consolidated onto one Lenovo contract. "
 "Nutanix policy: Extended Support Services for Software on OEM Hardware is available on OEM appliances only. See topic thinkagile-hx-single-point-of-support-mechanism.",
 "Lenovo Press lp2133, lp2229; pubs.lenovo.com ThinkAgile HX licence considerations; Nutanix support policy", "2026-08-12"),

("thinkagile-hx-single-point-of-support-mechanism",
 "ThinkAgile HX|ThinkAgile FX|Nutanix|Premier Support", "proven",
 "How to answer 'NX has one line of support, Lenovo splits hardware and software': explain the mechanism, do not repeat the slogan 'end-to-end'",
 "MECHANISM: for ThinkAgile HX the customer calls Lenovo (one number, 24x7). Lenovo owns the case and performs problem determination; for a software issue Lenovo escalates to Nutanix ON THE CUSTOMER'S BEHALF, after which Nutanix contacts the customer and owns the software fix to closure. The customer is never told to hang up and call Nutanix. "
 "PREMIER: under Lenovo Premier Support the technicians stay engaged from case creation to closure, and for third-party software Lenovo opens the vendor case (through TSANet) and keeps collaborating until closure. So Lenovo is the CASE MANAGER end to end while Nutanix owns the software TECHNICAL FIX; both statements are true. 'End-to-end case management' means case ownership, not that Lenovo repairs the software. "
 "APPLIES TO CERTIFIED NODES: Lenovo's documentation says the service covers both HX Appliances and HX Certified Nodes, and lp2133 describes single-contact hardware and software escalation regardless of whether licences are bought separately or through Lenovo. "
 "HONEST NUANCE a sharp SE will probe: there are two support ENTITLEMENTS underneath (Lenovo hardware, and Nutanix software on the customer's Nutanix contract). That is a procurement fact, not a two-phone-numbers fact. Appliance consolidates software support onto the Lenovo contract; CN does not. "
 "THE ONE CONDITION: Lenovo engages Nutanix only if the customer holds an active Nutanix software support contract (Lenovo's collaborative-support terms require the third-party maintenance contract to be active). A Certified Node with Nutanix licences bought direct satisfies this; if that support lapses the single front door breaks. "
 "TO BULLETPROOF: quote the exact 'Warranty and support' wording from lp2133, and confirm the Premier tier on the specific quote carries the ThinkAgile Advantage single-point-of-support with Nutanix escalation rather than only generic Premier collaborative software support. "
 "Do not claim Nutanix NX single-vendor support is gone; it is current. Related topic: hx-integrated-system-vs-certified-node-and-7dg4-suffixes.",
 "Lenovo Press lp2133; Lenovo Premier Support datasheet ds0075; pubs.lenovo.com ThinkAgile HX; Nutanix support policy", "2026-07-21"),

("nutanix-on-lenovo-public-proof-points",
 "ThinkAgile HX|ThinkAgile FX|Nutanix|XClarity", "proven",
 "Reusable public proof points for Nutanix on Lenovo: XClarity plus Prism, supply chain, reliability, and the rule against quoting node-reduction numbers without the customer's own sizer output",
 "MANAGEMENT: ThinkAgile builds include XClarity One (Standard) and XCC3 Premier per node. XCC3 is out-of-band per-node hardware management (remote console, power, health). XClarity One is centralized firmware compliance and updates, hardware inventory, health and event monitoring and warranty. "
 "Lenovo ThinkAgile XClarity Integrator for Nutanix surfaces Lenovo hardware health and events inside Prism and offers one-click firmware; firmware lifecycle runs from Prism through Nutanix LCM using Lenovo-validated payloads (Lenovo support article ht505781). "
 "SUPPLY CHAIN: Lenovo Trusted Supplier Program, Intel Transparent Supply Chain (Lenovo Press LP1434), a US-based manufacturing option (secure end to end in the US by verified US persons), Security by Design (LP1116), and Gartner Supply Chain Top 25 (ranked #3 in High Tech in 2023). "
 "RELIABILITY: ITIC uptime ranking, see topic lenovo-itic-x86-uptime-ranking-12-years. "
 "SIZING DISCIPLINE: Xeon 6 (Granite Rapids) per-core and per-socket performance can let the Nutanix Sizer consolidate to fewer nodes than an older estate, but the real node count depends on the Collector run, whether the design is compute- or capacity-bound, and RF and N+1 headroom. Never state a node-reduction number without the customer's actual Collector or Sizer output. "
 "For a named, industry-matched reference customer who will take a call, request one through the Lenovo and Nutanix account teams; public case studies will not cover every vertical.",
 "Lenovo Press LP1434, LP1116; Lenovo support ht505781; Lenovo product-security pages 2026-07-21", "2026-07-21"),

("nutanix-no-mixed-hardware-vendors-in-one-cluster",
 "Nutanix|ThinkAgile HX|Nutanix NX|Cisco UCS|Dell XC", "unknown",
 "Nutanix does not support mixing hardware vendors in one cluster, so every competitive swap is whole-cluster or a parallel new cluster, never node-by-node",
 "No Lenovo HX with Cisco UCS, no HX with NX, no HX with Dell XC in the same cluster. What IS allowed inside one vendor: different models, different generations, different CPU generations, and all-flash mixed with hybrid. "
 "So a customer instinct of 'swap a few nodes to Lenovo and see how it goes' is not an option. The only two shapes are: (1) replace the ENTIRE cluster at once, including any compute-only nodes, or (2) stand up a separate Lenovo cluster alongside and migrate workloads into it, with both clusters managed together from Prism Central, which works across vendors even though a single cluster cannot mix. "
 "Say this up front; discovering it after a partial quote is out makes the deal look mis-scoped. It is also why another vendor's compute-only nodes cannot simply be re-hosted on Lenovo. "
 "Status is UNKNOWN because the source note cites no document: confirm the current wording in Nutanix's hardware compatibility and support documentation before quoting it to a customer.",
 "Nutanix hardware compatibility and support policy (confirm current wording)", "2026-08-14"),

("nutanix-nx-hardware-eosl-by-generation",
 "Nutanix NX|ThinkAgile HX", "proven",
 "Nutanix NX hardware end-of-service-life by generation: G6 and older are out of hardware service life, G7 runs to 2027-28, G8 to 2029; EOSL is hardware only",
 "EOSL means Nutanix ends HARDWARE support and parts for that model. It is NOT software support: Nutanix software and subscription support continue on their own contract, so the accurate line is 'the hardware is past Nutanix service life', never 'they lost all support'. "
 "By generation (checked 2026-07-21): pre-G4 (NX-3050, NX-3060, NX-6000 and similar) Feb to May 2021, out. G4 Feb to Jul 2022, out. G5 Dec 2022 to 30 Sep 2024, out. "
 "G6 mostly 30 Jan 2025, NX-3170-G6 30 May 2025, NX-1175S-G6 and NX-5155-G6 30 Dec 2025, all out (the last G6 expired 30 Dec 2025). "
 "G7 earliest 30 Mar 2027 (NX-8170, NX-8155, NX-8035, NX-3170, NX-3155G, NX-1065-G7), others 30 Jun 2027 and Dec 2027 to Jun 2028, still supported. G8 all models 30 Jul 2029, still supported. "
 "As of mid-2026 everything G6 and older is out of hardware service life and G7 plus G8 are still supported. An NX-8170-G7 reaches hardware EOSL 30 Mar 2027, under a year out, which is a legitimate refresh trigger; do not use 'out of support' against G8 customers. "
 "ACCURATE POSITIONING for a G6-or-older customer: their NX hardware is past Nutanix's end of service life and running production on hardware Nutanix no longer supports, a good time to refresh to current-generation Lenovo HX and keep the Nutanix software licence on supported hardware. "
 "Live check: the Nutanix portal platform EOL list. Related topic: nutanix-no-mixed-hardware-vendors-in-one-cluster.",
 "Third-party EOSL database for NX checked 2026-07-21; authoritative check is the Nutanix portal platform EOL list", "2026-07-21"),

("nutanix-edge-answers-hx1021-towers-and-single-socket",
 "ThinkAgile HX|HX630 V4|HX650 V4|HX1021|ThinkEdge|Nutanix NVD", "proven",
 "Nutanix edge and multi-site answers on Lenovo: HX1021 is withdrawn, no Lenovo tower or ThinkEdge is Nutanix-certified, and single-socket source nodes go to HX650 V4 not HX630 V4",
 "1. HX1021 is withdrawn (Lenovo Press lp1384) and was SE350 with Xeon D, so it cannot meet a Xeon 6, 512GB, 7.68TB NVMe spec. Any Nutanix Validated Design or partner document that still calls for HX1021 is stale. "
 "2. Nothing in the Lenovo tower (ST) or ThinkEdge (SE) line is Nutanix-certified. ThinkAgile HX (datasheet ds0046) is 1U and 2U rack only, and Nutanix compute-only on ThinkSystem (lp2421) lists only SR630 V4, SR650 V4, SR645 V3 and SR665 V3. "
 "So the edge answer must be a rack HX with 115V PSU and ASHRAE A3 or A4 validation, not a different form factor. "
 "3. For single-socket source nodes use HX650 V4, not HX630 V4. The HX630 V4 guide says 'Two Intel Xeon 6700P/6500P processors' (2 sockets mandatory), so a 16C-per-node source becomes 32C per node, +256 NCI cores over a 16-node estate; HX650 V4 builds single socket in DCSC. The cost of the fix is 2U instead of 1U. "
 "EDGE-HARDENING FACTS: C2Y9 1300W and BWM3 or C0U8 800W are 230V/115V; C0U3 2000W is 230V-only and never belongs at an edge site. SR650 V4 is ASHRAE A2 (10-35C) standard and A3 (5-40C) or A4 (5-45C) on qualifying configs. "
 "Acoustics are 47 dB idle and 54 dB at full TDP, GPU-rich 56 dB and 75 dB. HX630 V4 depth is 788 mm and needs roughly a 1000 mm rack; shallow wall boxes will not take it. "
 "LICENSING: NCI-E per-VM edge licensing is on the HX price list (C1W0 to C1W5, plus NCM-E C4X7 to C4XC); for small edge sites it sidesteps the per-core socket penalty, ask Nutanix about eligibility. "
 "MEMORY: 384GB is not a buildable DIMM population on these nodes (6 DIMMs); offer 512GB as 8x C0TQ. C1X9 7.68TB NVMe and BS2C L4 24GB GPU are both non-TCE (2026-08). See also topics hx630-v4-requires-two-cpus-and-memory-totals and hx650-v4-drive-bay-option-dictates-socket-count.",
 "Lenovo Press lp1384, lp2132, lp2133, lp2421; ThinkAgile HX datasheet ds0046; DCSC 2026-08-12", "2026-08-12"),

("dcsc-tce-filter-hides-gpu-cards-on-hx650-v4",
 "HX650 V4|7DG4CTO1WW", "proven",
 "With the TCE filter on, HX650 V4 GPU Adapter shows only the GPU-Ready Installation kit BP4X and no cards; the L4 and L40S are non-TCE and need Full Mode",
 "Hit live in DCSC 2026-08-12. With the Top Choice Express filter ON, the GPU Adapter category on 7DG4CTO1WW shows only BP4X 'ThinkSystem Double Width GPU-Ready Installation' (the only TCE line there) and no actual cards, which reads as 'DCSC will not let me add a GPU'. "
 "Both cards are non-TCE, so switch to Full Mode to see them: BS2C L4 24GB single-wide (max 8 on HX650 V4) and BYFH L40S 48GB double-wide (max 2). BP4X is the double-wide prep kit and is not what a single-wide L4 needs. "
 "The HX650 V4 guide also warns that some GPUs are only available with VMware ESXi selected as the hypervisor (B15S is the AHV line, C89R is ESXi), so if Full Mode still hides the card, flip the hypervisor line and test. "
 "Adding a non-TCE GPU ends TCE for the whole config, see tce-core-rules. The HX650a V4 (7DG4CTO3WW) is the platform with TCE-badged GPUs, see topic hx650a-v4-is-the-gpu-rich-variant-of-hx650-v4.",
 "DCSC live panel 2026-08-12; Lenovo Press lp2133", "2026-08-12"),

("hx650a-v4-is-the-gpu-rich-variant-of-hx650-v4",
 "HX650a V4|HX650 V4|7DG4CTO3WW", "proven",
 "HX650a V4 (7DG4CTO3WW) is the GPU-rich AI variant of HX650 V4: up to 4 front double-wide GPUs but only 8 NVMe bays, and its TCE-badged GPUs do not transfer to the plain HX650 V4",
 "The 'a' means AI or GPU-rich, as on SR650a V4 (HX650a is the Nutanix-bundled version of that platform). Both HX650 V4 and HX650a V4 are 2-socket 2U Intel Xeon 6 (Granite Rapids) nodes with the same PSU lineup (800W, 1300W, 2000W, 2700W, 3200W); the real fork is GPU capacity traded against drive bays. "
 "HX650 V4 is 7DG4CTO1WW (7DG4CTO2WW is Storage): up to 2 double-wide GPUs (L40S 48GB), up to 10 single-wide (L4 24GB, max 8 of that part), front bays 24x or 16x 2.5in NVMe (Storage model: 8x 3.5in plus 4x AnyBay, optional 4x 2.5in rear). "
 "HX650a V4 is 7DG4CTO3WW: up to 4 double-wide GPUs mounted in the front, NVLink-pairable (H200 NVL, RTX PRO 6000 Blackwell), up to 8 single-wide, and only 8x 2.5in NVMe with no rear bays because the front slots are the GPUs. "
 "So HX650a trades two thirds of the NVMe capacity for double the double-wide GPU count and the Hopper and Blackwell parts the plain HX650 cannot take. Positioning: HX650a for Nutanix Enterprise AI and agentic inference, HX650 for general HCI plus light vGPU. "
 "TCE (seen live 2026-08-12): HX650a V4 and HX650 V4 Storage were TCE-enabled; CBK8 RTX PRO 6000 Blackwell 96GB and CBFN H200 GPU-Ready Installation were badged Top Choice Express on the HX650a, while C3V3 H200 NVL was still non-TCE with supply status X. "
 "A stored catalog scrape showed zero TCE lines for 7DG4CTO2WW and 7DG4CTO3WW, so scraped tc flags are a pre-screen only. "
 "Do NOT read the HX650a's TCE GPUs as a fix for a plain HX650 V4 GPU build: CBK8, CBFN and C3V3 are 7DG4CTO3WW parts only, and the HX650 V4's own GPUs (BS2C L4 24GB, BYFH L40S 48GB) are Not TCE in lp2133 Table 13. Re-check the L4 badge live before quoting.",
 "Lenovo Press lp2133 (HX650 V4), lp2229 (HX650a V4), lp2390 (HX Solution for AI with Nutanix Enterprise AI); DCSC live 2026-08-12", "2026-08-12"),

("hx665-v3-cannot-take-h200-nvl-or-rtx-pro-6000",
 "HX665 V3|HX650a V4", "flagged",
 "HX665 V3 (AMD, V3-only) has no H200 NVL or RTX PRO 6000 option; an LLM-inference ask means HX650a V4, but a GPU summary page contradicts the product guide",
 "HX665 V3 is the AMD EPYC 9005 'Turin' general-purpose 2U HCI node (1 or 2 CPUs, up to 128 cores per CPU, 24 DIMMs = 12 channels per CPU at 1DPC, max 6TB, 24x 2.5in SAS/SATA/NVMe front, Storage variant 12x 3.5in plus optional 4x 2.5in rear, PSU 750W, 1100W, 1800W, 2400W). "
 "CTOs: Integrated System 7D9NCTO1WW (GPU-controlled 7D9NCTOAWW), Certified Node 7D9NCTO3WW (GPU-controlled 7D9NCTOCWW), Storage 7D9NCTO2WW and 7D9NCTO4WW. GPU configs need the GPU-controlled CTO, not the standard one. "
 "There is no HX665 V4 and no HX665a as of 2026-08-06, so a customer wanting AMD plus current-generation GPUs has no HX answer. "
 "HX665 V3 GPU table (guide lp1649 Table 14): L40S 48GB (4X67A90669) max 3, RTX PRO 4500 Blackwell 32GB (4X67B12675) max 3, A16 64GB (4X67A76727) max 3, L4 24GB (4X67A84824) max 5. It has NO H200 NVL and NO RTX PRO 6000. "
 "HX650a V4 (guide lp2229): 2x Xeon 6 up to 86 cores per CPU, 32 DIMMs, max 8TB, up to 4 double-wide or 8 single-wide GPUs in the front, H200 NVL 141GB max 2, RTX PRO 6000 Blackwell Server Edition 96GB max 2, NVLink-pairable, 8x 2.5in NVMe only. "
 "So any real LLM-inference ask (large VRAM, NVLink) is HX650a V4, not HX665. GOTCHAS: HX650a 4-GPU configs push into 2700W and 3200W PSU territory, check 230V; Nutanix NCI is licensed per core, so EPYC's 128 cores per socket is a licence cost, not a win, unless the cores are needed. "
 "CONFLICT: Lenovo Press lp0768 (GPU summary) shows H200 NVL and RTX PRO 6000 as max 2 on HX665 V3, contradicting lp1649 Table 14. Treat lp1649 as authoritative and confirm in DCSC before quoting.",
 "Lenovo Press lp1649, lp2229, lp0768", "2026-08-06"),

("hx-storage-node-v3-vs-v4-3-5in-trade",
 "HX650 V4 Storage|HX650-Storage V3|7DG4CTO2WW|7D6NCTO2WW", "proven",
 "The 3.5in-drive HX storage node forces a trade: HX650-Storage V3 has 128GB DIMMs but no NVMe data drives, HX650 V4 Storage has NVMe AnyBay but no 128GB DIMM",
 "Only two current MTMs accept 3.5in drives on ThinkAgile HX. HX650 V4 Storage 7DG4CTO2WW: backplane C3RV = 8x 3.5in SAS/SATA plus 4x 3.5in AnyBay (12 front bays, 4 NVMe-capable) plus optional rear C46H 4x 2.5in NVMe Gen5; base HX650 V4 (7DG4CTO1WW) and HX630 V4 are 2.5in or E3.S NVMe only. "
 "HX650-Storage V3 7D6NCTO2WW (Integrated System) or 7D6NCTO4WW (Certified Node): backplane B8LT = 2U 12x 3.5in SAS/SATA plus B8LV 4x 2.5in SAS/SATA rear. "
 "V3: 128GB RDIMM yes (C4EA 128GB TruDDR5 5600 2Rx4; 96GB BWHV also exists); NVMe data drives NONE (only M.2 boot BKSR or BXMH), so the flash tier must be SAS/SATA SSD (BNWH 3.5in PM1653 3.84TB RI SAS 24Gb, BP3F 3.5in PM1653 7.68TB RI SAS 24Gb, BK7F 3.5in S4520 3.84TB RI SATA); CPU Emerald Rapids 5th Gen (for example BYVX Xeon Gold 6526Y 16C 195W 2.8GHz); 3.5in HDD ladder 4, 6, 8, 10, 12, 20, 24TB including 8TB AUU9. "
 "V4 Storage: 128GB RDIMM NO (largest is 96GB BZ7D); NVMe YES (3.5in U.3 7500 PRO C9ZW, C9ZX, C9ZY, C9ZZ = 1.92, 3.84, 7.68, 15.36TB, and 2.5in U.2 HX VA parts); CPU Granite Rapids Xeon 6 (for example C5QV 6517P 16C 190W 3.2GHz); 3.5in HDD ladder 12, 16, 20, 24TB with no 8TB. Neither platform offers an 18TB HDD. "
 "THE 128GB RULE, checked across the catalog: no 128GB DIMM exists on ANY V4 or Xeon 6 platform (SR650 V4, SR650a V4, HX630 V4, HX650 V4, HX650 V4 Storage); 128GB parts appear only on V3 MTMs. "
 "So 2048GB per node on V4 needs 32x 64GB C0TQ (all 32 slots, 2DPC, bus derates 6400 to 5200 MT/s per lp2133), while on V3 it is 16x 128GB C4EA at 1DPC, full speed, 16 slots free. Any Nutanix NX BOM quoting 128GB DIMMs pushes the conversion toward V3. "
 "96GB BZ7D is not TCE on any platform and, although the catalog lists it, live DCSC on 2026-08-13 did not accept 96GB DIMMs on the HX650 V4 Storage build at all. "
 "Risers have NO bearing on DIMM population. If a high-DIMM-count config errors, look at socket count (1 CPU caps you at 16 slots) or the thermal matrix, never risers.",
 "Lenovo Press lp2133; DCSC catalog 2026-07-02; live DCSC 2026-08-13", "2026-08-13"),

("hx650-v4-storage-joined-tce-and-single-socket-tce-ready",
 "HX650 V4 Storage|HX650 V4|7DG4CTO2WW|7DG4CTO1WW", "proven",
 "HX650 V4 Storage (7DG4CTO2WW) was added to Top Choice Express and HX650 V4 single socket became TCE build-ready 8/26/2026; a '1-Processor Support' slide is not a TCE list",
 "7DG4CTO2WW, the only current-generation ThinkAgile HX that accepts 3.5in drives, is on the TCE program (seen live in DCSC 2026-08-13). A stored catalog scrape from 2026-07-02 reported 0 TCE of 244 options on it, which predates the addition; an earlier note that the whole Storage model and its hybrid node config B0SV are 0-TCE is SUPERSEDED. "
 "Before the addition a hybrid 3.5in HDD plus flash Nutanix conversion appeared to have no fast-ship path; that reasoning is void and the hybrid node can be quoted on short lead time. Confirm at part level: an MTM joining the program does not mean every part carries the flag. TCE proof is feature code BU1E in the built config. "
 "SEPTEMBER 2026 CHANGE SET: (1) HX650 V4 single socket is TCE build-ready (announced 7/21/2026, build-ready 8/26/2026); it was corroborated earlier by BU1E-clean single-CPU 7DG4CTO1WW exports dated 7/28/2026 (1x C5QQ) and 8/10/2026 (1x C5RD 16C). "
 "(2) HX650 V4 Storage confirmed in TCE as a single-socket hybrid: minimum 2x 2.5in NVMe plus 4x 3.5in HDD, maximum 4x NVMe plus 8x HDD; NVMe 1.92 to 15.36TB, HDD 4 to 20TB; announce/build-ready 8/26/2026 for the 4TB to 10TB HDD range. TCE-proven HDDs in exports: C5X9 4TB, C4DA 12TB, C4D6 20TB (all 3.5in 7.2K SAS 512e v2). "
 "(3) removal: C5QQ 6505P 12C left the TCE list, see topic hx650-v4-tce-cpu-list-live-panel-2026-09-03. "
 "THE TRAP: the announcement slide is titled '1-Processor Support', NOT TCE. Single-socket availability and TCE membership are different things. It lists HX630 V3 ROBO, for which there is zero TCE evidence (every HX630 V3 config in the source corpus is non-TCE), so do not put HX630 V3 on a TCE document off that slide. "
 "Also on the slide: 2-node clusters are capped at 20TB per node. The 64GB C0TQ is the largest TCE RDIMM; 96GB BZ7D is not TCE on any platform.",
 "Live DCSC 2026-08-13; Lenovo TCE change announcement (7/21/2026 announce, 8/26/2026 build-ready); DCSC exports", "2026-09-03"),

("hx630-v4-requires-two-cpus-and-memory-totals",
 "HX630 V4|7DG3CTO1WW", "proven",
 "HX630 V4 needs two populated sockets and its allowed DIMM counts make 384GB impossible; valid totals jump from 256GB to 512GB",
 "HX630 V4 (SR630 V4 base, Xeon 6 P-core) per lp2132 and lp1971: 'Two Intel Xeon 6700P/6500P-series' are required, both CPUs need identical DIMM counts and all DIMMs must be the same part number (no mixing). "
 "Allowed quantities PER CPU: 16GB 1/4/8; 32GB x8-rank BYTJ (TCE) 1/4/8/12/16; 32GB C0U9 (TCE) 4/8; 64GB C0TQ (TCE) 1/4/8/12/16; 96GB and 128GB 8/16 only; 256GB 3DS 8/16. No 48GB DIMM is offered. "
 "Therefore 384GB total (192GB per CPU) cannot be built. Valid nearby totals are 256GB (8x 16GB per CPU, or 4x 32GB per CPU at half bandwidth) and 512GB (8x 32GB per CPU: all 8 channels, TCE, the config to quote). "
 "Customers refreshing from 384GB HX630 V3 nodes must move to 256 or 512, so pre-empt this in sizing conversations. RAM does not affect Nutanix licensing (cores and capacity based). "
 "MRDIMMs (32GB or 64GB, 8 per CPU only) are processor-model dependent and Not TCE. CXL memory exists on the platform but is unsupported on ESXi, so it is not a bridge to 384. "
 "RE-CONFIRMED 2026-08-24: HX630 V4 still requires two populated sockets. C5QQ 6505P 12C was offered and TCE on 7DG3CTO1WW at that date but you must buy two, so a single-socket 12C sizer line cannot be honoured on the 1U without doubling licensed cores (12 to 24 per node). Single socket on HX V4 is an HX650 V4 (7DG4CTO1WW) capability only. "
 "An earlier note treating the HX630 V4 2-CPU minimum as unproven is superseded by this re-check.",
 "Lenovo Press lp2132, lp1971; DCSC 2026-08-24", "2026-08-24"),

("hx650-v4-drive-bay-option-dictates-socket-count",
 "HX650 V4|7DG4CTO1WW", "proven",
 "HX650 V4 bay option dictates socket count: 8-NVMe (CJUF) is single-socket only, 16-NVMe (C9KA) and 24-NVMe (C703) need 2 CPUs",
 "Proven from 50 HX650 V4 exports (2026-08-24), zero exceptions: 8-NVMe backplane option CJUF (20 configs) has exactly 1.0 CPU per node in every one; 16-NVMe C9KA (16 configs) and 24-NVMe C703 (14 configs) have 2.0 CPUs minimum. "
 "The few readings above 2.0 are mixed-model configs that also contain HX630 V4 nodes, so the CPU sum spans both models and is not counter-evidence. All three bay codes are TCE-proven. "
 "CAUSE: one Xeon 6 CPU's PCIe lanes reach only 8 NVMe bays; bays 9 and up hang off the second processor. "
 "LICENSING NUANCE: more bays does NOT automatically double the licence, because a target core count can be split across two sockets (2x 12C = 1x 24C). The penalty comes from the TCE CPU LIST. Two identical TCE CPUs sum to 16, 32, 48 or 64 cores per node (parts are 8, 16, 24 and 32C after the 12C exit), so a node that needs 24 cores becomes 32 cores under dual-socket TCE (+33 percent, 96 versus 72 licensed cores over 3 nodes), while a node that needs 16 cores can be 2x 8C with no penalty. "
 "Off TCE the penalty vanishes (2x 12C = 1x 24C). An earlier version of this note, written when 16C looked like the TCE floor, said a 1x 16C node would double; that is superseded, see topic hx650-v4-tce-cpu-list-live-panel-2026-09-03. Never state 'more bays doubles the licence' as a general rule. "
 "ANSWERING 'is 8-NVMe right because storage is small?': the causation is backwards. You pick single socket to hold licensed cores down, and single socket only offers 8 bays; small storage is what makes 8 bays painless. Corollary: 4x 3.84TB in an 8-bay node leaves 4 bays, so raw capacity can double later with no CPU or licence change. "
 "Related topic: hx650-v4-all-flash-drive-minimum-is-per-socket.",
 "DCSC exports (50 HX650 V4 configs) 2026-08-24; 2026-09-03 TCE CPU panel", "2026-08-24"),

("hx650-v4-all-flash-drive-minimum-is-per-socket",
 "HX650 V4|7DG4CTO1WW", "proven",
 "HX650 V4 all-flash drive minimum is 2 NVMe PER POPULATED SOCKET; the guide's '4 to 24 NVMe' is the dual-processor figure, not a universal floor",
 "THE RULE (DCSC enforces it): each populated CPU requires 1 backplane and a minimum of 2 NVMe drives. Single socket = 1 backplane and 2 NVMe minimum; dual socket = 2 backplanes and 4 NVMe minimum. "
 "It is a PCIe lane-wiring rule: NVMe drives connect 1:1 to CPU lanes (lp2133: 24x NVMe without oversubscription, up to 36x onboard NVMe ports), so an unpopulated socket has no lanes to drive a second backplane. "
 "WHY THE GUIDE MISLEADS: lp2133 'Configuration rules' says flatly that for All Flash configurations the system supports from 4 to 24 NVMe, and for boot 2 drives are required in RAID 1. The '4' is the two-CPU floor (2 sockets x 2 drives) and the '24' is the ceiling (Table 7: C46P 8x 2.5in NVMe backplane, max 3 = 24 bays). "
 "It has no processor qualifier, so it reads as universal and customers will quote it back. The rule is absent from lp2127 (SR650 V4) too, so there is no citable published source. "
 "Boot M.2 never counts toward the data-drive minimum (separate rule, Table 8, max qty 2, carries the hypervisor not the storage pool). "
 "PROOF: single-socket builds with 2 data drives are accepted and compliant, for example 1x C5RD, 1x C46P and 2x CCVZ 3.2TB, and single-socket 2x C3QG 15.36TB per node. Do not tell anyone a 2-drive single-socket node is unsupported. "
 "PRACTICAL: a customer reading the guide may challenge any 2-drive node. You can explain the per-socket rule but cannot cite it, so on a formally documented design either get Lenovo HX product management to confirm in writing or sidestep it with 4 drives at a smaller TCE capacity (C1AC 1.92TB RI is TCE; 4x = 7.68TB per node).",
 "Lenovo Press lp2133 (Configuration rules, Tables 7 and 8); DCSC builds 2026-08-25", "2026-08-25"),

("hx650-v4-tce-cpu-list-live-panel-2026-09-03",
 "HX650 V4|7DG4CTO1WW", "proven",
 "HX650 V4 TCE CPU list on the live DCSC panel 2026-09-03: ten parts from 8C to 32C, no 12C; the list is NOT monotonic by core count",
 "The TCE-filtered processor panel for HX650 V4 on 2026-09-03 carried exactly ten parts, all with the Top Choice Express badge: "
 "C5R6 6507P 8C 150W 3.5GHz, C5R7 6714P 8C 165W 4.0GHz, C5RD 6515P 16C 150W 2.3GHz, C5QV 6517P 16C 190W 3.2GHz, C5R5 6724P 16C 210W 3.6GHz (4XG7B17660), "
 "C5QR 6520P 24C 210W 2.4GHz (4XG7B17661), C659 6527P 24C 255W 3.0GHz, C5QT 6530P 32C 225W 2.3GHz, C5R4 6730P 32C 250W 2.5GHz, C5QX 6737P 32C 270W 2.9GHz. "
 "C5QQ 6505P 12C is ABSENT and is temporarily out on ALL platforms, not just HX650 V4. Exports showed it TCE-clean as late as 2026-08-24 on HX630 V4, so the removal landed between 8/24 and 9/3. "
 "CONSEQUENCE: there is no 12-core in TCE any more. The ladder is 8C, 16C, 24C, 32C, so every open 12C config has to move to 8C or 16C, and 16C adds 4 cores per socket to the NCI licence count. Always re-price the Nutanix software before re-quoting; never just swap the CPU. "
 "NOT MONOTONIC: 8C C5R6 is on the list while 12C is not, so never infer 'if 12C is off then anything smaller is off'. Proof: a single-socket 5-node HX650 V4 export dated 2026-08-24 carried C5R6 6507P qty 5 (one per node), BU1E present, zero criticals. Dual-socket C5R6 on HX650 V4 has only non-TCE sightings (Jun and Jul 2026), so the 8C proof is single-socket only. "
 "LICENSING PITCH AT THE SMALL END: with 8C on the list, 1x 16C = 2x 8C = 16 licensed cores per node, so on any site sized at the floor single socket does NOT save NCI cores; its case there is CPU cost only (1x C5RD is cheaper than 2x C5R6) and it costs 2U against the HX630's 1U. Single socket wins on licensing only where the node needs more than two smallest TCE CPUs supply, for example 1x 24C replacing 2x 16C. "
 "STORAGE-NODE CAVEAT: the validated 7DG4CTO2WW exports only ever contain C5QV, C5QR and C659; same board, so the full list very likely applies, but pull the panel for 7DG4CTO2WW before stating it. "
 "RULE: a BU1E sighting in an export proves a part was buildable on that MTM on the export date, not that DCSC offers it today; never state a TCE CPU floor from exports alone, get the live TCE-filtered CPU dropdown before it goes in anything customer- or vendor-facing.",
 "Live DCSC TCE-filtered processor panel 2026-09-03; DCSC exports 2026-08-24", "2026-09-03"),

("hx650-v4-c0u2-16gb-dimm-breaks-tce",
 "HX650 V4|7DG4CTO1WW", "proven",
 "On HX650 V4, C0U2 16GB RDIMM is NOT TCE (controlled export comparison); BYTJ 32GB and CCVZ 3.2TB Mixed Use NVMe are, so the TCE DIMM range has a floor as well as the 64GB ceiling",
 "Proven 2026-09-14 by a controlled comparison of two DCSC exports of the same 15-node, three-role-group HX650 V4 cluster, one generated as TCE and one as non-TCE (with 16GB DIMMs). In the NON-TCE export the Worker group KEPT BU1E while the other two groups lost it, which isolates the breaker. "
 "The LB/Jump group CPU was C5R6 6507P 8C and the Control Plane CPU was C5QR 6520P 24C, both on the authoritative TCE list, so the CPU was not the breaker in either group. "
 "The one part present in both flag-losing groups and absent from the group that kept the flag was C0U2 ThinkSystem 16GB TruDDR5 6400MHz 1Rx8 RDIMM; the Worker group used BYTJ 32GB 2Rx8 and kept BU1E. Swapping C0U2 to BYTJ 32GB is exactly what the TCE export did, and it carries BU1E on all three groups. "
 "CONCLUSION: C0U2 16GB is not TCE-eligible on HX650 V4. The 64GB C0TQ is the TCE DIMM ceiling and 16GB sits below a floor, so the TCE DIMM range is bounded at both ends. When a config drops BU1E and the CPU checks out against the panel list, look at the DIMM next. "
 "Also proven in the same pair: CCVZ ThinkAgile HX 2.5in U.2 VA 3.2TB Mixed Use NVMe IS TCE-eligible (it was in the group that kept BU1E), so Mixed Use drives are not automatically a TCE-breaker. "
 "CAVEAT: earlier August 2026 part lists for other MTMs (for example SR650 V4) showed C0U2 as TCE. Membership is per MTM and per date, see topic tce-membership-is-per-mtm-and-per-date. Confirm on the live panel before it goes customer- or vendor-facing.",
 "DCSC exports (paired TCE and non-TCE, same cluster) 2026-09-02 and 2026-09-03", "2026-09-14"),

("tce-nvme-va-pcie5-capacity-window",
 "U.2 VA PCIe 5.0 NVMe|SR630 V4|SR650 V4|HX V4|SR635 V3", "proven",
 "The U.2 VA PCIe 5.0 NVMe TCE window is 3.2TB to 7.68TB: 1.6TB and 12.8TB are OFF the list, so converting to TCE forces capacity up",
 "Measured 2026-09-14 across 154 exports. Top Choice Express on the U.2 VA PCIe 5.0 NVMe family has a capacity FLOOR and a CEILING: 1.6TB C0ZR 24 configs, 0 TCE (below the floor); 3.2TB C0ZQ 7 of 7 TCE; 3.84TB RI C0ZU 12 of 12 TCE; 6.4TB C0ZP 10 of 10 TCE; 7.68TB RI C0ZT 18 of 21 TCE; "
 "12.8TB C0ZN 39 configs, 0 TCE (above the ceiling); 15.36TB RI C0ZS 0 TCE; 3.5in 7.68TB RI CFA4 0 TCE (the 3.5in form factor is off entirely). "
 "CONSEQUENCE: converting a PCIe 5.0 build to TCE forces every 1.6TB drive up to 3.2TB at minimum, so capacity goes UP, not down. On a 63-server conversion this added roughly 112TB of raw storage across four configurations while total cost still fell about 4 percent. Frame it to the customer as the TCE list forcing the size, not the engineer padding the build. "
 "THE PCIe 4.0 LINE HAS NO SUCH FLOOR: C18J U.2 VA 1.6TB Mixed Use PCIe 4.0 is TCE in 27 of 28 configs, which is why SR635 V3 nodes can hold 1.6TB and stay TCE while SR630 V4 nodes on PCIe 5.0 cannot. "
 "Same shape as the HX650 V4 CPU floor and DIMM floor: TCE lists have floors as well as ceilings and membership is never monotonic by size. Check the specific part, never infer from a neighbouring capacity. See topics u3-vs-u2-when-required-and-trimode-dependency and hx650-v4-c0u2-16gb-dimm-breaks-tce.",
 "DCSC exports (154 configs) 2026-09-14", "2026-09-14"),

("tce-membership-is-per-mtm-and-per-date",
 "ALL|SR650 V4|HX650 V4|SR650a V4|HX630 V4", "proven",
 "TCE membership is per MTM AND time-varying: C5QV 6517P left TCE on SR650 V4 in Aug-Sep 2026 while staying TCE on HX650 V4 and SR650a V4; date every TCE claim and name the MTM",
 "WORKED EXAMPLE C5QV Xeon 6517P 16C 3.2GHz. A 2026-07-28 catalog scrape carried tc=true for it on 7DGDCTO1WW (SR650 V4) and it genuinely was TCE then. The live panel on 2026-09-10 no longer offers it under TCE on that MTM. "
 "It was NOT globally withdrawn. Counting BU1E configs with zero criticals in the source corpus: SR650 V4 7DGDCTO1WW last BU1E config 2026-08-06, gone from the panel by 09-10; HX650 V4 7DG4CTO1WW BU1E as recently as 2026-09-03; SR650a V4 7DGDCTO2WW as recently as 2026-09-02; HX630 V4 7DG3CTO1WW through 2026-08-19. "
 "So the part left the TCE list for ONE MTM while staying on it for others. Never say 'X is not TCE' without naming the MTM and the date; a part that is off the list can also come back, so a stale 'not TCE' is as wrong as a stale 'is TCE'. "
 "CONSEQUENCE on SR650 V4: the 16-core TCE list became only C5RD 6515P and C5R5 6724P, a large per-socket price gap with nothing between; note C5R5 itself had only one BU1E config in the source corpus (dated 2026-06-29), so its status is thinly evidenced even though the panel offered it. "
 "THE SALES MOVE when a part drops off TCE: it is still orderable, just not fast-ship, and TCE is all-or-nothing per config. So the question is whether the customer's timeline actually needs the TCE lead time. If they order months out, the non-TCE part may be the better technical pick. Frame it as a trade the partner decides, not as a part that is unavailable. "
 "PROCESS: before naming a part as a TCE option, check the most recent BU1E date on the target MTM in exports. Evidence ladder: live DCSC panel first, then a validated export, then a dated catalog scrape; a bare tc=true with no recent export behind it is the weakest rung. See topics sr650-v4-16-core-tce-cpu-live-panel-2026-09-10 and sr630-v4-8-core-cpu-costs-more-than-16-and-24-core.",
 "Live DCSC panel 2026-09-10; DCSC exports by MTM and date", "2026-09-10"),

("tce-services-and-warranty-do-not-break-bu1e",
 "ALL", "proven",
 "Services, warranty and software lines do NOT break TCE: 264 of 264 BU1E-clean exports carry service lines; only shipped hardware counts",
 "TCE (feature code BU1E 'Lenovo Top Choice Express Flag') is config-level and appears only when every HARDWARE part is on the TCE list. Measured 2026-09-03 across the source corpus: of the 264 exports carrying BU1E with ZERO Critical messages, all 264 contain service lines (5WS7 Premier, 5PS7 Keep Your Drive, 5MS7 deployment, the 7Q0x CTO service SKUs and the base-warranty line) and 249 contain a software or licence line, 20 of them a factory-installed Windows Server preload. "
 "So a Premier warranty, a KYD add-on, deployment services or an OS licence with no TCE flag is normal and costs nothing. ANSWER to 'does adding Premier support break my TCE ship time?' is NO. "
 "NEVER present a non-TCE alternative without stating up front that it kills TCE for the entire bid. Where lead time is the reason the customer is talking to Lenovo, a non-TCE substitution is not neutral, it removes the reason for the deal; say so in the same breath as the suggestion or do not raise it. "
 "Example of the mistake: offering 16x 96GB BZ7D (1536GB at full 6400 MT/s) to fix a 2DPC derate without noting BZ7D 96GB is not TCE on any platform. "
 "A stored catalog scrape is not a source of truth for TCE flags: it went stale on multiple parts within weeks (C5R6 8C and the entry Xeon 6300P C520 4C were both TCE in DCSC on 2026-08-19 although the scrape called them non-TCE). Never assert a part is non-TCE from a scrape alone; ask what DCSC shows (BU1E present or not). "
 "The Nutanix Sizer TCE badge is also unreliable: on one small BOM it tagged only BE4T and left C5QV untagged although C5QV was TCE; absence of the badge proves nothing. Related: tce-core-rules.",
 "DCSC exports (264 BU1E-clean, zero-Critical exports) 2026-09-03; live DCSC 2026-08-13 and 2026-08-19", "2026-09-03"),

("hx-v4-tce-substitution-candidates-dated",
 "HX650 V4|HX630 V4|SR650 V4", "proven",
 "Dated TCE status of common substitution parts on V4 HX and SR650 V4 (Aug 2026): NVMe 1.92 / 3.84 / 15.36TB and 3.2TB MU yes, 7.68 / 6.4 / 1.6TB no; 64GB is the DIMM ceiling; 2048GB per node derates to 5200 MT/s",
 "As read from DCSC on 2026-08-13 to 2026-08-19 (re-check before use, lists rotate). MEMORY: C0TQ 64GB TruDDR5 6400 2Rx4 is the largest TCE RDIMM; BYTJ 32GB 2Rx8 and C0U9 32GB 1Rx4 are TCE; BZ7D 96GB is NOT TCE and no 128GB DIMM exists on V4 at all; MRDIMMs C0TY 32GB and C0TX 64GB are not TCE. "
 "C0U2 16GB is NOT TCE on HX650 V4, see topic hx650-v4-c0u2-16gb-dimm-breaks-tce. "
 "NVMe on HX650 V4 7DG4CTO1WW: C3Q9 3.84TB, C1AC 1.92TB, C3QG 15.36TB and CCVZ 3.2TB Mixed Use are TCE; C1X9 7.68TB, CCVY 6.4TB and CCW0 1.6TB are NOT. So 15.36TB per node is built as 4x C3Q9 or as 2x C3QG (same 30.72TB raw as 4x 7.68TB per node), never as 2x C1X9. CCW0 1.6TB MU was unverified (scrape said not TCE); CCVZ 3.2TB MU is TCE and swaps for CCW0 2:1 at identical capacity. "
 "CPUs: C5R6 6507P 8C is TCE (verified 2026-08-19 against a scrape that called it non-TCE); for the full ten-part list see topic hx650-v4-tce-cpu-list-live-panel-2026-09-03. "
 "MEMORY SIZING CONSEQUENCE: with 64GB as the TCE ceiling, 2048GB per node needs 32 DIMMs, which is 2 DIMMs per channel and derates the bus from 6400 to 5200 MT/s per lp2133. On a TCE bid that derate is not avoidable; state it as a fact of the build rather than offering a non-TCE escape. "
 "The catalog listing a part against an MTM does not mean DCSC will build it; scraped data has no dependency or gating data, so DCSC is the only authority.",
 "Live DCSC panels and exports 2026-08-13 to 2026-08-19; Lenovo Press lp2133", "2026-08-19"),

("tce-ceilings-amd-v3-vs-intel-v4-and-catalog-flag-corrections",
 "SR665 V3|SR655 V3|SR635 V3|SR645 V3|SR650 V4|SR630 V4|D4390", "proven",
 "TCE ceilings: AMD V3 reaches 64C per socket vs Intel V4's 32C; 100GbE is TCE only as PCIe; D4390 has zero TCE parts; and catalog tc flags were wrong in several directions",
 "AMD V3 (SR665 V3 7D9ACTO1WW, SR655 V3, SR635 V3): CPU ceiling BPVJ EPYC 9554 64C 360W 3.1GHz, then BR31 9474F 48C 3.6GHz, BREC 9334 32C 210W 2.7GHz, BREE 9124 16C. Turin C2AQ EPYC 9335 32C 3.0GHz and C2AL EPYC 9535 64C 300W 2.4GHz both hold BU1E despite tc=false in a stored scrape. "
 "No 96-core part is TCE on any AMD platform (C2AN 9645, C2AX 9655P, C2AU 9655, BPVK 9654 are all not TCE). Memory: CBND 64GB 6400 2Rx4 is TCE plus CBNC and CBNB 32GB and CC0A 16GB. NVMe ceiling C0ZT 7.68TB RI and C0ZP 6.4TB MU, also C0ZU 3.84TB, C0ZQ 3.2TB, C18N 1.92TB RI, C18J 1.6TB MU. "
 "M.2: only 480GB is TCE on V3 AMD, see topic m2-boot-rules-v3-amd-vs-v4-intel. Chassis and backplane: BLKK 2U 24x 2.5in and BS7Y 8x 2.5in NVMe Gen5 are TCE, so 24 NVMe bays is TCE-buildable. "
 "INTEL V4 (SR650 V4 7DGDCTO1WW, SR630 V4 7DG9CTO1WW): the TCE CPU tops out at 32C (C5QX 6737P 32C 270W, C5QT 6530P 32C, C659 6527P 24C, formerly down to C5QQ 6505P 12C, which left the list in Sep 2026), same 64GB C0TQ memory ceiling and same 7.68TB and 6.4TB drive ceiling. "
 "Memory geometry: Intel V4 has 8 channels per socket (16 or 32 DIMMs on 2 sockets, so 1536GB is unbuildable) while AMD V3 keeps 12 channels and 24 DIMMs. On any TCE re-spec check the AMD V3 list before assuming Intel V4. "
 "100GbE IS available on TCE but only as PCIe: BK1J Broadcom 57508 100GbE QSFP56 2-Port PCIe is TCE, the OCP version BPPX is NOT, and BFH1 100Gb SR4 QSFP28 transceiver is TCE. It costs a PCIe slot instead of the OCP bay; do not accept a drop to 25GbE. "
 "D4390 JBOD (7DAHCTO1WW) has ZERO TCE parts, so any config containing it can never carry BU1E and JBOD-attached storage always splits into its own config. "
 "CATALOG-FLAG CORRECTIONS (2026-08-19): backplanes, chassis, risers, motherboards, fans and rails showed as non-TCE in a scrape but do NOT gate BU1E (they are structural or auto-added); CABW 30.72TB RI SAS 24Gb holds BU1E (the 7.68TB ceiling applies to NVMe only, so always check SAS before declaring a capacity impossible under TCE); "
 "BM50 440-16i holds BU1E on the AMD V3 platforms examined despite tc=false (on SR650 V4 the 16i controllers are non-TCE, so this is per MTM); BE4T and BE4U ConnectX-6 Lx 10/25GbE (OCP and PCIe) are TCE, so use them when a customer specifies ConnectX-6 25GbE instead of Broadcom BN2T or BK1H. "
 "Use a scrape to generate candidates, never to rule something out; DCSC is the only authority. Related topics: amd-v3-cpu-generation-dictates-dimm-speed, tce-membership-is-per-mtm-and-per-date.",
 "DCSC exports and live panels 2026-08-14 to 2026-08-19; Lenovo Press lp2127, lp1971", "2026-08-19"),

("amd-v3-vs-intel-v4-tce-core-and-clock-matched-price",
 "SR665 V3|SR645 V3|SR635 V3|SR655 V3|SR650 V4|EPYC 9005|Xeon 6", "proven",
 "AMD V3 TCE reaches 64C per socket (2x64C = 128 cores per SR665 V3) against Intel V4's 32C, and clock-matched AMD parts list within about 6 percent of the Intel part; Intel still wins in four cases",
 "PROVEN from exports (BU1E, zero criticals): AMD V3 TCE reaches 64C per socket (C2AL 9535 on SR635 V3 and SR665 V3, BPVJ 9554 on SR655 V3 and SR665 V3); SR665 V3 has 2x 64C TCE builds = 128 cores per server; SR645 V3 is proven to 2x 32C (C2AQ 9335). Intel V4 TCE tops out at 32C. "
 "CLOCK-MATCHED DCSC LIST PRICES (2026-09-23, per unit): 9135 16C 3.65GHz lists about 6 percent below 6517P 16C 3.2GHz and about one third of 6724P 16C 3.6GHz; 9335 32C 3.0GHz lists about 6 percent below 6530P 32C 2.3GHz. "
 "COUNTEREXAMPLE to state honestly: Intel 6515P 16C lists about 7 percent BELOW AMD 9115 16C (and the 9115 is not TCE-proven). AMD 9015 8C is cheap on a July street scrape but not TCE-proven. "
 "WHERE INTEL STILL WINS: existing Intel clusters (no cross-vendor live migration between Intel and AMD hosts), Nutanix HX TCE is Intel V4 only, and SR650a V4 is the platform for TCE GPU builds. "
 "Do not carry generic 'AMD is always cheaper' claims into a quote; compare the exact SKUs at the time. Related topics: tce-ceilings-amd-v3-vs-intel-v4-and-catalog-flag-corrections and amd-v3-first-pick-claims-that-failed-verification.",
 "DCSC exports and live panel 2026-09-23", "2026-09-23"),

("amd-v3-first-pick-claims-that-failed-verification",
 "AMD V3|SR645 V3|SR665 V3|SR675 V3|HX665 V3|Xeon 6", "flagged",
 "Claims used in an 'AMD V3 first pick' pitch that failed verification, plus the supply-side citations that did hold up",
 "VERIFIED CITATIONS (checked against the published articles, not just agent-reported): Intel's CEO said at a Splunk conference that Intel is meeting about 50 percent of customer CPU demand (Motley Fool 2026-09-19); this is CPU demand, not server-specific. "
 "On Intel's Q4 2025 call, supply constraints 'meaningfully limited' its ability to capture demand and the CFO said capacity was being shifted to data center (The Register 2026-01-23). "
 "AMD reached 34.5 percent server CPU UNIT share in Q2 2026, up from 27.3 percent (Mercury Research via The Register 2026-08-21); a research pass mislabelled it revenue share, it is units. Lenovo x86 uptime: 12 straight years best per ITIC, see topic lenovo-itic-x86-uptime-ranking-12-years. "
 "CLAIMS THAT FAILED VERIFICATION, do not reuse: AMD 'cheaper by a fixed dollar amount' (DCSC lists say otherwise); a VMmark4 '64 versus 86 cores' comparison; about 25 percent licensing savings; '22 versus 29 servers, 10 percent TCO, 22 percent power'; the tagline 'More VMs. Same License. Better Value.' attributed to an AMD source (none found); and every vertical-slide statistic (45 percent database licensing, more than 1000x AI, 71 percent power). "
 "One slide also marked SR675, SR685a, SD665, SE455, MX455 and HX V3 as 'Available in TCE' with no BU1E evidence (SR675 V3 0 of 2 exports, HX665 V3 0 of 4). A promotional discount claimed for a fixed end date was unverified and left out. "
 "Status is flagged because these are claims to avoid, not rules. Related topic: amd-v3-vs-intel-v4-tce-core-and-clock-matched-price.",
 "The Register 2026-01-23 and 2026-08-21; Motley Fool 2026-09-19; Mercury Research; DCSC exports 2026-09-23", "2026-09-23"),

("tce-rack-chassis-and-tied-order-void-fast-ship",
 "ALL|7D6E rack|D4390", "proven",
 "DCSC hard rule: TCE order-to-ship is void with a rack chassis OR any tied order that holds non-TCE product, which is why racks and JBODs are quoted separately",
 "DCSC throws this warning: 'Please note that Lenovo Top Choice Express 10 business day order to ship is not supported when configured with a rack chassis or when ordered along with Non-TCE products (Tied Order).' Two separate killers, and the second is the one people miss. "
 "1. A RACK CHASSIS in the configuration voids TCE, so a TCE build is servers only. Racks, PDUs and factory rack integration come off the Lenovo quote and are picked up by the partner as a service line. "
 "2. A TIED ORDER containing any non-TCE product voids TCE for the whole order, not just the offending config. This is broader than the per-config BU1E rule: BU1E is per configuration, but a tied order drags everything down together. "
 "So non-TCE items (JBOD enclosures such as the D4390, which has zero TCE parts, 96-core CPUs, oversized drives) must be quoted as a genuinely separate order, not merely a separate config on the same quote. "
 "PLAN for a large bid where lead time is the selling point: (a) a servers-only TCE order, (b) a separate standard-lead order for anything non-TCE, (c) racks and integration as partner scope. Doing this kept BU1E on every server config of a large multi-config bid. Say it to the partner up front; it reads as a Lenovo limitation if it surfaces late. "
 "Note the DCSC message quotes 10 business days order to ship; other Lenovo materials quote about 21 days order to delivery, so state which milestone you mean. See also tce-core-rules.",
 "DCSC warning message seen 2026-08-19 on a multi-config rack build", "2026-08-19"),

("sr650-v4-tce-8-port-controller-cap-and-3-5in-bays",
 "SR650 V4|7DGDCTO1WW", "proven",
 "SR650 V4 3.5in: 12 usable bays and TCE are mutually exclusive because every 16i controller is non-TCE; the proven pairing is C46N plus B8NY (8 SAS/SATA bays)",
 "UPDATE 2026-09-30: the DCSC crawl of that date flags the 940-16i adapters B8NZ and BM35 as TCE on 7DGDCTO1WW, so this ceiling may no longer hold; build C3RW + B8NZ and check BU1E before relying on either answer (see dcsc-crawl-2026-09-30-tce-changes). "
 "As of 2026-09-10: on 7DGDCTO1WW, 12 usable 3.5in bays and Top Choice Express cannot coexist. The chassis C3QL (12x 3.5in) and 12-bay backplane C3RW are both TCE parts, but EVERY 16i controller on the MTM is non-TCE: B8P0, BM35 and B8NZ (940-16i), B8P1 and BM50 (440-16i); B8P0 940-16i Internal was also not offered in live DCSC on SR650 V4 in July 2026 despite a catalog TCE flag. "
 "The only TCE controllers are B8NY 940-8i and C0TU 545-8i, both 8-port, and one non-TCE part drops BU1E for the whole config. "
 "PROOF from exports, not inference: every config using C3RW is paired with a 16i (BM50, B8NZ) and carries TCE = no; every config using C46N (8x 3.5in SAS/SATA plus 4x 3.5in NVMe) is paired with B8NY or C0TU and most carry BU1E with zero criticals (14 configs). C46N plus B8NY is THE validated 3.5in pairing. "
 "So the TCE ceiling is 8 SAS/SATA drives (84TB usable at RAID 5 with 12TB drives). C0TU 545-8i cannot do RAID 5 or 6, so any parity build needs B8NY plus AUNP SuperCap, C21H supercap cable and C1XV SAS cable. Check the controller port ceiling BEFORE picking a backplane on any TCE build. "
 "TCE 3.5in HDDs on this MTM: C4DA 12TB SAS, C4D7 16TB SATA, C4D5 20TB SATA, C4D6 20TB SAS, C2BH 24TB SAS. Array codes: 5978 configured RAID plus B9XE RAID 5, B9XF RAID 6 or B9XG RAID 10, plus BA12 drives-in-array-1 and 2302 RAID Configuration. "
 "SINGLE SOCKET at 16 cores is often the right answer: one 16C part gives 16 cores and 8 memory channels, which takes 8x 64GB = 512GB fully balanced at 1DPC, is cheaper than two 8C parts and keeps per-core software licensing at 16. Single-socket configs need BEYJ CPU dummy and C3RM 1P air duct filler; drop both when populating the second socket. "
 "Related topics: sr650-v4-tce-backplanes-chassis-and-parts, dcsc-raid-controller-details-cff-nvme-and-supercap.",
 "DCSC exports (validated corpus) 2026-09-09; Lenovo Press lp2127", "2026-09-10"),

("sr650-v4-tce-backplanes-chassis-and-parts",
 "SR650 V4|7DGDCTO1WW", "proven",
 "SR650 V4 TCE backplanes, chassis and part list read from live DCSC on 2026-08-19: every TCE controller is 8-port, C46N is the mixed HDD+NVMe backplane, SR650 V3 has zero TCE backplanes",
 "Read from DCSC screens 2026-08-19 (where they disagree with a catalog scrape, these win). CONTROLLERS: C0TU RAID 545-8i PCIe Gen4 12Gb (no RAID 5/6, 0/1/10 only); B8NY RAID 940-8i 4GB Flash (full RAID 5/6/50/60 plus cache); NVMe RAID via VROC B96G Premium, BR9B Standard, BZ4W RAID1-only. BM50, BM51 and B8P1 (440-series) are not TCE. "
 "CONSEQUENCE: the maximum SAS/SATA bay count buildable under TCE is 8; a 12-bay all-SAS backplane cannot be driven and errors. "
 "TCE BACKPLANES: C46N 8x 3.5in SAS/SATA plus 4x 3.5in NVMe (the one for a mixed HDD plus flash node: 8 SAS bays match the 8i exactly and the 4 NVMe bays bypass the RAID controller, Xeon 6 drives NVMe direct via VMD with no retimer needed on V4); C3RW 12x 3.5in SAS/SATA (TCE as a part but not buildable with an 8i); "
 "C4DB 12x 3.5in SAS/SATA (GPU configs only, 8 drives max); C3RU 8x 2.5in AnyBay; C46P 8x 2.5in NVMe (no SAS controller required); C3RT 8x 2.5in SAS/SATA; C46J middle 4x 2.5in NVMe Gen5; C46H rear 4x 2.5in NVMe Gen5; C46G rear 4x 2.5in AnyBay Gen5. "
 "CHASSIS: C3QL 12x 3.5in and C3QK 24x 2.5in are TCE; C3QM EDSFF E3.S is not. "
 "WHY SR650 V4 for a mixed HDD plus NVMe node: it is the only 2U platform where a 3.5in HDD front and an NVMe tier are both TCE. SR665 V3 (AMD) has a TCE 12x 3.5in front but the BDY7 mid-bay NVMe is not TCE. SR650 V3 (Intel) has ZERO TCE backplanes in the source corpus, so never use it for a TCE build. "
 "OTHER TCE PARTS ON THE MTM: C5QT 6530P 32C 225W and C5QX 6737P 32C 270W (32C is the ceiling); memory C0TQ 64GB, C0U9 32GB and BYTJ 32GB at 6400 (C0U2 16GB was listed as TCE here in Aug 2026 but is not TCE on HX650 V4); drives C2BH 3.5in 24TB SAS, C4D6 3.5in 20TB SAS, C0ZT 2.5in 7.68TB U.2 NVMe; NIC BPPW 57504 25GbE 4-port OCP. "
 "MEMORY GEOMETRY: Xeon 6 has 8 channels per socket, so 16 DIMMs at 1DPC on 2 sockets; 768GB is unbuildable balanced (you get 512GB as 16x 32GB or 1024GB as 16x 64GB). Related topic: sr650-v4-tce-8-port-controller-cap-and-3-5in-bays.",
 "Live DCSC screens 2026-08-19; Lenovo Press lp2127", "2026-08-19"),

("sr650-v4-16-core-tce-cpu-live-panel-2026-09-10",
 "SR650 V4|7DGDCTO1WW", "proven",
 "SR650 V4 16-core TCE CPU list on the live panel 2026-09-10 is only C5RD 6515P and C5R5 6724P, a roughly 4.9x per-socket price gap with nothing between; C5QV is not offered",
 "Read off the live DCSC panel 2026-09-10: the 16-core TCE list on SR650 V4 (7DGDCTO1WW) is ONLY C5RD 6515P 2.3GHz and C5R5 6724P 3.6GHz. C5QV 6517P 16C 3.2GHz carried tc=true in a stored 2026-07-28 catalog scrape and was TCE in earlier exports, but the panel did not offer it under TCE on this MTM. "
 "C5R5 lists at about 4.9x the price of C5RD per socket, so the 16-core choice is genuinely cheap-and-slow or expensive-and-fast with no middle option. The 6515P is the right economic call, and the argument that closes the clock gap is that Xeon 6 does materially more work per clock than the older Cascade Lake parts customers are usually replacing. "
 "This was the second catalog-over-panel error in one day (the first was BS7F on SR645 V3, see topic m2-boot-rules-v3-amd-vs-v4-intel). Before naming a part as a TCE option, check whether any validated export contains it on that MTM; if none does, say 'catalog says yes, confirm in the panel' rather than recommending it. "
 "Related topics: tce-membership-is-per-mtm-and-per-date and the existing fact sr630-v4-tce-cpu-live-panel (same finding on SR630 V4 on 2026-09-23).",
 "Live DCSC panel 2026-09-10; DCSC exports", "2026-09-10"),

("sr630-v4-8-core-cpu-costs-more-than-16-and-24-core",
 "SR630 V4|SR650 V4|Xeon 6", "proven",
 "On SR630 V4 and SR650 V4 the only 8-core CPU (C5R7 6714P) is a high-clock premium SKU listing about 3.8x the 16C C5RD, so cutting cores to cut price backfires",
 "On SR630 V4 (7DG9CTO1WW) the TCE processor ladder is not monotonic in core count (Aug 2026 exports): C5QQ 6505P 12C 150W 2.2GHz; C5RD 6515P 16C 150W 2.3GHz; C5QV 6517P 16C 190W 3.2GHz; C5QR 6520P 24C 210W 2.4GHz; C5QT 6530P 32C 225W 2.3GHz; and C5R7 Xeon 6714P 8C 165W 4.0GHz. "
 "The 8-core is the MOST expensive part on the list because it is a high-frequency per-core-licensing SKU, not an entry chip: about 3.8x the 16C C5RD and about 2.1x the 24C C5QR. Dropping from 16C to 8C on this platform adds cost; the cheapest entry was the 12C. The same pattern holds on SR650 V4. "
 "STALE-LADDER UPDATE (2026-09-23 and 2026-09-25 live panels): the only TCE 16C part on 7DG9CTO1WW is C5R5 6724P (C5QV 6517P is not TCE), and the TCE 8C (6714P) and TCE 16C (6724P) are both high-clock and both list higher than C5QR 6520P 24C, so on the live panel the 24C is the cheapest TCE Intel CPU on SR630 V4. Prices are still a guide; TCE status is not, check the panel. "
 "Pairs with the Windows Server 16-core minimum: since Standard licenses 16 cores per server anyway, a 16C part is the first config where the customer uses all the cores they license. General lesson: never assume fewer cores means a lower price, pull the actual DCSC CPU list per MTM first. "
 "See topic windows-server-16-core-minimum-per-server and existing facts sr630-v4-tce-cpu-live-panel and sr630-v4-6724p-and-psu-ceiling.",
 "DCSC exports Aug 2026; live DCSC panels 2026-09-23 and 2026-09-25", "2026-09-25"),

("sr645-v3-4x3-5in-thermal-table",
 "SR645 V3|7D9CCTO1WW", "proven",
 "SR645 V3 4x 3.5in thermal table: every row starts at 200W TDP, so a CPU under 200W has no validated 4x 3.5in row; performance heatsink is mandatory",
 "Source (read 2026-09-10): pubs.lenovo.com/sr645-v3/thermal_rules, which the product guide lp1607 points to rather than reproducing. The guide's storage section confirms 4x 3.5in is the hard maximum bay count on this platform and that all four can be SAS/SATA (4x 3.5in hot-swap SAS/SATA, AnyBay, or 2x SAS/SATA plus 2x NVMe). "
 "THE COMPLETE 4x 3.5in ROWS (front drive bays only): 25C (Note 1) 320W <= TDP <= 400W, Performance heatsink, Performance fans, 1 or 2 CPUs, DIMMs >=96GB Y1. "
 "30C: 200W <= TDP <= 240W, Performance heatsink, Standard OR Performance fans, 1 or 2 CPUs, Y4. "
 "35C: 200W < TDP <= 400W, Neptune Direct Water Cooling heatsink, Standard or Performance fans, 2 CPUs, Y7. "
 "35C: 200W < TDP <= 300W, Performance heatsink, Performance fans, 1 or 2 CPUs, Y2. "
 "45C: 200W <= TDP <= 240W, Performance heatsink, Performance fans, 1 or 2 CPUs, Y2. "
 "Legend: Y2 = yes when max ambient <= 30C; Y4 = yes when using the performance fan; Y7 = yes when max ambient <= 30C and performance fan installed. Note 1 applies only to 9555, 9555P, 9565, 9645, 9655, 9655P, 9745, 9825 and 9845. "
 "THE RULE THAT MATTERS: every 4x 3.5in row starts at 200W. There is NO row for TDP below 200W, so a sub-200W CPU has no validated 4x 3.5in thermal configuration. INFERENCE (not confirmed by DCSC message text): this is almost certainly why a build that paired C2AG EPYC 9115 16C (125W) with the BLK3 4x 3.5in chassis threw a DCSC Critical. "
 "The doc states that 'drive configuration does not trigger heatsink selection; rather, ambient temperature and TDP do', so an earlier explanation blaming an all-HDD front colliding with the 8-fan kit was WRONG. "
 "PRACTICAL CONSEQUENCES: BQ26 Performance heatsink is mandatory at every supported TDP on this drive config; single processor IS supported (1 or 2 on four of five rows, no 2-CPU minimum); at 30C ambient Standard fans are permitted (BH9N, cheaper than BH9M) while Performance fans buy the 45C row, the widest ambient band and worth keeping for sites that are not climate-controlled; "
 "8 fan positions in the 1U (single-socket builds run a 6x fan kit plus 2x B8NJ dummy); pick a CPU at 200W or above (BREE EPYC 9124 16C is exactly 200W and sits in the most permissive band); DIMMs under 96GB are unaffected by the Y-notes (BQ3D 64GB is clear); 3.5in is incompatible with the Neptune L2A liquid-cooling module, and EDSFF and front-PCIe configurations exclude 3.5in bays entirely. "
 "PROCESS LESSON: lp1607 does NOT contain the thermal tables. For any heatsink, fan or ambient question go straight to pubs.lenovo.com/<model>/thermal_rules and ask for the literal table rows, because a summary loses the TDP bands that carry all the meaning.",
 "pubs.lenovo.com/sr645-v3/thermal_rules read 2026-09-10; Lenovo Press lp1607", "2026-09-10"),

("copper-10gbe-is-tce-on-ocp-100gbe-ocp-is-not",
 "SR645 V3|7D9CCTO1WW|AMD V3", "proven",
 "On SR645 V3, copper 10GbE and 1GbE ARE TCE on OCP (C4GB, B5ST, BPPY, BW97, B5T1); the 'PCIe-only' TCE rule is specific to 100GbE",
 "On SR645 V3 (7D9CCTO1WW) the catalog carries BOTH C4GC Broadcom 57412 10GBase-T 4-Port PCIe and C4GB the same adapter as OCP, and both carry the TCE badge. So do BPPY Intel X710-T4L 4-port OCP, B5ST Broadcom 57416 2-port OCP, BW97 I350 1GbE 4-port OCP and B5T1 5719 1GbE 4-port OCP. "
 "This NARROWS the 100GbE rule: '100GbE is TCE only as PCIe, the OCP version is NOT' is true for 100GbE specifically (BK1J yes, BPPX no) and must not be generalised to all speeds. At 10GbE and 1GbE the OCP versions are TCE. "
 "Always check for the OCP twin before spending a PCIe slot; on the build where this was found it saved a slot and gave a true 1:1 with the competitor's OCP 3.0 NIC. "
 "WHY AN EXPORT-ONLY CHECK MISSED IT: a part search on the MTM for Base-T or 1GbE returned zero hits because no copper-NIC config had ever been built on it, while the catalog listed all seven. Exports answer 'what is proven to build' and the catalog answers 'what exists'; query both, a miss in one is not an absence. "
 "RELATED VALIDATION FACT: every validated dual-socket BU1E SR645 V3 config on the MTM uses 8 fans, so a build carrying a single BH9M fan under-specifies the thermal kit. See existing fact 8x-10gb-sfp-on-sr630v4-sr645v3 and topic psu-voltage-rule-230v-only-vs-dual-voltage-and-redundancy.",
 "DCSC catalog and exports for 7D9CCTO1WW 2026-09-03", "2026-09-03"),

("tce-is-not-v4-only-40-v3-configs",
 "ST250 V3|SR665 V3|SR645 V3|SR635 V3|SR250 V3|SR655 V3", "proven",
 "Top Choice Express is NOT V4-only: six V3 families have BU1E configs (40 in total); only Intel mainstream V3 (SR630 V3 and SR650 V3) genuinely has zero TCE",
 "CORRECTION established 2026-08-28: the premise that TCE is V4-only is false. Counted from the validated export corpus, configs carrying BU1E with zero Criticals: ST250 V3 7DCECTO1WW 14 of 17; SR665 V3 7D9ACTO1WW 9 of 22; SR645 V3 7D9CCTO1WW 7 of 14; SR635 V3 7D9GCTO1WW 5 of 15; SR250 V3 7DCLCTO1WW 3 of 4; SR655 V3 7D9ECTO1WW 2 of 8. That is 40 TCE configs on V3 platforms: the program shape is AMD V3 plus the entry 250-class V3, not 'V4 only'. "
 "FAMILIES WITH ZERO TCE in the corpus: SR630 V3, SR650 V3, ST650 V3, HX665 V3, HX630 V3, HX630 and HX650 gen1. The Intel mainstream V3 pair (SR630 V3 and SR650 V3) is the confirmed dead end (SR650 V3 has zero TCE backplanes). For the rest, zero-seen means UNKNOWN, not unavailable: warn and check the panel, never conclude it is impossible. "
 "EVIDENCE CAVEAT: ST650 V3 and gen1 HX650 each rest on a single observed config, and SR675 V3 (0 of 2), SE450 (0 of 3) and ThinkAgile MX630 V4 (0 of 2) are too thin to call. If any ever turns up a BU1E config, move it to the proven set. Note HX630 V4 is the LARGEST TCE platform in the corpus (71 TCE-clean configs), so do not confuse it with gen1 HX630. "
 "Related topics: tce-ceilings-amd-v3-vs-intel-v4-and-catalog-flag-corrections and tce-membership-is-per-mtm-and-per-date.",
 "DCSC exports (validated corpus) 2026-08-28 and 2026-09-03", "2026-09-03"),

("hx650-v4-all-flash-single-cpu-and-nvme-tce-drives",
 "HX650 V4|7DG4CTO1WW|HX650-Storage V3", "proven",
 "HX650 V4 all-flash builds fine with ONE CPU (an earlier '2 processors required' claim was disproved in live DCSC); all-flash uses Flash Node Config B0SW, and 1.92/3.84/15.36TB NVMe are TCE",
 "CORRECTION 2026-08-06: the claim that all-flash HX650 V4 (7DG4CTO1WW) REQUIRES 2 processors is WRONG. It came from a guide extraction (which put the 1-CPU option only on HX650 V4 Storage 7DG4CTO2WW) and was disproved by two live DCSC builds on 7DG4CTO1WW, both all-flash, both 100 percent TCE with BU1E present, exported with zero Criticals: "
 "one with C659 Xeon 6527P 24C qty 3 across 3 nodes = 1 CPU per node, where DCSC's own B6C1 Node Cores = 72 (24 x 3, not 144); one with C5QV 6517P 16C x3 = 1 per node, B6C1 = 48. "
 "WHAT IT MEANS: when a Nutanix sizer calls for a single-socket node, do NOT concede that the core count must double; check HX650 V4 (2U) first. On the source cluster this saved 24 NCI cores. "
 "OTHER VERIFIED FACTS: V4 has no 1100W PSU (options 800, 1300, 2000, 2700, 3200W), so use 1300W Titanium (C0U4 or C2Y9); V4 uses XCC3, not XCC2; all-NVMe drops the 440-16i SAS HBA (direct-attach), NVMe backplane C46P (8x 2.5in NVMe, up to x3 = 24 bays). "
 "HYBRID VS FLASH: the Nutanix Hybrid Node Config B0SV exists only on HX650 V4 Storage (7DG4CTO2WW); all-flash models (7DG4CTO1WW, 7DG3CTO1WW) use Flash Node Config B0SW. An earlier note that the Storage model is entirely non-TCE is superseded by topic hx650-v4-storage-joined-tce-and-single-socket-tce-ready. "
 "NVME TCE FLAGS: 1.92TB C1AC and 3.84TB C3Q9 are TCE, C3QG 15.36TB is TCE, C1X9 7.68TB is NOT TCE; a cluster asking 4x 7.68TB per node was built as 2x C3QG 15.36TB per node (same 30.72TB raw, all-TCE, half the drive count). "
 "LESSON: Lenovo Press guide extractions were wrong twice on this platform (the 2-CPU minimum and the NVMe TCE column); live DCSC is the only authority. First step in DCSC: load the MTM, TCE filter ON, and check the NVMe list.",
 "Live DCSC builds 2026-08-06; Lenovo Press lp2133", "2026-08-06"),

("psu-voltage-rule-230v-only-vs-dual-voltage-and-redundancy",
 "ALL|HX630 V4|SR650 V4|SR650 V3|AMD V3", "proven",
 "Whether a Lenovo config is power-redundant at 110V is decided by the specific PSU, not the server model; how to read the DCSC Power Report for redundancy",
 "NAMING RULE from the product guides: PSUs labelled '230V/115V' are dual-voltage and run at both about 110V and about 230V. PSUs labelled just '230V' (typically the high-wattage 2000W, 2700W and 3200W class) are 200-240V high-line ONLY and do not power on at 110V. "
 "HX630 V4 (lp2132 p.8) offers 800W, 1300W and 2000W AC PSUs and states that all AC supplies support 230V while some also support 115V, so the 2000W is the 230V-only one and 800W and 1300W support 115V. "
 "REDUNDANCY (N+1) at 110V holds only if ONE surviving PSU, at its often-derated 110V output, covers the node's full peak draw. So even a 115V-capable PSU can fail redundancy at 110V if the load exceeds one supply: an 800W on a dual-CPU plus many-NVMe node is marginal, a 1300W has headroom. "
 "READING THE DCSC POWER REPORT: utilization percent = worst-case DC power divided by the capacity base. With 'N+N with over-subscription' the base is 1.2x one PSU (750W becomes 900W); 'without over-subscription' the base is one PSU at its low-line rating. "
 "Measured on real reports: an SR650 V3 750W Gen2 PSU (BNFG) delivers the full 750W at 115V (no derating), while an SR650 V4 1300W CRPS PSU (C0U5) derates to about 1000W at 115V. Sanity check for any quote: worst-case DC watts divided by a single PSU's low-line rating below 100 percent = true redundancy without throttle. "
 "GOTCHA: a Nutanix or ThinkAgile HX sizer 'Hardware Summary' export lists CPU, RAM, drives and NICs but NOT the PSU. To answer redundancy definitively, get the PSU wattage from the full DCSC quote or its Power Report tab. See topic psu-part-numbers-by-voltage-and-us-wall-cords.",
 "Lenovo Press lp2132 p.8; DCSC Power Report tabs 2026-07-10", "2026-07-10"),

("psu-part-numbers-by-voltage-and-us-wall-cords",
 "AMD V3|SR650 V4|HX630 V4|FX630 V4|SR250 V3", "proven",
 "PSU feature codes by input voltage (AMD V3 and V4) and the NEMA wall-cord codes for 115V sites; a 230V-only PSU with a 120V cord will not power on",
 "AMD V3 (SR635/645/655/665 V3), catalog-verified 2026-09-03 on 7D9CCTO1WW. 230V-ONLY: BLKH 1100W Titanium, BPK9 1800W Titanium, BMUF 1800W Platinum v2, BR1X 750W Titanium v3, C07V 750W Titanium v4. MIXED-MODE 230V/115V: BNFH 1100W Platinum v3 and BNFG 750W Platinum v3. "
 "TRAP: at 1100W the Titanium option is 230V-only and the only low-line-capable 1100W is Platinum, so on a 120V site you accept the lower efficiency tier. CCTL 1100W is -48V DC, a different power domain entirely and not a low-line answer. "
 "V4 and entry parts: C0U4 1300W 230V/115V (TCE on 7DG3CTO1WW, 7DG4CTO1WW and 7DG4CTO2WW), C2Y9 1300W and BWM3 or C0U8 800W are 230V/115V, C0U3 2000W Titanium is 230V-only (FX630 V4 uses it, so a 115V site kills FX), V4 has no 1100W (800, 1300, 2000, 2700, 3200W). SR250 V3 BWM5 800W Platinum and BWM3 800W Titanium CRPS are both 230V/115V. "
 "US WALL-OUTLET CORDS (verified in the DCSC catalog 2026-07-10): DCSC quotes default to C13-C14 jumper cords (for a rack PDU). For 115V wall outlets swap to NEMA 5-15P line cords: FC 6313 (2.8m 10A/120V), 6401 (2.8m 13A/120V), and 6370 or AX8A (4.3m variants). All four were TCE-flagged on SR650 V4. "
 "Sizing: the 13A cord (6401) for 1300W PSUs (about 11A max at 120V), the 10A (6313) is fine for 750W and 800W. They are easy to miss in the DCSC cord picker among the C13-C14 jumpers because the server end looks identical. "
 "DCSC GOTCHA (confirmed 2026-07-10): the Line Cord group stays locked at 'None' while jumper cords fill the PSU cord slots. Zero the jumper quantity first and the NEMA line cords become selectable. '115V AC' in the DCSC voltage dropdown is the same US wall power as the cords' 120V or 125V ratings; no voltage change is needed. "
 "VALIDATION LOGIC WORTH COPYING: an automated build once paired the 230V-only 1100W Titanium BLKH with C13-to-NEMA-5-15P 120V cords, which will not power on; the correct part was BNFH. Only a NEMA 5-15P or 5-20P plug, or a single rating at or below 127V, proves a 120V outlet; the C13-to-C14 jumper and C13-to-C20 rack cables are rated 100-250V (voltage-agnostic, the PDU decides), so treating those as low-line would condemn nearly every rack config. "
 "Related topic: psu-voltage-rule-230v-only-vs-dual-voltage-and-redundancy.",
 "DCSC catalog 2026-07-10 and 2026-09-03; DCSC exports; Lenovo Press lp2132", "2026-09-03"),

("dcsc-service-ladder-standard-premier-4hour-plus",
 "ALL|SR250 V3|ThinkSystem", "proven",
 "DCSC A-la-Carte service ladder: Standard NBD and Premier NBD have the SAME on-site response; Premier NBD to 4-hour is a small step, Standard to 4-hour roughly doubles the service line",
 "Read off the live DCSC A-la-Carte service panel 2026-08-28 (SR250 V3, CAD). Prices are per platform but the SHAPE of the ladder is constant. Tiers: Standard (NBD, 9x5 problem determination); Premier Support (NBD, 24x7); Premier Support (4 Hour, 24x7); Premier Support Plus (4 Hour, 24x7). "
 "Ratios to Standard NBD at 3 years: Premier NBD about 2.2x, Premier 4-hour about 2.3x, Premier Plus about 4.6x; at 5 years about 2.0x, 2.2x and 4.4x. "
 "THE THING PEOPLE GET WRONG: Standard and Premier NBD have the SAME on-site response. Both are Next Business Day with Lenovo technician-installed parts; Premier does not get an engineer there faster. What Premier adds is problem determination 24x7 instead of 9x5, direct access to senior-level engineers instead of first-line, and end-to-end case management. "
 "Never describe Premier NBD as '24x7 response': the 24x7 is the phone and problem-determination window, the response is still NBD. The 24x7 RESPONSE tier is a separate, more expensive line. "
 "PREMIER NBD TO PREMIER 4-HOUR is only about +3 percent at 3 years and about +9 percent at 5 years, cheap and worth offering to anyone already on Premier who cares about downtime. BUT ALWAYS STATE THE BASELINE: from STANDARD NBD, which is what a cost-sensitive small build usually sits on, 4-hour roughly DOUBLES the service line (about 2.3x at 3 years, 2.2x at 5 years). Never say '4-hour adds very little' without checking which tier the config is on. "
 "PREMIER SUPPORT PLUS is usually not worth it on small deals: it bundles Keep Your Drive (KYD) and XClarity One PSP plus AI-driven failure detection and a service manager (SEM) for onboarding and reviews. At 3 years PSP was about 1.8x Premier 4-hour plus KYD. It earns its place on estate deals with real reporting needs. "
 "TERMS AND ADD-ONS: the panel prices only to 5 years, but 6-year terms exist (Standard NBD 72 months and KYD 72 months are selectable) and are not on the a-la-carte grid, so pull 6-year prices from DCSC rather than extrapolating. Keep Your Drive is a separate add-on (7Q01CTSAWW) EXCEPT inside Premier Support Plus, which includes it; attach it where regulated or financial data lives on the drives. "
 "SR250 V3 specifics: 8x5 NBD maps to 7Q01CTS1WW SERVER STANDARD NBD RESP (not the Premier equivalent, so quoting Premier charges more for nothing on response time); a-la-carte SKUs 5WS7C02386 and 5WS7C02388 (3 and 5 year Premier NBD), 5WS7C02392 and 5WS7C02394 (3 and 5 year Premier 24x7 4hr), 5PS7C02401 and 5PS7C02403 (3 and 5 year KYD). Service lines show tc=n in a catalog scrape but do NOT break BU1E, see topic tce-services-and-warranty-do-not-break-bu1e.",
 "Live DCSC A-la-Carte service panel 2026-08-28; DCSC exports", "2026-08-28"),

("lenovo-ds-series-is-netapp-asa-r2",
 "DS3200|DS5200|DS7200|DS5200C|NetApp ASA r2", "proven",
 "Lenovo's answer to NetApp ASA is the ThinkSystem DS Series: spec-identical to ASA r2 (DS3200 = ASA A20, DS5200 = A30, DS7200 = A50, DS5200C = C30), and it stops at DS7200",
 "Lenovo Press LP2296 (updated 14 May 2026) describes the DS Series as powered by a SAN-optimized version of ONTAP, and its key-features list is the ASA r2 feature set: symmetric active-active, a single storage pool accessible to both controllers in an HA pair (NetApp's storage availability zone), simplified GUI, SnapMirror active sync, autonomous ransomware protection, tamper-proof snapshots, multi-admin verification. "
 "THE MATCH IS SPEC-IDENTICAL, not approximate (both vendors' published pages): ASA A20 = DS3200 (MTM 7DP4): 128 GB per HA pair, 48 drives, 3 SAN HA pairs, 0.7344 PB max raw per HA pair. ASA A30 = DS5200 (7DP5): 128 GB, 72 drives, 4 HA pairs, 1.1016 PB. ASA A50 = DS7200 (7DP6): 256 GB, 120 drives, 6 HA pairs, 1.8360 PB. ASA C30 = DS5200C (7DP7): 128 GB, 48 drives, 4 HA pairs, 1.47 PB (QLC). "
 "NetApp's raw figures are exactly drive count x 15.36 TB, which is how the mapping was proved. NetApp computes capacity at 15.3, 30.7 and 61.4 TB where Lenovo labels the same drives 15.36, 30.72 and 61.44 TB; that is the only reason matched PB figures differ in the third decimal, and drive counts match exactly, which is the stronger proof. "
 "DS tops out at DS7200: there is NO Lenovo answer to ASA A70, A90 or A1K. DS Series carries Top Choice Express. The new DS is ONTAP block storage and is nothing like the old Engenio-based DS2200, DS4200 and DS6200; do not confuse them. "
 "Related topics: lenovo-dm-dg-de-crosswalk-to-netapp-and-current-lineup, lenovo-ontap-array-gotchas-personality-metrocluster-minimums.",
 "Lenovo Press LP2296; NetApp published ASA key specifications", "2026-09-11"),

("lenovo-dm-dg-de-crosswalk-to-netapp-and-current-lineup",
 "DM Series|DG Series|DE Series|NetApp AFF|NetApp FAS|NetApp E-Series", "proven",
 "NetApp to Lenovo storage map beyond ASA: DM = AFF A, DG = AFF C, DE = E-Series, plus the no-equivalent list, the current 2026 Lenovo lineup and Lenovo's SAN OS naming",
 "UNIFIED ALL-FLASH: DM Series (ONTAP 9.16.1) = AFF A-Series. DM3200F (7DJ0: 128 GB, 48 drives, 3 HA pairs) is about AFF A20; DM5200F (7DJ2: 128 GB, 72, 4) about A30; DM7200F (7DJ3: 256 GB, 120, 12 HA pairs NAS or 6 SAN) matches AFF A50 exactly. "
 "CAPACITY QLC: DG Series = AFF C-Series. DG5200 (7DHY: 72 drives x 30.72 TB = 2.21 PB) equals AFF C30's published 2.2104 PB; DG7200 (7DHZ: 120 x 61.44 TB = 7.37 PB) equals AFF C60's 7.3680 PB. Exact. "
 "E-SERIES: DE Series = E-Series and EF-Series: DE4200H (7DCA, 7DCQ), DE4800H and F (7DCB, 7DCR, 7DCS, 7DCC), DE6400 (7DB6), DE6600 (7DB7), DE2000H Gen2. Lenovo does NOT call the DE OS SANtricity: the product guides say 'Lenovo SAN OS' 11.60 and 11.80 (zero hits for SANtricity in LP2072, LP1642, LP1643), the same E-Series lineage under Lenovo's label. "
 "FAS-CLASS HYBRID: DM5200H (7DJ1), DM5000H and DM3010H. FC switches: DB Series (DB710S and others) are the Brocade fabric on both sides. "
 "PRIOR-GENERATION EXACT MATCHES: AFF C30 = DG5200 (128 GB, 72 drives, 2.2104 PB both); AFF C60 = DG7200 (128 GB, 120 drives, 7.3680 PB both); AFF A250 = DM5200F (128 GB and 1.1016 PB identical, but DM loses cluster scale, 4 versus 12 NAS HA pairs); ASA A250 = DS3200 (128 GB and 0.7344 PB identical, DS3200 clusters to 3 versus the A250's 6); FAS500f = DM5200F (128 GB and 1.1016 PB identical); AFF C800 = DG7200 on max raw (7.3680 PB) but the C800 is 4U with 1280 GB. "
 "THE RECURRING DIFFERENCE is cluster scale, not the box: Lenovo DM and DG cluster to 3-4 HA pairs (DM7200F is the exception at 12 NAS or 6 SAN). Most NetApp prior-gen models cluster to 12 NAS or 6 SAN. Always ask how many HA pairs the existing cluster has before matching on box specs alone. "
 "CAPACITY GAP IS UNIFIED-ONLY: block figures match exactly because ASA r2 also caps at 15.3 TB drives, but AFF publishes 4.0392 PB per HA pair on A20, A30 and A50 (about 264 drives derived) against Lenovo DM's 48, 72 and 120 drives; AFF lists 12 Gb SAS ports and takes SAS shelves while the all-flash DM is NVMe-shelf only. "
 "NO LENOVO EQUIVALENT: StorageGRID (no object platform in the 265-model DCSC catalogue), AFX, FAS70 and FAS90 class, FAS8300, 8700 and 9500, AFF C80, ASA and AFF A70, A90, A1K, ASA A800, A900 and C800, AFF A800 and A900, EF80, EF300C and EF600C (QLC-only E-Series). "
 "CURRENT LENOVO LINEUP (2026): DM3200F, DM5200F, DM7200F, DM5200H; DG5200, DG7200; DS3200, DS5200, DS7200, DS5200C; DE4200H, DE4800, DE6400, DE6600. WITHDRAWN OR PRIOR GEN: DM5100F, DM7100F and H, DM7000H, DG5000, DG7000, DE4000, DE6000. All of DS, DM and DG share the base chassis BF3C 'ThinkSystem Storage 2U NVMe Chassis' and the same HIC list; the ONTAP personality is the difference. "
 "NETAPP E-SERIES CURRENT: EF50, EF80, E4000, EF300, EF300C, EF600, EF600C; E2800, EF280, E5700 and EF570 are end-of-availability. FAS and E-Series figures came from vendor summaries rather than a NetApp docs page, so treat those as unconfirmed. "
 "Related topic: lenovo-ds-series-is-netapp-asa-r2.",
 "Lenovo Press LP2296, LP2072, LP1642, LP1643; NetApp published platform specifications", "2026-09-11"),

("lenovo-ontap-array-gotchas-personality-metrocluster-minimums",
 "DS Series|DM Series|DG Series|DM5200H|DM7200F", "proven",
 "Lenovo ONTAP array gotchas: personality fixed at purchase, DS has no MetroCluster IP or FabricPool, all-flash DM is NVMe-shelf only, and capacity minimums are enforced",
 "PERSONALITY IS FIXED AT PURCHASE (NetApp states it): a DS array is block-only for life; any chance of file services later means quoting DM or DG. "
 "DS has NO MetroCluster IP and NO FabricPool; DM and DG have both. DS lacks the C4AD 100Gb iWARP MCC-IP adapter that DM and DG carry, which is why it has no MetroCluster; SnapMirror active sync on DS is a different mechanism, not a substitute. "
 "SHELVES: all-flash DM takes NVMe shelves only (DM242N); only DM5200H has the 4-port 12Gb SAS card, and it is expansion-only with no host support. "
 "CAPACITY MINIMUMS ARE ENFORCED: DM7200F 68 TB, DG5200 122 TB, DG7200 245 TB, DM5200H 100 TB NL-SAS or 50 TB flash. The drive minimum is 8 per HA pair almost everywhere (DM3200F allows 6 with 1.92 TB). "
 "The one real capacity gap is unified, not block: Lenovo publishes NVMe up to 15.36 TB on DM (DM7200F = 1.84 PB raw per HA pair) while NetApp publishes 4.0392 PB on AFF A20, A30 and A50. "
 "The product guides name ONTAP by version and list SnapMirror, SnapVault, SnapCenter, FlexClone, FabricPool, MetroCluster IP and RAID-DP or RAID-TEC, so the technical argument stands on its own; the Lenovo and NetApp commercial arrangement was not verified and does not need to be characterised. "
 "FASTEST WAY TO GET NETAPP SPECS: NetApp publishes docs as open source on GitHub in machine-parseable form (repos NetAppDocs/ontap-systems for AFF, ASA, ASA r2, FAS and AFX; NetAppDocs/e-series; NetAppDocs/storagegrid-appliances). Spec files are overview.adoc (older models) or key-specifications.adoc (newer) and contain Max Raw Capacity, Memory, Form Factor, PCIe Expansion Slots, Minimum ONTAP Version, scale-out maximums and Storage Networking Supported. ASA C30 and AFX key specs are genuinely unpublished, so say so rather than guessing. "
 "docs.netapp.com and netapp.com can return HTTP 403 to automated fetchers but read fine in a normal browser; Lenovo Press PDFs (lenovopress.lenovo.com/<id>.pdf) download cleanly and parse with standard PDF tools, search the text for 'System specifications' to land on the spec table. Units: write TB, not TiB.",
 "Lenovo Press LP2296, DM and DG product guides; NetApp documentation on GitHub", "2026-09-11"),

("lenovo-itic-x86-uptime-ranking-12-years",
 "ALL|ThinkSystem", "proven",
 "Lenovo x86 servers ranked best uptime among all x86 platforms for the 12th straight year (ITIC 2025 report, cited in LP1117); it is survey-based, know the methodology",
 "Lenovo Press LP1117 (updated 2026-03-02) cites the ITIC 2025 Global Server Hardware, Server OS Reliability Report: Lenovo x86 servers had the best uptime among all x86 platforms for the 12th straight year. Say twelve, not eleven (an earlier note had 11, one report behind). State it plainly; do not hedge it. "
 "It is the strongest single third-party proof point in a commodity-hardware argument. METHODOLOGY: ITIC runs an independent annual survey of IT managers across thousands of enterprises measuring self-reported unplanned downtime by hardware platform. It is survey data, not lab-measured MTBF, so have the answer ready when an engineer asks 'ranked by what?'. Framed correctly it still wins: twelve straight years of real operators reporting less downtime beats any vendor lab figure. "
 "Offer the current report and actually send it (request the latest ITIC PDF from the Lenovo channel team). "
 "COMMODITY-PARITY POSITIONING: everyone sources the same silicon (same AMD parts, same Broadcom and Mellanox NICs, same NAND and DRAM). Never claim 'you can buy the same part numbers from Dell': Lenovo feature codes are Lenovo SKUs and OEM drives and NICs carry vendor-specific firmware and VPD. Say silicon, not part numbers. Then differentiate on lead time (TCE), ITIC uptime, part-revision consistency across phases, firmware lifecycle tooling and the support model.",
 "Lenovo Press LP1117; ITIC 2025 Global Server Hardware, Server OS Reliability Report", "2026-09-23"),

("lenovo-press-docs-with-excel-export",
 "ALL|Lenovo Press", "proven",
 "Eight Lenovo Press docs are live filterable databases with an Export to Excel button (RAID/HBA, GPUs, servers, SSDs, Xeon, EPYC, racks, rails); backplanes and M.2 adapters have no exportable tool",
 "Eight Lenovo Press docs are interactive databases with an Export dropdown ('Excel - Search results' or 'Excel - All data') plus a Transpose button, not static product guides (found 2026-08-11 by scanning 128 docs for the export-trigger CSS class): "
 "lp1288 RAID adapters and HBAs; lp2265 GPUs; lp1263 ThinkSystem server comparison; lp1261 ThinkSystem SSD portfolio; lp1262 Intel Xeon Scalable reference; lp1767 AMD EPYC reference; lp1287 rack cabinet reference; lp1838 rail kit reference. URL pattern: lenovopress.lenovo.com/<docid>-<slug>. "
 "EXPORT LAYOUT: attributes down column A, products across the columns, one sheet named 'Sheet 1'. It ends with a long '<server> Support' block (one row per server model, for example 'SR650a V4 Support'), which is how you answer 'does part X work in server Y' without opening a product guide. "
 "TWO GOTCHAS: a withdrawal date of 2050-01-01 is a placeholder meaning NOT withdrawn; and the pages default to an 'Availability = Available' filter, so withdrawn parts are missing until you Reset. "
 "NO EXPORTABLE TOOL exists for M.2 adapters (lp0769 is static) or for backplanes; backplane feature codes live only inside each server's product guide, so do not promise a spreadsheet for those. "
 "Reach for these before hand-building a comparison table: a Lenovo-generated export beats an assembled one.",
 "Lenovo Press pages lp1288, lp2265, lp1263, lp1261, lp1262, lp1767, lp1287, lp1838 scanned 2026-08-11", "2026-08-11"),

("sr650a-v4-single-gpu-ships-at-two-gpu-thermal-spec",
 "SR650a V4|7DGDCTO2WW|RTX PRO 6000 Blackwell", "proven",
 "SR650a V4 with one RTX PRO 6000 Blackwell ships built to the full 2-GPU thermal and power spec; the 4-GPU path uses a different GPU feature code and riser cage",
 "A 1x RTX PRO 6000 Blackwell SR650a V4 is a real, buildable, TCE-eligible configuration (proven 2026-09-14 by comparing a 1-GPU TCE export with a 2-GPU TCE export). Lenovo Press LP2128 documents 2-to-4 GPU changes but is silent on 1-to-2. "
 "THE 1-GPU BOX ALREADY CARRIES THE FULL 2-GPU ENVELOPE. Identical in both: CC8X 2U 24K Ultra Fan Module for 600W x6, C0UD 3200W 230V Titanium PSU x2, C9R6 2U FGPU Riser Cage for 600W x2, CBMX 2U Front Double Width Air Duct for 600W x1, C5MT mylar, C3SG 8x25 HDD cage. The only delta between 1 and 2 GPUs is the GPU (CBK8) and one GPU power cable (C3QU). "
 "HEATSINK CAVEAT: the 1-GPU sample used BPDR Standard heatsink with a 250W CPU and the 2-GPU sample used C3QR Performance heatsink with a 270W CPU. That tracks CPU TDP, not GPU count, but two samples cannot fully separate them; confirm before promising. "
 "THE 4-GPU PATH IS A DIFFERENT ECOSYSTEM: the GPU feature code locks to the riser cage. CBK8 always pairs with C9R6 (seen at 1 and 2 GPUs only); CHWT and CHWU always pair with C3S1, and every 4-GPU build uses CHWT plus C3S1. So 1-to-2 within the CBK8/C9R6 family looks mechanically trivial, but 1-to-4 means changing the GPU part number AND the riser cages. If 4 GPUs is ever plausible, start on CHWT plus C3S1. "
 "FIELD UPGRADES (from the LP2128 PDF, found by searching the PDF text, not visible through a web fetch): when a GPU or other high-thermal component is added as a field upgrade, all empty DIMM slots must have a DIMM filler installed for airflow (part 4M27A11810, FC AURS). So Lenovo contemplates GPUs as field upgrades on this platform, but the Processor Neptune Core Module is CTO only and explicitly not a field upgrade. "
 "WHAT THIS DOES NOT PROVE: that Lenovo supports a field upgrade. Exports show what DCSC builds, not support policy. The precise question for Lenovo is whether there is a field-installable option part number for CBK8 on SR650a V4 and whether the 1x configuration is thermally validated at 2x without changing the heatsink or fan kit. See existing fact sr650i-v4-fixed-inference-bom.",
 "DCSC exports (1-GPU and 2-GPU SR650a V4) 2026-09-14; Lenovo Press LP2128", "2026-09-14"),

("sr650a-v4-connectx7-bqbn-and-200g-optics-hidden-by-tce-filter",
 "SR650a V4|7DGDCTO2WW|ConnectX-7", "proven",
 "SR650a V4 BQBN is the ConnectX-7 '200GbE NIC' customers ask for despite the 'InfiniBand Adapter' name; the TCE filter hides the only 200G optic",
 "Verified in DCSC 2026-09-02 on a 4-server SR650a V4 build (4x RTX PRO 6000 each, 1 TB per node). BQBN 'ThinkSystem NVIDIA ConnectX-7 NDR200/200GbE QSFP112 2-port PCIe Gen5 x16 InfiniBand Adapter' is the part. The 'InfiniBand Adapter' name is why reps and customers think the ConnectX-7 is missing from a build that already has it; 200GbE is a native mode. It is TCE on 7DGDCTO2WW. "
 "NOT A SUPERSET OF THE BROADCOM 57608: BQBN is 200Gb per port with NO 400G mode, while the 57608 does 1x 400GbE. The 57608 appears in ZERO exports, so its availability on this MTM is unproven. "
 "THE TCE FILTER HIDES THE ONLY 200G OPTIC: with TCE mode on, the Transceiver and Cables panels top out at 100G (BFH1 QSFP28 optic, AV20 3m 100G QSFP28 DAC). Turn TCE mode OFF and BQJZ appears: 'ThinkSystem NDR/NDR200 QSFP112 Multi Mode Transceiver', 4TC7A81831, supply G, NOT TCE, labelled for InfiniBand so 200GbE Ethernet-mode support must be confirmed before quoting it for Ethernet. CFUD is a 400GbE QSFP112 optic, irrelevant because BQBN cannot do 400G, and its supply is X. "
 "COST: a 200G optic lists at about the same as (slightly above) the card itself, so eight of them cost roughly eight cards' worth server-side. Push 200G optics to the customer's switch vendor: transceivers are coded to the switch and the customer buys both ends, usually cheaper. Give them the spec (QSFP112, 200GbE Ethernet mode not IB-only, MMF or SMF per run) so a wrong buy is not your install problem. "
 "OPTIC OR DAC, NEVER BOTH: a transceiver and a DAC are two ways to make one link. 2x BF10 per node covers the 25GbE Broadcom OCP ports outright; the AV1X 25G DAC is the alternative, not an addition. DACs are coded end to end, so a Lenovo DAC often fails into Arista or Cisco; SR optics plus LC-LC OM4 let each side buy its own coded part. "
 "46C3447 (FC 5053) is a 10Gb SFP+ optic, NOT 25G: it seats in an SFP28 cage and caps the port at 10G, is never the answer for a 25G NIC, and cannot go in a QSFP112 cage at all. "
 "SLOT POOLS ARE SEPARATE: DCSC Message History gives BQBN eligible slots 5, 8, 4, 7, 3B and 6B; the 4 GPUs (CHWT) sit in the front pool 17A, 21A, 19A, 23A. GPUs do NOT consume the NIC slots, so more ConnectX-7 cards can be added; 3B and 6B are low-profile, so an x16 FHHL card will not fit there. See topic dcsc-supply-status-column-vs-tce-badge.",
 "DCSC live panels and Message History 2026-09-02", "2026-09-02"),

("nvidia-certified-inference-ram-and-core-sizing-rule",
 "SR655 V3|SR650a V4|SR650i V4|GPU servers", "proven",
 "NVIDIA-Certified inference sizing rule: system RAM at least 2x total GPU memory spread across all channels and at least 6 CPU cores per GPU; lean GPU builds fall below it",
 "NVIDIA-Certified inference guidance (docs.nvidia.com, 2026-09): system RAM should be at least 2x the total GPU memory, populated across all memory channels, and there should be at least 6 physical CPU cores per GPU. "
 "CONSEQUENCE: 2x RTX PRO 6000 96GB (192GB of VRAM) wants at least 384GB of system RAM; lean builds of 256GB (SR650a V4) or 192GB (SR655 V3) with two such GPUs are BELOW NVIDIA's guideline. Do not trim memory on an LLM box to hit a price without saying it is under the guideline. "
 "PLATFORM NOTES: SR655 V3 is single-socket with DIMM quantity 1, 2, 4, 6, 8, 10 or 12 (lp1610 p.27). EPYC 9004 and 9005 have 12 channels per socket, so 12 DIMMs is the full-bandwidth population. "
 "RELATED GPU BANDWIDTH FACTS: RTX PRO 6000 Server Edition has 1,597 GB/s of memory bandwidth and Max-Q 1,792 GB/s; the RTX 4500 Ada 24GB (C4RX) is 432 GB/s, 200W, Not TCE, max 3 on SR655 V3, so two of them give only 48GB of VRAM, less model capacity than a single 128GB unified-memory ThinkStation PGX. GPU power scales with the platform: the SR650a V4 pair of 600W cards needs a 3200W 230V PSU. "
 "See existing fact a16-is-vdi-not-llm-and-sr655v3-ai-mtm and topic thinkstation-pgx-is-dgx-spark-273gbs-bandwidth-bound.",
 "docs.nvidia.com NVIDIA-Certified inference guidance 2026-09; Lenovo Press lp1610", "2026-09-28"),

("thinkstation-pgx-is-dgx-spark-273gbs-bandwidth-bound",
 "ThinkStation PGX|NVIDIA GB10|DGX Spark", "proven",
 "ThinkStation PGX (30KL) is Lenovo's NVIDIA DGX Spark: 273 GB/s of unified memory bandwidth caps decode speed, so it is a development box, not a department server",
 "ThinkStation PGX (30KL0002US = 1TB model, Lenovo Press LP2321): NVIDIA GB10 superchip, 20-core Arm (10 X925 plus 10 A725), 128GB LPDDR5x unified memory, 273 GB/s, 1TB or 4TB NVMe, 2x QSFP ConnectX-7 plus 1x 10GbE RJ45, 240W USB-C PSU, DGX OS (Ubuntu). Up to 200B parameters on one unit and 405B with two linked over ConnectX-7. LP2321 says it is designed solely for AI development (prototyping, fine-tuning, inference). "
 "SPEED IS BANDWIDTH-BOUND, so model choice matters more than size. Ollama's own tests (v0.12.6, 2025-10-23): gpt-oss-120b 41 tok/s, gpt-oss-20b 58, Llama 3.1 70B q4 only 4.4, Qwen3 32B q4 9.4. Mixture-of-experts models run fast; large dense models crawl. SGLang and llama.cpp beat stock Ollama. Ignore third-party '14 tok/s on 120b' figures, they contradict Ollama's. "
 "CUSTOMER MISCONCEPTIONS: Ollama is the runtime and API, NOT the chat UI (that is Open WebUI; NVIDIA's DGX Spark playbooks cover both). The Ollama API port 11434 has no authentication, so publish Open WebUI through ZTNA and never the API. The Hugging Face risk is pickle-format model files that execute code, not the 2024 Spaces breach; use GGUF or safetensors from official publishers. "
 "VS DGX SPARK FOUNDERS EDITION: same GB10 silicon, so identical performance; the Founders Edition was cheaper than the PGX 1TB in 2026-09. What the PGX adds: a 1-year onsite base warranty (PSREF), Lenovo channel and bid pricing, and a self-encrypting SSD. "
 "VS APPLE MAC STUDIO: decode is bandwidth-bound and the Mac wins it (M3 Ultra about 3.4x Spark per EXO Labs), while the Spark wins prefill (about 3.8x over M3 Ultra) plus CUDA, fine-tuning and Linux headless serving; M5 Ultra versus Spark numbers were unverified, and a claim that a 256GB Mac Studio costs about the same as a PGX is STALE (Apple raised memory-upgrade pricing in 2026 and paused 256GB and 512GB M3 Ultra). "
 "MULTI-USER OR COMPANY-WIDE demand means size a GPU server instead. See topic nvidia-certified-inference-ram-and-core-sizing-rule and existing facts sr650i-v4-fixed-inference-bom, a16-is-vdi-not-llm-and-sr655v3-ai-mtm.",
 "Lenovo Press LP2321; Ollama v0.12.6 benchmark post 2025-10-23; NVIDIA and Apple public specifications 2026-09-28", "2026-09-28"),

("sr250-v3-udimm-xcc2-platinum-and-onboard-raid",
 "SR250 V3|7DCLCTO1WW", "proven",
 "SR250 V3 (7DCLCTO1WW) build facts: UDIMM not RDIMM, remote KVM needs the paid XCC2 Platinum upgrade SBCV, and onboard SATA software RAID AVV0 is TCE-proven and free",
 "Verified 2026-09-11 against 8 TCE-validated error-free exports on 7DCLCTO1WW. UDIMM, NOT RDIMM: C527 16GB and C528 32GB TruDDR5 5600 ECC UDIMM; do not carry DIMM feature codes over from an SR630 or SR650 V4 build, they will not apply. "
 "REMOTE CONSOLE IS A PAID FOD: SBCV XClarity XCC2 Platinum Upgrade. Base XCC2 has no remote KVM or virtual media, so any spec asking for 'onboard management like iDRAC or iLO' needs this line or it does not meet the ask. Same trap on V4 with SCY0 XCC3 Premier. "
 "AVV0 On Board SATA Software RAID Mode is TCE-proven and costs nothing: a viable alternative to the B8NY 940-8i on small builds where the drives are SATA and battery-backed cache is not needed. "
 "M.2 is NOT supported with 8x 2.5in on onboard SATA (lp1802 configuration 6) because it shares those SATA ports. "
 "OTHER VERIFIED PARTS: BWM1 chassis base, BWMG motherboard, BWMW RoT/TPM, BMPU 8x 2.5in SAS/SATA backplane, BMWQ x8/x8 riser, C521 6333P 6C 65W and C524 6353P 8C 65W CPUs, BRG7 2.4TB 10K SAS HDD, BWM5 800W Platinum and BWM3 800W Titanium CRPS (both 230V/115V), AUKP Broadcom 57416 10GBASE-T 2-port PCIe. "
 "SERVICE: 8x5 NBD maps to 7Q01CTS1WW SERVER STANDARD NBD RESP, not the Premier equivalent; Standard and Premier NBD carry the same response, see topic dcsc-service-ladder-standard-premier-4hour-plus. "
 "WINDOWS: SDA9 Standard (16 core) or SDAU Essentials (10 core, 25 users and 50 devices, NOT preinstalled); the 6C and 8C CPUs here still need the full 16-core Standard licence, see topic windows-server-16-core-minimum-per-server. See also existing facts sr250-v3-only-1u-under-23in and sr250-v3-35in-m2-tce-build.",
 "DCSC exports (8 TCE-validated 7DCLCTO1WW configs) 2026-09-11; Lenovo Press lp1802", "2026-09-11"),

("sr250-v3-tce-cpu-and-memory-live-panel-2026-08-28",
 "SR250 V3|7DCLCTO1WW", "proven",
 "SR250 V3 live TCE panel 2026-08-28: only 4C C520 and 8C C524 are selectable, and TCE memory is 16GB C527 only, so 64GB means four DIMMs; SR250 V3 only, do not apply to ST250 V3",
 "LIVE PANEL 2026-08-28 (SR250 V3, 7DCLCTO1WW): the TCE CPU list offered ONLY 4C C520 (6325P 3.5GHz) and 8C C524 (6353P 2.7GHz). The 6C C521 (6333P) is TCE-proven in exports but was NOT selectable in the panel. Recommend the 8C; it is also still under the 10-core Windows Server Essentials cap. "
 "MEMORY ON TCE IS 16GB C527 ONLY. C528 32GB shows TCE-proven in exports and tc=true in a catalog scrape, but it is not offered in the TCE memory panel. So on a TCE build here 32GB is 2x C527 and 64GB is 4x C527, filling all four slots with no cheaper path and no room to grow. Do not recommend 2x C528; it is not selectable (off TCE, 2x C528 would be cheaper and leave 2 slots free, which is why export data misleads). "
 "SCOPE WARNING: this is an SR250 V3 (7DCLCTO1WW) fact and nothing else; it was explicitly scoped so it must not be applied to ST250 V3 or any other model. Every other platform gets its own panel check. "
 "CONSEQUENCE TO STATE TO CUSTOMERS: because 64GB needs four DIMMs, memory becomes the largest single line in the build and the 32GB-to-64GB step is roughly 40 percent of the system price; on a small file or QuickBooks host that will never approach 32GB, the easiest place to defend a smaller spec is memory, putting the money into a longer support term instead. "
 "On SR250 V3 the panel refused a part the exports called TCE-proven twice (C528 32GB and the 6-core C521), so treat exports as a shortlist FOR THIS MTM and ask for the panel before promising a part. Related topic: tce-membership-is-per-mtm-and-per-date.",
 "Live DCSC panel 2026-08-28; DCSC exports", "2026-08-28"),

("sr250-v3-tce-part-list-and-m2-raid-trap",
 "SR250 V3|7DCLCTO1WW", "proven",
 "SR250 V3 TCE-proven part list, and the M.2 trap: BYFF B540i-2i RAID is NOT TCE, the TCE path is BM8X plus BS7Q plus BS7C plus 2x CABU",
 "TCE-PROVEN PARTS (BU1E, zero Criticals, validated exports): BWM1 2.5in chassis base; CPUs C520 and C524 (see topic sr250-v3-tce-cpu-and-memory-live-panel-2026-08-28); C527 16GB and C528 32GB UDIMM; BMPU 8x 2.5in hot-swap backplane; B8NY RAID 940-8i 4GB plus AUNP SuperCap; CDNK RAID 545-8i Internal Adapter (CFF, costs no PCIe slot, but no RAID 5/6); BYLT 1.92TB RI SATA SSD; BRG7 2.5in 2.4TB 10K SAS HDD; AUZV Broadcom 5719 1GbE 4-port; BMWQ x8/x8 riser; "
 "BWM3 800W Titanium CRPS (BWM5 Platinum lists cheaper); BK7W toolless rails; BXBP 1U security bezel. BWMY power interposer is auto-added with dual PSUs. "
 "M.2 BOOT TCE TRAP: BYFF 'M.2 RAID B540i-2i' is NOT TCE and drops BU1E for the whole config. The TCE path is BM8X 2-bay adapter plus BS7Q onboard SATA software RAID plus BS7C RAID 1 plus 2x CABU 480GB (BS7Q plus BS7C proven on ST250 V3, unproven on SR250 V3). An automated BOM mapper may pick BYFF on its own; override it. "
 "SERVICES: service lines show tc=n in a catalog scrape but do NOT break BU1E, proven by a TCE export carrying 5WS7C02386 and 5PS7C02401. "
 "BUILD-ORDER GOTCHA (shared with ST250 V3): changing the chassis or backplane wipes the array. Order: chassis, backplane, 5978, controller, RAID level, drives. "
 "Related existing facts: sr250-v3-35in-m2-tce-build and windows-factory-install-needs-boot-array.",
 "DCSC exports (validated 7DCLCTO1WW configs) 2026-09-28", "2026-09-28"),

("windows-server-16-core-minimum-per-server",
 "ALL|Windows Server 2025", "proven",
 "Windows Server Standard licenses a 16-core minimum per server, so cutting CPU cores saves nothing on the OS and 'downsize the processor' is a false economy",
 "Windows Server 2025 Standard requires every physical core licensed with a 16-core minimum per server; the DCSC part is literally named SDA9 'Windows Server 2025 Standard (16 core)'. Consequence: dropping to a lower core count does not reduce the Windows licence cost. A 16C CPU consumes exactly the 16-core base licence; an 8C CPU still needs the same 16-core base licence, so the customer pays identically for Windows and receives half the compute. "
 "So when a competitor or an earlier quote shows a 16-core CPU on a Windows Server box, the 16C is probably not oversizing, it is sized to the licence floor. Read it that way before proposing a cheaper processor. It commonly bites when an ST250 V3 (8C ceiling) is proposed against a competing box with a 16C Xeon Gold: the hardware saving is real, the licensing saving does not exist. "
 "Additional cores beyond 16 are licensed in 2-core packs (SDCN Standard Additional License 2-core). CAL parts on ST250 V3, all TCE-proven: SDDC 1-User, SDDX 10-User, SDDZ 50-User, SDER RDS CAL. "
 "Moving to Windows Server Essentials (10-core cap) does cut the OS cost, cutting cores never does; see topic windows-server-essentials-vs-standard-plus-cals-under-25-users and existing fact windows-factory-install-needs-boot-array.",
 "DCSC exports and part descriptions 2026-08-20; Microsoft Windows Server licensing terms", "2026-08-20"),

("windows-server-essentials-vs-standard-plus-cals-under-25-users",
 "SR250 V3|ST250 V3|Windows Server 2025", "proven",
 "For 25 users or fewer quote Windows Server 2025 Essentials, not Standard plus CALs: well under half the cost at list; DCSC feature codes for OS and CALs",
 "WINDOWS SERVER 2025 CODES (parent MTMs 7S1SCTO5WW for the OS and 7S1SCTOAWW for CALs; these are NOT in catalog scrapes, only in DCSC exports): SDA9 Standard 16-core English factory-installed; SDAE Standard 16-core MultiLang not-preinstalled; SDAU Essentials 10-core MultiLang; SDAG Datacenter 16-core; SDCN Standard Additional License 2-core; SDDC CAL 1-User; SDDX CAL 10-User; SDDZ CAL 50-User; SDE6 RDS CAL. "
 "THE MOVE on any deal at 25 users or fewer: Essentials is about 0.3x the list cost of Standard plus 5 single-user CALs and needs no CALs at any count. Essentials covers 25 users and 50 devices, caps at 10 cores and 1 socket, and licenses one instance in a physical OR a virtual OSE, so a host running only Hyper-V plus 1 VM is exactly what it permits. "
 "TWO REAL TRADES to state: it is not factory installed (see existing fact windows-factory-install-needs-boot-array), and the 10-core cap means the CPU must stay at or under 10 cores. Single-user CALs (SDDC) cost less than a 10-user pack (SDDX) until roughly 9 users. "
 "TRAP: Essentials does not fit a 16-core CPU and is not a VM-farm licence; do not let anyone anchor on its price for a virtualization host. See topic hypervisor-is-free-guest-windows-is-the-cost and topic windows-server-16-core-minimum-per-server.",
 "DCSC exports 2026-08-28", "2026-08-28"),

("hypervisor-is-free-guest-windows-is-the-cost",
 "SR630 V4|Windows Server 2025|Proxmox VE|VMware ESXi|Nutanix|Azure Local", "proven",
 "The hypervisor is nearly free and guest Windows is the cost; SR630 V4 certified OS list, Standard-vs-Datacenter crossover at about 10 VMs, and the Proxmox raw-disk fork",
 "HARD FRAME: the hypervisor is nearly free; guest OS licensing is the entire cost, and Windows Server is licensed per PHYSICAL HOST CORE so it follows the hardware. Choosing Proxmox does not dodge Windows licensing for Windows guests. "
 "SR630 V4 CERTIFIED OS LIST (Lenovo Press lp1971 p117) is exactly: Windows Server 2022 and 2025, RHEL 9.4 to 10.2, SLES 15 SP6 and SP7 plus 16, Ubuntu 22.04, 24.04 and 26.04 LTS, VMware ESXi 8.0U3, 9.0 and 9.1. Proxmox VE is NOT on it (0 mentions in the guide). Ubuntu 24.04 LTS plus KVM/libvirt is the cheapest CERTIFIED path (the same KVM Proxmox wraps, no licence cost, Lenovo-supported); Proxmox trades certification for a web UI, fine for internal boxes, name the tradeoff. "
 "WINDOWS SERVER 2025: SDA9 Standard (16 core) covers 2 Windows VMs and stacks (another full licence per 2 VMs); SDAG Datacenter (16 core) is unlimited VMs; CROSSOVER AT ABOUT 10 VMs: 5x Standard lists just above 1x Datacenter. CALs are separate and real (SDDX 10-user, SDDZ 50-user). 16-core CPUs align exactly to Standard's 16-core minimum, so there are no 2-core add-ons (SDCN). SDAU Essentials is a trap here because it caps at 10 cores and 1 socket. "
 "HCI ON A SINGLE NODE IS POINTLESS: all its value is distributed storage and failover across 3+ nodes. Proven from real exports: Nutanix Cloud Platform Pro is genuinely PER CORE (Mission Critical costs more per core than Production), so a 1-node 24-core HX630 V4 was several tens of thousands in licensing alone; a 1-node Azure Local (MX630 V4) also carried a mandatory deployment service line on top of the OS. "
 "SCALE COMPUTING: Lenovo IS an official Scale partner (see existing fact scale-computing-on-lenovo); it is a paid per-node subscription and still fails 'cheapest' for one internal box. VMware has zero SKUs in the source exports although lp1971 offers ESXi as a CTO preload. "
 "PROXMOX STORAGE FORK: Proxmox's flagship storage is ZFS and ZFS wants RAW disks; ZFS over hardware RAID is discouraged by both Proxmox and OpenZFS because the controller hides the disks, so ZFS can DETECT corruption but not repair it. Same family as the vSAN, S2D and Nutanix raw-drive rule. "
 "Path A: keep the 545-8i with HW RAID 10 giving one volume on LVM-thin; fully supported by Proxmox, snapshots work, NO BOM change, TCE preserved, every part proven. Path B: swap to a true HBA and use ZFS mirror pairs, which adds checksumming, compression (about 1.3 to 1.5x effective) and zfs send/recv replication; lp1971 p14 confirms SR630 V4 supports a 12Gb SAS/SATA HBA (non-RAID), BUT zero HBAs appear in any of 44 SR630 V4 exports, and BM51 440-8i exists only on SR645 V3, SR630 V3, HX630 and SR655 V3. An unproven part on a TCE bid is how BU1E quietly drops (absence of evidence, not proof of prohibition). ZFS's real wins need a replication target, so they pay off at node two.",
 "Lenovo Press lp1971 p14 and p117; DCSC exports (44 SR630 V4 configs)", "2026-09-23"),

("azure-local-s2d-capacity-witness-and-quorum-rules",
 "Azure Local|Storage Spaces Direct|ThinkAgile MX", "proven",
 "Azure Local storage is Storage Spaces Direct, not vSAN: capacity efficiency by resiliency type, the reserve rule, and two easy errors (3 nodes do not remove the witness or survive two node failures)",
 "Verified against Microsoft Learn 2026-09-14. Azure Local storage is S2D, NOT vSAN. Do not size it with Azure VMware Solution (AVS) material: AVS is VMware on Microsoft-managed bare metal in Azure and uses vSAN FTT and RAID math (3 hosts for FTT=1 RAID-1 at 50 percent, 5 hosts for FTT=2 RAID-1), where S2D does the equivalent in 2 and 3 servers. Azure Migrate has no Azure Local assessment type; its targets are all in-cloud. The Azure Local sizing tool is the ODIN Sizer (azure.github.io/odinforazurelocal/sizer), provided as-is without Microsoft support. "
 "CAPACITY EFFICIENCY (Microsoft Learn fault-tolerance and plan-volumes pages): two-way mirror 50 percent, 2 servers minimum, 1 failure; nested two-way mirror 25 percent, exactly 2 servers, recommended for production 2-node; nested mirror-accelerated parity about 35-40 percent, exactly 2 servers; three-way mirror 33.3 percent, 3 servers minimum; dual parity 50-80 percent, 4 servers minimum. "
 "RESERVE CAPACITY: reserve the equivalent of one capacity drive per server, up to 4 drives, and subtract it from raw BEFORE applying the efficiency percentage. "
 "TWO THINGS EASY TO GET WRONG: (1) going from 2 to 3 nodes does NOT remove the witness. Microsoft: a witness is required at 2 nodes, strongly recommended at 3-4, unneeded at 5+; it is a cloud witness (Azure blob) or file share witness, and a disk witness is not supported with S2D. "
 "(2) A 3-node pool does NOT survive two simultaneous node failures. The pool-quorum table is stricter than cluster quorum: 3 nodes plus witness survives one node, but not 'one then another' and not two at once; only 4 plus witness or 5+ survive two. What three-way mirror actually survives is one node down plus drive failures on another node, the same practical tolerance nested resiliency gives on 2 nodes. "
 "So 2-node versus 3-node is a capacity-efficiency decision, not a resiliency one. Never claim three-way mirror 'survives two simultaneous failures' without saying two DRIVES, or one node plus a drive. "
 "MIRROR VS PARITY FOR SQL: Microsoft explicitly points SQL Server and latency-sensitive workloads at mirroring; mirror-accelerated parity is much slower than mirror, so a SQL-heavy estate rules out the higher-efficiency parity layouts. Units: write TB, not TiB.",
 "Microsoft Learn (Windows Server storage fault-tolerance, plan-volumes, Azure Local documentation) 2026-09-14", "2026-09-14"),

("azure-local-sizer-inputs-dedup-vms-and-vcpu-ratio",
 "Azure Local|ODIN Sizer|Lenovo Sizer", "proven",
 "Azure Local sizer inputs: dedup and compression at 1:1 unless measured, size to POWERED-ON VMs, and use a 4:1 vCPU ratio (2:1 for SQL)",
 "Verified 2026-09-15. DEDUPLICATION AND COMPRESSION: set to NONE (1:1) unless the customer has MEASURED their own ratio. Microsoft publishes NO expected data-reduction ratio for ReFS dedup anywhere in the Azure Local documentation, so any percentage entered in a sizer is invented. ReFS dedup is aimed at VDI-type workloads (active, performance-sensitive, read-heavy, such as Azure Virtual Desktop), is NOT enabled by default (a manual or scheduled job after deployment), and dedupes SQL and backup data poorly. Sizing on an assumed ratio and missing it leaves the cluster short after the money is spent. "
 "Windows Data Deduplication is a DIFFERENT feature from ReFS dedup, may give better savings, suits file servers and backup targets, and cannot run simultaneously with ReFS dedup. "
 "DATA TYPE: pick the general-purpose or server-virtualization profile for a mixed estate; avoid the VDI profile, which carries optimistic dedup assumptions. "
 "NUMBER OF VMs: use the POWERED-ON count, not total objects. RVTools totals include powered-off VMs and templates, and sizing to the graveyard multiplies by the resiliency factor: in one estate 34 powered-off VMs held about 7 TB, which is about 21 TB of raw under three-way mirror. Feed aggregate vCPU, RAM and in-use storage directly if the tool allows it rather than letting it derive from a per-VM template. "
 "vCPU TO PHYSICAL CORE RATIO: 4:1 is the standard default (Azure Migrate uses it for AVS, and the Nutanix Sizer does too). Hold SQL tiers at 2:1 if the tool allows per-tier ratios: oversubscription hurts database latency and buys nothing when SQL is licensed per physical core at host level. This field rarely drives the outcome, because modern Xeon 6 core counts usually leave CPU far from the binding constraint and storage sizes the cluster. "
 "See topic azure-local-s2d-capacity-witness-and-quorum-rules.",
 "Microsoft Learn Azure Local and ReFS deduplication documentation 2026-09-15", "2026-09-15"),

("nutanix-compute-only-clusters-and-external-storage",
 "SR630 V4|SR650 V4|SR645 V3|SR665 V3|Nutanix NCI|AHV|ThinkSystem DM", "flagged",
 "Running Nutanix AHV without HCI on plain ThinkSystem: never standalone, compute-only nodes or an NCI compute cluster on an external array; Lenovo's LP2421 brief is stale and array support is unresolved",
 "AHV is never sold or installed standalone; it ships as part of AOS. There is no supported 'install AHV on any server' path. Nutanix Community Edition is the only whitebox install and it is free, unsupported and non-production. "
 "TWO SUPPORTED WAYS to run Nutanix with no local HCI storage: (1) COMPUTE-ONLY (CO) NODES joined to an existing HCI cluster. AHV clusters only. Nutanix guidance: start at 4 HCI nodes, keep roughly 2 HCI to 1 CO so the storage layer does not saturate, and use 2+ CO nodes if database VMs need HA. The platform still has to be on the Nutanix HCL. "
 "(2) NCI COMPUTE CLUSTER BACKED BY AN EXTERNAL ARRAY, the real 'Nutanix without HCI': no local data drives; the AOS storage controller consumes an external array. GA Dec 2025 or Jan 2026. Minimum 3 CO nodes; 1-node and 2-node NCI compute clusters are unsupported in prod AND non-prod. One array per compute cluster, though one array can serve several clusters. Each AHV vDisk becomes its own array volume; snapshots and clones translate to array-side operations. "
 "ETHERNET ONLY: Nutanix has no plans to support Fibre Channel near or long term; only PowerFlex SDC, NVMe/TCP or NFS. An FC-attached array is NOT on this architecture. "
 "ARRAY AND SERVER MATRIX (DCIG, Apr 2026): Pure FlashArray //X, //XL, //C: Cisco UCS, Dell PowerEdge, HPE ProLiant or Apollo, NO Lenovo, NVMe/TCP, GA. Dell PowerFlex: Dell PowerEdge only, PowerFlex SDC, GA. Dell PowerStore: Dell PowerEdge only, NVMe/TCP, summer 2026. NetApp ONTAP: multi-vendor, NFS, about Q3 2026. Lenovo ThinkSystem storage (ONTAP-based DM series): Lenovo ThinkSystem servers only, NFS, about Q3 2026. An older source said //X and //XL only with no //C; verify on the HCL before quoting. "
 "THE LENOVO TRAP: Lenovo compute is only supported with Lenovo storage. A customer keeping a Pure array cannot buy Lenovo compute nodes for it because Pure's supported-server list is Cisco, Dell and HPE; Lenovo plays only if the array is replaced too. "
 "LENOVO'S OFFER: Lenovo Press LP2421 'Nutanix Compute only Cluster on Lenovo ThinkSystem Servers' covers SR630 V4, SR650 V4, SR645 V3 and SR665 V3 plus ThinkSystem DM and DG, sized 3 nodes small to 8+ large. Its 30 Apr 2026 revision still says it is a work in progress and not generally available, and DCIG targeted about Q3 2026. "
 "IT HAS SHIPPED: a 'Nutanix compute only' selection appeared in DCSC while building an SR650 on 2026-08-14, so the LP2421 brief is stale; trust DCSC over the brief. An automated BOM mapper may return C9U9 'ThinkSystem Virtualization - Max Performance' instead, so pick the Nutanix compute-only option by hand in DCSC. "
 "STILL UNRESOLVED: which external arrays Lenovo compute-only is supported against. Lenovo's validated pairing is ThinkSystem DM and DG (ONTAP over NFS), while Pure's server list is Cisco, Dell and HPE. A DCSC option proves Lenovo will sell it; it does not prove Nutanix's HCL blesses Lenovo servers against a third-party array. So the safe Lenovo answer for supported Nutanix today is still ThinkAgile HX. "
 "Related topics: hx-integrated-system-vs-certified-node-and-7dg4-suffixes, nutanix-no-mixed-hardware-vendors-in-one-cluster.",
 "Lenovo Press LP2421 (30 Apr 2026 revision); DCIG analysis Apr 2026; live DCSC 2026-08-14", "2026-08-14"),

("nutanix-sizing-storage-tell-n-plus-1-cores-and-raw-formula",
 "Nutanix Sizer|HX630 V4|HX650 V4", "flagged",
 "Nutanix sizing heuristics: a large drop in 'future' storage versus 'current' usually means consumed, not required; N+1 licensed-core math and the raw-capacity formula",
 "THE CURRENT-VS-FUTURE STORAGE TELL (heuristic, not confirmed with the customer): when a sizer ask shows compute and RAM cut about 50 percent (normal right-sizing) but storage cut about 80 percent (for example one site 56 TiB to 2.8 TiB, another 36 to 6.2 TiB), the 'future' column is almost certainly collector-measured CONSUMED capacity while 'current' is PROVISIONED. Size storage to current and compute to future, or you are about 100 TB short at migration. Ask what the future storage figure measures. "
 "N+1 CORE MATH (cores that must survive on nodes minus one), verified: 3 nodes of single-socket 24C = 72 licensed and 48 surviving; 3 nodes of single 12C = 36 and 24; 3 nodes of dual 16C = 96 and 64. "
 "STORAGE RAW FORMULA: raw = usable TB x 2 (RF2) divided by 0.9 (CVM and metadata) x N/(N-1) (rebuild headroom). "
 "SINGLE-SOCKET FLOOR DIFFERS BY PLATFORM AND DRIVES NCI LICENSING: HX630 V4 needs 2 populated sockets, so its licensed-core floor is 2x the smallest TCE CPU (16 cores per node with C5R6 8C); HX650 V4 builds single socket (proven, TCE 8C exists there). Single socket saves licensed cores only where the node needs more cores than two smallest TCE CPUs supply, see topic hx650-v4-tce-cpu-list-live-panel-2026-09-03. An earlier version of this note gave 12C as the HX650 V4 floor; that is superseded (12C left TCE and 8C is on the list). "
 "A combined multi-site sizer run is a calculator view, not a consolidation proposal: a Nutanix cluster cannot span sites, so size each site's cluster separately. Units: write TB, not TiB (the Nutanix Sizer emits TiB; convert by x1.0995).",
 "Nutanix Sizer outputs and DCSC exports 2026-08-24; arithmetic verified", "2026-08-24"),

("dcsc-raid-controller-details-cff-nvme-and-supercap",
 "SR630 V4|SR650 V4|ThinkSystem V4", "proven",
 "DCSC RAID controller details: Internal (CFF) versus PCIe Adapter slot cost, port count must cover the backplane, NVMe never attaches to a SAS RAID card, and supercap auto-adds",
 "Verified in live DCSC on SR630 V4 (7DG9CTO1WW) 2026-08-06. (1) INTERNAL ADAPTER = CFF = costs no PCIe slot; ADAPTER = PCIe card = costs a riser slot. The description wording is the tell: CDNK RAID 545-8i Internal Adapter (CFF); B8P0 RAID 940-16i 8GB Flash Internal Adapter (CFF, parity RAID, the ideal fix when slots are tight, BUT it showed TCE in a catalog scrape yet was NOT offered in live DCSC on SR650 V4 7DGD in July 2026, check before promising it); B8NY RAID 940-8i 4GB Flash Adapter (PCIe card, needs a riser). "
 "On the 1U SR630 V4 the riser positions ship as fillers (C1YX cage 1 filler, C1YW cage 2 filler). Populating one costs C1Z7 or C9AR (Full Height plus Low Profile Riser 1 cage) or C1ZC, plus C1YH, C1ZB or C1Z4 for the riser itself. Riser 2 requires CPU 2 populated. "
 "(2) CONTROLLER PORT COUNT must cover the BACKPLANE, not the drive count. An 8i controller has 8 ports, so pair it with C21T 8x 2.5in SAS/SATA, not C21W 10x 2.5in, even when only 3 drives are installed; 16i controllers cover the 10-bay. "
 "(3) NVMe NEVER ATTACHES TO A SAS/SATA RAID CONTROLLER. U.2 NVMe drives behind a 545-8i produce two Critical errors at once: an invalid-drive-selection error naming the drive and a 'Tri-Mode Enablement [CH5Z] is required' error. The fix is almost always to change the drives to SAS/SATA, not to add tri-mode. "
 "(4) RAID 545-8i cannot do RAID 5 or 6 (see existing fact raid-545-8i-two-virtual-drive-limit). A stale or intermediate config CAN export with CDNK and B9XE RAID 5 both present, so an exported BOM is not proof the combination is valid; the live configurator is. "
 "(5) SUPERCAP: adding a 940-series controller auto-pulls AUNP RAID 930/940 SuperCap plus BK70 holder kit plus C21G supercap cable and drops the B8NK Super Cap Holder Dummy. If the dummy survives in a config, the write-back cache does not; check for it. "
 "(6) LENOVO FC HBAs INCLUDE THEIR OPTICS: BA1F QLogic QLE2772 32Gb 2-Port ships with hot-pluggable 32Gb SFP+ short-wave (850nm) LC transceivers (lp1307), so do not quote transceivers separately; only LC-LC fibre jumpers are site-supplied. "
 "(7) TCE narrows the controller list hard: on SR650 V4 the only TCE controllers are the 8-port C0TU and B8NY, which caps SAS/SATA bays at 8, see topic sr650-v4-tce-8-port-controller-cap-and-3-5in-bays. NVMe bays bypass the SAS controller on V4 (Xeon 6 drives them direct via VMD, no retimer needed).",
 "Live DCSC 2026-08-06 and 2026-08-19; Lenovo Press lp1307", "2026-08-20"),

("u3-vs-u2-when-required-and-trimode-dependency",
 "SR645 V3|SR630 V4|SR650 V4|MX630 V4", "proven",
 "When a U.3 drive is actually required versus swappable for U.2, what tri-mode does in Lenovo's catalog (940-series only), and why U.3 kills TCE",
 "U.3 NVMe SSDs have ZERO TCE configs. Measured across 154 exports 2026-09-14: U.2 NVMe SSDs = 22 distinct parts, 257 configs, 223 TCE rows; U.3 NVMe SSDs = 6 parts, 22 configs, 0 TCE rows. If a build needs Top Choice Express, a U.3 data drive is a blocker. "
 "WHAT TRI-MODE IS: generically protocol flexibility (SAS, SATA and NVMe on the same lanes), not RAID, and tri-mode HBAs exist in the industry. But in Lenovo's catalog tri-mode is exclusively a 940-series RAID adapter feature: the enablement parts are CH5Z (Tri-Mode Enablement) and BE38 (940 Series Flash Adapter for U.3 Trimode Setting), and every 440-series HBA in the catalog (BM50 440-16i, B8P7 440-16e, BM51 440-8i) is SAS/SATA only with no NVMe. So on ThinkSystem the 940 is the only controller that can reach NVMe and tri-mode is the switch that lets it. "
 "All 6 tri-mode configs in the exports carry a RAID 940-8i, zero exceptions (SR645 V3 and SR630 V4 only), but 3 of the 6 have NO HW RAID Array lines, so the controller can be present with tri-mode on and no arrays built. Do not assume tri-mode implies configured arrays. "
 "THE REAL DEPENDENCY TEST: U.3 is required only when you want a controller in front of NVMe (hardware RAID on NVMe, or mixed SAS/SATA plus NVMe in one backplane). For direct-attach NVMe it buys nothing. Removing tri-mode is NOT a drive swap: the 940 goes blind to the NVMe drives, they fall back to CPU PCIe lanes and the hardware RAID arrays cease to exist. If the build has no SAS/SATA drives, the 940-8i and its SuperCap become dead cost too. "
 "WORKED EXAMPLE (SR645 V3 control-plane node): 4x C2BV U.3 1.6TB per node in two HW RAID 1 mirrors on a 940-8i via BE38 plus CH5Z on a BB3T AnyBay backplane, boot separately mirrored on M.2 (B8P9). Swapping to C18J U.2 deletes the whole RAID layer. C18J is TCE in 27 of 28 configs; C2BV is TCE in 0 of 2; but C18J never appears on SR645 V3 in the exports, so verify it builds before promising it. "
 "COUNTER-EXAMPLE (ThinkAgile MX630 V4 / Azure Local): no tri-mode, no RAID adapter, direct-attach NVMe on a C21X Gen5 backplane with 5977 'no configured RAID required'. S2D mandates direct-attach with no RAID, so U.3 there is pure cost plus a TCE blocker; the same platform was built both U.3 (C2BS) and U.2 (C0BA) on the identical backplane, proving U.3 is not required. "
 "See existing fact sr650-v4-nvme-raid-three-paths and topic azure-local-s2d-capacity-witness-and-quorum-rules.",
 "DCSC exports (154 configs) 2026-09-14", "2026-09-14"),

("thinksystem-mixes-nic-vendors-and-epyc-needs-12-dimms",
 "ThinkSystem|SR675 V3|SR645 V3|SR665 V3|EPYC 9004|EPYC 9005", "proven",
 "The single-vendor NIC rule is ThinkAgile HX only (ThinkSystem mixes NIC vendors freely), and EPYC 9004/9005 need 12 DIMMs per socket for full bandwidth",
 "1. THE SINGLE-VENDOR NIC RULE DOES NOT APPLY TO THINKSYSTEM. The HX rule comes from the ThinkAgile HX product guides and governs HX and Nutanix appliances only (see existing fact hx-nic-vendor-rule-two-conflicting-statements). ThinkSystem servers mix NIC vendors freely. Proof: a Lenovo-issued SR675 V3 quote dated 2026-08-19 is a validly quoted config carrying BE4U Mellanox ConnectX-6 Lx 25GbE PCIe alongside BPPX Broadcom 57508 100GbE OCP. After a run of HX deals it is easy to carry the rule across and wrongly tell a customer they must pick one vendor; check the platform family first. "
 "2. EPYC 9004 and 9005 (Genoa and Turin) have 12 memory channels PER SOCKET, so 1 DIMM per channel = 12 DIMMs per socket and 24 on a 2-socket box. Anything less leaves channels empty and cuts memory bandwidth; DCSC will happily build 8 DIMMs and it is a legal config, just not bandwidth-optimal. On AI and HPC boxes this is real money left on the table, so flag it. Contrast Intel Xeon 6: 8 channels per socket, so 8 DIMMs per CPU is the full-bandwidth number. "
 "3. SR675 V3 4-DW-GPU SLOT MAP (pubs.lenovo.com/sr675-v3 technical specs, 2026-08-20), useful because customers assume the GPUs consume all the slots: slots 1-2 PCIe x16 FH/FL (front IO riser BR7H); slots 3-10 PCIe x16 400W FH/FL (the double-wide GPU slots, riser BR7S, BR7Q or BR7R); slots 15-16 and 20-21 PCIe x16 75W FH/HL (rear, BR7L x16/x16 Riser Option Kit); slot 27 OCP. There is no documented dependency on processor count for slot availability, so a single-CPU build does not lose slots. "
 "4. A 100GbE QSFP adapter in the OCP slot (BPPX) does not look like a 'card' on a config list, so customers ask for a QSFP card they already own; the PCIe equivalent is BK1J Broadcom 57508 100GbE QSFP56 2-Port. GPU boxes are lead-time constrained rather than TCE. See topic amd-v3-cpu-generation-dictates-dimm-speed.",
 "pubs.lenovo.com/sr675-v3 2026-08-20; DCSC exports and a Lenovo-issued quote 2026-08-19", "2026-08-21"),

("hx-nic-rdma-mellanox-copper-ocp-and-lom-rules",
 "ThinkAgile HX630 V4|HX650 V4|HX665 V3", "proven",
 "HX NIC rules beyond the vendor-mixing note: RDMA needs Mellanox ConnectX-6 PCIe, Mellanox has no 10GBASE-T, the OCP adapter is mandatory on HX630 V4, and sizer 'NIC LOM' lines are not orderable",
 "Rules from the ThinkAgile HX product guides (HX630 V4 lp2132, HX650 V4 lp2133, HX665 V3 lp1649, identical wording) and DCSC. The vendor-mixing statements themselves are in existing fact hx-nic-vendor-rule-two-conflicting-statements. "
 "1. RDMA/RoCE = MELLANOX CONNECTX-6 PCIe ONLY, MINIMUM QTY TWO. The OCP ConnectX-6 Lx is NOT the RDMA adapter. Nutanix's own RDMA matrix agrees (RoCE and Zero-Touch RoCE need ConnectX-5 or 6). "
 "2. MELLANOX OFFERS NO 10GBASE-T (RJ45 copper) on this platform, only SFP28 and QSFP. Any build needing a 10GBASE-T copper port must be ALL-BROADCOM (57412 or 57416 copper plus 57414 for 25G). "
 "3. THE OCP ADAPTER IS MANDATORY ON HX630 V4; DCSC blocks removing it (verified July 2026). To trim ports on a 3-card node (1 OCP plus 2 PCIe), drop a PCIe card, never the OCP. "
 "4. NUTANIX SIZER 'NIC LOM' LINES ARE MOTHERBOARD PORTS, NOT ORDERABLE OPTIONS. NX BOMs itemise '1 x 1GbE Dedicated IPMI (NIC LOM)' and '2 x 10GBase-T (IPMI Failover) (NIC LOM)'; nobody selected those, they are soldered on. The dedicated IPMI port maps to XCC on Lenovo, built into every node with no feature code to order (no management-port line exists in the DCSC catalog for 7DG3CTO1WW or 7DG4CTO1WW). "
 "The 10GBASE-T LOM ports have NO free equivalent, because ThinkSystem V4 has no onboard LOM at all: every port is an OCP or PCIe adapter. If the customer actually uses those copper ports you must buy a card, and since the only 10GBASE-T parts are Broadcom (B5ST OCP, AUKP PCIe, C4GB and C4GC 4-port, all TCE), that decision forces the whole node all-Broadcom. Ask what is plugged into them before assuming. "
 "5. RECURRING SIZER PAIRING: Nutanix-sized BOMs often pair a Mellanox 25G OCP (BE4T) with a Broadcom 10GBASE-T PCIe (for example 57416 AUKP). This DOES build on Lenovo HX and can still be TCE (13 HX exports mix Broadcom and Mellanox and 9 are TCE-clean with zero criticals). It is a Warning plus a design question, not a blocker: ask whether those two cards are ever bonded together. "
 "If they are, go all-Broadcom: Broadcom 57414 10/25G SFP28 OCP (BN2T, option 4XC7A08237, also TCE) plus 57416 10GBASE-T. For non-RDMA clusters the Broadcom 57414 and ConnectX-6 Lx are functionally equivalent 25G NICs, so nothing is lost; keep Mellanox only if RDMA/RoCE is a design goal, in which case it is 2x ConnectX-6 PCIe per node. Design rule that survives: keep each redundant PAIR on one vendor.",
 "Lenovo Press lp2132, lp2133, lp1649; Nutanix RDMA NIC matrix; DCSC exports and panel 2026-09-17", "2026-09-17"),

("xclarity-one-portal-hub-and-v4-xcc3-access",
 "XClarity One|XCC3|ThinkSystem V4|ThinkAgile HX", "proven",
 "XClarity One is Portal plus Hub: the Hub is an on-prem VM even with the SaaS Portal, so 'cloud or a VM?' is both; plus V4 XCC3 management-port and first-access facts",
 "Verified 2026-08-20 from XClarity One Product Guide lp1992. PORTAL = the management interface, deployable either as Lenovo-hosted cloud or SaaS OR as an on-prem local VM (the on-prem Portal caps at 4,000 devices). HUB = a lightweight virtual appliance that runs on-premises regardless of which Portal you pick; it is the secure bridge between managed devices and the Portal. One Hub covers many devices and multiple Hubs support multi-site. "
 "So the answer to 'is XClarity One cloud based, or do we spin up a VM?' is BOTH: even on the cloud Portal they stand up one Hub VM in the data center. Getting this wrong sets a false expectation of zero on-prem footprint. "
 "XClarity One replaces the withdrawn LXCA, LXCO and Pro line (see topic xclarity-pro-to-one-transition). It is NOT a substitute for XCC3 Premier: XCC3 Premier is the per-server controller tier that provides remote console (KVM), virtual media and boot capture; XClarity One is fleet management. Quote both when a customer wants remote hands-off access AND single-pane management. "
 "V4 OUT-OF-BAND FACTS (XCC3), verified the same day: a dedicated 1GbE management port sits on the rear of every node, standard, with no feature code to order (no management-port line exists in the catalog for 7DG3CTO1WW or 7DG4CTO1WW). An optional SECOND dedicated BMC port installs in the OCP adapter bay, so it is unavailable whenever the OCP slot holds a NIC (which on HX is always). "
 "XCC3 tries DHCP first and falls back to the documented static address 192.168.70.125; the default user is USERID and the default password is in the XCC3 user guide (confirm against the node label; whether V4 ships unique defaults is unverified). "
 "AVOIDING A CRASH CART for the initial IP: patch the dedicated ports to a DHCP management network and pull leases, or connect a laptop to the rear XCC port, or use the front USB management port (wrench icon; hold the ID button 3 seconds to switch the port to management mode). On HX and Nutanix builds, Foundation discovers nodes and can set the IPMI addresses during imaging, so per-node manual IP setting is often unnecessary; raise this before a customer plans crash-cart work. "
 "Docs: Lenovo Press lp1992, lp2132; XCC3 user guide; SR630 V4 configuration guide on pubs.lenovo.com.",
 "Lenovo Press lp1992, lp2132; pubs.lenovo.com XCC3 user guide 2026-08-20", "2026-08-20"),

("xcc2-platinum-vs-xcc3-premier-controller-tiers",
 "ThinkSystem V3|ThinkSystem V4|ThinkAgile", "proven",
 "XCC2 Platinum and XCC3 Premier are the top tier of two controller generations, not alternatives: V3 gets Platinum, V4 gets Premier, and Premier is cheaper",
 "Verified 2026-09-02 across 154 DCSC exports. XCC2 PLATINUM = V3 and older: SBCV plus BRPJ XCC Platinum plus 7S0XCTO5WW. Seen on SR250, SR630, SR635, SR645, SR650, SR655 and SR665 V3, ST250 V3, HX630, HX650 and HX665 V3, and SE450. "
 "XCC3 PREMIER = V4 only: SCY0 plus 7S0XCTO8WW. Seen on SR630, SR650 and SR650a V4, HX630 and HX650 V4, FX630 V4 and MX630 V4. The split is clean (one stray SR630 V3 row is a mislabelled config). "
 "Lenovo renamed the ceiling tier from Platinum to Premier at the generation boundary, so an old V3 quote with no 'Premier' option is not missing anything. XCC3 Premier is about 17 percent CHEAPER per node than XCC2 Platinum, which is counterintuitive and worth saying out loud. "
 "Both tiers cover remote KVM, virtual media, power control and diagnostics, so either satisfies a spec asking for those. Do NOT quote a feature-by-feature delta from memory: sub-tier feature lists have shifted between releases, so pull the current Lenovo XCC feature matrix before putting specifics in writing. "
 "When a customer asks to price 'premium management features' separately, this line is the answer. Related existing topics: sr250-v3 build facts (SBCV paid FOD) and topic xclarity-one-portal-hub-and-v4-xcc3-access.",
 "DCSC exports (154 configs) 2026-09-02", "2026-09-02"),

("xclarity-pro-to-one-transition",
 "XClarity Administrator|XClarity Orchestrator|XClarity Pro|XClarity One", "proven",
 "XClarity Administrator, Orchestrator and Pro were withdrawn 30 June 2026 (support to 30 June 2027); XClarity One Standard is the official 1:1 replacement in quotes",
 "Lenovo withdrew XClarity Administrator, XClarity Orchestrator and the XClarity Pro licence from marketing on 30 June 2026, with support running to 30 June 2027. All roadmap investment goes to XClarity One (SaaS and on-prem). Eligible Pro licences map 1:1 to XClarity One Standard with subscription end dates preserved. "
 "HOW TO APPLY: when a customer compares a new DCSC quote against a pre-July-2026 reference and asks why XClarity Pro is missing (or DCSC has no Pro option), the answer is that Pro is no longer orderable, and One Standard at the same term is Lenovo's official like-for-like successor. Cite 'Migrating to Lenovo XClarity One' (Lenovo Press lp2429). "
 "See topic xclarity-one-portal-hub-and-v4-xcc3-access.",
 "Lenovo Press lp2429", "2026-07-08"),

("st250-v3-tce-ssds-require-2-5in-chassis",
 "ST250 V3|7DCECTO1WW|SR250 V3", "flagged",
 "ST250 V3: the 3.5in chassis caps TCE SSDs at 960GB so an all-SSD TCE build needs the 2.5in chassis (BZB9 plus B41E); 1.92TB Mixed Use is a TCE gap; one guide-vs-catalog conflict",
 "Checked 2026-07-31 against the catalog (240 FCs, 159 TCE). If a customer mandates SSDs and the config must stay Top Choice Express, you must be on the 2.5in chassis. "
 "BZB8 3.5in chassis base: the only TCE-flagged 3.5in SSDs are 480GB (BYLJ RI, BYM3 MU) and 960GB (BYLY RI); every 3.5in SSD at 1.92TB or larger was non-TCE (BYLZ and BYM8 1.92TB, BYM0 and BYLX 3.84TB, all SED variants CCZx). So 3.5in forces a choice between SSDs and TCE, which is why builders fall back to HDDs such as C5X8 2TB 7.2K. "
 "BZB9 2.5in chassis base [TCE] plus B41E ST250 V3 8x 2.5in SATA/SAS Backplane Kit [TCE] gives the full TCE SSD ladder: BYLR 480GB RI, BYLS 960GB RI, BYLT 1.92TB RI, BYLU 3.84TB RI, BYLV 7.68TB RI, plus Mixed Use BYM2 480GB, BYM4 960GB, BYM6 3.84TB; SED twins (CBVx) mostly TCE too. "
 "CONFLICT (2026-09-29): Lenovo Press lp1803 p.44 and a catalog scrape tag BYLX 3.5in 3.84TB MU as TCE, contradicting 'every 3.5in SSD >= 1.92TB is non-TCE'. No ST250 V3 export has carried BYLX; check the panel. BYM4 2.5in 960GB MU is BU1E-proven on ST250 V3 (a 2026-09-29 export with 6x behind a BMFT 540-8i). "
 "TCE GAP TO REMEMBER: BYM5 2.5in 1.92TB Mixed Use is NOT TCE; in TCE, Mixed Use jumps from 960GB to 3.84TB with nothing between. A write-heavy workload wanting about 2TB must either take 1.92TB Read Intensive (BYLT, about 1 DWPD) or step up to 3.84TB MU (BYM6, about 3 DWPD). The same shape of gap likely exists on the sibling SR250 V3, so check before promising a 1.92TB MU TCE part. Endurance shorthand: Read Intensive is about 1 DWPD and Mixed Use about 3 DWPD; RDS and VDI hosts (profiles, temp files, paging) are write-heavy, so MU. "
 "A 3.5in to 2.5in chassis swap also drops B41L 4x 3.5in HDD Cage (HDD 4-7), AVJ3 3.5in fillers and the 3.5in backplane cables (BM7H, BMPW, BMNU); DCSC re-derives fillers and cables, they are auto-added and not selectable catalog entries. "
 "TWO DCSC WARNINGS THAT SHIP ON ST250 V3 CONFIGS (read Message History): (1) 'If need to upgrade from 8x drive SW RAID to 8x drive HW RAID, please include 4X97A81466, ThinkSystem ST250 V3 RAID Cable Kit as part of purchase', so going to the 8x 2.5in backplane behind a B8NY 940-8i needs the 8-drive cable kit while a 4-bay build only carries BM7H (4-drive); verify explicitly, do not assume DCSC adds it. "
 "(2) 'Changing selections will cause the HDD selections and/or RAID configuration to be lost', so changing the chassis base WIPES the array. Rebuild order: chassis, backplane, 5978 configured RAID, controller, RAID-level FC, drives, then re-verify the M.2 boot array. "
 "Related topic: sr250-v3-tce-part-list-and-m2-raid-trap.",
 "Catalog check 2026-07-31; Lenovo Press lp1803 p.44; DCSC exports 2026-09-29", "2026-09-29"),

("m2-boot-rules-v3-amd-vs-v4-intel",
 "SR635 V3|SR645 V3|SR655 V3|SR665 V3|SR630 V4|SR650 V4", "proven",
 "M.2 boot rules are platform-specific: V3 AMD caps TCE at 480GB and has no factory M.2 mirror (B8P9 mirrors in UEFI), while V4 Intel has a factory VROC array; the catalog trap of a code listed on 53 MTMs but built on one",
 "Verified 2026-09-02 across all 154 exports and CONFIRMED on a live panel 2026-09-03 (a live DCSC search for BS7F on SR645 V3 returned nothing). Both rules below are platform-specific; check the platform before applying either. "
 "V3 AMD (SR635, SR645, SR655, SR665 V3): (a) the TCE M.2 ceiling is 480GB (CBSZ NVMe): 44 TCE configs use it, while the 960GB V3 AMD part (CBT0) appears in 6 configs, all non-TCE, and C287 (the TCE 960GB) does not exist on V3 AMD, so on a TCE bid there is no 960GB M.2 option at all. "
 "(b) There is NO factory-preconfigured M.2 RAID on V3 AMD. C2ZC appears on SR630 V4 only; BS7F appears in exactly 4 configs, all SR630 V4. Proof: five SR645 V3 configs have 5978 'configured RAID' plus 2302 'RAID Configuration' populated with B9XD or B9XJ arrays, but those are all Controller 1 (the 940-8i); the B8P9 plus M.2 pair beside them gets ZERO array codes. DCSC will not build an M.2 array on this platform. "
 "So the boot pair on SR645 V3 is 2 drives with no factory array and the mirror created in UEFI at deployment. B8P9 'M.2 NVMe 2-Bay RAID Adapter' carries the RAID capability (a Marvell hardware RAID controller, mirror created in UEFI at first boot, about 2 minutes per node) and is the part to keep; BM8X 'M.2 SATA/x4 NVMe 2-Bay Adapter' is a passive carrier at roughly one fifth the price, do not downgrade to it. Quote it as 'hardware RAID 1 mirrored boot pair' and leave RAID Type on 5977. "
 "You also cannot drop to a single boot drive: both TCE M.2 enablement options (B8P9, BM8X) are 2-bay and DCSC will not accept qty 1 of CBSZ against them, so 2x M.2 is forced and 'we do not ship an unmirrored boot device' is true of how the box builds (a competitor's BOSS-N1 with 1x 480GB is genuinely weaker). "
 "Front NVMe on V3 AMD is always BC4V 'Non RAID NVMe' plus 5977, because no NVMe hardware RAID exists there (no AMD VROC equivalent), so a 940-16i on an all-NVMe V3 AMD config is an orphan card eating a PCIe slot. "
 "V4 INTEL (SR630, SR650, SR650a V4, HX630, HX650 V4, FX630 V4): the factory array IS real. Flip the RAID Type selector to C2ZC 'ThinkSystem Select Storage devices - configured M.2 RAID', which exposes BS7F 'M.2 NVMe Array 1 RAID 1' plus BS7J 'M.2 NVMe Array 1 HDDs' (qty 2), arrays under M2_VROC_ARRAY_1, with the CC7H B350i-2i enablement kit and an Intel VROC key (BZ4X RAID1-only, BS7M Standard, BS7N Premium, or B96G Premium); BS7F is BU1E-proven there. Note the earlier rule 'V4 M.2 960GB costs the same as 480GB' is STALE, see existing fact m2-480-vs-960-price-gap. "
 "CATALOG TRAP, quantified: a catalog scrape listed BS7A (Configured M.2/7mm RAID), BS7E (NVMe Array RAID 0), BS7F (NVMe Array RAID 1), BS7B and BS7C (SATA arrays) against 7D9CCTO1WW, all tc=true, none of them offered. BS7F appears on 53 of 265 MTMs in the scrape and has been BUILT on exactly 1 (SR630 V4, 4 configs). A 53:1 listed-to-built ratio is the signature of a code the scrape attaches broadly and DCSC gates per platform. Before recommending any array or config-selector feature code, compare the MTM count in the catalog with the count actually built; a big gap means do not promise it. "
 "Related existing fact: m2-b550-vs-b350-why-dcsc-hides-raid1.",
 "DCSC exports (154 configs) 2026-09-02; live DCSC panel 2026-09-03; Lenovo Press lp1971", "2026-09-03"),

]
