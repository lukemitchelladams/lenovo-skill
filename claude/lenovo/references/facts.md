# Lenovo verified facts

48 facts (46 proven, 2 flagged, 0 unknown). Generated 2026-09-30 from `kb/kb_facts.py`.

- **proven**: verified against DCSC exports and/or Lenovo Press on the date shown.
- **flagged**: sources conflict or the evidence is thin; say so when you use it.
- TCE membership **rotates** per MTM and per date. Treat any TCE claim older than a few weeks as a lead to re-check in the live DCSC panel.
- "The source corpus" means the author's own DCSC exports, which are not published. Prices are omitted on purpose.

## Neither Dell nor Lenovo sells a 10Gb-only OPTICAL NIC on current-gen rack servers; every 10Gb card is BASE-T RJ45

`dell-vs-lenovo-10gb-nic-media` | **proven** | scope: SR630 V4|SR650 V4|SR645 V3|Dell PowerEdge 16G|Dell PowerEdge 17G | verified: 2026-09-18

Dell 16G (R660/R760) and 17G (R470/R670/R770/R6715): EVERY 10GbE configurator option is BASE-T RJ45. 16G list: Broadcom 57416 Dual Port 10GbE BASE-T OCP, Broadcom 57454 Quad Port 10GbE Base-T, Intel X710-T2L and X710-T4L Base-T. 17G list: Broadcom 57412 Dual and Quad Port 10GbE BASE-T OCP 3.0 +Sec, Intel E610-XAT2 and E610-XAT4 10GbE BASE-T OCP. ZERO 10GbE SFP+ entries on any of the six platforms. Dell's lowest optical speed is now 25GbE SFP28. Dell 10Gb SFP+ cards stop at 15G (R650/R750/R6525/R7525): Broadcom 57412 Dual Port 10GbE SFP+ OCP 540-BCOQ, Marvell FastLinQ 41132 Dual Port 10GbE SFP+ OCP 540-BCOX, Intel X710 Dual Port 10GbE SFP+ PCIe 540-BDQZ. Lenovo is identical: the lp1971 SR630 V4, lp2127 SR650 V4 and lp1607 SR645 V3 adapter tables carry exactly one 10Gb heading, '10 Gb Ethernet - 10GBASE-T'. Zero 10Gb SFP+ adapters, and zero across the source corpus of DCSC exports. COMPETITIVE USE: kills any claim that Dell can do 10Gb optical and Lenovo cannot. Both vendors dropped it. INFERENCE: if a customer distinguishes a 10Gb card from a 25Gb card on current hardware they mean RJ45 BASE-T, because every optical card in either lineup is 25G-capable and would be called a 25Gb card. Confirm if their install base is 15G, where 10Gb SFP+ genuinely existed.

*Source: Dell.com configurator and product pages 540-BCOX 540-BFPR 540-BBVM; Lenovo Press lp1971 lp2127 lp1607*

## Dell to Lenovo NIC crosswalk for data plus storage network splits

`dell-to-lenovo-nic-crosswalk` | **proven** | scope: SR630 V4|SR650 V4 | verified: 2026-09-18

Dell Broadcom 57416 or 57412 Dual Port 10GbE BASE-T OCP maps to Lenovo B5ST ThinkSystem Broadcom 57416 10GBASE-T 2-port OCP, TCE. PCIe equivalent AUKP 57416 10GBASE-T 2-Port PCIe, TCE. Dell Broadcom 57414 Dual Port 25GbE SFP28 OCP maps to Lenovo BN2T 57414 10/25GbE SFP28 2-Port OCP, TCE; PCIe is BK1H, TCE. Same silicon, same media, same port count. Dell Intel E810-XXV 25GbE SFP28 maps to Lenovo BCD4 OCP or BCD6 PCIe Intel E810-DA2 10/25GbE SFP28. Dell NVIDIA ConnectX-6 Lx 25GbE SFP28 maps to Lenovo BE4T OCP or BE4U PCIe, NOT TCE on SR630 V4.

*Source: Dell configurator; DCSC exports*

## The number 57412 identifies NOTHING about the connector; resolve the SKU, never the chip number

`nic-part-number-naming-trap` | **proven** | scope: ALL | verified: 2026-09-18

Dell sold the 57412 as a 10GbE SFP+ card on 15G (540-BCOQ) and REUSES the same 57412 label for a 10GbE BASE-T card on 17G (540-BFPR, 540-BFPN). Lenovo 57412 (C4GB OCP, C4GC PCIe) is a 4-port 10GBASE-T copper card. So 57412 spans SFP+ and RJ45 across vendors and generations. Dell's own metadata is unreliable at chip level: SKU 540-BCOR is titled 57414 but its spec page lists Processor 1 x Broadcom BCM57412. UNCONFIRMED: Dell 16G 540-BCOR is titled 57414 Dual Port 10/25GbE SFP28 but 17G 540-BFPM is titled 25GbE SFP28 with no 10Gb mention. Whether the 17G part down-negotiates to 10G could not be confirmed from Dell docs.

*Source: Dell product pages; Lenovo Press lp1971 Tables 65 and 67*

## Copper means two incompatible things; ask RJ45 jack or SFP cage, never copper or fiber

`sfp28-vs-baset-two-kinds-of-copper` | **proven** | scope: ALL | verified: 2026-09-18

BASE-T copper is an RJ45 jack with Cat6a and needs a BASE-T PHY: Lenovo 57416 (B5ST OCP, AUKP PCIe), 57412 (C4GB OCP, C4GC PCIe), Intel E610 parts. Twinax or DAC copper is a direct-attach cable with SFP+ or SFP28 ends moulded on and plugs into an SFP cage. The 57414 (BN2T, BK1H) takes fiber optics AND twinax DAC but can NEVER take an RJ45 plug. Proven in exports: BN2T paired with A1PK 5m Passive DAC SFP+ Cable; several 57414 builds paired with AV1X 3m Passive 25G SFP28 DAC; optical is BYBJ or BF10, both named Dual Rate 10G/25G SR SFP28. There is NO RJ45-in-an-SFP-cage adapter in the Lenovo catalog: no transceiver in the source corpus has RJ45 or BASE-T in its description. You cannot bridge the two with a module.

*Source: DCSC exports; Lenovo Press lp1971*

## Lenovo publishes TWO conflicting mixed-vendor NIC rules on HX; the hard ban is stale but still quotable

`hx-nic-vendor-rule-two-conflicting-statements` | **flagged** | scope: HX630 V4|HX650 V4|HX665 V3 | verified: 2026-09-18

SOFT, current V3 and V4 product guides lp2132 lp2133 lp1649, uniform across the family, sits above the OCP adapter table: 'When using different vendor NICs, failover is not supported between these NICs. When possible, select only one vendor for network adapters. When multiple vendors must be used, ensure that redundant links are on NICs from the same vendor.' HARD, Reference Architecture for Workloads using Lenovo ThinkAgile HX and FX Series LP0665 v3.5 section 2.4 p.8, NOT withdrawn: HX supports Broadcom and Mellanox 10/25GbE adapters 'but mixing vendors is not supported. HX configurations only support network adapters from one vendor.' The same sentence is in withdrawn guides lp1482 lp1481 lp1383, which is its origin. WHAT DCSC ACTUALLY DOES: emits the failover sentence as a WARNING, never a Critical. 13 HX exports in the source corpus mix Broadcom and Mellanox and 9 are TCE-clean with 0 criticals (combinations seen: BE4T OCP + AUKP PCIe; BN2T OCP + BE4U PCIe; BE4T + BNWM). DESIGN RULE THAT SURVIVES: keep each redundant PAIR on one vendor; never bond a Broadcom port to a Mellanox port. Nutanix's own rule is narrower and per-BOND, AHV Networking Best Practices BP-2071: do not mix NIC models from different vendors in the same bond, do not mix speeds, do not mix drivers. NOTE: lp1971 and lp2127 for ThinkSystem SR630 and SR650 V4 carry NO such note. HX-guide-only language.

*Source: Lenovo Press lp0665 v3.5 p.8, lp2132, lp2133, lp1649; Nutanix BP-2071; DCSC message severity*

## SR630 V4 has TWO OCP 3.0 slots plus up to 3 PCIe; the rear hot-swap M.2 cage costs one PCIe slot

`sr630-v4-slot-budget` | **proven** | scope: SR630 V4 | verified: 2026-09-18

lp1971: supports up to 3x PCIe slots at the rear of the server, plus 2x OCP slots at the rear. Rear-access choices are 3x PCIe 5.0 (1 full-height, 2 low-profile) OR 2x PCIe 5.0 (1 FH, 1 LP) plus 2x hot-swap M.2 bays. So a build carrying the rear hot-swap M.2 cage C1YV has 2 OCP plus 2 PCIe, which is 4 adapter positions. Both OCP slots default to x8 lanes; a PCIe x16 OCP adapter needs cable kit C1YK. An unused OCP slot appears in the BOM as BPP5 OCP3.0 Filler with screw, and that filler is the tell that a free slot exists. Dual-OCP is proven TCE on SR630 V4: several BU1E exports carry BN2T qty 2 per node.

*Source: Lenovo Press lp1971 Tables 65 to 67; DCSC exports*

## SR630 V4 on ONE CPU keeps slots 1-2, OCP1 x16 and internal CFF RAID; loses slot 3 and OCP2

`sr630-v4-single-socket-slots` | **proven** | scope: SR630 V4 | verified: 2026-09-23

lp1971 p30 One-processor configurations: 16 DIMMs (1TB max), PCIe slots 1 and 2 only (slot 3 hangs off CPU 2), 1x OCP 3.0 slot OCP1 with x16, up to 8x 2.5in NVMe, internal CFF RAID or HBA allowed EXCEPT with the 10-bay AnyBay backplane (needs 2 CPUs unless tri-mode). lp1971 p82: OCP slot 7 connects to CPU 2. Proven 1-CPU TCE combos (BU1E, 0 criticals): 1x C5RD + 8x C0TQ 64GB (512GB on one socket, all 8 channels); 1x C5R7 + B8NY 940-8i adapter + BN2T OCP + BK1H PCIe; 1x C5QV + B8P0 940-16i CFF + C21W 10-bay SAS/SATA (June 2026, B8P0 has since left TCE); 1x C5RD + B8NY + C21T + C2NL x8/x8 riser + BWM3 800W. Use it against 2x 8C competitor boxes: 1x 16C matches the core count, fills every memory channel with 8 DIMMs, and halves VMware per-CPU 16-core-minimum licensing. For TCE the 16C part is C5R5 6724P (see sr630-v4-tce-cpu-live-panel).

*Source: Lenovo Press lp1971 p30, p82; DCSC exports*

## SR630 V4: the 940-16i PCIe ADAPTER (B8NZ 8GB, BM35 4GB) is TCE; the 940-16i INTERNAL CFF (B8P0) is NOT TCE

`sr630-v4-940-16i-adapter-vs-internal-tce` | **proven** | scope: SR630 V4 | verified: 2026-09-23

lp1971 p71-72 TCE column: B8NY 940-8i 4GB adapter TCE, BM35 940-16i 4GB adapter TCE, B8NZ 940-16i 8GB adapter TCE, CDNK 545-8i internal TCE; B8P0 940-16i 8GB INTERNAL (CFF) Not TCE, C0TU 545-8i adapter Not TCE, every U.3 variant (BGM1 BM36 BDY4 BGM2) Not TCE. PROVEN LIVE 2026-09-23: a BU1E export with 1x C5R5 Xeon 6724P 16C single-socket + 16x BYTJ + B8NZ + C21Z (6 SAS/SATA + 2 AnyBay + 2 NVMe) + 8x CBVC 1.92TB RI SATA SED + BN2T + BK1H + C0U5, with 60mo Premier 24x7 4hr + KYD. B8P0 carried BU1E in June 2026 exports and has since rotated OUT. Do NOT generalise the SR650 V4 rule 'every 16i is non-TCE' to SR630 V4. C21Z + B8NY (8 ports on C21Z's 8 SAS/SATA-capable bays) is also TCE. MEMORY PRICE SURGE 2026: BYTJ 32GB roughly DOUBLED between Jun-Jul and late Sep 2026, and C0TQ 64GB rose about 57%. Stored export prices for DIMMs go stale within weeks; estimate totals from a live export only.

*Source: Lenovo Press lp1971 p71-72; live DCSC export 2026-09-23; DCSC exports*

## SR630 V4 TCE 16-core CPU on the LIVE DCSC panel 2026-09-23 is C5R5 6724P only; C5QV 6517P is NOT TCE

`sr630-v4-tce-cpu-live-panel` | **proven** | scope: SR630 V4 | verified: 2026-09-23

Live DCSC panel on 7DG9CTO1WW, 2026-09-23: the 6517P (C5QV) is not available in Top Choice Express, and the TCE CPU has to be C5R5 Xeon 6724P 16C 210W 3.6GHz, which is what current BU1E exports carry. The lp1971 TCE column still marks C5QV and C5RD as TCE, and exports from June-Aug 2026 carry BU1E with them, so BOTH of those sources were stale. Treat C5RD 6515P as unconfirmed for TCE until a current panel shows it. Never propose a CPU swap as a TCE saving from lp1971 or export history alone; the live panel decides.

*Source: Live DCSC panel 2026-09-23; DCSC exports*

## The DCSC xlsx export does NOT show the config-group quantity; only the CFXML inside the zip does

`dcsc-xlsx-hides-config-group-qty` | **proven** | scope: ALL | verified: 2026-09-23

Every xlsx tab (Quote, Summary, ConfigGroupView, Power Report) prints qty 1.0 per line and a single-server total, even when the configuration group is set to several systems. The multiplier lives only in the .xml: <ConfigurationGroupLineItem><configurationGroupName>Config 1</configurationGroupName><quantity>6</quantity><unitListPrice>...</unitListPrice>, where unitListPrice is PER SYSTEM. Proven on two exports 2026-09-23 where the xlsx showed 1 server and the xml group qty was 6. ALWAYS read <ConfigurationGroupLineItem><quantity> from the xml before stating a server count or order total.

*Source: DCSC CFXML exports 2026-09-23*

## Complete SR630 V4 10Gb and 25Gb adapter list with TCE status

`sr630-v4-10gb-and-25gb-adapter-options` | **proven** | scope: SR630 V4 | verified: 2026-09-18

OCP 10 Gb Ethernet 10GBASE-T: C4GB Broadcom 57412 4-Port TCE max 2 x8; B5ST Broadcom 57416 2-port TCE max 2 x8; C4HS Intel E610-T2 2-Port TCE; C4HU Intel E610-T4 4-Port TCE. OCP 25 Gb: BN2T Broadcom 57414 2-Port SFP28 TCE x8; BPPW Broadcom 57504 4-Port SFP28 TCE x16; BCD4 Intel E810-DA2 2-Port SFP28 TCE; BE4T Mellanox ConnectX-6 Lx 2-port SFP28 NOT TCE. PCIe 10GBASE-T: C4GC Broadcom 57412 4-Port TCE slots 1 and 3; AUKP Broadcom 57416 2-Port TCE max 3 slots 1 2 3; C4HT Intel E610-T4 4-Port TCE. PCIe 25 Gb: BK1H Broadcom 57414 2-port SFP28 TCE max 3 slots 1 2 3; BNWM Broadcom 57504 4-port SFP28 TCE x16; BCD6 Intel E810-DA2 2-Port SFP28 TCE; BE4U Mellanox ConnectX-6 Lx 2-port NOT TCE; C62J NVIDIA ConnectX-7 4-Port NOT TCE. There is NO 10Gb SFP+ card in either table.

*Source: Lenovo Press lp1971 Tables 65 and 67*

## The optics and DAC parts that actually appear in real exports

`transceivers-and-dacs-verified` | **proven** | scope: ALL | verified: 2026-09-18

BYBJ ThinkSystem Finisar Dual Rate 10G/25G SR SFP28 Transceiver, the cheap optical answer (about a third the price of BF10). BF10 Lenovo Dual Rate 10G/25G SR SFP28 85C Transceiver. AV1W Lenovo 1m Passive 25G SFP28 DAC Cable. AV1X Lenovo 3m Passive 25G SFP28 DAC Cable. A1PK 5m Passive DAC SFP+ Cable, 10G twinax. AV20 Lenovo 3m Passive 100G QSFP28 DAC. BNDR ThinkSystem Accelink 10G SR SFP+ Ethernet transceiver. Both dual-rate parts are literally NAMED Dual Rate 10G/25G, which is the documentary proof that an SFP28 port runs at 10G. Product guides do NOT carry a transceiver table; lp1971 jumps from adapters Table 67 straight to the ConnectX-8 aux cable Table 68. Sizer and DCSC BOMs routinely ship with ZERO optics, so always check.

*Source: DCSC exports*

## Top Choice Express: the non-negotiable rules

`tce-core-rules` | **proven** | scope: ALL | verified: 2026-09-18

TCE is proven ONLY by feature code BU1E present in a DCSC export. Nothing else proves it. TCE is all-or-nothing: one non-TCE part drops BU1E for the entire bid. Membership is per-MTM and per-date and it rotates; a part can be TCE on HX650 V4 and not on SR650 V4 the same week. Lists are NOT monotonic by size, they have floors as well as ceilings. Verified: HX650 V4 CPU floor where 8C C5R6 is TCE but 12C C5QQ is not; a 16GB DIMM floor where C0U2 breaks TCE; U.2 VA PCIe 5.0 window of 3.2TB to 7.68TB only. A rack chassis on the order voids TCE, as does any tied order holding non-TCE product. TCE is 21 days order to delivery. Customer-facing writing says Top Choice Express (TCE), never quick-ship.

*Source: DCSC exports*

## How to read a DCSC export without getting the numbers wrong

`reading-dcsc-exports` | **proven** | scope: ALL | verified: 2026-09-18

The price column is PER UNIT. Total Part Price is an uncached spreadsheet formula and comes back EMPTY when read programmatically, so compute qty times unit yourself. In the KB, part.qty is the TOTAL across all nodes, so divide by config.nodes for per-node. Supply status Green or Gray is NOT the same as TCE. Always check the currency. Scraped street-price files tend to be exact on chassis, CPU, NIC, PSU and services but ran about 83 percent low on memory and drives in 2026, so never quote a DIMM or drive price from anything but a real export.

*Source: Measured against DCSC exports*

## Drive, controller and software-defined storage rules that gate a build

`storage-controller-rules` | **proven** | scope: ALL | verified: 2026-09-18

U.3 NVMe SSDs have ZERO TCE configs, so U.3 in a build blocks TCE. Tri-mode (CH5Z plus BE38) is a 940-series RAID adapter feature only; every 440-series HBA is SAS/SATA only. U.3 is required only when a controller sits in front of NVMe. SAS/SATA needs a controller for protocol translation; NVMe does not because it is PCIe native. A backplane that exposes SAS/SATA bays forces a controller in DCSC even when those bays are empty. Software-defined storage (S2D, vSAN, Nutanix, Ceph) requires raw drives; hardware RAID breaks it. The 545-8i has no RAID 5 or 6. Internal means CFF form factor, Adapter means PCIe. Controller ports must match bay count. Write TB never TiB, convert by 1.0995 rather than relabel. Nutanix Sizer and DCSC B6C2 both emit TiB.

*Source: DCSC exports; Lenovo Press*

## Evidence discipline for any Lenovo answer

`answer-discipline` | **proven** | scope: ALL | verified: 2026-09-18

Never claim a part is TCE without a BU1E config proving it. Distinguish absence of evidence from proof of prohibition: 'this never appears in 469 configs' is a FLAG, not a rule, so say which one you have. Distinguish what DCSC BUILT from what Lenovo SUPPORTS; an export KB answers the first only. Never state a Nutanix node-reduction number without the customer's own Collector or Sizer output. Model knowledge on Lenovo feature codes is unreliable and the catalogue rotates, so never answer from memory.

*Source: Method*

## The NVIDIA L4 is the ONLY GPU the SR630 V4 supports, it is Not TCE, and it drags three other parts with it

`sr630-v4-gpu-is-l4-only-and-kills-tce` | **proven** | scope: SR630 V4 | verified: 2026-09-22

lp1971 Table 70 page 91: the SR630 V4 supported-GPU table has exactly ONE row, 4X67A84824 BS2C ThinkSystem NVIDIA L4 24GB PCIe Gen4 Passive GPU, Not TCE, Controlled (export-restricted), max 3, slots 1/2/3. There is no other GPU option on this platform. Because TCE is all-or-nothing, ANY SR630 V4 with a GPU is automatically outside Top Choice Express, no matter how clean the rest of the build is. A DCSC panel check 2026-08-12 agrees BS2C is Not TCE. THREE FORCED COMPANIONS: (1) the L4 is passively cooled, so lp1971 p.91 requires performance fans, C1YT not C1YS, and p.94 requires 4 fan modules with 2 CPUs / 3 with 1 CPU. (2) lp1971 p.41 requires a DIMM filler AURS in every empty DIMM slot whenever a GPU is fitted, so a 16-of-32 memory config needs 16x AURS. (3) lp1971 p.124 caps ambient at 30C once a rear GPU is installed. Automated BOM mappers tend to miss the fans and the fillers, so add them by hand. COMPETITIVE NOTE: HPE DL360 Gen12 also quotes a High Performance Fan Kit, a DIMM Blank Kit and a 30C ambient tracking code alongside its L4, so all three are parity items, not Lenovo weaknesses.

*Source: Lenovo Press lp1971 Tables 70 and 73, pages 41, 91, 94, 124; DCSC panel 2026-08-12*

## 6724P 16C 210W 3.6GHz IS on SR630 V4 and IS TCE; the PSU ceiling is 1300W Platinum / 2000W Titanium

`sr630-v4-6724p-and-psu-ceiling` | **proven** | scope: SR630 V4 | verified: 2026-09-22

lp1971 page 26: 4XG7B04168 C5R5 Intel Xeon 6724P 16C 210W 3.6GHz, TCE, max quantity 2. An export corpus may only show C5R5 on HX630 V4 and SR650 V4, so export history alone under-reports it - always check lp1971 p.26 before telling anyone a V4 CPU is unavailable on the SR630. Neighbours on the same page: C5R7 6714P 8C 165W 4.0GHz TCE, CE89 6725P 16C 235W 3.7GHz Not TCE CTO-only, C5R4 6730P 32C 250W TCE, C5QN 6731P Not TCE. PSU CEILING lp1971 p.123: Platinum tops out at 1300W (C0U5 230V/115V). Titanium reaches 2000W but that SKU is 230V-only with no support at 100V. There is NO 1600W supply on this platform, so an HPE 1600W Flex Slot Platinum line always maps DOWN to 1300W. Sanity check the draw first: 2x 210W CPU + 16x 64GB + an L4 peaks near 850W, so a 1300W N+1 pair is correct and the HPE 1600W is oversized. M.2 BOOT: on SR630 V4 the 960GB C287 is NOT the same price as the 480GB C286. The same-price-960GB shortcut does not hold here.

*Source: Lenovo Press lp1971 pages 26 and 123; DCSC exports*

## DCSC shows no RAID 1 choice with a B550 M.2 kit because that panel is the Intel VROC selector, and VROC only exists for the NON-RAID B350i-2i/B340i-2i

`m2-b550-vs-b350-why-dcsc-hides-raid1` | **proven** | scope: SR630 V4|SR650 V4|SR650a V4|HX630 V4|HX650 V4 | verified: 2026-09-22

THE SYMPTOM: you pick a B550 M.2 enablement kit, the DCSC 'M.2 RAID Configuration' section is empty or greyed, and the export says '5977 Select Storage devices - no configured RAID required'. That is correct behaviour, not a missing option. WHY: every B550 and B545 kit carries its own onboard Broadcom SAS3808N RAID controller and does the mirror on the card, so DCSC has nothing to configure. lp1971 p.65-66: with 2 drives the B550i-2i, B545i-2i, B550p-2HS and B550d-2HS all support RAID-0, RAID-1 or JBOD, and the B550i-2i and B545i-2i explicitly document 'default is RAID-1'. You set the array in UEFI at deployment. The B350i-2i (CC7H) and B340i-2i have NO built-in RAID and are the ONLY adapters that take Intel VROC, which is what the M.2 RAID Configuration panel is actually selecting: BZ4X 'Intel VROC RAID1 Only for M.2' (TCE, RAID-1) or BS7M 'Intel VROC Standard for M.2' (TCE, RAID-0/1). Both enable VROC for ALL installed drives, not just M.2. EXPORT PROOF: across ~470 exports, ZERO configs carrying CCCZ, CD0S, CD0R or CC7G also carry BS7F (M.2 NVMe Array 1 RAID 1). All 176 CCCZ configs carry 5977 'no configured RAID required'. Every SR630 V4 export that DOES carry BS7F uses CC7H plus VROC. WHICH KIT: CCCZ 4XH7B11658 = REAR hot-swap B550p-2HS, TCE, the mainstream pick (176 exports). CD0S 4XH7B11659 = FRONT hot-swap B550d-2HS, TCE, rare in practice. CC7G 4Y37B09898 = INTERNAL non-hot-swap B550i-2i, TCE. CC7H 4Y37B09897 = internal B350i-2i, TCE, no hardware RAID. If an automated mapper picks CD0S, CCCZ is usually what you want. SLOT COST: the rear hot-swap M.2 cage consumes one PCIe position, leaving 1 FH + 1 LP + both OCP slots. COMPETITIVE: HPE NS204i-u v2 is hot-plug hardware RAID, so CCCZ is the like-for-like answer and CC7H+VROC (software RAID, non-hot-swap) is not.

*Source: Lenovo Press lp1971 Tables 41 and 42, pages 62-66; DCSC panel 2026-09-22; DCSC exports*

## Live DCSC panel 2026-09-22: M.2 VA 960GB costs ~31% more per drive than 480GB; stored export prices ran low

`sr630-v4-m2-drive-live-panel-prices` | **proven** | scope: SR630 V4 | verified: 2026-09-22

DCSC panel 2026-09-22 on 7DG9CTO1WW: C286 ThinkSystem M.2 VA 480GB Read Intensive NVMe NHS SSD (4XB7A93140) and C287 M.2 VA 960GB (4XB7A93141): the 960GB is about 31% more per drive, so a mirrored pair costs noticeably more per node. Stored export history for C286 on SR630 V4 was ALL below the current panel price, so quote M.2 from a live panel, not from export history. PANEL READING TRAP: in the DCSC option list the Price column is per unit, but the collapsed SELECTED summary row at the top of a section shows the EXTENDED price for the chosen quantity. Do not read the summary row as a unit price.

*Source: DCSC panel 2026-09-22, MTM 7DG9CTO1WW*

## NVIDIA vGPU subscription licences are Lenovo-orderable 7S02 SKUs, not pass-through NVIDIA part numbers

`nvidia-vgpu-licenses-are-lenovo-skus` | **proven** | scope: ALL | verified: 2026-09-22

CONFIRMED FROM A LIVE DCSC PANEL 2026-09-22: 7S02003GWW 'NVIDIA vPC Subscription License 5 Years, 1 CCU'. Licences carry a 7S02 MTM-style number and are quoted as their own line, separate from the server CTO - they are NOT feature codes inside the config, so they will not appear in the DCSC part list of a server export. Quantity is per concurrent user, matching NVIDIA's own CCU model. SEARCH GAP, so do not conclude these do not exist: a server-export KB returns ZERO rows for vPC, CCU, vWS or any 7S02 feature code, and the Lenovo Press corpus returns only false positives - VPC meaning Virtual Private Cloud and vPC meaning Cisco virtual PortChannel, both in lp0665. Neither source covers software licence SKUs. Get them from the DCSC software catalogue or the price file. COMPETITIVE MAP: HPE R3Q53AAE 'NVIDIA Virtual PC 1 Concurrent User 5-year Subscription E-LTU' maps 1:1 to 7S02003GWW. Same NVIDIA licence, same 5-year term, same per-CCU counting - only the reseller SKU changes, so never present a vGPU licence as a Lenovo gap or as a pass-through the customer must buy elsewhere.

*Source: DCSC panel 2026-09-22; HPE quote; absence verified against DCSC exports and the Lenovo Press corpus*

## Lenovo PARTNERS with Scale Computing - SC//HyperCore is sold and supported on Lenovo hardware, it is not a competitor

`scale-computing-on-lenovo` | **proven** | scope: SR630 V3|SR650 V3|ThinkEdge SE100|ALL | verified: 2026-09-23

Scale Computing SC//HyperCore is an official Lenovo solution. Lenovo Press lp2279 (published 2025-08-13, updated 2025-09-25) names three certified platforms: ThinkSystem SR630 V3, ThinkSystem SR650 V3, ThinkEdge SE100. Scale's Lenovo page (scalecomputing.com/lenovo) links a 'Scale Computing on Lenovo' solution inside DCSC (dcsc.lenovo.com) and describes joint Scale plus Lenovo support. Press release 2025-12-17: 3-node ThinkEdge SE100 cluster with SC//HyperCore Standard Essentials from about USD 10,000 via Lenovo On Demand - LIMITED-TIME, one per customer, do not quote it for a future refresh. SALES USE: when a Scale customer asks 'what does Lenovo have to compete with Scale', the first answer is keep Scale and put it on Lenovo hardware - it preserves their Acronis agentless integration and retraining cost is zero. FLAGGED GAPS: lp2279 lists V3 Intel only, no V4 and no AMD, as of its last update; confirm V4 certification before quoting a refresh. No Scale SKUs appear in the source export corpus. lp2279 is not in the default Lenovo Press download list, so a local-corpus search will wrongly return zero hits for Scale.

*Source: Lenovo Press lp2279; scalecomputing.com/lenovo; Scale press release 2025-12-17*

## Lenovo Deployment Ready Solution for Red Hat OpenShift Virtualization: SR650 V4, single-node (edge/ROBO) or 3-node HA

`openshift-virtualization-lenovo-drs` | **proven** | scope: SR650 V4 | verified: 2026-09-23

Lenovo Press lp2376 (published 2026-02-18). Validated single-server design for edge, ROBO, lab and dev, and a three-node cluster for production HA. Reference BOM per node: 2x Xeon 6520P 24C, 512GB (8x 64GB), 2x 960GB M.2 NVMe boot, 4x 3.84TB U.2 NVMe, dual 10/25GbE plus 4-port 1GbE, XClarity Pro, Premier 24x7 4hr. Related docs: lp2432 (Modern Virtualization with OpenShift on ThinkSystem), lp1671 (OpenShift DRS), lp0968 (OpenShift RA on ThinkSystem, ThinkEdge and ThinkAgile HX). CAVEATS: OpenShift is a Kubernetes platform - Red Hat subscriptions are real cost and it needs Kubernetes skills, a poor fit for thin-IT sites. Note the reference BOM carries XClarity Pro, which was withdrawn 2026-06-30; XClarity One is the successor. The reference BOM is not a TCE proof.

*Source: Lenovo Press lp2376, lp2432, lp1671, lp0968*

## Acronis agentless backup covers Scale HyperCore, Proxmox VE, Hyper-V, VMware, Nutanix AHV and KVM - NOT OpenShift Virtualization

`acronis-hypervisor-support` | **proven** | scope: ALL | verified: 2026-09-23

Acronis agentless backup for Scale Computing SC//HyperCore 8.8, 8.9, 9.0 ships as a qcow2 virtual appliance and can target Acronis cloud, local HyperCore storage, SMB, NFS, Azure, AWS or Wasabi. Acronis added agentless Proxmox VE backup (VMs and LXC) for Proxmox 8.2 to 9.0. The Acronis supported-systems list also includes VMware, Hyper-V, Linux KVM, Nutanix AHV and Virtuozzo. So an Acronis shop that leaves Scale keeps Acronis on Proxmox, Hyper-V or Nutanix. Acronis does NOT support Red Hat OpenShift Virtualization / KubeVirt at the platform level: the Acronis Cyber Protect supported virtualization list (checked 2026-09-23) has vSphere, Hyper-V, Citrix, RHEV/RHV/oVirt, Oracle LVM, AHV, KVM, Scale HyperCore, Virtuozzo, Proxmox - no OpenShift, KubeVirt or Kubernetes. RHV support is NOT OpenShift Virtualization (RHV is the retired oVirt-based product). Only fallback is agent-based in-guest backup, which Acronis supports on any VM (one agent per VM, no hypervisor-level protection). Products that DO support OpenShift Virtualization: Veeam (Kasten / KubeVirt CBT), CloudCasa, Veritas NetBackup for Kubernetes, Red Hat OADP. SALES USE: pitching OpenShift to an Acronis shop means changing their backup product too.

*Source: acronis.com Proxmox integration + blog; scalecomputing.com Acronis data sheet; acronis.com supported systems; Acronis doc agentbased-agentless-backup; veeam.com OpenShift Virtualization blog*

## Lenovo has NO own equivalent of Dell NativeEdge or HPE Morpheus; LOC-A was withdrawn 2025-08-08

`lenovo-vs-nativeedge-morpheus` | **proven** | scope: ALL|ThinkEdge|XClarity One | verified: 2026-09-23

Dell NativeEdge = edge orchestration (zero-touch onboarding, app blueprints). HPE Morpheus = hybrid cloud management plus Morpheus VM Essentials with HPE's own KVM-based HVM hypervisor, licensed per socket. Lenovo has neither. Lenovo Open Cloud Automation (LOC-A, lp1974) did near-zero-touch provisioning of OS and clusters (Ubuntu, ESXi, Red Hat, Azure Local) on ThinkEdge SE350 V2/SE360 V2/SE450/SE455 V3 and SR630/SR650 V2-V3, per-node subscription, but it was WITHDRAWN FROM MARKETING 2025-08-08 and support ended 2026-03-31. Never pitch it. It never ran VMs or apps. XClarity One (lp1992, updated 2026-07-17) does firmware, monitoring and bare-metal OS deployment (Hub 1.5 / Portal 25.3+) across sites via Hubs, supports ThinkEdge, but does NOT orchestrate VMs or apps. Lenovo's XClarity One launch release said it would integrate LOC-A functionality (provisioning), not VM orchestration. No 'XClarity FCC' product exists in Lenovo Press or on the web (checked 2026-09-23); XCC/XCC3 is the per-server BMC (hardware only), and XClarity Orchestrator (LXCO, lp1337) is withdrawn and was hardware management too. No XClarity product manages or orchestrates VMs. Lenovo's answer is partner software: Scale Computing SC//Fleet Manager is the closest NativeEdge match (cloud console, zero-touch provisioning, app lifecycle management, 1 to 50,000 clusters) and runs on Lenovo (see scale-computing-on-lenovo). MORPHEUS ON LENOVO: HPE markets VM Essentials as vendor agnostic, but the HPE compatibility matrix (dp00005501, 2025-06) says testing at launch was limited to HPE hardware and qualifies only HPE plus Dell 660/670; no Lenovo. Unlisted hardware = best-effort support. Backup for HVM: Veeam 12.3+/13, Commvault, Cohesity, NetBackup, HPE built-in; Acronis NOT on the list and HVM is absent from Acronis supported platforms.

*Source: Lenovo Press lp1974, lp1992; HPE dp00005501 compatibility matrix 2025-06; veeam.com VM Essentials blog; commvault docs; scalecomputing.com/sc-fleet-manager*

## TruScale IaaS changes WHEN the customer pays, not how much; Scale-on-SE100 is offered with TruScale for SMB

`truscale-budget-framing` | **proven** | scope: ALL|ThinkEdge SE100|TruScale | verified: 2026-09-23

Lenovo TruScale Infrastructure as a Service (datasheet ds0164): pay-as-you-go on-prem, bundles hardware (ThinkAgile, ThinkSystem, storage), install/deploy/managed services, 24/7 monitoring, a customer success manager, and partner software (Microsoft, Nutanix, VMware named). Terms seen: 36/48/60 months, shorter negotiable. Minimum deal size, end-of-term options and multi-site terms are NOT published - quote-based via Lenovo. Lenovo press release 2025-09-24: TruScale for SMBs spans leasing, predictable subscription and consumption pricing, and the SMB 'AI Edge-Ready Node' bundle is ThinkEdge SE100 with Scale Computing HyperCore. SALES FRAMING: TruScale converts capex to opex; over the term it generally costs the same or more than buying (it carries services and financing). Pitch it for capex/cash-flow constraints, not to lower total cost. Scale also sells Reliant Platform edge-computing-as-a-service on SE100 (retail/hospitality focus). PC-vs-SERVER TRAP: 'Lenovo Device Orchestration' (LDO) is PC ENDPOINT management (Intune agent, BIOS/driver patching, third-party PCs) - NOT a server or edge-cluster provisioning successor to LOC-A. An AI-generated summary claiming LDO / 'Lenovo Cloud Deploy' replaced LOC-A was wrong (2026-09-23).

*Source: Lenovo Press ds0164; Lenovo StoryHub 2025-09-24 SMB release; Scale press release 2025-12-17; lenovo.com LDO page*

## SR650 V4 NVMe RAID has three paths: VROC direct (x4 Gen5), RAID 960W-32i (x2 Gen5, U.2), 940 tri-mode (x1 Gen4, U.3 only)

`sr650-v4-nvme-raid-three-paths` | **proven** | scope: SR650 V4 | verified: 2026-09-24

lp2127 p.99-102. (1) ONBOARD NVMe + Intel VROC: each drive PCIe 5.0 x4 to the CPU, no RAID card. BZ4W RAID1-only, BR9B Standard (RAID 0/1/10), B96G Premium (adds RAID 5), all TCE per lp2127 Table 55. RAID 1 max 2 drives per array, RAID 10 max 4. ESXi supports VROC RAID 1 ONLY; Windows/Linux get 0/1/5/10. SED not supported with VROC. Keep an array's drives on one CPU. C46P 8x2.5in NVMe backplane runs on onboard NVMe with 1 or 2 CPUs (TCE, 5977, no BC4V line; BC4V never appears on any V4 export). (2) CECC RAID 960W-32i NVMe PCIe Gen5 adapter: hardware RAID, NVMe ONLY, U.2 drives at x2, 16 drives max, Not TCE, listed on C46P (config 152-1); field cable kit 4X97B17364; no builds in the source corpus. (3) 940-8i/940-16i + CH5Z tri-mode (new July 2026, replaces BGM1/BM36/BDY4/BGM2): PCIe 4.0 x1 link per NVMe drive, U.3 drives ONLY (7500 MAX/PRO C2BV/C2BW/C2BF etc, all Not TCE), needs C3RU AnyBay. An HPE MR416i tri-mode NVMe design should map to (1) or (2), never (3), when the workload is IOPS-bound. Watch automated mappers that put U.2 drives behind B8NZ with HW RAID arrays on C46P; that cannot work.

*Source: Lenovo Press lp2127 p.69, 88, 99-102, 108; DCSC exports*

## VA Mixed Use NVMe IOPS minimums: PCIe 5.0 1.6TB 1.44M read/270K write, 3.2TB 1.71M/360K

`va-mixed-use-nvme-iops` | **proven** | scope: ALL | verified: 2026-09-24

lp2257 Table 2 (Vendor Agnostic MU 3 DWPD, minimum values). 2.5in PCIe 5.0: 1.6TB 1,440,000 read / 270,000 write 4K IOPS; 3.2TB 1,710,000 / 360,000; 6.4TB and 12.8TB 1,800,000 / 360,000; seq read 10,800 MBps. 2.5in PCIe 4.0: 800GB 720K/130K, 1.6TB 630K/180K. E3.S 1T PCIe 5.0 reads match 2.5in but writes are lower (1.6TB 135K). RAID 10 SIZING: reads scale with all drives, writes with half. 4x 1.6TB PCIe 5.0 RAID 10 = ~5.7M read, ~540K write, ~1.48M at 70/30. A '1M IOPS' DB requirement is met on reads and OLTP mixes but NOT at 100% random write on 4 drives, even at 3.2TB (~720K).

*Source: Lenovo Press lp2257 p.7*

## The '960GB M.2 costs the same as 480GB' rule is STALE on V4 Intel; the live panel shows ~31% more per drive

`m2-480-vs-960-price-gap` | **proven** | scope: SR630 V4|SR650 V4 | verified: 2026-09-24

DCSC panel 2026-09-22 (SR630 V4): C287 960GB costs about 31% more per drive than C286 480GB. For an HPE NS204i-u 480GB match use CCCZ rear hot-swap B550p-2HS + 2x C286; the mirror is on the card (5977), no BS7F.

*Source: fact sr630-v4-m2-drive-live-panel-prices; fact m2-b550-vs-b350-why-dcsc-hides-raid1*

## RAID 545-8i (C0TU adapter / CDNK internal) supports only 2 virtual drives, so any 3-array layout cannot be built on it

`raid-545-8i-two-virtual-drive-limit` | **proven** | scope: ALL | verified: 2026-09-24

lp1552 p.3: RAID 545-8i = 8 drives, no expander, 2 virtual drives (540-8i/16i = 32). It is also cacheless, uses a fixed 64KB stripe, runs 24Gb SAS drives at 12Gb, and has no online capacity expansion or RAID level migration. The 940 series supports 240 virtual drives per controller (lp1282 p.5). A DB + logs + archive split (3 arrays) needs B8NY 940-8i: TCE, and paired with C21T in 11 SR630 V4 exports. Seen in the field 2026-09-24: CDNK + 6x CABR + 2x CABQ exported with BU1E and 0 criticals even though 3 arrays were intended, because DCSC was at 5977 (no configured RAID) and never checked the array count. BU1E and a clean Message History do NOT prove the RAID layout fits.

*Source: Lenovo Press lp1552 p.3, lp1282 p.5; DCSC exports*

## SR630 V4 on ONE CPU runs 8 NVMe bays off onboard ports via 2x C2NN, TCE-proven, no controller

`sr630-v4-single-socket-8-nvme-tce` | **proven** | scope: SR630 V4 | verified: 2026-09-24

lp1971 p.30: 1-CPU SR630 V4 takes up to 8x 2.5in NVMe; lp1971 p.50 config 4-2 (1 CPU only) = 2x C2NN 4x2.5in NVMe G5 on onboard NVMe. C21X 10-bay NVMe is in 2-CPU builds. PROVEN: a BU1E export 2026-06-25 = C1XE + 1x C5RD + 2x C2NN + 4x C0ZU per node + 5977, no RAID adapter. VROC on SR630 V4: B96G Premium and BZ4W both appear only in TCE exports, including single-socket builds. Swap recipe from a SAS build: remove the controller + C21T + SAS drives, add 2x C2NN + U.2 drives + VROC.

*Source: Lenovo Press lp1971 p.30, p.50; DCSC exports*

## DCSC will not factory-build a 4-drive VROC RAID 10 on front NVMe; its VROC array panel caps at 2 drives. Use 5977 + UEFI, or 2212

`dcsc-vroc-front-arrays-need-2212-or-uefi` | **proven** | scope: SR630 V4|SR650 V4 | verified: 2026-09-24

SYMPTOM (live DCSC session 2026-09-24): with VROC selected, DCSC only allows 2 drives per RAID array. EXPORT PROOF: across every export carrying B96G/BR9B/BZ4W, the ONLY VROC array feature codes are M.2 (BS7F 'M.2 NVMe Array 1 RAID 1' + BS7J, 2 drives). There is no front-NVMe VROC RAID 10 array code in ~470 exports. Every SR630 V4 export with VROC + 4x U.2 NVMe that meant RAID used 2212 'Storage devices - Custom RAID Configuration' (9 exports, all BU1E) or 5977 no configured RAID. VROC itself does RAID 10 on up to 4 drives (lp1971 p.73, lp2127 p.101); RAID 1 is 2 drives max. Also check the key: BZ4W is RAID 1 ONLY and caps every array at 2 drives. BR9B Standard = 0/1/10, B96G Premium adds 5. FIX: keep B96G or BR9B, set 5977 and build arrays in UEFI at deploy (free), or add 2212 with the layout in the config instructions for a factory build.

*Source: DCSC exports; Lenovo Press lp1971 p.73-74, lp2127 p.101-102*

## LIVE 2026-09-24: BR9B VROC Standard IS TCE on SR630 V4; 1-CPU 8x C0ZQ via 2x C2NN, no controller, BU1E

`sr630-v4-vroc-nvme-tce-live-export` | **proven** | scope: SR630 V4 | verified: 2026-09-24

Export 2026-09-24 (BU1E, all messages Normal): 7DG9CTO1WW, C1XE, 1x C5R5 6724P, 8x C0TQ, 5977 + BR9B, 8x C0ZQ 3.2TB U.2 VA MU Gen5, 2x C2NN + 2x C3NZ + C2NT, no RAID adapter (B8NK supercap dummy stays), CCCZ + 2x C286, BN2T + 2x AV1X, 3x C1YT performance fans (auto), 2x C0U5, 690.9W worst case at 115V. First BU1E proof for BR9B. PRICE SURGE: C0ZQ rose about 61% between June and late Sep 2026, so on the same day 8x 3.2TB NVMe cost MORE than 6x CABR 1.6TB + 2x CABQ 3.2TB SAS. July export prices for drives were ~30% low. Never estimate a drive swap delta from export history.

*Source: DCSC export 2026-09-24*

## LIVE 2026-09-24: HW RAID on NVMe on SR650 V4 = 2x B8NY 940-8i + CH5Z + 2x C3RU + U.3 7500 MAX; builds clean, NOT TCE (no BU1E)

`sr650-v4-hw-raid-nvme-trimode-live-build` | **proven** | scope: SR650 V4 | verified: 2026-09-24

Export 2026-09-24 (the filename said TCE but it had NO BU1E - never trust a filename): 7DGDCTO1WW, C3QK, 1x C5R5, 8x C0TQ, 5978 + 2302, 2x B8NY in C3R4 slot 3 + C62D slot 5, CH5Z, 2x C3RU AnyBay, 6x C2BV U.3 7500 MAX 1.6TB + 2x C2BW 3.2TB, arrays B9XG (C1 A1 RAID 10) + B9XJ (C1 A2 RAID 1) + B9XV (C2 A1 RAID 1), 2x AUNP auto, 2x C3QX SAS cables. Only Normal messages. 792.2W worst case at 115V = 72.67% on 2x C0U5 with 1 CPU. Premier 24x7 4hr 60mo cost ~40% more on SR650 V4 than on SR630 V4. Tri-mode links each NVMe drive at PCIe 4.0 x1 (lp2127 p.100). This is the answer when a customer mandates hardware RAID arrays on NVMe; VROC is software RAID and CECC 960W-32i is the Gen5 alternative (no builds seen). U.3 drives are what kill TCE here.

*Source: DCSC export 2026-09-24; Lenovo Press lp2127 p.100*

## HPE MicroServer Gen11 -> ThinkSystem ST50 V3 (7DF3CTO1WW): same Xeon 6300 CPUs incl. the exact 6337P (C522); no ST50 V3 exports in the source corpus

`st50-v3-hpe-microserver-gen11-answer` | **flagged** | scope: ST50 V3|ST45 V3|HPE MicroServer Gen11 | verified: 2026-09-25

ST50 V3 is the MicroServer Gen11 match: 1S 17-liter tower, Xeon 6300 / E-2400 / Pentium, 4x UDIMM (C527 16GB 5600 TCE, 1/2/4 DIMMs, all identical), 3x 3.5in non-hot-swap + 1x 2.5in bay, 1 fixed PSU (300W or 500W, single PSU is the platform, not a build error), XCC2, 7DF3 = 3yr 9x5 NBD onsite base (7DF4 = 1yr). CPU TCE per lp1907 p.24: ONLY C520 6325P 4C and C524 6353P 8C are TCE; C521 6333P 6C and C522 6337P 6C 80W 3.5GHz are Not TCE. CONFLICT: a 2026-07-28 catalog crawl tagged C521 as TCE, the guide (downloaded 2026-09-18) says Not TCE; no BU1E export exists either way. Drives: BMEC 2TB and BMEG 4TB 512n NHS SATA are TCE, the 512e v2 twins C5X5/C6C9 are Not TCE. Onboard AVV0 VROC SATA RAID (RSTe, RAID 0/1/5, TCE) is NOT supported under any hypervisor (lp1907 p.32), AHCI only; RAID adapter options are BMFT 540-8i (TCE) and C0TU 545-8i. US Top Choice Stock models (lp1907 p.23): 7DF31005NA 6315P 4C 16GB, 7DF31006NA 6315P 4C 32GB, 7DF3A03CNA 6333P 6C 16GB XCC2 Platinum, 7DF31007NA 6353P 8C 32GB 500W. 2nd/3rd 3.5in drives use cage kits 4XF7A79662 / 4XF7A93516. ST45 V3 (lp1994) is AMD EPYC 4005, only 2 UDIMM slots, and has NO XClarity Controller, so it fails an iLO-parity ask.

*Source: Lenovo Press lp1907 p.13/15/23/24/27/32/35, lp1994 p.5-6/35*

## DCSC gate: FACTORY-INSTALLED Windows (SDA9) requires a boot target, either an M.2 SSD or a 5978 configured RAID array; not-preinstalled SDAE does not

`windows-factory-install-needs-boot-array` | **proven** | scope: ALL|SR250 V3|ST250 V3|SR630 V4|SR650 V4|ST50 V3 | verified: 2026-09-28

Hit live 2026-09-25 on ST50 V3: adding Windows Server 2025 said it needs an M.2 SSD or a RAID-configured storage array. Export proof: every SDA9 (English, factory installed) config carries 5978 'Select Storage devices - configured RAID', 22 of 22 across SR250 V3 (5), ST250 V3 (14), SR630 V4 (1), SR650 V4 (1). SDAE (Standard 16-core MultiLang, NOT preinstalled) builds WITHOUT 5978 and without any M.2 SSD: SR630 V4 3 of 4, SR650 V4 3 of 3. So the gate is the factory preload, not the licence. Fixes: (1) configure the array (5978 -> controller or AVV0 onboard SW RAID -> RAID level -> assign drives), or (2) switch to the not-preinstalled SKU (SDAE Standard, SDAU Essentials). SDAU without an array is unproven. ST50 V3 unproven either way. REFINED 2026-09-28: an M.2 SSD alone satisfies the gate. An SR250 V3 export built SDA9 on 5977 (no configured RAID) with BM8X + 2x CABU M.2 and BU1E. TRAP: that means the preload lands on ONE unmirrored M.2 and the second M.2 ships blank. For a mirrored boot pair, set 5978 + BS7Q + BS7C on the M.2 pair.

*Source: Live DCSC session 2026-09-25; DCSC exports SDA9/SDAE vs 5978; SR250 V3 export 2026-09-28*

## SR250 V3 is the only Lenovo 1U rack server that fits a 23-inch depth limit; the mainstream 1U boxes are 30-31 inches

`sr250-v3-only-1u-under-23in` | **proven** | scope: SR250 V3|SR630 V4|SR645 V3|SR635 V3 | verified: 2026-09-28

Depths from Lenovo Press: SR250 V3 561 mm (22.1 in), 523 mm flange-to-PSU-handle, ~570 mm (22.4 in) with the 1U bezel (lp1802 p56). SR630 V4 788 mm (31 in) with 2.5-in drives, 845 mm with E3.S (lp1971 p121). SR645 V3 773 mm (30.4 in, lp1607 p115). SR635 V3 773 mm (30.4 in, lp1609 p93). So a short-depth 1U request is an SR250 V3 answer, with its limits: 8C max CPU (Xeon 6300 / E-2400), 4 UDIMM slots / 128GB max, 4x 3.5-in or 8x 2.5-in bays, M.2 SATA only (no NVMe M.2 drive offered, 480GB CABU is the smallest and the only TCE one), 2x x8 LP slots + 1 internal storage-controller slot. M.2 adapter uses a dummy PCIe card so it takes one LP slot.

*Source: Lenovo Press lp1802 lp1971 lp1607 lp1609*

## SR250 V3 default rail BK7W needs 24-34in between rack posts; a short-depth request needs B7L3 (14-24in) or B6H2 2-post

`sr250-v3-rail-kit-rack-depth` | **proven** | scope: SR250 V3 | verified: 2026-09-28

lp1802 p53 Table 49: BK7W Toolless Friction Rail v2 (4M17A13564) rail length 751.2 mm (29.6in), front-to-rear flange distance 609.6-863.6 mm (24-34in). B7L3 Short Rack Rail Kit (4M17A37605) rail 484 mm (19.1in), 355.6-609.6 mm (14-24in). B6H2 Friction 2-Post Screw-in (4M17A37105) for 2-post racks. All three TCE per lp1802; only BK7W appears in exports, so re-check BU1E after a swap. DCSC defaults BK7W, so a 'server can't exceed 23in' ask (= shallow rack) will ship rails that do not fit unless swapped. Customer 'server length' = depth front-to-back; width and height are fixed by the 19in rack and 1U.

*Source: Lenovo Press lp1802 p53*

## SR250 V3 3.5-in chassis + M.2 boot + 4-port 1GbE builds TCE (BU1E); corrects the old 'no M.2 on SR250 V3' note

`sr250-v3-35in-m2-tce-build` | **proven** | scope: SR250 V3 | verified: 2026-09-28

Export 2026-09-28, 2x 7DCLCTO1WW, BU1E present, warnings only: BWM2 3.5in chassis, BMPX 4x3.5 HS backplane + B405 onboard cable, AVV0 onboard SATA SW RAID mode, 3x AUU8 4TB 7.2K SATA 512n, BM8X M.2 2-bay + BWN1 VROC M.2 signal cable + BMTU dummy PCIe card, 2x CABU 480GB M.2 SATA, AUZV Broadcom 5719 4-port 1GbE, BMWQ x8/x8 riser, 2x BWM3 800W Titanium, C524 6353P 8C, 4x C527 16GB (memory was 59% of the server price), SDA9, SBCV, SCJD. First 3.5in-chassis (BWM2) and first M.2 SR250 V3 build seen. Built on 5977 with no M.2 or data array, so both are unmirrored as exported.

*Source: DCSC export 2026-09-28*

## '4-port NIC x2 + 2-port Fiber Channel' on SR630 V4 = 2x quad 1GbE + QLE2772 32Gb FC HBA; all TCE, fits with 2 CPUs

`sr630-v4-8x1gbe-plus-fc-slot-plan` | **proven** | scope: SR630 V4 | verified: 2026-09-25

Reading the spec: 'Fiber channel' is a Fibre Channel HBA for a SAN (storage protocol), NOT fiber Ethernet; a quad-port NIC with no speed stated is normally 1GbE RJ45 (flag it, ask 1Gb or 10Gb and RJ45 jack or SFP cage). SR630 V4 has 3 rear PCIe + 2 OCP; slot 3 and OCP slot 7 hang off CPU 2 (lp1971 p.81-82). Parts per lp1971: B5T1 Broadcom 5719 1GbE 4-port OCP TCE max 2 (p.87, 14/14 SR630 V4 exports with it are BU1E); AUZV same chip as PCIe, TCE max 2, slots 1,3 (p.88); BA1F QLogic QLE2772 32Gb 2-port FC TCE max 3 slots 1,2,3 (p.92, 3/3 exports BU1E); C5FD Emulex LPe38102 64Gb FC TCE. If they really mean 10/25: C4GC 57412 10GBase-T 4-port PCIe TCE, C4HU E610-T4 10GBase-T 4-port OCP (3/3 BU1E), BNWM 57504 10/25 SFP28 4-port PCIe (7/7 BU1E). 2x B5T1 in one config has never been exported (flagged).

*Source: Lenovo Press lp1971 p.81/87/88/92; DCSC exports*

## 8x 10Gb SFP ports per 1U server = two 4-port Broadcom 57504 10/25 SFP28 cards; on SR645 V3 the PCIe one is FULL-HEIGHT and max 1

`8x-10gb-sfp-on-sr630v4-sr645v3` | **proven** | scope: SR630 V4|SR645 V3 | verified: 2026-09-25

There is no 10Gb-only SFP+ card on either platform, so the 57504 10/25GbE SFP28 (dual-speed) IS the 10Gb SFP answer. SR630 V4 (lp1971 + fact sr630-v4-10gb-and-25gb-adapter-options): BPPW 57504 4-port OCP TCE x16, BNWM 57504 4-port PCIe TCE x16 (7/7 exports BU1E). Two OCP slots with 2 CPUs, so 2x BPPW or BPPW + BNWM (2x BPPW in one config never exported, flagged). SR645 V3 (lp1607 p.83-84): BPPW OCP TCE max 1; BNWM PCIe TCE but form factor FHHL, max quantity 1, slots 2,3 (dagger footnote) = needs a full-height riser; the LP+LP riser cage BLK9 will not take it. So SR645 V3 = 1x BPPW (OCP) + 1x BNWM (FH PCIe) + FC HBA in the remaining LP slot. Optics are never bundled: per server 8x BYBJ Finisar Dual Rate 10G/25G SR SFP28 for fiber, or AV1W 1m / AV1X 3m passive SFP28 DAC (TCE). Ask fiber vs DAC and the distance. 5m DAC TRAP: AV1Y 'Lenovo 5m Passive 25G SFP28 DAC' is NOT TCE (catalog crawl 2026-07-28; lp1793 p.12 agrees), while A1PK '5m Passive DAC SFP+ Cable' (10G) IS TCE there and runs fine in a 57504 SFP28 port at 10Gb (an export pairs A1PK with the 57414 SFP28). For 10Gb switch ports at 5m, pick A1PK. A1PK has no BU1E export yet, so confirm BU1E holds. RAID 1 on the CDNK 545-8i internal = 5978 + B9XD 'Controller 1 HW RAID Array 1 RAID 1' + BA12 x2; DCSC auto-adds 2302 RAID Configuration. PROVEN TCE on SR645 V3 2026-09-25 (export: BU1E held, no Criticals, with BPPW + BNWM + BLK8 LP+FH riser cage + BA1F FC). lp1607 p.64 lists CDNK as RAID 0/1/10, TCE.

*Source: Lenovo Press lp1971 p.85/87, lp1607 p.83-84; DCSC exports*

## SR650i V4 is a FIXED-BOM SR650a V4 (CF3G): 2x 6530P, 2x CBK8 RTX PRO 6000 96GB, 512GB, nothing major can change

`sr650i-v4-fixed-inference-bom` | **proven** | scope: SR650a V4|SR650i V4 | verified: 2026-09-28

lp2128 p.15: SR650i V4 Inference Model = CF3G on 7DGDCTO2WW/7DGCCTO2WW; select via DCSC Full Mode, Base tab. Fixed: 2x C5QT Xeon 6530P 32C, 2x CBK8 RTX PRO 6000 Server Edition 96GB (600W, C9R6 cages), 8x C0TQ 64GB = 512GB, 2x C0ZU 3.84TB U.2 VA RI, 2x C287 960GB M.2 on CC7G B550i-2i, BK1H 57414 10/25GbE. 'All major components are fixed and cannot be changed in the CTO order.' In a 2026-09-28 export the memory was 41% of the total, MORE than the two GPUs. PSU C0UD 3200W 230V only + BK15 high voltage: needs 200-240V C19 power. BU1E WAS present on the 2026-09-28 export even though lp2128 says to switch out of Top Choice Express mode to select CF3G, so confirm TCE on the bid. CBK8/C9R6 caps it at 2 GPUs; the 4-GPU path is CHWT + C3S1 (a different build). To trim memory or CPU, build a standard SR650a V4 instead: BYTJ 32GB and C5RD 6515P 16C appear in TCE SR650a V4 exports.

*Source: Lenovo Press lp2128 p.15; DCSC export 2026-09-28*

## 7DGDCTO4WW / 7DGCCTO4WW 'SR650a V4 Workstation' is the Windows 10/11 CLIENT-OS model with a restricted adapter/drive list, not a better box

`sr650a-v4-workstation-mtm-is-windows-client` | **proven** | scope: SR650a V4 | verified: 2026-09-28

lp2128 p.13 Table 3: 'The SR650a V4 can run Windows 10 and Windows 11, however only a subset of adapters and drives can be installed' and the CTO4WW models exist to build that subset. For a Linux LLM/inference server use 7DGDCTO2WW. A Workstation export 2026-09-28 (2x CBK8, 2x 6530P, 8x C0U9 32GB = 256GB, 2x C1W8 E3.S 1.92TB) came in about 25% under the SR650i V4 with the same GPUs and CPUs, almost all of it from halving memory and smaller storage/boot. It had NO network adapter (only OCP fillers BPP5), NO M.2 boot, and NO BU1E. lp2128 lists C1W8 E3.S 1.92TB as Not TCE, while C0U9, BYTJ and C0ZU U.2 3.84TB are TCE, so C1W8 is a proven TCE-breaker (the CTO4WW model itself is unproven either way).

*Source: Lenovo Press lp2128 p.13 and memory/drive tables; DCSC export 2026-09-28*

## BQZU NVIDIA A16 64GB is a VDI card (4x 16GB GPUs on one board), never an LLM answer; RTX PRO 6000 on SR655 V3 needs the 'for AI' MTM 7D9ECTO3WW

`a16-is-vdi-not-llm-and-sr655v3-ai-mtm` | **proven** | scope: SR655 V3|ALL | verified: 2026-09-28

A16 = four separate 16GB GDDR6 GPUs, 128-bit each (~200 GB/s per GPU, below the 273 GB/s of a DGX Spark/PGX), no FP8/FP4. A 2x A16 box has 128GB split across EIGHT 16GB GPUs, so a 65GB+ model must be sharded over PCIe; it is built for vGPU desktops. lp1610 GPU table: BQZU Not TCE, max 3; CBU5 RTX PRO 6000 Max-Q 96GB Not TCE, max 3, slots 2/5/7. WHY THE MTM MATTERS (lp1610 p.80): CBU5 is an export-CONTROLLED GPU, and a Controlled GPU can only be configured on a 'for AI' base model (7D9ECTO3WW), while a non-controlled GPU only goes on the non-AI models. You cannot switch MTM inside a config, so start a NEW one on CTO3WW. Also p.80: no GPUs with CPU TDP over 300W, no flash storage adapters, no middle/rear bays, all GPUs identical, a DW GPU in slot 2/5/7 kills slot 1/4/8. Factory-installed CBU5 is on 7D9ECTO3WW only. Base 7D9ECTO1WW offers CGNJ 'GPU-Ready Installation' (no charge): lp1610 p.79 says it ships power cables/ducts/PSUs/fans 'without actually including the GPUs themselves', and GPU-Ready codes are NOT offered on CTO3WW. The card can ride the same CTO1WW order as option PN 4X67B09095, but on 2026-09-28 the loose option part was ~13% more than the factory CBU5 feature code on CTO3WW, so the CTO3WW path is factory-integrated and cheaper. Build both and compare. NVIDIA-Certified inference guidance (docs.nvidia.com, 2026-09): system RAM min 2x total GPU memory spread across all channels, min 6 physical CPU cores per GPU. SR655 V3 is single-socket, DIMM qty 1/2/4/6/8/10/12 (lp1610 p.27).

*Source: Lenovo Press lp1610 p.27, p.78-80; DCSC exports 2026-09-28; docs.nvidia.com*

## CFD6 SN861 1.92TB U.2 NVMe priced over 2x a TCE VA 7.68TB (2026-09-28). Use the VA line, and use a Gen5 NVMe backplane, not AnyBay

`sr655v3-sn861-drive-price-trap` | **proven** | scope: SR655 V3|AMD V3 | verified: 2026-09-28

SR655 V3 for AI export 2026-09-28 (7D9ECTO3WW, 2x CBU5 factory, EPYC 9335, 12x CBN9 32GB = 384GB): ONE CFD6 SN861 1.92TB drive was ~15% of the whole server price. lp1610: SN861 CFD6/5/4/3 all Not TCE; VA U.2 PCIe 5.0 RI C0ZU 3.84TB and C0ZT 7.68TB are TCE (C0ZV 1.92TB and C0ZS 15.36TB are not), matching the 3.2-7.68TB TCE window. The C0ZT 7.68TB is less than half the price of the 1.92TB SN861 at 4x the capacity. The BH8B AnyBay backplane is Gen4 and exposes SAS/SATA, which forced a BMFT 540-8i that cannot drive NVMe; BS7Y 8x2.5in NVMe Gen5 backplane (TCE) removes the controller.

*Source: Lenovo Press lp1610 drive + backplane tables; DCSC exports 2026-09-28*

## ROBO-branded HX models exist ONLY in V3 (HX630 V3 ROBO IS 7D6MCTO2WW / CN 7D6MCTO4WW); V4 has no ROBO SKU but HX630 V4 lists ROBO/Edge as a target workload and supports 2-node

`hx-robo-v3-only-v4-folds-in` | **proven** | scope: HX630 V3|HX630 V4|HX650 V4|ThinkAgile HX|Nutanix | verified: 2026-09-28

lp1667 Table 1: HX630 V3 ROBO = 1 or 2 CPUs (standard HX630 V3 = 2 only), cluster sizes 1, 2*, 3+ (standard 1 or 3+; *2-node under limited workload conditions), 4x 3.5in SAS/SATA front + optional 2x 2.5in rear, hybrid or all-flash, 440-8i HBA, target 'Entry, SMB, ROBO/Edge'. CTO w/ controlled GPU: ROBO IS 7D6MCTOBWW, ROBO CN 7D6MCTODWW. Built on SR630 V3, Xeon 5th Gen. lp1667 updated 2026-07-07, NOT withdrawn; a 2026-06-30 export of HX630-Robo V3 CN x3 (BRP1 base, BTS9, 1x BYW4 4510 12C + CPU dummy, 8x16GB, 2x BA4Y 1.92TB SATA, BM51 440-8i, BNFG 750W 115V) had no BU1E. V4: lp2132 HX630 V4 Table 1 target workloads include 'ROBO/Edge', note '2-node cluster is supported with HX630 V4 under limited workload conditions', 2-node max 20 TB storage per node, but 2 CPUs required and all-flash NVMe/E3.S only. Single socket moved to HX650 V4 (1 CPU = 8x 2.5in NVMe, 16 DIMMs, 4TB); 3.5in hybrid moved to HX650 V4 Storage (1 or 2 CPU). lp2133 lists HX650 V4 cluster sizes as 1 or 3+. C0U4 1300W 230V/115V is TCE on 7DG3CTO1WW, 7DG4CTO1WW and 7DG4CTO2WW. Same-site comparison: a 3-node HX630 V4 TCE build (2x 6505P, 256GB, 2x 1.92TB NVMe) came in ~27% above the 3-node V3 ROBO. NCI-Edge (Nutanix datasheet): per powered-on VM, max 5 nodes, 25 VMs per cluster, 96GB per VM, dedicated cluster; so the HX630 V4 2-CPU rule costs no license on NCI-Edge. Not in lp2132/lp2133 license tables.

*Source: Lenovo Press lp1667 p9/p13/p15, lp2132 p8/p16, lp2133 p7-8; Nutanix NCI-Edge datasheet; DCSC exports*

## Dell PowerEdge R360 (8x2.5in, PERC H355, 4x1GbE 5719) -> SR250 V3 all-TCE: C524 8C, 2x C527, B8NY 940-8i (5977 unconfigured), BRG7, AUZV, BMWQ, BWM5, SBCV; no CMA exists, both PCIe slots end up full, so M.2 boot cannot be added

`sr250-v3-dell-r360-match` | **proven** | scope: SR250 V3|Dell R360 | verified: 2026-09-28

Every line proven in BU1E SR250 V3 exports (2026-08/09). The E-2486 6C 3.5GHz 95W match is C523 6349P (Not TCE per lp1802 p23); E-2436 BWMB is the only E-2400 and also Not TCE. PERC H355 is front-mounted; the Lenovo RAID 5 card B8NY takes a PCIe slot, so with AUZV both LP slots are used. CDNK 545-8i Internal is slotless but RAID 0/1/10 only (and never exported on SR250 V3). lp1802 p53 Table 49: BK7W/B7L3/B6H2 all CMA=None, half-out friction, no in-rack maintenance, so a Dell CMA line has no equivalent. 800W (BWM3/BWM5) is the only hot-swap PSU. lp1802 p28: the M.2 adapter (BM8X) mounts on a dummy PCIe card (BMTU) in a PCIe slot, so 940-8i + 4-port NIC leaves no room for M.2 boot; Dell BOSS Blank = no boot drive, so the match has none. iDRAC9 Enterprise = SBCV XCC2 Platinum FOD. COMMON AUTO-MAPPER ERRORS on this BOM: picking C521 (off the TCE panel) or a single C528 (not in the TCE memory panel), pairing CDNK with RAID 5, leaving iDRAC9 Enterprise unmapped (it is SBCV), picking the AX8A 4.3m cord over 6313 2.8m.

*Source: Lenovo Press lp1802 p23/p28/p33/p43/p53; DCSC exports*

## Dell T160 with PERC H755 + SAS Mixed Use SSD maps to ST250 V3, not ST50 V3; the 540-8i is cacheless RAID 0/1/10 only, so an H755 RAID 5 needs the 940-8i

`dell-t160-to-st250-v3` | **proven** | scope: ST250 V3|ST50 V3|Dell PowerEdge T160 | verified: 2026-09-29

ST50 V3 is the T160's size peer but fails three ways: SAS drives not supported (lp1907 p3), SSDs are Read Intensive SATA only (p35-36), RAID cards are 540-8i/545-8i only (p32). ST250 V3 has NO SAS SSDs either, SATA only (lp1803 p41-44), and Lenovo makes no 1.6TB SATA SSD; 1.92TB MU is Not TCE in 2.5in (BYM5) and 3.5in (BYM8). RAID 540-8i (BMFT): cacheless, RAID 0/1/10 only, no RAID 5 (lp1552 p3-4); H755 equivalent is B8NY 940-8i 4GB + AUNP (12 of 12 ST250 V3 exports pair them). The 6337P is C522 on ST250 V3, Not TCE (lp1803 p26); C520 6325P 4C 3.5GHz is the TCE clock match. BCM5720 2x1GbE is onboard on ST250 V3 (lp1803 p14). A 2026-09-29 export proves BU1E with BZB9 + B41E + BMFT + 6x BYM4 960GB MU + C524 + 2x C527 + SDA9 + SDDQ. COMMON AUTO-MAPPER ERRORS on this BOM: claiming ST250 V3 has no onboard LOM and adding AUZV, omitting the BZB8/BZB9 chassis base, AUNP and 5978, and saying Windows/CALs break TCE (SDA9 is in 13 BU1E ST250 V3 exports). BYLX 3.5in 3.84TB MU: lp1803 p44 and a July catalog crawl say TCE, a later catalog check said not, and no ST250 V3 export has it.

*Source: Lenovo Press lp1907 p3/p32/p35, lp1803 p14/p26/p41-44/p53, lp1552 p3-4; DCSC export 2026-09-29*
