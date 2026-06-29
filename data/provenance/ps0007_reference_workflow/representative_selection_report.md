# PS0007 Representative Selection Report

Run directory: retained here under `data/provenance/ps0007_reference_workflow/` and `data/provenance/ps0007_short_read_assignment/`

Output directory: `data/provenance/ps0007_reference_workflow/`

Generated: 2026-06-20T16:45:23

## Inputs

- Representative-selection script: `representative-selection script used in the historical analysis; final representatives are retained in this repository`
- Pairwise table: `historical PS0007 reproducibility run retained here under data/provenance/pairwise_long.tsv`
- FASTA: `historical PS0007 reproducibility run retained here under data/provenance/all_plasmids.fa`
- Cluster file: `data/provenance/ps0007_reference_workflow/plasmid_cluster_PS0007.tsv`

The raw cluster file is headerless because the original script treats every row as data. A human-readable annotated copy was also written as `plasmid_cluster_PS0007_annotated.tsv`.

## Cluster-label decision

Two labels were considered for the pCOS001_98/PQ241462.1/PQ241463.1 component:

- `C06`: recommended for PS0007 outputs because the component is a de novo multi-member connected component and PS0007 yields six multi-member clusters plus five singletons.
- `S02_expanded`: useful as an alias in documentation because pCOS001_98 was historical singleton S02 in the original 30-reference grouping.

This run uses `C06` as the stable computational label and documents `S02_expanded` as the historical alias.

## Selected representatives

| Cluster | PS0007 representative | Sum S2 score | Pairs used | Cluster size | Members |
|---|---|---:|---:|---:|---|
| C01 | pZDA002_73 | 0.983392 | 1 | 5 | pM27284_79; pPAD003_131; pZAC001_148; pZDA002_73; pZEI002_55 |
| C02 | pZCU001_77 | 3.976657 | 4 | 5 | pBAR001_77; pM25979_84; pROS002_77; pZCU001_77; pZDZ001_75 |
| C03 | pM25992_249 | 4.626350 | 5 | 7 | pM25992_249; pM25979_249; pZAG001_232; pZCA001_256; pZDA001_456; PQ247031.1; PQ247032.1 |
| C04 | pCBO001_150 | 4.944580 | 5 | 7 | pCBO001_150; pM27284_154; pHCU002_151; pM17277_139; pZCA001_134; pZCU001_132; pZCV001_167 |
| C05 | pWW19C-KPC2 | 0.000000 | 0 | 2 | pWW14A-KPC2; pWW19C-KPC2 |
| C06 | PQ241463.1 | 1.979789 | 2 | 3 | pCOS001_98; PQ241462.1; PQ241463.1 |
| S01 | pPAD003_22 | 0.000000 | 0 | 1 | pPAD003_22 |
| S03 | pM25992_107 | 0.000000 | 0 | 1 | pM25992_107 |
| S04 | pVLP001_339 | 0.000000 | 0 | 1 | pVLP001_339 |
| S05 | pPA2047_44 | 0.000000 | 0 | 1 | pPA2047_44 |
| S06 | pHdC_pae | 0.000000 | 0 | 1 | pHdC_pae |

## Comparison to original manuscript/table representatives

| Original label | PS0007 label | Original representative | PS0007 representative | Reason |
|---|---|---|---|---|
| S02 | C06 | pCOS001_98 | PQ241463.1 | Historical S02 is no longer a singleton under PS0007; pCOS001_98 clusters naturally with PQ241462.1 and PQ241463.1, and the script-selected medoid is PQ241463.1. |
| new_34_reference_component_alias_S02_expanded | C06 | pCOS001_98 was historical S02 representative | PQ241463.1 | PQ241463.1 has the highest medoid score within the pCOS001_98/PQ241462.1/PQ241463.1 component. |

All historical C01-C05 representatives are retained under PS0007. Historical singletons S01, S03, S04, S05, and S06 also retain their own representatives.

## New pCOS/PQ component

Members of `C06`:

- pCOS001_98
- PQ241462.1
- PQ241463.1

Selected medoid representative: `PQ241463.1`.

Pairwise support inside C06:

| Plasmid A | Plasmid B | Max HSP identity | Weighted identity | Reciprocal coverage | S2 |
|---|---|---:|---:|---:|---:|
| pCOS001_98 | PQ241462.1 | 100.000 | 98.615 | 100.000 | 0.986153 |
| pCOS001_98 | PQ241463.1 | 100.000 | 99.349 | 100.000 | 0.993486 |
| PQ241462.1 | PQ241463.1 | 100.000 | 98.630 | 100.000 | 0.986303 |

pCOS001_98 remains a biologically understandable historical representative for continuity with the original S02 singleton, but it is not the medoid under the original script. PQ241463.1 is selected because it has the highest sum of S2 values to the other two members, by a very small margin.

## Figure/table implications

If the manuscript and figures are aligned to PS0007, a structural update is needed wherever pCOS001_98 is shown as a singleton S02 or where PQ241462.1/PQ241463.1 are not represented in the pCOS-related component. C01-C05 representative identities do not need updating.

If the current figures are retained as historical/curated grouping figures, then the PS0007 result should be documented as a reproducibility/sensitivity update rather than silently substituted.
