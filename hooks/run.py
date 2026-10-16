# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Phillip Miavelstuck

"""Hook entry point: ``run.py session-start|subagent-start`` with the hook input as JSON on stdin.

Runs on the standard library alone, outside the project environment. The
output is pure ASCII, so no console encoding can break it. Any failure prints
one plain line and exits 0, so a broken hook never blocks a session.
"""

import json
import sys
from pathlib import Path


def main() -> int:
    event = sys.argv[1] if len(sys.argv) > 1 else ""
    try:
        sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
        from jerry import hooks

        handler = {"session-start": hooks.session_start, "subagent-start": hooks.subagent_start}.get(event)
        if handler is None:
            raise ValueError("unknown event")
        result = handler(json.loads(sys.stdin.buffer.read().decode("utf-8")))
        output = "" if result is None else json.dumps(result, ensure_ascii=True)
    except Exception as exc:
        output = f"Jerry {event} hook: {' '.join(str(exc).split()) or type(exc).__name__}\n"
    sys.stdout.buffer.write(output.encode("ascii", "backslashreplace"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
