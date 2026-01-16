#!/usr/bin/env python3
import json
import re
import shutil
import sys
from pathlib import Path


def load_mapping(root, provider):
    tiers_path = root / "model-tiers.json"
    if not tiers_path.exists():
        print(f"ERROR: Missing model tiers file: {tiers_path}")
        sys.exit(1)

    data = json.loads(tiers_path.read_text())
    providers = data.get("providers", {})
    mapping = providers.get(provider)
    if not mapping:
        print(f"ERROR: Provider not found in model-tiers.json: {provider}")
        sys.exit(1)

    return mapping


def apply_mapping(content, mapping, source_path):
    def replace(match):
        tier = match.group(1)
        model = mapping.get(tier)
        if not model:
            print(f"ERROR: Missing mapping for {tier} in {source_path}")
            sys.exit(1)
        return f"model: {model}"

    return re.sub(r"^model:\s*(tier-[\w-]+)\s*$", replace, content, flags=re.MULTILINE)


def sync_dir(src_dir, dest_dir, mapping):
    if dest_dir.exists():
        shutil.rmtree(dest_dir)
    dest_dir.mkdir(parents=True, exist_ok=True)

    for src_file in src_dir.rglob("*.md"):
        rel_path = src_file.relative_to(src_dir)
        dest_file = dest_dir / rel_path
        dest_file.parent.mkdir(parents=True, exist_ok=True)
        content = src_file.read_text()
        dest_file.write_text(apply_mapping(content, mapping, src_file))


def main():
    if len(sys.argv) != 2 or sys.argv[1] in {"-h", "--help"}:
        print("Usage: apply-model-tiers.py <provider>")
        sys.exit(1)

    provider = sys.argv[1]
    root = Path(__file__).resolve().parents[1]
    provider_dir = root / "providers" / provider
    if not provider_dir.exists():
        print(f"ERROR: Provider folder not found: {provider_dir}")
        sys.exit(1)

    mapping = load_mapping(root, provider)

    for name in ["agents", "commands"]:
        src_dir = root / name
        if not src_dir.exists():
            continue
        sync_dir(src_dir, provider_dir / name, mapping)

    print(f"OK: Wrote model-mapped files to {provider_dir}")


if __name__ == "__main__":
    main()
