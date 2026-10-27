"""SessionStart hook: remind the user when the harness review is overdue.

Reads `last-review: YYYY-MM-DD` from docs/harness-review.md and, once that date is
more than MAX_AGE_DAYS old, shows a message to the user (not to Claude, so it costs
no tokens). Offline and silent while the review is fresh.
"""

import json
import re
import sys
from datetime import date
from pathlib import Path

LOG = Path(__file__).resolve().parents[2] / "docs" / "harness-review.md"
MAX_AGE_DAYS = 30
LAST_REVIEW = re.compile(r"^- last-review: (\d{4}-\d{2}-\d{2})$", re.MULTILINE)


def reminder(log: str, today: date) -> str | None:
    match = LAST_REVIEW.search(log)
    if match and (today - date.fromisoformat(match[1])).days <= MAX_AGE_DAYS:
        return None
    since = f"on {match[1]}" if match else "never"
    return (
        f"Harness last reviewed {since}. Run /harness-review to check new Claude Code "
        "best practices against this harness before you start."
    )


def main(log: Path = LOG) -> int:
    text = log.read_text(encoding="utf-8") if log.exists() else ""
    if message := reminder(text, date.today()):
        print(json.dumps({"systemMessage": message}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
