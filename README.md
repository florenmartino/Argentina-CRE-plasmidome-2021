# Argentina CRE plasmidome 2021

Public repository for the computational analysis accompanying a genomic epidemiology study of carbapenem-resistant Enterobacterales collected in Argentina during 2021.

The analysis integrates closed carbapenemase-carrying plasmids, curated plasmid backbone clustering, short-read projection to representative plasmid backbones, and final manuscript figure inputs.

## Scientific Scope

This repository preserves the final manuscript products and the minimal computational provenance needed to understand their lineage:

1. 34 closed reference plasmids.
2. Reference plasmid clustering and representative selection.
3. Short-read coverage projection against representative backbones.
4. Raw PS0007 backbone assignments.
5. Curated final backbone assignments.
6. Figure 2 source data and frozen publication files.
7. Figure 3 final Sankey input and publication files.

## Repository Layout

| Path | Contents |
| --- | --- |
| `data/accession_lists/` | Reference plasmid manifests and reference inventory. |
| `data/plasmid_references/references_34/` | Complete 34-plasmid FASTA collection used for the final reference set. |
| `data/plasmid_references/genbank_missing/` | Four GenBank FASTAs retained as accession provenance and also present in `references_34/`. |
| `data/metadata/` | Assembly inventory retained for reproducibility context. |
| `data/provenance/` | PS0007 clustering, representative-selection, coverage, and assignment provenance. |
| `data/derived/` | Curated final assignment tables and Figure 2 source data. |
| `figures/figure2_backbone_summary/` | Frozen publication Figure 2 PDF and editable PowerPoint. |
| `figures/figure3_sankey/` | Final Figure 3 Sankey input and publication exports. |
| `scripts/` | Public validation and figure-generation scripts. |
| `validation/` | Deterministic validation reports, hashes, and traceability tables. |

## Requirements

The public validation workflow uses Python standard-library modules and Node.js. Optional reference BLAST validation requires BLAST+.

Recommended conda environment:

```bash
conda env create -f environment.yml
conda activate argentina-cre-plasmidome-2021
```

Node dependencies:

```bash
npm install
```

The project has no external npm package dependencies.

## Quick Validation

Run the public validation workflow:

```bash
npm run validate
```

This command checks reference FASTA completeness, validates retained provenance tables, validates final assignments, validates the Figure 3 Sankey counts, and regenerates a content-validating SVG from `sankey_input_final.tsv`.

Figure 3 SVG regeneration is content-validating but not expected to be byte-identical to the frozen publication SVG because SVG serialization can differ across runtime environments.

## Figure Policy

Figure 2 is retained as a frozen publication figure derived from the curated Figure 2 source data and the full PS0007 reference provenance. The public workflow validates the retained source data and provenance but does not regenerate Figure 2.

Figure 3 is regenerated from `figures/figure3_sankey/sankey_input_final.tsv` using `scripts/04_figures/make_figure3_sankey.mjs`. The frozen SVG, PDF, PPTX, and 600 dpi PNG are retained under `figures/figure3_sankey/`.

## Final Figure 3 Counts

| Metric | Value |
| --- | ---: |
| Total isolates | 70 |
| Carbapenemase-positive isolates | 68 |
| Carbapenemase-negative isolates | 2 |
| Carbapenemase-positive isolates with assigned plasmid backbone shown in Sankey | 63 |
| Dual-backbone isolates expanded into two rows | 4 |
| Total Sankey flows | 67 |

Backbone counts in the final Sankey input:

| Backbone | Flows |
| --- | ---: |
| C01 | 10 |
| C02 | 18 |
| C03 | 11 |
| C04 | 10 |
| C05 | 16 |
| S01 | 1 |
| S03 | 1 |

Dual-backbone isolates expanded in the Sankey: `PAD003`, `ZCA001`, `ZCU001`, and `ZCZ001`.

Carbapenemase-negative isolates and carbapenemase-positive isolates lacking an assigned plasmid backbone are excluded from plotted Sankey flows.

## Main Commands

```bash
python3 scripts/03_tables/build_input_inventory.py
python3 scripts/03_tables/validate_public_release.py
python3 scripts/02_backbone_assignment/validate_sankey_input.py
node scripts/04_figures/make_figure3_sankey.mjs --out-dir validation/figure3_sankey_regenerated_svg
```

Optional BLAST reference workflow:

```bash
ROOT="$PWD" THREADS=4 bash scripts/01_reference_plasmid_workflow/cluster_reference_plasmids.sh
```

The optional BLAST workflow writes to `validation/reference_plasmid_workflow/` and does not modify curated input data.

## Documentation

See:

- `WORKFLOW.md`
- `SCRIPT_DAG.md`
- `DATA_AVAILABILITY.md`
- `REPRODUCIBILITY.md`
- `MANIFEST.md`

