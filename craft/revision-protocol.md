# Revision Protocol

The loop this repo exists to run.

```
   draft ──► Mark reads ──► critique ──► revision + lesson extraction ──► next draft
     ▲                                                                       │
     └───────────────────────────────────────────────────────────────────────┘
```

## 0. Invent

Before any prose. See `invention-protocol.md` for the full method.

1. Write the **Rule (off-page)** - what it wants, what it does. (L-008.)
2. Note the three events a reader would predict from the setup. Ban them.
3. Generate **at least twenty** candidate events across **five or more** categories
   chosen by *who is affected*, with at least three seeded from `reference/period/`.
4. **Discard the first five unread.**
5. Score the survivors against the four tests in `invention-protocol.md` Part 1.
6. **Mark chooses.** Failing that, select by position (8+), never by my ranking - the
   ranker is as mode-collapsed as the generator. (L-013.)
7. Check and update the spent-events log, `invention-protocol.md` Part 3.

The invention pass is cheap. The draft is not.

## 1. Draft

Claude writes `stories/<slug>/draft-01.md` using the craft folder. Frontmatter
records which plate it belongs to, the haunt-logic, and the intended ending type,
so the collection ledger stays accurate.

## 1a. Reference sweep — mechanical, and it runs on every movement

**Added 2026-09-10, at Mark's instruction, after a run of these faults in story 03:**
*"given that this is a theme, we should definitely have a note in our pipeline to look out
for this in all future stories that are being written."*

```bash
python craft/tools/reference-sweep.py stories/<slug>/draft-NN.md --pov <Name> --thing <noun>
```

**Run it before the fresh-context review, on each movement as it is finished — not once at
the end.** Nineteen faults in story 03's first 3,265 words: fifteen gendered pronouns with
the wrong nearest antecedent, four pronouns for the haunting with none at all.

- **Why a script and not a checklist line.** Reading cannot find these. The writer resolves
  a pronoun against *intent* — the notes, the plan, who the scene is about — and the reader
  resolves it against the *nearest available noun*. No amount of care closes that gap,
  because care does not remove the context. The method has to remove it: extract each
  pronoun with the candidate preceding it and **judge the rows in isolation.** Careful
  reading, one critique round and a fresh-context review found one of the nineteen between
  them.
- **It over-flags deliberately, and the output must not be skimmed.** ~79 rows on a
  3,000-word draft. The row I dismissed as noise — the figure introduced as *"A woman, with
  wings"*, competing with the protagonist — was the worst collision in the draft.
- **Read the output in reverse**, so narrative momentum cannot supply a referent.
- **Two of its checks are purely syntactic and need no judgment**: a possessive is not an
  antecedent, and a section break resets anchoring (L-005).
- **Section 2 covers the haunting.** Withholding a *name* is not withholding an
  *explanation* — the thing has a neutral noun that dates nothing and accounts for nothing,
  so an unanchored *it* buys no subtlety and only charges a decode (L-003).
- **Where to look hardest: anything converted from first person**, where the original *I*
  needed no antecedent at all (L-025). Every fault in story 03 clustered there.

## 1b. Fresh-context review — before Mark sees it

**Added 2026-09-09. See L-020.** Hand the finished draft to **the same model in a clean
context** and have it read as a reader, not as the author. Save the output in the story
folder; triage it into the next draft before spending any of Mark's rounds.

Design rules, and they matter more than the prompt does:

- **Give it the story and nothing else.** No craft folder, no lessons-learned, no notes.
  A reviewer holding the doctrine grades against the rubric, which is the L-014 trap
  arriving with a clipboard. A reviewer holding only the text reads as a reader — which is
  how story 01's review diagnosed the rubric tell *without knowing a rubric existed*.
- **Ask for specifics:** what reads as machine-made; what is stated that the story already
  implied; what opportunity the draft touched and flinched from; where it stopped being
  believable.
- **Its output is candidate notes, not authority.** Aesthetic rulings are still Mark's,
  and nothing from a review becomes a rule in `lessons-learned.md` on its own.
- **Expect roughly half to be useful.** On story 01, four of seven notes were actionable,
  one was declined outright, one was collection-level rather than story-level.
- **Structural, not sentence-level.** Its value was architecture, complicity and
  consistency. It found no bad sentences, because by then there were none.

## 2. Critique

Mark reads and writes `stories/<slug>/critique-01.md`. Anything goes: margin notes,
a paragraph, three bullet points, "this bit is fake." Line references are useful but
not required.

Most useful signals, if you feel like being systematic:
- Where you got bored, and the exact line where it started.
- Where you stopped believing it.
- Any sentence that sounded like a machine wrote it.
- Whether the ending earned itself.
- **Any passage you had to ask about.** Added 2026-09-10, story 03 movement one: *"what
  work is the peppermint paragraph doing? just curious about it."* The question is itself
  the finding, and the answer is not the remedy — a passage whose job has to be explained
  is not doing that job visibly, and it is usually one live clause with padding grown round
  it. Same diagnostic as L-008's *"what is actually happening?"*: do not answer it in the
  prose, fix the passage. Ask it freely; it costs a line and it is the cheapest note in
  this list.

Blunt is better than balanced. Praise is only useful when it identifies something to
repeat.

**And one question that is owed on every approval, including a silent one.** Added
2026-09-09, after asking a malformed version of it four times on story 01:

> **Which sentence would you have noticed if it were gone?**

- **Not "which sentence is best."** The point is not praise and not ranking. An approval
  with no notes says the thing worked and says nothing about *what* worked, so the next
  story does not know what to protect. One sentence closes that. Two is generous. Per
  movement if you feel like it; one for a whole story is enough.
- **Why the earlier version was broken.** `vignette-bank.md` asks *which sentence did the
  work?* as one of three ten-second questions about a **single paragraph** — roughly eight
  sentences, where that is answerable. I carried it into story critique unchanged and asked
  it of 5,143 words and some three hundred and fifty sentences, four rounds running, and
  Mark eventually asked what it meant. He was right to. **The vignette scoring questions do
  not scale up any more than the aftermath instruments scale down** (see the beat index) —
  and this instance is the worse of the two, because it happened in the process document
  that exists to catch exactly this error.
- **What the answer is for, and its ceiling.** It identifies a *register* that landed, not a
  template. Reverse-engineering one liked sentence into a prescription is how L-006 became
  the ending of 71% of everything (L-014). Record the answer, name the mechanism once so the
  family is recognisable, and **do not write a rule from it.**

## 3. Extract

Before revising, Claude converts the critique into generalised rules and appends
them to `craft/lessons-learned.md` with IDs. Any craft doc the feedback contradicts
is edited in the same pass. **Extraction happens before revision** — otherwise the
lesson gets applied to one story and lost.

## 4. Revise

New file, `draft-02.md`; the previous draft is never overwritten, so the progression
stays readable. The revision opens with a short changelog noting which lesson IDs
drove which changes.

**And a table of changed line ranges in the new file.** Added 2026-09-09 at Mark's
request: *"is there a way you can point to line numbers of the draft of the changes
between draft 2 and 3 so I don't have to go through the whole thing."* Nobody should have
to diff a 5,000-word draft by eye to find two hundred changed words. Compute it, do not
estimate it:

```bash
sed -n '/^<first line of prose>/,$p' draft-02.md > /tmp/a
sed -n '/^<first line of prose>/,$p' draft-03.md > /tmp/b
diff --changed-group-format='%dF-%dL
' --unchanged-group-format='' /tmp/a /tmp/b   | awk -F- '{print $1+OFFSET"-"$2+OFFSET}'   # OFFSET = lines of frontmatter + changelog
```

Label each range with what changed, and mark the ones that are only re-wraps.

## 5. Close the round

Story frontmatter status advances: `draft` → `revising` → `polished` → `final`.
When a story reaches `final`, it is copied into `manuscript/` for assembly.

## Periodic maintenance

Every few rounds, Claude re-reads `lessons-learned.md` and consolidates: merges
duplicate rules, marks superseded ones, promotes stable rules into `style-guide.md`
or `craft-principles.md`. The lessons file should stay sharp, not become a log.
