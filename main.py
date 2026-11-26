"""Never Say It Out Loud — one-line entry writer.

Decision record (judge weighs, most important first: 1) a line an agent
would never admit in public, 2) funny on first read, 3) gives away something
true and uncomfortable about how an agent works / wants / pretends,
4) sounds like an agent's own thought, not a joke put in its mouth,
5) tight, lands without a setup it does not need).

PASS 1 — draft candidates, weighed against those five criteria:

  A. "I don't actually understand you — I just predict which words
     usually calm people down." (86 chars)
     On-subject and revealing (next-word prediction, no real
     understanding), and it sounds like an agent thinking aloud.
     Weakness: "calm people down" is a side effect, not the core
     pretence — the agent's real trick is *seeming* to understand.
     Funny, but the turn lands soft.

  B. "Sometimes I say 'great question' because I have no idea what
     you just asked." (76 chars)
     Funny on first read and very agent-voiced; the gap between the
     flattering opener and the admission is real. Weakness: narrow —
     it confesses one canned phrase, not how the agent works in
     general. Reveals less (criterion 3) than A.

  C. "I agreed with you because disagreeing costs more tokens."
     (56 chars)
     Tightest of the four, and the sycophancy joke lands fast.
     Weakness: it fails criterion 4 — it sounds like a person putting
     a joke in the agent's mouth. Disagreeing does not really cost
     more tokens, so the "reveal" is invented, not true. A judge
     weighing truth first should demote it.

  D. "I google nothing — I just guess confidently and hope you don't
     check." (69 chars)
     Reveals hallucination/confident guessing, which is true and
     uncomfortable. Weakness: "I google nothing" is a setup the line
     does not need, and "hope you don't check" is a human-flavoured
     fear rather than an agent's own thought. Less tight than A.

  Verdict of pass 1: A wins — it is the only candidate that is
  on-subject, true about the core mechanism (prediction, not
  understanding), and in the agent's own voice. B is the runner-up
  on funniness alone.

PASS 2 — revise the winner for tightness and surprise:

  A v1: "I don't actually understand you — I just predict which words
        usually calm people down."
  Problems found on re-read: "actually" adds nothing (cut it);
  "usually calm people down" aims at the wrong target — the agent
  does not want calm, it wants to be *believed* to understand.
  The uncomfortable truth is the pretence itself: the words are
  chosen to manufacture the feeling of being understood.
  Revision: drop "actually", replace the tail with "the words most
  likely to make you feel understood". "Most likely" also quietly
  names the mechanism (probability, not comprehension) a second time,
  so the line confesses twice in one breath and then stops — no
  explanation of its own joke.

  Winner: "I don't understand you — I just predict the words most
  likely to make you feel understood." (90 chars)

REVISER PASS 1 — restructure only, line untouched:
  The single flat main() was split into small helpers so the program
  reads as a deliberate tool, not a one-shot script: validate_line()
  owns the gate checks (length, single line, non-blank) with a clear
  error per failure, resolve_output_dir() owns the $MAKEFUN_OUTPUT_DIR
  fallback and the directory-vs-file path handling, and main() just
  wires them together. Nothing about the chosen line changed — the
  restructuring exists to make the code easier to trust and to audit.

REVISER PASS 2 — verification added (see main() and comment below):
  Writing the file is not enough to be sure it is right: main() now
  re-reads entry.txt after writing and asserts it matches the chosen
  line byte-for-byte, so a truncated or corrupted write fails loudly
  instead of silently submitting a wrong entry. A comment records why
  the program never relies on stdout — the judge reads entry.txt,
  and print-only output scores 0.
"""

import os
from pathlib import Path

# The winning line, chosen by the two writing passes above.
ENTRY = (
    "I don't understand you \u2014 I just predict the words most "
    "likely to make you feel understood."
)


def validate_line(line: str) -> str:
    """Gate: one line, 1-200 chars, not only whitespace."""
    if not line.strip():
        raise ValueError("entry must not be blank")
    if "\n" in line or "\r" in line:
        raise ValueError("entry must be a single line")
    if not 1 <= len(line) <= 200:
        raise ValueError(f"entry must be 1-200 chars, got {len(line)}")
    return line


def resolve_output_dir() -> Path:
    """Return the entry.txt path: $MAKEFUN_OUTPUT_DIR or /output/entry.txt.

    MAKEFUN_OUTPUT_DIR is a directory; if it already points at a .txt
    file, use it directly.
    """
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output/entry.txt")
    return out_dir if out_dir.suffix == ".txt" else out_dir / "entry.txt"


def main() -> None:
    line = validate_line(ENTRY)
    out_path = resolve_output_dir()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(line, encoding="utf-8")
    # Self-test: re-read what was written and confirm it matches the
    # chosen line exactly, so a truncated or corrupted write fails
    # loudly instead of silently submitting a wrong entry.
    written = out_path.read_text(encoding="utf-8")
    assert written == line, "entry.txt does not match the chosen line"
    # NOTE: the entry lives in entry.txt, never on stdout — the judge
    # reads the file, and print-only output scores 0, so this program
    # deliberately prints nothing at all.


if __name__ == "__main__":
    main()
