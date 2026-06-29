#!/usr/bin/env bash

# Reference plasmid preparation and optional all-vs-all BLAST workflow.
# This script is path-safe: all inputs and outputs are supplied as arguments or
# through environment variables. It does not modify the curated reference FASTA
# collection.

set -u

ROOT="${ROOT:-$(pwd)}"
FASTADIR="${FASTADIR:-${ROOT}/data/plasmid_references/references_34}"
OUTDIR="${OUTDIR:-${ROOT}/validation/reference_plasmid_workflow}"
THREADS="${THREADS:-4}"

mkdir -p "${OUTDIR}/renamed_fastas" "${OUTDIR}/logs" "${OUTDIR}/blastdb"

missing=0
for tool in awk basename blastn makeblastdb; do
  if ! command -v "${tool}" >/dev/null 2>&1; then
    echo "[missing] ${tool}" >&2
    missing=1
  fi
done

if [ "${missing}" -ne 0 ]; then
  echo "Required command-line tools are missing. Install the environment before running the BLAST workflow." >&2
  false
else
  echo "[info] Input FASTA directory: ${FASTADIR}"
  echo "[info] Output directory: ${OUTDIR}"

  find "${OUTDIR}/renamed_fastas" -type f -name '*.renamed.fasta' -delete

  fasta_count=0
  for fasta in "${FASTADIR}"/*.fasta "${FASTADIR}"/*.fa "${FASTADIR}"/*.fna; do
    if [ ! -f "${fasta}" ]; then
      continue
    fi
    fasta_count=$((fasta_count + 1))
    base="$(basename "${fasta}")"
    prefix="${base%.*}"
    awk -v prefix="${prefix}" '
      BEGIN { n = 0 }
      /^>/ { n += 1; printf(">SEQ__%s__%05d\n", prefix, n); next }
      { print }
    ' "${fasta}" > "${OUTDIR}/renamed_fastas/${prefix}.renamed.fasta"
  done

  if [ "${fasta_count}" -ne 34 ]; then
    echo "[warning] Expected 34 FASTA files but found ${fasta_count}." >&2
  fi

  cat "${OUTDIR}"/renamed_fastas/*.renamed.fasta > "${OUTDIR}/all_plasmids.fa"
  awk '
    /^>/ {
      if (seq != "") { print header; print seq seq }
      header = $0; seq = ""; next
    }
    { seq = seq $0 }
    END { if (seq != "") { print header; print seq seq } }
  ' "${OUTDIR}/all_plasmids.fa" > "${OUTDIR}/all_plasmids_doubled.fa"

  awk '
    /^>/ {
      if (seq != "") print id "\t" length(seq)
      id = substr($0, 2); sub(/ .*/, "", id); seq = ""; next
    }
    { seq = seq $0 }
    END { if (seq != "") print id "\t" length(seq) }
  ' "${OUTDIR}/all_plasmids.fa" > "${OUTDIR}/len_orig.tsv"

  makeblastdb \
    -in "${OUTDIR}/all_plasmids_doubled.fa" \
    -dbtype nucl \
    -out "${OUTDIR}/blastdb/plasmids" \
    > "${OUTDIR}/logs/makeblastdb.log" 2>&1

  blastn \
    -query "${OUTDIR}/all_plasmids.fa" \
    -db "${OUTDIR}/blastdb/plasmids" \
    -task blastn \
    -evalue 1e-20 \
    -num_threads "${THREADS}" \
    -max_target_seqs 5000 \
    -outfmt '6 qseqid sseqid pident length qlen slen' \
    > "${OUTDIR}/blast_all_vs_all.tsv"

  echo "[ok] Wrote ${OUTDIR}/blast_all_vs_all.tsv"
fi
