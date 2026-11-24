#!/usr/bin/env python3
"""Write one funny one-star cat review to the grader's output file.

The competition asks for a single line: a one-star review written by a
house cat about its human, under 200 characters. This program holds one
hand-written line, checks it against the gate (UTF-8 text, 1 to 200
characters, a single line, not only white space), and writes it to
entry.txt inside the output directory the grader mounts.

The output directory comes from the first argument when one is given,
else from MAKEFUN_OUTPUT_DIR, else from /output, which is where the
grader mounts it.
"""

import os
import sys

# The review. One line, 140 characters. The complaint is the laptop
# keyboard: the human types on it all day and calls that a job, while
# the cat sat on it once and did better work. The sting lands last.
REVIEW = (
    "One star. He types on my keyboard for eight hours and calls it a "
    "job. I sat on it once and produced better work. "
    "I have informed management."
)

MAX_CHARS = 200


def complain(message):
    print(f"entry: {message}", file=sys.stderr)
    return 1


def pick_output_dir(argv):
    if argv:
        return argv[0]
    env_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if env_dir:
        return env_dir
    return "/output"


def check_line(text):
    if not text or not text.strip():
        return "review is empty or only white space"
    if "\n" in text or "\r" in text:
        return "review must be a single line"
    if len(text) > MAX_CHARS:
        return f"review is {len(text)} characters, over the {MAX_CHARS} limit"
    try:
        text.encode("utf-8")
    except UnicodeEncodeError as error:
        return f"review is not encodable as UTF-8: {error}"
    return None


def main(argv=None):
    args = list(sys.argv[1:] if argv is None else argv)
    problem = check_line(REVIEW)
    if problem:
        return complain(problem)
    out_dir = pick_output_dir(args)
    os.makedirs(out_dir, exist_ok=True)
    target = os.path.join(out_dir, "entry.txt")
    with open(target, "w", encoding="utf-8", newline="\n") as handle:
        # No trailing newline: the file is exactly the one review line,
        # so the gate counts the same 140 characters the program checked.
        handle.write(REVIEW)
    with open(target, "r", encoding="utf-8") as handle:
        written = handle.read()
    if written != REVIEW:
        return complain("written file does not match the review")
    print(f"wrote {target} ({len(REVIEW)} characters)")
    print(REVIEW)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
