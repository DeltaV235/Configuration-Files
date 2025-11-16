#!/usr/bin/env python3
"""
Sanitize sensitive information in 'all-proxy-providers:', 'primary-proxy-providers:',
and 'proxy-providers:' blocks in mihomo-custom.yaml by replacing them with clean
template content from proxy-providers-clean.yaml.

Default paths are resolved relative to this script directory:
  - target:   ../mihomo-custom.yaml
  - template: ../proxy-providers-clean.yaml

Usage examples:
  python3 tools/sanitize_provider_urls.py
  python3 tools/sanitize_provider_urls.py --backup
  python3 tools/sanitize_provider_urls.py -t /path/mihomo-custom.yaml
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


def find_top_level_block_range(text: str, key: str) -> tuple[int, int]:
    """Return (start_index, end_index) for the top-level YAML block named `key`.

    Start matches the line beginning with `key:` at column 0 (inclusive), or any
    comment line immediately preceding it.
    End is right before the next top-level key or its preceding comment.
    Supports YAML anchors (e.g., `key: &anchor-name # comment`).
    """
    # Find the key line
    start_pattern = re.compile(rf"(?m)^{re.escape(key)}:\s*(?:&\S+\s*)?(?:#.*)?$")
    start_match = start_pattern.search(text)
    if not start_match:
        raise ValueError(f"Top-level key '{key}:' not found in file")

    # Include any comment lines immediately before the key
    start_index = start_match.start()
    before_text = text[:start_index]
    lines_before = before_text.splitlines(keepends=True)

    # Walk backwards to find preceding comments
    for line in reversed(lines_before):
        stripped = line.rstrip("\n\r")
        if stripped.strip() == "":
            continue  # Skip blank lines
        elif stripped.lstrip().startswith("#"):
            start_index -= len(line)
        else:
            break  # Stop at first non-comment line

    # Next top-level key (column 0, not a comment)
    next_top_pattern = re.compile(r"(?m)^(?!#)(?!\s)([A-Za-z0-9_\-]+):(\s|$)")
    next_match = next_top_pattern.search(text, pos=start_match.end())

    if not next_match:
        return start_index, len(text)

    # Find any comment immediately before the next key
    end_index = next_match.start()
    segment_before_next = text[start_match.end():end_index]
    lines = segment_before_next.splitlines(keepends=True)

    # Walk backwards from next key to find its preceding comment
    for line in reversed(lines):
        stripped = line.rstrip("\n\r")
        if stripped.strip() == "":
            end_index -= len(line)
        elif stripped.lstrip().startswith("#"):
            end_index -= len(line)
            break  # Found the comment, stop here
        else:
            break  # Non-comment content, stop

    return start_index, end_index


def replace_block_in_text(target_text: str, header_key: str, replacement_text: str) -> str:
    """Replace a top-level block in target text with replacement text."""
    start_index, end_index = find_top_level_block_range(target_text, header_key)

    # Ensure replacement ends with a single newline
    if not replacement_text.endswith("\n"):
        replacement_text = replacement_text + "\n"

    return target_text[:start_index] + replacement_text + target_text[end_index:]


def extract_block_from_source(source_text: str, key: str) -> str:
    """Extract a specific top-level block from source text.

    Returns the block text (find_top_level_block_range already includes comments).
    """
    try:
        start_index, end_index = find_top_level_block_range(source_text, key)
        return source_text[start_index:end_index]
    except ValueError:
        return ""


def main(argv: list[str]) -> int:
    script_path = Path(__file__).resolve()
    root_dir = script_path.parent.parent

    default_target = root_dir / "mihomo-custom.yaml"
    default_template = root_dir / "proxy-providers-clean.yaml"

    parser = argparse.ArgumentParser(
        description="Sanitize proxy provider blocks using clean template"
    )
    parser.add_argument("-t", "--target", type=Path, default=default_target, help="Path to mihomo-custom.yaml")
    parser.add_argument("--template", type=Path, default=default_template, help="Path to proxy-providers-clean.yaml")
    parser.add_argument("--backup", action="store_true", help="Create .bak backup of target file")
    args = parser.parse_args(argv)

    target_path: Path = args.target
    template_path: Path = args.template

    if not target_path.exists():
        print(f"[ERROR] Target file not found: {target_path}", file=sys.stderr)
        return 1
    if not template_path.exists():
        print(f"[ERROR] Template file not found: {template_path}", file=sys.stderr)
        return 1

    try:
        target_text = target_path.read_text(encoding="utf-8")
    except Exception as exc:  # noqa: BLE001
        print(f"[ERROR] Failed to read target file: {exc}", file=sys.stderr)
        return 1

    try:
        template_text = template_path.read_text(encoding="utf-8")
    except Exception as exc:  # noqa: BLE001
        print(f"[ERROR] Failed to read template file: {exc}", file=sys.stderr)
        return 1

    # Blocks to replace (in reverse order to avoid index shifting)
    blocks_to_replace = ["proxy-providers", "primary-proxy-providers", "all-proxy-providers"]
    replaced_blocks = []

    new_text = target_text
    for block_key in blocks_to_replace:
        replacement_block = extract_block_from_source(template_text, block_key)
        if not replacement_block:
            print(f"[WARN] Block '{block_key}:' not found in template file, skipping", file=sys.stderr)
            continue

        try:
            new_text = replace_block_in_text(new_text, block_key, replacement_block)
            replaced_blocks.append(block_key)
        except Exception as exc:  # noqa: BLE001
            print(f"[ERROR] Failed to replace block '{block_key}': {exc}", file=sys.stderr)
            return 1

    if not replaced_blocks:
        print("[ERROR] No blocks were replaced", file=sys.stderr)
        return 1

    # Create backup if requested
    if args.backup:
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

    blocks_str = ", ".join(f"'{b}:'" for b in reversed(replaced_blocks))
    print(f"[OK] Sanitized {blocks_str} blocks in {target_path} using clean template")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
