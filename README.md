# Personal LLM CLI Configuration

Provider-agnostic agent workflows with provider-specific configs in `providers/`.

## Layout

- `AGENTS.md`: global behavior and documentation style
- `agents/`: reusable agent roles
- `commands/`: command definitions
- `skills/`: reusable skills and tooling
- `providers/claude-code/`: Claude Code settings, hooks, plugins, statusline, and workflows
- `providers/codex/`: Codex settings template
- `providers/*/agents/` and `providers/*/commands/`: generated model-mapped copies

## Usage

1. Copy a provider folder into your tool's config directory
2. Apply model tier mappings for that provider (see `model-tiers.json` and `scripts/apply-model-tiers.py`)
3. Restart the tool
