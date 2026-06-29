# 30-reference versus 34-reference clustering comparison

Generated during the historical analysis: 2026-06-20

Original 30-reference output: historical reference set summarized in retained provenance tables

New 34-reference run: retained here under `data/provenance/ps0007_reference_workflow/` and `data/provenance/ps0007_short_read_assignment/`

## Run configuration

- Workflow script: `reference clustering workflow used in the historical analysis; public clustering wrapper is scripts/01_reference_plasmid_workflow/cluster_reference_plasmids.sh`
- Representative script: `representative-selection script used in the historical analysis; final representatives are retained in this repository`
- Edge preset: `CLASSIC95_MAX` (`RECIP_PID_T=95`, `RECIP_COV_T=85`, `EDGE_ID_MODE=MAX`, no length guards)
- Input reference directory: `data/plasmid_references/references_34`

## Summary counts

| Metric | Original 30-reference | New 34-reference |
|---|---:|---:|
| Input plasmids | 30 | 34 |
| Pairwise rows | 870 | 1120 |
| Edges | 48 | 63 |
| Connected components | 11 | 10 |
| Multi-member clusters | 5 | 5 |
| Singletons | 6 | 5 |
| Representative rows | 11 | 10 |
| Component sizes | [7, 5, 5, 5, 2, 1, 1, 1, 1, 1, 1] | [8, 7, 7, 5, 2, 1, 1, 1, 1, 1] |

## New 34-reference cluster membership

- `C01` (7): CBO001_OXA_48L, CP166604.1_pM27284_154_IncC_blaNDM-1, HCU002_NDM_1, MH995507.1_pM17277_NDM, ZCA001_OXA_163, ZCU001_OXA_163, ZCV001_KPC_3
- `C02` (7): CP166596.1_pM25992_249_IncFIB_IncHI1B_blaNDM-5, CP166600.1_pM25979_249_IncFIB-IncHI1B_blaNDM-5_, PQ247031.1, PQ247032.1, ZAG001_KPC_2, ZCA001_NDM_5, ZDA001_NDM_5
- `C03` (8): COS001_NDM_5, CP166605.1_pM27284_79_IncR_blaKPC-3_, PAD003_NDM_5, PQ241462.1, PQ241463.1, ZAC001_KPC_2, ZDA002_KPC_2, ZEI002_KPC_2
- `C04` (5): BAR001_KPC_2, CP166602.1_pM25979_84_IncM1_blaKPC-2, ROS002_KPC_2, ZCU001_KPC_2, ZDZ001_KPC_2
- `C05` (2): pWW14A-KPC2_CP080103.1, pWW19C-KPC2_CP080110.1
- `C06` (1): CP166597.1_pM25992_10_IncFIB_pQil_IncFII_K_blaKPC-2_
- `C07` (1): MN082782.1_pPA2047
- `C08` (1): PAD003_KPC_2
- `C09` (1): VLP001_OXA_439
- `C10` (1): pHdC_pae_OL780449.1

## How the original 30-reference clusters map to the 34-reference result

| Old cluster | Old size | Best new cluster | Old members retained | New members added to that component |
|---|---:|---|---:|---|
| `C01` | 7 | `C01` | 7 | none |
| `C02` | 5 | `C02` | 5 | PQ247031.1, PQ247032.1 |
| `C03` | 5 | `C03` | 5 | COS001_NDM_5, PQ241462.1, PQ241463.1 |
| `C04` | 5 | `C04` | 5 | none |
| `C05` | 2 | `C05` | 2 | none |
| `C06` | 1 | `C03` | 1 | CP166605.1_pM27284_79_IncR_blaKPC-3_, PAD003_NDM_5, PQ241462.1, PQ241463.1, ZAC001_KPC_2, ZDA002_KPC_2, ZEI002_KPC_2 |
| `C07` | 1 | `C06` | 1 | none |
| `C08` | 1 | `C07` | 1 | none |
| `C09` | 1 | `C08` | 1 | none |
| `C10` | 1 | `C10` | 1 | none |
| `C11` | 1 | `C09` | 1 | none |

## New PQ accession placement

- `PQ241462.1` -> `C03`
- `PQ241463.1` -> `C03`
- `PQ247031.1` -> `C02`
- `PQ247032.1` -> `C02`

## Representative changes

| Old cluster | Best new cluster | Original representative | New representative | Same? |
|---|---|---|---|---|
| `C01` | `C01` | `CBO001_OXA_48L` | `CBO001_OXA_48L` | yes |
| `C02` | `C02` | `CP166596.1_pM25992_249_IncFIB_IncHI1B_blaNDM-5` | `CP166596.1_pM25992_249_IncFIB_IncHI1B_blaNDM-5` | yes |
| `C03` | `C03` | `ZDA002_KPC_2` | `PQ241463.1` | no |
| `C04` | `C04` | `ZCU001_KPC_2` | `ZCU001_KPC_2` | yes |
| `C05` | `C05` | `pWW19C-KPC2_CP080110.1` | `pWW19C-KPC2_CP080110.1` | yes |
| `C06` | `C03` | `COS001_NDM_5` | `PQ241463.1` | no |
| `C07` | `C06` | `CP166597.1_pM25992_10_IncFIB_pQil_IncFII_K_blaKPC-2_` | `CP166597.1_pM25992_10_IncFIB_pQil_IncFII_K_blaKPC-2_` | yes |
| `C08` | `C07` | `MN082782.1_pPA2047` | `MN082782.1_pPA2047` | yes |
| `C09` | `C08` | `PAD003_KPC_2` | `PAD003_KPC_2` | yes |
| `C10` | `C10` | `pHdC_pae_OL780449.1` | `pHdC_pae_OL780449.1` | yes |
| `C11` | `C09` | `VLP001_OXA_439` | `VLP001_OXA_439` | yes |

## Edges involving PQ accessions or the former COS singleton

- `COS001_NDM_5` -- `PQ241462.1`
- `COS001_NDM_5` -- `PQ241463.1`
- `CP166596.1_pM25992_249_IncFIB_IncHI1B_blaNDM-5` -- `PQ247031.1`
- `CP166596.1_pM25992_249_IncFIB_IncHI1B_blaNDM-5` -- `PQ247032.1`
- `CP166600.1_pM25979_249_IncFIB-IncHI1B_blaNDM-5_` -- `PQ247031.1`
- `CP166600.1_pM25979_249_IncFIB-IncHI1B_blaNDM-5_` -- `PQ247032.1`
- `PAD003_NDM_5` -- `PQ241462.1`
- `PQ241462.1` -- `PQ241463.1`
- `PQ247031.1` -- `PQ247032.1`
- `PQ247031.1` -- `ZAG001_KPC_2`
- `PQ247031.1` -- `ZCA001_NDM_5`
- `PQ247031.1` -- `ZDA001_NDM_5`
- `PQ247032.1` -- `ZAG001_KPC_2`
- `PQ247032.1` -- `ZCA001_NDM_5`
- `PQ247032.1` -- `ZDA001_NDM_5`

## Manuscript statement check

The new 34-reference run produced 10 connected components total: 5 multi-member clusters and 5 singletons. The manuscript statement of six clusters and five singletons is therefore **not reproduced** by this 34-reference run when using the historical `CLASSIC95_MAX` edge behavior that matches the preserved 30-reference output.

The four added PQ references join existing components rather than creating a sixth multi-member cluster. `PQ247031.1` and `PQ247032.1` join the former C02 component. `PQ241462.1` and `PQ241463.1` join the component that now also includes the former `COS001_NDM_5` singleton and the former C03 members.
