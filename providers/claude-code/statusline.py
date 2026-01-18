#!/usr/bin/env python3
import json
import os
import subprocess
import sys


def run_git(args):
    try:
        result = subprocess.run(
            args,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=True,
        )
        if result.returncode == 0:
            return result.stdout.strip()
    except Exception:
        return ""
    return ""


def git_info(cwd):
    if not cwd:
        return "", ""
    if not os.path.exists(os.path.join(cwd, ".git")):
        return "", ""

    branch = run_git(["git", "-C", cwd, "branch", "--show-current"])
    if not branch:
        short = run_git(["git", "-C", cwd, "rev-parse", "--short", "HEAD"])
        if short:
            branch = f"HEAD@{short}"
    if not branch:
        return "", ""

    status = ""
    dirty = run_git(["git", "-C", cwd, "status", "--porcelain"])
    if dirty:
        status += "*"

    upstream = run_git(["git", "-C", cwd, "rev-parse", "--abbrev-ref", "@{u}"])
    if upstream:
        ahead = run_git(["git", "-C", cwd, "rev-list", "--count", "@{u}..HEAD"])
        behind = run_git(["git", "-C", cwd, "rev-list", "--count", "HEAD..@{u}"])
        if ahead and ahead != "0":
            status += f"^{ahead}"
        if behind and behind != "0":
            status += f"v{behind}"

    return branch, status


def main():
    try:
        data = json.load(sys.stdin)
    except Exception:
        return 0

    model = data.get("model", {}).get("display_name") or "Model"
    workspace = data.get("workspace", {}) or {}
    current_dir = workspace.get("current_dir")
    project_dir = workspace.get("project_dir")
    used_pct = data.get("context_window", {}).get("used_percentage")

    project_path = project_dir or current_dir or ""
    project_name = os.path.basename(project_path) if project_path else "no-project"

    branch, status = git_info(current_dir)
    parts = [project_name, model]
    if branch:
        parts.append(f"{branch}{status}")

    if used_pct is not None and used_pct != "null":
        try:
            pct = int(round(float(used_pct)))
            pct = max(0, min(pct, 100))
            parts.append(f"{pct}% ctx")
        except (ValueError, TypeError):
            pass

    sys.stdout.write(" | ".join(parts))
    return 0


if __name__ == "__main__":
    sys.exit(main())
