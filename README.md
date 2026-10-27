# LEA Open Rules

An open library of 781 host security and compliance checks for Linux, macOS and Windows, in the rule format used by the LEA Platform.

- Website: https://gsr-lea.com
- Repository: https://github.com/gsr-public/lea-rules

## About the LEA Platform

LEA is a self-hosted compliance monitoring platform by GSR. Lightweight agents on each host run read-only commands and send the raw output (file contents, `/proc` values, registry queries) to the LEA server. The agents do not decide whether a host is compliant; the server validates the raw output against each rule, so detection logic can be changed centrally without touching endpoints. Results are stored as HMAC-signed evidence records mapped to frameworks such as CIS Controls, ISO/IEC 27001, SOC 2, CMMC, PCI DSS, HIPAA and NIST CSF, and are summarised in PDF reports for auditors and other stakeholders.

## What this repository contains

```
rules/<platform>/<category>/<rule-slug>.json   one rule per file
retired.json                                   rules withdrawn from the library (uid, name, reason)
schema/rule.schema.json                        JSON Schema for a rule file
tools/build_pack.py                            builds a signed LEA rule pack from rules/
MAPPINGS.md                                    framework control -> rules
CHANGELOG.md                                   release notes, renames, fixes
.github/workflows/validate.yml                 schema and regex validation
```

Platforms are `linux`, `macos`, `windows`, and `multi` for rules that cover more than one operating system (for example SSH server checks that run on both Linux and macOS). Each file is a single flat JSON object in exactly the shape the LEA admin API accepts, so it can be posted without conversion.

## Rule format

```json
{
  "uid": "1b0e5d0c-6f7e-4a59-9a43-2c1f0d7b8e21",
  "name": "SSH Root Login Disabled",
  "description": "What is checked, why it matters, and the minimum privilege needed.",
  "active": true,
  "category": "access_control",
  "cycle": 3600,
  "cmd_info_key": null,
  "cmd": {
    "validation": [
      {"command": "cat /etc/ssh/sshd_config", "system": ["Linux"], "distribution": []}
    ],
    "expect": [
      {"system": ["Linux"], "distribution": [],
       "re": {"stdout": "(?mi)^[ \\t]*PermitRootLogin[ \\t]+no\\b"},
       "not_re": {"stdout": "(?mi)^[ \\t]*PermitRootLogin[ \\t]+(?!no\\b)\\S"}}
    ],
    "_remedy": [],
    "system": []
  },
  "parameters": [],
  "tags": ["std:CIS", "std:CIS_Controls_v8:5.4", "std:SOC2:CC6.3", "cat:access_control", "env:linux", "env:host_level", "risk:high"]
}
```

| Field | Meaning |
|---|---|
| `uid` | Stable identity of the rule (UUID). It never changes, also when the rule is renamed; LEA deployments track versions and updates by it. |
| `name` | Unique, human-readable rule name. The file name is its kebab-case slug. |
| `former_names` | Optional: earlier names of the rule. A deployment that created the rule under such a name is matched to it on import. |
| `builtin` | Optional: platform rule (host name, MAC address, package inventory) that LEA creates and activates when the pack is imported. |
| `severity` | Optional: `informative`, `low`, `medium`, `high` or `critical`; otherwise LEA derives it from the `risk:` tag. |
| `description` | What the rule verifies and why. Rules that need elevated rights end with a `Required sudo rule` or `Required Windows permission` line naming the exact command to delegate. |
| `active` | Whether the rule is scheduled after import. |
| `category` | Functional group (also used to browse the library in the LEA console). |
| `cycle` | Seconds between evaluations (3600 by default; 43200 for expensive filesystem scans and signature-age checks). |
| `cmd_info_key` | Key under which LEA stores the output in the host's metadata (`cmd_info`, used by dynamic groups); `null` except for the built-in platform rules. |
| `cmd.validation` | Commands the agent runs. Each block has a `command`, a `system` filter (`Linux`, `Darwin`, `Windows`, compared with the agent's `uname` system) and a `distribution` filter. Linux and macOS commands run through `sh -c`; Windows commands run through PowerShell. When several blocks apply, their outputs are concatenated with newlines. |
| `cmd.expect` | Server-side checks on the raw output. `re` must match, `not_re` must not match (per stream: `stdout`, `stderr`), `returncode` must equal the exit code, `md5` must equal the stdout hash, and `function` calls a built-in LEA server check. All applicable blocks must pass. |
| `cmd._remedy` | Remediation commands that correct the setting, shipped disabled (see [Remediation is disabled by default](#remediation-is-disabled-by-default)). Empty when no safe, idempotent, non-interactive fix exists. |
| `parameters` | Rule parameters: `%name%` placeholders in commands with default values (`[{"name", "value", "type": "internal"}]`); sites tune the values per rule in LEA without forking the definition. |
| `tags` | `std:` framework mappings, `cat:` category, `env:` operating systems, `risk:` `low`/`medium`/`high`, and `priv:required` when the agent needs elevated rights. |

Conventions followed by every rule:

- Commands only read raw state (`cat /proc/...`, `cat` of configuration files, `stat`, `reg query`). There is no client-side `grep`, `awk`, `sed` or `cut` filtering and no `sudo` in commands; all interpretation happens on the server.
- Regular expressions are Python `re` syntax and use inline flags such as `(?m)`, `(?i)`, `(?s)`.
- Checks for an optional service print `LEA_RULE_no_service` when the service is not present, and the expect pattern accepts that marker. For example, SSH configuration rules pass on Linux hosts where no `sshd` process runs.
- Rules that only use `not_re` also require some output (`re: \S`), so an unreadable file fails instead of passing silently.
- Distribution filters use the exact `NAME` value from `/etc/os-release` (for example `Debian GNU/Linux`, `Red Hat Enterprise Linux`, `Rocky Linux`).

## How evaluation works

1. On each cycle the agent runs the `validation` commands that match its operating system and distribution and sends stdout, stderr and the exit code to the server.
2. The server selects the `expect` blocks for the same system and distribution. Blocks that name the host's distribution take precedence over blocks with an empty distribution list.
3. Every applicable `re`, `not_re`, `returncode`, `md5` or `function` check must succeed for the result to be recorded as passing. Each result, including the raw output and any failed pattern, is stored and signed as evidence.
4. If the result fails and the rule has an enabled `remedy` (see below), the server returns the remedy commands to the agent. The agent runs them and returns their output, which the server evaluates with the same expect blocks. Remedies in this library therefore end by printing the re-validation output (for example `sysctl -w kernel.kptr_restrict=1 >/dev/null && cat /proc/sys/kernel/kptr_restrict`).
5. The next scheduled validation confirms the state independently.

Remedies are applied at runtime only (for example `sysctl -w` does not persist across reboots).

### Remediation is disabled by default

Every rule stores its remediation commands under `cmd._remedy`, not `cmd.remedy`. The leading underscore keeps the commands in the rule (in this repository and in the rule stored by LEA after import) so they can be reviewed, while the LEA server only runs commands under a key named exactly `remedy`, so no remediation runs after import.

To enable remediation for a rule, rename `_remedy` to `remedy` in that rule before posting it (or edit the rule in LEA). Enable remedies deliberately, per rule and per group, after reviewing the commands for the hosts they will run on.

## Using the rules with LEA

The library ships to LEA deployments as a signed rule pack: `lea-rules-<version>.tgz` (the `rules/` tree plus a
`manifest.json` with every rule's uid, path and sha256, and the retired uids), a detached ed25519 signature
(`.tgz.sig`) and a `latest.json` feed. Every LEA release bundles the current pack; newer packs can be imported in the
console (Settings → Rule sources), with `lea rules import`, or with `./lea_rules.sh import` on air-gapped servers, and
connected servers can watch the feed. The server verifies the signature with GSR's public key before reading the pack.

Importing never changes running rules. New rules wait in the console's rule library (Rules → Add from library), changed
ones in Rules → Updates, where an administrator applies them to all hosts or to new hosts only (hosts already running a
rule keep their version until promoted). Built-in platform rules (`builtin`) are created and activated on import.

To run your own rules next to (or instead of) these, keep them in a repository with the same layout, build packs with
`python3 tools/build_pack.py --version 1.0.0 --key your-ed25519.key` (`openssl genpkey -algorithm ed25519 -out your-ed25519.key`)
and add a rule source with your public key in LEA (the `.sig` file prints it as `public_key`).

Review rule descriptions before you add rules to a group: some rules are intended only for a subset of hosts (for
example container-only rules, IPv6 forwarding on container hosts, SquashFS on Ubuntu hosts with snaps, UDF on Azure VMs,
Kernel FIPS Mode Enabled outside FIPS scope).

### Evidence report prefixes

The LEA compliance snapshot service selects rules for a framework report by tag prefix. A tag is counted when it equals the prefix or starts with the prefix followed by a colon:

| Report | Prefix the product expects | Tag form used here |
|---|---|---|
| CIS | `std:CIS` | `std:CIS` on every rule with a CIS Controls v8 safeguard, plus `std:CIS_Controls_v8:<safeguard>` |
| ISO 27001 | `std:ISO27001` | `std:ISO27001:A.8.9` (2022 Annex A; some rules also keep 2013 IDs) |
| SOC 2 | `std:SOC2` | `std:SOC2:CC6.1` |
| CMMC | `std:CMMC` | `std:CMMC:AC.L2-3.1.1` |

Because `std:CIS_Controls_v8:...` does not start with `std:CIS:`, the generic `std:CIS` tag is what includes a rule in the CIS report; the safeguard tag documents the mapping. NIST SP 800-53, PCI DSS 4.0, NIS2, DORA, HIPAA, NIST CSF 2.0, ASD Essential Eight and post-quantum tags are informative and are not used by the current evidence reports.

## Coverage

All counts are computed from the files in `rules/`.

Rules by platform folder:

| Platform | Rules |
|---|---|
| linux | 356 |
| macos | 78 |
| windows | 299 |
| multi | 48 |
| **Total** | **781** |

Rules that run on each operating system (multi-platform rules counted once per system): Linux 403, macOS 121, Windows 311.

Rules by category:

| Category | linux | macos | windows | multi | Total |
|---|---|---|---|---|---|
| access_control | 23 | 14 | 69 | 15 | 121 |
| application_security | 4 | 0 | 0 | 0 | 4 |
| audit | 54 | 5 | 49 | 2 | 110 |
| authentication | 6 | 6 | 27 | 10 | 49 |
| container_security | 15 | 0 | 0 | 0 | 15 |
| identity_management | 16 | 5 | 3 | 0 | 24 |
| integrity | 8 | 7 | 39 | 3 | 57 |
| inventory | 0 | 0 | 0 | 1 | 1 |
| kernel_security | 49 | 1 | 6 | 0 | 56 |
| metadata | 0 | 0 | 0 | 2 | 2 |
| network_security | 87 | 22 | 54 | 8 | 171 |
| password_policy | 17 | 5 | 7 | 4 | 33 |
| system_hardening | 77 | 13 | 45 | 3 | 138 |
| **Total** | **356** | **78** | **299** | **48** | **781** |

Rules by framework (a rule is counted once per framework, however many controls it maps to):

| Framework | Tag prefix | Rules | Distinct controls |
|---|---|---|---|
| CIS Controls v8 | `std:CIS_Controls_v8:` | 697 | 35 safeguards |
| CIS (product report tag) | `std:CIS` | 697 | - |
| NIST SP 800-53 Rev. 5 | `std:NIST_800-53:` | 778 | 46 |
| ISO/IEC 27001:2022 Annex A | `std:ISO27001:` | 776 | 22 (2022 IDs) |
| SOC 2 | `std:SOC2:` | 768 | 10 |
| CMMC 2.0 Level 2 | `std:CMMC:` | 764 | 39 |
| PCI DSS 4.0 | `std:PCI_DSS_4:` | 730 | 39 |
| NIS2 Art. 21(2) | `std:NIS2:` | 758 | 7 |
| DORA | `std:DORA:` | 761 | 2 |
| HIPAA Security Rule | `std:HIPAA:` | 768 | 16 |
| NIST CSF 2.0 | `std:NIST_CSF_2:` | 772 | 16 |
| ASD Essential Eight | `std:ASD_E8:` | 59 | 6 |
| Post-quantum readiness | `std:NIST_PQC:` | 31 | - |

Other facts: 109 rules include a remedy under `_remedy`; 157 rules are tagged `priv:required`; 1 rule is inactive (deprecated); 3 rules are built-in platform rules (`builtin`).

See [MAPPINGS.md](MAPPINGS.md) for the full control-to-rule mapping.

## Post-quantum readiness pack

31 rules, tagged `std:NIST_PQC:`, check the cryptographic baseline that a migration to post-quantum and hybrid key exchange depends on: retiring legacy protocols and weak algorithms (which are exposed to harvest-now-decrypt-later collection), and confirming that the installed software can negotiate hybrid post-quantum key exchange.

| Area | Rules |
|---|---|
| Post-quantum capability | OpenSSH Version Supports Post-Quantum Key Exchange; SSH Server Post-Quantum Key Exchange Not Removed; OpenSSL Provides Native ML-KEM (OpenSSL 3.5+); OpenSSL 1.1.1 or 3.x Crypto Baseline |
| System crypto policy | System Crypto Policy FUTURE or FIPS; System Crypto Policy Not LEGACY; Windows FIPS-Compliant Algorithms Enforced |
| Protocol baseline | OpenSSL System Minimum Protocol TLS 1.2 or Higher; GnuTLS Legacy Protocols Disabled; Java TLS Legacy Protocols and Weak Algorithms Disabled; Windows Legacy SSL/TLS Server Protocols Not Enabled; Windows TLS 1.0 Server Protocol Disabled; Windows TLS 1.1 Server Protocol Disabled; Windows TLS 1.2 Server Protocol Not Disabled; .NET Framework Strong Cryptography Enabled (64-bit); .NET Framework Strong Cryptography Enabled (32-bit); Windows .NET Framework Uses System Default TLS Versions (32-bit); Windows .NET Framework Uses System Default TLS Versions (64-bit); Windows SSL 2.0 Server Protocol Disabled; Windows SSL 3.0 Client Protocol Disabled; Windows SSL 3.0 Server Protocol Disabled; Windows TLS 1.0 Client Protocol Disabled; Windows TLS 1.1 Client Protocol Disabled |
| Algorithms and key sizes | SSH Legacy Algorithms Disabled; SSH Host RSA Key At Least 3072 Bits; OpenSSL Default Cipher List Excludes Weak Ciphers; Java JAR Weak Signature Algorithms Disabled; Windows SChannel RC4 Ciphers Not Enabled; Windows SChannel Triple-DES Cipher Disabled; Windows Diffie-Hellman Server Minimum Key Size 2048 Bits; Windows SChannel NULL, DES and RC2 Ciphers Not Enabled |

These rules indicate readiness; they do not test that post-quantum algorithms are negotiated in production traffic.

## Contributing

Contributions of new rules, fixes and mapping corrections are welcome. See [CONTRIBUTING.md](CONTRIBUTING.md). To report a security issue, see [SECURITY.md](SECURITY.md).

## Disclaimer

Framework mappings in this repository are informative. They are not an official CIS Benchmark, are not endorsed by the Center for Internet Security or any other standards body, and passing these rules is not an audit opinion or a certification under any framework. Validate the rules and mappings against your own requirements before relying on them.

"CIS" and "CIS Controls" are trademarks of the Center for Internet Security, Inc. Other framework names are the property of their respective owners.

## License

Apache License 2.0. See [LICENSE](LICENSE).
