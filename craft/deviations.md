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

---

## Standing watch

Prescriptions whose **Fired** count has outrun their **Basis** in `lessons-learned.md`,
and are therefore due a deliberate test — write the version that ignores the rule and
put both in front of Mark:

- **L-006** (basis 1, fired 12) — the most over-trusted rule in the repo. 71% of all
  vignettes end on an accommodation.
- **L-010** (basis 1, fired 6) — wrongness in the approach. Not yet a shape, but
  trending.
