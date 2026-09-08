# Revision Protocol

The loop this repo exists to run.

```
   draft ──► Mark reads ──► critique ──► revision + lesson extraction ──► next draft
     ▲                                                                       │
     └───────────────────────────────────────────────────────────────────────┘
```

## 1. Draft

Claude writes `stories/<slug>/draft-01.md` using the craft folder. Frontmatter
records which plate it belongs to, the haunt-logic, and the intended ending type,
so the collection ledger stays accurate.

## 2. Critique

Mark reads and writes `stories/<slug>/critique-01.md`. Anything goes: margin notes,
a paragraph, three bullet points, "this bit is fake." Line references are useful but
not required.

Most useful signals, if you feel like being systematic:
- Where you got bored, and the exact line where it started.
- Where you stopped believing it.
- Any sentence that sounded like a machine wrote it.
- Whether the ending earned itself.

Blunt is better than balanced. Praise is only useful when it identifies something to
repeat.

## 3. Extract

Before revising, Claude converts the critique into generalised rules and appends
them to `craft/lessons-learned.md` with IDs. Any craft doc the feedback contradicts
is edited in the same pass. **Extraction happens before revision** — otherwise the
lesson gets applied to one story and lost.

## 4. Revise

New file, `draft-02.md`; the previous draft is never overwritten, so the progression
stays readable. The revision opens with a short changelog noting which lesson IDs
drove which changes.

## 5. Close the round

Story frontmatter status advances: `draft` → `revising` → `polished` → `final`.
When a story reaches `final`, it is copied into `manuscript/` for assembly.

## Periodic maintenance

Every few rounds, Claude re-reads `lessons-learned.md` and consolidates: merges
duplicate rules, marks superseded ones, promotes stable rules into `style-guide.md`
or `craft-principles.md`. The lessons file should stay sharp, not become a log.
