#!/bin/bash
# Build .docx via Pandoc from manuscript_master.md
# Usage: bash analysis_v2/build_docx.sh
set -e

ROOT="$(cd "$(dirname "$0")"/.. && pwd)"
SRC="$ROOT/analysis_v2/reports/manuscript_master.md"
OUT_DIR="$ROOT/coursework"
mkdir -p "$OUT_DIR"
OUT="$OUT_DIR/coursework_draft.docx"

# Rebuild manuscript_master.md first to pick up latest chapter edits
bash "$ROOT/analysis_v2/build_manuscript.sh" > /dev/null

TEMPLATE="$ROOT/coursework/hse_template.docx"
REF_DOC_FLAG=""
if [ -f "$TEMPLATE" ]; then
    REF_DOC_FLAG="--reference-doc=$TEMPLATE"
fi

pandoc "$SRC" \
    -o "$OUT" \
    --from=markdown+tex_math_dollars+raw_tex \
    --to=docx \
    -V lang=ru \
    --standalone \
    --resource-path="$ROOT/analysis_v2/reports:$ROOT/analysis_v2/output/figures:$ROOT" \
    $REF_DOC_FLAG

echo "Built: $OUT ($(du -h "$OUT" | cut -f1))"
echo "Sha256: $(shasum -a 256 "$OUT" | cut -d' ' -f1)"
