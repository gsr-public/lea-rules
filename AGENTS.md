# AGENTS.md - lea-open-rules

## Remediation key: `_remedy`, never `remedy`
- Every rule stores remediation commands under `cmd._remedy` (also when empty: `"_remedy": []`)
- Purpose: show the remediation commands while keeping remediation disabled by default; the LEA server only runs `cmd.remedy` (`server/routes_client.py`)
- New or edited rules must use `_remedy`; never add a `remedy` key
- `schema/rule.schema.json` requires `_remedy` in `cmd`; keep schema, README ("Remediation is disabled by default") and CONTRIBUTING in sync with this convention
- Enabling remediation = renaming `_remedy` to `remedy` at import time, done by the user, not in this repository

## Could not check: `unknown_re`, keep stderr
- Every expect block carries `unknown_re` (Linux/macOS `{"stderr": "Permission denied|Operation not permitted"}`, Windows the PowerShell access-denied pattern, see CONTRIBUTING); the LEA server records a match as *Could not check*, never a failure (`server/routes_client.py`)
- Commands keep stderr: no `2>/dev/null` except in the `cat /proc/*/comm 2>/dev/null | grep -q` service guard
- Never put an access marker (`Permission denied`, `LEA_RULE_no_access`) in `not_re`: a `not_re` match is a proven violation and wins over `unknown_re`

## Rule identity: `uid`
- Every rule has a `uid` (UUID v4). Never change or reuse it; LEA deployments track rules and their versions by uid
- New rule = new uid; renamed rule = same uid, old name appended to `former_names`; withdrawn rule = file deleted and an entry in `retired.json`
- The validate workflow rejects duplicate uids and former names that clash with other rules
- Framework profiles: `frameworks/<id>.json` (report wording, `schema/framework.schema.json`), `id` = file name = the `<id>` of `std:<id>` tags; new standard = tag rules + add a profile; keep legal text factual
- Packs: `tools/build_pack.py` (the LEA repo runs it via `./lea_release.sh rules` and signs with the GSR ed25519 rule-signing key)
