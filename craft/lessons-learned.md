# Lessons Learned

Distilled from Mark's critiques. This is the highest-authority craft document in the
repo: where it conflicts with `style-guide.md` or `craft-principles.md`, **this file
wins**, and the conflicting doc should be amended.

## The status of these rules

Mark, 2026-09-08: *"we shouldn't have hard rules, if you can break a rule and it has a
good effect, then do that."*

**The effect is the only authority.** Every rule in this file is a *cached judgment* -
a compressed record of something Mark reacted to once. The cache exists because he
cannot read every sentence, not because the rule outranks him. When a rule and the
effect on the page disagree, **the effect wins and the rule gets amended the same day.**

That is easy to write and hard to act on, so three mechanisms make it real.

### 1. Rules come in three kinds, and they do not have equal force

| Kind | What it says | Force |
|---|---|---|
| **Prohibition** | *Avoid this - it reliably fails* | Near-absolute. Cheap to obey; not doing something rarely costs originality. Break only with an argument for the specific case. |
| **Prescription** | *This move worked once* | **Available, never required.** Ration it. A prescription applied every time has stopped being a rule and become a shape. |
| **Working** | *How we operate* | Obey. These govern process, not prose, and breaking them just means working badly. |

**This distinction is the whole answer to the tension.** L-006 collapsed into formula
because it was written as a prescription and then obeyed like a prohibition - a move
Mark liked once became the ending of 71% of everything. Prohibitions cannot collapse
that way: avoiding the tactile register or refusing to answer unasked questions
constrains failure without dictating what fills the space.

### 2. Every rule carries its evidence, and thin evidence is a warning

`Basis: n` records how many independent critiques support a rule. **Almost everything
here is n=1.** A prescription with `n=1` that has fired more than three times without
re-validation has outrun its evidence and is due for a deliberate test - write the
version that ignores it and put both in front of Mark.

Current standing: **L-006 is n=1 and has fired twelve times.** It is the most
over-trusted rule in the repo.

### 3. Breaking a rule is an experiment, and experiments get logged

Not a licence and not a quota. When a passage is better for ignoring a prescription,
do it, then record it in `craft/deviations.md`: the rule, what was done instead, the
argument, and Mark's verdict. A break Mark likes amends the rule. A break he does not
becomes a counterexample that strengthens it. Either way the doctrine learns, which an
unlogged break cannot make it do.

**What this does not license.** "It felt better" is not an argument. Neither is breaking
a prohibition to seem bold - using a banned phrase is not a deviation, it is a mistake
with a story attached.

---

## Quick index

Read the full entry before applying. Standing decisions (D-nnn) are Mark's direct
instructions and outrank everything.

| ID | Kind | Basis | Fired | Rule |
|---|---|---|---|---|
| D-001 | decision | - | - | Fully standalone stories - no shared geography, family, object, continuity |
| D-002 | decision | - | - | Mostly period (c. 1850-1920), one or two modern stories that earn it |
| D-003 | decision | - | - | Body horror is a regular instrument - vegetal register, spent late |
| L-001 | prescription | 2 | 15 | The body answers before the mind does - and coarsely, never clinically |
| L-002 | working | 1 | - | Feedback names an experience, not a mechanism |
| L-003 | prohibition | 1 | - | Obliquity is not restraint - plain words for plain things |
| L-004 | prohibition | 1 | - | No answers to unasked questions |
| L-005 | prohibition | 1 | - | Elide on the second mention; never restate to negate |
| L-006 | **prescription** | **1** | **12** | Price the fear; end on the accommodation ← **over-trusted** |
| L-007 | prohibition | 1 | - | Change the register, not the adjective - the tactile one is spent |
| L-008 | working | 1 | - | Know the rule; never state it. Undecided is not withheld |
| L-009 | prohibition | 1 | - | Establish the frame before the strangeness |
| L-010 | prescription | 1 | 6 | Put the wrongness in the approach |
| L-011 | prohibition | 1 | - | Polysyndeton is an instrument, not a default |
| L-012 | working | 1 | - | Choose the event; four tests before any prose is written |
| L-013 | working | 1 | - | Defeat mode collapse structurally - long lists, and I do not pick |
| L-014 | working | 1 | - | The doctrine is itself a collapse vector - ration the prescriptions |
| L-015 | working | 1 | - | Grow stories from vignettes; do not outline first |

**Kind** determines force (see above): prohibitions are near-absolute, prescriptions are
available but never required, working rules govern process. **Basis** is how many
independent critiques support the rule. **Fired** counts prescriptions only - how many
pieces have applied it. A prescription whose Fired count badly exceeds its Basis is a
formula waiting to be noticed.

**The bookkeeping family (L-003, L-004, L-005).** One failure in three shapes: a
sentence that makes the reader stop and do clerical work. All three read as *odd*
rather than *wrong* - when a line is reported as strange rather than incorrect, look
for the bookkeeping.

## How entries are made

After each critique round, every piece of feedback is converted into a durable,
generalisable rule. Raw feedback stays in the story folder
(`stories/<slug>/critique-NN.md`); only the generalised lesson comes here.

A good entry states the rule, the evidence, and how to apply it — so that it is
actionable on a story that has nothing to do with the one that produced it.

Entry format:

```
### L-007 — Short rule name
**Rule:** One sentence, imperative.
**Origin:** Story slug, critique round, date.
**Evidence:** What Mark actually objected to, briefly quoted.
**How to apply:** What to do differently, concretely.
**Status:** active | superseded by L-0NN
```

## Standing decisions from Mark

Direction given outright rather than extracted from a critique. Same authority as a
lesson: these override anything written elsewhere in the repo.

### D-001 — Fully standalone stories
**Rule:** No shared geography, family, object, or continuity between stories; none
may depend on another having been read.
**Origin:** Setup, 2026-09-08.
**How to apply:** Invent a fresh corner of the Gulf South per story. Cohesion comes
from register and motif only. Resist every temptation toward callbacks — including
the two plates that share a staircase.
**Consequences:** `craft-principles.md` §12 rewritten; `book-bible.md` § Setting
rewritten; the linked-collection proposal in `plate-inventory.md` withdrawn.
**Status:** active

### D-002 — Mostly period, some modern
**Rule:** Center the book c. 1850–1920; allow one or two present-day stories that
inherit a period object or house.
**Origin:** Setup, 2026-09-08.
**How to apply:** A modern story must be frightening in a way a period story could
not be — otherwise set it in the past. Track period in the ledger so the modern
stories stay rare.
**Consequences:** `craft-principles.md` §10 rewritten.
**Status:** active

### D-003 — Willing to get physical
**Rule:** Body horror is a regular instrument, spent precisely and late, in a
vegetal rather than visceral register.
**Origin:** Setup, 2026-09-08.
**Evidence:** Mark chose "willing to get physical" over my restraint default,
consistent with Plate V.
**How to apply:** Growth through the body, waterlogged tissue, root and fibre — not
blood and wounds. Flattest sentence in the story delivers the worst image. Roughly a
third of stories explicit, a third threatened, a third at the edge of frame. The
child-harm limit still stands.
**Consequences:** `craft-principles.md` §11 rewritten from "Cruelty budget"; ledger
gained a `Physical` column.
**Status:** active

## Lessons from critiques

### L-001 — The body answers before the mind does
**Rule:** Render the involuntary physical event in sequence — body first, then
knowing, then behaviour — and give the body its own sentences.
**Origin:** Vignette batch 01 (A1, "The staircase"), critique 01, 2026-09-08.
**Evidence:** Mark: *"the thing that happens should be the effect the feeling has on
the person, which is pretty much absent. I want something describing the hair
standing up on the back of the neck of the character in a way that elicits this in
the reader."*
**How to apply:**
- Put the autonomic event **before** the character understands anything. She does not
  become frightened and then get gooseflesh; the gooseflesh is how she finds out.
- Pick **one or two** physical facts and render them with anatomical precision and
  **duration**. Not "her hair stood up" but the nape wet since six, and the hair
  unsticking from the skin a few at a time. The cliché versions are compressions; the
  fix is to decompress, not to substitute a fresher cliché.
- Prefer sensations that contradict the conditions: gooseflesh in a hot hall, sweat
  going cold on a bright morning. Physiology that fights the weather reads as fact.
- **Behaviour alone is under-rendering.** Misfired actions (`style-guide.md` §
  Emotion) are the *aftermath* of fear and cannot carry it by themselves. A paragraph
  built only of behaviour makes the reader a witness rather than a participant.
- The ban in `style-guide.md` covers **naming the emotion** and the **stock
  renderings** ("a shiver ran down her spine"). It does not cover the body.
**Ceiling (added 2026-09-08, critique 02):** render the body at the resolution the
*frightened person* has of it, never an anatomist's. **Fear narrows perception; it
does not sharpen it.** She does not feel individual hairs release in sequence — she
feels something large and stupid and wants to be outside. One or two blunt physical
facts, then get her moving. Precision belongs to the *approach*; the moment itself is
coarse. Over-rendering fails in exactly the same way under-rendering does: the reader
watches instead of feeling.
**Consequences:** `style-guide.md` § Emotion rewritten into three tiers;
`ai-tells.md` §E gains check 9.
**Status:** active, amended by L-002


### L-002 — Feedback names an experience, not a mechanism
**Rule:** When Mark names a detail, he is naming the effect he wants; build the
experience, and treat the named detail as optional.
**Origin:** Vignette 1 r2, critique 02, 2026-09-08.
**Evidence:** *"'Hair on the back of your neck' was meant to be a metaphor for
'describe a human experiencing fear in this situation', not a request to give a
medically accurate description of the process of piloerection."*
**How to apply:** Read every note as *"produce this feeling"* first and *"insert this
thing"* only if the literal reading still makes sense afterward. Idioms in particular
("her blood ran cold", "it made my skin crawl", "a slap in the face") are names for
states, not specifications. The tell that the literal reading has been taken: the
draft explains the mechanism of something the reader already knows by feel. If a note
could be satisfied without the named noun appearing once, that is usually the better
draft.
**Status:** active

### L-003 — Obliquity is not restraint
**Rule:** Say the plain thing about a strange event; never a strange thing about a
plain one. If the reader must decode a sentence, it has failed.
**Origin:** Vignette 1 r2, critique 02, 2026-09-08.
**Evidence:** *"'It was wet there', is this describing sweat on her neck? That's a
super weird way to describe it."*
**How to apply:** Sweat is sweat. The urge to avoid a plain word because it feels
stock is the wrong instinct — the cure for a stale phrase is a *more specific* plain
statement, not an oblique one. Test: could a reader name the referent of this sentence
without going back a line? If not, rewrite it flat. The strangeness budget belongs to
the haunting; ordinary bodies and ordinary furniture get ordinary words.
**Status:** active

### L-004 — No answers to unasked questions
**Rule:** Cut any sentence that defends, excuses, or corrects something the reader has
not yet thought about.
**Origin:** Vignette 1 r2, critique 02, 2026-09-08.
**Evidence:** *"the layout of the house was a fault in the builder and not in her.
That just seemed like an odd thing to add... when I read it, it just seemed strange"*
**How to apply:** The reader stops and hunts for the argument the sentence is
answering, finds none, and registers it as *off* without being able to say why — Mark
could not, and it still cost him the paragraph. Three specific forms to grep for:
- **The pre-emptive defence.** Excusing a character before anything has been alleged.
- **The narrator's aside at the threshold.** Wit immediately before the fear puts a
  commentator between the reader and the character. Be funny early or not at all.
- **The pre-excused reaction.** Signalling that a character is about to be frightened
  and that it is reasonable. It spoils the event and defuses it in one move.
**Status:** active

### L-005 — Elide on the second mention; never restate to negate
**Rule:** When a sentence reverses or corrects the one before it, replace the repeated
words with the shortest pro-form English allows, and put the resolution within a
clause of the contradiction.
**Origin:** Vignette 1 r3, critique 03, 2026-09-08.
**Evidence:** Mark on *"The basket was on the wrong hip. It was not on the wrong hip,
but that was the thought she had"*: *"sounds a little awkward reading it because 'but
that was the thought she had' resolves the strangeness of the contradiction too late.
It's something to do with saying something, and then using almost the same words to
say the opposite."*
**How to apply:**
- **Mechanism.** A restated phrase makes the reader re-parse words they already hold,
  hunting for what changed. If the only change is a negation, they have spent five
  words of attention to receive one bit — and for the whole length of that phrase the
  contradiction is standing unexplained. "It wasn't" costs nothing and carries the
  same bit, so the resolution arrives while the contradiction is still warm.
- **Rule of thumb:** a contradiction may stand unresolved for about a clause. Longer
  and the reader stops reading and starts doing bookkeeping.
- **Not a blanket ban on repetition.** Full restatement is an emphasis figure and it
  works when the repetition *intensifies* — "He was not a kind man. He was not a kind
  man at all." It fails when the repetition *reverses*, because reversal is new
  information and verbatim repetition signals the absence of new information. The
  form contradicts the content.
- **Near deixis in free indirect style:** *this* thought, not *that* thought. "That"
  narrates her from outside; "this" is in her head. Use the closer word wherever the
  prose is inside a character.
- While rewriting, **count the pronouns.** Three referents for "it" in one sentence is
  the same tax arriving by another route.

**Pattern — the bookkeeping family (L-003, L-004, L-005).** These are one failure in
three shapes: **a sentence that makes the reader stop and do clerical work.** Decoding
a referent (L-003), hunting for an argument that was never made (L-004), holding a
contradiction that has not yet resolved (L-005). None of them reads as *wrong*; each
reads as faintly *odd* — which is why Mark reported the symptom twice while saying he
could not explain it. **When a line is reported as strange rather than as incorrect,
look for the bookkeeping.** That is the diagnostic.
**Status:** active

### L-006 — Price the fear; end on the accommodation
**Rule:** Measure a fear by what the character permanently pays to avoid it. State the
price in a unit, never state the fear, and never join the two.
**Origin:** Vignette 1 r4, critique 04, 2026-09-08.
**Evidence:** Mark: *"It was an inconvenience for her to use the kitchen door but she
did it to avoid going by the stairs, and this was a good way of describing it."*
Control available in-repo: draft 01 ended on the same detour and the same eleven steps
and was inert.
**How to apply:**
- **Quantify the cost; leave the fear unnamed.** "Eleven steps each way" is exact and
  countable; the thing on the landing is never described or referred to again. The
  reader divides one by the other and sizes the fear themselves.
- **Make the price small.** Fleeing the house is proportionate to fright and therefore
  carries no information. A trivial, permanent, daily tax is worse, because it says the
  character has neither fought the thing nor run from it — she has built a workaround
  and gone on with her life. **The accommodation implies the haunting is a settled
  condition and that she knows it.**
- **Never join cause to cost.** The word *stairs* must not appear in the paragraph that
  charges for them. The reader closes the gap in one step, and closing it is what makes
  them complicit.
- **Withdraw interiority for the last beat.** Retreat to logistics and behaviour. She
  has stopped having a crisis about it, because it is her life now; the narration
  stopping too is the proof.
- **Duration, not escalation.** Nothing gets worse; it gets permanent. "For the rest of
  the summer" is the whole move.
- **Precondition — this is why the draft-01 version was dead.** A price is only
  information if the reader already knows what is being bought. Do not reach for the
  accommodation ending unless the fear has actually landed on the page first.

**Boundary — the good gap vs. the bookkeeping family (L-003/004/005).** The reader must
infer *kitchen door → avoiding the stairs*, which resembles the clerical work those
lessons ban. The test that separates them: **does the reader complete the inference or
search for it?** Complete: every piece present, one step, unambiguous, and a small
pleasure to arrive at. Search: re-parsing words already held, hunting material never
supplied, or holding a contradiction open. Aim for gaps that get *closed*, never gaps
that get *searched*.
**Status:** active

### L-007 — Change the register, not the adjective
**Rule:** When a sensation is clichéd, render it in a different sensory register
rather than hunting a fresher word for the same one. Put the strangeness in the
**perception**; keep the **words** plain.
**Origin:** Vignette 1 r4, critique 05, 2026-09-08.
**Evidence:** Mark on *"Her back had never been so much of her before. She could feel
the whole width of it."* — *"It captures the feeling of someone being behind you that
doesn't feel cliche."*
**How to apply:**
- **The tactile register is spent.** Hair rising, skin crawling, prickling, cold
  spots, gooseflesh — every stock rendering of *someone is behind you* lives here.
  r2 rendered the tactile version at maximum resolution and was still dead, which is
  the proof that resolution is not the variable. Register is.
- **Registers available**, none of them worked out:
  - **Proprioceptive** — how big a part of you feels, whether a limb still seems
    yours. *(the back becoming a larger fraction of her)*
  - **Spatial** — distance misbehaving. *(the hall was nine feet and took a long
    time)*
  - **Temporal** — duration misbehaving.
  - **Cognitive** — the stupid thought that will not drop. *(the basket on the wrong
    hip)*
  - **Motor** — what the body tries to do, or fails at. *(the latch worked twice; her
    legs went)*
  - **Attentional** — what she cannot stop monitoring.
- **Strange perception, plain words.** Compare the two lines from the same vignette:

  | | perception | phrasing | result |
  |---|---|---|---|
  | "It was wet there" | ordinary | oblique | fails (L-003) |
  | "her back had never been so much of her before" | strange | plain | works |

  Oblique phrasing of an ordinary perception is the failure; plain phrasing of an odd
  perception is the fix. This is the positive statement of L-003.
- **No simile *for a sensation*.** "It was as if her back had become enormous" inserts
  an author performing a comparison. Declare the impossible-sounding fact flatly. A
  statement about a character's relation to her own body is unfalsifiable — the reader
  can only check it against theirs, where it is true. Aim for recognition, not
  persuasion.
  **Boundary (added 2026-09-08):** a simile that identifies an *action* or its *social
  register* is permitted and is often the sharpest instrument available — *"the fingers
  folded over his own to be sure of it, the way you would give a man his change."* The
  banned kind decorates a feeling the reader must be made to have; the permitted kind
  classifies a behaviour, and by making the impossible act *ordinary and social* it
  does the work no direct description can. Test: **is the comparison telling the reader
  how something felt, or what kind of thing it was?** The first is dressing; the second
  is evidence.
- **Choose the axis deliberately.** *Width*, not size or shape: the lateral dimension
  is the surface that can be **seen**, so the word says the threat is a gaze rather
  than a hand without either word appearing.
- **Audit by register.** Count the fear-renderings in a passage and tag each one. r2:
  four renderings, three tactile — failed. r4: five renderings, none tactile — worked.
  If two or more sit in the same register, move one.
**Consequences:** `style-guide.md` § Emotion tier 1 rewritten (it still recommended
the tactile examples and still asked for anatomical resolution, both reversed by the
L-001 ceiling); `ai-tells.md` §C gains "The tactile default".
**Status:** active

### L-008 - Know the rule; never state it. Undecided is not withheld.
**Rule:** Before drafting, write down in one sentence what the thing wants and what it
does. Keep it off the page permanently - but do not begin without it.
**Origin:** Vignettes 2 and 3 r5, critique 06, 2026-09-08.
**Evidence:** Mark: *"what's happening in this story exactly? Why is there an extra
spot? who sits in it? What is the reason that this is scary?"* and *"what happened when
he retrieved his knife? He let other things go for a reason. Why?"*
**How to apply:**
- `craft-principles.md` §3 and James's *"we do not want to see the bones of their
  theory"* both presuppose **that there is a theory**. Withholding a rule and never
  having formed one produce opposite prose: the first is dense with consequences that
  imply a cause; the second is gestures that imply nothing.
- **The diagnostic is the reader's question.** *"What is actually happening?"* is never
  a request for exposition - it is the reader reporting that the gestures do not add
  up. Do not answer it in the story. Fix the hollow.
- **The reader is owed consequences in exchange for the rule.** Something must be
  measurably different afterward: an object changed, a habit changed, a cost paid. In
  r5 nothing happened to the man in the pond - he was handed a knife and went home. A
  contact with no consequence is an anecdote.
- Record the rule in the vignette or story file as **"Rule (off-page)"**, above the
  prose, never inside it. If it cannot be written in one sentence, the story is not
  ready.
**Consequences:** `craft-principles.md` §3 amended; `vignette-bank.md` gains a
mandatory Rule field.
**Status:** active

### L-009 - Establish the frame before the strangeness
**Rule:** Name the ordinary activity plainly in the first sentence. The wrongness needs
a normal to be wrong against.
**Origin:** Vignette 5 r5, critique 06, 2026-09-08.
**Evidence:** Mark: *"I honestly have no idea what he is doing, I spent the entire time
trying to decode the hidden message of what this guy is doing with a scissors a bowl and
newspaper, instead of being engrossed in the story telling. Is he cleaning a fish?"*
**How to apply:**
- Say *beard*. Say *table*, *coffin*, *baby* - whatever the mundane frame is, in plain
  words, immediately. This is L-003 at scene scale.
- **Ambiguous props are noise, not clues.** Scissors + bowl + newspaper + good light
  describes cleaning a fish as well as it describes trimming a beard. A prop only works
  once the reader knows what activity it belongs to.
- **Withholding the frame is not suspense.** Suspense requires the reader to know what
  is at stake. A reader who is decoding is not afraid; they are working, and they will
  finish the paragraph having felt nothing.
- Ask of every opening: *could a careless reader name what this person is doing?* If
  not, rewrite until they can. The horror is never the frame - it is what the frame
  turns out to contain, and it cannot turn out to contain anything until it exists.
**Status:** active

### L-010 - Put the wrongness in the approach
**Rule:** Signal before contact. The passage leading to the impossible carries the
concrete detail; the contact itself stays thin.
**Origin:** Vignette 3 r5, critique 06, 2026-09-08.
**Evidence:** Mark: *"The description of the water doesn't include any feelings that
something is amiss."*
**How to apply:**
- This is `influences/james-rules.md` §3 - *most concrete in the approach, least
  concrete in the touch* - and r5 had it exactly backwards: a flat approach and a
  heavily rendered touch.
- **Prefer absence-signals to presence-signals.** *"Nothing moved away from him when he
  came in. A pond that size, you put a leg in and the whole of it goes somewhere
  else."* An ordinary thing that fails to happen is more disturbing and far cheaper
  than an extraordinary thing that does, and it does not spend the story's one
  impossible thing.
- One or two signals, placed early, unremarked by the character. He notices; he does
  not interpret.
**Status:** active

### L-011 - Polysyndeton is an instrument, not a default
**Rule:** Vary how long sentences are made long. Chained *and* is for accumulation, once
or twice a passage.
**Origin:** Vignette 4 r5, critique 06, 2026-09-08.
**Evidence:** Mark: *"Sometimes the sentences seem short and awkward though, they don't
seem to flow. lot's of fragments that start with 'and'."*
**How to apply:**
- **The technique is sound and period-correct** - chained *and* is genuine to
  nineteenth-century vernacular, the KJV-inflected Southern register, and Twain through
  McCarthy. Do not remove it on principle; the "fragments" are in fact complete
  clauses, and the objection is to frequency, not grammar.
- **The failure is monotony of construction, not of length.** `ai-tells.md` §B warns
  about uniform sentence *length*; this is uniform sentence *architecture*. When every
  long sentence is a chain, the passage has two speeds and no way to mark which clause
  matters - every element arrives at the same weight, which flattens exactly the beats
  that need to land.
- Extend sentences by other means as well: subordination, apposition, a colon, a full
  stop where an *and* was. Then keep one chain and put it where accumulation is the
  point.
**Consequences:** `ai-tells.md` §B "Rhythmic uniformity" extended to construction.
**Status:** active

### L-012 - Choose the event; do not arrive at it
**Rule:** Decide what happens before writing how it happens, and test the candidate
against four questions. Execution quality cannot rescue an unchosen event.
**Origin:** Vignette 3 batch 02 ("The wake"), critique 07, 2026-09-08.
**Evidence:** Mark: *"I really like the setup, but it was a little bit of a let down
when basically a ghost combed his hair... I think a part of this process will be coming
up with potential things that could happen in the story and whether that thing is scary
or unsettling."* And, on the eighteen alternatives: *"all of these are better than the
original, which tells me that even pointing out that this should be something we focus
attention on improves the result."*
**How to apply:**
- **The finding is about attention, not about ghosts.** Naming the event as a thing to
  be worked on produced eighteen candidates that all beat the default. Any element that
  is never made an explicit object of attention will be filled with the modal answer,
  written well. Applies to endings, names, objects, weather, and the last line as much
  as to the haunting.
- **The four tests.** An event earns the page only if all four pass:
  1. **Does it touch the living?** Decorating the dead, the house or the past is
     scenery. A ghost that tidies has no appetite.
  2. **Does it implicate the witness?** `craft-principles.md` §6 is notice → intrude →
     implicate; defaults stop at intrude. Is she worse off than before?
  3. **Does it imply more than itself?** A complete, fully picturable event is a closed
     loop. The frightening version leaves a residue - a schedule, a second night, a
     purpose.
  4. **Does it change her future?** If the horror ends when the paragraph does, it was
     an anecdote. (L-006 then prices the change.)
- *"Somebody had combed his hair"* scored nought of four while being some of the
  cleanest prose in the batch. That is the whole lesson.
**Consequences:** `craft/invention-protocol.md` created; `revision-protocol.md` gains
step 0; `ai-tells.md` gains §F.
**Status:** active

### L-013 - Defeat mode collapse structurally; the model does not get to pick
**Rule:** Generate long, quota by category, discard the head of the list, seed from
outside the genre - and hand selection to Mark or to position, never to my own ranking.
**Origin:** Mark's process note, 2026-09-08.
**Evidence:** *"Another thing that I think will be invaluable in our process is creating
lists of things like this, and taking items further down the list to avoid the RL mode
collapse of LLM's and their propensity to do the same thing if not prompted otherwise."*
**How to apply:**
- **The ranker is as collapsed as the generator.** Producing twenty candidates and then
  recommending three re-applies the prior the list was built to escape: the list widens,
  the pick narrows it straight back to the middle. Presenting a shortlist as the
  deliverable is the relapse, not the remedy.
- **Selection order of preference:** (1) Mark picks; (2) by position, default 8+;
  (3) if I must, take the lowest-ranked candidate that passes L-012's four tests, not
  the highest.
- **Twenty minimum, discard the first five unread.** The obvious runs out somewhere past
  item eight. A genuinely right answer in the discarded band is re-derivable; defaulting
  to it is not recoverable.
- **Quota by category, and choose the categories by who is affected** - not by mood.
  Variance came from the six-axis structure of the wake list, not from any instruction
  to be original.
- **Seed from `reference/period/`.** A real object, custom or belief picked *without
  regard to whether it is spooky* is the strongest decorrelator available, because it
  draws from outside the horror-fiction distribution entirely.
- **Write the reader's three guesses first and ban them.** Converts the prior into an
  exclusion list for the price of one line.
- **State the limit honestly:** I cannot sample independently of myself. Two "separate"
  generations in one context are correlated, my sense of what is unusual is unreliable,
  and my randomness is not random. The mechanical steps carry this lesson; my
  self-diversification is a prior, not a control.
**Consequences:** `craft/invention-protocol.md` Part 2 and Part 3 (spent-events log).
**Status:** active

### L-014 - The doctrine is itself a collapse vector
**Rule:** Ration ending shapes the way events are rationed, and require every piece to
break one rule deliberately and say which.
**Origin:** Batch 03 (Fable) read against batches 01-02, 2026-09-08.
**Evidence:** Mark: *"Check out the fable batch entries which were written by a more
powerful LLM. To my eye I don't notice a massive improvement. I think in some ways I
like the stories a bit less."*
**How to apply:**
- **The finding.** Batch 03 was written by a stronger model under thirteen lessons and a
  full invention protocol, and reads as *smoother and less surprising* than batch 01,
  which was written under two or three. A rule followed faithfully by a more capable
  model produces more uniform output, not better output. Capability raises the floor and
  the doctrine lowers the ceiling, and the two meet in the middle.
- **The visible symptom is the audit.** When the rubric can be reverse-engineered from
  the prose - one non-tactile register per rendering, no repeats, an accommodation
  ending, a quotable line per piece - the piece has become an exam answer. Batch 03's
  own pre-flight note reports "no two renderings in one vignette share a register",
  which is a spreadsheet result, not a reason anything is frightening.
- **Ending shapes are rationed.** `craft-principles.md` §7 lists three. No more than one
  in three consecutive pieces uses the same one. L-006's accommodation ending is the
  current offender: five of six in batch 01 r5, four of six in batch 03. **A rule that
  fires every time has stopped being a rule and become a shape.**
- **Do not fix this with another hard rule.** The first version of this lesson required
  *"every piece breaks one rule and says which"*, which Mark's next note correctly
  killed: a mandatory deviation is still a rubric item, and it would have been satisfied
  by breaking something trivial. Replaced by the three mechanisms in **The status of
  these rules** above - kind, basis, and the deviation log. Deviation is permitted
  wherever it works and recorded when it happens; it is never scheduled.
- **Corollary for reading critiques.** The best lines in this project - *"her back had
  never been so much of her before"*, *"the way you would give a man his change"* - were
  discoveries that the rules were written to explain **afterward**. Rules preserve
  discoveries; they do not produce them. Treat every lesson as a floor, never a target.
**Consequences:** `invention-protocol.md` Part 5; `ai-tells.md` §D extended;
`lessons-learned.md` gains the rule-status section and `craft/deviations.md`.
**Status:** active

### L-015 - Grow stories from vignettes; do not outline first
**Rule:** Build a story outward from tested paragraphs. Write the outline last, if at
all.
**Origin:** Mark's process note, 2026-09-08.
**Evidence:** *"I was starting to get ideas for stories while reading the short
paragraphs. The way to write these stories might be to start from snippets like these,
get ideas, and slowly build up like that, instead of trying to come out with the outline
for a story all at once."*
**How to apply:**
- **An outline is where collapse happens first.** The model's plan for a ghost story is
  the modal ghost story, produced before a word is drafted; every well-executed scene
  afterward then serves a generic shape. An outline is also cheap to make and expensive
  to abandon, so the first one survives by default.
- **The signal to grow from is appetite, not quality.** Which vignette makes the reader
  want to know what happened on either side of it - a different question from which is
  best written, and one only Mark can answer. Ask for it explicitly at each scoring
  round.
- **Grow by question.** What had to be true before this? What does it cost tomorrow?
  Each answer is another vignette, run through the same tests.
- **Fill the bible ledger progressively.** An honest TBD beats a guess that then
  constrains what the story could have become.
**Consequences:** `invention-protocol.md` Part 4.
**Status:** active

---

## Open questions for Mark

1. **Length and count.** Rough target: how many stories, and how long a book? My
   working assumption is 10–12 stories, ~45,000 words.
2. **The frame.** Do the photographs sit inside the fiction — the book presented as
   a found album, the stories as the plates' provenance? I lean toward no frame plus
   a short unsigned front-matter note: cheap to write, easy to cut. Note that a
   heavy frame would sit awkwardly with D-001.
3. **Place name.** Standalone means each story invents its own; still worth agreeing
   whether the register is real Louisiana toponymy or invented-but-plausible.
4. **The growth seed.** Which vignette made you want to know what happened on either
   side of it? That is the appetite signal L-015 grows a story from, and it is a
   different question from which is best written.
