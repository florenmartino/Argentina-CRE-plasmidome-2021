# Release Manifest

Repository: `Argentina-CRE-plasmidome-2021-public`

Release date: 2026-06-29

## Scientific Summary

This repository accompanies a genomic epidemiology analysis of carbapenem-resistant Enterobacterales from Argentina. It preserves the final reference plasmid collection, PS0007 plasmid backbone provenance, curated final assignments, and final publication figure files.

## Key Counts

| Item | Count |
| --- | ---: |
| Reference plasmids | 34 |
| Reference FASTA files in `references_34/` | 34 |
| GenBank accession-provenance FASTAs | 4 |
| Total isolates | 70 |
| Carbapenemase-positive isolates | 68 |
| Carbapenemase-negative isolates | 2 |
| Dual-backbone isolates in Figure 3 | 4 |
| Figure 3 Sankey flows | 67 |

## Figure Outputs

Figure 2:

- `figures/figure2_backbone_summary/figure_PS0007_backbones_epi_v3.pdf`
- `figures/figure2_backbone_summary/figure_PS0007_backbones_epi_v3.pptx`

Figure 3:

- `figures/figure3_sankey/RECAPTARII_Figure3_sankey_final.svg`
- `figures/figure3_sankey/RECAPTARII_Figure3_sankey_final.pdf`
- `figures/figure3_sankey/RECAPTARII_Figure3_sankey_final.pptx`
- `figures/figure3_sankey/RECAPTARII_Figure3_sankey_final_600dpi.png`

## Table Outputs

- `data/provenance/ps0007_reference_workflow/updated_cluster_table_PS0007.tsv`
- `data/provenance/ps0007_short_read_assignment/coverage_summary_PS0007.tsv`
- `data/provenance/ps0007_short_read_assignment/backbone_assignments_PS0007.tsv`
- `data/derived/final_assignments.tsv`
- `data/derived/figure_PS0007_backbones_epi_v3_source_data.tsv`
- `figures/figure3_sankey/sankey_input_final.tsv`

## Validation Outputs

- `validation/input_inventory.tsv`
- `validation/reference_plasmid_validation.md`
- `validation/release_validation.md`
- `validation/release_hashes.tsv`
- `validation/figure3_sankey_validation.md`
- `validation/figure3_sankey_counts.tsv`
- `validation/traceability_retained_files.tsv`
- `validation/traceability_excluded_files.tsv`

## Software

- Python 3.12
- Node.js 20
- BLAST+ 2.16 for optional reference validation
- librsvg 2.58 for optional static export from SVG

