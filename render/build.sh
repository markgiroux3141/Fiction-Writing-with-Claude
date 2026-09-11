#!/usr/bin/env bash
# Standing Water render pipeline.
#
#   bash render/build.sh            # edition, then facsimile, then flipbook
#   bash render/build.sh edition    # clean, selectable, printable
#   bash render/build.sh facsimile  # the same pages aged into a handled book
#   bash render/build.sh flip       # the two-page flipbook, from the facsimile
#
# Source of truth for the text: manuscript/ if it has anything in it, otherwise
# the highest-numbered draft in each stories/<nn>-<slug>/ directory. That way
# the pipeline runs against work in progress and does not wait on promotion.

set -uo pipefail
cd "$(dirname "$0")" || exit 1
TARGET="${1:-all}"
mkdir -p out plates

# Plates live outside the repo under generator filenames with spaces and
# commas in them, which graphicx handles badly. plates.json names the source
# for each slug; sync copies them in under clean names.
sync_plates() {
  python scripts/sync_plates.py || return 1
}

# Which file of each story the book is built from. scripts/sources.py picks
# the newest of manuscript/<slug>.md and the highest-numbered draft, and names
# its choice — a promoted copy left behind by continued revising used to win
# silently, and the build reported success while setting stale text.
collect_sources() {
  python scripts/sources.py
}

build_edition() {
  echo "== syncing plates =="
  sync_plates || return 1

  echo "== compiling body =="
  local -a units
  mapfile -t units < <(collect_sources)
  if [ ${#units[@]} -eq 0 ]; then echo "   no sources found"; return 1; fi
  python scripts/build_tex.py "${units[@]}" > out/body.tex || return 1

  echo "== xelatex (2 passes) =="
  for i in 1 2; do
    xelatex -interaction=batchmode -output-directory=out tex/edition.tex >/dev/null 2>&1
  done
  if [ ! -f out/edition.pdf ]; then
    echo "FAILED — last 30 lines of log:"; tail -30 out/edition.log; return 1
  fi
  # XeLaTeX emits a PDF from a document riddled with errors, so the existence
  # of out/edition.pdf proves nothing. Check the log.
  local nerr
  nerr=$(grep -cE '^! ' out/edition.log 2>/dev/null | tr -d '[:space:]')
  if [ "${nerr:-0}" -gt 0 ]; then
    echo "   $nerr LaTeX error(s):"
    grep -E '^! ' out/edition.log | sort -u | head -8 | sed 's/^/     /'
    echo "   (full log: render/out/edition.log)"
    return 1
  fi
  # The destination may be open in a viewer, which locks it on Windows.
  if ! cp -f out/edition.pdf out/standing-water-edition.pdf 2>/dev/null; then
    echo "   FAILED to write out/standing-water-edition.pdf — it is locked."
    echo "   Close it in any PDF viewer and re-run."
    return 1
  fi
  echo "   -> out/standing-water-edition.pdf ($(pdfinfo out/standing-water-edition.pdf 2>/dev/null | grep -i '^Pages' | tr -s ' ' | cut -d' ' -f2) pages)"
}

# Photographed sheets used as the page ground. render/paper/ wins if it
# exists; the scans currently live under "cover art/blank pages" because that
# is where they were first put, and they are not cover art.
paper_dir() {
  if compgen -G "paper/*.png" > /dev/null || compgen -G "paper/*.jpg" > /dev/null; then
    echo "paper"
  elif [ -d "../cover art/blank pages" ]; then
    echo "../cover art/blank pages"
  fi
}

build_facsimile() {
  [ -f out/standing-water-edition.pdf ] || build_edition || return 1
  echo "== ageing pass =="
  local pd; pd="$(paper_dir)"
  local -a pargs=()
  [ -n "$pd" ] && pargs=(--paper-dir "$pd")
  python scripts/age.py out/standing-water-edition.pdf \
      out/standing-water-facsimile.pdf --dpi 200 --age 1.1 \
      "${pargs[@]}" "${@}" || return 1
}

build_flip() {
  [ -f out/standing-water-facsimile.pdf ] || build_facsimile || return 1
  echo "== flipbook =="
  python scripts/build_flip.py out/standing-water-facsimile.pdf ../flip || return 1
}

case "$TARGET" in
  edition)   build_edition ;;
  facsimile) shift || true; build_facsimile "$@" ;;
  flip)      build_flip ;;
  all)       build_edition && build_facsimile && build_flip ;;
  *) echo "unknown target: $TARGET"; exit 2 ;;
esac
