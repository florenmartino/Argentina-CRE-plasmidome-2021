# Updated Table Change Log for PS0007

No manuscript or figure files were modified. This table uses PS0007 outputs and the requested display-label relabeling only; underlying PS0007 memberships are unchanged.

## Display Label Crosswalk

underlying_PS0007_cluster_id	display_cluster_id	display_replicon_family	underlying_representative_id	representative_plasmid	display_note
C01	C01	IncR	SEQ__ZDA002_KPC_2__00001	pZDA002_73	Historical IncR backbone group.
C02	C02	IncL/M	SEQ__ZCU001_KPC_2__00001	pZCU001_77	Historical IncL/M backbone group.
C03	C03	IncFIB(Mar)/IncHI1B	SEQ__CP166596.1_pM25992_249_IncFIB_IncHI1B_blaNDM-5__00001	pM25992_249	Historical IncFIB(Mar)/IncHI1B backbone group plus PQ247031.1 and PQ247032.1 under PS0007.
C04	C04	IncC	SEQ__CBO001_OXA_48L__00001	pCBO001_150	Historical IncC backbone group.
C05	C06	IncP6-like	SEQ__pWW19C-KPC2_CP080110.1__00001	pWW19C-KPC2	Display relabel of underlying PS0007 C05: IncP6-like KPC minor cluster.
C06	C05	IncFII	SEQ__PQ241463.1__00001	PQ241463.1	Display relabel of underlying PS0007 C06: pCOS/PQ IncFII NDM-5 component.
S01	S01	ColRNAI	SEQ__PAD003_KPC_2__00001	pPAD003_22	Historical singleton retained.
S03	S03	IncFIB(pQil)/IncFII	SEQ__CP166597.1_pM25992_10_IncFIB_pQil_IncFII_K_blaKPC-2___00001	pM25992_107	Historical singleton retained.
S04	S04	IncHI1A/IncHI1B	SEQ__VLP001_OXA_439__00001	pVLP001_339	Historical singleton retained.
S05	S05	ND	SEQ__MN082782.1_pPA2047__00001	pPA2047_44	Historical singleton retained.
S06	S06	ND	SEQ__pHdC_pae_OL780449.1__00001	pHdC_pae	Historical singleton retained.


## Group Summary

display_cluster_id	member_count	members	representative
C01	5	pM27284_79; pPAD003_131; pZAC001_148; pZDA002_73; pZEI002_55	pZDA002_73
C02	5	pBAR001_77; pM25979_84; pROS002_77; pZCU001_77; pZDZ001_75	pZCU001_77
C03	7	pM25992_249; pM25979_249; pZAG001_232; pZCA001_256; pZDA001_456; PQ247031.1; PQ247032.1	pM25992_249
C04	7	pCBO001_150; pM27284_154; pHCU002_151; pM17277_139; pZCA001_134; pZCU001_132; pZCV001_167	pCBO001_150
C05	3	pCOS001_98; PQ241462.1; PQ241463.1	PQ241463.1
C06	2	pWW14A-KPC2; pWW19C-KPC2	pWW19C-KPC2
S01	1	pPAD003_22	pPAD003_22
S03	1	pM25992_107	pM25992_107
S04	1	pVLP001_339	pVLP001_339
S05	1	pPA2047_44	pPA2047_44
S06	1	pHdC_pae	pHdC_pae


## Differences Versus the Pasted Historical Table

- pCOS001_98 moves from historical singleton S02 to display C05, the pCOS/PQ IncFII NDM-5 component.
- PQ241462.1 is added to display C05.
- PQ241463.1 is added to display C05 and is the PS0007 medoid representative for that component.
- PQ247031.1 and PQ247032.1 are added to display C03.
- pWW14A-KPC2 and pWW19C-KPC2 are display-labeled as C06/minor C06, following the requested relabeling of underlying PS0007 C05.
- Historical C01-C04 members remain unchanged, with C03 expanded by PQ247031.1 and PQ247032.1 as requested.
- Historical singletons S01, S03, S04, S05, and S06 remain singleton.
- Historical S02 is no longer shown as a singleton.
- Short-read comparison check: 17 changed rows; 0 not explained by S02-to-C05 display relabeling.
- PQ241462.1 notes retain the pEco265-NDM5 header naming; no pEco256/pEco265 silent renaming was performed.

## Critical Checks

check	status	expected	observed	missing	unexpected
C01_membership	PASS	pM27284_79; pPAD003_131; pZAC001_148; pZDA002_73; pZEI002_55	pM27284_79; pPAD003_131; pZAC001_148; pZDA002_73; pZEI002_55	none	none
C02_membership	PASS	pBAR001_77; pM25979_84; pROS002_77; pZCU001_77; pZDZ001_75	pBAR001_77; pM25979_84; pROS002_77; pZCU001_77; pZDZ001_75	none	none
C03_membership	PASS	PQ247031.1; PQ247032.1; pM25979_249; pM25992_249; pZAG001_232; pZCA001_256; pZDA001_456	PQ247031.1; PQ247032.1; pM25979_249; pM25992_249; pZAG001_232; pZCA001_256; pZDA001_456	none	none
C04_membership	PASS	pCBO001_150; pHCU002_151; pM17277_139; pM27284_154; pZCA001_134; pZCU001_132; pZCV001_167	pCBO001_150; pHCU002_151; pM17277_139; pM27284_154; pZCA001_134; pZCU001_132; pZCV001_167	none	none
C05_membership	PASS	PQ241462.1; PQ241463.1; pCOS001_98	PQ241462.1; PQ241463.1; pCOS001_98	none	none
C06_membership	PASS	pWW14A-KPC2; pWW19C-KPC2	pWW14A-KPC2; pWW19C-KPC2	none	none
S01_membership	PASS	pPAD003_22	pPAD003_22	none	none
S03_membership	PASS	pM25992_107	pM25992_107	none	none
S04_membership	PASS	pVLP001_339	pVLP001_339	none	none
S05_membership	PASS	pPA2047_44	pPA2047_44	none	none
S06_membership	PASS	pHdC_pae	pHdC_pae	none	none
34_plasmids	PASS	34	34	none	none
pCOS001_98_not_singleton	PASS	C05	C05	none	none
17_short_read_changes_S02_to_C05_only	PASS	17 changes, all S02-to-C05 relabeling only	17 changed rows; 0 not explained by S02-to-C05 display relabeling	none	none


## Missing Annotation Fields Recorded as ND

- Accession: 19 row(s) contain ND.
- Best short-read coverage hits: 6 row(s) contain ND.
- Carbapenemase: 5 row(s) contain ND.
- Carbapenemase.1: 3 row(s) contain ND.
- Other Antimicrobial Resistance Genes: 34 row(s) contain ND.
- Replicon type: 2 row(s) contain ND.
- Replicon type.1: 2 row(s) contain ND.

Notes: Other antimicrobial resistance genes were not present in the specified PS0007/reference inputs and are therefore recorded as ND rather than inferred from unrelated files. Carbapenemase values are taken from clinical metadata for study isolates when available or parsed from explicit reference names/headers where present.
