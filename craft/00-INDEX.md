# Craft Folder — Index

The guidance system for writing *Standing Water*. Read in this order before drafting.

| File | What it governs | Authority |
|---|---|---|
| `lessons-learned.md` | Rules distilled from Mark's actual critiques | **Highest** — overrides everything below |
| `craft-principles.md` | Story architecture: escalation, haunt logic, endings | High |
| `style-guide.md` | Prose: voice, sentences, diction, dialogue | High |
| `ai-tells.md` | Failure modes and banned patterns; pre-flight checklist | Mandatory check before delivery |
| `invention-protocol.md` | Choosing what happens, and defeating mode collapse | Process - runs first |
| `revision-protocol.md` | How a critique becomes a revision and a new rule | Process |
| `deviations.md` | Rules broken on purpose, with the argument and Mark's verdict | Evidence |
| `tools/pick.py` | Random selection from a candidate list, outside the model | Tool |
| `vignette-bank.md` | Calibration paragraphs: one lever of dread each, for fast critique rounds | Bench test |

**Force rule:** rules are not equal. Prohibitions are near-absolute; **prescriptions are available and never required**; working rules govern process. See *The status of these rules* at the top of `lessons-learned.md`. If breaking a prescription makes the passage better, break it and log it in `deviations.md`.

**Conflict rule:** later critique beats earlier doctrine. If Mark's feedback
contradicts something written here, the feedback wins, the lesson is logged in
`lessons-learned.md`, and the contradicted document is edited in the same pass so
the repo never holds stale guidance.

**Before inventing:** run `invention-protocol.md`. An event that was never chosen
cannot be rescued by good prose, and it is the cheapest thing in the pipeline to fix.

**Before drafting:** read `lessons-learned.md` and `ai-tells.md` at minimum.
**Before delivering:** run the pre-flight checklist in `ai-tells.md` §E.
