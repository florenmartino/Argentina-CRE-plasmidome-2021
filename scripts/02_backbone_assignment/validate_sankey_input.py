#!/usr/bin/env python3
"""Validate the curated Figure 3 Sankey input table."""

from __future__ import annotations

import argparse
import csv
from collections import Counter, defaultdict
from pathlib import Path


EXPECTED_TOTAL_ISOLATES = 70
EXPECTED_POSITIVE_ISOLATES = 68
EXPECTED_NEGATIVE_ISOLATES = 2
EXPECTED_INCLUDED_ISOLATES = 63
EXPECTED_FLOWS = 67
EXPECTED_DUALS = ["PAD003", "ZCA001", "ZCU001", "ZCZ001"]
EXPECTED_BACKBONES = {
    "C01": 10,
    "C02": 18,
    "C03": 11,
    "C04": 10,
    "C05": 16,
    "S01": 1,
    "S03": 1,
}


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        expected = ["isolate_id", "species", "sequence_type", "backbone_cluster", "carbapenemase_allele"]
        if reader.fieldnames != expected:
            raise ValueError(f"Unexpected header in {path}: {reader.fieldnames}")
        return list(reader)


def count_rows(rows: list[dict[str, str]]) -> dict[str, Counter[str]]:
    counters: dict[str, Counter[str]] = {
        "isolates": Counter(),
        "species": Counter(),
        "sequence_types": Counter(),
        "backbones": Counter(),
        "carbapenemases": Counter(),
    }
    for row in rows:
        for field in ["isolate_id", "species", "sequence_type", "backbone_cluster", "carbapenemase_allele"]:
            if not row[field]:
                raise ValueError(f"Missing {field} in row: {row}")
        if "negative" in row["carbapenemase_allele"].lower():
            raise ValueError(f"Carbapenemase-negative row present in Sankey input: {row}")
        counters["isolates"][row["isolate_id"]] += 1
        counters["species"][row["species"]] += 1
        counters["sequence_types"][row["sequence_type"]] += 1
        counters["backbones"][row["backbone_cluster"]] += 1
        counters["carbapenemases"][row["carbapenemase_allele"]] += 1
    return counters


def require_equal(label: str, observed, expected) -> None:
    if observed != expected:
        raise ValueError(f"{label}: expected {expected}, observed {observed}")


def markdown_table(counter: Counter[str], left: str, right: str = "Count") -> list[str]:
    lines = [f"| {left} | {right} |", "| --- | ---: |"]
    for key in sorted(counter, key=lambda value: (value.startswith("S"), value)):
        lines.append(f"| {key} | {counter[key]} |")
    return lines


def write_report(path: Path, counters: dict[str, Counter[str]], duals: list[str]) -> None:
    lines: list[str] = [
        "# Figure 3 Sankey Validation",
        "",
        f"Total isolates: {EXPECTED_TOTAL_ISOLATES}",
        f"Carbapenemase-positive isolates: {EXPECTED_POSITIVE_ISOLATES}",
        f"Carbapenemase-negative isolates: {EXPECTED_NEGATIVE_ISOLATES}",
        f"Unique isolates included in Sankey: {len(counters['isolates'])}",
        f"Total Sankey flows: {sum(counters['backbones'].values())}",
        f"Dual-backbone isolates: {', '.join(duals)}",
        "",
        "Carbapenemase-negative isolates are excluded from the plotted Sankey flows.",
        "Carbapenemase-positive isolates lacking an assigned plasmid backbone are excluded from the plotted Sankey flows.",
        "",
        "## Backbone Counts",
        "",
        *markdown_table(counters["backbones"], "Backbone"),
        "",
        "## Carbapenemase Counts",
        "",
        *markdown_table(counters["carbapenemases"], "Carbapenemase"),
        "",
        "## Species Counts",
        "",
        *markdown_table(counters["species"], "Species"),
        "",
        "## Sequence Type Counts",
        "",
        *markdown_table(counters["sequence_types"], "Sequence type"),
        "",
        "Validation status: passed.",
        "",
    ]
    path.write_text("\n".join(lines))


def write_counts_tsv(path: Path, counters: dict[str, Counter[str]]) -> None:
    with path.open("w", newline="") as handle:
        writer = csv.writer(handle, delimiter="\t")
        writer.writerow(["category", "label", "count"])
        for category, counter in counters.items():
            for label, count in sorted(counter.items()):
                writer.writerow([category, label, count])


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=Path("figures/figure3_sankey/sankey_input_final.tsv"))
    parser.add_argument("--report", type=Path, default=Path("validation/figure3_sankey_validation.md"))
    parser.add_argument("--counts", type=Path, default=Path("validation/figure3_sankey_counts.tsv"))
    args = parser.parse_args()

    rows = read_rows(args.input)
    counters = count_rows(rows)
    duals = sorted([isolate for isolate, count in counters["isolates"].items() if count == 2])
    over_expanded = [isolate for isolate, count in counters["isolates"].items() if count > 2]

    require_equal("Total Sankey rows", len(rows), EXPECTED_FLOWS)
    require_equal("Unique isolates included", len(counters["isolates"]), EXPECTED_INCLUDED_ISOLATES)
    require_equal("Dual-backbone isolate list", duals, EXPECTED_DUALS)
    require_equal("Over-expanded isolates", over_expanded, [])
    require_equal("Backbone counts", dict(counters["backbones"]), EXPECTED_BACKBONES)

    incoming: defaultdict[str, int] = defaultdict(int)
    outgoing: defaultdict[str, int] = defaultdict(int)
    for row in rows:
        incoming[row["backbone_cluster"]] += 1
        outgoing[row["backbone_cluster"]] += 1
    for backbone, expected in EXPECTED_BACKBONES.items():
        require_equal(f"{backbone} incoming/node/outgoing", (incoming[backbone], counters["backbones"][backbone], outgoing[backbone]), (expected, expected, expected))

    args.report.parent.mkdir(parents=True, exist_ok=True)
    write_report(args.report, counters, duals)
    write_counts_tsv(args.counts, counters)
    print(f"Figure 3 Sankey validation passed: {len(rows)} flows, {len(counters['isolates'])} isolates.")


if __name__ == "__main__":
    main()
