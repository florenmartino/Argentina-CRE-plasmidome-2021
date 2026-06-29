# Data Availability

This repository retains the data required to validate the final public analysis package.

## Retained Data

| Data class | Location |
| --- | --- |
| Reference manifest | `data/accession_lists/reference_plasmids_34.tsv` |
| Reference inventory | `data/accession_lists/reference_inventory_34.tsv` |
| Complete 34-reference FASTA collection | `data/plasmid_references/references_34/` |
| GenBank accession provenance FASTAs | `data/plasmid_references/genbank_missing/` |
| Assembly inventory | `data/metadata/assembly_inventory.tsv` |
| PS0007 reference workflow provenance | `data/provenance/ps0007_reference_workflow/` |
| PS0007 short-read assignment provenance | `data/provenance/ps0007_short_read_assignment/` |
| Curated derived tables | `data/derived/` |
| Final Figure 2 files | `figures/figure2_backbone_summary/` |
| Final Figure 3 files | `figures/figure3_sankey/` |

## Reference FASTAs

The final reference collection contains 34 FASTA files in `data/plasmid_references/references_34/`. Four GenBank records added during final reference curation are also retained in `data/plasmid_references/genbank_missing/` to document their accession provenance.

## Figures

Figure 2 is retained as a frozen publication figure together with source and provenance tables.

Figure 3 is retained as SVG, PDF, PPTX, and 600 dpi PNG, and the editable SVG can be regenerated from the final Sankey TSV.

## Non-Retained Data

The public repository does not include temporary BLAST databases, scratch files, preview figures, cache directories, previous development exports, or non-public working folders.

