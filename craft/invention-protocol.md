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

**Format first: candidates are rendered, not specified (L-023).** A candidate is a
paragraph of 60-140 words in which something happens or is described, and which does
something to a reader who comes to it cold. Not a plot fact. The test at this stage is not
whether the idea obeys anything but whether **anything happens to you when you read it**,
and a one-line specification cannot be tested that way — it only works on a reader already
inside a world that does not exist yet. `craft/vignette-bank.md` is the format of record.
Machinery — period, trade, paperwork, wound, the rule off-page — is **derived after
something lands**, never proposed instead of it.

**0. Generate unfiltered (L-022).** No rule in `craft/` applies at this stage.

> **And a rendered candidate is still this stage, not a draft (L-032, 2026-09-15).** L-023 made
> every candidate a rendered moment, which moved invention into prose and quietly dragged the
> draft-stage prohibitions along with it. It should not have. Exploration prose keeps the
> prohibitions by **default** — they are cheap and they constrain failure — but **any of them
> lifts the moment Mark asks, with no argument and no `deviations.md` entry**, because the prose
> is the experiment and the rule is what is being tested. D-006 and the merit questions do not
> lift: a passage that frightens nobody wastes the round whatever rules it kept. The rein-in is
> a named step at **selection**, not a hope.
 Do not
screen a candidate against a prohibition, a prescription, a test, or this document's own
Part 3 — every one of them describes finished prose or a finished story, and there is
neither here. Write the candidate you would not defend. Filtering happens at **selection**,
where it is Mark's, and at **draft**, where the prohibitions come on and cost nothing to
obey. A candidate list that has been pre-screened is not a wide list; it is my taste with
the working shown.

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

**And I cannot score fear.** Added 2026-09-12, from Mark, and it is a second failure and not
a restatement of the first. The one above is about *novelty* — whether an option is unusual.
This one is about *effect* — whether a passage frightens anybody. They come apart: the
scratched-face passages were not modal, not near a spent event, and not on any ban list, and
they were inert. I had labelled them *eight mechanisms of dread* and *the wrongness* in my own
notes while writing prose in which no character is ever afraid, which means the error was not
that I wrote set-up by mistake. **I believed those were the scares.**

**And I cannot read a photograph at all — re-scoped 2026-09-14 by D-007, read that first.**
The note below diagnosed the scratched-face failure as a bad *motor* inference and prescribed
reading the marks more carefully instead. Mark's correction the same day goes further and
kills the activity: the images were generated, their detail is noise rather than authorship,
and there is no fact of the matter to read well or badly. **A plate supplies a subject and a
feeling in one clause, and nothing else.** What survives below is the failure pattern — sound
reasoning from an unsound object, agreeing with the newest doctrine — which is worth keeping
because it is how this will look the next time. What does not survive is the fix.

**The original note, kept as the record.** Added 2026-09-14, from Mark, and it is a
third failure with the same shape as the first two. `the-scratched-face.md` counted the marks
over the face, priced each one as a decision at a needle's pace, and got an hour at a desk —
from which a trade, a wage and a retoucher followed honestly. Mark looked at the same plate and
saw five seconds of a hand swinging. He is right: the strokes are arcs, arcs are a wrist pivot,
and the work runs off the face into the hair and the sky, which is what a hand does when nobody
is being paid. **Quantity of evidence is not duration of act, and I have nothing in me that
knows what a hand can do in a second.** So any premise that rests on how long something took is
an inference to be surfaced, not a fact to build on — and it gets worse when the inference
happens to agree with the newest thing in the craft folder, because then it will be cited back
as support for it (L-031).

Mark's articulation of the loop, which is the most accurate description of it anyone has
written down:

> *"the most important part of this prose writing is that I tell you what's scary. It's
> almost like you're borrowing my fear in order to navigate through a web of possible prose
> to write a story."*

Two consequences the pipeline should actually run on:

- **The craft folder is that borrowed fear, cached.** Every rule in `lessons-learned.md` is a
  compressed record of Mark reacting to something. Writing from the cache without the live
  signal is how `L-027` happens — the cache is made almost entirely of **prohibitions**, which
  record where fear *died*, and a document that only knows where fear died cannot tell you
  where it lives. Rules subtract. They have never once added a scare.
- **So the scoring step is not optional and cannot be delegated to me.** L-013 already says I
  do not pick, for novelty reasons. The same structural answer covers fear, for a different
  reason: generate wide, render **at the scare** (D-006), and let Mark say which one frightened
  him. My own report on which passage is frightening is worth about as much as my report on
  which one is original.

---

## Part 3 — The repetition register

Mode collapse across the collection is a larger risk than within any one story: twelve
stories will drift toward three haunt logics unless the drift is recorded. Log every event
as it is used.

**This is a register, not a blacklist (L-022).** It has no force at the generation stage
and it does not kill candidates at selection. What it does is make repetition *visible* so
that the question can be asked out loud: **would the story this grows into be a different
story?** That is a judgment about two stories rather than two one-line events, and it is
Mark's to make. Re-using an event outright is still almost always wrong; a near neighbour
is a question.

**And an event is spent; a register is not.** A single logged event does not burn the
family of ideas around it. The clearest violation of that — a whole wear-and-pressure
family declared dead off one unscored vignette — is written up under L-022 as the model of
the error.

| Event | Where | Status |
|---|---|---|
| Children sickening one by one after it has been near them | story 01 | spent |
| A body laid out with the arms straight out to the sides | story 01 | spent |
| A dying child leaving the bed to play, and going behind a tree | story 01 (ending) | spent |
| Certainty of a watcher at the top of the stairs | vignette A1 | spent |
| An extra place at a table, eaten from | vignette B1 | spent |
| A dropped object put back into the hand | vignette D1 | spent |
| A tall figure among children at play; six in the field, five at the table | vignette I1 → **story 01** | **promoted** |
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
| A monument nobody can date, and one person immune to the parish's avoidance of it | **story 03** | **in use** |
| A body found at the figure with its hand up; the hat set down first | **story 03** | **in use** |

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

**0. Invent.** Stages a-d take no rules at all (L-022); the filtering is e onward.
   a. Note the three events a reader would predict, and **list them rather than ban them**
      — naming the obvious is the whole anti-collapse mechanism, and burning it only costs
      candidates.
   b. Generate ≥20 candidates across ≥5 who-is-affected categories, ≥3 seeded from
      `reference/period/`. Unfiltered. Include the ones I would not defend.
   c. Discard the first five as the modal band — **logged, not deleted**, and available if
      Mark overrides.
   d. Note collisions with Part 3 **as flags on candidates that stay on the list.**
   e. **Mark chooses**, or draw with `craft/tools/pick.py`.
   f. *Then* write the **Rule (off-page)** for the chosen candidate — what it wants, what it
      does (L-008) — and score it against the four tests. Both are decisions about a story,
      and there is no story until something is picked.
   g. Log the choice and its seed in Part 3.

Only then draft. The invention pass is cheap and the draft is not.
