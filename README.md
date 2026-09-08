# Standing Water

*Of Roots, Reflections, and the Faces Beneath*

A collection of ghost stories written with Claude, illustrated with five wet-plate
photographs, and developed through rounds of reading and critique.

The stories are the easy part. The real artifact is `craft/` — a guidance system
that starts from general ghost-story craft and is rewritten after every critique
round until it encodes what actually works for this book.

## How the loop runs

1. Claude drafts a story into `stories/<nn>-<slug>/draft-01.md`.
2. Mark reads it and writes `critique-01.md` in the same folder. Blunt is better
   than balanced.
3. Claude turns the critique into durable rules in `craft/lessons-learned.md`,
   amends any craft doc the feedback contradicts, then revises into `draft-02.md`.
4. Repeat until the story is `final`, then it moves to `manuscript/`.

`craft/revision-protocol.md` has the detail. `CLAUDE.md` is the operating manual.

## Where things are

| Path | Contents |
|---|---|
| `craft/` | The living guidance system — start at `00-INDEX.md` |
| `bible/` | Book bible and the plate inventory |
| `stories/` | Drafts and critiques, one folder per story |
| `manuscript/` | Finished stories in reading order |
| `reference/` | Influences and research |
| `wet plate photographs/`, `cover art/` | The images |

## Status

Repo prepared. No stories drafted yet. Open questions awaiting Mark's decisions are
listed at the bottom of `craft/lessons-learned.md`.
