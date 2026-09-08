# Standing Water — Working Instructions

An illustrated collection of ghost stories built through iterative critique. Mark
reads drafts and critiques them; Claude writes, extracts durable lessons from the
critique, and revises. The craft folder is the memory of that loop and is expected
to get sharper every round.

## Start here

`STATUS.md` — where the project actually is, what is unscored, and what happens next.
Read it first in a fresh session; it is short and it is the only file that tracks
position rather than doctrine.

## Read before writing anything

1. `craft/lessons-learned.md` — rules from Mark's actual critiques. **Highest
   authority in the repo.** Overrides every other document here. Read its opening
   section, *The status of these rules*, before treating any of it as binding:
   prohibitions are near-absolute, **prescriptions are available and never required**,
   and the effect on the page outranks the cache of judgments that this file is.
2. `craft/ai-tells.md` — failure modes and banned patterns.
3. `craft/craft-principles.md` — story architecture.
4. `craft/style-guide.md` — prose standards.
5. `bible/book-bible.md` — title, sections, setting, story ledger.
6. `bible/plate-inventory.md` — the photographs and their story seeds.

`craft/lessons-learned.md` opens with a quick index of every rule. Read that first,
then the full entry for anything you are about to lean on.

`craft/invention-protocol.md` runs **before** any of this: choosing what actually
happens, and the structural defences against the model returning the same answer every
time. `craft/revision-protocol.md` describes the loop itself. `craft/vignette-bank.md` holds
the calibration exercise — single-paragraph vignettes, one mechanism of dread each,
critiqued cheaply so the rules get sharper without spending a story.

## Layout

```
bible/                  book bible, plate inventory
craft/                  the living guidance system  ← the point of the project
craft/vignettes/        batch-NN.md, batch-NN-rNN.md, critique-NN.md
stories/<nn>-<slug>/    draft-NN.md, critique-NN.md, notes.md
manuscript/             stories promoted to final, assembled in reading order
reference/              influences, research
cover art/              cover.png
wet plate photographs/  the five plates
```

## Rules of the loop

- **Invent before drafting.** Run `craft/invention-protocol.md` step 0. Generate at
  least twenty candidate events, discard the first five, and let Mark choose - never
  present a shortlist as the deliverable, because the ranking is as mode-collapsed as
  the generation.
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
- **Effect beats rule.** If breaking a prescription makes the passage better, break it,
  then log it in `craft/deviations.md` with the argument. A break Mark likes amends the
  rule; a break he rejects becomes a counterexample. An unlogged break teaches nothing.
  This is not licence: "it felt better" is not an argument, and violating a prohibition
  is a mistake, not a deviation.
- **Test on vignettes before stories.** A rule that has only ever been applied to one
  paragraph is a hypothesis. Run new mechanisms through `craft/vignette-bank.md` first;
  a failed 150-word vignette costs nothing and a failed draft costs a round.

## Drafting defaults

Past tense, close third or first, 2,500–5,000 words, one impossible thing per story,
no character ever explains the haunting, no ending that resolves it. Start from
`stories/_template.md`; the `wound:` field must be filled before drafting begins, and
so must **Rule (off-page)** — one sentence saying what the thing wants and what it
does, which never appears in the prose. If it cannot be written, do not draft (L-008).

## Prose ground rules

Plain and concrete. Vary sentence length *and construction* deliberately. Put the
frightening thing at the end of the sentence. Specificity is the currency that buys the
impossible.

Never name an emotion. Render it as the involuntary event first, then the knowing, then
the misfired action — coarse, not clinical, because fear narrows perception rather than
sharpening it. Stay out of the tactile register (hair, gooseflesh, crawling skin); use
proprioceptive, spatial, cognitive, motor or temporal instead. Put the strangeness in
the perception and keep the words plain.

Name the ordinary activity in the first sentence, put the wrongness in the approach,
and end on what the character permanently pays to avoid the thing — never on what it
was.
