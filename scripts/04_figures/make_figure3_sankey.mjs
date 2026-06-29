#!/usr/bin/env node

/*
Build and validate the Figure 3 Sankey SVG from the curated final Sankey input.

The repository includes the final publication SVG, PDF, PPTX, and 600 dpi PNG
under figures/figure3_sankey/. This script regenerates the editable SVG and
validation tables from the final TSV using public Node.js APIs only. Optional
PDF and PNG export can be performed with rsvg-convert when it is installed.
*/

import fs from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { spawnSync } from "node:child_process";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(__dirname, "../..");

const DEFAULT_INPUT = path.join(ROOT, "figures", "figure3_sankey", "sankey_input_final.tsv");
const DEFAULT_OUT = path.join(ROOT, "figures", "figure3_sankey", "regenerated");
const STEM = "RECAPTARII_Figure3_sankey_final";

const W = 1800;
const H = 1320;

const EXPECTED = {
  totalIsolates: 70,
  carbapenemasePositiveIsolates: 68,
  carbapenemaseNegativeIsolates: 2,
  representedIsolates: 63,
  totalFlows: 67,
  dualBackboneIsolates: ["PAD003", "ZCA001", "ZCU001", "ZCZ001"],
  backboneCounts: {
    C01: 10,
    C02: 18,
    C03: 11,
    C04: 10,
    C05: 16,
    S01: 1,
    S03: 1,
  },
};

const COLORS = {
  ink: "#111827",
  muted: "#4B5563",
  line: "#6B7280",
  background: "#FFFFFF",
  node: "#FFFFFF",
  cluster: {
    C01: "#0B6B3A",
    C02: "#0B4EA2",
    C03: "#7A1A7A",
    C04: "#F28C00",
    C05: "#D7191C",
    S01: "#8B8F96",
    S03: "#4B5563",
  },
};

const TITLE = "Distribution of species, sequence types, plasmid backbones and carbapenemase genes";
const SUBTITLE = "Among 70 isolates, 68 carried at least one carbapenemase gene. Sixty-three carbapenemase-positive isolates with an assigned plasmid backbone were included in the Sankey diagram. Four isolates carrying two carbapenemase-bearing plasmids were expanded into two backbone-level flows, yielding a total of 67 flows.";

const CAPTION = [
  "Figure 3. Distribution of bacterial species, multilocus sequence types (STs), plasmid backbone clusters, and carbapenemase genes among carbapenemase-producing isolates.",
  "",
  "The Sankey diagram summarizes plasmid backbone assignments based on the final curated reference backbone collection. Among the 70 isolates analyzed, 68 carried at least one carbapenemase gene. Sixty-three carbapenemase-positive isolates with an assigned plasmid backbone were included in the visualization. Four isolates carrying two carbapenemase-bearing plasmids (PAD003, ZCA001, ZCU001 and ZCZ001) were expanded into two independent backbone-level flows, resulting in 67 total flows.",
  "",
  "Clusters C01-C05 correspond to recurrent plasmid backbone groups, whereas S01 and S03 represent singleton plasmids. Carbapenemase-negative isolates and carbapenemase-positive isolates lacking an assigned plasmid backbone were excluded from the Sankey flows.",
  "",
  "Node counts correspond to backbone-level flows rather than unique isolates.",
];

function parseArgs(argv) {
  const args = { input: DEFAULT_INPUT, outDir: DEFAULT_OUT, exportStatic: false };
  for (let i = 0; i < argv.length; i += 1) {
    const arg = argv[i];
    if (arg === "--input") args.input = path.resolve(argv[++i]);
    else if (arg === "--out-dir") args.outDir = path.resolve(argv[++i]);
    else if (arg === "--export-static") args.exportStatic = true;
    else if (arg === "--help") {
      console.log("Usage: node scripts/04_figures/make_figure3_sankey.mjs [--input file.tsv] [--out-dir dir] [--export-static]");
      process.exitCode = 0;
      args.help = true;
    } else {
      throw new Error(`Unknown argument: ${arg}`);
    }
  }
  return args;
}

function esc(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;");
}

function parseTsv(text) {
  const lines = text.trim().split(/\r?\n/);
  const headers = lines.shift().split("\t");
  const expected = ["isolate_id", "species", "sequence_type", "backbone_cluster", "carbapenemase_allele"];
  if (headers.join("\t") !== expected.join("\t")) {
    throw new Error(`Unexpected input header: ${headers.join(", ")}`);
  }
  return lines.filter(Boolean).map((line, index) => {
    const values = line.split("\t");
    if (values.length !== headers.length) {
      throw new Error(`Malformed row ${index + 2}: expected ${headers.length} columns, found ${values.length}.`);
    }
    return Object.fromEntries(headers.map((header, i) => [header, values[i]]));
  });
}

function addCount(map, key, value = 1) {
  map.set(key, (map.get(key) || 0) + value);
}

function addEdge(map, source, target, backbone, value = 1) {
  const key = `${source}\t${target}\t${backbone}`;
  addCount(map, key, value);
}

function displaySpecies(species) {
  const names = {
    "Klebsiella pneumoniae": "K. pneumoniae",
    "Enterobacter hormaechei": "E. hormaechei",
    "Serratia marcescens": "S. marcescens",
    "Escherichia coli": "E. coli",
    "Proteus mirabilis": "P. mirabilis",
    "Klebsiella aerogenes": "K. aerogenes",
    "Citrobacter freundii": "C. freundii",
  };
  return names[species] || species;
}

function displaySt(st) {
  return st && st !== "ND" ? st : "No ST";
}

function displayBackbone(cluster) {
  const names = {
    C01: "C01-IncR",
    C02: "C02-IncL/M",
    C03: "C03-IncFIB(Mar)/IncHI1B",
    C04: "C04-IncC",
    C05: "C05-IncFII",
    S01: "S01-ColRNAI",
    S03: "S03-IncHI1A/IncHI1B",
  };
  return names[cluster] || cluster;
}

function mapObject(map) {
  return Object.fromEntries(Array.from(map.entries()).sort(([a], [b]) => a.localeCompare(b, undefined, { numeric: true })));
}

function assertEqual(observed, expected, label) {
  if (observed !== expected) {
    throw new Error(`${label} mismatch: expected ${expected}, observed ${observed}.`);
  }
}

function assertMap(map, expected, label) {
  const observed = mapObject(map);
  const expectedSorted = Object.fromEntries(Object.entries(expected).sort(([a], [b]) => a.localeCompare(b, undefined, { numeric: true })));
  if (JSON.stringify(observed) !== JSON.stringify(expectedSorted)) {
    throw new Error(`${label} mismatch: expected ${JSON.stringify(expectedSorted)}, observed ${JSON.stringify(observed)}.`);
  }
}

function validateRows(rows) {
  const isolates = new Map();
  const species = new Map();
  const st = new Map();
  const backbones = new Map();
  const carbapenemases = new Map();
  const allowedBackbones = new Set(Object.keys(EXPECTED.backboneCounts));

  for (const row of rows) {
    for (const field of ["isolate_id", "species", "sequence_type", "backbone_cluster", "carbapenemase_allele"]) {
      if (!row[field]) throw new Error(`Missing ${field} in row ${JSON.stringify(row)}.`);
    }
    if (!allowedBackbones.has(row.backbone_cluster)) {
      throw new Error(`Unexpected backbone cluster ${row.backbone_cluster}.`);
    }
    if (/negative/i.test(row.carbapenemase_allele)) {
      throw new Error(`Carbapenemase-negative isolate present in Sankey input: ${row.isolate_id}.`);
    }
    addCount(isolates, row.isolate_id);
    addCount(species, row.species);
    addCount(st, displaySt(row.sequence_type));
    addCount(backbones, row.backbone_cluster);
    addCount(carbapenemases, row.carbapenemase_allele);
  }

  const duals = Array.from(isolates.entries()).filter(([, count]) => count === 2).map(([id]) => id).sort();
  const overExpanded = Array.from(isolates.entries()).filter(([, count]) => count > 2);
  if (overExpanded.length) throw new Error(`Isolate appears more than twice: ${JSON.stringify(overExpanded)}.`);

  assertEqual(rows.length, EXPECTED.totalFlows, "Total Sankey flow rows");
  assertEqual(isolates.size, EXPECTED.representedIsolates, "Unique represented isolates");
  assertEqual(duals.join(","), EXPECTED.dualBackboneIsolates.join(","), "Dual-backbone isolate list");
  assertMap(backbones, EXPECTED.backboneCounts, "Backbone counts");

  return { isolates, species, st, backbones, carbapenemases, duals };
}

function buildDisplay(rows) {
  const validation = validateRows(rows);
  const speciesToSt = new Map();
  const stToBackbone = new Map();
  const backboneToAllele = new Map();

  for (const row of rows) {
    const st = displaySt(row.sequence_type);
    addEdge(speciesToSt, row.species, st, row.backbone_cluster);
    addEdge(stToBackbone, st, row.backbone_cluster, row.backbone_cluster);
    addEdge(backboneToAllele, row.backbone_cluster, row.carbapenemase_allele, row.backbone_cluster);
  }

  const speciesOrder = [
    "Klebsiella pneumoniae",
    "Enterobacter hormaechei",
    "Serratia marcescens",
    "Escherichia coli",
    "Proteus mirabilis",
    "Klebsiella aerogenes",
  ].filter((id) => validation.species.has(id));

  const stPriority = ["ST11", "ST258", "ST15", "ST25", "ST13", "ST307", "No ST", "ST78", "ST716", "ST190"];
  const stOrder = Array.from(validation.st.keys()).sort((a, b) => {
    const ai = stPriority.includes(a) ? stPriority.indexOf(a) : 999;
    const bi = stPriority.includes(b) ? stPriority.indexOf(b) : 999;
    if (ai !== bi) return ai - bi;
    return validation.st.get(b) - validation.st.get(a) || a.localeCompare(b, undefined, { numeric: true });
  });

  const backboneOrder = ["C01", "C02", "C03", "C04", "C05", "S01", "S03"];
  const carbapenemaseOrder = ["blaKPC-2", "blaKPC-3", "blaNDM-5", "blaNDM-1", "blaOXA-163", "blaOXA-517-like", "blaOXA-439"]
    .filter((id) => validation.carbapenemases.has(id));

  function edges(map, layer) {
    return Array.from(map.entries()).map(([key, value]) => {
      const [source, target, backbone] = key.split("\t");
      return { source, target, backbone, value, layer };
    });
  }

  const flowRows = [
    ...edges(speciesToSt, "species_st"),
    ...edges(stToBackbone, "st_backbone"),
    ...edges(backboneToAllele, "backbone_allele"),
  ];

  const incoming = new Map();
  const outgoing = new Map();
  for (const flow of edges(stToBackbone, "st_backbone")) addCount(incoming, flow.target, flow.value);
  for (const flow of edges(backboneToAllele, "backbone_allele")) addCount(outgoing, flow.source, flow.value);
  const conservation = backboneOrder.map((id) => ({
    id,
    incoming: incoming.get(id) || 0,
    node: validation.backbones.get(id) || 0,
    outgoing: outgoing.get(id) || 0,
  }));
  for (const row of conservation) {
    if (row.incoming !== row.node || row.outgoing !== row.node) {
      throw new Error(`Backbone conservation failed for ${row.id}: ${row.incoming}/${row.node}/${row.outgoing}.`);
    }
  }

  return { validation, conservation, flowRows, orders: { speciesOrder, stOrder, backboneOrder, carbapenemaseOrder } };
}

function makeNodes(ids, counts, x, width, top, bottom, color, label, scale) {
  const gap = ids.length > 18 ? 5 : ids.length > 10 ? 8 : 14;
  const totalHeight = ids.reduce((sum, id) => sum + counts.get(id) * scale, 0);
  const used = totalHeight + gap * Math.max(0, ids.length - 1);
  let y = top + Math.max(0, (bottom - top - used) / 2);
  return ids.map((id) => {
    const h = counts.get(id) * scale;
    const node = { id, value: counts.get(id), x, y, w: width, h, color: color(id), label: label(id, counts.get(id)) };
    y += h + gap;
    return node;
  });
}

function layoutLayer(flows, sourceNodes, targetNodes, sourceOrder, targetOrder, scale, x1, x2) {
  const sourceMap = new Map(sourceNodes.map((n) => [n.id, n]));
  const targetMap = new Map(targetNodes.map((n) => [n.id, n]));
  const sourceIndex = new Map(sourceOrder.map((id, i) => [id, i]));
  const targetIndex = new Map(targetOrder.map((id, i) => [id, i]));
  const backboneIndex = new Map(["C01", "C02", "C03", "C04", "C05", "S01", "S03"].map((id, i) => [id, i]));

  const sorted = flows
    .filter((flow) => sourceMap.has(flow.source) && targetMap.has(flow.target))
    .sort((a, b) =>
      (sourceIndex.get(a.source) ?? 999) - (sourceIndex.get(b.source) ?? 999) ||
      (targetIndex.get(a.target) ?? 999) - (targetIndex.get(b.target) ?? 999) ||
      (backboneIndex.get(a.backbone) ?? 999) - (backboneIndex.get(b.backbone) ?? 999));

  const sourceTotals = new Map();
  const targetTotals = new Map();
  for (const flow of sorted) {
    addCount(sourceTotals, flow.source, flow.value * scale);
    addCount(targetTotals, flow.target, flow.value * scale);
  }

  const sourceCursor = new Map();
  const targetCursor = new Map();
  for (const [id, total] of sourceTotals) {
    const node = sourceMap.get(id);
    sourceCursor.set(id, node.y + Math.max(0, (node.h - total) / 2));
  }
  for (const [id, total] of targetTotals) {
    const node = targetMap.get(id);
    targetCursor.set(id, node.y + Math.max(0, (node.h - total) / 2));
  }

  return sorted.map((flow) => {
    const width = flow.value * scale;
    const sy = sourceCursor.get(flow.source) + width / 2;
    const ty = targetCursor.get(flow.target) + width / 2;
    sourceCursor.set(flow.source, sourceCursor.get(flow.source) + width);
    targetCursor.set(flow.target, targetCursor.get(flow.target) + width);
    return { ...flow, x1, x2, sy, ty, width, color: COLORS.cluster[flow.backbone] };
  });
}

function buildLayout(display) {
  const scale = 10.0;
  const top = 155;
  const bottom = 960;
  const nodeWidth = 10;
  const speciesNodes = makeNodes(display.orders.speciesOrder, display.validation.species, 185, nodeWidth, top + 18, bottom - 40, () => COLORS.node, (id, n) => `${displaySpecies(id)} (${n})`, scale);
  const stNodes = makeNodes(display.orders.stOrder, display.validation.st, 560, nodeWidth, top, bottom, () => COLORS.node, (id, n) => `${id} (${n})`, scale);
  const backboneNodes = makeNodes(display.orders.backboneOrder, display.validation.backbones, 1045, 12, top + 48, bottom - 70, (id) => COLORS.cluster[id], (id, n) => `${displayBackbone(id)} (${n})`, scale);
  const carbapenemaseNodes = makeNodes(display.orders.carbapenemaseOrder, display.validation.carbapenemases, 1560, nodeWidth, top + 35, bottom - 25, () => COLORS.node, (id, n) => `${id} (${n})`, scale);

  const flowLayouts = [
    ...layoutLayer(display.flowRows.filter((f) => f.layer === "species_st"), speciesNodes, stNodes, display.orders.speciesOrder, display.orders.stOrder, scale, 195, 560),
    ...layoutLayer(display.flowRows.filter((f) => f.layer === "st_backbone"), stNodes, backboneNodes, display.orders.stOrder, display.orders.backboneOrder, scale, 570, 1045),
    ...layoutLayer(display.flowRows.filter((f) => f.layer === "backbone_allele"), backboneNodes, carbapenemaseNodes, display.orders.backboneOrder, display.orders.carbapenemaseOrder, scale, 1057, 1560),
  ];

  return { speciesNodes, stNodes, backboneNodes, carbapenemaseNodes, flowLayouts };
}

function text(text, x, y, opts = {}) {
  const size = opts.size || 13;
  const weight = opts.weight || 400;
  const fill = opts.fill || COLORS.ink;
  const anchor = opts.anchor || "start";
  return `<text x="${x}" y="${y}" font-family="Arial, Helvetica, sans-serif" font-size="${size}" font-weight="${weight}" fill="${fill}" text-anchor="${anchor}">${esc(text)}</text>`;
}

function rect(x, y, w, h, fill, stroke = "none", sw = 0, rx = 0) {
  return `<rect x="${x}" y="${y}" width="${w}" height="${h}" rx="${rx}" fill="${fill}" stroke="${stroke}" stroke-width="${sw}"/>`;
}

function wrap(input, maxChars) {
  const words = input.split(/\s+/);
  const lines = [];
  let line = "";
  for (const word of words) {
    const next = line ? `${line} ${word}` : word;
    if (next.length > maxChars && line) {
      lines.push(line);
      line = word;
    } else {
      line = next;
    }
  }
  if (line) lines.push(line);
  return lines;
}

function textLines(lines, x, y, opts = {}) {
  const size = opts.size || 13;
  const leading = opts.leading || 1.2;
  return lines.map((line, i) => text(line, x, y + i * size * leading, opts)).join("\n");
}

function ribbon(flow, opacity = 0.43) {
  const dx = Math.max(135, Math.abs(flow.x2 - flow.x1) * 0.52);
  const yTop1 = flow.sy - flow.width / 2;
  const yBot1 = flow.sy + flow.width / 2;
  const yTop2 = flow.ty - flow.width / 2;
  const yBot2 = flow.ty + flow.width / 2;
  const d = [
    `M${flow.x1},${yTop1}`,
    `C${flow.x1 + dx},${yTop1} ${flow.x2 - dx},${yTop2} ${flow.x2},${yTop2}`,
    `L${flow.x2},${yBot2}`,
    `C${flow.x2 - dx},${yBot2} ${flow.x1 + dx},${yBot1} ${flow.x1},${yBot1}`,
    "Z",
  ].join(" ");
  return `<path d="${d}" fill="${flow.color}" fill-opacity="${opacity}" stroke="none"/>`;
}

function renderSvg(display, layout) {
  const parts = [
    `<svg xmlns="http://www.w3.org/2000/svg" width="${W}" height="${H}" viewBox="0 0 ${W} ${H}" role="img" aria-label="Figure 3 Sankey diagram">`,
    rect(0, 0, W, H, COLORS.background),
    text(TITLE, 128, 42, { size: 29, weight: 700 }),
    textLines(wrap(SUBTITLE, 174), 128, 76, { size: 15, fill: COLORS.muted, leading: 1.2 }),
    text("Species", 185, 136, { size: 17, weight: 700 }),
    text("Sequence type", 560, 136, { size: 17, weight: 700 }),
    text("Plasmid backbone", 1045, 136, { size: 17, weight: 700 }),
    text("Carbapenemase gene", 1560, 136, { size: 17, weight: 700 }),
  ];

  for (const flow of layout.flowLayouts) parts.push(ribbon(flow));

  function node(node, side, size, fill = COLORS.node, stroke = COLORS.line, sw = 1.05) {
    parts.push(rect(node.x, node.y, node.w, node.h, fill, stroke, sw, 5));
    const x = side === "left" ? node.x - 9 : node.x + node.w + 9;
    const anchor = side === "left" ? "end" : "start";
    parts.push(text(node.label, x, node.y + node.h / 2 + size * 0.34, { size, weight: 500, anchor }));
  }

  layout.speciesNodes.forEach((n) => node(n, "left", n.value <= 1 ? 13 : 14.2));
  layout.stNodes.forEach((n) => node(n, "left", n.value <= 1 ? 11.4 : 12.6));
  layout.backboneNodes.forEach((n) => node(n, "right", n.value <= 1 ? 12.3 : 13.7, n.color, n.color, 0));
  layout.carbapenemaseNodes.forEach((n) => node(n, "right", n.value <= 1 ? 12.3 : 13.9));

  const legendY = 1032;
  parts.push(text("Backbone color key", 128, legendY, { size: 15, weight: 700 }));
  display.orders.backboneOrder.forEach((id, i) => {
    const x = 128 + i * 230;
    const y = legendY + 28;
    parts.push(rect(x, y - 9, 11, 11, COLORS.cluster[id], COLORS.cluster[id], 0, 2));
    parts.push(text(displayBackbone(id), x + 18, y + 1, { size: 12 }));
  });

  const captionLines = [];
  for (const line of CAPTION) captionLines.push(...(line ? wrap(line, 182) : [""]));
  parts.push(textLines(captionLines, 128, 1112, { size: 12.6, fill: COLORS.ink, leading: 1.22 }));
  parts.push("</svg>");
  return parts.join("\n");
}

function table(map) {
  return Object.entries(mapObject(map)).map(([key, value]) => `| ${key} | ${value} |`).join("\n");
}

function validationReport(display, inputPath) {
  const v = display.validation;
  return [
    "# Figure 3 Sankey validation",
    "",
    `Input: ${path.relative(ROOT, inputPath)}`,
    "",
    "## Required isolate counts",
    "",
    `- Total isolates: ${EXPECTED.totalIsolates}`,
    `- Carbapenemase-positive isolates: ${EXPECTED.carbapenemasePositiveIsolates}`,
    `- Carbapenemase-negative isolates: ${EXPECTED.carbapenemaseNegativeIsolates}`,
    `- Unique isolates included in Sankey: ${v.isolates.size}`,
    `- Total Sankey flows: ${EXPECTED.totalFlows}`,
    `- Dual-backbone isolates: ${EXPECTED.dualBackboneIsolates.join(", ")}`,
    "",
    "## Backbone conservation",
    "",
    "| Backbone | Incoming | Node value | Outgoing |",
    "| --- | ---: | ---: | ---: |",
    ...display.conservation.map((row) => `| ${row.id} | ${row.incoming} | ${row.node} | ${row.outgoing} |`),
    "",
    "## Backbone counts",
    "",
    "| Backbone | Count |",
    "| --- | ---: |",
    table(v.backbones),
    "",
    "## Carbapenemase counts",
    "",
    "| Carbapenemase | Count |",
    "| --- | ---: |",
    table(v.carbapenemases),
    "",
    "## Species counts",
    "",
    "| Species | Count |",
    "| --- | ---: |",
    table(v.species),
    "",
    "## Sequence type counts",
    "",
    "| Sequence type | Count |",
    "| --- | ---: |",
    table(v.st),
    "",
    "Validation status: passed.",
    "",
  ].join("\n");
}

function writeFlowTable(display) {
  const rows = ["layer\tsource\ttarget\tbackbone\tvalue"];
  for (const flow of display.flowRows) {
    rows.push([flow.layer, flow.source, flow.target, flow.backbone, flow.value].join("\t"));
  }
  return rows.join("\n") + "\n";
}

function tryExportStatic(svgPath, outDir) {
  const rsvg = spawnSync("rsvg-convert", ["--version"], { encoding: "utf8" });
  if (rsvg.status !== 0) {
    return "Static PDF/PNG export skipped because rsvg-convert was not found.";
  }
  const pdf = path.join(outDir, `${STEM}.pdf`);
  const png = path.join(outDir, `${STEM}_600dpi.png`);
  const pdfRun = spawnSync("rsvg-convert", ["-f", "pdf", "-o", pdf, svgPath], { encoding: "utf8" });
  const pngRun = spawnSync("rsvg-convert", ["-w", String(W * 6), "-h", String(H * 6), "-o", png, svgPath], { encoding: "utf8" });
  if (pdfRun.status !== 0 || pngRun.status !== 0) {
    throw new Error(`rsvg-convert failed. PDF stderr: ${pdfRun.stderr}. PNG stderr: ${pngRun.stderr}.`);
  }
  return `Static exports written: ${path.relative(ROOT, pdf)}, ${path.relative(ROOT, png)}`;
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  if (args.help) return;

  const rows = parseTsv(await fs.readFile(args.input, "utf8"));
  const display = buildDisplay(rows);
  const layout = buildLayout(display);
  const svg = renderSvg(display, layout);

  await fs.mkdir(args.outDir, { recursive: true });
  const svgPath = path.join(args.outDir, `${STEM}.svg`);
  await fs.writeFile(svgPath, svg, "utf8");
  await fs.writeFile(path.join(args.outDir, `${STEM}_validation.md`), validationReport(display, args.input), "utf8");
  await fs.writeFile(path.join(args.outDir, `${STEM}_display_flows.tsv`), writeFlowTable(display), "utf8");

  const messages = [
    "Figure 3 Sankey validation passed.",
    `SVG written: ${path.relative(ROOT, svgPath)}`,
    `Total flows: ${display.validation.isolates.size + EXPECTED.dualBackboneIsolates.length}`,
    `Unique isolates represented: ${display.validation.isolates.size}`,
    `Backbone counts: ${JSON.stringify(mapObject(display.validation.backbones))}`,
  ];
  if (args.exportStatic) messages.push(tryExportStatic(svgPath, args.outDir));
  console.log(messages.join("\n"));
}

main().catch((error) => {
  console.error(error.message);
  process.exitCode = 1;
});
