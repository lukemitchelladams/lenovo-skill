# Rules distilled from real competitor-to-Lenovo conversion builds. Loaded by kb_facts.py.
# Same schema as kb_facts.py.
# Tuple order: topic, scope, status, title, body, source, verified
# status: proven | flagged | unknown
#
# All customer, partner, reseller and person names, deal and quote numbers and prices have
# been removed. Price insights are kept only as ratios or direction. TCE membership
# ROTATES per MTM and per date: every TCE statement carries a date, treat it as a lead to
# re-check on the live DCSC panel (feature code BU1E present in the built config).

FACTS = [

("de4200h-sas-host-attach-needs-hic-and-440-16e",
 "DE4200H|DE Series|SR635 V3|SR645 V3|SR630 V4|SR650 V4|440-16e|940-8e", "proven",
 "Direct SAS-attaching a host to a DE4200H needs a 12Gb SAS HIC in each DE controller (C3HQ) AND an external SAS HBA in the host (440-16e B8P7), never a RAID adapter; 'Hybrid SAS' in the name is the drive side",
 "DE4200H out of the box has only 4x 10/25Gb iSCSI base ports (2 per controller, lp2071 p7). The two 12Gb SAS x4 ports on each controller are EXPANSION ports "
 "for DE240S/DE600S shelves (lp2071 p5), not host ports, so 'Hybrid SAS 2U24' describes the drives, not host connectivity. A DCSC export with C3HX "
 "'Blank HIC Blank Face Plate' has no SAS host port at all. HIC choices (lp2071 p11, one per controller, max 2): C3HQ 12Gb SAS 4-port (TCE), BWTF 16/32Gb FC "
 "4-port (TCE), BWTH 10GBASE-T 4-port (TCE), BWTK 25/10GbE 4-port (Not TCE); DCSC also has a host-connectivity selector (B4D9 SAS, B4DB 10G BaseT iSCSI, "
 "B4DC iSCSI optical). HOST SIDE for SAS: an external HBA, B8P7 ThinkSystem 440-16e (TCE on SR635 V3, lp1609 p67; 440-8e BNWK is Not TCE there). "
 "Do NOT use the RAID 940-8e (BNWJ): its supported external enclosures are the D1212/D1224/D3284/D4390 JBODs only (lp1586 p3) - the DE controllers do the RAID. "
 "CABLES (lp2071 p12, controller-to-host, TCE): AU16 0.5m, AU17 1m, AU18 2m, AU19 3m External MiniSAS HD 8644/8644. Order them on the HOST config, not the DE: the DE4200H CTO offers no cables in DCSC (rules snapshot 2026-09-30), while server CTOs carry them (BU1E SR630 V4 exports with AU19 alongside an external HBA). The SR635 V3 default option list does not show AU16-AU19 either, so confirm they appear once the 440-16e is selected (flagged). "
 "PORT MATH: two C3HQ = 8 SAS host ports = up to 4 hosts dual-path with no switch; the 4 iSCSI base ports dual-path only 2 hosts without a switch. "
 "iSCSI over the base ports needs no host adapter at all (the hosts' 10/25GbE NICs) but does need SFP28 modules or DACs on both ends. "
 "Confirm the OS and HBA combination in LSIC (lp2071 p33). "
 "DCSC MECHANICS: the host-connectivity selector (NETWORK_ADAPTER_CFC) and the HIC section are NOT required; iSCSI on the base ports needs no line at all, only the "
 "base-port optics (B4K9 10G, B4B4 or C4K4 25G, selectable without a HIC). The HIC list stays locked (q=[0]) until a connectivity type is picked. "
 "PROVEN both ways: a DE4200H export with 2x C3HX blank HICs (iSCSI base ports) and one with 2x C3HQ SAS HICs both carried BU1E with 0 criticals (2026-07/08).",
 "Lenovo Press lp2071 p5/p7/p11/p12/p33, lp1609 p67, lp1586 p3; DCSC rules crawl 2026-09-30; DCSC exports 2026-07 to 2026-09", "2026-10-01"),

("hx-sizer-nic-to-dcsc-mapping-ocp-mandatory",
 "HX630 V4|HX650 V4|Nutanix Sizer", "proven",
 "Nutanix Sizer NIC lines do not build as written on HX: the OCP slot is mandatory, ConnectX-6 Lx has no 10GBASE-T, and Sizer ships zero optics",
 "(1) The OCP slot is mandatory on HX. A Sizer line of '2x Mellanox ConnectX-6 Lx PCIe per node, No FLOM NIC' was built as 1x BE4T (OCP) plus 1x BE4U (PCIe): the same ConnectX-6 Lx silicon, the same 4x 10/25GbE ports per node, one NIC vendor. "
 "DCSC blocks a build that omits the OCP adapter altogether (an automated mapper produced one on a single-socket-source cluster, 2026-08-05). "
 "(2) ConnectX-6 Lx has no 10GBASE-T variant on HX, so a Sizer BOM with Broadcom 10GBASE-T LOM ports plus Mellanox 25GbE (mixed vendor) has to pick one vendor. "
 "All-Broadcom: B5ST 57416 10GBASE-T OCP plus 2x BK1H 57414 10/25GbE SFP28 PCIe = 2 copper plus 4 SFP28 per node, which matches the source port layout. "
 "All-Mellanox: 1x BE4T plus 2x BE4U (plus BE05 bracket) = 6 SFP28 and no copper. On one 3-node HX650 V4 pair the two builds differed by about 0.1 percent in list price, so the decider was copper, not price. "
 "(3) REPORTED, not re-verified in the product guide: RDMA needs the ConnectX PCIe adapter with a minimum of 2 per node. "
 "(4) BN2T OCP plus BK1H PCIe plus BNWM 57504 4-port PCIe gives 8 SFP28 ports per HX650 V4 node, all Broadcom. "
 "(5) Sizer BOMs, like DCSC BOMs, carry ZERO transceivers or DACs: multiply ports by nodes and add optics (TCE options seen: AV1B, BF10, BYBJ dual-rate 10G/25G SR SFP28) or DACs. "
 "See hx-nic-vendor-rule-two-conflicting-statements for the vendor-mixing rule itself.",
 "DCSC exports 2026-08-05 to 2026-08-18; Nutanix Sizer BOMs", "2026-08-18"),

("hx-60-month-term-three-line-edit",
 "ThinkAgile HX|HX650 V4|HX630 V4|SR650 V3|SR650 V4|ST250 V3", "proven",
 "Converting an HX config from 36 to 60 months is THREE edits (B0W1 to B0W2, Premier months, KYD months); service price scales with platform tier and term",
 "(1) Base tab: B0W1 '3 Years' to B0W2 '5 Years', the appliance-term feature code under B15S (Nutanix software stack). ThinkAgile HX has a SELECTABLE base (B0W1 3yr, B2UW 4yr, B0W2 5yr, verified on 7DG4CTO2WW). "
 "ThinkSystem SR650 V3 and V4 CTOs (7D76, 7DGD) were seen with a 3-year base only, and a 1-year request cannot be met on SR650 V3 (3 years is the minimum: quote 3-year Premier). "
 "(2) Services: the Premier parent SKU's QA0Y 'Months' field = 60 x number of nodes. "
 "(3) Services: the Keep Your Drive (KYD) parent SKU has its OWN QA0Y Months field, also 60 x nodes; leaving it at 36 lets drive retention expire two years before support. "
 "Worked values: 3 nodes 180, 4 nodes 240, 5 nodes 300, 32 nodes 1,920; a 6-server 36-month quote reads 216. XClarity One moves separately from SCJD (3yr) to SCJE (5yr). "
 "PRICE CAUTION (unverified): Premier is an upgrade over the base warranty, so base = 5 Years AND 300 Premier months may double-charge years 4 and 5. Pull the DCSC price preview both ways (B0W1 plus 300 versus B0W2 plus 300) and use the one that does not double-bill. "
 "RATIOS: 60-month Premier lists about 3x the 36-month price on SR650-class servers because years 4 and 5 sit outside the base warranty (expected, not an error); "
 "Premier NBD 60 months listed about 2.9x higher on SR630 V4 than on ST250 V3 for the same nominal service, so re-price services whenever a customer moves up a platform tier; "
 "on a storage array Premier rose about 1.9x when raw capacity rose about 2.2x.",
 "DCSC exports 2026-07-10 to 2026-09-03", "2026-09-03"),

("hx-dcsc-feature-code-glossary-and-no-nutanix-licence-lines",
 "ThinkAgile HX|HX650 V4|HX630 V4|SR630 V4", "proven",
 "HX feature codes seen in DCSC exports, and a Certified Node config carries NO Nutanix licence lines",
 "B15S Nutanix AHV stack (no charge). B6C1 = licensed node cores and B6C2 = licensed node capacity in TiB, both informational and no charge (for example B6C1 = 72 on 3 nodes of 1x 24C); B6C2 is TiB, convert before quoting TB. "
 "B0W1 / B2UW / B0W2 = 3 / 4 / 5-year appliance term. B4Z6 = deployment service selector (None means no Lenovo deployment is in the config; HX Remote Deployment appeared as 5MS7B00045 on an earlier revision). "
 "B7Y0 Enable IPMI over LAN. BPKR TPM 2.0. C3K9 XClarity Platinum Upgrade v3. SCY0 XCC3 Premier FOD. SCJD / SCJE XClarity One Standard 3yr / 5yr. "
 "CK17 = 'Nutanix Compute-Only node', a feature on the ThinkSystem SR630 V4 CTO 7DG9CTO1WW and not an HX MTM. "
 "SW-defined support SKUs on HX: 7Q04CTS2WW Premier NBD, 7Q04CTS4WW Premier 24x7 4hr, 7Q04CTSAWW KYD, against the 7Q01 family on plain ThinkSystem. "
 "NO NUTANIX LICENCE LINES: a pair of HX650 V4 Certified Node configs (2026-07) held zero NCI, NUS, NCM, NDL or EUC feature codes, only B15S at no charge plus the term code. "
 "So Nutanix software is bought from Nutanix, the Lenovo quote is hardware plus support only, support has two entitlements underneath, and any licence shortfall on a Sizer output is the Nutanix rep's to fix, not a Lenovo BOM defect. "
 "Example CTOs: HX650 V4 Certified Node 7DG4CTO1WW; HX665 V3 Certified Node 7D9NCTO3WW.",
 "DCSC exports 2026-07-31 to 2026-09-18", "2026-09-18"),

("hx-dcsc-spurious-370tb-warning-and-aos-capacity-bands",
 "ThinkAgile HX|HX630 V4|HX650 V4|Nutanix AOS", "proven",
 "DCSC warns 'Per node storage capacity over 370TB' on HX exports even at 30-50TB per node; the real Nutanix bands are 307-370TB per node with AOS 7.3+",
 "DCSC message on HX configs: 'Per node storage capacity over 370TB is only supported for Nutanix Unified Storage use cases.' It fired on 4 of 4 builds whose densest node was 30.72TB and on two clusters at roughly 38 to 48TB per node, so it is spurious for those builds, not a sizing problem; note it and move on. "
 "The real thresholds that Sizer surfaced: nodes between 307TB and 370TB need EVERY node in the cluster above 185TB and AOS 7.3 or later; the AOS 7.6 note says a greenfield cluster must start above about 92TB initial capacity to scale past the 307TB / 185TB cap. "
 "A node of 12x 24TB HDD plus 4x 15.36TB NVMe computes to about 349TB raw, squarely inside that band. "
 "Sizer also emits an NDL shortfall warning ('The NDL licenses configured on this scenario are insufficient for the storage configured in the solution. Nutanix assumes the customer has additional NDL licenses to cover the shortfall.'): forward it verbatim to the Nutanix rep because it is a Nutanix licence gap. "
 "'CVM resources opted is lower than what was recommended' is a Sizer warning about the customer's own sizing choice, again not a Lenovo defect.",
 "DCSC exports 2026-07-31 to 2026-09-03; Nutanix Sizer output", "2026-09-03"),

("nutanix-sizer-bom-reading-traps",
 "Nutanix Sizer|ThinkAgile HX|Nutanix NX", "proven",
 "Reading a Nutanix Sizer BOM: Term-Months is the contract term, 'N-core config' is ambiguous, revisions change platform silently, and multi-node blocks map per node",
 "TERM-MONTHS is the contract term (36, 60), not a per-node figure; do not multiply by node count and do not look for it as a node count (60 months = 5 years). "
 "CORES: a customer who labels configs 'X-core' and '2X-core' usually means cores PER CLUSTER, but the same label can also be a fleet total. NCI and NCM license per core, so the wrong reading doubles the licence (a fleet total of 2X becomes 4X). Ask which before building. "
 "REVISIONS: diff a revised Sizer file against the built BOM line by line. One revision moved an all-flash Files/Objects cluster to the hybrid HX650 V4 Storage model (7DG4CTO2WW) and silently changed base code, Flash to Hybrid node config, CPU 6527P 24C 255W 3.0GHz to 6520P 24C 210W 2.4GHz (same cores, lower clock), memory 8x 64GB to 16x 32GB (same 512GB), NVMe count cut sharply with 3.5in HDDs added, and NICs (BE4T plus AUKP), with 'No FLOM NIC Selected' against an OCP card in the build. Ask before rebuilding. "
 "Support levels can differ between clusters in the same Sizer (24x7 4hr on DR, NBD on production); confirm rather than change. "
 "MULTI-NODE BLOCKS: a 2U block holding 3 nodes maps each node to one 1U server, not the block to one 2U server. Automated mappers also omitted the mandatory OCP adapter, populated 2 DIMMs per CPU (not an allowed quantity on HX630 V4) and dropped the backplane and power cords: check all four. "
 "NX to HX is a vendor swap on the SAME Xeon 6 generation (a 6505P source maps to C5QQ silicon), so it is not a CPU-driven node reduction: node count comes from Nutanix's own Collector or Sizer run and nothing should be claimed beyond it. "
 "The Sizer NVMe line may name a Gen5 drive; verify the PCIe generation of the HX-branded part (the C3Q9 was described as Gen4) before promising it.",
 "Nutanix Sizer BOMs 2026-08-05 to 2026-08-18; DCSC exports", "2026-08-17"),

("nic-ocp-pcie-twin-map-and-second-ocp-cable-kit",
 "SR630 V4|SR650 V4|HX630 V4|HX650 V4|HX665 V3|SR645 V3", "proven",
 "OCP and PCIe twin NIC feature codes, how to quote a field-added PCIe NIC, and the C1YK plus CA9A/CA9B kit a second or x16 OCP adapter pulls in",
 "SAME-SILICON TWINS (OCP / PCIe): BN2T / BK1H Broadcom 57414 10/25GbE SFP28 2-port; B5ST / AUKP Broadcom 57416 10GBASE-T 2-port; C4GB / C4GC Broadcom 57412 10GBASE-T 4-port; BPPW / BNWM Broadcom 57504 10/25GbE SFP28 4-port; "
 "BCD4 / BCD6 Intel E810-DA2 10/25GbE SFP28 2-port; BE4T / BE4U ConnectX-6 Lx 10/25GbE SFP28 2-port; C4HU / C4HT Intel E610-T4 10GBASE-T 4-port; B5T1 / AUZV Broadcom 5719 1GbE 4-port; "
 "C62H / B8PP ConnectX-6 Dx 100GbE QSFP56 2-port; BPPX (OCP, Not TCE) / BK1J (PCIe, TCE) Broadcom 57508 100GbE. Check the OCP twin before spending a PCIe slot. "
 "ADDING A NIC TO A SHIPPED NODE: quote the PCIe twin as its own line so the big quote is not repriced (BK1H is the exact PCIe twin of BN2T: same chipset, speed, ports, driver and vendor, so the HX single-vendor rule holds). "
 "Confirm a free riser slot (a shipped HX665 V3 carried an empty x16/x8/x8 riser), remember it is a FIELD install unless factory-integrated, and that every added SFP28 port needs its own optic or DAC (30 cards means 60 optics). "
 "Whether an M.2 RAID adapter consumes a riser slot on that platform was not confirmed: check free slot count in DCSC. "
 "SECOND OR x16 OCP: on SR650 V4 and HX650 V4 a second OCP adapter, or an x16 OCP card such as the 4-port BPPW, brings in the C1YK OCP x16 cable kit plus CA9A/CA9B OCP expansion (both appeared when BPPW replaced a 10GBASE-T OCP card on a TCE-clean SR650 V4, and both disappeared when an HX650 V4 went from two BN2T to one). "
 "So when 'the NIC changed' is the only stated difference between two revisions, compare the line count: the cable kit and expansion lines move with it.",
 "Lenovo Press lp1971 Tables 65 and 67; DCSC exports 2026-07-16 to 2026-08-20", "2026-08-20"),

("sr630v4-nutanix-compute-only-node-ck17",
 "SR630 V4|7DG9CTO1WW|Nutanix compute-only", "proven",
 "Nutanix compute-only node on Lenovo is a ThinkSystem SR630 V4 CTO with feature CK17; two proven builds, and the sizing logic for compute-only 1U nodes",
 "MTM 7DG9CTO1WW labelled 'ComputeOnly : ThinkSystem SR630 V4' carries CK17 'Nutanix Compute-Only node'. It is not an HX MTM, and the HX-guide single-vendor NIC sentence is not in the SR630 V4 guide (lp1971), so treat NIC mixing as a ThinkSystem question. "
 "BUILD 1 (BU1E present, 10 nodes): 2x C5QX Xeon 6737P 32C 270W, 32x C0TQ 64GB (2TB), C1XE 1U 10x2.5in chassis with no data drives (5977 no RAID), CCCZ plus 2x C286 480GB M.2 boot, 2x C0U3 2000W 230V-only, 4x C1YT performance fans. "
 "BUILD 2 (two clusters of 3): 2x 32C or 2x 24C Xeon 6 per node, 16x C0TQ (1TB), CCCZ plus 2x C287 960GB M.2, BN2T 25GbE OCP with BPP5 filler leaving the second OCP slot free, 2x C2Y9 1300W. "
 "LOGIC: 1U is right because a compute-only node carries no data drives (6 nodes are 6U against 12U for SR650 V4). SR630 V4 accepts CPUs up to 350W, so 255W parts fit in 1U, but 270W CPUs with four adapters need a DCSC thermal re-check. "
 "The mirrored M.2 pair on the B550p-2HS RAID kit is standard on Nutanix builds and should not be flagged as removable; an automated mapper emitted ONE M.2 alongside the RAID kit, and a mirror needs two. "
 "On an external-storage cluster every storage IO crosses the network, so recommend 100GbE (C62H ConnectX-6 Dx OCP) even if the customer asks for two 25GbE ports: two 25GbE shared by VM and storage traffic is roughly 3 GB/s usable per node once one path is reserved for failover. "
 "Automated mappers returned a VX650 V4 with a VMware stack on a Nutanix ask: always name the HX or compute-only model explicitly, and pin the exact DIMM count because one pass emitted 12x 96GB (6 per socket, two channels empty) while calling it balanced.",
 "DCSC exports 2026-08-14 and 2026-09-09 to 2026-09-18", "2026-09-18"),

("nci-compute-only-external-storage-lenovo-support-gap",
 "Nutanix NCI compute-only|ThinkSystem SR630 V4|ThinkSystem SR650 V4", "flagged",
 "NCI compute clusters on an external array: FC is not a supported attach, and Lenovo compute was supported only against Lenovo storage (targeted about Q3 2026, not GA at lp2421 rev 30 Apr 2026)",
 "Supported external-storage attach for a Nutanix NCI compute cluster is NVMe/TCP, NFS and Dell PowerFlex SDC; Fibre Channel is NOT supported, so an FC-attached source cannot move to that design and falls back to compute-only nodes hanging off HCI nodes. "
 "Cisco UCS B-Series blades are on the supported server list for NCI compute clusters. "
 "As of Lenovo Press lp2421 (revision 30 Apr 2026), Lenovo compute is supported only against Lenovo ThinkSystem storage, targeted about Q3 2026 and not GA at that revision; one all-flash array vendor's own supported-server list at the time named Cisco, Dell and HPE and no Lenovo. "
 "So a customer keeping an existing third-party array under Lenovo compute may have no orderable supported answer: either replace the array in the same proposal or reposition to HX HCI, and say so early. "
 "Re-check the current lp2421 revision and the array vendor's list before quoting; the blade family named (Cascade Lake B200 M5) has been end of sale since 2023, so verify the exact model on the HCL. "
 "'Compute only, no storage' from a customer usually means the storage sits on an array, not that none exists: ask what array and how it is attached before designing anything, and do not describe a 3-node HX HCI cluster as compute-only.",
 "Lenovo Press lp2421 rev 2026-04-30; Nutanix HCL as reported 2026-08-14", "2026-08-14"),

("cluster-right-sizing-from-collector-and-node-failure-method",
 "HX630 V4|HX650 V4|SR630 V4|Nutanix Collector|Live Optics", "proven",
 "Right-size from the customer's own Collector or Live Optics data (consumed, not provisioned) and test the node-failure case; worked levers from HX conversions",
 "USE CONSUMED storage and observed peak or average utilisation, never installed or provisioned capacity, and state the caveats: collector age, 7-day window, growth since, DR, replication and VDI plans, and that Nutanix must bless the sizing. "
 "WORKED CONTRAST: a 3-node HX630 V4 quote carried about 4x the memory (512GB per node against a few hundred GiB of provisioned vRAM across about 20 VMs) and about 6.5x the consumed storage, with cluster CPU at 16 percent. "
 "Levers used: 512GB to 256GB per node by moving 24x C0TQ 64GB to 24x C0U9 32GB (TCE), about half of the memory list; and 2x 15.36TB to 5x C3Q9 3.84TB per node (19.2TB), which cut licensed TiB by about 38 percent while adding spindles. CPU was already entry level. "
 "FAILOVER METHOD: memory left after losing one node must cover peak RAM. Two nodes at 256GB leave 256GB against a peak of about 180GB; three nodes at 96GB leave 192GB, clearing peak by only about 10GB, so 2x256GB beat 3x96GB. "
 "A tiny estate (peak CPU in the low 20s percent, peak IOPS under 1,000, 2 hosts) does not justify a 3-node HX: a 2-node SR630 V4 at 192GB per node still survives one node loss. "
 "Windows Server Standard and VMware license at a 16-core minimum, so moving 16C to 8C saves nothing on software. "
 "Drive swaps that preserve raw capacity change failure behaviour: halving the drive count (4x 7.68TB to 2x 15.36TB per node) means less I/O parallelism and twice the data to rebuild per drive loss.",
 "Nutanix Collector and Live Optics outputs; DCSC exports 2026-07-16 to 2026-09-02", "2026-07-16"),

("requote-higher-after-leaner-config-diagnosis",
 "HX650 V4|HX630 V4|Nutanix", "flagged",
 "A requote that comes back HIGHER than an earlier one despite a leaner config: check the July 2026 price increase and scope mismatch before suspecting an error",
 "CASE: an HX650 V4 cluster requoted in July 2026 came back above the June quote although every hardware change was cheaper or equal (CPU 6517P 190W 3.2GHz to 6515P 150W 2.3GHz, 960GB to 480GB M.2, two NICs to one). "
 "When nothing changed can raise the price the cause is external: the 2026-07-01 Lenovo and Nutanix price increase (an HX630 V4 requote in the same month followed the same pattern), plus scope mismatch. "
 "The June quote bundled SW-defined Premier NBD 36 months plus SW-defined KYD plus XClarity One SCJD; the July quote showed a 3-year Premier NBD hardware SKU and dropped KYD and XClarity One, used a different PSU (C0U5 Platinum to C0U4 Titanium) and a different redundancy policy (BE0F no oversubscription to BE0E with oversubscription), and came from a different account owner. "
 "LEVER: ask whether the original bid, which predates 1 July, can be extended or re-released to hold pre-increase pricing rather than requoting into the new price; pull per-line pricing on both quotes to confirm scope and the size of the increase. "
 "Cause is inferred from the pattern, not from line-level prices.",
 "Lenovo quotes compared 2026-07-23; DCSC exports", "2026-07-23"),

("fx630-v4-solution-code-and-vmware-preload-codes",
 "FX630 V4|SR630 V4|SR635 V3|ThinkAgile FX", "proven",
 "FX630 V4 is any-to-any: a Nutanix bid built on the VMware vSAN solution code is wrong even when the hardware matches; VMware preload and vSAN feature codes",
 "FX630 V4 supports VMware, Nutanix and Microsoft stacks (HX is Nutanix-only). A Nutanix quote was found built on the VMware vSAN stack: C91V ESXi 9.0 preload, BT2G / BYRM vSAN ESA, CFU5 VMware solution code and 9207 VMware Specify, while the physical hardware already matched the Sizer 100 percent (2x C5QV 6517P = 96 cores across 3 nodes, 16x 32GB per node, C0BA 3.84TB NVMe, BE4T OCP plus BE4U PCIe ConnectX-6 Lx: one vendor, RDMA-correct). "
 "Fix: rebuild in DCSC with the Nutanix solution code and leave the hardware alone; do not send the quote until corrected. "
 "BZ97 is the factory ESXi 8.0 U3 preload (seen on SR630 V4 and SR635 V3 builds). Leave Software Preload = None when a third-party stack is installed on top. "
 "An HDD plus RAID design cannot become an FX630 V4 box and its TCE PSU is 230V-only, so a 115V build (BK14) cannot be converted unchanged.",
 "DCSC exports 2026-07-14 and 2026-09-10; Lenovo Press lp2132", "2026-09-10"),

("xeon6-tdp-not-monotonic-and-no-28c-mapping",
 "SR630 V4|SR650 V4|HX650 V4|Xeon 6", "proven",
 "Xeon 6 TDP and clock are not monotonic in core count (24C 255W 3.0GHz vs 32C 225W 2.3GHz), there is no 28-core part, and AMD is not a lower-power story at equal cores",
 "C659 6527P 24C is 255W at 3.0GHz; C5QT 6530P 32C is 225W at 2.3GHz; C5QX 6737P 32C is 270W. Stepping up in cores can therefore LOWER the clock and the per-socket draw, and a cluster of 24-core nodes can draw more per socket than a 32-core one; all sit inside the 350W CPU ceiling of SR630 V4. "
 "There is no 28-core Xeon 6 and no Silver or Gold tier: a 28C Gold 5520+ (205W, V3 BYW7) maps to 24C (fewer cores) or 32C (more), so phrase it as a licensing fallback decided by per-core licensing, not as a match, and name Xeon 6 configs by core count. "
 "Against a Cascade Lake Gold 6242 (16C 2.8GHz) the 16C 6515P runs 2.3GHz and the 6520P and 6530P run 2.4 and 2.3GHz: claim architecture and memory bandwidth, never frequency. "
 "EPYC 9135 16C is 200W at 3.65GHz against 150W for a Xeon 6515P 16C; a 2-node comparison measured about 11 percent higher nominal maximum draw on the AMD build (roughly 780W against 700W at 115V), so do not take a power angle into a colo conversation. "
 "C5R7 6714P 8C 165W 4.0GHz is a high-frequency SKU: on 2026-08-21 it was the only 8C listed on SR630 V4 and cost about 3.8x a 16C C5RD, while on 2026-09-02 C5R6 6507P 8C listed at about 0.98x a C5RD 16C. Neither saves money, and Windows and VMware still license 16 cores.",
 "DCSC exports 2026-08-14 to 2026-09-02", "2026-09-02"),

("amd-v3-epyc-parts-that-do-not-exist-and-substitutions",
 "SR635 V3|SR645 V3|SR655 V3|SR665 V3|EPYC 9004|EPYC 9005", "proven",
 "EPYC 9634 (84C) and 9354P do not exist on Lenovo AMD V3; substitutes, exact-match codes, and why the P-suffix 96C part is the pick for single socket",
 "A competitor BOM naming EPYC 9634 (84C Genoa) or 9354P (32C Genoa, 1P) needs a substitute; the same 28-SKU EPYC list was seen across SR635 V3, SR655 V3 and SR665 V3 (2026-07-24). "
 "For 9634: C2AN 9645 96C 320W Turin (12 more cores, newer generation, lifts that node's memory from 4800 to 6400 and matches the volume SKU elsewhere in a fleet) or, when per-core licensing matters, C2AS 9565 72C or C2AL 9535 64C. "
 "For 9354P: C2AV 9355P 32C 280W 3.55GHz Turin, 1P-only, same cores and higher clock. "
 "EXACT matches: 9654 = BPVK, 9555 = C2AY, 9555P = C2AW, 9645 = C2AN. Other codes: BREE 9124 16C 200W 3.0GHz, C2AK 9135 16C 200W 3.65GHz, BREC 9334 32C 210W 2.7GHz (Genoa), C2AQ 9335 32C 210W 3.0GHz (Turin), BPVJ 9554 64C. "
 "Single-socket 96C: C2AX 9655P and C2AU 9655 are the same 96C 400W in a 1S box and the P part lists cheaper. "
 "A 400W part appears only once chassis, thermal and ambient settings allow it, and in June 2026 Turin parts were visible only in DCSC Full Mode; that TCE-mode gap is now stale because C2AQ has since been proven in BU1E exports on SR645 V3. "
 "Turin memory codes are 6400 (CBNC 32GB, CBND 64GB, CBN9 32GB, CBFR 64GB); Genoa memory is 4800 (BQ3D 64GB); CC0A 16GB is not TCE. See amd-v3-cpu-generation-dictates-dimm-speed for the pairing rule.",
 "DCSC catalog snapshot 2026-07-24; DCSC exports 2026-06 to 2026-09", "2026-09-03"),

("lenovo-cto-mtm-quick-map",
 "ALL|ThinkSystem|ThinkAgile|ThinkEdge", "proven",
 "CTO base MTM quick map for V3 and V4 platforms, and why the CTO suffix matters (CTO1WW is standard, CTO2/3/4/B variants restrict options)",
 "ThinkSystem V4: SR630 V4 7DG9CTO1WW (also the ComputeOnly variant with CK17); SR650 V4 7DGDCTO1WW; SR650a V4 7DGDCTO2WW and 7DGCCTO2WW (inference model feature CF3G), Workstation 7DGDCTO4WW and 7DGCCTO4WW. "
 "ThinkSystem V3: SR650 V3 7D76CTO1WW (avoid the SAP HANA CTO 7D77CTO1WW when a standard build is wanted); SR635 V3 7D9GCTO1WW (1U 1S AMD); SR645 V3 7D9CCTO1WW (1U 2S AMD, the only 1U two-socket AMD ThinkSystem); "
 "SR655 V3 7D9ECTO1WW (2U 1S) and its 'for AI' model 7D9ECTO3WW; SR665 V3 7D9ACTO1WW (2U 2S) and its 'for AI' model 7D9ACTOBWW; SR675 V3 7D9R (3U GPU); ST650 V3 quotes carry 7D7A. "
 "Entry: ST45 V3 7DH5CTO1WW; ST50 V3 7DF3CTO1WW; ST250 V3 7DCECTO1WW; SR250 V3 7DCLCTO1WW. "
 "ThinkAgile: HX630 V4 7DG3CTO1WW; HX650 V4 7DG4CTO1WW (all-flash), 7DG4CTO2WW (Storage, hybrid), 7DG4CTO3WW (HX650a); HX665 V3 Certified Node 7D9NCTO3WW; FX630 V4 7DPLCTO1WW. Storage: DM3010H 7DCVCTO1WW; D4390 JBOD 7DAHCTO1WW. "
 "RULE FROM THESE EXAMPLES: CTO1WW is the standard base and higher suffixes are variant models with restricted option lists (storage node, AI, workstation, controlled-GPU). "
 "Choosing the wrong suffix silently removes options: a 2-GPU box built on the base SR655 V3 MTM offered only the no-charge GPU-Ready code and exported with zero GPUs and a suspiciously low price. "
 "A controlled (export-restricted) GPU can only be configured on the 'for AI' model, and you cannot change MTM inside a config: start a new one.",
 "DCSC exports 2026-06 to 2026-09; Lenovo Press lp1610 p.80", "2026-09-28"),

("chassis-backplane-feature-codes-sr630v4-amd-v3-towers",
 "SR630 V4|SR635 V3|SR645 V3|SR655 V3|ST250 V3|SR250 V3", "proven",
 "Chassis, backplane and riser feature codes for SR630 V4, AMD V3 and entry towers (SR650 V4 codes are in the SR650 V4 topics)",
 "SR630 V4: C1XE 1U 10x2.5in chassis; C21X 10-bay NVMe; C21Z 10-bay with 6 SAS/SATA plus 2 AnyBay plus 2 NVMe Gen5; C21W 10x2.5in SAS/SATA seen with 16-port controllers; C21T SAS/SATA-only seen with 8-port controllers (545-8i, 940-8i); C2NN 4x2.5in NVMe Gen5 on onboard ports. "
 "SR635 and SR645 V3: BLK4 1U 10x2.5in chassis (TCE in June 2026; the 4x2.5in Front I/O chassis BQ7M was flagged non-TCE by DCSC that month, though later evidence says structural parts may not gate BU1E, so confirm by BU1E); "
 "backplanes BB3T 10x2.5 AnyBay Gen4, BCQQ 10x2.5 NVMe Gen4, BLKC AnyBay Gen5, BRQX NVMe Gen5, B8N0 8x2.5 SAS/SATA; SR645 V3 BU1W 10x2.5 (6 SAS/SATA plus 2 AnyBay plus 2 NVMe). "
 "SR645 V3 risers: BLK9 LP plus LP, BLK8 LP plus FH, BLKB / BLK7 / BP39 without rear-drive support, BLKE with rear drive (pulls in BDY6, auto-added cage BCGY, BQ26 performance heatsink and 8x BH9M fans). "
 "SR655 V3: BS7Y 8x2.5 NVMe Gen5 (three fill a 24-bay chassis, TCE-buildable) and BH8B AnyBay Gen4 (Gen4, exposes SAS/SATA and so forces a controller). "
 "ST250 V3: BZB8 plus B41D = 4x3.5in; BZB9 plus B41E = 8x2.5in. SR250 V3: BWM1 2.5in chassis, BWM2 3.5in chassis, BMPX 4x3.5in hot-swap backplane. "
 "HX650 V4 16-bay NVMe C9KA needs 2 CPUs; C46H is the rear 2.5in NVMe backplane on HX650 V4 Storage.",
 "DCSC exports 2026-06-24 to 2026-09-28; Lenovo Press lp1607 lp1609", "2026-09-24"),

("dcsc-voltage-and-environment-selectors-are-report-inputs",
 "ALL|SR630 V4|SR650 V4|HX630 V4|HX650 V4|SR645 V3", "proven",
 "BK14 / BK15, BVGL / BL0H, BFYA and BE0E / BE0F are no-charge Power Report inputs, not hardware; read the PSU description, and reset a stale 230V selector before export",
 "BK14 'Low voltage (100V+)' and BK15 'High voltage (200V+)' are no-charge report inputs. Two configs that differ only in the voltage selector but carry the same dual-voltage PSU (a 230V/115V 1300W Titanium CRPS) and the same 6400 C13-C14 jumper cords ship identical parts; only the wattage and amperage math on the Power Report changes. "
 "The same holds for BVGL 30C and BL0H 25C data-centre temperature, BFYA operating mode, and BE0E (redundancy with oversubscription) versus BE0F (no oversubscription). Do not raise such a difference as a config error. "
 "READ THE PSU DESCRIPTION instead: '230V/115V' = dual voltage; a 2000W or 3200W part with no 115V is high-line only and genuinely cannot run on a 120V feed. "
 "REVERSE CHECK: a 230V selector left over from testing makes the Power Report disagree with a 120V wall-power site; reset to the site voltage (BK14 for wall plugs) and re-export before sending. "
 "SITE-POWER METHOD from a worked 115V case: about 740W nominal and 930W worst case on an N+1 pair of 1100W supplies = 6.6A and 8.2A; 8.2A is inside the 12A continuous limit (80 percent of 15A) of a 15A/120V NEMA 5-15 circuit, so a wall-plug quote is fine. "
 "A competitor quote carrying NEMA 5-15P cords implies a 120V feed.",
 "DCSC Power Report tabs and exports 2026-07-10 to 2026-09-03", "2026-09-03"),

("pcie-gpu-8-per-node-has-no-intel-equivalent",
 "SR675 V3|SR650a V4|SR680a V3|SR680a V4", "proven",
 "An 8x double-wide PCIe GPU node (SR675 V3 class) has no Intel ThinkSystem equivalent: SR650a V4 holds 2 to 4 cards and SR680a is HGX/SXM, so conversion is an architecture change",
 "SR675 V3 (3U, AMD) with 2x BR7S 'Switched 4x16 PCIe DW GPU Direct RDMA' risers holds 8 double-wide PCIe GPUs with switched peer-to-peer paths. "
 "SR650a V4 holds 2 RTX PRO 6000 class cards (one CPU) or 4 (two CPUs), and the SR680a V3 and V4 are 8U HGX/SXM platforms (B200, B300, H100, H200) that do not take PCIe RTX PRO 6000 cards. "
 "So 8 PCIe GPUs per node maps to 2 to 4 chassis per original node, and splitting a node's GPUs across chassis changes GPU topology: this is an architecture change, not a substitution. "
 "WORKED COMPARISON: 16 GPUs at 2 per chassis is 8 SR650a V4 chassis (16U) against 2 SR675 V3 (6U) and came out about 17 percent higher in cost; at 4 GPUs per chassis, 4 chassis kept the same totals (16 GPUs, 128 cores) with memory at 2,048GB against 2,304GB (Xeon 6 is 8-channel, so 4 nodes give 2,048 or 4,096GB, nothing between) and about 6 to 7 percent below the original price. "
 "The 4-GPU build used a C46P NVMe-only backplane instead of an AnyBay backplane, which let the 940-8i, its SuperCap and cable come off (about 4 percent of a node) and nearly paid for a CPU clock upgrade. "
 "Do not tell a customer that GPU builds are '8 weeks regardless of platform': a TCE-capable GPU platform changes the lead time, but the GPU card lead time is separate from the chassis, see sr650a-v4-chwt-cbk8-riser-cpu-gates.",
 "DCSC exports 2026-08-14 to 2026-08-17; Lenovo product guides", "2026-08-17"),

("sr650a-v4-chwt-cbk8-riser-cpu-gates",
 "SR650a V4|7DGDCTO2WW|RTX PRO 6000 Blackwell", "proven",
 "SR650a V4 RTX PRO 6000: CBK8 (600W, 2 cards, slots 21/23) versus CHWT (450W cap, 4 cards but ONLY with 2 CPUs); CHWU is an empty slot; the ambient, fan and PSU gates",
 "CBK8 = the full-power RTX PRO 6000 Blackwell Server Edition 96GB on the cable risers C9R5 / CATS ('x16 Cable Riser Slot 21 / Slot 23, up to 600W'); slots 21 and 23 only, so at most 2 GPUs. "
 "CHWT = the same card slot-capped at 450W on the front risers C4U1 to C4U4 (slots 17, 19, 21, 23), which allows 4 GPUs but only with TWO CPUs: the second socket feeds the front riser assembly serving slots 17 and 19, while with one CPU only slots 21 and 23 (riser assembly 7) have a PCIe root. "
 "That single-CPU behaviour is what Lenovo Press describes ('up to two high-watt double-wide adapters (400W to 600W) in Slot 21 and Slot 23 of PCIe riser assembly 7'), so the Press text reads as a hard 2-GPU limit; DCSC built 4x CHWT with 2 CPUs and BU1E on 2026-08-14 and again as a four-node build on 2026-08-17. "
 "CHWU is an EMPTY prepared slot ('GPU-Ready Installation', no charge, no card): the listed parts sum exactly to the Summary total, so a cheap-looking node with CHWU has zero GPUs. If GPU-Ready is the only path, TCE unbundles the chassis lead time from the card lead time: confirm a bookable BU1E-carrying card exists before promising a fast ship. "
 "GATES for the 4-GPU node: 2 CPUs; ambient BL0H 25C (default BVGL 30C fails thermal); 6x CC8X '2U 6056 24K Ultra Fan Module for 600W PCIe Adapter' (5 for a 2-GPU node); 2x C0UD 3200W 230V Titanium CRPS; front riser slots C4U1 to C4U4; 2x C3S1 GPU riser cages; 4x C3QU GPU power cables. "
 "Worked node: 2x C5QV 6517P, 16x BYTJ 32GB (512GB, all 8 channels per socket), 2x C0ZU 3.84TB U.2 on a C46P NVMe-only backplane, CCCZ plus 2x C287, one BQBN ConnectX-7 (rear riser C4U9) and BN2T 25GbE OCP: about 3.0kW worst case per node against one 3.2kW supply under N+N (about 94 percent), so the site needs 230V and roughly 3kW per node. "
 "The 450W cap trades about 25 percent of per-GPU power for the 4-card density and for TCE.",
 "DCSC exports and live builds 2026-08-14 to 2026-08-17; Lenovo Press lp2128", "2026-08-17"),

("rtx-pro-6000-edition-platform-cost-driver",
 "SR650a V4|SR655 V3|SR665 V3|VX655 V3|VX665 V3", "proven",
 "The RTX PRO 6000 edition, not the CPU brand, drives GPU-box cost: Server Edition (600W passive) forces expensive plumbing, Max-Q (300W active) exists only on AMD 'for AI' platforms",
 "Two editions: RTX PRO 6000 Blackwell Server Edition (600W passive datacenter, CBK8) and Max-Q Workstation Edition 96GB (300W active dual-slot, CBU5). On the Intel SR650a V4 only the Server Edition is offered and it forces 600W cabled GPU risers (C9R5 / CATS), 24K Ultra fans (CC8X), a front GPU cage and 2x 2000W-class PSUs. "
 "The Max-Q part is offered only on the AMD 'for AI' models: SR655 V3 7D9ECTO3WW (single socket), SR665 V3 7D9ACTOBWW (dual socket) and VX655 / VX665 V3 (Lenovo Press lp2364). "
 "So a white-label 2-GPU box using Max-Q cards maps to SR655 V3 for AI, and the reason is the GPU edition (about 65 percent of the cost either way), not AMD versus Intel CPU price. "
 "SR635 V3 is 1U single socket and cannot fit two double-wide GPUs; SR655 V3 (2U single socket) is the match, SR665 V3 only if two CPUs are wanted. "
 "A 2-GPU build with real 96GB cards costs roughly double a build carrying only GPU-Ready codes, so a low first number usually means the GPUs are missing (see lenovo-cto-mtm-quick-map). "
 "On the AMD platforms neither edition was TCE-flagged in July 2026 (the SR650a V4 CHWT later proved BU1E, see sr650a-v4-chwt-cbk8-riser-cpu-gates). Integrators sell the same NVIDIA card below Lenovo list, so Lenovo rarely wins a GPU-dominated box on price: sell warranty, single-vendor support, KYD and integration. "
 "Right-size the rest: 128GB and a 16-core CPU are enough to feed two GPUs; VRAM is the spec that matters for on-prem LLM hosting. Redundant 1100W supplies beat a single 2500W unit.",
 "Lenovo Press lp2364; DCSC exports 2026-07-15", "2026-07-15"),

("amd-v3-supermicro-mapping-rules",
 "SR635 V3|SR645 V3|SR655 V3|SR665 V3|D4390|Supermicro", "proven",
 "Mapping a Supermicro AMD node to Lenovo AMD V3: platform map, SR635 V3 thermal cap, PSU right-sizing, NIC, boot and JBOD rules (proven on a 1U all-NVMe node and a multi-role fleet)",
 "PLATFORM MAP: 1U single-socket all-NVMe to SR635 V3 (7D9GCTO1WW); 2U single-socket to SR655 V3 (7D9ECTO1WW); 2U dual-socket to SR665 V3 (7D9ACTO1WW); 1U dual-socket to SR645 V3. "
 "THERMAL: an SR635 V3 with a 320W-or-higher CPU on air is limited to the 4x2.5in front-bay chassis; the 10-bay chassis needs closed-loop liquid for such CPUs. "
 "PSU: Supermicro ships oversized CRPS supplies (2000W); Lenovo V3 steps are 750W / 1100W (BNFH, BLKH) / 1800W (BPK9) / 2600W (BKTJ) and the 1U maximum is 1800W, so size to the real draw (about 600 to 750W in the worked case) with 2x 1100W Titanium 1+1 (BLKH); the default 750W Platinum is too tight for a 400W CPU with 768GB. "
 "NIC: ConnectX-4 Lx is end of life, current Lenovo 25GbE is ConnectX-6 Lx (BE4T OCP, BE4U PCIe); a ConnectX-6 Dx 100GbE QSFP56 2-port PCIe (B8PP) exists and is TCE. "
 "BOOT: no 480GB 7mm NVMe exists (960GB minimum), M.2 RAID and 7mm RAID are mutually exclusive, 7mm enablement errors until 'Rear 7mm Install Drive Type' is set, and a front U.3 NVMe drive appears only after the backplane is set to NVMe or AnyBay. "
 "JBOD: a 4U 60-bay dual-expander JBOD has no 60-bay Lenovo twin; quote the ThinkSystem D4390 populated with 60 NL-SAS drives (the D3284 84-bay with 60 populated was the earlier option) and a 440-16e external SAS HBA per server (two per server were quoted). D4390 has zero TCE parts. "
 "DDR5: a Supermicro Turin board may cap DIMMs at 6000 while Lenovo Turin DIMMs are 6400 and Genoa stays 4800. CPU: prefer the P-suffix part on single socket (see amd-v3-epyc-parts-that-do-not-exist-and-substitutions). "
 "MEMORY-HEAVY ROLES stay on AMD V3: Intel V4 cannot build 1,536GB balanced (8 channels per socket) while SR665 V3 keeps 24 DIMMs.",
 "DCSC exports and catalog 2026-06-26 to 2026-09-16", "2026-07-24"),

("supermicro-sys-521c-nr-is-single-socket",
 "SR650 V4|Supermicro SYS-521C-NR", "proven",
 "Supermicro SYS-521C-NR is single-socket (Socket E, 12x3.5in): a spec reading '2x Xeon Gold 6448H' on it is a different model or two servers; the Lenovo mapping and RAID math",
 "supermicro.com lists SYS-521C-NR as SINGLE-socket (Socket E LGA-4677, 16 DIMM slots / 8 channels, 12x 3.5in bays, 2x M.2, 2x 1200W Titanium). A spec of '2x Xeon Gold 6448H, 64C/128T' on that model is therefore either a different dual-socket model or 2 servers x 1 CPU: resolve it before sizing, because the Lenovo side changes by 2x and a customer's '2' may count servers, not sockets. "
 "Same spec: 9x 7.2K SAS = 54TB, a Broadcom 3916 16-port RAID card, 8x 10Gb SFP+ and a management suite. "
 "LENOVO MAP: SR650 V4 (7DGDCTO1WW); 2x 6530P 32C (or one CPU if the source is single-socket); 8x C0U9 32GB (4 of 8 channels per CPU, so add memory if bandwidth matters); RAID 940-8i plus SuperCap because every TCE controller on SR650 V4 is 8-port and the 16-port 940-16i is not TCE; "
 "5x C4DA 12TB on C46N instead of 9x 6TB (6TB SAS is not TCE); 8x SFP+ maps to 2x BN2T plus BNWM = 8x 10/25 SFP28 (no SFP+ card exists); 2x C0U3 2000W 230V-only unless the site is 115V; XCC3 Premier plus XClarity One Standard. "
 "RAID USABLE: RAID 5 ties at 48TB (9x6TB and 5x12TB); RAID 6 is 36TB against 42TB, so a sixth drive fixes it. Gaps to close on the first pass: no M.2 boot, no optics or DACs, 230V-only PSU.",
 "supermicro.com SYS-521C-NR specification read 2026-09-23; DCSC export 2026-09-23", "2026-09-23"),

("sr650-v3-v4-hpe-dl380-gen11-gen12-parity-mapping",
 "SR650 V3|SR650 V4|HPE DL380 Gen11|HPE DL380 Gen12", "proven",
 "HPE DL380 Gen11/Gen12 to SR650 V3/V4 parity map: CPU, boot (NS204i-u), RAID cache (MR416i-p), tri-mode, PSU and the cache talk track",
 "CPU exact match: Xeon Silver 4516Y+ 24C 185W single socket maps 1:1 on V3; Gold 5520+ 28C 205W maps to BYW7 on SR650 V3 (DCSC swapped the entry heatsink for the standard BPDR at 205W and the list price came out slightly UNDER the Silver 4516Y+ build) and to C5QT 6530P 32C or C659 6527P 24C on V4. "
 "MEMORY: 8x 64GB DDR5-5600 on V3, C0TQ 64GB 6400 on V4. BOOT: HPE NS204i-u hot-plug RAID 1 maps to 2x 480GB RI NVMe M.2 (CBSZ) plus RAID 540-8i boot enablement (BVL3) on V3, and to CCCZ B550p-2HS hot-swap plus 2x C286 plus C2ZC on V4; the CC7H B350i-2i kit is not hot-swap, so CCCZ is the parity pick. "
 "RAID: HPE MR416i-p 8GB cache maps to 940-16i 8GB flash (BDY4) on V3. On V4 the B8P0 16i internal was flagged TCE in a catalog snapshot but the live panel showed the TCE controller ceiling on 7DGD is B8NY 940-8i 4GB (other TCE options: 545-8i and VROC), so a TCE V4 build carries 4GB cache. "
 "'HPE 8SFF x1 TriMode U.3' maps to an AnyBay backplane plus tri-mode enablement (CH5Z on V4, BE38 on V3) at x1 per bay; on the Gold V4 build CH5Z landed at no charge. The 4-port 1GbE OCP is B5T1 Broadcom 5719 on both. "
 "PSU: V3 750W; V4 has no 750W, use 2x BWM3 800W 230V/115V Titanium (matches HPE Titanium) or C0U5 1300W (a 1300W pair drew about 753W worst case; 800W would sit near 94 percent). A 2000W C0U3 is 230V-only and broke a 115V wall-power site; reverting to C0U5 kept BU1E. "
 "DRIVES on V4 TCE: no 1.92TB Mixed Use drive is TCE on 7DGD (BYM5 is not); BYM6 3.84TB MU SATA, BYLT 1.92TB RI SATA and BYLU 3.84TB RI SATA are; SATA MU against HPE SAS MU is a price play at equal capacity and endurance. "
 "CACHE TALK TRACK: same Broadcom MegaRAID family as the MR416i-p; 8 versus 16 lanes and 4 versus 8GB cache are headroom a 5-drive SATA SSD array cannot use; power-loss protection is identical (flash-backed plus supercap); 8 lanes already cover all 8 wired bays and more than 8 drives needs a new backplane on any vendor. "
 "Odd spindle counts give no RAID 10 and less usable after parity. XCC licence lines can hide duplicates: see xclarity-one-scjd-scje-and-c3k9-double-entitlement. "
 "The V4 TCE build came in about 9 percent under the V3 exact-match at total price.",
 "Lenovo DCSC exports 2026-07-10; HPE quote", "2026-07-10"),

("cisco-c220-m7-and-b200-m5-to-lenovo-mapping",
 "SR630 V4|Cisco UCS C220 M7|Cisco UCS B200 M5|Nutanix", "proven",
 "Cisco to Lenovo mapping logic: C220 M7 (2x8C) to single-socket SR630 V4, B200 M5 blades to Nutanix compute-only SR630 V4 nodes, and the automated-mapper errors seen",
 "C220 M7 (2x Xeon Silver 4509Y 8C, 512GB, 12G SAS RAID 4GB plus 8x 1.9TB SATA 3 DWPD, VIC 15427 4x10/25/50G, 2x 1200W Titanium, SNTC 24x7x4, Intersight Essentials) maps to a SINGLE-socket SR630 V4: 2x8C = 16 cores becomes 1x 16C (C5RD 6515P, or C5R5 6724P for TCE), 8x C0TQ 64GB = 512GB at 1DPC, a 940-8i (B8NY, TCE) or the 940-16i adapter B8NZ (TCE; the internal B8P0 is not) on a 10-bay backplane, 8x 1.92TB RI SATA (BYLT, or CBVC SED); "
 "the Cisco 3 DWPD SATA equivalent is 1.92TB Mixed Use BYM5, which is NOT TCE; VIC maps to BN2T plus BK1H; SNTC to Premier 24x7 4hr; Intersight to XClarity One Standard plus XCC3 Premier (SCY0). "
 "Open questions: FI-attached IMM-managed servers cannot plug into a non-Cisco fabric, and the workload decides 1 versus 2 sockets. "
 "MAPPER ERRORS: 2x C5R7 8C in place of 1x 16C (about 7.6x the CPU cost), TCE-swapping drives UP to 3.84TB, pairing a 10-bay backplane (C21W) with an 8-port 940-8i (never seen in exports), claiming the platform needs a boot device, and omitting the AUNP SuperCap and management. "
 "B200 M5 BLADES (2x Gold 6242 16C Cascade Lake 2.8GHz, 512GB, no local storage, 2 clusters of 5) become 3 SR630 V4 compute-only nodes per cluster (see sr630v4-nutanix-compute-only-node-ck17): 1U because there are no drives. "
 "Keep core parity across the pair by splitting CPUs, for example 32C for production (192 cores) and 24C for DR (144 cores) = 336 against 320, better than 288 or 384; flag that a DR cluster smaller than production runs short at failover. "
 "Per-node memory steps are 512 or 1024GB on 8-channel Xeon 6, so 3 nodes x 1024GB = 3072GB fits a 2560GB need better than 4 nodes at 2048GB (short) or 4096GB (60 percent over). Memory was about 85 percent of hardware cost. "
 "Cascade Lake blades are end of sale since 2023.",
 "Cisco vendor quote; DCSC exports 2026-08-14 and 2026-09-23", "2026-09-23"),

("sr645-v3-dell-r6625-parity-build",
 "SR645 V3|7D9CCTO1WW|Dell PowerEdge R6625", "proven",
 "Dell R6625 (1U 2S AMD) to SR645 V3 parity build: exact-match lines, the four real substitutions, rails with CMA, forced 2-drive M.2 and the Genoa versus Turin upsell",
 "SR645 V3 (7D9CCTO1WW, the only 1U two-socket AMD ThinkSystem) had 7 BU1E configs with zero criticals. EXACT-MATCH lines: BREC EPYC 9334 32C 2.7GHz x2 = 64 cores; CBNC 32GB 6400 2Rx8 x8 = 256GB; BRG7 2.4TB 10K SAS 512e; BYLS 960GB RI SATA; CBSZ 480GB M.2; BPKR TPM; BH9M performance fans (8 for dual socket, single socket uses 6 plus dummies); 7Q01CTS4WW Premier 24x7 4hr. "
 "FOUR SUBSTITUTIONS: Dell 5720 dual 1GbE LOM to AUZV Broadcom 5719 QUAD 1GbE PCIe (SR645 V3 has no LOM, so it eats a slot; risers BLKB plus BLK9 give 2 LP slots, both consumed, BVHN riser 2 adds headroom); Dell 1100W Titanium to BNFH 1100W 230V/115V Platinum or BLKH 1100W Titanium (230V-only); "
 "PERC H355 (RAID 0/1/10) to BM51 440-8i HBA (no RAID at all; B8NY 940-8i adds RAID 5/6 for a modest premium); storage BU1W 10x2.5 backplane plus BM51 (a proven pair: 8 drives fill 6 SAS/SATA plus 2 AnyBay bays, the 2 NVMe-only bays take AVEN fillers). "
 "RAILS: Dell quotes rails plus CMA, so pick C4TM Toolless Stab-in Slide Rail V3 with 1U CMA rather than bare B8LA (B8LC is the alternative). "
 "BOOT: both TCE M.2 kits are 2-bay and DCSC rejects a single M.2, so 2x CBSZ is forced and the mirror is built in UEFI (no factory array); that is stronger than a single-drive BOSS-N1. "
 "GENOA VERSUS TURIN: Dell's 'EPYC 9334 with 6400 MT/s RDIMMs' clocks down to 4800 because Genoa caps there; upsell C2AQ EPYC 9335 32C 210W 3.0GHz (Turin, 6400, +11 percent clock, same cores and TDP, needs Turin board C2BD plus RoT C257 which DCSC selects automatically) and it was proven in 3 BU1E configs where BREC was catalogue-only. "
 "BALANCE: 8 DIMMs on two EPYC sockets is 4 of 12 channels per socket, a third of platform bandwidth despite a 'Performance Optimized' label; 12x 32GB is the next step; CC0A 16GB is not TCE, so 16x16GB is no fast-ship path. "
 "POWER at 115V measured about 740W nominal and 930W worst case (6.6A and 8.2A), fine on a 15A wall plug. Six core lines (BREC, CBNC, BRG7, BYLS, C4GB, AUZV) were catalogue-badge-only before the build validated: confirm BU1E in the panel before quoting 21 days.",
 "Dell quote; DCSC export 2026-09-03", "2026-09-03"),

("entry-tower-st45-st50-st250-v3-ceilings",
 "ST45 V3|ST50 V3|ST250 V3|SR250 V3", "proven",
 "Entry tower ceilings: ST50 V3 and ST250 V3 top out at 8 cores, ST45 V3 at 16 (no XCC); no tower offers more than 8C plus remote management plus more than 128GB; ST45 V3 64GB breaks TCE",
 "CORE CEILINGS: ST50 V3 8C (Xeon 6300 or E-2400, lp1907 p4); ST250 V3 8C (lp1803 p12; only C520 6325P 4C and C524 6353P 8C exist, no 16C); ST45 V3 16C (EPYC 4005, lp1994 p17). The cheapest tower has the MOST cores. "
 "No Lenovo tower offers more than 8 cores AND remote management AND more than 128GB: that combination exists only in rack. ST45 V3 has no XCC; ST50 V3 and ST250 V3 have XCC2. "
 "MEMORY: ST250 V3 has 4 UDIMM slots and a 128GB ceiling (C528 32GB is the largest, C527 16GB the TCE part); ST50 V3 has 4 UDIMM slots, so 4x C527 16GB keeps TCE at 64GB and 128GB is reachable later; ST45 V3 has only 2 UDIMM slots and lp1994 Table 16 marks C1G7 16GB TCE and C1G6 32GB NOT TCE with both DIMMs required to match, so the 64GB step (2x32GB) breaks TCE and 64GB is the permanent ceiling. "
 "TYPICAL ALL-SSD quotes on these towers used onboard software RAID (no hardware controller), one fixed 500W non-redundant PSU, no hot-swap, and 5977 (no array configured: the mirror is built at OS install). "
 "ST250 V3: 3.5in = 4 bays (BZB8 plus B41D), 2.5in = 8 bays (BZB9 plus B41E), M.2 is CABU 480GB SATA only (the NVMe CBSZ never appeared on this MTM), hot-swap redundant 800W PSUs (BWM3). "
 "SIZING: 32GB less about 4GB of host runs three 8GB VMs, not four. ST45 V3 as configured IS TCE (BU1E) but its 64GB upgrade is not.",
 "Lenovo Press lp1907 lp1803 lp1994; DCSC exports 2026-08 to 2026-09-18", "2026-09-18"),

("hpe-config-export-quantity-column-is-total",
 "ALL|HPE DL360 Gen12|HPE DL380 Gen12", "proven",
 "HPE configuration exports show the TOTAL quantity across all servers in the qty column; read the support line's 'Support For' attribute for the server count",
 "An HPE export for a 10-server order listed chassis 10, CPU 20, DIMM 160 and PSU 20: the qty column is the total across servers, not per server, and the per-line quantities look exactly like a x10 scaling factor. "
 "The tell is the support line's 'Support For' attribute, which lists the covered chassis part with the server count in parentheses; read it before deciding node count on any HPE CSV export. "
 "Cross-check: CPUs per chassis times chassis must equal the CPU line. The reverse trap exists on DCSC xlsx exports (see dcsc-xlsx-hides-config-group-qty). "
 "Also check licence lines against node count: a vGPU (vPC) licence count that works out to a handful of concurrent users per 24GB L4 is far below what the card carries, so either the licence count or the node count is not the fixed number; ask which. "
 "Exact-silicon matches on that DL360 Gen12 order were CPU C5R5 (6724P), memory C0TQ, GPU BS2C and NIC BN2T.",
 "HPE configuration export 2026-09-22", "2026-09-22"),

("sr645-v3-rear-drive-riser-forces-performance-thermal-kit",
 "SR645 V3|7D9CCTO1WW", "flagged",
 "SR645 V3 1U: the rear-drive riser forces the performance heatsink plus 8 performance fans, which DCSC rejects with a 4x3.5in all-HDD front; the fix and a caveat against the thermal table",
 "OBSERVED Critical: 'If 4x All HDDs is selected, selection of 8x ThinkSystem V3 1U Performance Fan Option Kit v2 [BH9M] is not valid.' The fan quantity and heatsink were LOCKED because they are system-rule consequences of the rear drive path: riser BLKE ('1U x16 Riser1 PCIe Gen4 with Rear drive') enables the rear bay, BDY6 (1U 2x2.5in NVMe rear backplane) sits in it, BCGY (1U rear 2x2.5in HDD cage) is auto-added, and rear drives block the 1U exhaust path so DCSC mandates BQ26 Performance Heatsink (Neptune Air) plus 8x BH9M. "
 "That fan kit is then refused alongside a 4x3.5in all-HDD front, so on the 1U SR645 V3 a 4x3.5in all-HDD front and the rear drive bay are mutually exclusive. "
 "FIX: delete BDY6 (Storage tab) and swap BLKE (PCI tab) for a riser without rear-drive support (BLK7, BLKB or BP39, all TCE), which cascades the cage and fans away; that also loses the NVMe tier, so a mixed 3.5in HDD plus NVMe node belongs on 2U (SR650 V4 with the C46N backplane). "
 "CAVEAT: the SR645 V3 thermal table (pubs.lenovo.com thermal_rules, see sr645-v3-4x3-5in-thermal-table) says TDP band and ambient, not drive configuration, drive heatsink selection and that every 4x3.5in row starts at 200W; the two observations may be complementary (the rear path forces the performance kit, and the 4x3.5in rows accept it only in the 200W-and-up bands). Re-test before quoting a 1U with a rear cage. "
 "Related auto-swaps: a 205W CPU on SR650 V3 moved from the entry to the standard BPDR heatsink; a 210W CPU on SR650 V4 adds the performance heatsink and fans; a passively cooled GPU on SR630 V4 forces C1YT performance fans.",
 "DCSC Critical message and exports 2026-08-20 and 2026-07-10", "2026-08-20"),

("xeon6-16c-tce-panel-churn-2026-09-30",
 "SR630 V4|SR650 V4|Xeon 6 16C", "flagged",
 "Xeon 6 16-core TCE eligibility moved within weeks (Aug to Sep 2026) and a live panel on 2026-09-30 no longer offered 6724P as TCE; exports and guides lag the panel",
 "C5QV 6517P and C5RD 6515P carried BU1E in exports through August; on live panels dated 2026-09-23 the 6517P was not offered in TCE and C5R5 6724P was the only TCE 16C on SR630 V4 (see sr630-v4-tce-cpu-live-panel); on 2026-09-30 a live panel reported that the Intel 6724P 16C no longer fits TCE, and a host design was moved to AMD (SR635 V3 with a 16C EPYC) to keep the TCE lead time. The platform behind the 09-30 reading was not recorded. "
 "Exports lag the panel by days and product-guide TCE columns lag by more, so a CPU swap 'saving' or a TCE claim taken from an export or a guide is only a lead. Never offer a CPU change as TCE-safe without opening the live panel the same day, and say what the fallback is (AMD V3 or a non-TCE order) in the same message.",
 "DCSC live panels 2026-09-23 and 2026-09-30", "2026-09-30"),

("tce-label-vs-bu1e-mismatch-cases",
 "ALL|SR650 V4|SR645 V3|HX650 V4", "proven",
 "A file name, quote label or customer statement saying 'TCE' proves nothing; only BU1E in the export does. Four cases where the label was wrong",
 "(1) A hardware-RAID NVMe build on SR650 V4 exported with 'TCE' in the file name and NO BU1E (the U.3 drives were the breaker). "
 "(2) A multi-role-group HX650 V4 quote labelled TCE did not match the TCE DCSC export: it carried the non-TCE 24C control-plane CPU, 3.2TB mixed-use worker drives and 4x 1.92TB drives with only the DIMMs swapped to 32GB, so whether it earns BU1E is unconfirmed. Compare quote lines to the export part for part across every role group before labelling. "
 "(3) In a six-config bid batch none of the exported configs carried BU1E although the thread assumed a TCE revision existed; one file believed to be the TCE revision of a compute node was a different storage-server variant. "
 "(4) A statement that 'no TCE AMD builds exist' was written to a partner; an SR645 V3 with EPYC 9124 carried BU1E. TCE eligibility is per part per model, not per CPU architecture, so never say never without a panel check. "
 "Habit: open the export, search for BU1E, and check the Critical count; a clean Message History does not prove the RAID layout fits either.",
 "DCSC exports 2026-08-14 to 2026-09-24", "2026-09-14"),

("st250-v3-live-panel-memory-and-term-sample-bias",
 "ST250 V3|7DCECTO1WW", "flagged",
 "ST250 V3 live panel 2026-08-20: TCE memory offered only as 16GB C527 (so 64GB fills all 4 slots), although exports show C528 32GB; and '36 months only' was sample bias, 60-month Premier exists",
 "On a live ST250 V3 build the DCSC memory panel offered only the 16GB C527 under TCE even though C528 32GB appears in six ST250 V3 exports at quantity 4, some TCE; something in that build gated it. Consequence: 64GB uses all four slots and there is zero headroom. "
 "The same shape as the SR250 V3 finding on the neighbouring platform, now seen on ST250 V3 too: exports are a shortlist for the MTM, the live panel is the authority, and 'TCE-proven' means proven in SOME configuration, not offered in every build. "
 "Support term: earlier exports were all 36 months, which was wrongly read as a ceiling; 60-month Premier NBD and KYD were selectable on ST250 V3 (7Q01CTS2WW, 7Q01CTSAWW), XClarity One SCJE 5-year was selectable, and Premier NBD is selectable (Standard NBD is 7Q01CTS1WW, Premier 24x7 4hr is 7Q01CTS4WW). "
 "Windows on ST250 V3: SDA9 plus 2x SDDX (20 CALs) held BU1E. A ST250 V3 quote against an ST650 V3 or a 16C competitor box needs the scope-gap list ready: hardware RAID (B8NY 940-8i plus AUNP plus B9XE and BA12), a second BWM3 PSU (BWJN is the single-PSU filler), Windows, XClarity One and term.",
 "Live DCSC panel 2026-08-20; DCSC exports", "2026-08-20"),

("dcsc-supply-outlook-and-forced-vs-optional-tce-changes",
 "SR650 V4|SR630 V3|HX630 V4", "flagged",
 "DCSC exports carry per-part supply outlook messages; a competitor or customer config can be unbuildable ('outlook more than 12 months'), and how to split forced from optional changes when converting to TCE",
 "A customer-supplied SR650 V4 export carried the C5QQ 6505P flagged 'outlook more than 12 months, please select alternative' (2026-08-24), while the SR630 V3 alternative was about 5 months; only the TCE build had a committed date, which was the whole pitch. Outlook rotates, so re-check at quote time. Supply status Green or Gray is not TCE and outlook is not TCE either. "
 "FORCED by TCE (each verified): C5QQ 12C to C5RD 16C; the 440-16i HBA to a 940-8i plus SuperCap (no HBA is TCE on 7DGD); the C3RW 12-bay backplane to C46N (8 SAS plus 4 NVMe). "
 "OPTIONAL and revertible: the NIC split BCD4 plus BK1H (the BPPW 4-port OCP is TCE-proven, so reverting saves cost), XClarity One Starter to Standard, and 545-8i in place of 940-8i (a large saving, only valid if RAID 5 and 6 will never be needed). "
 "2x BYTJ 32GB equals one 64GB DIMM's capacity, is TCE and populates two channels instead of one for about the same price on V4. "
 "READ THE QUANTITY: an export line of 4x 20TB per server is 80TB PER SERVER, so N servers is N x 80TB and not 80TB; a belief of '80TB total' would have left most of the drives unnecessary, so confirm per-server against fleet before building.",
 "DCSC export supply messages 2026-08-24; DCSC exports 2026-09-10", "2026-09-10"),

("high-capacity-nvme-30tb-options-retimers-and-fill-economics",
 "SR635 V3|SR655 V3|SR665 V3|SR650 V4|Gen5 NVMe", "proven",
 "30.72TB drive options and TCE, the 7.68TB U.2 TCE ceiling, Gen5 retimers that must stay 1:1 with backplanes, and fill-the-bays economics",
 "30.72TB options (AMD V3, Aug 2026): only CABW SAS is TCE; NVMe choices were C8DK BM1743 U.2 Gen5 (QLC, about 1 DWPD, constrained supply, later replaced), BZC1 U.3 Gen4 (constrained) and CA3Q PM9D3a Gen5 (green supply, about 1.18x the price of C8DK; CABW about 1.16x C8DK). "
 "No 1.5 or 2 DWPD option exists at 30.72TB, 7.68TB parts are mostly RI about 1 DWPD, and 2 DWPD or more exists only at 6.4TB MU. "
 "TCE CEILING: the largest U.2 NVMe carrying BU1E is 7.68TB (C0ZU 3.84TB and C0ZT 7.68TB proven; the 15.36TB ThinkSystem U.2 CGP6 is not TCE, confirmed in DCSC 2026-08-17), which forces more drives, more nodes or less capacity on any all-flash TCE build; TCE at 7.68TB is about 1.18x worse per TB than 30.72TB. "
 "ECONOMICS (worked, one part untested): to reach about 215TB raw, splitting to 2 nodes of 14x 7.68TB cost about 18 percent MORE than the original single node (the second node duplicates CPU, memory, NICs, chassis and power), while ONE node filled to all 24 bays with 7.68TB (184TB raw, 14 percent under) was estimated about 10 percent BELOW the original and stays a single box. "
 "RETIMERS: a BLKY PCIe Gen5 NVMe retimer per Gen5 backplane must stay 1:1 (3 backplanes, 3 retimers); a retimer keeps Gen5 signalling inside its loss budget and a shortfall drops drives to Gen4 or leaves them unenumerated. "
 "The SR655 V3 24-bay chassis takes 3x BS7Y 8-bay Gen5 backplanes.",
 "DCSC exports and panels 2026-08-13 to 2026-08-17", "2026-08-17"),

("dimm-channel-population-mistakes-and-node-count-steps",
 "SR630 V4|SR650 V4|HX650 V4|SR635 V3|SR645 V3|Xeon 6|EPYC 9004|EPYC 9005", "proven",
 "DIMM channel population: Xeon 6 has 8 channels per socket, EPYC 12; common under-populations, 2x32GB versus 1x64GB, and how balanced steps drive node count",
 "Xeon 6 = 8 memory channels per socket, EPYC 9004/9005 = 12; balanced means every channel populated equally. "
 "MISTAKES SEEN: one 64GB DIMM per node on a single-socket Xeon 6 (1 of 8 channels, plus 15 fillers) on a box built to stream from 12 HDDs; 8 DIMMs on a DUAL-socket Xeon 6 (4 of 8 channels per socket, half the bandwidth: use 16x 32GB for the same 512GB); "
 "8 DIMMs on a dual-socket EPYC (4 of 12 channels per socket, a third of bandwidth; the next step used was 12x 32GB); a single 64GB DIMM on an 8-channel CPU where 2x BYTJ 32GB gives the same capacity, is TCE and about the same price on V4 (on AMD V3 2x 32GB listed near 60 percent of one 64GB). "
 "NODE COUNT FOLLOWS MEMORY STEPS: balanced dual-socket Xeon 6 offers 512GB (16x32GB) or 1024GB (16x64GB) per node and nothing between, so N nodes give cluster memory in coarse steps; for a 2.5TB need, 3 nodes at 1TB (3TB) beat 4 nodes at 512GB (2TB, short) or 1TB (4TB, 60 percent over). "
 "A memory-heavy node on 128GB DIMMs cannot be rebuilt on V4 (no 128GB RDIMM exists there, and 2DPC derates the bus to about 5200 MT/s). "
 "When a line count looks wrong, count DIMMs per socket first: the upside of fixing it is bandwidth, and it is usually cost-neutral.",
 "DCSC exports 2026-07-28 to 2026-09-23", "2026-08-14"),

("dimm-pricing-and-memory-share-of-bom",
 "ALL|SR630 V4|SR250 V3|SR635 V3|AMD V3", "proven",
 "Memory is the dominant BOM line (40 to 85 percent of hardware) and prices step fast: about 1.6 to 1.8x between 2026-08-10 and 08-13 on AMD V3 64GB DIMMs; CPU is rarely the lever",
 "SHARE OF HARDWARE PRICE (2026): 41 percent on a fixed 512GB inference server, 56 percent on a roughly 100-node AMD V3 bid (nearly 1,000 64GB DIMMs on one line = 43 percent of the bid, CPU only 7.6 percent), about 59 percent on an SR250 V3 with 4x16GB, 62 percent on an SR630 V4 with 16x32GB, 71 to 78 percent on SR635 V3 hosts at 256GB, and 85 percent on an SR630 V4 with 16x64GB. "
 "Cutting CPU specification and adding nodes therefore LOSES money, because every added node multiplies the memory line. "
 "STEP CHANGES: between 2026-08-10 and 2026-08-13 AMD V3 64GB DIMM list prices rose about 1.83x (CBND 6400), 1.57x (BQ3D 4800) and 1.65x (CBFR 6400); stored export prices for memory and NVMe went stale within days (July drive prices ran about 30 percent low by late September). "
 "A whole bid figure built on a stale memory price is not quotable: re-price DIMMs from a live export. "
 "LEVER ORDER when a build is over budget: memory first, then drives, then CPU; use an in-place capacity cut (128GB to 64GB, 32GB to 16GB where TCE allows) before touching the CPU. See export-price-aggregation-and-scraped-price-traps.",
 "DCSC exports 2026-08-10 to 2026-09-23", "2026-09-02"),

("sr650-v3-sds-backplane-expander-and-controller-lanes",
 "SR650 V3|7D76CTO1WW|vSAN|third-party SDS", "proven",
 "SR650 V3 12x3.5in software-defined-storage nodes: use a NON-expander backplane; a 540-8i forces the expander, a 540-16i does not; the post-2026-06-30 12-bay option fails clustered SDS",
 "An expander backplane has a FIXED SAS address that collides across nodes and fails a clustered SDS (DCSC warns 'VMware vSAN cluster will fail'; behaviour on other SDS was unconfirmed), so use a NON-expander backplane. "
 "LANE TRAP: a 540-8i (8 lanes) cannot direct-attach 12 bays and forces the EXPANDER backplane; a 540-16i (16 lanes) direct-attaches all 12 bays with the non-expander backplane and listed slightly cheaper in total than 8i plus expander. "
 "A 440-16i HBA is the clean JBOD choice but was not exposed in one CTO, so a 540-16i in JBOD or pass-through was the accepted fallback. "
 "After 2026-06-30 the only 12-bay 3.5in option on SR650 V3 became the Rear-4-Bay-Expander backplane, which Lenovo says fails clustered SDS. The fast path was an 8x3.5in AnyBay or non-expander backplane (8 lanes direct-attach 8 bays) with fewer, larger drives: 6x 24TB plus 2x 3.84TB SSD (144TB) in 8 bays instead of 9x 16TB plus 2 SSD in 12. "
 "Disclose the trade: about a third fewer spindles, a bigger rebuild domain and less growth room. "
 "DRIVES: 2.5in SSDs in a 3.5in backplane need 3.5-to-2.5 trays, while 3.5in SATA SSD parts include the carrier; pick Mixed Use over Read Intensive for SDS write cache (a 3.84TB part visible by default was RI; Mixed Use appears under 'Show all'); encryption None (DCSC notes it is unsupported with vSAN). "
 "Third-party HCI software stays licensed by its vendor outside DCSC (Software Preload = None); confirm the platform and controller on that vendor's HCL.",
 "DCSC builds 2026-06-24; DCSC messages", "2026-06-24"),

("dcsc-jbod-workflow-litmus-and-orphan-controllers",
 "SR650 V3|SR650 V4|SR630 V4|DCSC", "proven",
 "DCSC JBOD workflow: RAID Type and Controllers tabs decide, the 540-16i is RAID-or-JBOD only so boot RAID on it kills JBOD data drives, and orphan controllers to strip from all-NVMe builds",
 "On SR650 V3 (June 2026) data drives are added on the RAID Configuration sub-tab while any RAID array exists; the Internal Storage sub-tab only holds encryption enablement and the SD flash card until the arrays are deleted, then it unlocks and takes JBOD drives. "
 "The gates are the RAID Type sub-tab (HW RAID / SW RAID / Non-RAID) and Controllers sub-tab; for SDS choose Non-RAID and an HBA or JBOD-capable controller. LITMUS TEST: if DCSC makes you pick a RAID level for the data drives, RAID Type or controller is still RAID. "
 "A 540-16i is RAID-OR-JBOD only and cannot mix: a boot mirror that rides the same controller (front-bay mirror or 7mm rear mirror) flips it into RAID mode and kills the JBOD data drives; only an M.2 boot kit with its own RAID engine avoids the conflict. "
 "BUILD ONE NODE and set the system quantity: every per-node selection times the quantity must reconcile to the source BOM (4 DIMMs x 7 = 28, 5 HDD x 7 = 35, 4 optics x 7 = 28). "
 "WRITE 'Controller: NONE' in the build sheet whenever a build has no RAID card, since leaving it implicit reads as a missing line. "
 "ORPHAN CONTROLLERS on all-NVMe builds do nothing and cost real money: a 940-8i plus SuperCap plus cable (about 4 percent of a GPU node), BM50 SAS HBAs left on two all-NVMe roles, an orphan 545-8i after the backplane became C46P NVMe. Removing them is usually a backplane swap (AnyBay C3RU to NVMe-only C46P) and cascades the cable and supercap away.",
 "DCSC builds 2026-06-24 to 2026-09-24", "2026-06-24"),

("m2-and-7mm-boot-kit-feature-code-map",
 "SR650 V3|SR635 V3|SR645 V3|SR250 V3|SR650 V4|SR630 V4", "proven",
 "M.2 and 7mm boot kit feature codes, which kits have their own RAID engine, which need VROC, the array lines they pull in, and cable-kit behaviour",
 "BM8X = non-RAID 2-bay M.2 enablement (on SR250 V3 it mounts on the BMTU dummy PCIe card with the BWN1 VROC M.2 signal cable, costing one LP slot). "
 "B8P9 = M.2 NVMe 2-Bay RAID Adapter (4Y37A09750): the adapter has NO RAID chip; on Intel it needs VROC (BZ4X RAID1-only) and DCSC then shows 'M.2 NVMe Array 1 RAID 1' (BS7F); with B8P9 and no VROC the 'Configured M.2/7mm RAID' choice is greyed out. "
 "BYFF = B540i-2i (4Y37A90063): its own Marvell RAID chip for SATA M.2 (2x CABU 480GB), the mirror is built in adapter UEFI at deployment, so BS7A stays greyed or None and that is correct. "
 "BYFG = 7mm SATA/NVMe 2-bay rear hot-swap RAID enablement kit (4Y37A90062), array line BS9S '7mm SATA Array 1 RAID 1'; BS7A is the M.2 path and conflicts with the 7mm cage ('BS7A not valid'); BT7P is the RAID 540-8i used for 7mm boot on SR635 V3. B5XJ and BM8X are non-RAID carriers, so an 'M.2 mirror' on them is not real. "
 "SR250 V3 mirrored pair: 5978 plus BS7Q plus BS7C. V4 Intel: CCCZ B550p-2HS carries its own controller (5977, no VROC). "
 "SR650 V3 cable kits are adapter-specific (B8P9 4X97A82925; BM8X non-RAID 4X97A82924) and are AUTO-BUNDLED in CTO mode; 'order the cable separately' is a pre-configured-mode caveat, so confirm by validating with no missing-cable error. "
 "Swapping the M.2 adapter RESETS the array selection: re-confirm RAID 1. "
 "VROC RAID1-only (BZ4X) is a one-time key, not a subscription (ESXi 7.0U3d and 8.x inbox driver, UEFI). "
 "SR645 V3: both TCE M.2 kits are 2-bay and DCSC rejects quantity 1, so two drives are forced and the mirror is built in UEFI. "
 "CONFLICT TO RE-TEST: on SR650 V4 (2026-07-14) swapping to the B550i-2i kit still forced a VROC feature code when the M.2 drives were NVMe (the kit's onboard RAID looked SATA-only in the rules), while September exports show CCCZ builds with 5977 and no VROC; if DCSC forces VROC on a B550i build, try CCCZ.",
 "DCSC builds and exports 2026-06-24 to 2026-09-28", "2026-07-14"),

("raid-usable-capacity-hdd-to-ssd-swap-method",
 "SR630 V4|SR650 V4|SR645 V3|940-8i|545-8i", "proven",
 "RAID usable arithmetic for HDD-to-SSD and drive-size swaps: RAID 5 (n-1), RAID 6 (n-2), 24Gb SAS on 12Gb controllers, and why 'drop-in' is the honest argument against NVMe",
 "RAID 5 usable = (n-1) x drive; RAID 6 = (n-2) x drive. 5x 2.4TB RAID 5 = 9.6TB = 4x 3.2TB RAID 5 (identical usable, one fewer failure point, one bay freed); 9x 6TB and 5x 12TB RAID 5 tie at 48TB while RAID 6 gives 42TB against 36TB (a sixth 12TB drive closes it). "
 "No 2.4TB SSD exists; the nearest is 3.2TB Mixed Use (CABQ, 3 DWPD) and Mixed Use is the right endurance for SQL writes against Read Intensive at 1 DWPD. "
 "The 940-8i is a 12Gb SAS controller and the 545-8i also runs 12Gb, so 24Gb SAS drives (CABQ, CABR) negotiate down: do not sell interface speed. An 8x2.5in SAS/SATA backplane cannot take NVMe (it needs AnyBay), so 'drop-in' is the honest reason against NVMe, not price. "
 "Odd spindle counts give no RAID 10 and less usable after parity. Verify the TCE lead time of the swapped drive live before promising a ship date.",
 "DCSC exports 2026-08-11 and 2026-09-23", "2026-09-23"),

("dm3010h-licence-and-service-scale-with-capacity",
 "DM3010H|7DCVCTO1WW|NetApp FAS", "proven",
 "DM3010H unified licence (SBW7 per 0.1TB) and Premier service scale with raw capacity: re-price on every pack change; a diskless server head next to a DM is unnecessary",
 "The DM3010H unified software licence is capacity-based: SBW7 'NLSAS Unified Complete SW License, Per 0.1TB', quantity = raw TB x 10 (1200 for 120TB raw, 1920 for 192TB, 2640 for 264TB). Every pack change must re-price SBW7: going from 120TB to 192TB raw added about 18 percent of the original array price in licence alone, on top of drives. "
 "Premier service also scales with capacity (about 1.9x when raw went from 120TB to 264TB). The CTO unit price already bundles the licence and services, so summing the service lines separately double-counts (about 1.3x). "
 "USABLE is about 60 percent of raw for planning (120TB raw about 72TB usable, 192TB about 109 to 123TB, 264TB about 158TB depending on RAID-DP versus RAID-TEC and snapshot reserve): a 40x4TB FAS replacement (160TB raw, about 96TB usable) is not matched by 120TB raw. "
 "Packs seen: 6x10TB (60TB), 6x22TB (132TB), 6x24TB (144TB); whether a 6x16TB (96TB) pack exists or is TCE is UNVERIFIED, and on a 12-bay base the usable steps skip the 100 to 120TB band (or use 12x10TB plus a DM120S). "
 "The DM3010H is a complete dual-controller array and needs no server head: a design with a diskless SR655 head plus a DM can delete the head. Hardware seen: 2x controllers BWTE 64GB, HIC BWTM (2-port 32Gb FC plus 2-port 25GbE; a quad-port 25GbE HIC doubles Ethernet if FC is not used), 2x B4CH 1TB NVMe cache, and one AV1W DAC per controller (no port redundancy). "
 "BU1E was present on the DM3010H build; see dm3010h-drives-sold-in-6-packs-dcsc-forces-qty-2 for pack ordering.",
 "DCSC exports 2026-08-13 to 2026-08-17", "2026-08-17"),

("de4200h-san-for-small-virtualization-clusters",
 "DE4200H|Proxmox VE|Hyper-V|iSCSI SAN", "flagged",
 "DE4200H iSCSI SAN as shared storage for a 2 to 3 host cluster: 2U12 HDD RAID 6 is cheapest but IOPS-limited, 2U24 SSD RAID 6 suits SQL; a 2-node HA cluster needs a quorum device",
 "For a 2 or 3 host design (Proxmox or Hyper-V) that replaces an older VMware pair and a roughly 20TB SAN: DE4200H 2U12 with 5x 24TB in RAID 6 is the cheapest capacity and carries an IOPS warning; "
 "DE4200H 2U24 with 13x 1.92TB SSD in RAID 6 (about 21TB usable) was the recommendation for a SQL-backed application. A 2-node HA cluster needs a third vote (a QDevice or witness). "
 "Where the customer supplies third-party switches and optics (SFP+ switch ports, their own DACs) no optics go on the Lenovo BOM: say so, and confirm the SFP28 NIC runs at 10G on the customer's transceivers (see sfp28-broadcom-57414-speed-open-questions). "
 "Hypervisor licence is nil and guest Windows is the cost: see hypervisor-is-free-guest-windows-is-the-cost. "
 "The design had not been exported from DCSC when recorded, so every part is unproven until built.",
 "DCSC panels 2026-09-30", "2026-09-30"),

("dcsc-partner-switch-catalog-and-in-rack-cabling",
 "NVIDIA Spectrum|Nokia SR Linux|DCSC partner switches|SFP28 DAC", "proven",
 "DCSC resells partner switches (NVIDIA, Nokia, Cornelis): InfiniBand is listed under the Ethernet header, SN2201 is 1GbE, and in-rack cabling should be DAC with an optic count that includes ISLs",
 "DCSC resells partner-brand switches: NVIDIA Networking (Spectrum Ethernet SN2201, SN3420, SN4700, SN5600, SN5610; Quantum QM9700 and QM9790), Nokia (7215, 7220 IXR-D2L and D3L) and Cornelis. "
 "TRAPS: QM9700 and QM9790 (0724HEB / HEC / HED / HEE) are NDR InfiniBand yet sit under the Ethernet header, and Cornelis Omni-Path is an HPC fabric; neither connects to Ethernet NICs. SN2201 is 48x1GbE RJ45 with only 4x25G uplinks and cannot carry 10/25G server links. "
 "The only 25G SFP28 top-of-rack options in the catalogue were NVIDIA SN3420 (48x 10/25G SFP28 plus 100G uplinks; managed model 7DSFCTOKWW) and Nokia 7220 IXR-D2L (48 SFP28 plus 8x100G plus 2 SFP+, SR Linux), both oversized for 6 to 14 used ports; NVIDIA's purpose-built 18-port HCI switch SN2010 was NOT in Lenovo's catalogue. "
 "The switch SKU is a fixed bundle ('no config', bare box): SN3420 includes 2 power cords, 3-year Premier 24x7, a rack kit and a Cat5e management cable but NO optics, and base supply shows Extended Lead Time, so flag lead time. Match the airflow variant (PSE or oPSE) to the server front-to-rear. "
 "Partner DC switches do not replicate campus NAC, 802.1X or portal security from a campus-security vendor; fine for a storage or data top of rack. "
 "CABLING: a port takes EITHER a transceiver OR a DAC/AOC, never both, and a DAC is the whole link, so it REPLACES the server-side transceivers. In-rack top of rack should be passive DAC (reliable to about 7m at 10G); use transceivers plus fibre only across racks or beyond that. "
 "The Lenovo 3m passive 25G SFP28 DAC (7Z57A03558) listed about 18 percent cheaper than the 10G SFP+ DAC (90Y9430) and is 25G-capable, so buy the SFP28 DAC even for a 10G design; 1m is 7Z57A03557; a 100G QSFP28 DAC covers a switch-pair ISL. "
 "Optic counts = server links plus inter-switch links (a BOM showing 32 and 16 was 28 and 12 server links plus about 4 ISL each). Use Lenovo-coded optics (a NIC flags third-party parts) and the BNDR Accelink 10G SR SFP+ is proven in SFP28 ports.",
 "DCSC catalog and builds 2026-06-24", "2026-06-24"),

("sfp28-broadcom-57414-speed-open-questions",
 "SR630 V4|SR650 V3|Broadcom 57414|Broadcom 57454|Broadcom 57504", "flagged",
 "Open points on SFP28 speed behaviour: a DCSC warning that dual-rate optics give no 10G on Broadcom 57414/57454, and unverified mixed-speed ports on one 57414 card",
 "(1) A DCSC message seen in June 2026 on an SR650 V3 build (paraphrased, exact wording not preserved) warned that dual-rate 10G/25G SFP28 optics do not give 10G with Broadcom 57414 or 57454 adapters; that build avoided dual-rate optics and used 10G SR SFP+ (BNDR) in the 57504 ports. "
 "This CONFLICTS with the documentary argument that BYBJ and BF10 (named 'Dual Rate 10G/25G') run at 10G in a 57414 port and with exports pairing dual-rate optics with the 57414 (see transceivers-and-dacs-verified). If a customer needs 10G on a 57414, prefer a 10G SR SFP+ optic or a DAC and re-read the live DCSC message. "
 "(2) Whether ONE 57414 can run port 0 at 10G and port 1 at 25G simultaneously is not stated in Lenovo docs: do not assert it. "
 "(3) A design that needs a card physically incapable of the other speed can only be met with 10GBASE-T cards (B5ST, AUKP), not SFP28 cards configured at 10G. "
 "(4) Mixed nodes are proven: B5ST or AUKP with BN2T or BK1H built clean in 18 exports (16 TCE-clean, 0 criticals), all Broadcom so no vendor-mixing question; the OCP copper card B5ST is about 10 percent cheaper than the PCIe AUKP and keeps the shared-management path on the data side (unverified). "
 "(5) Redundancy trade: with one card per speed a card loss removes that whole speed while two ports per card keep only port redundancy; state it once, it is the customer's call. "
 "(6) SR630 V4 with the rear M.2 cage has 2 OCP plus 2 PCIe = 4 adapters, so two cards per speed is possible (see sr630-v4-slot-budget).",
 "DCSC message June 2026; DCSC exports 2026-09-18", "2026-09-18"),

("sr650-v4-vsan-mtm-and-ready-node-compliance",
 "SR650 V4|SR650 V4 for vSAN|ThinkAgile VX|VMware vSAN", "proven",
 "ThinkSystem SR is a supported vSAN platform ('SR650 V4 for vSAN' MTMs exist); DCSC does not auto-validate vSAN compliance, so check the Broadcom Compatibility Guide; do not swap a rack-server match for VX",
 "Lenovo publishes dedicated MTMs 'SR650 V4 for vSAN' in 1-year and 3-year warranty variants (Lenovo Press lp2127), and a DCSC notice states that Lenovo vSAN Ready Nodes and vSAN Max Ready Nodes ARE ThinkSystem servers certified for VMware vSAN. "
 "So a request to 'convert to a ThinkAgile VX certified node before quoting' is not required. When a competitor quoted plain rack servers (PowerEdge, not VxRail) a VX answer breaks the like-for-like comparison (different price point and support model), and only the storage nodes touch vSAN; compute-only ESXi hosts do not. "
 "DCSC does NOT auto-validate vSAN compliance: check the vSAN nodes against the Broadcom Compatibility Guide as a certified Ready Node yourself. "
 "If the customer later wants HCI, quote VX for the storage tier as a SECOND option alongside the match, not a replacement, and note VX is not TCE. "
 "Build notes from a large VMware bid: 3x 7.68TB RI U.2 NVMe per node (against Dell E3.S, equivalent), 2x 960GB M.2 RAID 1 boot via B350i plus VROC RAID1-only (against Dell BOSS-N1; no recurring licence on either side), 2x Broadcom 57504 quad 25GbE (BPPW OCP plus BNWM PCIe), KYD on every node (Dell has no KYD equivalent). "
 "Compute nodes at 32x 64GB run 2 DIMMs per channel at about 5200 MT/s against 6400 and a 128GB RDIMM is offered only non-TCE, so disclose the speed. "
 "Power: one 1300W PSU at 230V held a worst case near 95 percent (passes with no headroom) while at 120V it derates to about 1000W and redundancy is lost, so confirm site voltage before choosing 1300W over 2000W.",
 "Lenovo Press lp2127; DCSC notice and exports 2026-07-14 to 2026-07-28", "2026-07-28"),

("xclarity-one-scjd-scje-and-c3k9-double-entitlement",
 "SR650 V3|SR650 V4|SR250 V3|ThinkAgile HX", "proven",
 "XClarity One and XCC licence codes: SCJD 3yr, SCJE 5yr, SCY0 XCC3 Premier, SBCV XCC2 Platinum, C3K9 'Platinum Upgrade v3', and a possible double entitlement",
 "SCJD = XClarity One Standard 3-year; SCJE = 5-year (about 1.65x the 3-year price for two more years, per endpoint); XClarity One Starter to Standard is a separate step. SCY0 = XCC3 Premier FOD (V4); SBCV = XCC2 Platinum FOD (V3 and ST50 V3); C3K9 = 'XClarity Platinum Upgrade v3'. "
 "POSSIBLE DOUBLE ENTITLEMENT (unverified): C3K9 together with the XCC3 Premier FOD (SCY0) may be the same entitlement twice; the same pattern existed on V3 as BRPJ plus SBCV. Ask the rep. "
 "TERM ALIGNMENT: a 5-year Premier with a 3-year XClarity One is a common miss; fix SCJD to SCJE. "
 "Generation map: V3 = XCC2, V4 = XCC3, ST45 V3 has no XCC. Remote KVM on a base XCC needs the paid FOD (SBCV or SCY0). "
 "On a customer-managed stack (a third-party HCI or SDDC vendor manages the cluster) XClarity One is optional: flag it as such rather than dropping it silently.",
 "DCSC exports 2026-06-24 to 2026-07-10", "2026-07-10"),

("small-virtualization-host-spindle-count-vm-heuristic",
 "SR630 V4|SR645 V3|ST45 V3|small virtualization host", "flagged",
 "One worked heuristic for a small VM host: VM count tracked SPINDLE COUNT, not AMD versus Intel; assumptions stated, and cloud-baseline traps",
 "ASSUMPTIONS (a model, not Lenovo data): about 25 sustained write IOPS per general-purpose VM and about 175 write IOPS per 10K SAS spindle in RAID 10 (writes land on half the drives). Under it, 4 drives in RAID 10 give about 350 write IOPS and about 14 VMs; 2 drives in RAID 1 give about 175 and about 7. "
 "On three storage-bound quotes the VM ceiling followed spindle count only: the Intel box had the HIGHER CPU ceiling (24C = 48 VMs against 16C = 32) and CPU never bound, so explain an IOPS gap as 'spindle count', never as 'the AMD build'. "
 "The CPU-versus-memory guess for a small host: 4 to 5 always-on 2 vCPU / 8GB endpoints fit a 4-core tower at 2:1, but 32GB less 4GB host memory runs three 8GB endpoints, not four or five. "
 "CLOUD BASELINE: a first-pass cloud figure was about 3.7x too high once real instance rates were used, and Windows guests add an on-prem licence that cloud rows bundle: pin the guest OS before quoting payback. "
 "A single node is a single failure domain with no HA and no backup target in the BOM: say so.",
 "DCSC exports 2026-09-18", "2026-09-18"),

]
