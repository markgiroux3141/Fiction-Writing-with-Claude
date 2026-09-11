# Fresh-context review prompt

For `revision-protocol.md` step 1b (L-020). Start a **new session**, attach or paste the
story file, and send the prompt below verbatim.

## The one rule that must not be broken

**Give it the story and nothing else.** No craft folder, no `lessons-learned.md`, no
`notes.md`, no critique history, no mention that a rule system exists. A reviewer holding
the doctrine grades against the rubric, which is the L-014 failure arriving with a
clipboard. Story 01's review diagnosed the visible architecture *because it did not know a
rubric existed*. The ignorance is the instrument.

Do not tell it the story is AI-written until after its structural notes — knowing that
skews it toward hunting for tells instead of reading.

---

## The prompt

> Read this short story and give me a hard, specific critique. I want to know whether it
> works, not whether it is competent.
>
> Answer these, in this order:
>
> 1. **Where did you stop believing it?** Name the line. Not where it was implausible in
>    principle — where *you* checked out.
> 2. **What does the story state that it has already shown?** Quote any sentence whose
>    job is to make sure the reader kept up, or to make an earlier moment hold up. Be
>    ruthless; this is the commonest fault.
> 3. **What did it touch and then flinch from?** Is there a darker or more implicating
>    version of something it raises and then resolves too comfortably? Quote the sentence
>    where the nerve was there and the story stepped back.
> 4. **Does the architecture show?** Repetitions, symmetries, an escalation that arrives
>    too neatly, section breaks at regular intervals, variations that read as a set. Say
>    where it feels designed rather than lived.
> 5. **What obligations does the setting take on and not pay?** Anything the period,
>    place or social arrangement makes a reader expect that the narration never looks at.
> 6. **The ending.** Does it earn itself, or does it arrive because the story needed to
>    finish?
> 7. **Best beat in the piece**, quoted, and say why. Praise is only useful if it
>    identifies something to repeat.
>
> Then, only after all of the above: does any of it read as machine-written, and where?
>
> Constraints on you: quote lines rather than paraphrasing. Do not rewrite anything — I
> want the diagnosis, not a revision. Do not soften. If the whole thing is fine, say so
> plainly and briefly rather than manufacturing notes.

---

## Triage on the way back

- Save the raw output to `stories/<slug>/review-of-draft-NN.txt`.
- Triage into `stories/<slug>/critique-NN.md` under four headings: **act / act but
  narrower than the note / not a draft edit / declined with reasons.**
- **Candidate notes, not authority.** Aesthetic rulings are Mark's. Nothing from a review
  enters `lessons-learned.md` on its own.
- **Expect roughly half to land.** Story 01: four of seven actionable, one declined
  outright, one collection-level rather than story-level.
- **Do not let it drive prose polish.** Its value is architecture, complicity and
  consistency. On story 01 it found no bad sentences, because there were none left.
- **Watch for regression pressure.** A fresh reviewer will sometimes ask for something a
  previous round deliberately removed. The rejection history in `critique-*.md` outranks
  it.
