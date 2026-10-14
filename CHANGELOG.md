# Changelog

## v1.0.0 - 2026-10-14

First public release: 244 rules.

### Exported

- 123 rules exported from the LEA Platform production rule set (129 production rules, 6 not exported, see below).
- 97 of the exported rules were renamed to clearer, outcome-oriented names (table below).
- The 22 legacy one-rule-per-file CIS drafts that preceded the production set were not exported separately. Each duplicated a production rule; their remaining ideas (core dump resource limit, time synchronization daemon, firewall per distribution family) are included as improved rules.

Not exported:

| Original rule | Reason |
|---|---|
| Host Name | Platform-internal host metadata collector, not a security control |
| MAC Address | Platform-internal host metadata collector, not a security control |
| Package Inventory Snapshot | Platform-internal asset inventory collector, not a security control |
| SSH Protocol Version 2 Only (Linux-only variant) | Duplicate of the multi-platform rule |
| Reverse Path Filtering Enabled | Duplicate of the two per-key reverse path filter rules |
| Martian Packet Logging Enabled | Duplicate of the two per-key martian logging rules |

No rule contained secrets or credentials in `parameters`; all exported rules have an empty parameter list.

### Added

- 121 new rules: 59 Linux, 11 macOS, 37 Windows and 14 multi-platform (SSH server rules that run on Linux and macOS).
- 10 of the new rules extend the post-quantum readiness pack (23 rules in total).

### Framework mappings

- Every rule now carries framework tags derived from a consistent control mapping: CIS Controls v8 safeguards (`std:CIS_Controls_v8:`), NIST SP 800-53 (`std:NIST_800-53:`), ISO/IEC 27001:2022 Annex A (`std:ISO27001:`), SOC 2 (`std:SOC2:`), CMMC 2.0 Level 2 (`std:CMMC:`), PCI DSS 4.0 (`std:PCI_DSS_4:`), NIS2 Article 21(2) (`std:NIS2:`) and DORA (`std:DORA:`).
- Removed CIS Benchmark section numbers (`std:CIS:5.2.8`, `std:CIS:5.3.1`) that could not be verified against a specific benchmark version; the generic `std:CIS` tag is kept.
- Replaced `std:PCI_DSS`, `std:PCI_DSS:4.0` and PCI requirement tags with PCI DSS 4.0 requirement numbers under `std:PCI_DSS_4:`; corrected requirement numbers (password history is 8.3.7, complexity is 8.3.6, password change interval is 8.3.9).
- Replaced `std:EU:DORA` with `std:DORA:Art9`; removed `std:NIST_800-53:AC-1` (a policy control) from the UAC rule.

### Fixed in exported rules

- Distribution filters now use the exact `NAME` values from `/etc/os-release` (for example `Debian GNU/Linux`, `Red Hat Enterprise Linux`, `Rocky Linux`). The LEA server matches the agent's distribution name as a substring of each listed value, so short names such as `Debian` or `Red Hat` never matched.
- Rules with several validation commands whose output was checked with `^0$` could never pass (the agent joins outputs with newlines). Source routing, ICMP redirect and IPv4/IPv6 forwarding rules now read all values in one command and require every value to match.
- `/etc/shadow` and `/etc/passwd` permission rules use a single `stat` format string per platform; the macOS variant previously parsed Linux `stat` output and always failed.
- Windows Defender service check now calls `sc.exe`; in PowerShell `sc` is an alias of `Set-Content`.
- Windows SMBv1 client check now reads the `mrxsmb10` driver start type (the actual control) instead of a non-existent LanmanWorkstation value.
- Windows SCHANNEL legacy protocol, firewall profile and TLS 1.2 checks no longer let a match run across unrelated registry keys or profiles; the TLS 1.2 registry path is quoted for PowerShell.
- Java TLS and JAR algorithm rules evaluate backslash continuation lines in `java.security` and search all installed OpenJDK runtimes instead of only Java 11.
- SSH rules read `sshd_config` drop-in files, reject conflicting insecure values, ignore indented comments and pass with `LEA_RULE_no_service` when no sshd process runs on Linux. `SSH Idle Session Timeout Configured` no longer accepts `ClientAliveCountMax 0`, which disables termination since OpenSSH 8.2. `SSH Protocol Version 2 Only` became `SSH Legacy Protocol 1 Not Enabled`, because OpenSSH 7.4+ ignores the Protocol keyword.
- `Unprivileged eBPF Disabled` accepts value 2 (Ubuntu default). `Linux TCP SYN Backlog At Least 2000` accepts values of 10000 and above. `Root Filesystem Usage Below 85%` accepts single-digit percentages. `Microsoft Defender for Endpoint Definitions Up to Date` accepts the quoted value printed by `mdatp health`. `AppArmor Enabled` reads `/sys/module/apparmor/parameters/enabled` instead of `apparmor_status` (needs root on current releases).
- `Offensive Security Tools Not Running` uses `ps -axco command` on macOS so user names in paths cannot cause false matches.
- `OpenSSL 1.1.1 or 3.x Crypto Baseline` and `OpenSSL System Minimum Protocol TLS 1.2 or Higher` no longer run on macOS, where `/usr/bin/openssl` is LibreSSL and the checks always failed; the minimum protocol rule also accepts TLSv1.3.
- `Telnet Server Not Listening` reads `/proc/net/tcp` and `/proc/net/tcp6` instead of `ss`.
- Remedies now print the re-validation output (the server evaluates the remedy output with the same expect blocks). Remedies that can break legitimate configurations were removed: IPv4/IPv6 forwarding (container hosts, routers), IPv6 router advertisement acceptance (SLAAC hosts), macOS forwarding (Internet Sharing) and Windows `Tcp1323Opts` (also disables TCP window scaling). Reverse path filter remedies apply loose mode (2). The typo in the `EnablePMTUDiscovery` remedy registry path was fixed.

### Renamed

| Original name | New name |
|---|---|
| .NET Strong Crypto Enabled 32bit | .NET Framework Strong Cryptography Enabled (32-bit) |
| .NET Strong Crypto Enabled 64bit | .NET Framework Strong Cryptography Enabled (64-bit) |
| ASLR Enabled | Kernel ASLR Fully Enabled |
| Account Lockout Policy Configured | Windows Account Lockout Threshold 1-10 Attempts |
| Administrator Account Renamed | Windows Built-in Administrator Account Renamed |
| Anti-Malware Service Running | Windows Defender Antivirus Service Running |
| Audit Log Retention Configured | Audit Logs Retained Instead of Overwritten |
| Audit Log Storage Size Configured | Audit Log File Size Limit At Least 20 MB |
| Audit Service Running | Linux Audit Daemon (auditd) Running |
| Automatic Updates Enabled | Automatic Security Updates Enabled |
| Avahi Service Disabled | Avahi mDNS Daemon Not Running |
| Blacklisted Offensive Tools Not Running | Offensive Security Tools Not Running |
| CUPS Service Disabled | CUPS Print Daemon Not Running |
| Cloud Default User Absent | Cloud Image Default Accounts Removed |
| Container SSH Server Not Running | SSH Server Not Running in Container |
| Core Dumps Restricted | SUID Program Core Dumps Disabled |
| Cramfs Module Disabled | cramfs Filesystem Module Not Loaded |
| Disk Capacity Threshold | Root Filesystem Usage Below 85% |
| Disk Encryption Enabled (Linux) | Linux Encrypted Volumes Configured (crypttab) |
| Disk Encryption Enabled (Windows) | Windows BitLocker System Drive Fully Encrypted |
| Disk Encryption Enabled (macOS) | macOS FileVault Enabled |
| Docker Socket Not Mounted | Docker Socket Not Exposed |
| Firewall Default Policy Secure | Linux Firewall Default Deny Policy (iptables) |
| Guest Account Disabled | Windows Guest Account Disabled |
| ICMP Redirects Disabled | Linux ICMP Redirects Not Accepted (All Interfaces) |
| IP Forwarding Disabled | Linux IPv6 Forwarding Disabled |
| Inactive Accounts Locked | Inactive Accounts Disabled Within 30 Days |
| Java TLS Weak Algorithms Disabled | Java TLS Legacy Protocols and Weak Algorithms Disabled |
| Kernel Modules Locked | Kernel Module Loading Disabled at Runtime |
| Kernel dmesg Restricted | Kernel Log Access (dmesg) Restricted |
| Linux AIDE Installed | File Integrity Monitoring (AIDE) Installed |
| Linux Firewall Service Running | Linux Host Firewall Active (ufw or firewalld) |
| Linux ICMP Broadcast Ignore Enabled | Linux ICMP Broadcast Echo Ignored |
| Linux IP Forwarding Disabled | Linux IPv4 Forwarding Disabled |
| Linux IPv6 Router Advertisements Disabled All | Linux IPv6 Router Advertisements Not Accepted (All Interfaces) |
| Linux IPv6 Router Advertisements Disabled Default | Linux IPv6 Router Advertisements Not Accepted (Default) |
| Linux Ignore Bogus ICMP Error Responses | Linux Bogus ICMP Error Responses Ignored |
| Linux Kernel Pointer Restriction Enabled | Kernel Pointer Exposure Restricted |
| Linux Protected FIFOs Strict | Kernel Protected FIFOs Enforced |
| Linux Protected Hardlinks Enabled | Kernel Protected Hardlinks Enabled |
| Linux Protected Regular Files Strict | Kernel Protected Regular Files Enforced |
| Linux Protected Symlinks Enabled | Kernel Protected Symlinks Enabled |
| Linux RFC1337 Protection Enabled | Linux TIME-WAIT Assassination Protection (RFC 1337) |
| Linux Sudo Installed | Sudo Installed for Controlled Privilege Escalation |
| Linux Swappiness Tuned | Linux Swappiness Within Controlled Range |
| Linux System Crypto Policy Future Or FIPS | System Crypto Policy FUTURE or FIPS |
| Linux TCP FIN Timeout Optimized | Linux TCP FIN Timeout Bounded (15-60 Seconds) |
| Linux TCP Keepalive Time Optimized | Linux TCP Keepalive Time Bounded (300-900 Seconds) |
| Linux TCP Max SYN Backlog Sized | Linux TCP SYN Backlog At Least 2000 |
| Linux TCP Retries2 Bounded | Linux TCP Retransmission Limit Bounded (5-15) |
| Linux TCP Syncookies Enabled | Linux TCP SYN Cookies Enabled |
| Linux Unprivileged BPF Disabled | Unprivileged eBPF Disabled |
| Linux Yama Ptrace Scope Restricted | Ptrace Scope Restricted (Yama) |
| Linux mmap Minimum Address Hardened | Low Memory Mapping Restricted (mmap_min_addr) |
| Local Password Maximum Age | Password Maximum Age 90 Days or Less |
| Local Password Minimum Age | Password Minimum Age At Least 1 Day |
| Local Password Minimum Length | Password Minimum Length At Least 12 Characters |
| Local Password Warning Period | Password Expiry Warning At Least 7 Days |
| MDATP Daemon Running | Microsoft Defender for Endpoint Running (macOS) |
| MDATP Definitions Up To Date | Microsoft Defender for Endpoint Definitions Up to Date |
| Multi-Platform Account Lockout Policy | Account Lockout Enforced After Failed Logins |
| Network Boundaries | Outbound TCP Connections Within Network Boundary |
| No Empty Passwords | No Accounts with Empty Passwords |
| No Unauthorized UID 0 Accounts | Root Is the Only UID 0 Account |
| No Unowned Files | No Unowned Files on Local Filesystems |
| No World Writable Files | No World-Writable Files on Local Filesystems |
| OpenSSL Version Quantum-Transition Ready | OpenSSL 1.1.1 or 3.x Crypto Baseline |
| OpenSSL Weak Ciphers Disabled | OpenSSL Default Cipher List Excludes Weak Ciphers |
| Passwd File Permissions Secure | /etc/passwd Permissions 644 or Stricter |
| Password Complexity Requirements Configured | Password Complexity Enforced (pwquality) |
| Password History Enforced | Password Reuse Limited (History of 5 or More) |
| RDP Network Level Authentication Required | Windows RDP Network Level Authentication Required |
| Remote Desktop Disabled | Windows Remote Desktop Disabled |
| SSH Idle Timeout Configured | SSH Idle Session Timeout Configured |
| SSH Protocol Version 2 Only | SSH Legacy Protocol 1 Not Enabled |
| Samba SMBv1 Disabled | Samba SMBv1 (NT1) Not Allowed |
| Shadow File Permissions Secure | /etc/shadow Permissions and Ownership Restricted |
| Source Routing Disabled | Linux Source-Routed Packets Rejected (All Interfaces) |
| System TLS Minimum Protocol TLS1.2 | OpenSSL System Minimum Protocol TLS 1.2 or Higher |
| Telnet Service Disabled | Telnet Server Not Listening |
| Time Synchronization Enabled | Linux System Clock Synchronized |
| User Account Control Enabled | Windows User Account Control Enabled |
| Windows FIPS Algorithm Policy Enabled | Windows FIPS-Compliant Algorithms Enforced |
| Windows Firewall Enabled | Windows Firewall Enabled for All Profiles |
| Windows ICMP Redirects Disabled | Windows ICMP Redirects Not Accepted |
| Windows Legacy TLS Protocols Disabled | Windows Legacy SSL/TLS Server Protocols Not Enabled |
| Windows PMTU Blackhole Detection Disabled | Windows PMTU Black Hole Detection Disabled |
| Windows Password History Size | Windows Password History At Least 4 |
| Windows SMBv1 Client Disabled | Windows SMBv1 Client Driver Disabled |
| Windows TCP SYN Protection Enabled | Windows TCP SYN Attack Protection Enabled |
| Windows TLS12 Or Higher Enabled | Windows TLS 1.2 Server Protocol Not Disabled |
| Xinetd Service Not Running | xinetd Super-Server Not Running |
| macOS Firewall Enabled | macOS Application Firewall Enabled |
| macOS IPv4 ICMP Redirects Disabled | macOS ICMP Redirects Not Sent |
| macOS IPv6 Redirect Accept Disabled | macOS IPv6 ICMP Redirects Not Accepted |
| macOS Password Minimum Length Policy | macOS Password Minimum Length At Least 12 |
| macOS Screen Lock Short Delay | macOS Screen Lock Password Delay Within 5 Minutes |

### New rules

- SSH Empty Password Logins Rejected (`rules/multi/authentication/ssh-empty-password-logins-rejected.json`)
- SSH Maximum Authentication Attempts 4 or Fewer (`rules/multi/authentication/ssh-maximum-authentication-attempts-4-or-fewer.json`)
- SSH X11 Forwarding Disabled (`rules/multi/access_control/ssh-x11-forwarding-disabled.json`)
- SSH Login Grace Time 60 Seconds or Less (`rules/multi/access_control/ssh-login-grace-time-60-seconds-or-less.json`)
- SSH Warning Banner Configured (`rules/multi/access_control/ssh-warning-banner-configured.json`)
- SSH Host-Based Authentication Disabled (`rules/multi/authentication/ssh-host-based-authentication-disabled.json`)
- SSH .rhosts Files Ignored (`rules/multi/authentication/ssh-rhosts-files-ignored.json`)
- SSH User Environment Overrides Disabled (`rules/multi/access_control/ssh-user-environment-overrides-disabled.json`)
- SSH Weak MAC Algorithms Not Enabled (`rules/multi/network_security/ssh-weak-mac-algorithms-not-enabled.json`)
- SSH Weak Ciphers Not Enabled (`rules/multi/network_security/ssh-weak-ciphers-not-enabled.json`)
- SSH Server Post-Quantum Key Exchange Not Removed (`rules/multi/network_security/ssh-server-post-quantum-key-exchange-not-removed.json`)
- OpenSSH Version Supports Post-Quantum Key Exchange (`rules/multi/network_security/openssh-version-supports-post-quantum-key-exchange.json`)
- sshd_config Permissions Restricted (`rules/linux/access_control/sshd-config-permissions-restricted.json`)
- SSH Host RSA Key At Least 3072 Bits (`rules/multi/network_security/ssh-host-rsa-key-at-least-3072-bits.json`)
- SSH DSA Host Key Absent (`rules/multi/network_security/ssh-dsa-host-key-absent.json`)
- rsh, rlogin and rexec Servers Not Running (`rules/linux/network_security/rsh-rlogin-and-rexec-servers-not-running.json`)
- FTP Server Not Running (`rules/linux/network_security/ftp-server-not-running.json`)
- TFTP Server Not Running (`rules/linux/network_security/tftp-server-not-running.json`)
- SNMP Daemon Not Running (`rules/linux/network_security/snmp-daemon-not-running.json`)
- NIS Services Not Running (`rules/linux/network_security/nis-services-not-running.json`)
- Mail Transfer Agent Listens Only on Loopback (`rules/linux/network_security/mail-transfer-agent-listens-only-on-loopback.json`)
- Cron Daemon Running (`rules/linux/system_hardening/cron-daemon-running.json`)
- System Logging Daemon Running (`rules/linux/audit/system-logging-daemon-running.json`)
- Time Synchronization Daemon Running (`rules/linux/system_hardening/time-synchronization-daemon-running.json`)
- Journald Persistent Storage Configured (`rules/linux/audit/journald-persistent-storage-configured.json`)
- Remote Log Forwarding Configured (rsyslog) (`rules/linux/audit/remote-log-forwarding-configured-rsyslog.json`)
- Auditing Enabled for Processes Started Before auditd (`rules/linux/audit/auditing-enabled-for-processes-started-before-auditd.json`)
- Audit Rules Watch Identity Files (`rules/linux/audit/audit-rules-watch-identity-files.json`)
- Audit Rules Watch Sudoers Changes (`rules/linux/audit/audit-rules-watch-sudoers-changes.json`)
- Audit Rules Track Kernel Module Loading (`rules/linux/audit/audit-rules-track-kernel-module-loading.json`)
- Audit Rules Track System Time Changes (`rules/linux/audit/audit-rules-track-system-time-changes.json`)
- Audit Configuration Immutable (`rules/linux/audit/audit-configuration-immutable.json`)
- Kernel perf_event Access Restricted (`rules/linux/kernel_security/kernel-perf-event-access-restricted.json`)
- Core Dumps Disabled via Resource Limits (`rules/linux/system_hardening/core-dumps-disabled-via-resource-limits.json`)
- Kernel FIPS Mode Enabled (`rules/linux/system_hardening/kernel-fips-mode-enabled.json`)
- Linux ICMP Redirects Not Accepted (Default) (`rules/linux/network_security/linux-icmp-redirects-not-accepted-default.json`)
- Linux Source-Routed Packets Rejected (Default) (`rules/linux/network_security/linux-source-routed-packets-rejected-default.json`)
- SELinux Enforcing at Boot (`rules/linux/kernel_security/selinux-enforcing-at-boot.json`)
- freevxfs Filesystem Module Not Loaded (`rules/linux/kernel_security/freevxfs-filesystem-module-not-loaded.json`)
- HFS Filesystem Module Not Loaded (`rules/linux/kernel_security/hfs-filesystem-module-not-loaded.json`)
- HFS+ Filesystem Module Not Loaded (`rules/linux/kernel_security/hfsplus-filesystem-module-not-loaded.json`)
- JFFS2 Filesystem Module Not Loaded (`rules/linux/kernel_security/jffs2-filesystem-module-not-loaded.json`)
- SquashFS Filesystem Module Not Loaded (`rules/linux/kernel_security/squashfs-filesystem-module-not-loaded.json`)
- UDF Filesystem Module Not Loaded (`rules/linux/kernel_security/udf-filesystem-module-not-loaded.json`)
- USB Mass Storage Driver Not Loaded (`rules/linux/kernel_security/usb-mass-storage-driver-not-loaded.json`)
- DCCP Protocol Module Not Loaded (`rules/linux/network_security/dccp-protocol-module-not-loaded.json`)
- SCTP Protocol Module Not Loaded (`rules/linux/network_security/sctp-protocol-module-not-loaded.json`)
- /tmp Is a Separate Mount (`rules/linux/system_hardening/tmp-is-a-separate-mount.json`)
- /tmp Mounted with nodev (`rules/linux/system_hardening/tmp-mounted-with-nodev.json`)
- /tmp Mounted with nosuid (`rules/linux/system_hardening/tmp-mounted-with-nosuid.json`)
- /tmp Mounted with noexec (`rules/linux/system_hardening/tmp-mounted-with-noexec.json`)
- /dev/shm Mounted with nodev (`rules/linux/system_hardening/dev-shm-mounted-with-nodev.json`)
- /dev/shm Mounted with nosuid (`rules/linux/system_hardening/dev-shm-mounted-with-nosuid.json`)
- /dev/shm Mounted with noexec (`rules/linux/system_hardening/dev-shm-mounted-with-noexec.json`)
- /var/tmp Mount Options Hardened (`rules/linux/system_hardening/var-tmp-mount-options-hardened.json`)
- /etc/group Permissions 644 or Stricter (`rules/linux/system_hardening/etc-group-permissions-644-or-stricter.json`)
- /etc/gshadow Permissions and Ownership Restricted (`rules/linux/system_hardening/etc-gshadow-permissions-and-ownership-restricted.json`)
- /etc/crontab Permissions Restricted (`rules/linux/system_hardening/etc-crontab-permissions-restricted.json`)
- /etc/sudoers Permissions 440 or Stricter (`rules/linux/system_hardening/etc-sudoers-permissions-440-or-stricter.json`)
- Password Hashes Not Stored in /etc/passwd (`rules/linux/identity_management/password-hashes-not-stored-in-etc-passwd.json`)
- System Accounts Use Non-Login Shells (`rules/linux/identity_management/system-accounts-use-non-login-shells.json`)
- Default umask 027 or Stricter (`rules/linux/system_hardening/default-umask-027-or-stricter.json`)
- Strong Password Hashing Algorithm (SHA-512 or yescrypt) (`rules/linux/password_policy/strong-password-hashing-algorithm-sha-512-or-yescrypt.json`)
- Password Minimum Length At Least 14 (pwquality) (`rules/linux/password_policy/password-minimum-length-at-least-14-pwquality.json`)
- Account Lockout After 5 or Fewer Failures (faillock) (`rules/linux/authentication/account-lockout-after-5-or-fewer-failures-faillock.json`)
- Account Lockout Duration At Least 15 Minutes (faillock) (`rules/linux/authentication/account-lockout-duration-at-least-15-minutes-faillock.json`)
- Sudo Commands Run in a Pseudo-Terminal (`rules/linux/access_control/sudo-commands-run-in-a-pseudo-terminal.json`)
- Sudo Activity Logged to a Dedicated File (`rules/linux/audit/sudo-activity-logged-to-a-dedicated-file.json`)
- su Restricted to an Administrative Group (pam_wheel) (`rules/linux/access_control/su-restricted-to-an-administrative-group-pam-wheel.json`)
- hosts.equiv Trust File Empty or Absent (`rules/linux/authentication/hosts-equiv-trust-file-empty-or-absent.json`)
- Package Signature Verification Enforced (`rules/linux/integrity/package-signature-verification-enforced.json`)
- System Crypto Policy Not LEGACY (`rules/linux/system_hardening/system-crypto-policy-not-legacy.json`)
- OpenSSL Provides Native ML-KEM (OpenSSL 3.5+) (`rules/linux/system_hardening/openssl-provides-native-ml-kem-openssl-3-5plus.json`)
- macOS Gatekeeper Enabled (`rules/macos/integrity/macos-gatekeeper-enabled.json`)
- macOS System Integrity Protection Enabled (`rules/macos/integrity/macos-system-integrity-protection-enabled.json`)
- macOS Firewall Stealth Mode Enabled (`rules/macos/network_security/macos-firewall-stealth-mode-enabled.json`)
- macOS Firewall Logging Enabled (`rules/macos/audit/macos-firewall-logging-enabled.json`)
- macOS Automatic Update Check Enabled (`rules/macos/system_hardening/macos-automatic-update-check-enabled.json`)
- macOS Security Responses Installed Automatically (`rules/macos/system_hardening/macos-security-responses-installed-automatically.json`)
- macOS Remote Login (SSH) Disabled (`rules/macos/access_control/macos-remote-login-ssh-disabled.json`)
- macOS Remote Apple Events Disabled (`rules/macos/access_control/macos-remote-apple-events-disabled.json`)
- macOS Guest Account Disabled (`rules/macos/identity_management/macos-guest-account-disabled.json`)
- macOS Automatic Login Disabled (`rules/macos/authentication/macos-automatic-login-disabled.json`)
- macOS Network Time Synchronization Enabled (`rules/macos/system_hardening/macos-network-time-synchronization-enabled.json`)
- Windows SMB Server Signing Required (`rules/windows/network_security/windows-smb-server-signing-required.json`)
- Windows SMB Client Signing Required (`rules/windows/network_security/windows-smb-client-signing-required.json`)
- Windows LSA Protection (RunAsPPL) Enabled (`rules/windows/authentication/windows-lsa-protection-runasppl-enabled.json`)
- Windows WDigest Plaintext Credential Caching Disabled (`rules/windows/authentication/windows-wdigest-plaintext-credential-caching-disabled.json`)
- Windows LM Hash Storage Disabled (`rules/windows/authentication/windows-lm-hash-storage-disabled.json`)
- Windows NTLMv2 Only Authentication (`rules/windows/authentication/windows-ntlmv2-only-authentication.json`)
- Windows Anonymous SAM Enumeration Restricted (`rules/windows/access_control/windows-anonymous-sam-enumeration-restricted.json`)
- Windows Defender Real-Time Protection Enabled (`rules/windows/integrity/windows-defender-real-time-protection-enabled.json`)
- Windows Defender Signatures Updated Within 7 Days (`rules/windows/integrity/windows-defender-signatures-updated-within-7-days.json`)
- Windows Defender Tamper Protection Enabled (`rules/windows/integrity/windows-defender-tamper-protection-enabled.json`)
- Windows BitLocker Protection On for System Drive (`rules/windows/system_hardening/windows-bitlocker-protection-on-for-system-drive.json`)
- Windows RDP Encryption Level High (`rules/windows/access_control/windows-rdp-encryption-level-high.json`)
- Windows RDP Uses TLS Security Layer (`rules/windows/access_control/windows-rdp-uses-tls-security-layer.json`)
- Windows Audit Logon Events (Success and Failure) (`rules/windows/audit/windows-audit-logon-events-success-and-failure.json`)
- Windows Audit Credential Validation (Success and Failure) (`rules/windows/audit/windows-audit-credential-validation-success-and-failure.json`)
- Windows Audit User Account Management (Success and Failure) (`rules/windows/audit/windows-audit-user-account-management-success-and-failure.json`)
- Windows Audit Process Creation (`rules/windows/audit/windows-audit-process-creation.json`)
- Windows Audit Policy Change Events (`rules/windows/audit/windows-audit-policy-change-events.json`)
- Windows Audit Sensitive Privilege Use (Success and Failure) (`rules/windows/audit/windows-audit-sensitive-privilege-use-success-and-failure.json`)
- Windows LLMNR Disabled (`rules/windows/network_security/windows-llmnr-disabled.json`)
- Windows PowerShell Script Block Logging Enabled (`rules/windows/audit/windows-powershell-script-block-logging-enabled.json`)
- Windows PowerShell Module Logging Enabled (`rules/windows/audit/windows-powershell-module-logging-enabled.json`)
- Windows AutoPlay Disabled for All Drives (`rules/windows/system_hardening/windows-autoplay-disabled-for-all-drives.json`)
- Windows AutoRun Commands Disabled (`rules/windows/system_hardening/windows-autorun-commands-disabled.json`)
- Windows TLS 1.0 Server Protocol Disabled (`rules/windows/network_security/windows-tls-1-0-server-protocol-disabled.json`)
- Windows TLS 1.1 Server Protocol Disabled (`rules/windows/network_security/windows-tls-1-1-server-protocol-disabled.json`)
- Windows Firewall Blocks Inbound by Default (`rules/windows/network_security/windows-firewall-blocks-inbound-by-default.json`)
- Windows Machine Inactivity Lock Within 15 Minutes (`rules/windows/access_control/windows-machine-inactivity-lock-within-15-minutes.json`)
- Windows Defender SmartScreen Enabled (`rules/windows/integrity/windows-defender-smartscreen-enabled.json`)
- Windows Secure Boot Enabled (`rules/windows/system_hardening/windows-secure-boot-enabled.json`)
- Windows UAC Prompts Administrators for Consent (`rules/windows/access_control/windows-uac-prompts-administrators-for-consent.json`)
- Windows Account Lockout Duration At Least 15 Minutes (`rules/windows/authentication/windows-account-lockout-duration-at-least-15-minutes.json`)
- Windows Security Event Log Size At Least 192 MB (`rules/windows/audit/windows-security-event-log-size-at-least-192-mb.json`)
- Windows Insecure SMB Guest Logons Disabled (`rules/windows/network_security/windows-insecure-smb-guest-logons-disabled.json`)
- Windows SChannel RC4 Ciphers Not Enabled (`rules/windows/network_security/windows-schannel-rc4-ciphers-not-enabled.json`)
- Windows SChannel Triple-DES Cipher Disabled (`rules/windows/network_security/windows-schannel-triple-des-cipher-disabled.json`)
- Windows Diffie-Hellman Server Minimum Key Size 2048 Bits (`rules/windows/network_security/windows-diffie-hellman-server-minimum-key-size-2048-bits.json`)
