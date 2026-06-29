#!/usr/bin/env python3
"""Create repository input inventory and reference FASTA validation reports."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


def fasta_length(path: Path) -> int:
    total = 0
    with path.open() as handle:
        for line in handle:
            if line.startswith(">"):
                continue
            total += len(line.strip())
    return total


def read_manifest(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def write_inventory(root: Path, output: Path) -> None:
    rows = []
    for path in sorted(root.glob("data/**/*")):
        if not path.is_file():
            continue
        role = "input"
        if "/derived/" in path.as_posix():
            role = "derived_input"
        rows.append({
            "path": path.relative_to(root).as_posix(),
            "bytes": path.stat().st_size,
            "role": role,
        })
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, delimiter="\t", fieldnames=["path", "bytes", "role"])
        writer.writeheader()
        writer.writerows(rows)


def write_reference_report(root: Path, manifest_path: Path, output: Path) -> None:
    manifest = read_manifest(manifest_path)
    missing = []
    length_mismatches = []
    observed = []
    for row in manifest:
        fasta = root / row["local_fasta"]
        if not fasta.exists():
            missing.append(row["local_fasta"])
            continue
        observed_length = fasta_length(fasta)
        observed.append(fasta.relative_to(root).as_posix())
        expected_length = int(row["length_bp"])
        if observed_length != expected_length:
            length_mismatches.append((row["local_fasta"], expected_length, observed_length))

    lines = [
        "# Reference Plasmid Validation",
        "",
        f"Manifest: {manifest_path.relative_to(root)}",
        f"Manifest rows: {len(manifest)}",
        f"Reference FASTA files observed from manifest: {len(observed)}",
        f"Missing FASTA files: {len(missing)}",
        f"Length mismatches: {len(length_mismatches)}",
        "",
        "The complete 34-reference FASTA collection is retained under data/plasmid_references/references_34/.",
        "The genbank_missing/ directory is retained as provenance for GenBank records that were added during final curation and also copied into references_34/.",
        "",
    ]
    if missing:
        lines.extend(["## Missing FASTA Files", "", *[f"- {item}" for item in missing], ""])
    if length_mismatches:
        lines.extend(["## Length Mismatches", "", "| FASTA | Expected bp | Observed bp |", "| --- | ---: | ---: |"])
        lines.extend(f"| {name} | {expected} | {observed_value} |" for name, expected, observed_value in length_mismatches)
        lines.append("")
    lines.append("Validation status: passed." if not missing and not length_mismatches and len(manifest) == 34 else "Validation status: review required.")
    lines.append("")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(lines))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path("."))
    parser.add_argument("--inventory", type=Path, default=Path("validation/input_inventory.tsv"))
    parser.add_argument("--reference-report", type=Path, default=Path("validation/reference_plasmid_validation.md"))
    args = parser.parse_args()

    root = args.root.resolve()
    manifest = root / "data/accession_lists/reference_plasmids_34.tsv"
    write_inventory(root, root / args.inventory)
    write_reference_report(root, manifest, root / args.reference_report)
    print(f"Wrote {args.inventory} and {args.reference_report}")


if __name__ == "__main__":
    main()
