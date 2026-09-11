# Render pipeline

Turns the drafts into three artifacts from one source.

| Target | Output | What it is |
|---|---|---|
| `edition` | `out/standing-water-edition.pdf` | Clean, selectable, printable. Real typography, no texture. |
| `facsimile` | `out/standing-water-facsimile.pdf` | The same pages aged into a handled book. Raster; text not selectable, which is correct for a scan. |
| `flip` | `../books/<id>/` | One bundle per book, for the Android app to read. |

```bash
bash render/build.sh            # all three
bash render/build.sh edition
bash render/build.sh facsimile
bash render/build.sh flip
```

Grown from the Necronomicon pipeline at `D:/Claude Code Projects/Necronomicon/render`.
`scripts/paper.py` is that project's, unchanged; `scripts/age.py` is that project's
with one substantive change (see **Finding the plates**). Everything else is new,
because the book is a different object — see **Typographic premise**.

---

## Typographic premise

**An illustrated collection of 1898, set in the Fell types.**

The Fell punches were acquired by Oxford in the 1670s and revived there in 1877, so
they were available in 1898 — but only at Oxford, and only for private press work. A
New Orleans trade book of that date would have been set in a Modern, and `oldstandard`
in `tex/faces/` is exactly that if the accurate choice is ever wanted back.

Fell is the deliberate anachronism. It is by a wide margin the oldest-looking of the
candidates, its outlines carry the original inking irregularities so the page looks
worn before anything ages it, and it takes the ageing pass better than a high-contrast
Modern, which loses its hairlines under ink spread. It also has a real small-capitals
cut. Compare for yourself: `render/out/faces/00-specimens.pdf` is the same aged page set
five ways.

**`Scale = 1.07`.** Fell English was cut for about 14pt, so at the document's 11pt it
sets below its optical size — small, tight, and about 66 characters to the line on this
measure. A seventh larger brings it to about 58, which is where a Fell page actually
sits, and it stops the measure forcing hyphenation on short words.

The face has no bold, and neither does the design: emphasis is italic, headings are
letterspaced capitals. `\ls{n}{...}` letterspaces anything. `\caps` is small capitals —
the real cut where a face has one, and otherwise uppercase at 82% of the current size,
letterspaced.

Trim is 5.5 × 8.25 in. Folio in the outer corner of the head, running title centred.

### Changing the face

```bash
python render/scripts/set_face.py --list
python render/scripts/set_face.py goudy
bash render/build.sh
```

`tex/faces/<name>.tex` sets the main font and, where the face has a real small-capitals
cut, points `\caps` at it. `set_face.py` copies the chosen one to `tex/face.tex`, which
the preamble inputs; with no such file the preamble falls back to Old Standard.

On disk: `fell` (in use), `goudy` (Goudy Old Style 1915, real small caps, the balanced
choice), `oldstandard` (the historically correct Modern), `caslon` and `baskerville` —
both of which are drawn for screens and set far too large at 11pt. They would need a
`Scale` well below 1 before they could be judged fairly.

**Note on `\caps`.** `@size` is a bare number, not a length, so `0.82@size` expands
to something like `0.8210.95` and XeTeX reports *Illegal unit of measure*. It has to go
through a length register first. The definition in `tex/preamble.tex` does.

## Text

`scripts/build_tex.py` compiles story Markdown into the body TeX:

```bash
python scripts/build_tex.py <story.md> [<story.md> ...] > out/body.tex
```

### Which file each story is built from

`scripts/sources.py` decides, and the build prints its choice for every story:

```
   01-the-game/  <-  draft-03.md (newer than the manuscript copy, which is behind)
```

**The newest file wins** between `manuscript/<slug>.md` and the highest-numbered
`stories/<slug>/draft-NN.md`. The rule used to be "manuscript wins if it exists at
all", which is the obvious reading of a promoted-work directory and is wrong in exactly
one common case: a story is promoted, revising continues, and every build after that
quietly sets the promoted copy. That happened — a manuscript holding draft 01 shadowed
drafts 02 and 03, and the build reported success and the right unit count each time.
Nothing in the output said which text it had used, which is why it now always does.

A promoted story whose draft directory has gone away is still included.

**The promoted copy is matched to its folder by front matter, not by filename.** The
manuscript file is named for the title, and a title chosen after the folder was made
leaves the two disagreeing — `The Long Way Round` is promoted out of
`stories/03-ti-jean/` as `manuscript/03-the-long-way-round.md`. Matching on the
filename then found no promoted copy for the folder *and* no folder for the promoted
copy, so the story went into the book twice, once from each, and the build called it
two units and reported success. `slug:` in the front matter is the story's identity;
the filename is a label.

Front-matter scalars end at an unquoted ` #`, as YAML does. The drafts annotate their
front matter freely, and `title: The Long Way Round   # chosen by Mark, 2026-09-10`
set the comment as part of the title on the printed page until the parser stripped it.

There is no editorial apparatus, no line numbering and no `reledmac`. This is a trade
collection, not a critical edition, and the whole scholarly machinery that carries the
Necronomicon would read here as a different and much sillier book.

Handled: YAML front matter (`title`), `<!-- comments -->` dropped so working notes
never reach the page, `---` alone on a line as a scene break, `*italic*`,
`**bold**` → letterspaced small capitals, paragraphs.

The first paragraph of each story and of each scene opens with a two-line drop capital
and runs its first three or four words on in small capitals, stopping at the first
comma so the caps never run past a clause. Anything standing before the initial — an
opening quote, if the scene begins on speech — is set ahead of the drop capital. It
used to be captured by the regex and then dropped, so a scene opening on dialogue lost
its quote mark with nothing said; neither story in the book does that yet, which is
the only reason it was never seen.

### Encoding

`build_tex.py` forces UTF-8 on stdout. It has to. The body is emitted on stdout and
redirected into `out/body.tex` by `build.sh`, and on Windows Python otherwise encodes
stdout in the console codepage — cp1252 here — so every em dash was written as the
single byte `0x97`. XeLaTeX reads UTF-8, in which `0x97` is not a valid start byte, and
it neither errors nor stops: the dashes simply came out as garbage glyphs mid-sentence
and the build reported success.

Anything else that writes a file in this pipeline passes `encoding="utf-8"` explicitly
for the same reason, and `sources.py` additionally forces LF line endings: it prints
paths that `build.sh` reads into a shell array with `mapfile`, and CRLF left a carriage
return on the end of every path, so each one failed to open with *Invalid argument*.

### Quotes

**Write the drafts with straight quotes. `build_tex.py` turns them, and the font must
never be left to do it.**

The faces are loaded with `Ligatures = TeX`, which switches on XeTeX's `tex-text`
mapping. That mapping rewrites a lone `"` as U+201D — a *closing* quote — because it
expects the old TeX input convention of `` `` `` and `''`. Nothing warns. The first
facsimile printed every quotation in the book opening with a closing mark, and it
survived a full read of the PDF because a wrong-facing quote looks like old
typography until you compare it with the mark at the other end of the sentence.

It is not a period convention. An 1898 trade octavo set `“` and `”` distinctly, and so
did the Fell types two centuries earlier. There are genuine conventions that look
strange now — an opening quote repeated at the head of every line of a long speech,
guillemets in French work — but an inverted opening mark is a fault in any century.

`quotes()` in `build_tex.py` decides each mark from its neighbours: a double quote
opens when what precedes it is nothing, space, an opening bracket or a dash **and**
what follows is not space, which is what keeps interrupted dialogue (`"I never—"`)
closing correctly. Single quotes all become apostrophes except one against the inside
of a double quote, so possessives, `o'clock`, `'em` and `'98` cannot be turned the
wrong way; genuine nested speech is the one case handled, and it is the one case that
is unambiguous.

`check_quotes()` warns on stderr — never stdout, which is the TeX — for any paragraph
with an odd number of quote marks, since that is exactly where the rule had to guess.
A continued speech that opens a paragraph without closing it would trip this
legitimately; if the book ever does that, relax the check then rather than now.

If the face is changed, confirm the new one carries U+2018/U+2019/U+201C/U+201D.
XeLaTeX logs a missing character as a warning and still reports a successful build.

## Plates

`plates.json` maps a story slug to a photograph. The key is the story's `slug:`
front-matter field — the folder name, not the manuscript filename:

```json
{ "_photos_root": "D:/Mark Backup/wet plate photography/enhanced",
  "01-the-game": { "src": "ChatGPT Image ....png", "file": "plate-01.jpg",
                   "numeral": "I", "caption": "...", "where": "before" } }
```

`scripts/sync_plates.py` resolves it, crops away the physical plate edge, runs it
through a period reproduction process, and writes JPEG into `plates/` under clean
names — the originals carry spaces and commas in their filenames, which `graphicx`
handles badly. Per-plate keys: `process`, `crop` (explicit `[l, t, r, b]` fractions),
`inset`, `process_args`.

### What the book prints

**The picture, not the plate.** What comes out of the image generator is a photograph
*of a wet-plate object* — hand-cut edges, collodion pour ridges, bare corners, varnish
crazing, the whole artifact on a copy stand. That is a museum scan, and it is a way of
looking at a 19th-century object that belongs entirely to the 21st. No process
available in 1898 could print any of it: the negative is masked to a rectangle in the
printing frame and every physical edge falls outside the image area.

`scripts/plate_process.py` crops it off and reproduces what is left. Two processes,
both correct for the date:

**`photogravure`** (default). Intaglio, continuous tone, no screen — the prestige
process, printed from etched copper on damp rag paper and tipped in on its own leaf.
Warm brown-black, no true black and no paper-white anywhere inside the image, aquatint
grain strongest in the midtones, and a **plate mark**: the embossed rectangle where the
edge of the copper bit into the paper. That mark is the single strongest signal that a
page was printed from an intaglio plate, and it is drawn as an emboss — a fine dark
trough with a fine light ridge outside it — because drawn as a plain rule it reads as
a border and convinces nobody.

**`mounted_print`** (in use). Not a printing process at all: an actual photographic
print, trimmed and pasted to the leaf by hand, one at a time. This is the older and
more expensive way an illustrated book carried a photograph, and it is why books of the
1870s and 1880s with real prints cost what they cost.

It differs from a gravure in what the reader is looking at. A gravure is ink *in* paper
and lies flat in the page. A pasted print is an **object on** the page: it has its own
edge, sits very slightly proud, was never quite square, and — the detail that dates a
genuine one — its chemistry bled into the mount over the following century and left a
halo. All three are rendered.

It deliberately adds **no photo corners**. Gummed corners are a snapshot-album
technology of roughly 1905 onward, twenty years late for this book, and they assert a
different frame: someone's album assembled by hand, rather than a published edition.
Corners and a plate mark cannot both be true on the same page.

**`as_is`** (in use). No reproduction process at all — the source image, whole, printed
**full bleed as the entire leaf**. For a source that is already a finished leaf: a print
on its own album mount, photographed, corners and all.

The route to that was two wrong turns, and both were the same mistake. First the whole
mount was centred on a page of the book's own paper — one sheet of paper laid on
another, and the join showed as a rectangle. Then the print was cropped out of its mount
and enlarged, which removed the second ground but also cut off the corners, which were
the point. The answer was neither: the photograph does not go *on* a leaf, it *is* the
leaf. `as_is` shaves a hair off each edge to lose the scan's white surround and
cover-crops to the trim aspect — never stretches, because a leaf stretched to a
different aspect skews everything printed on it — and `\platefull` prints it to the
paper edge.

A full-bleed plate carries **no numeral and no caption**: there is no margin left to set
one in.

**`halftone`**. Screened relief, the new process in 1898 and the one taking over trade
publishing, because it printed on the same press as the type. Visible dot screen,
range flattened at both ends, shadows blocking up.

Two things worth knowing before switching to it:

- **The dot follows the area law.** Coverage is `pi*r^2`, so `r = sqrt(c/pi)`. Taking
  the radius as `sqrt(coverage)` — the obvious-looking form, and the first version
  here — overinks by a factor of pi: mid grey printed at 78% coverage and the plate
  went to mud.
- **It does not survive this pipeline unchanged.** A screen is a high-frequency
  pattern, and the facsimile rasterizes at 200 dpi while the screen is built for the
  plate's own ~235 ppi, so it aliases. Photogravure is continuous tone and comes
  through the raster-and-downsample chain intact. Using halftone properly means
  screening at the final raster as the last step, not here.

Neither process ages the photograph. The image is already an aged object, and
`age.py` leaves plate leaves alone for the same reason.

The **cover** is the exception: a mounted albumen print set into a board *is* the
physical object, so it keeps its edges.

### Full-bleed plates, and why they are not aged

`age.py` passes plate leaves through **untouched**. Every plate here is a photograph of
a leaf that is already an aged object, with its own paper, its own tone and its own
damage, so there is nothing for the ageing pass to add and everything it might add is a
second copy of something already there.

An earlier version multiplied the book's paper over the plate page so the mount would
match the text block, which was right while the plate was a small image centred on a
leaf of the book's own paper. Once the photograph became the whole leaf it was a second
sheet laid over the first, and it showed: the plate came out visibly darker and browner
than the photograph it was made from.

### Placement and the height cap

The `\plate` height cap is load-bearing, not taste. The plate, its caption and the
`fill` above and below have to fit one `	extheight`. At `0.80` they did not: the box
spilled onto the following recto, `\cleardoublepage` then pushed the story a further
leaf on, and it no longer faced its plate — with no error and no warning that named the
cause. **If a plate is ever enlarged, check that the story still opens on the recto
opposite it.**


A plate is tipped in **facing** the story it belongs to, which means it prints on a
**verso**. `\plate` lands on a recto, leaves that recto blank (it is the back of the
inserted leaf), prints the plate on the verso, and the story then opens on the recto
opposite. The obvious reading of "its own leaf" — putting the plate on a recto — leaves
a blank page between the photograph and the story it is of, which is what the first
version did.

The frontispiece is the exception. `\frontispieceplate` prints on the verso
immediately after the half-title with no inserted blank and no caption, so that it
faces the title page.

## Ageing

`scripts/age.py` is a pure post-process, so typography is never compromised to serve
texture. Per page: rasterize, lift the ink and vary its density with low-frequency
noise plus a roller band, spread it slightly, multiply over a freshly generated sheet
(`scripts/paper.py`, fractal noise, no bitmap assets), bleed a faint mirror of the
previous page through, and drift the sheet a fraction of a degree.

```bash
python scripts/age.py in.pdf out.pdf --dpi 200 --age 1.1 --pages 5-8
```

`--age` scales foxing, mottle, edge tanning and damp staining. `--pages` limits the
range, which is how to iterate without waiting on the whole book.

`--fade` sets how deep the under-inking goes. The density field is normalised on every
page, so it spans the same range each time and the roller band takes another tenth off
in places: the faintest type is a fact about every page rather than an occasional
accident, and at the full starve it fell to 0.56 of density — the stroke cores of the
lightest passages came out at luminance 97 against paper at 206, which is a passage the
reader has to work at. **0.5, the default, halves the starving**: the faintest cores
print at 63, about 0.8 of full density, and the pattern of variation is unchanged, only
shallower. Only the starved side is pulled back — the field runs above full density too,
and nothing above 1.0 is rescaled, so the heavy passages are exactly as they were and no
page comes out darker than before. `--fade 1.0` restores the old depth, `--fade 0` inks
the forme evenly.

### The ground: photographed paper

`scripts/paper.py` builds a sheet out of fractal noise. It is good at what noise is
good at — broad mottle, fibre, an even scatter of foxing — and it cannot do the things
that actually make old paper look old: a stain with a hard tide line and a soft centre,
damage that clusters, a sheet that remembers being folded.

`scripts/paper_scan.py` uses photographs of real sheets instead. `build.sh` picks them
up automatically from `render/paper/`, falling back to `cover art/blank pages/`, and
falls back again to procedural paper if neither has anything in it.

Two things have to be imposed on a scan, because a photograph of a sheet does not know
it is a page in a bound book:

**The gutter edge does not exist.** In a bound book you see the fore-edge, the head and
the tail. You never see the spine edge of the leaf — it is sewn into the binding. A
scan with four ragged, darkened, torn edges reads as a loose leaf lying on a table, and
in a two-page spread two of those ragged edges meet in the middle of the book, which
nothing bound has ever looked like. So the scan is cropped 5.5% **into** the leaf, all
four edges are thrown away, and the directional tanning is put back procedurally:
heaviest at the fore-edge, clean at the gutter, with a thumb-grime bloom in the outer
corner where a reader's hand actually lands.

**A leaf has two sides.** Pages 3 and 4 are the same piece of paper, so the verso is the
recto mirrored, with the gutter and the tanning reversed. This halves how many scans are
needed and is the detail that makes a repeated sheet read as a book rather than as a
repeat. A slow per-page tonal drift breaks the recurrence further.

#### What to generate

| | |
|---|---|
| **Aspect** | Match the trim, currently 1:1.5. The scans in hand are 1:1.374 and lose 8% to the cover-crop — the build reports this per sheet. |
| **Size** | ~2000 × 3000. The 5.5% inset leaves ~1780px across a 5.5in page, about 320 ppi, enough for a 300 dpi printable facsimile. 1070px is 195 ppi and is already being upscaled by the 200 dpi ageing pass. |
| **Count** | 16 or so, not one per page. With the recto/verso mirroring one sheet covers a whole leaf, so 16 sheets recur about every 32 pages — further apart than a reader holds in memory. |
| **Content** | Interior only: stains with hard tide lines, foxing clusters, fold creases, damp mottle, fibre. **Not** torn or deckled edges — they are cropped off, and effort spent on them is wasted. |

### Finding the plates

**By continuous tone, not by saturation** — the one substantive change from the
Necronomicon's `age.py`. That book tested colour saturation, because every plate in it
was a warm sepia and every text page was neutral. Here the plates are wet-plate
collodion and several are all but neutral grey; the sheet on the staircase has almost
no saturation at all, and the saturation test sent it through the ink-and-rag-paper
pass as though it were type.

`is_plate()` now measures the fraction of pixels in the midtones. A text page is white
with a few per cent of near-black ink and a thin antialiased fringe, and almost nothing
in between; a photograph fills half the leaf with midtones. No manifest, no page
numbers, no extra pass.

Plates get a lighter treatment (`age_plate_page`): the sheet pulled to the same cream
as the rag paper, a faint broad tone, a darkened extreme edge, and a fraction of a
degree of rotation because it was tipped in by hand. No foxing, no fibre, no
show-through in either direction.

## The reader, and the book format

`flip/` is a reader, not a book. It knows about **bundles**, and nothing about
Standing Water in particular.

```
books/<id>/book.json
books/<id>/pages/0001.jpg ...
```

`book.json` is the entire contract:

```json
{ "schema": 1, "id": "standing-water", "title": "Standing Water",
  "subtitle": "Of Roots, Reflections, and the Faces Beneath",
  "pageWidth": 2200, "pageHeight": 3300,
  "spread": true, "showCover": true,
  "cover": "pages/0001.jpg", "count": 46, "pages": ["pages/0001.jpg", "..."] }
```

`spread: false` reads one leaf at a time instead of a two-page spread — right for
a five-page story, wrong for a bound volume. It is a hand-editable field: flipping it
in `book.json` and reopening the app is the whole change, no rebuild.

**`id` must be stable across rebuilds.** Last-read position and, later, bookmarks hang
off it; changing it orphans the reader's place silently.

`scripts/build_bundle.py` makes a bundle from **any** PDF, not only ours:

```bash
python scripts/build_bundle.py <any.pdf> ../books     --id august-heat --title "August Heat" --subtitle "W. F. Harvey, 1910"
```

### Books from elsewhere

`build.sh flip` only builds Standing Water, because that is the only book this repo
writes. Anything else is imported once, by hand, and then simply lives in `books/`.
The Necronomicon — a different project's facsimile, at
`D:/Claude Code Projects/Necronomicon/render/out/` — went in with:

```bash
python scripts/build_bundle.py     "D:/Claude Code Projects/Necronomicon/render/out/necronomicon-facsimile.pdf"     ../books --id necronomicon --title "The Necronomicon"     --subtitle "The Book of the Finishing and the Remainder - Marsh, 1881"     --author "Rev. Josiah Ellwood Marsh, M.A. (ed.)"
```

188 leaves, 38 MB, twenty seconds. Its first page is a tipped-in plate photographing the
volume itself, which makes an unusually good shelf thumbnail, and it needs no `--boards`
because it does not open on one.

**188 pages turned out to be fine, and I had expected it not to be.** The reasoning that
said a book this long would need lazy loading was wrong: `ImagePageCollection.load()`
does set `.src` on every image at once, but that only holds the *encoded* JPEG — Chrome
decodes on draw and evicts under pressure, so the decoded-bitmap arithmetic that
predicted over a gigabyte never happens. Measured on the tablet with the whole book
open: 36 MB native heap, 136 MB of GL texture (the canvas, independent of page count),
a two-second open and clean turns. Lazy loading is still the right answer eventually;
it is not needed at two hundred pages.

### The loupe

`M`, or the glass in the bar. A brass magnifier follows the finger; the page turns are
suspended while it is up, because the layer that tracks the finger takes the pointer.

**It magnifies the page image, not the screen.** page-flip's canvas backing store is
sized in CSS pixels with no device-pixel scaling, so it is *lower* resolution than the
display — sampling it would have magnified a downsample. The lens is instead a circular
window onto the page JPEG at 2200 px, positioned so the point under the glass sits at
the aperture's centre. At 1.75× that works out to 1.43 source pixels per device pixel:
the magnification is real, not interpolated, which is the whole reason the ageing pass
moved to 400 dpi.

The artwork is `cover art/magnifying glass short handle.png`, used **whole**. Its lens
aperture was measured by flood-filling the alpha channel from the border — whatever
transparent pixels are left enclosed *are* the aperture — giving centre (49.94%, 28.17%)
and radius 42.42% of the width. Those numbers are in `app.js`, and the CSS
`transform-origin` must match them or the glass rotates off its own lens.

Three things that had to be got right, each of which looked like a different bug:

- **The glass is sized by its lens, not by its width.** The first artwork was 39% lens
  by width and this one is 85%; sizing by width made the second one taller than the
  screen. The aperture is what the reader looks through, so that is the dimension that
  is held constant (250 px) when the artwork changes.
- **The artwork is never cropped.** The long-handled version was cropped to keep it on
  screen, which cut through the middle of the handle — and the straight cut edge read
  exactly like the glass being clipped by the display.
- **The box is square and centred on the lens**, sized to twice the distance from the
  lens centre to the furthest corner of the artwork. Rotating the handle south-east
  swings the image outside a box cut to the artwork's own proportions, and the
  `filter` on that box clips to its region.

The handle hangs south-east and the finger grips near its end, so the lens rides up and
to the left of the hand — a magnifier held any other way has your own knuckles in it.
One consequence of the geometry: the lens centre cannot go above about 145 px from the
top of the screen without the brass rim leaving it, which on this trim is the running
head and the folio.

### Resolution, and the chain of ceilings

Every rasterization in the pipeline is a ceiling, and for a long time two of them were
set too low:

```
drafts  →  edition.pdf      vector, lossless
        →  facsimile.pdf    age.py --dpi 400   → 2200 px per page
        →  bundle           build_bundle --width 2200 (dpi derived) → 2200 px
        →  screen           ~880 device px per leaf on the Tab S10 Lite
```

That leaves **2.5× of real detail** above what the screen shows — which is what a
magnifier can draw on, and it also makes ordinary reading sharper, because the page is
now supersampled rather than merely matched.

Two bugs were in the way. `age.py` ran at 200 dpi, giving 1100 px per page against 880
device px: 1.2× headroom, nothing to magnify. And `build_bundle.py` hardcoded **150 dpi**
and then resized *up* to the target width — on a 5.5-inch page that is 825 px stretched
to 1100, so every page in every bundle carried a third fewer pixels than it claimed.
Upscaling also injects interpolation noise that JPEG spends bytes on, so the pages were
softer *and* larger: fixing it made the Necronomicon 25% more pixels for 40% fewer bytes.
`build_bundle.py` now derives the dpi from the trim and never resamples.

Measured cost of 400 dpi, on the device, with the whole book open:

| | 200 dpi / 1100 px | 400 dpi / 2200 px |
|---|---|---|
| facsimile PDF | 19 MB | 56 MB |
| ageing pass | ~1 min | 3 min 45 s |
| bundle | 12.9 MB | 37.2 MB |
| open the book | — | 426 ms |
| page turn | 908 ms (850 ms is the animation) | 908 ms — unchanged |
| native heap | 34 MB | 34 MB — unchanged |
| GL texture | 136 MB | 207 MB |

**The next ceiling is the paper, not the type.** `cover art/blank pages` holds two
photographed sheets 1070 px wide, and `paper_scan.py` resizes them to the page — so at
400 dpi the paper is already upscaled 2×. Going to 600 would sharpen the type and
visibly smear the foxing. Re-photographing those sheets is what would unlock more, not
a higher `--dpi`.

**The ink effects scale with dpi now.** They are measured in pixels and were tuned at
200, so without scaling the bite of the type and the show-through would tighten as the
resolution rose and a 400 dpi facsimile would stop looking like the same press. See
`TUNED_DPI` in `age.py`.

### Why the PDF is not read directly

It could be, and it should not be. The ageing pass rasterizes every page to a 200 dpi
image and wraps it in PDF, so a PDF engine in the app would parse a container, decode a
print-resolution raster, and hand back exactly the JPEG a bundle ships anyway — at three
times the pixels a tablet leaf can show, plus the engine's memory. Preprocessing is
strictly cheaper. It also keeps a PDF engine out of the app, so adding pdf.js later for
drop-in PDFs is a pure addition that converts to the same bundle format and rewrites
nothing.

### Where books live

Nothing is bundled into the APK. Every book is found at runtime in the app's own folder
on the device:

```
/sdcard/Android/data/com.standingwater.facsimile/files/books/<id>/
```

That directory needs **no storage permission**, is visible over USB and in My Files, and
is created on first run so there is always a real folder to drop a book into. The shelf
is simply whatever is in it: add a book by copying a directory, remove one by deleting
it. No rebuild, no reinstall.

```
launch\Push books.cmd            everything in books/
launch\Push books.cmd <id>       just that one
```

**The package id still says `standingwater`, deliberately.** It is invisible except in
that path, and changing it would make Android treat this as a different app — orphaning
every book already on the tablet.

**A reinstall empties the shelf.** `Android/data/<pkg>/` is app data, and replacing the
app clears it; the app then comes up saying *No books yet* and the books look lost rather
than deleted. `Build and install app.cmd` therefore pushes the library again on every
install rather than leaving it as a step to remember.

**The front board is page one of the PDF.** A book cannot really contain a photograph of
itself; this one does it anyway, because it is the fastest way to know which book you
have opened and the facsimile is the object people actually look at. `\coverleaf` prints
it full bleed with the inside of the board blank behind it.

**The back board is added here, not bound in.** They are not paper and
must not go through the ageing pass. The front board is `cover art/cover.png`, which is
already the page aspect exactly. The back board is derived from it: mirrored, its panel
emptied of the title and the mounted print and refilled with the cloth's own colour, a
generated weave, and the blind-stamped double rule a real back board carries. The
border, corners and edge wear are the front board's own.

The leaves between the two boards have to pair up: page-flip shows the first and last
alone, as a closed book does, so an odd number in between leaves one spread unmatched
and every spread after it off by one. The book's own last leaf is blank, so it is
duplicated as the pastedown inside the back board — both the fix and what is really
there.

The first version filled the back board's panel with the front board's **high-frequency
detail**,
on the theory that a high-pass keeps texture. A high-pass keeps *edges*, and the
strongest edges in that panel are the lettering and the print's border, so the back
board came out with a legible mirror-image "Standing Water" embossed across it. Bookcloth
at this scale is a fine weave, and a weave is cheaper to generate than to rescue.

**The book has no half-title and no frontispiece.** It opens on its title page, because
the flipbook puts the boards in front of that and a half-title between a cover and a
title page is a leaf the reader turns past without reading. Both were removed together,
which keeps the count even and the title page on a recto.

The viewer is [page-flip](https://github.com/Nodlik/StPageFlip) (MIT), vendored at
`flip/vendor/`. It draws leaf shadows but not the gutter — the trough between the two
leaves belongs to the binding rather than to either page — so `index.html` overlays
one, and fades it out while a leaf is in motion.

**It is patched.** page-flip's `clear()` filled its whole canvas white on every frame,
so any part of the stage no leaf covered came out as a slab of bright white paper — most
visibly beside the closed front board, which is the first thing anyone sees. It now
clears transparent, so the page ground shows through and a closed book sits on the table
it is on. The patch is one method, noted in a comment at the top of the vendored file,
and has to be reapplied if the vendor copy is ever updated.

**Sizing is page-flip's, not ours.** The viewer used to measure the viewport once at
load and build a `size: 'fixed'` book from it, so rotating a tablet or restoring the
window left the book at the old trim. It is now `size: 'stretch'` with `autoSize`, which
keeps the aspect with a percentage padding and rebinds itself on resize; CSS caps the
stage against the window's height as well as its width.

`?book=<id>` opens straight into one book and `#p=12` lands on a leaf — for checking a
single spread without walking the shelf to reach it.

**The book fills the height, and the controls float.** Reserving flow space for the bar
cost 104 px of book on every screen in order to show three buttons that a swipe makes
optional anyway, so the bar is now a `position: fixed` pill over the foot of the page
that withdraws after about four seconds and returns on any touch, move, key or page
turn. The overlay is `pointer-events: none` except the buttons themselves — otherwise it
swallowed drags on the bottom corners of the page, which is exactly where a reader grabs
a leaf. A spread is 4:3 and a tablet is 16:10, so filling the height means margins at
the sides; that trade is the point. `I` toggles an inset view that stands the book on
visible ground instead, `B` hides the controls for good, `F` is fullscreen.

### The Android app

**From a fresh clone**, once: `app/node_modules/` is not tracked, so Capacitor's CLI has
to be fetched before anything can sync.

```bash
cd app && npm ci        # or npm install
```

Then the ordinary loop, from the repo root:

```bash
bash render/build.sh                    # edition -> facsimile -> bundles
launch\Build and install app.cmd        # apk, install, and re-push the books
```


`app/` is a Capacitor project that wraps `flip/` — the reader, and nothing else — into
a real APK, served from `https://localhost`, Capacitor's internal origin. It needs no
cable, no server and no network, ever. 4.1 MB, because the books are not in it.

**There is no browser version.** The reader was briefly a PWA as well; that route is
gone, along with its service worker, web manifest and web icons. It could only ever
show books bundled into the page, since a browser cannot read the device's filesystem,
which is exactly the limitation the app does not have.

```
launch\Build and install app.cmd          build, then install over USB
launch\Build and install app.cmd build    build only
```

Verified on a Galaxy Tab S10 Lite (Android 16): launches on the closed front board,
fullscreen with no system bars, 46 pages from the APK, and `serviceWorkers: 0` — the
viewer detects `window.Capacitor` and skips registering its worker, because caching
assets that are already local just makes a second copy that can go stale against the
first.

Two things the wrapper needed beyond `cap add android`:

- **Immersive mode in `MainActivity.java`.** Android 15+ force apps edge-to-edge and
  ignore the old fullscreen flags, so the bars come off through
  `WindowInsetsControllerCompat`, with `BEHAVIOR_SHOW_TRANSIENT_BARS_BY_SWIPE` — a page
  turn *is* an edge swipe, and a reader who summoned the navigation bar every time they
  turned a leaf would stop turning leaves. Re-hidden on every focus gain.
- **Java.** Capacitor 8's Gradle plugin needs a JDK newer than 21 and the system JDK
  here is 17, so the build script points `JAVA_HOME` at the JDK that ships inside
  Android Studio rather than asking anyone to install a second one.

**The `Books` native plugin.** `BooksPlugin.java` lists the bundles in the app's own
external folder and returns each manifest plus its absolute path; the web side turns
that path into a loadable URL with `Capacitor.convertFileSrc`, so page images stay
ordinary `<img src>` streamed natively — no base64, no second copy of the book in
memory. Sixty lines of plain Java instead of `@capacitor/filesystem`, which is a much
larger dependency for three operations and which declares a Kotlin `jvmToolchain(21)` —
a hard requirement for a JDK that is not installed here. See the Java note in
`app/android/build.gradle`.

**Where the reader keeps its place.** `localStorage`, keyed by bundle id, holding the
last spread per book; the shelf card shows it as *at 12*. Named bookmarks are not built
yet — that is the next piece, and it belongs in the same record.

`launch\Build and install app.cmd` calls `gradlew.bat` by absolute path on purpose: this
machine has `NoDefaultCurrentDirectoryInExePath=1`, under which cmd will not find a
batch file sitting in the current directory, and the build dies claiming gradlew is not
a recognised command.

## Requirements

Verified on this machine: MiKTeX (XeLaTeX, `lettrine`, `fancyhdr`, `microtype`,
`fontspec`, `geometry`, `needspace`, `ragged2e`), Python 3.12 with Pillow, numpy and
`img2pdf`, poppler (`pdftoppm`, `pdfinfo`), ImageMagick 7.

Fonts in `fonts/` are OFL, fetched from `google/fonts`: **Old Standard** (body),
**Libre Caslon Text** (spare — see below).

---

## Open, and Mark's to settle

Nothing below blocks the pipeline; all of it changes what the book looks like.

0. **Which process the plates use.** Plate I is `as_is` — the photograph as supplied,
   corners and all, which makes the book an album of real prints. `mounted_print` and
   `photogravure` make it a published edition instead. One field per plate in
   `plates.json`, and all the plates should agree with each other.
2. **The imprint.** `tex/edition.tex` currently says New Orleans, 1898, "printed for
   the publishers". The date sets the register of everything: 1898 is a trade book,
   1878 is a subscription volume, 1912 is a reprint with worse paper.
3. **The frame.** `bible/book-bible.md` leaves this open — found album (a) or implicit
   (b). The title-page verso currently carries one unsigned line, which is Mark's
   leaning towards (b) and is one `\clearpage` from being cut.
4. **How much ageing.** Currently `--age 1.1` at 200 dpi. The foxing reads a little
   even and a little orange to me at that setting; `0.7` is a book that was shelved,
   `1.6` is a book that was in a barn.
5. **Photogravure or halftone.** Photogravure is the default and is the better
   picture; halftone is the likelier choice for a modest New Orleans imprint and needs
   the screening moved to the end of the pipeline before it can be used. One field per
   plate in `plates.json`.
6. **The cover.** `cover art/cover.png` is not in the build at all yet. The flipbook
   currently opens on the half-title; a real closed book opens on boards.
7. **A quote against a drop capital.** A scene opening on dialogue now sets its `“`
   ahead of the initial, which is correct and plain. The finer setting hangs it in the
   margin so the capital stays flush with the measure. Nothing in the book triggers it
   yet — the first story to open on speech will.
