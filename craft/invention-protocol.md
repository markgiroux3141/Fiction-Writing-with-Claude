# Invention Protocol

Every other document in `craft/` governs **execution** — how to write the thing well.
This one governs **invention**: choosing what happens at all, and defeating the model's
pull toward the same answer every time.

Origin: Mark, 2026-09-08, on the wake vignette — *"all of these are better than the
original, which tells me that even pointing out that this should be something we focus
attention on improves the result."* Eighteen candidates generated under an explicit
brief all beat the one produced by default. That is the whole argument for this
document.

---

## Part 1 — The event must be chosen, not arrived at

The default failure is not a bad event. It is an event nobody ever decided on: the
first thing that fit the shape, written well.

### The four tests

An event earns the page only if it passes all four.

1. **Does it touch the living?** *"The ghost must want something, and what it wants
   must be bad for the living."* An event that only decorates the dead, the house, or
   the past is scenery. A ghost that tidies is a ghost with no appetite.
2. **Does it implicate the witness?** `craft-principles.md` §6 escalates notice →
   intrude → **implicate**. Most default events stop at intrude. Ask: is she in a worse
   position than before? Was she used, moved, included, or made an accomplice?
3. **Does it imply something larger than itself?** A complete event — one you can
   picture entirely, with nothing left over — is a closed loop. The frightening version
   leaves a residue: a schedule, a second night, a purpose, an appetite that is not
   finished.
4. **Does it change her future?** If the horror is over when the paragraph ends, it was
   an anecdote. The event should make the next day, the next night, or the rest of her
   life different. (This is what L-006 then prices.)

### Worked example — why "somebody had combed his hair" failed

| Test | Verdict |
|---|---|
| Touches the living | **No.** Entirely about the corpse. |
| Implicates the witness | **No.** She slept through it and woke uninvolved. |
| Implies more | **No.** Complete, picturable, self-contained. |
| Changes her future | **No.** Over when the paragraph is. |

Nought for four, and the prose was some of the cleanest in the batch. **Execution
quality cannot rescue an event that has not been chosen.**

---

## Part 2 — Defeating mode collapse

The model converges. Asked for a frightening event, it returns the modal answer from
its training distribution, and asked for a *more original* one it returns a different
flavour of modal answer. Exhortation does not work. Structure does.

### The load-bearing rule: I am not allowed to choose

**My ranking is drawn from the same distribution as my generation.** Generating twenty
candidates and then picking the best three re-applies the prior I was trying to escape —
the list gets wide and the selection narrows it back to the middle. So:

- **Mark picks.** Selection by a human is the single most effective decorrelator
  available and it costs one message.
- **When Mark cannot pick, draw at random with `craft/tools/pick.py`.** Mark's
  proposal, 2026-09-08, and better than my earlier positional heuristic: position 8+ is
  still *my* ordering, so it only launders the same prior. A pseudorandom draw from
  outside the model is the only selection step in the pipeline that is genuinely
  independent of the model.

  ```
  python craft/tools/pick.py CANDIDATES.md -n 1            # uniform over the pool
  python craft/tools/pick.py CANDIDATES.md --tail          # weight toward later items
  python craft/tools/pick.py CANDIDATES.md --seed 20260908 # reproduce a past draw
  ```

  It discards the head of the list (default 5) before drawing, accepts `--exclude` for
  the spent-events log, and always prints its seed. **Log the seed beside the choice.**
  A pick that cannot be reproduced cannot be audited, and an unauditable pick is
  indistinguishable from my having chosen after all.

  Keep candidate files free of any recommendation section. When this was first run
  against `batch-02-wake-options.md` the draw returned an entry from my own "my three"
  paragraph — the shortlist had contaminated the pool it was meant to be drawn from.
- Never present three recommendations as though the list were the work. The list is
  the work; the recommendation is a relapse.

### Generation rules

1. **Twenty minimum.** Not five. The interesting territory starts where the obvious
   runs out, which in practice is somewhere past item eight.
2. **Discard the first five unread.** Treat them as the modal band. If one of them is
   genuinely the right answer it will be re-derivable later; the cost of losing it is
   far below the cost of defaulting to it.
3. **Quota by category, and choose categories by *who is affected*** — not by mood.
   The wake list used: it used **her** / **he** went somewhere / **she** went somewhere
   / it is still in the room / the arithmetic / absence. Six axes, ≥3 candidates each.
   The category structure is what produced the variance, not the instruction to be
   original.
4. **Seed at least three candidates from `reference/period/`.** Open
   `material-culture.md`, `folklore-and-belief.md`, `death-and-mourning.md` or
   `medicine-and-disease.md`, take a real object, custom or belief **chosen without
   regard to whether it is spooky**, and build an event from it. Real-world
   specificity is the strongest available decorrelator because it pulls from outside
   the horror-fiction distribution entirely.
5. **Write the reader's guesses first.** Before generating, note the three things a
   reader would predict from the setup. Ban them. Cheap, and it converts the prior into
   an exclusion list.
6. **Invert once.** Take the modal event and turn it on its head — change the target
   (the act aimed at the living instead of the dead), the agent (she did it), or the
   tense (it is about the next night rather than the last one). The wake list's
   strongest options came from exactly this move.

### What I cannot be trusted to do

Stated plainly so the pipeline does not lean on it: I cannot sample independently of
myself. Two "separate" generations in one context are correlated, my sense of which
option is unusual is unreliable, and my randomness is not random. **The mechanical
steps — Mark choosing, positional selection, external seeds, the exclusion list — do
the real work.** My self-diversification is a helpful prior, not a control.

---

## Part 3 — Spent events

Mode collapse across the collection is a larger risk than within any one story: twelve
stories will drift toward three haunt logics unless the drift is recorded. Log every
event as it is used. Nothing here may be reused, and no new event may be a near
neighbour of one on the list.

| Event | Where | Status |
|---|---|---|
| Certainty of a watcher at the top of the stairs | vignette A1 | spent |
| An extra place at a table, eaten from | vignette B1 | spent |
| A dropped object put back into the hand | vignette D1 | spent |
| A stranger joining a children's game and not stopping | vignette I1 | spent |
| Root-matter growing through a face, trimmed as routine | vignette G1 | spent |
| Wear on a chair and floor from a body that never moved | vignette F1 | spent |
| A ledger entry in the writer's own hand that he did not make | vignette C1 | spent |
| A witness reporting the protagonist abroad at night | vignette J1 | spent |
| A monument that shifts between two exposures | vignette F2 | spent |
| A remote viewer seeing what the person in the room cannot | vignette J2 | spent |
| Bees leaving a house after being told the right name | batch 03 (Fable) #1 | spent |
| A dead tenant's account credited weekly with cane he is still cutting | batch 03 (Fable) #2 | spent |
| A ferry's tally over by one fare a night; the flat sits lower at dusk | batch 03 (Fable) #3 | spent |
| The bed held steady through a malarial chill; the quinine poured away | batch 03 (Fable) #4 | spent |
| A third dress on the line, worn through where the owner's are | batch 03 (Fable) #5 | spent |
| A widow measuring longer at each mourning fitting; waterlogged feet | batch 03 (Fable) #6 | spent |

---

## Part 4 — Stories are grown, not outlined

Mark, 2026-09-08: *"I was starting to get ideas for stories while reading the short
paragraphs. The way to write these stories might be to start from snippets like these,
get ideas, and slowly build up like that, instead of trying to come out with the outline
for a story all at once."*

This is the composition method for the book, and it follows from everything the vignette
loop has demonstrated.

**Why outlining first is the wrong order.** An outline is a plan for a story, and the
model's plan for a ghost story is the modal ghost story — the collapse happens at the
outline stage, before a word is written, and every well-executed scene afterward is a
scene serving a generic shape. Worse, an outline is cheap to produce and expensive to
abandon, so the first one tends to survive.

**The order that works instead:**

1. **Vignettes first, with no story in mind.** One paragraph, one lever, one event that
   passed the four tests. Cheap, disposable, and critiqued in minutes.
2. **Notice which ones generate appetite.** Not which are best written — which make the
   reader want to know what happens on either side of them. That is a different signal
   and only a reader can supply it.
3. **Grow outward from the ones that do.** What had to be true before this? What does
   this cost tomorrow? Each answer is another vignette, tested the same way.
4. **The story is the accretion.** Shape emerges from tested material rather than
   material being poured into a shape. An outline may get written late, as a record of
   what the story turned out to be.

**Consequence for the ledger.** `book-bible.md` asks for a story row *before* drafting.
Under this method the row is filled in progressively — haunt logic and period early,
ending type and physical band only once the story has grown enough to have them. An
honest "TBD" is better than a guess that then constrains the growth.

## Part 5 — The doctrine is itself a collapse vector

Observed 2026-09-08 on batch 03, and the most uncomfortable finding in the project: **a
rule followed faithfully by a more capable model produces more uniform output, not
better output.** See L-014. Two standing counterweights:

- **Ending shapes are rationed like events.** `craft-principles.md` §7 lists three; no
  more than one in three pieces may use the same one. The accommodation ending (L-006)
  is the current offender — five of six in batch 01 r5, four of six in batch 03.
- **Prescriptions are optional by construction.** See *The status of these rules* in
  `lessons-learned.md`: prohibitions are near-absolute, prescriptions are available and
  never required. L-006 collapsed into a shape because it was written as a prescription
  and obeyed like a prohibition. Deviations go in `craft/deviations.md` as experiments
  with verdicts - never as a scheduled quota, which is what the first draft of this
  section wrongly asked for.

## Part 6 — Where this sits in the loop

`revision-protocol.md` begins at **Draft**. This runs before it:

**0. Invent.**
   a. Write the **Rule (off-page)** — what it wants, what it does. (L-008.)
   b. Note the three events a reader would predict. Ban them.
   c. Generate ≥20 candidates across ≥5 who-is-affected categories, ≥3 seeded from
      `reference/period/`.
   d. Discard the first five.
   e. Score survivors against the four tests.
   f. **Mark chooses**, or select by position from 8+.
   g. Check `Part 3 — Spent events`. Log the choice.

Only then draft. The invention pass is cheap and the draft is not.
