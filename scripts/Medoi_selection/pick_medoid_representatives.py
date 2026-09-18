#!/usr/bin/env python3
"""
Pick one representative per cluster using a medoid strategy on S2.

Inputs (expected in current working directory):
  - cluster_analysis/plasmid_cluster.tsv  (two columns: seq_id <TAB> cluster_id)
  - pairwise_long.tsv                     (tabular with headers including:
                                           q, s, pid_weighted, pid_hspmax,
                                           cov_q, cov_s, S2, hitlen_bp, len_sim)
  - len_orig.tsv                          (seq_id <TAB> original_length_bp)
  - all_plasmids.fa                       (FASTA with the renamed IDs)

Outputs:
  - cluster_representatives_medoid.tsv    (cluster_id,rep_id,score,sum_pairs,cluster_size,rep_length_bp,median_len_bp,max_pid_hspmax)
  - representatives_medoid.fa             (FASTA of chosen representatives)

Run:
  python pick_medoid_representatives.py
"""

import sys
import csv
from collections import defaultdict, Counter
from statistics import median
from pathlib import Path

# ---------- Configurable thresholds (kept here for transparency) ----------
MIN_ALN_BP = 3000       # ignore pairs with too little aligned bases
MIN_LEN_SIM = 0.88      # ignore pairs with strong length mismatch

# ---------- Paths ----------
base = Path(".")
clusters_tsv = base / "cluster_analysis" / "plasmid_cluster.tsv"
pairwise_tsv = base / "pairwise_long.tsv"
len_tsv      = base / "len_orig.tsv"
all_fa       = base / "all_plasmids.fa"

out_table = base / "cluster_representatives_medoid.tsv"
out_fa    = base / "representatives_medoid.fa"

# ---------- Load cluster membership ----------
cluster_of = {}               # seq_id -> cluster_id
members_by_cluster = defaultdict(list)

with clusters_tsv.open() as f:
    for row in csv.reader(f, delimiter="\t"):
        if not row or len(row) < 2:
            continue
        sid, cid = row[0], row[1]
        cluster_of[sid] = cid
        members_by_cluster[cid].append(sid)

# ---------- Load lengths ----------
length_bp = {}
with len_tsv.open() as f:
    for row in csv.reader(f, delimiter="\t"):
        if not row or len(row) < 2:
            continue
        sid, lbp = row[0], row[1]
        try:
            length_bp[sid] = int(lbp)
        except ValueError:
            pass

# ---------- Load pairwise stats ----------
# We will store, for within-cluster pairs, the S2 and pid_hspmax that pass filters.
S2 = defaultdict(dict)        # S2[a][b] = value (symmetric)
PIDMAX = defaultdict(dict)    # pid_hspmax[a][b] (symmetric)

# Identify column indices from header
with pairwise_tsv.open() as f:
    header = f.readline().rstrip("\n").split("\t")
    idx = {name: i for i, name in enumerate(header)}
    required = ["q", "s", "S2", "hitlen_bp", "len_sim", "pid_hspmax"]
    for r in required:
        if r not in idx:
            sys.exit(f"[ERROR] Column '{r}' not found in {pairwise_tsv}")

    for line in f:
        parts = line.rstrip("\n").split("\t")
        if len(parts) < len(header):
            continue
        q = parts[idx["q"]]
        s = parts[idx["s"]]
        # Only consider pairs inside the same cluster
        cq = cluster_of.get(q)
        cs = cluster_of.get(s)
        if not cq or not cs or cq != cs or q == s:
            continue

        try:
            s2 = float(parts[idx["S2"]])
            hb = float(parts[idx["hitlen_bp"]])
            ls = float(parts[idx["len_sim"]])
            pm = float(parts[idx["pid_hspmax"]])
        except ValueError:
            continue

        # Pair-wise quality gate
        if hb < MIN_ALN_BP or ls < MIN_LEN_SIM:
            continue

        a, b = (q, s) if q < s else (s, q)
        S2[a][b] = s2
        S2[b][a] = s2
        PIDMAX[a][b] = pm
        PIDMAX[b][a] = pm

# ---------- Scoring: sum of S2 to other members (passing gates) ----------
def pick_representative(cluster_id, members):
    # Precompute median length for tiebreak
    lens = [length_bp.get(m, 0) for m in members]
    med_len = int(median([l for l in lens if l > 0])) if any(l > 0 for l in lens) else 0

    best = None
    for m in members:
        # Sum S2 only over members with a valid, gated S2
        s2_sum = 0.0
        pairs_used = 0
        for n in members:
            if n == m:
                continue
            val = S2[m].get(n)
            if val is not None:
                s2_sum += val
                pairs_used += 1

        # Tiebreakers:
        # 1) length closeness to cluster median
        mlen = length_bp.get(m, 0)
        len_dev = abs(mlen - med_len) if med_len > 0 and mlen > 0 else float("inf")

        # 2) strongest max pid_hspmax against cluster peers
        max_pm = 0.0
        for n in members:
            if n == m:
                continue
            pm = PIDMAX[m].get(n, 0.0)
            if pm > max_pm:
                max_pm = pm

        candidate = (s2_sum, -pairs_used, len_dev, -max_pm, m)  # we want max s2_sum, max pairs, min len_dev, max pidmax, then ID
        if best is None or candidate > best[0]:
            best = (candidate, m, s2_sum, pairs_used, mlen, med_len, max_pm)

    if best is None:
        # Fallback: cluster with single member or no usable pairs
        # choose the lexicographically smallest ID, length as reported
        m = sorted(members)[0]
        mlen = length_bp.get(m, 0)
        return m, 0.0, 0, mlen, (int(median([length_bp.get(x, 0) for x in members])) if members else 0), 0.0

    _, rep, s2_sum, pairs_used, mlen, med_len, max_pm = best
    return rep, s2_sum, pairs_used, mlen, med_len, max_pm

# ---------- Compute representatives ----------
rows = []
for cid, members in sorted(members_by_cluster.items(), key=lambda x: x[0]):
    rep, s2_sum, pairs_used, mlen, med_len, max_pm = pick_representative(cid, members)
    rows.append({
        "cluster_id": cid,
        "rep_id": rep,
        "score_sum_S2": f"{s2_sum:.6f}",
        "sum_pairs_used": pairs_used,
        "cluster_size": len(members),
        "rep_length_bp": mlen,
        "cluster_median_len_bp": med_len,
        "rep_max_pid_hspmax": f"{max_pm:.3f}",
    })

# ---------- Write table ----------
with out_table.open("w", newline="") as f:
    w = csv.DictWriter(f, delimiter="\t", fieldnames=[
        "cluster_id","rep_id","score_sum_S2","sum_pairs_used","cluster_size",
        "rep_length_bp","cluster_median_len_bp","rep_max_pid_hspmax"
    ])
    w.writeheader()
    for r in rows:
        w.writerow(r)

# ---------- Write FASTA of representatives ----------
want = {r["rep_id"] for r in rows}
seqs = {}

# Stream FASTA without loading everything if file is large
def fasta_iter(path):
    with path.open() as fh:
        header = None
        seq = []
        for line in fh:
            if line.startswith(">"):
                if header is not None:
                    yield header, "".join(seq)
                header = line.strip()[1:].split()[0]
                seq = []
            else:
                seq.append(line.strip())
        if header is not None:
            yield header, "".join(seq)

with out_fa.open("w") as out:
    for h, s in fasta_iter(all_fa):
        if h in want:
            out.write(f">{h}\n")
            # wrap to 80 for readability
            for i in range(0, len(s), 80):
                out.write(s[i:i+80] + "\n")

print(f"[OK] Wrote {out_table}")
print(f"[OK] Wrote {out_fa}")
