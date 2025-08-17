#!/usr/bin/env python3
"""
Replace the top-level 'proxy-providers:' block (including its header line)
in 'mihomo-custom.yaml' with the entire contents of 'proxy-providers-info.yaml'.

Default paths are resolved relative to this script directory:
  - target:   ../mihomo-custom.yaml
  - source:   ../proxy-providers-info.yaml

Usage examples:
  python3 tools/replace_proxy_providers.py
  python3 tools/replace_proxy_providers.py -t /abs/path/mihomo-custom.yaml -s /abs/path/proxy-providers-info.yaml
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


def find_top_level_block_range(text: str, key: str) -> tuple[int, int]:
    """Return (start_index, end_index) for the top-level YAML block named `key`.

    The start matches the line beginning with `key:` at column 0.
    The end is right before the next top-level key (column-0 `something:`) or EOF.
    """
    start_pattern = re.compile(rf"(?m)^{re.escape(key)}:\s*(?:#.*)?$")
    start_match = start_pattern.search(text)
    if not start_match:
        raise ValueError(f"Top-level key '{key}:' not found in target file")

    # Next top-level key (column 0, not a comment), excluding the same key at start.
    next_top_pattern = re.compile(r"(?m)^(?!#)(?!\s)([A-Za-z0-9_\-]+):(\s|$)")
    next_match = next_top_pattern.search(text, pos=start_match.end())

    start_index = start_match.start()
    end_index = next_match.start() if next_match else len(text)
    return start_index, end_index


def ensure_replacement_has_header(replacement_text: str, header_key: str) -> str:
    """Ensure the replacement text begins with the `header_key:` at column 0.
    If not, wrap the content under that header and indent by two spaces.
    """
    has_header = re.search(rf"(?m)^{re.escape(header_key)}:\s*", replacement_text) is not None
    if has_header:
        return replacement_text

    # Indent each non-empty line by two spaces
    indented_lines = []
    for line in replacement_text.splitlines():
        if line.strip() == "":
            indented_lines.append("")
        else:
            indented_lines.append("  " + line)
    wrapped = header_key + ":\n" + "\n".join(indented_lines)
    return wrapped


def replace_block_in_text(target_text: str, header_key: str, replacement_text: str) -> str:
    start_index, end_index = find_top_level_block_range(target_text, header_key)

    # Normalize newlines: ensure the replacement ends with a single newline
    if not replacement_text.endswith("\n"):
        replacement_text = replacement_text + "\n"

    # Preserve everything before and after the block
    before = target_text[:start_index]
    after = target_text[end_index:]
    return before + replacement_text + after


def main(argv: list[str]) -> int:
    script_path = Path(__file__).resolve()
    root_dir = script_path.parent.parent

    default_target = root_dir / "mihomo-custom.yaml"
    default_source = root_dir / "proxy-providers-info.yaml"

    parser = argparse.ArgumentParser(description="Replace 'proxy-providers:' block in mihomo-custom.yaml")
    parser.add_argument("-t", "--target", type=Path, default=default_target, help="Path to mihomo-custom.yaml")
    parser.add_argument("-s", "--source", type=Path, default=default_source, help="Path to proxy-providers-info.yaml")
    parser.add_argument("--no-backup", action="store_true", help="Do not create .bak backup of target file")
    args = parser.parse_args(argv)

    target_path: Path = args.target
    source_path: Path = args.source

    if not target_path.exists():
        print(f"[ERROR] Target file not found: {target_path}", file=sys.stderr)
        return 1
    if not source_path.exists():
        print(f"[ERROR] Source file not found: {source_path}", file=sys.stderr)
        return 1

    try:
        target_text = target_path.read_text(encoding="utf-8")
    except Exception as exc:  # noqa: BLE001
        print(f"[ERROR] Failed to read target file: {exc}", file=sys.stderr)
        return 1

    try:
        replacement_raw = source_path.read_text(encoding="utf-8")
    except Exception as exc:  # noqa: BLE001
        print(f"[ERROR] Failed to read source file: {exc}", file=sys.stderr)
        return 1

    replacement_text = ensure_replacement_has_header(replacement_raw, "proxy-providers")

    try:
        new_text = replace_block_in_text(target_text, "proxy-providers", replacement_text)
    except Exception as exc:  # noqa: BLE001
        print(f"[ERROR] Replacement failed: {exc}", file=sys.stderr)
        return 1

    # Create backup unless disabled
    if not args.no_backup:
        backup_path = target_path.with_suffix(target_path.suffix + ".bak")
        try:
            backup_path.write_text(target_text, encoding="utf-8")
            print(f"[INFO] Backup created: {backup_path}")
        except Exception as exc:  # noqa: BLE001
            print(f"[WARN] Failed to create backup: {exc}", file=sys.stderr)

    try:
        target_path.write_text(new_text, encoding="utf-8")
    except Exception as exc:  # noqa: BLE001
        print(f"[ERROR] Failed to write target file: {exc}", file=sys.stderr)
        return 1

    print(f"[OK] Replaced 'proxy-providers:' block in {target_path} using {source_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))


