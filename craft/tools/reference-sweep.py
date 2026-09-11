#!/usr/bin/env python3
"""
reference-sweep.py — mechanical referent check for a draft.

    python craft/tools/reference-sweep.py stories/03-ti-jean/draft-02.md \
        --pov Elmire --thing figure

WHY THIS IS A SCRIPT AND NOT A CHECKLIST ITEM
---------------------------------------------
Reading cannot find these faults. The writer resolves a pronoun against *intent* — the
notes, the plan, who the scene is about — and the reader resolves it against the *nearest
available noun*. Those two operations disagree, and no amount of care closes the gap,
because carefulness does not remove the context. So the method removes the context
instead: extract each pronoun with the candidate that precedes it, and judge the rows in
isolation, without the paragraph's meaning in front of you.

Story 03 had fifteen gendered-pronoun faults and four haunting-pronoun faults in 3,265
words. Careful reading, a critique round and a fresh-context review found one of them
between them. A triage list like this one found the rest.

It over-flags on purpose. False positives cost a glance; the row dismissed as noise in
story 03 — "A woman, with wings" competing with Elmire — was the worst collision in the
draft. Do not skim the output. Judge every row, in reverse order, so narrative momentum
cannot supply a referent.

WHAT IT CHECKS
--------------
  1. NEAREST CANDIDATE for every gendered pronoun, flagged where that is not the expected
     referent — which is the whole fault: "One afternoon in July she was at her own plot",
     nearest candidate `mare`.
  2. POSSESSIVE-ONLY ANTECEDENT (L-005). "Elmire's brother" leaves a later bare "she" with
     nothing to attach to. The name is on the page, which is exactly why proofreading
     misses it. Purely syntactic; no judgment required.
  3. SECTION-BREAK RESET (L-005). A reader who has just crossed white space is not still
     holding a pronoun. Name the subject in the first sentence after a break.
  4. it / its — every occurrence, and whether the haunting's own noun (--thing) is nearest.
     Withholding a *name* is not withholding an *explanation*: the haunting has a neutral
     noun that dates nothing and accounts for nothing, so an unanchored pronoun for it buys
     no subtlety and only charges a decode (L-003).
  5. ADJACENT SENTENCES sharing a pronoun form, where one may be the haunting and the other
     ordinary: "He said it was watching at her. / Elmire let it go."

Gender is not assumed. It is inferred per name from the pronouns that follow it, so a
character called Father Ancelet does not end up competing for "she". Names the inference
cannot settle are left in both pools, which over-flags rather than under-flags.

Highest-yield place to look: anything converted from first person, where the original "I"
needed no antecedent at all (L-025).
"""

import io
import re
import sys
from collections import Counter, defaultdict

FEM = r"\b(she|her|hers|herself)\b"
MASC = r"\b(he|him|his|himself)\b"

ROLE_F = ["aunt", "mother", "sister", "daughter", "wife", "grandmother", "girl", "woman",
          "widow", "housekeeper", "mare", "sister-in-law", "cousin", "nun", "sister"]
ROLE_M = ["father", "brother", "son", "husband", "grandfather", "boy", "man", "sexton",
          "priest", "doctor", "drummer", "child", "baby"]

TITLES = r"(?:Father|Madame|Mademoiselle|Monsieur|Tante|Nonc|Mrs|Mr|Dr|Widow)"

STOP = set("""
January February March April May June July August September October November December
Sunday Monday Tuesday Wednesday Thursday Friday Saturday
All Saints Mass Easter Lent Christmas Toussaint God Lord Church
Father Madame Mademoiselle Monsieur Tante Mrs Mr Dr Widow Nonc
""".split())


def sections(path):
    s = io.open(path, encoding="utf-8").read()
    m = re.search(r"^## ", s, re.M)
    if m:
        s = s[m.start():]
    out = []
    for block in s.split("\n\n"):
        b = " ".join(block.split())
        if b:
            out.append(("BREAK", b) if b.startswith("##") else ("P", b))
    return out


NAME_RE = re.compile(
    TITLES + r"\s+[A-ZÀ-Þ][\w'’\-]+"
    r"|\b[A-ZÀ-Þ][a-zà-þ'’]+(?:-[A-ZÀ-Þ]?[a-zà-þ'’]+)?\b"
)


def detect_names(text):
    """Capitalised forms that occur at least once mid-sentence and are not stopwords."""
    counts = Counter()
    for m in NAME_RE.finditer(text):
        raw = m.group(0)
        pre = text[:m.start()].rstrip()
        if pre and pre[-1] not in ".!?\"'":
            base = re.sub(r"['’]s$", "", raw)
            if base.split()[0] in STOP or base in STOP:
                continue
            if len(base) < 3:
                continue
            counts[base] += 1
    # drop any name wholly contained in a longer one (Ancelet inside Father Ancelet)
    keep = []
    for n in sorted(counts, key=lambda x: -len(x)):
        if not any(n != k and n in k for k in keep):
            keep.append(n)
    return sorted(keep, key=lambda n: -counts[n])


def infer_gender(text, names):
    """Assign each name F/M/? from the pronouns that follow it within 90 chars."""
    tally = defaultdict(Counter)
    for n in names:
        for m in re.finditer(r"\b" + re.escape(n) + r"\b", text):
            window = text[m.end(): m.end() + 90]
            tally[n]["F"] += len(re.findall(FEM, window, re.I))
            tally[n]["M"] += len(re.findall(MASC, window, re.I))
    out = {}
    for n in names:
        f, mm = tally[n]["F"], tally[n]["M"]
        out[n] = "F" if f > mm * 1.5 else "M" if mm > f * 1.5 else "?"
    return out


def nearest(scope, pool):
    best = None
    for n in pool:
        for m in re.finditer(r"\b" + re.escape(n) + r"\b", scope, re.I):
            tail = scope[m.end(): m.end() + 3]
            poss = tail.startswith("'s") or tail.startswith("’s")
            if best is None or m.start() > best[0]:
                best = (m.start(), n, poss)
    return best


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    path = sys.argv[1]

    def opt(flag, default=None):
        return sys.argv[sys.argv.index(flag) + 1] if flag in sys.argv else default

    thing = opt("--thing", "figure")
    blocks = sections(path)
    body = " ".join(b for k, b in blocks if k == "P")
    names = detect_names(body)
    gender = infer_gender(body, names)
    pov = opt("--pov", names[0] if names else None)

    fem_pool = [n for n in names if gender[n] in "F?"] + ROLE_F
    masc_pool = [n for n in names if gender[n] in "M?"] + ROLE_M
    masc_names = [n for n in names if gender[n] == "M"]

    print("=" * 78)
    print("REFERENCE SWEEP  %s" % path)
    print("  F: %s" % ", ".join(n for n in names if gender[n] == "F"))
    print("  M: %s" % ", ".join(masc_names))
    print("  ?: %s" % ", ".join(n for n in names if gender[n] == "?"))
    print("  pov=%s   haunting noun=%s" % (pov, thing))
    print("=" * 78)
    print("\n### 1. NEAREST CANDIDATE per gendered pronoun\n")

    faults = 0
    prev_p = ""
    after_break = False
    for idx, (kind, para) in enumerate(blocks):
        if kind == "BREAK":
            after_break = True
            continue
        scope = prev_p + "  ||  " + para
        offset = len(prev_p) + 6
        live_m = {n for n in masc_names if re.search(r"\b" + re.escape(n) + r"\b", scope, re.I)}

        for label, pron, pool in (("F", FEM, fem_pool), ("M", MASC, masc_pool)):
            for m in re.finditer(pron, para, re.I):
                hit = nearest(scope[:offset + m.start()], pool)
                if not hit:
                    continue
                _pos, cand, poss = hit
                flags = []
                if label == "F" and pov and cand.lower() != pov.lower():
                    flags.append("NEAREST IS '%s', not %s" % (cand, pov))
                if poss:
                    flags.append("POSSESSIVE-ONLY: '%s's' is not an antecedent" % cand)
                if after_break and m.start() < 140:
                    flags.append("AFTER SECTION BREAK — name the subject")
                if label == "M" and len(live_m) >= 3:
                    flags.append("%d male names live: %s" % (len(live_m), sorted(live_m)))
                if not flags:
                    continue
                faults += 1
                print("[p%02d %s] '%s'  <- %s" % (idx, label, m.group(0), cand))
                for f in flags:
                    print("        %s" % f)
                print("        ...%s..." % para[max(0, m.start() - 55): m.start() + 32])
        after_break = False
        prev_p = para

    print("\n### 2. it / its  —  '??' = '%s' is not the nearest noun (L-003)\n" % thing)
    for idx, (kind, para) in enumerate(blocks):
        if kind == "BREAK":
            continue
        for m in re.finditer(r"\bits?\b", para):
            pre = para[max(0, m.start() - 90): m.start()]
            mark = "  " if thing in pre[-55:].lower() else "??"
            print("[p%02d]%s ...%s[%s]" % (idx, mark, pre[-62:], para[m.start(): m.start() + 24]))

    print("\n### 3. ADJACENT SENTENCES sharing a pronoun form — split referents?\n")
    for idx, (kind, para) in enumerate(blocks):
        if kind == "BREAK":
            continue
        sents = re.split(r"(?<=[.!?])\s+", para)
        for a, b in zip(sents, sents[1:]):
            for p in ("it", "she", "he", "her", "him", "his"):
                r = r"\b" + p + r"\b"
                if re.search(r, a, re.I) and re.search(r, b, re.I):
                    print("[p%02d] '%s'\n   A: %s\n   B: %s" % (idx, p, a, b))
                    break

    print("\n%d flagged rows in section 1. Read in reverse. Judge every row." % faults)


if __name__ == "__main__":
    main()
