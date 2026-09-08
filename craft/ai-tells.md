# AI Tells & Failure Modes

A checklist to run against every draft before it goes to Mark. These are the
patterns that make generated prose identifiable, and most of them are *default*
behaviours — they appear unless actively suppressed.

Treat this as a pre-flight checklist, not background reading. Grep for the literal
phrases where possible.

---

## A. Banned phrases (literal)

Search for these. Zero tolerance.

- "little did (he/she/they) know"
- "unbeknownst to"
- "it was then that"
- "she couldn't shake the feeling"
- "a shiver ran down (his/her) spine"
- "(his/her) blood ran cold"
- "a chill ran through"
- "sent a chill"
- "the air grew cold" / "the temperature dropped" as the primary supernatural signal
- "a mixture of X and Y" / "a combination of X and Y"
- "in that moment"
- "little more than"
- "something was deeply wrong"
- "an inexplicable sense of"
- "the silence was deafening"
- "a testament to"
- "little did the house know" and all inanimate variants
- "copper and rot" / "iron and copper" (the default AI smell)
- "danced" for firelight, shadows, dust motes, or anything else
- "the darkness seemed to breathe"
- "as if it had always been there"
- "and then, silence."

## B. Structural tells

**The tricolon habit.** Three adjectives, three clauses, three examples — endlessly.
"It was cold, dark, and utterly still." Cut to one, occasionally two. If a sentence
has three of anything, justify it or kill one.

**Rhythmic uniformity.** Paragraphs of near-identical length, sentences of
near-identical length. Machine prose breathes evenly. Human prose gasps and rambles.

Uniformity of **construction** counts too, and is harder to see: if every long sentence
is extended the same way - usually a chain of *and* clauses - the passage has two speeds
and no way to mark which clause matters. Extend by other means as well (subordination,
apposition, a colon, a full stop where the *and* was), and keep the chain for where
accumulation is the point. (L-011.)

**The balanced ending sentence.** "And in the standing water, something waited."
The final line that lands on a portentous noun with a trailing verb. It is the
default cadence and it is exhausted.

**Restate to negate.** "The basket was on the wrong hip. It was not on the wrong
hip." Repetition signals intensification; reversal is information, so the form fights
the content — and the contradiction stands unresolved for the length of the repeat.
Use a pro-form ("It wasn't") and resolve within a clause. (L-005.)

**Fragment for effect.** "The door opened. Slowly." Once per story, maximum.

**Symmetrical scene structure.** Every scene the same length with the same
setup-tension-sting shape. Vary the shapes: end a scene mid-conversation, open one
in the middle of an action.

**The summary paragraph.** A closing paragraph that tells the reader what the story
meant. Delete it. Always.

## C. Content tells

**Over-explanation.** The impulse to make the haunting coherent — a backstory that
accounts for every manifestation. Resist. See craft-principles §3.

**Emotional signposting.** Naming the feeling immediately after the event that
caused it. Trust the event.

**The knowledgeable local.** An old-timer who exists to deliver the town's dark
history in one scene. If exposition is needed, let the character find it in a
document, incompletely, and misread part of it.

**Tidy moral resolution.** The ghost is laid to rest because someone did the right
thing. Ghost stories are not about justice being served.

**Everything is significant.** Every object mentioned turns out to matter. Real
texture requires details that go nowhere.

**On-the-nose naming.** Characters named Grimm, Crowe, Blackwood, Ashe. Towns named
Ravenshollow. Use plain regional names: Dell, Fontenot, Marsh, Ivey, Cobb.

**The unasked question.** A sentence that defends, excuses, or corrects something
nobody has raised — "which was a fault in the building and not in her." The reader
hunts for the argument it belongs to, finds none, and registers the prose as odd
without being able to say why. Includes the narrator's witty aside placed just before
a fright. (L-004.)

**Decoding tax.** Obliquity mistaken for restraint: "It was wet there" for sweat. If
the reader has to work out the referent, they have left the character to solve a
puzzle. Plain word, more specific. (L-003.)

**The tactile default.** Every rendering of fear reaching for skin: hair rising,
crawling, prickling, gooseflesh, cold spots. The register is spent and a fresher
adjective does not repair it — change register instead (proprioceptive, spatial,
cognitive, motor, temporal). Audit by tagging each fear-rendering in a passage; two in
the same register means one moves. (L-007.)

**Over-rendering the body.** Fear narrows perception. A character who notices
individual hairs releasing in sequence is not frightened, she is being examined.
Blunt physical fact, then movement. (L-001 ceiling.)

**Generic gothic furniture.** Candles, flickering lamps, howling wind, storms
arriving exactly on cue, grandfather clocks striking midnight. Every one of these
must earn its place or be replaced with something specific to *this* place.

**Weather as mood ring.** Rain when sad, storm when scared. Let the weather be
indifferent — a bright hot morning is a better setting for the worst scene.

## D. The "competent but dead" problem

The most dangerous failure is not a bad draft. It is a draft that is clean,
well-paced, correctly structured, and completely inert — no line that surprises,
no observation that only this narrator would make, nothing risked.

Symptoms:
- Nothing in it is strange except the ghost.
- No sentence you would quote to someone.
- The narrator has no opinions about anything other than the plot.
- You could swap the protagonist with the protagonist of another story and lose
  nothing.

Cure: give the narrator a specific, slightly unreasonable preoccupation — a trade,
a grudge, a way of counting things — and let it colour the observation of every
scene, including the frightening ones.

**The rubric tell (added 2026-09-08).** A late-stage variant that appears only once the
craft docs are good: prose from which the checklist can be reverse-engineered. Every
fear-rendering in a different register, an accommodation ending, exactly one quotable
line, no repeated construction — all boxes ticked and nothing risked. The piece is
answering an exam. Symptoms: the handover note can audit itself cleanly, and no sentence
would have surprised the person who wrote the rules. Cure: ration the prescriptions (see *The status of these
rules* in `lessons-learned.md`), and log deviations in `craft/deviations.md` when they
earn their place. Do not schedule them. (L-014.)

## F. Modal events

The event-level equivalent of the banned phrases in §A: the haunting a model reaches
for when nobody has decided what happens. Banned by default; usable only if the
`invention-protocol.md` four tests are argued explicitly.

- the corpse that is warm, or has shifted slightly
- the figure standing at the foot of the bed
- **the ghost that tidies, arranges, or grooms** (our own failure - batch 02 #3)
- footsteps in the hall that stop outside the door
- the reflection that lags or blinks late
- a child's laughter with no child
- the photograph with an extra figure in it
- the door that will not stay shut
- writing that appears in dust, steam, or on glass
- the rocking chair rocking
- the handprint on the inside of the window
- the clock stopped at the hour of death
- the dog that will not enter a room

**Audit of our own bank, run 2026-09-08.** Several entries in `vignette-bank.md` are
themselves modal and were written before this section existed: **E1 (the basin
reflection)** and **the photograph's extra hand** are on the list above outright; **A2
(the chair settles)** and **A3 (the dog will not go down the hall)** are near
neighbours. Rewrite or retire them before use. The bank was generated by the same
process it is meant to correct.

## E. Pre-flight checklist

Before any draft is handed over:

1. Grep the banned-phrase list. Zero hits.
2. Read the last paragraph alone. Does it explain or summarise? Cut it.
3. Count sentences in three consecutive paragraphs. Is the variance real?
4. Find every named emotion. Replace at least half with behaviour.
5. Is there more than one impossible thing? Cut back to one.
6. Does any character explain the haunting? Remove.
7. Name three details that serve no plot function. If you cannot, the world is too
   tidy.
8. Is there one sentence worth quoting? If not, the draft is not done.
9. At each moment of fear, does the body go first? If the character knows before she
   feels, or if the only rendering is behaviour, the passage is under-rendered.
   (L-001.)
10. Re-read anything that feels merely *odd* rather than wrong. It is almost always
    bookkeeping: a referent to decode, an argument never made, or a contradiction left
    hanging. (L-003 / L-004 / L-005.)
11. Was the central event *chosen*? Score it against the four tests in
    `invention-protocol.md` and check it against §F. An unchosen event cannot be
    rescued by good prose. (L-012.)
