# Lenovo hard rules

These override any inference. Each one was proven against real DCSC exports or Lenovo Press, usually after an answer based on inference turned out wrong.

## Top Choice Express (TCE)

- TCE is proven by feature code **BU1E** present in a DCSC export. Nothing else proves it: not a product guide's TCE column, not a catalog crawl, not a filename that says "TCE".
- TCE is **all-or-nothing**. One non-TCE part drops BU1E for the entire bid.
- TCE membership is **per MTM, per date**, and it rotates. A part can be TCE on HX650 V4 and not on SR650 V4 in the same week. Product guides and older exports go stale; the live DCSC panel decides.
- TCE lists are **not monotonic by size**. They have floors as well as ceilings, so never infer that a smaller or larger variant is also eligible. Verified cases: the HX650 V4 CPU floor (8C C5R6 is TCE, 12C C5QQ is not), the 16GB DIMM floor (C0U2 breaks TCE), and the U.2 VA PCIe 5.0 capacity window of 3.2TB to 7.68TB.
- A rack chassis on the order voids TCE, as does any tied order that holds non-TCE product.
- TCE is 21 days from order to delivery.
- Customer-facing writing says "Top Choice Express (TCE)". Never "quick-ship".

## Storage

- U.3 NVMe SSDs have **zero** TCE configs. U.3 in a build blocks TCE.
- Tri-mode (`CH5Z` + `BE38`) is a **940-series RAID adapter** feature. Every 440-series HBA is SAS/SATA only. U.3 is required only when a controller sits in front of NVMe.
- SAS/SATA needs a controller (protocol translation). NVMe does not (it is PCIe native). A backplane that exposes SAS/SATA bays forces a controller in DCSC even if those bays are empty.
- Software-defined storage (S2D, vSAN, Nutanix, Ceph) needs raw drives. Hardware RAID breaks it.
- The RAID 545-8i has no RAID 5 or 6, and supports only 2 virtual drives.
- "Internal" means the CFF form factor; "Adapter" means a PCIe card. Controller ports must match the bay count.
- Write **TB, never TiB**. Convert (x 1.0995), do not relabel. Nutanix Sizer and DCSC `B6C2` both emit TiB.

## Reading exports

- The price column is **per unit**. "Total Part Price" is an uncached formula and reads back empty, so compute qty x unit yourself.
- The xlsx never shows the configuration-group quantity. Only the `.xml` in the export zip does (`<ConfigurationGroupLineItem><quantity>`). Read it before stating a server count or order total.
- In a KB built from exports, `qty` is total across all nodes. Divide by `config.nodes` for per-node.
- Supply status (Green/Gray) is NOT the same as TCE.
- Always check the currency.
- Never quote a DIMM or drive price from anything but a current export. Memory and NVMe prices moved 50-100% within weeks in 2026.
- A clean Message History and BU1E do not prove a RAID layout fits. DCSC does not check the array count when set to 5977 (no configured RAID).

## Answer discipline

- Never claim a part is TCE without a BU1E config proving it.
- Distinguish **absence of evidence** from **proof of prohibition**. "This never appears in 470 configs" is a flag, not a rule. Say which one you have.
- Distinguish what DCSC **built** from what Lenovo **supports**. An export KB answers only the first. Lenovo Press answers the second, and is often silent on field upgrades and configurator gating.
- Never state a Nutanix node-reduction number without the customer's own Collector or Sizer output.
- Model knowledge of Lenovo feature codes is unreliable and the catalogue rotates. Never answer a feature-code question from memory.
- If a Lenovo Press fetch does not return the section you need, say so. Do not paraphrase a passage you could not read.
