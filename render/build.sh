#!/usr/bin/env bash
# Standing Water render pipeline.
#
#   bash render/build.sh            # edition, then facsimile, then flipbook
#   bash render/build.sh edition    # clean, selectable, printable
#   bash render/build.sh facsimile  # the same pages aged into a handled book
#   bash render/build.sh flip       # the book bundles the Android app reads
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
  # 400 dpi, not 200. At 200 the facsimile held 1100 px per page, and a leaf
  # on the tablet is about 880 device px - so there was 1.2x of real detail
  # and nothing to magnify. 400 gives 2200 px and 2.5x, which is what makes
  # a loupe worth having, and it also sharpens ordinary reading because the
  # page is now supersampled rather than merely matched to the screen.
  #
  # Costs: about 3m45s for the book instead of a minute, and a 56 MB pdf
  # instead of 19 MB. The ink effects in age.py scale with dpi (TUNED_DPI),
  # so the press still looks like the same press.
  #
  # The ceiling above this is the PAPER: cover art/blank pages holds
  # photographed sheets 1070 px wide, already upscaled 2x at 400 dpi. Going
  # to 600 would sharpen the type and visibly smear the foxing.
  # Re-photographing those sheets is what would unlock more.
  python scripts/age.py out/standing-water-edition.pdf \
      out/standing-water-facsimile.pdf --dpi 400 --age 1.1 \
      "${pargs[@]}" "${@}" || return 1
}

build_flip() {
  [ -f out/standing-water-facsimile.pdf ] || build_facsimile || return 1

  # One bundle per book, and the reader knows nothing else about them.
  #
  # Only the facsimile. The clean edition was bundled here for a while to
  # prove the shelf held more than one book; it is not a book anybody wants
  # to read, and two cards with the same cover and the same title are a shelf
  # you have to guess at. Any PDF can be added back as a bundle at any time
  # without touching this file — see build_bundle.py.
  echo "== bundles =="
  python scripts/build_bundle.py out/standing-water-facsimile.pdf ../books \
      --id standing-water --title "Standing Water" \
      --subtitle "Of Roots, Reflections, and the Faces Beneath" \
      --boards "../cover art/cover.png" --width 2200 || return 1

  # Launcher icons for the app. Generated rather than only committed so a
  # fresh clone can build an apk without a preliminary step.
  if [ -d ../app/android/app/src/main/res ]; then
    echo "== icons =="
    python scripts/build_icons.py --android ../app/android/app/src/main/res \
      || return 1
  fi

  echo
  echo "   Bundles are in books/. Put them on the tablet with:"
  echo "     launch/Push books.cmd"
}

case "$TARGET" in
  edition)   build_edition ;;
  facsimile) shift || true; build_facsimile "$@" ;;
  flip)      build_flip ;;
  all)       build_edition && build_facsimile && build_flip ;;
  *) echo "unknown target: $TARGET"; exit 2 ;;
esac
