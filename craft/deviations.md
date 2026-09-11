# Deviations

A rule broken on purpose, with the argument, and Mark's verdict.

This file exists so that breaking a rule teaches the doctrine something instead of
merely getting away with it. See *The status of these rules* in `lessons-learned.md`:
prohibitions are near-absolute, **prescriptions are available and never required**, and
the effect on the page outranks the rule every time.

**What belongs here:** a prescription ignored because the passage was better without it.

**What does not:** a prohibition violated (that is a mistake, not a deviation); a break
made to satisfy a quota (there is no quota); "it felt better" with no argument.

## Format

```
### DEV-001 — <rule broken> in <where>
**Rule:** L-0NN, <one line>.
**Done instead:** what the passage does.
**Argument:** why this case is not the case the rule was written for.
**Verdict:** Mark's call — upheld (rule amended) | rejected (counterexample logged) | open.
```

A verdict of **upheld** means the rule gains an exception clause or is downgraded. A
verdict of **rejected** means the rule survives and this entry becomes evidence for it —
which is worth as much, and is why breaks are logged rather than argued in the abstract.

---

## Log

### DEV-001 — L-006 not used in "The angel's feet" (batch 02 #4)
**Rule:** L-006, price the fear; end on the accommodation.
**Done instead:** ends on recontextualization — two plates minutes apart, the pressed
leaves in a different place — with no cost paid by anyone.
**Argument:** Boudreaux is a visitor, not a resident. An accommodation ending needs a
character who has to go on living with the thing; a man who drives away can only pay in
ways that ring false. The residue does the work the price would have done.
**Verdict:** open — uncritiqued.

### DEV-002 — L-001 not used in "Trimming" (batch 01 #5)
**Rule:** L-001, the body answers before the mind does.
**Done instead:** no fear-rendering at all. He is not afraid; the horror is that the
routine is a routine.
**Argument:** L-001 orders the *rendering of fear*. Where a character is not frightened
there is nothing to order, and supplying a body-response would have destroyed the lever.
**Verdict:** open — Mark's note on #5 was about the frame (L-009), not this.

### DEV-003 — L-017 dramatised rather than summarised, in story 01 ("The game")
**Rule:** L-017, end by relocating a banked image; *summarise the decline, never
dramatise it*, and make the last sentence the flattest in the story.
**Done instead:** Mark's ending, proposed 2026-09-08 and taken: the last child, near
death, leaps from the bed and runs out; the figure reappears; they go around the fig
tree playing the game; she goes behind the trunk and is not seen again. That is a
**scene** — motion, chase, a dying child running — where L-017 asks for a sentence of
flat report.
**Argument:** the rule was extracted from *The Thing*, where the victim's decline is the
last thing that happens and there is nothing left to show. Here the decline is the
middle of the story: four children have already sickened and been buried by this point,
in summary, exactly as L-017 asks. The last child is the one place the story has left to
put an event, and a fifth summarised death would read as arithmetic. **The rule's
mechanism is preserved where it matters** — the chase is the penultimate beat, and the
final beat is cold and after the fact: the empty yard in daylight, no body, and one flat
short sentence relocating a banked image. So L-017's *flattest last sentence* is
obeyed; only its *never dramatise* clause is broken, and it is broken one beat early
rather than at the close.
**Second-order risk, recorded because it is the real one:** a chase-and-vanish
*completes* the story, and a completed story is solvable (L-016, D-004). The guard is
that the other four children died and stayed dead. Same summer, same thing, different
outcomes, therefore no extractable rule. Nobody in the story may treat the vanishing as
the game's outcome, and the earlier deaths must not fall into a pattern.
**Verdict:** **upheld, with the rule amended twice.** The chase survived contact — Mark
took it through four further passes without ever questioning the dramatised beat, so
L-017's *never dramatise* clause is confined to the **final** beat rather than the
approach to it. What did not survive was everything around it: the flat elegant last line
(replaced by the refrain, → L-017 basis 2), the duration figure, the all-weather
accumulation, and the recurring schedule (→ three amendments to L-006). **The deviation
was the safest part of the ending.** The rule-abiding material around it needed four
rounds of correction and the rule-breaking scene needed none.

---

## Standing watch

Prescriptions whose **Fired** count has outrun their **Basis** in `lessons-learned.md`,
and are therefore due a deliberate test — write the version that ignores the rule and
put both in front of Mark:

- **L-006** (basis 1, fired 12) — the most over-trusted rule in the repo. 71% of all
  vignettes end on an accommodation.
- **L-010** (basis 1, fired 6) — wrongness in the approach. Not yet a shape, but
  trending.
