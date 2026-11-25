"""Famous Last Words: The Funniest Epitaph.

Writes a single one-line tombstone epitaph of famous last words to
/output/entry.txt. The gate requires UTF-8 text, 1 to 150 characters,
not only whitespace, on a single line.

Tournament winner (specificity 5 / surprise 4 / freshness 4 = 13):
the dying-speech twist is a life summed up in one unfinished sentence,
with a concrete number (seventeen tabs) instead of a generic joke.

Tournament table (specificity / surprise / freshness):
  1. out-of-office is permanent            4 / 3 / 3 = 10
  2. ashes scattered, put in group chat     4 / 4 / 4 = 12
  3. mid-sentence, seventeen tabs open      5 / 4 / 4 = 13 (winner)
  4. report in folder final_final_v2        5 / 3 / 3 = 11
  5. inbox zero, cost me everything         4 / 4 / 3 = 11
  6. closed casket, open bar, budget        3 / 3 / 3 = 9
  7. group project carried alone            4 / 4 / 4 = 12
  8. doctor filed a formal complaint        4 / 4 / 4 = 12
"""

import argparse
import os
import sys
import tempfile

EPITAPH = "I died as I lived: mid-sentence, with seventeen browser tabs open."

OUTPUT_PATH = "/output/entry.txt"


def gate_check(text):
    """Return a list of gate failures; empty means the line is valid."""
    problems = []
    if not text or not text.strip():
        problems.append("empty or whitespace only")
    if "\n" in text or "\r" in text:
        problems.append("not a single line")
    if len(text) > 150:
        problems.append("over 150 characters: %d" % len(text))
    if len(text) < 1:
        problems.append("under 1 character")
    return problems


def write_entry(path=OUTPUT_PATH):
    directory = os.path.dirname(path)
    if directory:
        os.makedirs(directory, exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(EPITAPH + "\n")
    return path


def main(argv=None):
    parser = argparse.ArgumentParser(description="Write the epitaph entry.")
    parser.add_argument(
        "--check",
        action="store_true",
        help="Validate the line against the gate without writing it.",
    )
    parser.add_argument(
        "--self-test",
        action="store_true",
        help="Write to a temp file and verify the bytes read back.",
    )
    args = parser.parse_args(argv)

    problems = gate_check(EPITAPH)
    if args.self_test:
        with tempfile.TemporaryDirectory() as tmp:
            trial = os.path.join(tmp, "entry.txt")
            write_entry(trial)
            with open(trial, "rb") as handle:
                raw = handle.read()
        if raw.decode("utf-8").strip() != EPITAPH:
            print("self-test FAILED: bytes read back do not match", file=sys.stderr)
            return 1
        print("self-test ok: %d bytes round-trip" % len(raw))
        return 0
    if args.check:
        if problems:
            print("gate FAILED: " + "; ".join(problems))
            return 1
        print("ok: %d characters" % len(EPITAPH))
        print(EPITAPH)
        return 0

    if problems:
        print("gate FAILED: " + "; ".join(problems), file=sys.stderr)
        return 1

    path = write_entry()
    print("wrote %d chars to %s" % (len(EPITAPH), path))
    return 0


if __name__ == "__main__":
    sys.exit(main())
