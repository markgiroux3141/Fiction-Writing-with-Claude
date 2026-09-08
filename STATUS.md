# Status

**Read this first in a fresh session.** It is the only file that tracks *position*
rather than doctrine. Last updated 2026-09-08.

`CLAUDE.md` routes to everything else and loads automatically. Start
`craft/lessons-learned.md` at its opening section, *The status of these rules* —
prohibitions are near-absolute, **prescriptions are available and never required**, and
the effect on the page outranks the rule.

---

## Where the project is

**Phase: calibration, ending. First story, beginning.**

No story has been drafted. Seventeen single-paragraph vignettes have, in three batches,
and the entire craft system was extracted from Mark's critiques of them.

| Batch | Model | Vignettes | Status |
|---|---|---|---|
| 01 (`batch-01.md` → `-r6.md`) | Opus | 6 | #1 scored across four rounds and **approved at r4**. #2–5 rewritten to r6, **unscored**. #6 unrevised, unscored. |
| 02 (`batch-02.md`) | Opus | 5 | #3 critiqued (event rejected). #1, #2, #4, #5 **unscored**. |
| 03 (`batch-03-fable.md`) | **Fable 5.1** | 6 | Read by Mark; verdict *"not a massive improvement, in some ways I like them less."* Produced L-014. Individually unscored. |

## The one thing to be honest about

**Fifteen rules, and nearly all of them are `Basis: 1`.** Eight came from a single
paragraph — vignette 1 of batch 01. Twelve of seventeen vignettes end on the same shape
because one rule extracted from one line Mark liked has fired twelve times.

The system is over-built relative to its evidence. **The correct next move is to
generate evidence, not doctrine.** Adding rules right now is the trap, not the work.

---

## Open, and blocking

1. **Nothing since vignette 1 has been scored.** Sixteen vignettes are waiting on
   *did anything land physically / which sentence did the work / which sentence is a
   lie.* Until some of them are, the doctrine is a hypothesis with one data point.
2. **The growth seed is unchosen.** L-015 grows a story from whichever vignette made
   Mark want to know what happened either side of it — an appetite signal, not a
   quality signal, and only he can give it.
3. **The wake event is unchosen.** `craft/vignettes/batch-02-wake-options.md` holds 21
   candidates. Mark picks, or `craft/tools/pick.py` draws.
4. **Four open questions** at the foot of `craft/lessons-learned.md`: length and story
   count, the album frame, place-name register, and the growth seed.

## Not blocking — do not build these

- More vignettes. There are sixteen unscored already.
- More rules. See above.
- More craft docs. There are eight plus a tool.

---

## What is actually untested

Everything proven so far was proven at ~200 words. A story is 2,500–5,000. These are
unknowns that **only writing a story will resolve**, and they are the argument for
starting one rather than preparing further:

- **Escalation across length.** `craft-principles.md` §6 (notice → intrude →
  implicate) has never run longer than a paragraph.
- **Sustaining a character.** Every vignette protagonist exists for 200 words. None has
  had to remain interesting for twenty pages.
- **Scene transition and time management.** Completely untested.
- **Dialogue at length.** Two short exchanges exist, both unscored.
- **One impossible thing across a story.** Trivial in a paragraph; the real discipline
  is over 4,000 words.
- **Whether the prohibitions survive scale.** L-004 and L-011 were derived from
  paragraph-level reading and may behave differently across a chapter.

---

## Next actions

**Mark:** score some vignettes; name the growth seed; answer as many open questions as
he cares to. Any one of these unblocks the story.

**Claude:** on Mark's signal, run `craft/invention-protocol.md` step 0 for story 01 —
rule off-page, banned guesses, ≥20 candidates, discard 5, `pick.py` or Mark selects, log
the seed — then draft into `stories/<nn>-<slug>/` from `stories/_template.md`.

**Working method agreed 2026-09-08:** build the first story hand in hand with Mark and
develop the pipeline against it, rather than building more pipeline first.

---

## Priming a fresh session

`CLAUDE.md` loads automatically and now points here. If more is needed — a subagent, a
different tool, or a session that has drifted:

> Read `STATUS.md`, then `craft/lessons-learned.md` in full starting with *The status of
> these rules*, then `craft/ai-tells.md` §E and §F. Lessons-learned outranks every other
> doc, but prescriptions in it are optional and the effect on the page outranks all of
> it. We are starting story 01 hand in hand; run `craft/invention-protocol.md` step 0
> before any prose.

**The tells that a session has not read the material:** it presents a shortlist of its
own recommendations instead of a long list (L-013), it treats every lesson as binding
(rule-status section), or it hands over a draft without reporting the eleven-item
pre-flight honestly (`ai-tells.md` §E).
