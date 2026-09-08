# Standing Water — Working Instructions

An illustrated collection of ghost stories built through iterative critique. Mark
reads drafts and critiques them; Claude writes, extracts durable lessons from the
critique, and revises. The craft folder is the memory of that loop and is expected
to get sharper every round.

## Read before writing anything

1. `craft/lessons-learned.md` — rules from Mark's actual critiques. **Highest
   authority in the repo.** Overrides every other document here.
2. `craft/ai-tells.md` — failure modes and banned patterns.
3. `craft/craft-principles.md` — story architecture.
4. `craft/style-guide.md` — prose standards.
5. `bible/book-bible.md` — title, sections, setting, story ledger.
6. `bible/plate-inventory.md` — the photographs and their story seeds.

`craft/revision-protocol.md` describes the loop itself.

## Layout

```
bible/                  book bible, plate inventory
craft/                  the living guidance system  ← the point of the project
stories/<nn>-<slug>/    draft-NN.md, critique-NN.md, notes.md
manuscript/             stories promoted to final, assembled in reading order
reference/              influences, research
cover art/              cover.png
wet plate photographs/  the five plates
```

## Rules of the loop

- **Extract before revising.** When a critique arrives, first convert it into
  generalised rules in `craft/lessons-learned.md` with L-IDs, and amend any craft
  doc it contradicts. Only then revise the story. A lesson applied to one story and
  not written down is a lesson lost.
- **Never overwrite a draft.** New round, new file: `draft-02.md`. The progression is
  the record.
- **Update the ledger.** Add the story's row in `bible/book-bible.md` *before*
  drafting, so the collection does not accumulate three stories with the same shape.
- **Run the pre-flight checklist** (`craft/ai-tells.md` §E) before handing over any
  draft. Report honestly if something fails it.
- **Feedback beats doctrine.** If Mark contradicts a craft document, Mark is right
  and the document gets edited the same day.

## Drafting defaults

Past tense, close third or first, 2,500–5,000 words, one impossible thing per story,
no character ever explains the haunting, no ending that resolves it. Start from
`stories/_template.md`; the `wound:` field must be filled before drafting begins.

## Prose ground rules

Plain and concrete. Render emotion as behaviour, never name it. Vary sentence and
paragraph length deliberately. Put the frightening thing at the end of the sentence.
Specificity is the currency that buys the impossible.
