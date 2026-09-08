#!/usr/bin/env python3
"""
pick.py - take the choice away from the model.

The point of L-013 is that a model's ranking is drawn from the same distribution as
its generation, so letting it choose from its own list re-applies the prior the list
was built to escape. This script makes the selection mechanically, from outside.

Usage
-----
    python craft/tools/pick.py CANDIDATES.md                 # 1 pick, discard first 5
    python craft/tools/pick.py CANDIDATES.md -n 3            # 3 picks
    python craft/tools/pick.py CANDIDATES.md --discard 10    # discard first 10
    python craft/tools/pick.py CANDIDATES.md --tail          # weight toward the tail
    python craft/tools/pick.py CANDIDATES.md --seed 41724    # reproduce a past run
    python craft/tools/pick.py CANDIDATES.md --exclude spent.txt

Input format: one candidate per line. Lines are read if they look like list items -
"1. foo", "- foo", "* foo", "| 12 | foo |" - or, failing that, every non-blank line
that is not a markdown heading. Anything after a "#" comment marker is ignored.

Always prints the seed. Log it next to the choice: a pick that cannot be reproduced
cannot be audited, and an unauditable pick is indistinguishable from the model having
chosen after all.
"""

import argparse
import random
import re
import sys
from pathlib import Path

LIST_PATTERNS = [
    re.compile(r"^\s*\*\*([A-Z]?\d+[^*]*)\*\*\s*(.*)"),  # **A1 - Her hair.** rest
    re.compile(r"^\s*\d+[.)]\s+(.*\S)"),                  # 1. foo   /   1) foo
    re.compile(r"^\s*[-*+]\s+(.*\S)"),                    # - foo
    re.compile(r"^\s*\|\s*\d+\s*\|\s*(.*\S?)"),           # | 12 | foo |
]


def parse_candidates(text):
    """Pull candidate lines out of a file.

    Each pattern is tried across the whole file and the one yielding the most matches
    wins. First-match-wins is wrong for real markdown: a candidate file usually also
    contains a short numbered list of criteria or notes, and locking onto that instead
    of the candidates is a silent, dangerous failure - it would quietly narrow the pool
    the script exists to widen.
    """
    lines = [ln.rstrip() for ln in text.splitlines()]
    best = []
    for pat in LIST_PATTERNS:
        items = []
        for ln in lines:
            m = pat.match(ln)
            if not m:
                continue
            item = " ".join(g.strip() for g in m.groups() if g).strip().strip("|").strip()
            if item:
                items.append(item)
        if len(items) > len(best):
            best = items
    if best:
        return best
    # fallback: every non-blank, non-heading line
    return [
        ln.strip()
        for ln in lines
        if ln.strip() and not ln.lstrip().startswith((">", "#", "---", "==="))
    ]


def tail_weights(n, strength=2.0):
    """Linearly rising weights so later items are likelier. strength = last/first."""
    if n == 1:
        return [1.0]
    return [1.0 + (strength - 1.0) * i / (n - 1) for i in range(n)]


def main(argv=None):
    ap = argparse.ArgumentParser(description="Pick candidates at random, not by preference.")
    ap.add_argument("file", help="file containing the candidate list")
    ap.add_argument("-n", "--num", type=int, default=1, help="how many to pick (default 1)")
    ap.add_argument("--discard", type=int, default=5,
                    help="drop this many from the head of the list unread (default 5)")
    ap.add_argument("--tail", action="store_true",
                    help="weight selection toward later items")
    ap.add_argument("--strength", type=float, default=2.0,
                    help="with --tail, how much likelier the last item is than the first")
    ap.add_argument("--seed", type=int, default=None,
                    help="reproduce a previous run")
    ap.add_argument("--exclude", metavar="FILE",
                    help="file of already-spent items; candidates containing any of "
                         "these lines (case-insensitive substring) are dropped")
    args = ap.parse_args(argv)

    path = Path(args.file)
    if not path.exists():
        sys.exit(f"pick.py: no such file: {path}")

    items = parse_candidates(path.read_text(encoding="utf-8"))
    if not items:
        sys.exit(f"pick.py: no candidates found in {path}")

    total = len(items)
    pool = items[args.discard:]
    dropped_head = min(args.discard, total)

    excluded = 0
    if args.exclude:
        spent = [
            ln.strip().lower()
            for ln in Path(args.exclude).read_text(encoding="utf-8").splitlines()
            if ln.strip()
        ]
        kept = [it for it in pool if not any(s in it.lower() for s in spent)]
        excluded = len(pool) - len(kept)
        pool = kept

    if not pool:
        sys.exit("pick.py: nothing left to pick from after discard/exclude")

    n = min(args.num, len(pool))
    seed = args.seed if args.seed is not None else random.randrange(2**31)
    rng = random.Random(seed)

    if args.tail:
        weights = tail_weights(len(pool), args.strength)
        picks, remaining, rw = [], list(pool), list(weights)
        for _ in range(n):
            chosen = rng.choices(remaining, weights=rw, k=1)[0]
            i = remaining.index(chosen)
            picks.append(chosen)
            remaining.pop(i)
            rw.pop(i)
    else:
        picks = rng.sample(pool, n)

    print(f"file      : {path}")
    print(f"candidates: {total}  (head {dropped_head} discarded"
          + (f", {excluded} excluded" if excluded else "") + f", {len(pool)} in pool)")
    print(f"mode      : {'tail-weighted x' + str(args.strength) if args.tail else 'uniform'}")
    print(f"seed      : {seed}        <-- log this next to the choice")
    print()
    for i, p in enumerate(picks, 1):
        print(f"{i}. {p}")


if __name__ == "__main__":
    main()
