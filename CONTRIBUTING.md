# Contributing

Thank you for helping improve LEA Open Rules. Pull requests with new rules, bug fixes and mapping corrections are welcome.

## Adding or changing a rule

1. Put exactly one rule object in `rules/<platform>/<category>/<slug>.json`.
   - `platform` is `linux`, `macos`, `windows`, or `multi` when the rule has validation blocks for more than one system.
   - `category` must equal the rule's `category` field.
   - `slug` is the rule name in lower case with every run of non-alphanumeric characters replaced by `-` (`+` becomes `plus`).
2. Follow the conventions described in the README:
   - Collect raw state only: `cat` of files and `/proc` entries, `stat`, `reg query`, read-only status commands. Do not filter on the client with `grep`, `awk`, `sed` or `cut`, and do not use `sudo` in commands. The only accepted `grep` is the service-presence guard: `if cat /proc/*/comm 2>/dev/null | grep -q '^name$'; then cat <config>; else echo 'LEA_RULE_no_service'; fi`.
   - Put all logic in the `expect` block as Python-compatible regular expressions. Prefer `[ \t]` over `\s` inside a line, use word boundaries (`\bname\b`), and anchor keyword checks at the start of a line so commented-out settings do not match.
   - Add `re: {"stdout": "\\S"}` next to a `not_re` when an empty or unreadable output must not pass.
   - Use one validation block and matching expect block(s) per system. Use the exact `/etc/os-release` `NAME` values in `distribution` filters.
   - Add a remedy (under `_remedy`, so it ships disabled) only when it is safe on every host the rule targets, idempotent and non-interactive, and make it print the re-validation output.
3. Write a description that states what is checked, why it matters, and any limits. If elevated rights are required, add `priv:required` and end the description with the exact command to delegate (see existing rules for the wording).
4. Add tags: `cat:<category>`, one `env:` tag per system plus `env:host_level`, `risk:low|medium|high`, and framework tags you can justify. Use the tag prefixes listed in the README; add `std:CIS` whenever you add a `std:CIS_Controls_v8:` tag. Do not add CIS Benchmark section numbers.
5. In the pull request, include sample command output for a passing and a failing host, so reviewers can check the regular expressions.

The `Validate rules` workflow checks every file against `schema/rule.schema.json`, compiles every regular expression, and checks file names, folders and duplicate names. Please make sure it passes.

## Mapping corrections

If you believe a framework mapping is wrong or missing, open an issue or pull request that cites the control text. Mappings are informative and are reviewed conservatively.

## License of contributions

By submitting a contribution you agree that it is licensed under the Apache License 2.0, as described in section 5 of the license.
