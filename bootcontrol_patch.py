#!/usr/bin/env python3

import sys
from pathlib import Path

HOOK = "/etc/init.d/S62u1-wled start"


def remove_hook(text: str) -> str:
    lines = [line for line in text.splitlines() if line.strip() != HOOK]
    return "\n".join(lines) + ("\n" if text.endswith("\n") else "")


def install_hook(text: str) -> str:
    lines = remove_hook(text).splitlines()

    start_index = None
    for i, line in enumerate(lines):
        if line.strip() == "start)":
            start_index = i
            break

    if start_index is None:
        raise ValueError("Could not find start) branch in S99_bootcontrol")

    insert_index = None
    for i in range(start_index + 1, len(lines)):
        if lines[i].strip() == ";;":
            insert_index = i
            break

    if insert_index is None:
        raise ValueError("Could not find end of start) branch in S99_bootcontrol")

    indent = lines[insert_index][: len(lines[insert_index]) - len(lines[insert_index].lstrip())]
    lines.insert(insert_index, f"{indent}{HOOK}")

    return "\n".join(lines) + ("\n" if text.endswith("\n") else "")


def main() -> int:
    remove = False
    args = sys.argv[1:]
    if args and args[0] == "--remove":
        remove = True
        args = args[1:]

    if len(args) != 1:
        print(
            f"Usage: {sys.argv[0]} [--remove] /etc/init.d/S99_bootcontrol",
            file=sys.stderr,
        )
        return 2

    path = Path(args[0])
    try:
        original = path.read_text()
        patched = remove_hook(original) if remove else install_hook(original)
    except (OSError, ValueError) as exc:
        print(f"bootcontrol patch failed: {exc}", file=sys.stderr)
        return 1

    if patched != original:
        path.write_text(patched)
        print("Removed S99_bootcontrol WLED launcher" if remove else "Updated S99_bootcontrol WLED launcher")
    else:
        print("S99_bootcontrol WLED launcher already absent" if remove else "S99_bootcontrol WLED launcher already correct")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
