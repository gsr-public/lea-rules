# CLAUDE.md - lea-open-rules

## Remediation key: `_remedy`, never `remedy`
- Every rule stores remediation commands under `cmd._remedy` (also when empty: `"_remedy": []`)
- Purpose: show the remediation commands while keeping remediation disabled by default; the LEA server only runs `cmd.remedy` (`server/routes_client.py`)
- New or edited rules must use `_remedy`; never add a `remedy` key
- `schema/rule.schema.json` requires `_remedy` in `cmd`; keep schema, README ("Remediation is disabled by default") and CONTRIBUTING in sync with this convention
- Enabling remediation = renaming `_remedy` to `remedy` at import time, done by the user, not in this repository

## Rule identity: `uid`
- Every rule has a `uid` (UUID v4). Never change or reuse it; LEA deployments track rules and their versions by uid
- New rule = new uid; renamed rule = same uid, old name appended to `former_names`; withdrawn rule = file deleted and an entry in `retired.json`
- The validate workflow rejects duplicate uids and former names that clash with other rules
- Packs: `tools/build_pack.py` (the LEA repo runs it via `./lea_release.sh rules` and signs with the GSR ed25519 rule-signing key)
