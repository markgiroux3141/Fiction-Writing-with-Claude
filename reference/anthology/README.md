# Sixty-Two Ghost Stories — a reading anthology

`sixty-two-ghost-stories.pdf` — 1,222 pages, 539,912 words, 3.9 MB.

The best of `reference/texts`, lifted out of their parent volumes and set as one
book to be **read** rather than grepped. Everything else in `reference/` is a
lookup table; this is the opposite.

6×9, Libre Caslon Text over Old Standard, chronological by first publication,
62 PDF bookmarks and a linked contents page.

## What was left out, and why

- **The four in-copyright pieces** in `texts/additional/` — Bradbury's *The Small
  Assassin*, Jackson's *The Lottery*, Leiber's *Smoke Ghost*, Campbell's *Who Goes
  There?*. They are private reference copies of works Mark already holds and the
  manifest says not to redistribute them; a compiled volume is a step toward
  distribution, so they are out. Say the word and they go in — it is one line in
  `spec.py` each.
- **Whole novels and near-novels** kept for structure rather than pleasure:
  Oliphant's *A Beleaguered City*, Riddell's *The Uninhabited House*, the John
  Silence stories (in the reading map as a cautionary example).
- **The Gulf South shelf** — Cable, Hearn, Chopin, King, Dunbar-Nelson. Register
  and place, not horror. They belong in a second volume if one is wanted.
- **The craft essays** — M. R. James and Lovecraft on the form. Not stories.
- Lovecraft's *Cthulhu*, *Dunwich* and *Innsmouth*, the remaining Poe, the rest of
  Bierce, Saki, Freeman, Crawford and Onions. Good; not among the very best.

## Three manifest entries that turned out to be wrong

Found while locating stories, and **not yet corrected in `../texts/MANIFEST.md`**:

| Manifest claims | Actually |
|---|---|
| `gaskell__the-grey-woman-and-other-tales` contains *The Old Nurse's Story* | It does not. The volume is *The Grey Woman*, *Curious If True*, *Six Weeks at Heppenheim*, *Libbie Marsh's Three Eras*, *Christmas Storms and Sunshine*, *Hand and Heart*, *Bessy's Troubles at Home*, *Disappearances*. **The Old Nurse's Story is not in the library at all.** |
| `lefanu__ghostly-tales-v1`/`-v2` contain *Madam Crowl's Ghost* and *Squire Toby's Will* | They do not. v1 is *Schalken the Painter* + *Aungier Street*; v2 is *An Authentic Narrative of a Haunted House* + *Ultor De Lacy*. Both stories are missing from the library. |
| `maupassant__original-short-stories-v4-the-horla` contains *The Horla* | It contains *The Trip of the Horla*, an 1887 account of a balloon ascent. The real *Horla* is in `anthology__masterpieces-of-mystery-ghost-stories`, and that is the text used here. |

The reading map also lists Blackwood's *The Willows* as "not in the downloaded
volume; worth finding" — it has since been downloaded standalone, and is here.

## Rebuilding

```bash
cd reference/anthology
python build.py                                   # -> sixty-two-ghost-stories.tex
xelatex sixty-two-ghost-stories.tex               # x3, for TOC and bookmarks
```

Needs XeLaTeX and the fonts in `render/fonts/`.

| File | What it is |
|---|---|
| `spec.py` | the selection: source file, start line, end line, title, author, year |
| `extract.py` | slices each story out, strips Gutenberg and editorial matter, rebuilds paragraphs |
| `tex.py` | text → LaTeX (quotes, dashes, `_italics_`, escaping) plus the preamble |
| `build.py` | orders by year, emits the `.tex` |

Boundaries were resolved by grepping each volume's table of contents against its
body, then eyeballing the first and last paragraph of all 62 extractions. Add a
story by appending one row to `spec.py` and rerunning; the opening and closing
lines print on every run so a bad boundary shows up immediately.

## Contents

| Year | Story | Author | Words | Source |
|---|---|---|---|---|
| 1824 | Wandering Willie's Tale | Sir Walter Scott | 7,676 | `canon/anthology__great-short-stories-v2-ghost-stories.txt` |
| 1836 | La Morte Amoureuse | Théophile Gautier | 9,561 | `canon/anthology__great-short-stories-v2-ghost-stories.txt` |
| 1838 | Ligeia | Edgar Allan Poe | 6,045 | `canon/poe__works-raven-edition.txt` |
| 1839 | The Fall of the House of Usher | Edgar Allan Poe | 7,055 | `canon/poe__works-raven-edition.txt` |
| 1839 | Schalken the Painter | J. Sheridan Le Fanu | 7,348 | `canon/lefanu__ghostly-tales-v1.txt` |
| 1842 | The Masque of the Red Death | Edgar Allan Poe | 2,393 | `canon/poe__works-raven-edition.txt` |
| 1842 | The Pit and the Pendulum | Edgar Allan Poe | 6,050 | `canon/poe__works-raven-edition.txt` |
| 1843 | The Black Cat | Edgar Allan Poe | 3,848 | `canon/poe__works-raven-edition.txt` |
| 1843 | The Tell-Tale Heart | Edgar Allan Poe | 2,076 | `canon/poe__works-raven-edition.txt` |
| 1845 | The Facts in the Case of M. Valdemar | Edgar Allan Poe | 3,481 | `canon/poe__works-raven-edition.txt` |
| 1846 | The Cask of Amontillado | Edgar Allan Poe | 2,306 | `canon/poe__works-raven-edition.txt` |
| 1859 | The House and the Brain | Edward Bulwer-Lytton | 10,919 | `canon/anthology__great-short-stories-v2-ghost-stories.txt` |
| 1859 | What Was It? | Fitz-James O'Brien | 5,107 | `canon/anthology__famous-modern-ghost-stories.txt` |
| 1861 | The Grey Woman | Elizabeth Gaskell | 23,340 | `canon/gaskell__the-grey-woman-and-other-tales.txt` |
| 1866 | The Signal-Man | Charles Dickens | 5,077 | `canon/anthology__great-short-stories-v2-ghost-stories.txt` |
| 1867 | The Four-Fifteen Express | Amelia B. Edwards | 9,620 | `canon/anthology__stories-of-mystery.txt` |
| 1872 | Carmilla | J. Sheridan Le Fanu | 27,857 | `canon/lefanu__in-a-glass-darkly-v3.txt` |
| 1872 | Green Tea | J. Sheridan Le Fanu | 12,820 | `canon/lefanu__in-a-glass-darkly-v1-green-tea.txt` |
| 1872 | The Familiar | J. Sheridan Le Fanu | 14,496 | `canon/lefanu__in-a-glass-darkly-v1-green-tea.txt` |
| 1881 | Thrawn Janet | Robert Louis Stevenson | 4,387 | `canon/anthology__great-short-stories-v2-ghost-stories.txt` |
| 1884 | The Body-Snatcher | Robert Louis Stevenson | 7,415 | `canon/stevenson__swanston-v3-body-snatcher.txt` |
| 1885 | The Phantom 'Rickshaw | Rudyard Kipling | 8,030 | `canon/anthology__great-short-stories-v2-ghost-stories.txt` |
| 1886 | The Upper Berth | F. Marion Crawford | 8,502 | `canon/crawford__wandering-ghosts-upper-berth.txt` |
| 1887 | Man-Size in Marble | E. Nesbit | 5,356 | `canon/nesbit__grim-tales.txt` |
| 1887 | The Horla | Guy de Maupassant | 9,971 | `canon/anthology__masterpieces-of-mystery-ghost-stories.txt` |
| 1890 | The Middle Toe of the Right Foot | Ambrose Bierce | 3,206 | `canon/bierce__can-such-things-be.txt` |
| 1891 | The Death of Halpin Frayser | Ambrose Bierce | 5,707 | `canon/bierce__can-such-things-be.txt` |
| 1891 | John Charrington's Wedding | E. Nesbit | 2,832 | `canon/nesbit__grim-tales.txt` |
| 1892 | The Yellow Wallpaper | Charlotte Perkins Gilman | 6,078 | `canon/gilman__the-yellow-wallpaper.txt` |
| 1893 | The Damned Thing | Ambrose Bierce | 3,218 | `canon/bierce__can-such-things-be.txt` |
| 1894 | The Great God Pan | Arthur Machen | 21,634 | `canon/machen__the-house-of-souls.txt` |
| 1895 | Canon Alberic's Scrap-book | M. R. James | 4,624 | `canon/james-mr__ghost-stories-of-an-antiquary.txt` |
| 1895 | Lost Hearts | M. R. James | 3,905 | `canon/james-mr__ghost-stories-of-an-antiquary.txt` |
| 1896 | The Red Room | H. G. Wells | 3,915 | `canon/anthology__great-short-stories-v2-ghost-stories.txt` |
| 1898 | The Turn of the Screw | Henry James | 42,210 | `canon/james-henry__the-turn-of-the-screw.txt` |
| 1899 | The Dead Smile | F. Marion Crawford | 8,500 | `canon/crawford__wandering-ghosts-upper-berth.txt` |
| 1902 | The Monkey's Paw | W. W. Jacobs | 3,941 | `canon/jacobs__the-lady-of-the-barge.txt` |
| 1903 | Luella Miller | Mary E. Wilkins Freeman | 6,031 | `canon/freeman__the-wind-in-the-rose-bush.txt` |
| 1903 | The Lost Ghost | Mary E. Wilkins Freeman | 7,131 | `canon/freeman__the-wind-in-the-rose-bush.txt` |
| 1903 | The Shadows on the Wall | Mary E. Wilkins Freeman | 5,345 | `canon/freeman__the-wind-in-the-rose-bush.txt` |
| 1903 | The Wind in the Rose-Bush | Mary E. Wilkins Freeman | 5,871 | `canon/freeman__the-wind-in-the-rose-bush.txt` |
| 1904 | The White People | Arthur Machen | 17,507 | `canon/machen__the-house-of-souls.txt` |
| 1904 | Count Magnus | M. R. James | 5,318 | `canon/james-mr__ghost-stories-of-an-antiquary.txt` |
| 1904 | The Ash-tree | M. R. James | 5,377 | `canon/james-mr__ghost-stories-of-an-antiquary.txt` |
| 1904 | The Mezzotint | M. R. James | 4,538 | `canon/james-mr__ghost-stories-of-an-antiquary.txt` |
| 1904 | “Oh, Whistle, and I’ll Come to You, My Lad” | M. R. James | 7,926 | `canon/james-mr__ghost-stories-of-an-antiquary.txt` |
| 1907 | The Willows | Algernon Blackwood | 19,549 | `canon/blackwood__the-willows.txt` |
| 1907 | The Moonlit Road | Ambrose Bierce | 3,551 | `canon/bierce__can-such-things-be.txt` |
| 1908 | The Screaming Skull | F. Marion Crawford | 13,091 | `canon/crawford__wandering-ghosts-upper-berth.txt` |
| 1910 | The Wendigo | Algernon Blackwood | 18,379 | `canon/blackwood__the-wendigo.txt` |
| 1910 | Afterward | Edith Wharton | 11,426 | `canon/wharton__tales-of-men-and-ghosts.txt` |
| 1910 | The Eyes | Edith Wharton | 7,996 | `canon/wharton__tales-of-men-and-ghosts.txt` |
| 1910 | August Heat | W. F. Harvey | 1,744 | `additional/harvey__august-heat.txt` |
| 1911 | Casting the Runes | M. R. James | 8,765 | `canon/james-mr__more-ghost-stories.txt` |
| 1911 | The Beckoning Fair One | Oliver Onions | 25,164 | `canon/onions__widdershins.txt` |
| 1911 | Sredni Vashtar | Saki | 1,784 | `canon/saki__the-chronicles-of-clovis.txt` |
| 1911 | The Music on the Hill | Saki | 2,149 | `canon/saki__the-chronicles-of-clovis.txt` |
| 1917 | The Woman at Seven Brothers | Wilbur Daniel Steele | 7,867 | `canon/anthology__famous-modern-ghost-stories.txt` |
| 1919 | The Beast with Five Fingers | W. F. Harvey | 9,920 | `canon/anthology__famous-modern-ghost-stories.txt` |
| 1924 | The Rats in the Walls | H. P. Lovecraft | 7,940 | `weird-pulp/lovecraft__the-rats-in-the-walls.md` |
| 1927 | The Colour Out of Space | H. P. Lovecraft | 12,314 | `weird-pulp/lovecraft__the-colour-out-of-space.txt` |
| 1936 | The Graveyard Rats | Henry Kuttner | 2,723 | `weird-pulp/kuttner__the-graveyard-rats.txt` |