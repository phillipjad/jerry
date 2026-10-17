# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Phillip Miavelstuck

"""Smoke test: run the hooks exactly as hooks/hooks.json declares them, from a plugin path with a space.

Usage: python hook_smoke.py

Copies the tracked plugin files to ``<tmp>/Jerry Smoke/jerry``, makes a projects root next to it,
then runs SessionStart, the ``jerry focus`` command it prints, SessionStart again and SubagentStart
as separate processes, the way Claude Code starts them: exec form, no shell, ``${CLAUDE_PLUGIN_ROOT}``
replaced by the plugin path with forward slashes. Standard library only; CI runs it on every OS.
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
SESSION = "hook-smoke"
WARM_LIMIT = 5.0


def hook_argv(plugin: Path, event: str) -> tuple[list[str], float]:
    hooks = json.loads((plugin / "hooks" / "hooks.json").read_text(encoding="utf-8"))["hooks"]
    hook = hooks[event][0]["hooks"][0]
    root = plugin.as_posix()
    return [hook["command"], *(arg.replace("${CLAUDE_PLUGIN_ROOT}", root) for arg in hook["args"])], hook["timeout"]


def run(argv: list[str], cwd: Path, env: dict[str, str], stdin: str = "", timeout: float = 120) -> tuple[str, float]:
    start = time.monotonic()
    done = subprocess.run(argv, cwd=cwd, env=env, input=stdin.encode("utf-8"), capture_output=True, timeout=timeout)
    elapsed = time.monotonic() - start
    if done.returncode != 0:
        raise AssertionError(f"{argv[-1]} exited {done.returncode}: {done.stderr.decode('utf-8', 'replace')}")
    return done.stdout.decode("utf-8"), elapsed


def hook(plugin: Path, event: str, cwd: Path, env: dict[str, str], source: str = "startup") -> tuple[str, float]:
    argv, timeout = hook_argv(plugin, event)
    payload = {"session_id": SESSION, "cwd": str(cwd), "hook_event_name": event, "source": source}
    out, elapsed = run(argv, cwd, env, json.dumps(payload), timeout)
    assert out.isascii(), f"{event} printed non-ASCII output"
    context = json.loads(out)["hookSpecificOutput"]["additionalContext"]
    print(f"{event} ({source}): {elapsed:.2f} s, {len(context)} characters")
    return context, elapsed


def main() -> int:
    scratch = Path(tempfile.mkdtemp()).resolve()
    try:
        return smoke(scratch / "Jerry Smoke")
    finally:
        shutil.rmtree(scratch, ignore_errors=True)


def smoke(base: Path) -> int:
    plugin, work, home = base / "jerry", base / "work", base / "home"
    tracked = subprocess.run(["git", "ls-files", "-z"], cwd=REPO, capture_output=True, check=True).stdout
    for rel in filter(None, tracked.decode("utf-8").split("\0")):
        (plugin / rel).parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(REPO / rel, plugin / rel)
    project = work / "projects" / "PROJ-001-sample"
    project.mkdir(parents=True)
    (project / "project.toml").write_text('title = "Sample"\nstatus = "active"\nsummary = ""\n', encoding="utf-8-sig")
    (project / "RESUME.md").write_text("## Pick up here\r\n\r\n- Train in the time chamber.\r\n", encoding="utf-8")
    home.mkdir()
    env = {k: v for k, v in os.environ.items() if k not in ("PYTHONUTF8", "CLAUDE_CODE_SESSION_ID")}
    env.update(HOME=str(home), USERPROFILE=str(home))

    context, _ = hook(plugin, "SessionStart", work, env)
    assert context.startswith(f"Jerry plugin root: {plugin.as_posix()}."), context[:200]
    assert "Focus: nothing is focused" in context and "PROJ-001" in context, context

    focus = [
        "uv", "run", "--project", plugin.as_posix(), "jerry", "focus", "set", "PROJ-001", "--session", SESSION,
    ]
    out, elapsed = run(focus, work, env)
    print(f"jerry focus set: {elapsed:.2f} s")
    assert "Train in the time chamber." in out, out

    context, elapsed = hook(plugin, "SessionStart", work, env, source="resume")
    assert "PROJ-001" in context and "Train in the time chamber." in context, context
    assert elapsed < WARM_LIMIT, f"warm SessionStart took {elapsed:.2f} s"

    context, _ = hook(plugin, "SubagentStart", work, env)
    assert context.startswith("Jerry focus: {project_dir} = ") and "PROJ-001-sample" in context, context
    print("hook smoke passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
