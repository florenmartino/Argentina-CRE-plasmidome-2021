#!/usr/bin/env python3
"""Validate the public release package without changing scientific results."""

from __future__ import annotations

import csv
import hashlib
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]

REQUIRED_FILES = [
    "README.md",
    "WORKFLOW.md",
    "SCRIPT_DAG.md",
    "DATA_AVAILABILITY.md",
    "REPRODUCIBILITY.md",
    "MANIFEST.md",
    "environment.yml",
    "package.json",
    "data/accession_lists/reference_plasmids_34.tsv",
    "data/accession_lists/reference_inventory_34.tsv",
    "data/provenance/ps0007_reference_workflow/updated_cluster_table_PS0007.tsv",
    "data/provenance/ps0007_reference_workflow/updated_cluster_table_PS0007.xlsx",
    "data/provenance/ps0007_reference_workflow/representative_selection_report.md",
    "data/provenance/ps0007_reference_workflow/reference_workflow_comparison.md",
    "data/provenance/ps0007_reference_workflow/group_summary_PS0007.tsv",
    "data/provenance/ps0007_reference_workflow/critical_checks_PS0007.tsv",
    "data/provenance/ps0007_short_read_assignment/coverage_summary_PS0007.tsv",
    "data/provenance/ps0007_short_read_assignment/backbone_assignments_PS0007.tsv",
    "data/provenance/ps0007_short_read_assignment/delta_rule_impact_PS0007.tsv",
    "data/derived/all_candidate_hits.tsv",
    "data/derived/excluded_small_plasmid_hits.tsv",
    "data/derived/final_assignments.tsv",
    "data/derived/figure_PS0007_backbones_epi_v3_source_data.tsv",
    "figures/figure2_backbone_summary/figure_PS0007_backbones_epi_v3.pdf",
    "figures/figure2_backbone_summary/figure_PS0007_backbones_epi_v3.pptx",
    "figures/figure3_sankey/sankey_input_final.tsv",
    "figures/figure3_sankey/RECAPTARII_Figure3_sankey_final.svg",
    "figures/figure3_sankey/RECAPTARII_Figure3_sankey_final.pdf",
    "figures/figure3_sankey/RECAPTARII_Figure3_sankey_final.pptx",
    "figures/figure3_sankey/RECAPTARII_Figure3_sankey_final_600dpi.png",
    "scripts/01_reference_plasmid_workflow/cluster_reference_plasmids.sh",
    "scripts/02_backbone_assignment/validate_sankey_input.py",
    "scripts/03_tables/build_input_inventory.py",
    "scripts/04_figures/make_figure3_sankey.mjs",
]

EXPECTED_SANKY_BACKBONES = {
    "C01": 10,
    "C02": 18,
    "C03": 11,
    "C04": 10,
    "C05": 16,
    "S01": 1,
    "S03": 1,
}

EXPECTED_UPDATED_CLUSTER_COUNTS = {
    "C01": 5,
    "C02": 5,
    "C03": 7,
    "C04": 7,
    "C05": 3,
    "C06": 2,
    "S01": 1,
    "S03": 1,
    "S04": 1,
    "S05": 1,
    "S06": 1,
}

EXPECTED_FIGURE2_CLOSED_COUNTS = {
    "C01": 5,
    "C02": 5,
    "C03": 7,
    "C04": 7,
    "C05": 3,
}

EXPECTED_FIGURE2_ISOLATE_COUNTS = {
    "C01": 6,
    "C02": 14,
    "C03": 8,
    "C04": 5,
    "C05": 15,
}


def read_tsv(relative_path: str) -> list[dict[str, str]]:
    with (ROOT / relative_path).open(newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def fasta_length(path: Path) -> int:
    total = 0
    with path.open() as handle:
        for line in handle:
            if line.startswith(">"):
                continue
            total += len(line.strip())
    return total


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def require(label: str, observed, expected) -> None:
    if observed != expected:
        raise ValueError(f"{label}: expected {expected}, observed {observed}")


def check_required_files(lines: list[str]) -> None:
    missing = [item for item in REQUIRED_FILES if not (ROOT / item).exists()]
    require("missing required files", missing, [])
    lines.append(f"Required files present: {len(REQUIRED_FILES)}")


def check_references(lines: list[str]) -> None:
    manifest = read_tsv("data/accession_lists/reference_plasmids_34.tsv")
    inventory = read_tsv("data/accession_lists/reference_inventory_34.tsv")
    fastas = sorted((ROOT / "data/plasmid_references/references_34").glob("*.fasta"))
    genbank_fastas = sorted((ROOT / "data/plasmid_references/genbank_missing").glob("*.fasta"))

    require("reference manifest rows", len(manifest), 34)
    require("reference inventory rows", len(inventory), 34)
    require("reference FASTA count", len(fastas), 34)
    require("GenBank provenance FASTA count", len(genbank_fastas), 4)

    for row in manifest:
        fasta = ROOT / row["local_fasta"]
        if not fasta.exists():
            raise ValueError(f"missing reference FASTA listed in manifest: {row['local_fasta']}")
        require(f"length for {row['local_fasta']}", fasta_length(fasta), int(row["length_bp"]))

    lines.append("Reference plasmid manifest rows: 34")
    lines.append("Reference FASTA files in references_34: 34")
    lines.append("GenBank provenance FASTA files: 4")


def check_provenance(lines: list[str]) -> None:
    updated = read_tsv("data/provenance/ps0007_reference_workflow/updated_cluster_table_PS0007.tsv")
    groups = Counter(row["Cluster and Representative plasmid"].split(";")[0] for row in updated)
    require("updated cluster table rows", len(updated), 34)
    require("updated cluster membership counts", dict(groups), EXPECTED_UPDATED_CLUSTER_COUNTS)

    coverage = read_tsv("data/provenance/ps0007_short_read_assignment/coverage_summary_PS0007.tsv")
    assignments = read_tsv("data/provenance/ps0007_short_read_assignment/backbone_assignments_PS0007.tsv")
    require("coverage summary rows", len(coverage), 627)
    require("backbone assignment rows", len(assignments), 58)
    require("backbone assignment samples", len({row["sample"] for row in assignments}), 49)

    lines.append("Updated PS0007 cluster table rows: 34")
    lines.append("Coverage summary rows: 627")
    lines.append("Raw backbone assignment rows: 58")
    lines.append("Raw backbone assignment samples: 49")


def check_final_tables(lines: list[str]) -> None:
    final_assignments = read_tsv("data/derived/final_assignments.tsv")
    figure2 = read_tsv("data/derived/figure_PS0007_backbones_epi_v3_source_data.tsv")
    require("final assignment rows", len(final_assignments), 48)
    require("Figure 2 source rows", len(figure2), 75)

    closed_counts = Counter(row["display_cluster"] for row in figure2 if row["record_type"] == "closed_plasmid")
    isolate_counts = Counter(row["display_cluster"] for row in figure2 if row["record_type"] == "recaptar_isolate")
    require("Figure 2 closed plasmid counts", dict(closed_counts), EXPECTED_FIGURE2_CLOSED_COUNTS)
    require("Figure 2 isolate counts", dict(isolate_counts), EXPECTED_FIGURE2_ISOLATE_COUNTS)

    lines.append("Final assignment rows: 48")
    lines.append("Figure 2 source rows: 75")


def check_sankey(lines: list[str]) -> None:
    rows = read_tsv("figures/figure3_sankey/sankey_input_final.tsv")
    isolate_counts = Counter(row["isolate_id"] for row in rows)
    backbone_counts = Counter(row["backbone_cluster"] for row in rows)
    duals = sorted(isolate for isolate, count in isolate_counts.items() if count == 2)

    require("Sankey rows", len(rows), 67)
    require("Sankey unique isolates", len(isolate_counts), 63)
    require("Sankey dual-backbone isolates", duals, ["PAD003", "ZCA001", "ZCU001", "ZCZ001"])
    require("Sankey backbone counts", dict(backbone_counts), EXPECTED_SANKY_BACKBONES)

    lines.append("Total isolates: 70")
    lines.append("Carbapenemase-positive isolates: 68")
    lines.append("Carbapenemase-negative isolates: 2")
    lines.append("Unique isolates included in Figure 3 Sankey: 63")
    lines.append("Figure 3 Sankey flows: 67")
    lines.append("Dual-backbone isolates: PAD003, ZCA001, ZCU001, ZCZ001")


def write_hashes() -> None:
    hashed_paths = [
        "data/accession_lists/reference_plasmids_34.tsv",
        "data/accession_lists/reference_inventory_34.tsv",
        "data/provenance/ps0007_reference_workflow/updated_cluster_table_PS0007.tsv",
        "data/provenance/ps0007_short_read_assignment/coverage_summary_PS0007.tsv",
        "data/provenance/ps0007_short_read_assignment/backbone_assignments_PS0007.tsv",
        "data/derived/final_assignments.tsv",
        "data/derived/figure_PS0007_backbones_epi_v3_source_data.tsv",
        "figures/figure2_backbone_summary/figure_PS0007_backbones_epi_v3.pdf",
        "figures/figure2_backbone_summary/figure_PS0007_backbones_epi_v3.pptx",
        "figures/figure3_sankey/sankey_input_final.tsv",
        "figures/figure3_sankey/RECAPTARII_Figure3_sankey_final.svg",
        "figures/figure3_sankey/RECAPTARII_Figure3_sankey_final.pdf",
        "figures/figure3_sankey/RECAPTARII_Figure3_sankey_final.pptx",
        "figures/figure3_sankey/RECAPTARII_Figure3_sankey_final_600dpi.png",
    ]
    output = ROOT / "validation/release_hashes.tsv"
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", newline="") as handle:
        writer = csv.writer(handle, delimiter="\t")
        writer.writerow(["path", "sha256"])
        for relative_path in hashed_paths:
            writer.writerow([relative_path, sha256(ROOT / relative_path)])


def write_report(lines: list[str]) -> None:
    report = ROOT / "validation/release_validation.md"
    report.parent.mkdir(parents=True, exist_ok=True)
    report.write_text("\n".join([
        "# Release Validation",
        "",
        *[f"- {line}" for line in lines],
        "",
        "Validation status: passed.",
        "",
    ]))


def main() -> None:
    lines: list[str] = []
    check_required_files(lines)
    check_references(lines)
    check_provenance(lines)
    check_final_tables(lines)
    check_sankey(lines)
    write_hashes()
    write_report(lines)
    print("Public release validation passed.")


if __name__ == "__main__":
    main()
