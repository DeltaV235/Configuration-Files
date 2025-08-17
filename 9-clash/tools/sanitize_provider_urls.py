#!/usr/bin/env python3
"""
Sanitize provider subscription URLs in the 'proxy-providers:' block.

Only the top-level 'url:' under each provider is redacted. Nested 'url' (e.g.,
under health-check in other sections) are NOT touched, as we scope the change
strictly to the 'proxy-providers:' block and the immediate children of each
provider entry.

Defaults:
  - target:     ../mihomo-custom.yaml
  - header key: proxy-providers
  - placeholder: "" (empty string)
  - backup:     on (writes <target>.bak)

Examples:
  python3 tools/sanitize_provider_urls.py
  python3 tools/sanitize_provider_urls.py -t /abs/path/mihomo-custom.yaml
  python3 tools/sanitize_provider_urls.py -t ../proxy-providers-info.yaml --placeholder REDACTED
  python3 tools/sanitize_provider_urls.py --no-backup
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


def find_top_level_block_range(text: str, key: str) -> tuple[int, int]:
    """Return (start_index, end_index) for the top-level YAML block named `key`.

    Start matches the line beginning with `key:` at column 0 (inclusive).
    End is right before the next top-level key, while preserving any contiguous
    top-level comments/blank-lines immediately preceding that next key.
    """
    start_pattern = re.compile(rf"(?m)^{re.escape(key)}:\s*(?:#.*)?$")
    start_match = start_pattern.search(text)
    if not start_match:
        raise ValueError(f"Top-level key '{key}:' not found in target file")

    next_top_pattern = re.compile(r"(?m)^(?!#)(?!\s)([A-Za-z0-9_\-]+):(\s|$)")
    next_match = next_top_pattern.search(text, pos=start_match.end())

    start_index = start_match.start()
    if not next_match:
        return start_index, len(text)

    end_index = next_match.start()

    # Preserve contiguous top-level comments and blank lines just before the next key.
    MAX_BACKSCAN_LINES = 50
    segment_start = start_match.end()
    segment_end = end_index
    segment = text[segment_start:segment_end]
    lines = segment.splitlines(keepends=True)
    preserve_char_count = 0
    scanned_lines = 0
    for line in reversed(lines):
        if scanned_lines >= MAX_BACKSCAN_LINES:
            break
        raw = line[:-1] if line.endswith("\n") else line
        if raw.endswith("\r"):
            raw = raw[:-1]
        if raw.strip() == "" or raw.startswith("#"):
            preserve_char_count += len(line)
            scanned_lines += 1
            continue
        break

    end_index = segment_end - preserve_char_count
    return start_index, end_index


def build_quoted_value(placeholder: str) -> str:
    # Use double-quoted YAML string and escape backslash and double quotes
    return '"' + placeholder.replace('\\', r'\\').replace('"', r'\"') + '"'


def sanitize_provider_urls_in_block(block_text: str, placeholder: str) -> tuple[str, int]:
    """Return (new_block, num_replacements).

    Redacts only lines of the form (indent == provider child indent):
        <child_indent>url: <anything> [# comment]
    Replaces the value with the provided placeholder (quoted), preserving
    indentation and line endings. Attempts to preserve inline comments when
    present by adding a single space before '#'.
    """
    lines = block_text.splitlines(keepends=True)
    if not lines:
        return block_text, 0

    # Header line is the 'proxy-providers:' line
    result: list[str] = [lines[0]]
    num_changed = 0

    current_provider_indent: str | None = None
    current_child_indent: str | None = None

    quoted_value = build_quoted_value(placeholder)

    def leading_ws(s: str) -> str:
        idx = 0
        while idx < len(s) and s[idx] in (" ", "\t"):
            idx += 1
        return s[:idx]

    for raw in lines[1:]:
        line_no_eol = raw.rstrip("\n\r")
        eol = raw[len(line_no_eol):]

        # Preserve empty lines and pure comments as-is
        if line_no_eol.strip() == "" or line_no_eol.lstrip().startswith("#"):
            result.append(raw)
            continue

        indent = leading_ws(line_no_eol)
        content = line_no_eol[len(indent):]

        # Detect the first provider header indent (e.g., "  1.primary:")
        if current_provider_indent is None:
            if content.endswith(":") and not content.startswith("#"):
                current_provider_indent = indent
            result.append(raw)
            continue

        # Detect new provider header (same indent as provider indent)
        if content.endswith(":") and len(indent) == len(current_provider_indent):
            current_child_indent = None
            result.append(raw)
            continue

        # Establish child indent on first child line under provider
        if current_child_indent is None and len(indent) > len(current_provider_indent):
            current_child_indent = indent

        # Perform redaction only for direct child 'url:' lines
        if current_child_indent is not None and indent == current_child_indent and content.lstrip().startswith("url:"):
            # Compose new line with same indentation and EOL
            # Preserve any inline comment if present
            hash_pos = content.find("#")
            if hash_pos != -1:
                comment = content[hash_pos:]
                new_content = f"url: {quoted_value} " + comment
            else:
                new_content = f"url: {quoted_value}"

            result.append(indent + new_content + eol)
            num_changed += 1
            continue

        result.append(raw)

    return "".join(result), num_changed


def main(argv: list[str]) -> int:
    script_path = Path(__file__).resolve()
    root_dir = script_path.parent.parent

    parser = argparse.ArgumentParser(description="Sanitize provider URLs in 'proxy-providers:' block")
    parser.add_argument("-t", "--target", type=Path, default=root_dir / "mihomo-custom.yaml", help="Path to target YAML file")
    parser.add_argument("-k", "--key", default="proxy-providers", help="Top-level key for providers block")
    parser.add_argument("--placeholder", default="", help="Replacement value for provider 'url' (default: empty string)")
    parser.add_argument("--no-backup", action="store_true", help="Do not create .bak backup of target file")
    args = parser.parse_args(argv)

    if not args.target.exists():
        print(f"[ERROR] Target file not found: {args.target}", file=sys.stderr)
        return 1

    try:
        original_text = args.target.read_text(encoding="utf-8")
    except Exception as exc:  # noqa: BLE001
        print(f"[ERROR] Failed to read target file: {exc}", file=sys.stderr)
        return 1

    try:
        start, end = find_top_level_block_range(original_text, args.key)
    except Exception as exc:  # noqa: BLE001
        print(f"[ERROR] Failed to locate block '{args.key}': {exc}", file=sys.stderr)
        return 1

    block_text = original_text[start:end]
    new_block, num_replaced = sanitize_provider_urls_in_block(block_text, args.placeholder)

    if num_replaced == 0:
        print("[INFO] No provider 'url:' entries found to sanitize.")
        return 0

    if not args.no_backup:
        backup_path = args.target.with_suffix(args.target.suffix + ".bak")
        try:
            backup_path.write_text(original_text, encoding="utf-8")
            print(f"[INFO] Backup created: {backup_path}")
        except Exception as exc:  # noqa: BLE001
            print(f"[WARN] Failed to create backup: {exc}", file=sys.stderr)

    new_text = original_text[:start] + new_block + original_text[end:]
    try:
        args.target.write_text(new_text, encoding="utf-8")
    except Exception as exc:  # noqa: BLE001
        print(f"[ERROR] Failed to write target file: {exc}", file=sys.stderr)
        return 1

    print(f"[OK] Sanitized {num_replaced} provider URL(s) in {args.target}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))


