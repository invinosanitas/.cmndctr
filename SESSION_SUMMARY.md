IMPORTANT: A password was shared in chat; rotate credentials and use PAT or `gh auth login` for GitHub. Do not paste secrets into chat.

**What was done**
- Updated commands/docs workflows to use `/cc`, scan all `*.md`, and gate new docs to explicit user request.
- Updated doc-implementer instructions to only create new docs when explicitly requested.
- Fixed worktree paths to use `../worktreeN` instead of `/worktreeN`.
- Added `--clean` to `scripts/apply-model-tiers.py` and made it preserve provider overrides by default.
- Added `providers/claude-code/settings.unix.json` and `providers/claude-code/statusline.py`.
- Updated `README.md` usage to mention `settings.unix.json` and `--clean`.
- Regenerated provider copies with `--clean` for `codex` and `claude-code`.
- Committed in `.cmndctr`: `ee64be5` ("chore(config): align commands and add unix settings").

**In-progress / needs work**
- Submodule add in `/Users/quinn/Documents/GitHub/OriginBrandsCmnd` timed out mid-clone; repo now shows untracked `.cmndctr/`, with `.cmndctr/.git` pointing to `.git/modules/.cmndctr` and HEAD ref set to `.invalid`. No `.gitmodules` entry yet.
- Need to complete submodule setup with authenticated GitHub access (PAT or `gh auth login`), then configure project-local Codex/Claude usage.

**Recommended next steps (OriginBrandsCmnd)**
1. Clean partial submodule:
   ```sh
   cd /Users/quinn/Documents/GitHub/OriginBrandsCmnd
   git submodule deinit -f .cmndctr
   rm -rf .git/modules/.cmndctr .cmndctr
   rm -f .gitmodules
   ```
2. Authenticate (PAT or `gh auth login`) and re-add:
   ```sh
   git submodule add https://github.com/invinosanitas/.cmndctr.git .cmndctr
   git submodule update --init --recursive
   ```
3. Configure project-local Codex/Claude using relative paths to `./.cmndctr/providers/*` (symlinks or tool config path).
