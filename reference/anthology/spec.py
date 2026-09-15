# (file, start_line, end_line, title, author, year)
# start_line is the heading line of the story in the source; the cleaner drops
# heading/blurb lines from the top. end_line is exclusive.
C  = "canon/"
W  = "weird-pulp/"
A  = "additional/"
GSA  = C+"james-mr__ghost-stories-of-an-antiquary.txt"
MGS  = C+"james-mr__more-ghost-stories.txt"
POE  = C+"poe__works-raven-edition.txt"
GSS2 = C+"anthology__great-short-stories-v2-ghost-stories.txt"
FMGS = C+"anthology__famous-modern-ghost-stories.txt"
MAST = C+"anthology__masterpieces-of-mystery-ghost-stories.txt"
SOM  = C+"anthology__stories-of-mystery.txt"
GT1  = C+"lefanu__ghostly-tales-v1.txt"
IGD1 = C+"lefanu__in-a-glass-darkly-v1-green-tea.txt"
IGD3 = C+"lefanu__in-a-glass-darkly-v3.txt"
BIER = C+"bierce__can-such-things-be.txt"
FREE = C+"freeman__the-wind-in-the-rose-bush.txt"
NESB = C+"nesbit__grim-tales.txt"
CRAW = C+"crawford__wandering-ghosts-upper-berth.txt"
WHAR = C+"wharton__tales-of-men-and-ghosts.txt"
SAKI = C+"saki__the-chronicles-of-clovis.txt"
MACH = C+"machen__the-house-of-souls.txt"

STORIES = [
 (GSS2, 14920, 15692, "Wandering Willie's Tale", "Sir Walter Scott", 1824),
 (GSS2,   133,  1069, "La Morte Amoureuse", "Th\u00e9ophile Gautier", 1836),
 (C+"gaskell__the-grey-woman-and-other-tales.txt", 88, 2137, "The Grey Woman", "Elizabeth Gaskell", 1861),
 (GT1,     46,   784, "Schalken the Painter", "J. Sheridan Le Fanu", 1839),
 (POE,  27072, 27690, "Ligeia", "Edgar Allan Poe", 1838),
 (POE,  13447, 14217, "The Fall of the House of Usher", "Edgar Allan Poe", 1839),
 (POE,  14358, 14601, "The Masque of the Red Death", "Edgar Allan Poe", 1842),
 (POE,  15878, 16483, "The Pit and the Pendulum", "Edgar Allan Poe", 1842),
 (POE,  18992, 19201, "The Tell-Tale Heart", "Edgar Allan Poe", 1843),
 (POE,  13056, 13447, "The Black Cat", "Edgar Allan Poe", 1843),
 (POE,  12653, 13056, "The Facts in the Case of M. Valdemar", "Edgar Allan Poe", 1845),
 (POE,  14601, 14941, "The Cask of Amontillado", "Edgar Allan Poe", 1846),
 (FMGS,  7154,  7672, "What Was It?", "Fitz-James O'Brien", 1859),
 (GSS2,  3004,  4091, "The House and the Brain", "Edward Bulwer-Lytton", 1859),
 (GSS2,  6063,  6673, "The Signal-Man", "Charles Dickens", 1866),
 (SOM,   2026,  3264, "The Four-Fifteen Express", "Amelia B. Edwards", 1867),
 (IGD1,    72,  1495, "Green Tea", "J. Sheridan Le Fanu", 1872),
 (IGD1,  1495,  3175, "The Familiar", "J. Sheridan Le Fanu", 1872),
 (IGD3,   768,  3990, "Carmilla", "J. Sheridan Le Fanu", 1872),
 (GSS2,  8775,  9180, "Thrawn Janet", "Robert Louis Stevenson", 1881),
 (C+"stevenson__swanston-v3-body-snatcher.txt", 8677, 9446, "The Body-Snatcher", "Robert Louis Stevenson", 1884),
 (GSS2,  1518,  2345, "The Phantom 'Rickshaw", "Rudyard Kipling", 1885),
 (CRAW,  4254,  5131, "The Upper Berth", "F. Marion Crawford", 1886),
 (MAST,  2323,  3329, "The Horla", "Guy de Maupassant", 1887),
 (NESB,  1858,  2444, "Man-Size in Marble", "E. Nesbit", 1887),
 (NESB,   594,   944, "John Charrington's Wedding", "E. Nesbit", 1891),
 (BIER,  4526,  4868, "The Middle Toe of the Right Foot", "Ambrose Bierce", 1890),
 (BIER,    88,   697, "The Death of Halpin Frayser", "Ambrose Bierce", 1891),
 (BIER,  5453,  5833, "The Damned Thing", "Ambrose Bierce", 1893),
 (BIER,  1051,  1410, "The Moonlit Road", "Ambrose Bierce", 1907),
 (C+"gilman__the-yellow-wallpaper.txt", 33, 877, "The Yellow Wallpaper", "Charlotte Perkins Gilman", 1892),
 (MACH,  4893,  7085, "The Great God Pan", "Arthur Machen", 1894),
 (MACH,  3468,  4893, "The White People", "Arthur Machen", 1904),
 (GSS2,  1086,  1502, "The Red Room", "H. G. Wells", 1896),
 (C+"james-henry__the-turn-of-the-screw.txt", 70, 4580, "The Turn of the Screw", "Henry James", 1898),
 (CRAW,   122,  1031, "The Dead Smile", "F. Marion Crawford", 1899),
 (CRAW,  1031,  2192, "The Screaming Skull", "F. Marion Crawford", 1908),
 (C+"jacobs__the-lady-of-the-barge.txt", 643, 1178, "The Monkey's Paw", "W. W. Jacobs", 1902),
 (FREE,    66,   942, "The Wind in the Rose-Bush", "Mary E. Wilkins Freeman", 1903),
 (FREE,   942,  1722, "The Shadows on the Wall", "Mary E. Wilkins Freeman", 1903),
 (FREE,  1722,  2266, "Luella Miller", "Mary E. Wilkins Freeman", 1903),
 (FREE,  4201,  4975, "The Lost Ghost", "Mary E. Wilkins Freeman", 1903),
 (GSA,     73,   557, "Canon Alberic's Scrap-book", "M. R. James", 1895),
 (GSA,    557,   961, "Lost Hearts", "M. R. James", 1895),
 (GSA,    961,  1443, "The Mezzotint", "M. R. James", 1904),
 (GSA,   1443,  1986, "The Ash-tree", "M. R. James", 1904),
 (GSA,   2624,  3139, "Count Magnus", "M. R. James", 1904),
 (GSA,   3139,  3936, "\u201cOh, Whistle, and I\u2019ll Come to You, My Lad\u201d", "M. R. James", 1904),
 (MGS,   1484,  2299, "Casting the Runes", "M. R. James", 1911),
 (C+"blackwood__the-willows.txt", 48, 2126, "The Willows", "Algernon Blackwood", 1907),
 (C+"blackwood__the-wendigo.txt", 39, 1968, "The Wendigo", "Algernon Blackwood", 1910),
 (WHAR,  5852,  6635, "The Eyes", "Edith Wharton", 1910),
 (WHAR,  7737,  9061, "Afterward", "Edith Wharton", 1910),
 (A+"harvey__august-heat.txt", 8, 10**9, "August Heat", "W. F. Harvey", 1910),
 (C+"onions__widdershins.txt", 81, 2927, "The Beckoning Fair One", "Oliver Onions", 1911),
 (SAKI,  1858,  2042, "Sredni Vashtar", "Saki", 1911),
 (SAKI,  2979,  3204, "The Music on the Hill", "Saki", 1911),
 (FMGS,  8459,  9288, "The Woman at Seven Brothers", "Wilbur Daniel Steele", 1917),
 (FMGS,  5753,  6948, "The Beast with Five Fingers", "W. F. Harvey", 1919),
 (W+"lovecraft__the-rats-in-the-walls.md", 5, 10**9, "The Rats in the Walls", "H. P. Lovecraft", 1924),
 (W+"lovecraft__the-colour-out-of-space.txt", 52, 1169, "The Colour Out of Space", "H. P. Lovecraft", 1927),
 (W+"kuttner__the-graveyard-rats.txt", 48, 335, "The Graveyard Rats", "Henry Kuttner", 1936),
]
