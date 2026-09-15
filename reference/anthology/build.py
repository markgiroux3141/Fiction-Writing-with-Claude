# -*- coding: utf-8 -*-
import io, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from extract import build
from tex import latex, PREAMBLE

NAME = "sixty-two-ghost-stories"

HERE  = os.path.dirname(os.path.abspath(__file__))
OUT   = HERE
FONTS = os.path.abspath(os.path.join(HERE, "..", "..", "render", "fonts")).replace(os.sep, "/")

NOTE = r"""
Sixty-two stories, drawn from the public-domain texts collected under
\texttt{reference/texts} for the \textit{Standing Water} project and set here in
one volume for reading rather than for reference. They run from Walter Scott's
\textit{Wandering Willie's Tale} of 1824 to Henry Kuttner's \textit{The Graveyard
Rats} of 1936: the English antiquarian ghost story and its American cousins, the
Irish and Scottish tales that fed them, and the pulp weird that came after.

\vspace{3mm}
The texts are Project Gutenberg transcriptions except where the source manifest
notes otherwise. Each story has been lifted out of its parent volume, stripped of
prefatory matter, editors' biographical notes, transcriber's notes and running
footnote markers, and re-set. Sectional divisions and scene breaks are the
originals'. Nothing in the prose has been altered, modernised or abridged.

\vspace{3mm}
Everything here is in the public domain in the United States. The four
in-copyright pieces held in \texttt{reference/texts/additional} --- Bradbury's
\textit{The Small Assassin}, Jackson's \textit{The Lottery}, Leiber's
\textit{Smoke Ghost} and Campbell's \textit{Who Goes There?} --- are deliberately
not included.

\vspace{3mm}
Three entries in the source manifest turned out to be wrong, and the stories they
promised are not in the library at all: Gaskell's \textit{The Old Nurse's Story}
is not in \textit{The Grey Woman and Other Tales}, Le Fanu's \textit{Madam
Crowl's Ghost} and \textit{Squire Toby's Will} are not in either volume of
\textit{Ghostly Tales}, and the Maupassant volume holds \textit{The Trip of the
Horla}, a balloon ascent, not \textit{The Horla}. The Horla printed here was
recovered from the \textit{Masterpieces of Mystery} anthology instead.
"""


def render(story):
    title = latex(story['title']).replace(r'\emph', r'\textit')
    out = [r"\story{%s}{%s}{%d}" % (title, latex(story['author']), story['year'])]
    first = True
    for kind, txt in story['paras']:
        if kind == 'sect':
            out.append(r"\sect{%s}" % latex(txt))
            first = True
        elif kind == 'break':
            out.append(r"\scenebreak")
            first = True
        else:
            body = latex(txt)
            if not body:
                continue
            out.append((r"\noindent " if first else "") + body)
            out.append("")
            first = False
    return "\n".join(out)


def main():
    os.makedirs(OUT, exist_ok=True)
    stories = build()
    stories.sort(key=lambda s: (s['year'], s['author'], s['title']))
    body = "\n\n".join(render(s) for s in stories)
    doc = (PREAMBLE.replace("FONTPATH", FONTS)
                   .replace("NOTEBODY", NOTE)
                   .replace("BODY", body))
    io.open(os.path.join(OUT, NAME + ".tex"), "w", encoding="utf-8").write(doc)
    words = sum(s['words'] for s in stories)
    print("anthology.tex written: %d stories, %s words" % (len(stories), format(words, ',')))


main()
