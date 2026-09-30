# Platform specs

16 platforms, paraphrased from their Lenovo Press product guides (the `source` id). Hardware limits only: sockets, DIMM slots and channels, drive bays, PCIe/OCP slots, PSU and GPU notes. Always confirm against the named guide.

```
ThinkSystem SR630 V3  (1U rack)  [lp1600, as of 2026-07]
  MTMs        7D73CTO1WW 7D73CTO3WW 7D73CTOBWW 7D74CTO1WW
  Mach types  7D73, 7D74
  Sockets     1-2
  CPU         4th Gen (Sapphire Rapids) or 5th Gen (Emerald Rapids) Intel Xeon Scalable
  Memory      32 slots (16/socket, 8ch x 2 DPC), up to 5600 MT/s
              5600 MT/s at 1 DPC with 5th Gen Xeon; 4800 MT/s at 2 DPC or with 4th Gen Xeon.
  Drives      front max 10x 2.5", 4x 3.5"
              - Up to 4x 3.5-inch, or 12x 2.5-inch (10 front + 2 rear), or 16x EDSFF hot-swap
              - 3.5-inch limited to 4 front bays (1U); rear bays are 2.5-inch only (2x SAS/SATA or 2x 7mm SATA)
  PCIe        up to 5 slots + 1 OCP  (3 rear (2x PCIe 5.0 + 1x PCIe 4.0) and 2 front; front riser only in specific front-bay configurations.)
  PSU         2 bays. Two hot-swap redundant supplies.
  https://lenovopress.lenovo.com/lp1600
```

```
ThinkSystem SR630 V4  (1U rack)  [lp1971, as of 2026-09]
  MTMs        7DG9CTO1WW 7DG9CTO2WW 7DK1CTO1WW 7DLMCTO1WW
  Mach types  7DG8 (1 year warranty), 7DG9 (3 year warranty), 7DK1 (3 year warranty, Neptune Core liquid cooled), 7DLM (3 year warranty, SAP HANA)
  Sockets     1-2
  CPU         Intel Xeon 6 6700P/6500P-series (Granite Rapids, P-core) or 6700E-series (Sierra Forest, E-core)
  Memory      32 slots (16/socket, 8ch x 2 DPC), up to 6400 MT/s, max 8TB with 32x 256GB 3DS RDIMM
              RDIMM 6400 MT/s at 1 DPC, 5200 at 2 DPC; MRDIMM up to 8000 MT/s at 1 DPC only.
  Drives      front max 10x 2.5", no 3.5" front bays
              - Front: 10x 2.5-inch NVMe, AnyBay, or SAS/SATA mixes; 8x 2.5-inch NVMe or SAS/SATA; 16x E3.S 1T; 8x E3.S 2T; 8x E3.S 1T + 4x E3.S 2T
              - Rear: 2x 2.5-inch NVMe or SAS/SATA (12x 2.5-inch total)
              - M.2: 2x front/rear hot-swap M.2 bays or internal M.2 module
              - Up to 12x NVMe drives, all direct-connected
              No 3.5-inch drive bays (change from SR630 V3).
  PCIe        up to 3 slots + 2 OCP  (All PCIe 5.0, all at the rear; 2 OCP 3.0 slots (x8 or x16).)
  PSU         2 bays. 80 PLUS Platinum/Titanium; 800W, 1300W, 2000W AC. All support 230V, some also 115V. HVDC and -48V DC options exist.
  GPU         Up to 3x single-wide (75W) GPUs
  https://lenovopress.lenovo.com/lp1971
```

```
ThinkSystem SR650 V3  (2U rack)  [lp1601, as of 2026-07]
  MTMs        7D76CTO1WW 7D76CTO3WW 7D76CTO5WW 7D76CTOEWW 7D76CTOFWW 7D77CTO1WW
  Mach types  7D76, 7D77
  Sockets     1-2
  CPU         4th Gen (Sapphire Rapids) or 5th Gen (Emerald Rapids) Intel Xeon Scalable
  Memory      32 slots (16/socket, 8ch x 2 DPC), up to 5600 MT/s, max 8TB with 32x 256GB 3DS RDIMM
              5600 MT/s at 1 DPC, 4800 MT/s at 2 DPC. TruDDR5 RDIMM, 9x4 RDIMM, 3DS RDIMM.
  Drives      front max 24x 2.5", 12x 3.5"
              - Front: 3.5-inch 8 or 12 bays; 2.5-inch 8, 16 or 24 bays
              - With middle and rear bays: up to 20x 3.5-inch or 40x 2.5-inch
              - Up to 36x NVMe with 1:1 PCIe lane connectivity
  PCIe        up to 12 slots + 1 OCP  (10 rear + 2 front full-height half-length, plus a dedicated OCP 3.0 slot.)
  PSU         2 bays. Two hot-swap redundant supplies.
  https://lenovopress.lenovo.com/lp1601
```

```
ThinkSystem SR650 V4  (2U rack)  [lp2127, as of 2026-09]
  MTMs        7DGDCTO1WW 7DGDCTO3WW 7DLNCTO1WW
  Mach types  7DGC (1 year warranty), 7DGD (3 year warranty), 7DK2 (3 year warranty, Neptune Core liquid cooled), 7DLN (3 year warranty, SAP HANA)
  Sockets     1-2
  CPU         Intel Xeon 6 P-core (6700P-series or 6500P-series)
  Memory      32 slots (16/socket, 8ch x 2 DPC), up to 6400 MT/s, max 8TB with 32x 256GB 3DS RDIMM
              RDIMM 6400 MT/s at 1 DPC, 5200 at 2 DPC; MRDIMM up to 8000 MT/s at 1 DPC.
  Drives      front max 24x 2.5", 12x 3.5"
              - Front: 3.5-inch 8 or 12 bays; 2.5-inch 8, 16 or 24 bays; E3.S 32 bays
              - Middle: 8x 2.5-inch simple-swap
              - Rear: 4x 3.5-inch, or 4/8x 2.5-inch
              - Chassis totals up to 16x 3.5-inch, 40x 2.5-inch or 32x E3.S
  PCIe        up to 10 slots + 2 OCP  (All PCIe 5.0, all at the rear; risers 3 and 4 need 2 processors.)
  PSU         2 bays. 80 PLUS Platinum/Titanium; 800W, 1300W, 2000W, 2700W, 3200W AC. All support 230V, some also 115V. HVDC and -48V DC options exist.
  GPU         Up to 10x single-wide or 2x double-wide GPUs (4x double-wide: see SR650a V4)
  https://lenovopress.lenovo.com/lp2127
```

```
ThinkSystem SR650a V4  (2U rack)  [lp2128, as of 2026-09]
  MTMs        7DGDCTO2WW 7DGDCTO4WW
  Mach types  7DGC (1 year warranty (per LP2128)), 7DGD (3 year warranty (per LP2128))
  Sockets     1-2
  CPU         Intel Xeon 6 P-core 6700P-series or 6500P-series (Granite Rapids)
  Memory      32 slots (16/socket, 8ch x 2 DPC), up to 6400 MT/s, max 8TB with 32x 256GB 3DS RDIMM
              RDIMM 6400 MT/s at 1 DPC, 5200 at 2 DPC; MRDIMM up to 8000 MT/s at 1 DPC only (no 2 DPC).
  Drives      front max 8x 2.5", no 3.5" front bays
              - Front only: up to 8x 2.5-inch or 8x E3.S 1T hot-swap (E3.S is NVMe only)
              - No rear drive bays; M.2 boot options as on SR650 V4
              No 3.5-inch option.
  PCIe        up to 14 slots + 2 OCP  (Up to 8 front slots for GPUs (risers 6 and 7, 4 slots each) + 6 rear (risers 2 and 3); all PCIe 5.0; risers 3 and 6 need 2 processors.)
  PSU         2 bays. 80 PLUS Platinum/Titanium; 800W, 1300W, 2000W, 2700W, 3200W AC. All support 230V, some also 115V. HVDC and -48V DC options exist.
  GPU         GPU-optimised: up to 4x double-wide or 8x single-wide GPUs in the front slots (e.g. 2x H200 NVL 600W, 4x L40S, 8x L4)
  Note        LP2128 covers both SR650a V4 and SR650i V4.
  https://lenovopress.lenovo.com/lp2128
```

```
ThinkSystem SR635 V3  (1U rack)  [lp1609, as of 2026-09]
  MTMs        7D9GCTO1WW 7D9GCTO2WW 7D9GCTOAWW 7D9GCTOBWW
  Mach types  7D9G (3 year warranty), 7D9H (1 year warranty)
  Sockets     1
  CPU         One AMD EPYC processor: 5th Gen 9005 (Turin) or 4th Gen 9004 (Genoa)
  Memory      12 slots (12/socket, 12ch x 1 DPC), up to 6400 MT/s, max 3TB with 12x 256GB 3DS RDIMM
              6400 MT/s needs EPYC 9005; EPYC 9004 runs 4800 MT/s.
  Drives      front max 10x 2.5", no 3.5" front bays
              - Front: 4x, 8x or 10x 2.5-inch (SAS/SATA, AnyBay or NVMe); 16x E1.S EDSFF NVMe
              - Rear: 2x 2.5-inch SAS/SATA or NVMe, or 2x 7mm (12x 2.5-inch total)
              - Internal M.2 module (up to 2 drives)
              - Up to 12x NVMe, all direct-connected
              The guide states there are no 3.5-inch drive bay configurations.
  PCIe        up to 5 slots + 1 OCP  (Dedicated OCP 3.0 slot, rear or front.)
  PSU         2 bays. 80 PLUS Platinum/Titanium; 750W, 1100W, 1800W AC (220V); 750W and 1100W also accept 110V; a 1100W -48V DC option exists.
  GPU         Up to 4x single-wide 75W GPUs per the key-features text (the spec table says 5x): confirm in the guide
  https://lenovopress.lenovo.com/lp1609
```

```
ThinkSystem SR645 V3  (1U rack)  [lp1607, as of 2026-09]
  MTMs        7D9CCTO1WW 7D9CCTO2WW 7D9CCTOAWW 7D9CCTOBWW
  Mach types  7D9C (3 year warranty), 7D9D (1 year warranty)
  Sockets     1-2
  CPU         AMD EPYC 9005 (5th Gen, Turin) or 9004 (4th Gen, Genoa)
  Memory      24 slots (12/socket, 12ch x 1 DPC), up to 6400 MT/s, max 6TB with 24x 256GB 3DS RDIMM
              One DIMM per channel only. 6400 MT/s needs EPYC 9005.
  Drives      front max 10x 2.5", 4x 3.5"
              - Front 3.5-inch: 4x SAS/SATA, AnyBay, or 2x SAS/SATA + 2x NVMe
              - Front 2.5-inch: 2x/4x/8x/10x; 16x E1.S EDSFF NVMe
              - Rear: 2x 2.5-inch SAS/SATA or NVMe, or 2x 7mm (12x 2.5-inch total)
              - Up to 12x NVMe, all direct-connected
  PCIe        up to 5 slots + 1 OCP  (Rear 3x or 2x slots; front slots in some configurations; OCP 3.0 slot rear or front.)
  PSU         2 bays. 80 PLUS Platinum/Titanium; 500W, 750W, 1100W, 1800W AC (220V); 500W, 750W, 1100W also accept 110V; a 1100W -48V DC option exists.
  GPU         Up to 5x single-wide 75W GPUs
  https://lenovopress.lenovo.com/lp1607
```

```
ThinkSystem SR655 V3  (2U rack)  [lp1610, as of 2026-09]
  MTMs        7D9ECTO1WW 7D9ECTO2WW 7D9ECTO3WW 7D9ECTO4WW
  Mach types  7D9E (3 year warranty), 7D9F (1 year warranty)
  Sockets     1
  CPU         One AMD EPYC processor: 9005 (Turin) or 9004 (Genoa)
  Memory      12 slots (12/socket, 12ch x 1 DPC), up to 6400 MT/s, max 3TB with 12x 256GB 3DS RDIMM
              6400 MT/s with EPYC 9005, 4800 MT/s with EPYC 9004.
  Drives      front max 24x 2.5", 12x 3.5"
              - Front: 3.5-inch 8 or 12; 2.5-inch 8, 16 or 24
              - Middle: 4x 3.5-inch or 8x 2.5-inch
              - Rear: 2/4x 3.5-inch or 4/8x 2.5-inch
              - Chassis totals up to 20x 3.5-inch or 40x 2.5-inch
  PCIe        up to 10 slots + 1 OCP  (10 rear, or 6 rear + 2 front, plus a slot dedicated to the OCP adapter (rear or front).)
  PSU         2 bays. 80 PLUS Platinum/Titanium; 750W, 1100W, 1800W, 2400W, 2600W AC (220V); 750W and 1100W also accept 110V.
  GPU         Up to 8x single-wide or 3x double-wide GPUs
  Note        Single-socket only: no 2-CPU option.
  https://lenovopress.lenovo.com/lp1610
```

```
ThinkSystem SR665 V3  (2U rack)  [lp1608, as of 2026-09]
  MTMs        7D9ACTO1WW 7D9ACTO2WW 7D9ACTOAWW 7D9ACTOBWW
  Mach types  7D9A (3 year warranty), 7D9B (1 year warranty)
  Sockets     1-2
  CPU         AMD EPYC, 5th Gen 9005 (Turin) or 4th Gen 9004 (Genoa)
  Memory      24 slots (12/socket, 12ch x 1 DPC), up to 6400 MT/s, max 6TB with 24x 256GB 3DS RDIMM
              6400 MT/s applies to EPYC 9005 only; EPYC 9004 runs 4800 MT/s.
  Drives      front max 24x 2.5", 12x 3.5"
              - Front: 3.5-inch 8 or 12; 2.5-inch 8, 16 or 24
              - Middle: 4x 3.5-inch or 8x 2.5-inch
              - Rear: 2/4x 3.5-inch or 4/8x 2.5-inch, plus 2x 7mm and internal M.2
              - Chassis totals up to 20x 3.5-inch or 40x 2.5-inch; NVMe up to 32 without oversubscription
  PCIe        up to 12 slots + 1 OCP  (10 rear + 2 front, plus a dedicated OCP 3.0 slot; riser choice limits some slot/drive-bay combinations.)
  PSU         2 bays. 80 PLUS Platinum/Titanium; 750W, 1100W, 1800W, 2400W, 2600W AC (220V); 750W and 1100W also accept 110V; a 1100W -48V DC option exists.
  GPU         Up to 8x single-wide or 3x double-wide GPUs
  https://lenovopress.lenovo.com/lp1608
```

```
ThinkSystem ST650 V3  (4U tower)  [lp1604, as of 2026-07]
  MTMs        7D7ACTO1WW 7D7ACTOAWW
  Mach types  7D7A
  Sockets     1-2
  CPU         4th/5th Gen Intel Xeon Scalable, up to 32 cores / 250W
  Memory      32 slots (16/socket, 8ch x 2 DPC), up to 5600 MT/s, max 4TB with 32x 128GB 3DS RDIMM
              All 32 slots need two processors. 5600 MT/s only at 1 DPC with 5th Gen Xeon; 4800 (5th Gen) / 4400 (4th Gen) at 2 DPC.
  Drives      front max 32x 2.5", 16x 3.5"
              - Up to 32x 2.5-inch hot-swap (max 24x NVMe) plus 2x 5.25-inch media bays, OR up to 16x 3.5-inch hot-swap
              - The 2.5-inch and 3.5-inch chassis configurations differ
  PCIe        up to 9 slots + unconfirmed OCP  (OCP slot count not confirmed here (earlier research recorded 0); check LP1604.)
  PSU         2 bays. Two hot-swap redundant supplies.
  Note        Rack-convertible tower.
  https://lenovopress.lenovo.com/lp1604
```

```
ThinkSystem SR675 V3  (3U rack)  [lp1611, as of 2026-07]
  MTMs        7D9RCTO1WW 7D9RCTO2WW
  Mach types  7D9R
  Sockets     1-2
  CPU         AMD EPYC 9004 (Genoa) / 9005 (Turin)
  Memory      24 slots (12/socket, 12ch x 1 DPC), up to 6400 MT/s
              4800 MT/s with EPYC 9004; 6400 MT/s with EPYC 9005.
  Drives      front max 8x 2.5", no 3.5" front bays
              - 2.5-inch or EDSFF only; drive/slot maxima depend on the base model
              - 4-DW GPU model: up to 8x 2.5-inch AnyBay front
              - 8-DW GPU model: EDSFF (6x E1.S or 4x E3.S) instead of 2.5-inch
              - SXM model: up to 4x 2.5-inch
              No 3.5-inch option.
  PCIe        up to 14 slots + 1 OCP  (Up to 14 expansion slots + 1 OCP, limited by PCIe lanes and the GPU/drive-bay configuration.)
  PSU         4 bays. Four supply bays.
  GPU         GPU-rich 3U with three base models: 4x double-wide GPU, 8x double-wide GPU, SXM (NVIDIA HGX)
  https://lenovopress.lenovo.com/lp1611
```

```
ThinkSystem SR860 V3  (4U rack)  [lp1606, as of 2026-07]
  MTMs        7D93CTO1WW 7D93CTO2WW 7D95CTO1WW
  Mach types  7D93, 7D95
  Sockets     2-4
  CPU         4th Gen Intel Xeon Scalable (Gold or Platinum)
  Memory      64 slots (16/socket, 8ch x 2 DPC), up to 4800 MT/s
              4800 MT/s at 1 DPC, 4400 MT/s at 2 DPC.
  Drives      front max 48x 2.5", no 3.5" front bays
              - 2.5-inch bays only; up to 24x NVMe (PCIe Gen4/Gen5) of the 48 front bays
              No 3.5-inch bays.
  PCIe        up to 18 slots + 2 OCP
  PSU         4 bays. Four supply bays.
  Note        Mission-critical 4-socket design; two or four processors, single-CPU configurations are not offered.
  https://lenovopress.lenovo.com/lp1606
```

```
ThinkAgile HX630 V4  (1U rack)  [lp2132, as of 2026-09]
  MTMs        7DG3CTO1WW
  Mach types  7DG3
  Sockets     2  (HCI min 2 CPU)
  CPU         Intel Xeon 6 P-core 6500P/6700P series (Granite Rapids), up to 86 cores, up to 350W
  Memory      32 slots (16/socket, 8ch x 2 DPC), up to 6400 MT/s, max 8TB with 32x 256GB 3DS RDIMM
              RDIMM 6400 MT/s at 1 DPC, 5200 at 2 DPC; MRDIMM up to 8000 MT/s (needs 6700P CPUs).
  Drives      front max 10x 2.5", no 3.5" front bays
              - Front: 10x 2.5-inch NVMe or 16x E3.S
              - M.2 for OS boot
              All-flash NVMe only: no 3.5-inch and no SAS/SATA data drives.
  PCIe        up to 3 slots + 2 OCP  (All PCIe 5.0, all at the rear; 2 OCP 3.0 slots (x8 or x16).)
  PSU         2 bays. 80 PLUS Platinum/Titanium; 800W, 1300W, 2000W AC. All support 230V, some also 115V; HVDC and -48V DC options exist.
  GPU         Up to 3x single-wide GPUs
  Note        1U appliance built on the SR630 V4.
  Note        The guide lists two processors installed; there is no 1-CPU option.
  Note        Two-node clusters: guide limits storage to 20TB per node and notes limited-workload support.
  https://lenovopress.lenovo.com/lp2132
```

```
ThinkAgile HX650 V4  (2U rack)  [lp2133, as of 2026-09]
  MTMs        7DG4CTO1WW 7DG4CTO2WW
  Mach types  7DG4 (CTO1 = HX650 V4 (all-flash), CTO2 = HX650 V4 Storage (storage-heavy hybrid))
  Sockets     1-2
  CPU         Intel Xeon 6 P-core 6700P/6500P-series (Granite Rapids), up to 86 cores, up to 350W
  Memory      32 slots (16/socket, 8ch x 2 DPC), up to 6400 MT/s, max 8TB with 32x 256GB 3DS RDIMM
              RDIMM 6400 MT/s at 1 DPC, 5200 at 2 DPC; MRDIMM up to 8000 MT/s.
  Drives      front max 24x 2.5", 12x 3.5"
              - HX650 V4 (7DG4CTO1WW): front 16 or 24x 2.5-inch NVMe, no rear bays, no 3.5-inch
              - HX650 V4 Storage (7DG4CTO2WW): front 8x 3.5-inch SAS/SATA + 4x 3.5-inch AnyBay (12x 3.5-inch), rear 4x 2.5-inch (rear drive kit only with 10 or more HDDs)
              - Internal M.2 module (2 drives)
              - Guide notes: HDDs over 20TB are only for Nutanix Unified Storage use
              3.5-inch drives exist only on the Storage variant.
  PCIe        up to 10 slots + 2 OCP  (All PCIe 5.0, all at the rear; risers 3 and 4 need 2 processors (so the full 10 slots need 2 CPUs); the Storage variant lists up to 9.)
  PSU         2 bays. 80 PLUS Platinum/Titanium; 800W, 1300W, 2000W, 2700W, 3200W AC. All support 230V, some also 115V; HVDC and -48V DC options exist.
  GPU         Up to 10x single-wide or 2x double-wide GPUs (all-flash model)
  Note        The guide states HX650 V4 and HX650 V4 Storage each support 1 or 2 processors; an earlier revision listed the base model as 2-CPU only.
  Note        Nutanix capacity notes in the guide: per-node capacity over 307TB is only for Nutanix Unified Storage use (hybrid: 307TB to 550TB); a 2-node configuration is limited to 20TB per node.
  https://lenovopress.lenovo.com/lp2133
```

```
ThinkAgile VX630 V4  (1U rack)  [lp2134, as of 2026-09]
  MTMs        7DG5CTO1WW
  Mach types  7DG5 (3 or 5 year warranty)
  Sockets     1-2  (HCI min 1 CPU)
  CPU         Intel Xeon 6 P-core 6500P/6700P series (Granite Rapids-SP)
  Memory      32 slots (16/socket, 8ch x 2 DPC), up to 6400 MT/s, max 8TB with 32x 256GB 3DS RDIMM
              RDIMM 6400 MT/s at 1 DPC, 5200 at 2 DPC; MRDIMM up to 8000 MT/s at 1 DPC.
  Drives      front max 10x 2.5", no 3.5" front bays
              - Front: up to 10x 2.5-inch (NVMe or AnyBay); 12x 2.5-inch total with 2 rear
              - M.2 boot options
              2.5-inch only.
  PCIe        up to 3 slots + 2 OCP  (All at the rear; some slots are unavailable with 1 processor.)
  PSU         2 bays. 80 PLUS Platinum/Titanium; 800W, 1300W, 2000W AC. All support 230V, some also 115V.
  GPU         Up to 3x single-wide GPUs
  Note        vSAN: 2-node clusters use a witness appliance; VCF needs 4 nodes for a management domain, VVF 3 hosts minimum.
  https://lenovopress.lenovo.com/lp2134
```

```
ThinkAgile VX650 V4  (2U rack)  [lp2135, as of 2026-07]
  MTMs        7DG6CTO1WW 7DG6CTO4WW
  Mach types  7DG6
  Sockets     1-2  (HCI min 1 CPU)
  CPU         Intel Xeon 6 P-core 6500P/6700P-series (Granite Rapids-SP)
  Memory      32 slots (16/socket, 8ch x 2 DPC), up to 6400 MT/s
              RDIMM 6400 MT/s at 1 DPC, 5200 at 2 DPC; MRDIMM up to 8000 MT/s at 1 DPC.
  Drives      front max 24x 2.5", no 3.5" front bays
              - Front: 24x 2.5-inch or 24x E3.S
              - Up to 24x NVMe with 1:1 connectivity
              - Rear 2.5-inch or 3.5-inch bays and rear M.2 can replace some slots
              No 3.5-inch front option; a few rear 3.5-inch bays can replace PCIe slots.
  PCIe        up to 10 slots + 2 OCP
  PSU         2 bays. Two hot-swap redundant supplies.
  https://lenovopress.lenovo.com/lp2135
```
