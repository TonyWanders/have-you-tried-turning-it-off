#!/usr/bin/env python3
# Have You Tried Turning It Off?
#
# A tiny deterministic entry for the make.fun competition. The program
# writes one fixed tech-support joke to a text file. There is nothing
# to configure, nothing to fetch and nothing random: the line below is
# a constant, and the file it lands in is chosen from the command line,
# then the OUTPUT_PATH environment variable, then a fixed default.
#
# Usage:
#   python3 main.py [path]
#
# The entry must stay inside the competition gate of 1 to 199
# characters and must not be blank. If it ever fails that gate the
# program complains on stderr and exits with status 1 instead of
# writing anything.

import os
import sys
from pathlib import Path

# The joke. One string, 134 characters, written out in full so the
# output is obvious to anyone reading the source.
JOKE = (
    "Have you tried turning it off and on again? "
    "It fixed my toaster, "
    "my marriage is still loading, "
    "and your business is next in the queue."
)

# Competition gate, inclusive on both ends.
LOWER_LIMIT = 1
UPPER_LIMIT = 199

# Where the entry goes when no path is given anywhere else.
FALLBACK_PATH = Path("/output/entry.txt")


def resolve_output_path() -> Path:
    """Work out where the entry should be written.

    First argument wins, then $OUTPUT_PATH, then the fallback. An
    empty environment value counts as unset, so it falls through.
    """
    if len(sys.argv) > 1:
        return Path(sys.argv[1])
    if value := os.environ.get("OUTPUT_PATH"):
        return Path(value)
    return FALLBACK_PATH


def validate(text: str) -> int:
    """Check the entry against the competition gate.

    Returns the number of characters when the text is inside 1 to
    199 characters and is not only white space. Raises ValueError
    otherwise, with a message describing what went wrong.
    """
    length = len(text)
    if length < LOWER_LIMIT:
        raise ValueError("entry is empty, needs at least 1 character")
    if length > UPPER_LIMIT:
        raise ValueError(
            f"entry is {length} characters, over the 199 limit"
        )
    if text.isspace():
        raise ValueError("entry is only white space")
    return length


def write_entry(path: Path, text: str) -> int:
    """Validate the text, write it to path, and return its length.

    The parent directory is created when it does not exist yet, so
    running against a fresh /output works. The file is written as
    plain UTF-8 with no trailing newline added, exactly the text
    given. Validation happens before anything touches the disk.
    """
    count = validate(text)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return count


def main() -> int:
    """Entry point: write the joke and report what happened."""
    path = resolve_output_path()
    try:
        chars = write_entry(path, JOKE)
    except ValueError as exc:
        print(f"invalid entry: {exc}", file=sys.stderr)
        return 1
    except OSError as exc:
        print(f"could not write entry: {exc}", file=sys.stderr)
        return 1
    print(f"wrote {chars} characters to {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
