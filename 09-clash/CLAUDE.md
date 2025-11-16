# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Context

This is the `09-clash/` directory within a larger Configuration-Files repository. It contains Clash/Mihomo proxy configuration files and Python utilities for managing proxy provider configurations.

**Repository:** `git@github.com:DeltaV235/Configuration-Files.git`

## Core Architecture

### Configuration Files

- **mihomo-custom.yaml**: Main Mihomo configuration file with proxy groups, routing rules, DNS settings, and TUN configuration
  - Uses YAML anchors extensively for templating (e.g., `&primary-provider-template`, `&all-proxy-providers`)
  - Automatically sanitized by pre-commit hooks before commits
  - Includes specialized proxy groups for AI services with consistent-hashing strategy to reduce IP fluctuations

- **proxy-providers-secrets.yaml**: Contains real proxy provider configurations with sensitive information
  - Includes three blocks: `all-proxy-providers`, `primary-proxy-providers`, and `proxy-providers`
  - Contains actual subscription URLs, provider names, and references
  - **Ignored by Git** (in `.gitignore`) - never committed to version control

- **proxy-providers-clean.yaml**: Sanitized template for proxy provider blocks
  - Contains only placeholder/empty values (no sensitive data)
  - Uses simplified provider names (e.g., `1.primary1`, `2.primary2`)
  - Used to replace sensitive blocks before commits

- **qichiyuhub-mihomo-config.yaml**: Alternative Mihomo configuration template (read-only reference)

### Python Tools

Located in `tools/` directory:

1. **replace_proxy_providers.py**: Replaces three blocks in mihomo-custom.yaml from secrets file
   - Replaces: `all-proxy-providers`, `primary-proxy-providers`, and `proxy-providers`
   - Source: `proxy-providers-secrets.yaml` (contains real sensitive data)
   - Uses whole-block replacement (simple and efficient)
   - Default: no backup (use `--backup` to create .bak file)

2. **sanitize_provider_urls.py**: Sanitizes sensitive information using clean template
   - Replaces three blocks from `proxy-providers-clean.yaml`
   - Removes all sensitive provider names, URLs, paths, and references
   - Uses simplified provider names and empty values
   - Default: no backup (use `--backup` to create .bak file)

## Common Commands

### Managing Proxy Provider Configuration

```bash
# Replace with real configuration from secrets file (for local development)
python3 tools/replace_proxy_providers.py

# Replace with custom paths
python3 tools/replace_proxy_providers.py -t /path/mihomo-custom.yaml -s /path/proxy-providers-secrets.yaml

# Create backup when replacing
python3 tools/replace_proxy_providers.py --backup
```

### Sanitizing Sensitive Information

```bash
# Sanitize using clean template (removes all sensitive data)
python3 tools/sanitize_provider_urls.py

# Sanitize with custom template
python3 tools/sanitize_provider_urls.py --template /path/to/clean-template.yaml

# Create backup when sanitizing
python3 tools/sanitize_provider_urls.py --backup
```

## Git Workflow

### Initial Setup

After cloning the repository, run the setup script to configure Git hooks:

```bash
cd /Users/deltav/Developer/02-Configuration-Files
./setup-hooks.sh
```

This configures Git to use `.githooks/` directory for hooks (one-time setup per clone).

### Pre-commit Hook

The repository uses a custom pre-commit hook (located at `.githooks/pre-commit`) that:
- Automatically runs `sanitize_provider_urls.py` on `mihomo-custom.yaml` before each commit
- Replaces all three provider blocks with clean template (no sensitive data)
- Stages the sanitized file if it was modified
- Ensures sensitive information is never committed to version control

### Workflow Pattern

1. **Daily Development**: Use `replace_proxy_providers.py` to work with real configurations
2. **Before Committing**: Pre-commit hook automatically sanitizes (no manual action needed)
3. **After Commit**: `mihomo-custom.yaml` in Git contains only placeholder data

### Commit Guidelines

Based on recent commit history, this repository follows conventional commits:
- `feat(config):` - Configuration additions or enhancements
- `fix(config):` - Configuration bug fixes
- `docs:` - Documentation updates
- `refactor:` - Code/config restructuring without functional changes

## YAML Structure Notes

### Anchor System

The configuration heavily uses YAML anchors for DRY principles:
- Provider templates: `&primary-provider-template`, `&backup-provider-template`
- Provider references: `&all-proxy-providers`, `&primary-proxy-providers`
- Proxy group templates: `&pg`, `&auto-select-group-template`

When modifying configurations, be aware that changes to anchored sections affect all references.

### Top-Level Blocks

Key top-level sections in mihomo-custom.yaml:
- `proxy-providers:` - Provider definitions (managed by Python tools)
- `proxies:` - Direct proxy node definitions (usually empty)
- `dns:` - DNS configuration with fake-ip mode
- `proxy-groups:` - Proxy selection strategies
- `rule-providers:` - External rule set definitions
- `rules:` - Routing rules

### Provider Configuration Pattern

**In proxy-providers-secrets.yaml (real configuration)**:
```yaml
01-Primary-Provider1:
  url: "https://real-subscription-url"
  path: ./proxy_provider/Provider1.yaml
  <<: *primary-provider-template
  override:
    additional-prefix: "p1-"
```

**In proxy-providers-clean.yaml (sanitized template)**:
```yaml
1.primary1:
  url: ""
  path: ""
  <<: *primary-provider-template
  override:
    additional-prefix: ""
```

## AI Service Optimization

The configuration includes specialized proxy groups for AI services (OpenAI, Claude, etc.):
- **AI稳定节点**: Uses `fallback` type with `consistent-hashing` strategy to minimize IP changes
- **AI自动优选**: Uses `url-test` for automatic optimal node selection
- Both groups filter for US/Singapore nodes and exclude invalid/test nodes
- Long health-check intervals (1-2 hours) to reduce IP fluctuations

When modifying AI-related rules, maintain the focus on IP stability over raw speed.

## Development Notes

- Python scripts use `pathlib.Path` for cross-platform path handling
- All scripts include detailed docstrings with usage examples
- Error handling uses broad exception catching with user-friendly messages
- Scripts use whole-block replacement for simplicity and reliability
- Both tools share the same `find_top_level_block_range()` function for YAML parsing
- Backup is opt-in (use `--backup` flag) to avoid clutter

## File Structure Summary

```
09-clash/
├── mihomo-custom.yaml              # Main config (auto-sanitized on commit)
├── proxy-providers-secrets.yaml    # Real secrets (git-ignored, never committed)
├── proxy-providers-clean.yaml      # Clean template (committed to git)
├── tools/
│   ├── replace_proxy_providers.py  # Secrets → mihomo-custom.yaml
│   └── sanitize_provider_urls.py   # Clean template → mihomo-custom.yaml
└── CLAUDE.md                        # This file
```
