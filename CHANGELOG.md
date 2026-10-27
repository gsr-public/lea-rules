# Changelog

## v1.2.0 - 2026-10-27

781 rules, distributed as a signed LEA rule pack.

### Added

- `uid` on every rule: a stable identity (UUID) that LEA deployments use to track versions and updates across renames. The schema requires it and the validate workflow rejects duplicate uids.
- `former_names`: earlier names of renamed rules, so deployments that created a rule under an older name (for example from the LEA server's former built-in rule set) are matched to it. Added to the rules that the LEA server previously shipped under other names.
- `builtin` and the categories `metadata` and `inventory`: the LEA platform rules Host Name, MAC Address (feed host metadata used by dynamic groups) and Package Inventory Snapshot are now part of the library (`rules/multi/metadata/`, `rules/multi/inventory/`) and are created and activated when the pack is imported.
- Category `application_security` with four PHP2Shell demo-runtime rules (CVE-2026-109618/109619): patched PHP runtime, fatal error backtraces disabled, session upload progress disabled, memory limit with cgroup cap.
- Optional `severity` field.
- `tools/build_pack.py`: builds `lea-rules-<version>.tgz` with `manifest.json`, an ed25519 signature and `latest.json`; `retired.json` lists withdrawn rules.

### Changed

- The library is now the only rule source of the LEA Platform; the server's former `provision/rules` set was merged into it (its rules were already exported here with fixes, under the names listed in `former_names`).
- `vhost-module-not-loaded.json` renamed to match its rule name (`vhost-kernel-module-not-loaded-cve-2026-74580.json`).


## v1.1.0 - 2026-10-14

769 rules: 525 new rules, fixes to existing rules and three additional framework mappings.

### Added

- 525 new rules: 218 Linux, 53 macOS, 239 Windows and 15 multi-platform. Coverage now includes kernel exploit mitigations (kexec, BPF JIT hardening, user namespaces, io_uring, userfaultfd, TTY line disciplines), boot integrity (UEFI Secure Boot, kernel lockdown, module signature enforcement, boot loader password, CPU vulnerability mitigations), the full set of CIS audit rules (session and login records, DAC changes, failed access, deletions, mounts, MAC policy, network environment, privileged commands, commands run as another user), auditd failure handling, account database consistency (duplicate UIDs, GIDs and names, orphaned primary groups, GID 0), PAM and pwquality hardening, sudo hardening, exposed network listeners (Docker API, kubelet, Redis, MongoDB, Elasticsearch, databases, VNC, X11, SNMP, TFTP, LLMNR), mount options for /home, /var, /var/log and /var/log/audit, Docker daemon and kubelet configuration, Windows security options, user rights assignments, 28 additional advanced audit subcategories, Microsoft Defender configuration and 18 attack surface reduction rules, virtualization-based security and Credential Guard, LAPS, RDP, WinRM, SMB, LDAP and Netlogon hardening, PrintNightmare mitigations, unnecessary Windows services, macOS effective MDM preferences (read through NSUserDefaults), macOS sharing services, Secure Boot, MDM enrollment, BSM audit and account policies, additional SSH server settings, cryptocurrency miners and unapproved remote access tools.
- Every new rule was tested before release against passing and failing sample outputs for each operating system it targets, using a re-implementation of the LEA server expect logic (re, not_re, distribution precedence).

### Framework mappings

- New informative tag prefixes: `std:HIPAA:` (HIPAA Security Rule implementation specifications), `std:NIST_CSF_2:` (NIST CSF 2.0 subcategories) and `std:ASD_E8:` (ASD Essential Eight strategies). HIPAA and CSF 2.0 tags are derived for every rule, including the existing ones, from its NIST SP 800-53 controls with a fixed crosswalk; Essential Eight tags are assigned only where a rule directly supports a strategy.
- Some audit rules carry the specific PCI DSS 4.0 sub-requirement they evidence (10.2.1.2 administrative actions, 10.2.1.4 invalid access attempts, 10.2.1.5 credential changes, 10.2.1.6 audit log start/stop, 10.2.1.7 system-level objects).

### Fixed in existing rules

- `priv:required` tag removed (validation reads world-readable kernel parameters): Kernel Pointer Exposure Restricted, Kernel Protected FIFOs Enforced, Kernel Protected Hardlinks Enabled, Kernel Protected Regular Files Enforced, Kernel Protected Symlinks Enabled, Linux Bogus ICMP Error Responses Ignored, Linux ICMP Broadcast Echo Ignored, Linux IPv4 Forwarding Disabled, Linux IPv4 Send Redirects Disabled (All Interfaces), Linux IPv4 Send Redirects Disabled (Default), Linux IPv6 Router Advertisements Not Accepted (All Interfaces), Linux IPv6 Router Advertisements Not Accepted (Default), Linux Log Martian Packets All Interfaces, Linux Log Martian Packets Default Interfaces, Linux Reverse Path Filter All Interfaces, Linux Reverse Path Filter Default Interfaces, Linux Swappiness Within Controlled Range, Linux TCP FIN Timeout Bounded (15-60 Seconds), Linux TCP Keepalive Time Bounded (300-900 Seconds), Linux TCP Retransmission Limit Bounded (5-15), Linux TCP SYN Backlog At Least 2000, Linux TCP SYN Cookies Enabled, Linux TIME-WAIT Assassination Protection (RFC 1337), Low Memory Mapping Restricted (mmap_min_addr), Ptrace Scope Restricted (Yama), Unprivileged eBPF Disabled, macOS ICMP Broadcast Echo Disabled, macOS ICMP Redirects Not Sent, macOS IPv4 Forwarding Disabled, macOS IPv4 Source Routing Disabled, macOS IPv6 Forwarding Disabled, macOS IPv6 ICMP Redirects Not Accepted, macOS TCP Blackhole Protection Enabled, macOS UDP Blackhole Protection Enabled.
- Privilege note marked remedy-only: Linux Bogus ICMP Error Responses Ignored, Linux ICMP Broadcast Echo Ignored, Linux IPv4 Send Redirects Disabled (All Interfaces), Linux IPv4 Send Redirects Disabled (Default), Linux Log Martian Packets All Interfaces, Linux Log Martian Packets Default Interfaces, Linux TCP FIN Timeout Bounded (15-60 Seconds), Linux TCP Keepalive Time Bounded (300-900 Seconds), Linux TCP Retransmission Limit Bounded (5-15), Linux TCP SYN Backlog At Least 2000, Linux TCP SYN Cookies Enabled, Linux TIME-WAIT Assassination Protection (RFC 1337), macOS ICMP Broadcast Echo Disabled, macOS ICMP Redirects Not Sent, macOS IPv4 Source Routing Disabled, macOS IPv6 ICMP Redirects Not Accepted, macOS TCP Blackhole Protection Enabled, macOS UDP Blackhole Protection Enabled.
- Registry value anchored with word boundary: .NET Framework Strong Cryptography Enabled (32-bit), .NET Framework Strong Cryptography Enabled (64-bit), Windows FIPS-Compliant Algorithms Enforced, Windows ICMP Redirects Not Accepted, Windows IPv4 Source Routing Disabled, Windows PMTU Black Hole Detection Disabled, Windows PMTU Discovery Enabled, Windows RDP Network Level Authentication Required, Windows Remote Desktop Disabled, Windows SMBv1 Server Disabled, Windows TCP SYN Attack Protection Enabled, Windows TCP Timestamping Disabled, Windows User Account Control Enabled.
- Module match anchored to the module-name column of /proc/modules: DCCP Protocol Module Not Loaded, HFS Filesystem Module Not Loaded, HFS+ Filesystem Module Not Loaded, JFFS2 Filesystem Module Not Loaded, SCTP Protocol Module Not Loaded, SquashFS Filesystem Module Not Loaded, UDF Filesystem Module Not Loaded, USB Mass Storage Driver Not Loaded, cramfs Filesystem Module Not Loaded, freevxfs Filesystem Module Not Loaded.
- Removed incorrect privilege note for unprivileged reg query: Windows ICMP Redirects Not Accepted, Windows IPv4 Source Routing Disabled, Windows PMTU Black Hole Detection Disabled, Windows TCP SYN Attack Protection Enabled, Windows TCP Timestamping Disabled.
- Also reads deny= arguments in the PAM stack and rejects weaker values: Account Lockout After 5 or Fewer Failures (faillock).
- Privilege note added: Linux Encrypted Volumes Configured (crypttab).
- Duplicate cat tag removed: SSH Legacy Algorithms Disabled.
- `priv:required` tag removed (reg query needs no elevation): Windows FIPS-Compliant Algorithms Enforced.
- Fixed net accounts label (Length of password history maintained): Windows Password History At Least 4.
- Deactivated (setting ignored by supported Windows versions): Windows TCP SYN Attack Protection Enabled.
- Accepts current pwpolicy output format: macOS Password Minimum Length At Least 12.

### New rules

#### linux/access_control

- /etc/issue Does Not Disclose Operating System Details (`rules/linux/access_control/etc-issue-does-not-disclose-operating-system-details.json`)
- /etc/issue.net Does Not Disclose Operating System Details (`rules/linux/access_control/etc-issue-net-does-not-disclose-operating-system-details.json`)
- /etc/motd Does Not Disclose Operating System Details (`rules/linux/access_control/etc-motd-does-not-disclose-operating-system-details.json`)
- Cron and at Access Restricted to Allow Lists (`rules/linux/access_control/cron-and-at-access-restricted-to-allow-lists.json`)
- GDM Last User List Disabled (`rules/linux/access_control/gdm-last-user-list-disabled.json`)
- GDM Login Banner Enabled (`rules/linux/access_control/gdm-login-banner-enabled.json`)
- GNOME Screen Lock After 15 Minutes Idle (`rules/linux/access_control/gnome-screen-lock-after-15-minutes-idle.json`)
- Home Directories Permissions 750 or Stricter (`rules/linux/access_control/home-directories-permissions-750-or-stricter.json`)
- Local Login Warning Banner Configured (`rules/linux/access_control/local-login-warning-banner-configured.json`)
- Login Banner Files Permissions 644 or Stricter (`rules/linux/access_control/login-banner-files-permissions-644-or-stricter.json`)
- Root Home Directory Permissions 700 or Stricter (`rules/linux/access_control/root-home-directory-permissions-700-or-stricter.json`)
- Shell Idle Timeout (TMOUT) 15 Minutes or Less (`rules/linux/access_control/shell-idle-timeout-tmout-15-minutes-or-less.json`)
- SSH Private Host Keys Permissions Restricted (`rules/linux/access_control/ssh-private-host-keys-permissions-restricted.json`)
- SSH Public Host Keys Permissions 644 or Stricter (`rules/linux/access_control/ssh-public-host-keys-permissions-644-or-stricter.json`)
- Sudo Authentication Timeout 15 Minutes or Less (`rules/linux/access_control/sudo-authentication-timeout-15-minutes-or-less.json`)
- Sudo Does Not Grant Unrestricted Shells to Everyone (`rules/linux/access_control/sudo-does-not-grant-unrestricted-shells-to-everyone.json`)
- Sudo Re-authentication Not Disabled (`rules/linux/access_control/sudo-re-authentication-not-disabled.json`)
- Sudo Requires Password for Privilege Escalation (No NOPASSWD) (`rules/linux/access_control/sudo-requires-password-for-privilege-escalation-no-nopasswd.json`)
- User Dot Files Not Group or World Writable (`rules/linux/access_control/user-dot-files-not-group-or-world-writable.json`)

#### linux/audit

- Audit Backlog Limit At Least 8192 (`rules/linux/audit/audit-backlog-limit-at-least-8192.json`)
- Audit Daemon Acts When Admin Disk Space Is Exhausted (`rules/linux/audit/audit-daemon-acts-when-admin-disk-space-is-exhausted.json`)
- Audit Daemon Halts or Goes Single-User When Disk Is Full (`rules/linux/audit/audit-daemon-halts-or-goes-single-user-when-disk-is-full.json`)
- Audit Daemon Warns When Disk Space Is Low (`rules/linux/audit/audit-daemon-warns-when-disk-space-is-low.json`)
- Audit Log Files Permissions 640 or Stricter (`rules/linux/audit/audit-log-files-permissions-640-or-stricter.json`)
- Audit Records Forwarded to a Remote Server (audisp-remote) (`rules/linux/audit/audit-records-forwarded-to-a-remote-server-audisp-remote.json`)
- Audit Rules Track chage Execution (`rules/linux/audit/audit-rules-track-chage-execution.json`)
- Audit Rules Track chcon Execution (`rules/linux/audit/audit-rules-track-chcon-execution.json`)
- Audit Rules Track chsh Execution (`rules/linux/audit/audit-rules-track-chsh-execution.json`)
- Audit Rules Track Commands Run as Another User (`rules/linux/audit/audit-rules-track-commands-run-as-another-user.json`)
- Audit Rules Track crontab Execution (`rules/linux/audit/audit-rules-track-crontab-execution.json`)
- Audit Rules Track File Deletion and Renaming (`rules/linux/audit/audit-rules-track-file-deletion-and-renaming.json`)
- Audit Rules Track Filesystem Mounts (`rules/linux/audit/audit-rules-track-filesystem-mounts.json`)
- Audit Rules Track gpasswd Execution (`rules/linux/audit/audit-rules-track-gpasswd-execution.json`)
- Audit Rules Track Kernel Module Removal (`rules/linux/audit/audit-rules-track-kernel-module-removal.json`)
- Audit Rules Track Network Environment Changes (`rules/linux/audit/audit-rules-track-network-environment-changes.json`)
- Audit Rules Track newgrp Execution (`rules/linux/audit/audit-rules-track-newgrp-execution.json`)
- Audit Rules Track passwd Execution (`rules/linux/audit/audit-rules-track-passwd-execution.json`)
- Audit Rules Track Permission and Ownership Changes (`rules/linux/audit/audit-rules-track-permission-and-ownership-changes.json`)
- Audit Rules Track setfacl Execution (`rules/linux/audit/audit-rules-track-setfacl-execution.json`)
- Audit Rules Track su Execution (`rules/linux/audit/audit-rules-track-su-execution.json`)
- Audit Rules Track sudo Execution (`rules/linux/audit/audit-rules-track-sudo-execution.json`)
- Audit Rules Track Unsuccessful File Access Attempts (`rules/linux/audit/audit-rules-track-unsuccessful-file-access-attempts.json`)
- Audit Rules Track Use of Kernel Module Tools (`rules/linux/audit/audit-rules-track-use-of-kernel-module-tools.json`)
- Audit Rules Track usermod Execution (`rules/linux/audit/audit-rules-track-usermod-execution.json`)
- Audit Rules Watch Docker Daemon and Configuration (`rules/linux/audit/audit-rules-watch-docker-daemon-and-configuration.json`)
- Audit Rules Watch Login and Logout Records (`rules/linux/audit/audit-rules-watch-login-and-logout-records.json`)
- Audit Rules Watch Login Configuration (`rules/linux/audit/audit-rules-watch-login-configuration.json`)
- Audit Rules Watch Mandatory Access Control Policy (`rules/linux/audit/audit-rules-watch-mandatory-access-control-policy.json`)
- Audit Rules Watch Name Service Switch Configuration (`rules/linux/audit/audit-rules-watch-name-service-switch-configuration.json`)
- Audit Rules Watch PAM Configuration (`rules/linux/audit/audit-rules-watch-pam-configuration.json`)
- Audit Rules Watch Scheduled Task Configuration (`rules/linux/audit/audit-rules-watch-scheduled-task-configuration.json`)
- Audit Rules Watch Session Initiation (`rules/linux/audit/audit-rules-watch-session-initiation.json`)
- Audit Rules Watch SSH Server Configuration (`rules/linux/audit/audit-rules-watch-ssh-server-configuration.json`)
- Audit Rules Watch Sudo Log File (`rules/linux/audit/audit-rules-watch-sudo-log-file.json`)
- Audit Tools Protected from Modification (`rules/linux/audit/audit-tools-protected-from-modification.json`)
- Journald Log Compression Not Disabled (`rules/linux/audit/journald-log-compression-not-disabled.json`)
- Journald Not Limited to Tiny Log Retention (`rules/linux/audit/journald-not-limited-to-tiny-log-retention.json`)
- Log Files Not Accessible by Other Users (`rules/linux/audit/log-files-not-accessible-by-other-users.json`)
- rsyslog Log File Creation Mode 0640 or Stricter (`rules/linux/audit/rsyslog-log-file-creation-mode-0640-or-stricter.json`)
- rsyslog Not Accepting Remote Log Messages (`rules/linux/audit/rsyslog-not-accepting-remote-log-messages.json`)

#### linux/authentication

- Account Lockout Applies to Root (faillock) (`rules/linux/authentication/account-lockout-applies-to-root-faillock.json`)
- No .rhosts, .shosts, .netrc or .forward Files in Home Directories (`rules/linux/authentication/no-rhosts-shosts-netrc-or-forward-files-in-home-directories.json`)
- PAM Does Not Allow Empty Passwords (nullok) (`rules/linux/authentication/pam-does-not-allow-empty-passwords-nullok.json`)

#### linux/container_security

- Docker daemon.json Permissions 644 or Stricter (`rules/linux/container_security/docker-daemon-json-permissions-644-or-stricter.json`)
- Docker Insecure Registries Not Configured (`rules/linux/container_security/docker-insecure-registries-not-configured.json`)
- Docker Inter-Container Communication Restricted (`rules/linux/container_security/docker-inter-container-communication-restricted.json`)
- Docker Live Restore Enabled (`rules/linux/container_security/docker-live-restore-enabled.json`)
- Docker no-new-privileges Enabled by Default (`rules/linux/container_security/docker-no-new-privileges-enabled-by-default.json`)
- Docker Socket Permissions 660 or Stricter (`rules/linux/container_security/docker-socket-permissions-660-or-stricter.json`)
- Docker User Namespace Remapping Enabled (`rules/linux/container_security/docker-user-namespace-remapping-enabled.json`)
- Docker Userland Proxy Disabled (`rules/linux/container_security/docker-userland-proxy-disabled.json`)
- Kubelet Anonymous Authentication Disabled (`rules/linux/container_security/kubelet-anonymous-authentication-disabled.json`)
- Kubelet Authorization Mode Not AlwaysAllow (`rules/linux/container_security/kubelet-authorization-mode-not-alwaysallow.json`)
- Kubelet Client Certificate Rotation Not Disabled (`rules/linux/container_security/kubelet-client-certificate-rotation-not-disabled.json`)
- Kubelet Configuration Files Permissions 600 or Stricter (`rules/linux/container_security/kubelet-configuration-files-permissions-600-or-stricter.json`)
- Kubelet Protects Kernel Defaults (`rules/linux/container_security/kubelet-protects-kernel-defaults.json`)

#### linux/identity_management

- All Primary Groups in /etc/passwd Exist (`rules/linux/identity_management/all-primary-groups-in-etc-passwd-exist.json`)
- No Duplicate GIDs (`rules/linux/identity_management/no-duplicate-gids.json`)
- No Duplicate Group Names (`rules/linux/identity_management/no-duplicate-group-names.json`)
- No Duplicate UIDs (`rules/linux/identity_management/no-duplicate-uids.json`)
- No Duplicate User Names (`rules/linux/identity_management/no-duplicate-user-names.json`)
- nologin Not Listed as a Valid Shell (`rules/linux/identity_management/nologin-not-listed-as-a-valid-shell.json`)
- Password Inactivity Lock Applied to Existing Accounts (45 Days or Less) (`rules/linux/identity_management/password-inactivity-lock-applied-to-existing-accounts-45-days-or-less.json`)
- Root Is the Only GID 0 Account (`rules/linux/identity_management/root-is-the-only-gid-0-account.json`)
- Root Is the Only GID 0 Group (`rules/linux/identity_management/root-is-the-only-gid-0-group.json`)
- Shadow Group Has No Members (`rules/linux/identity_management/shadow-group-has-no-members.json`)
- System Accounts Have Locked Passwords (`rules/linux/identity_management/system-accounts-have-locked-passwords.json`)

#### linux/integrity

- Anti-Malware or EDR Agent Running (Linux) (`rules/linux/integrity/anti-malware-or-edr-agent-running-linux.json`)
- File Access Policy Daemon (fapolicyd) Running (`rules/linux/integrity/file-access-policy-daemon-fapolicyd-running.json`)
- File Integrity Baseline Initialized (AIDE) (`rules/linux/integrity/file-integrity-baseline-initialized-aide.json`)
- File Integrity Checks Scheduled (AIDE) (`rules/linux/integrity/file-integrity-checks-scheduled-aide.json`)
- Local Package Signature Verification Enforced (localpkg_gpgcheck) (`rules/linux/integrity/local-package-signature-verification-enforced-localpkg-gpgcheck.json`)

#### linux/kernel_security

- AFS Filesystem Module Not Loaded (`rules/linux/kernel_security/afs-filesystem-module-not-loaded.json`)
- AppArmor Has No Profiles in Complain Mode (`rules/linux/kernel_security/apparmor-has-no-profiles-in-complain-mode.json`)
- Boot Loader Configuration Permissions Restricted (`rules/linux/kernel_security/boot-loader-configuration-permissions-restricted.json`)
- Boot Loader Password Configured (`rules/linux/kernel_security/boot-loader-password-configured.json`)
- BPF JIT Compiler Hardened (`rules/linux/kernel_security/bpf-jit-compiler-hardened.json`)
- Ceph Filesystem Module Not Loaded (`rules/linux/kernel_security/ceph-filesystem-module-not-loaded.json`)
- CIFS Filesystem Module Not Loaded (`rules/linux/kernel_security/cifs-filesystem-module-not-loaded.json`)
- CPU Hardware Vulnerabilities Mitigated (`rules/linux/kernel_security/cpu-hardware-vulnerabilities-mitigated.json`)
- exFAT Filesystem Module Not Loaded (`rules/linux/kernel_security/exfat-filesystem-module-not-loaded.json`)
- FireWire Driver Not Loaded (`rules/linux/kernel_security/firewire-driver-not-loaded.json`)
- GFS2 Filesystem Module Not Loaded (`rules/linux/kernel_security/gfs2-filesystem-module-not-loaded.json`)
- io_uring Restricted for Unprivileged Users (`rules/linux/kernel_security/io-uring-restricted-for-unprivileged-users.json`)
- Kernel CPU Vulnerability Mitigations Not Disabled at Boot (`rules/linux/kernel_security/kernel-cpu-vulnerability-mitigations-not-disabled-at-boot.json`)
- Kernel kexec Loading Disabled (`rules/linux/kernel_security/kernel-kexec-loading-disabled.json`)
- Kernel Lockdown Mode Enabled (`rules/linux/kernel_security/kernel-lockdown-mode-enabled.json`)
- Kernel Module Signature Enforcement Active (`rules/linux/kernel_security/kernel-module-signature-enforcement-active.json`)
- Linux UEFI Secure Boot Enabled (`rules/linux/kernel_security/linux-uefi-secure-boot-enabled.json`)
- Magic SysRq Key Disabled (`rules/linux/kernel_security/magic-sysrq-key-disabled.json`)
- Mandatory Access Control Not Disabled at Boot (`rules/linux/kernel_security/mandatory-access-control-not-disabled-at-boot.json`)
- No Unconfined Services (SELinux) (`rules/linux/kernel_security/no-unconfined-services-selinux.json`)
- SELinux Policy Type Targeted or MLS (`rules/linux/kernel_security/selinux-policy-type-targeted-or-mls.json`)
- Thunderbolt Driver Not Loaded on Servers (`rules/linux/kernel_security/thunderbolt-driver-not-loaded-on-servers.json`)
- TTY Line Discipline Autoloading Disabled (`rules/linux/kernel_security/tty-line-discipline-autoloading-disabled.json`)
- Unprivileged User Namespaces Restricted (`rules/linux/kernel_security/unprivileged-user-namespaces-restricted.json`)
- Unprivileged userfaultfd Disabled (`rules/linux/kernel_security/unprivileged-userfaultfd-disabled.json`)
- USBGuard Daemon Running (`rules/linux/kernel_security/usbguard-daemon-running.json`)

#### linux/network_security

- ATM Protocol Module Not Loaded (`rules/linux/network_security/atm-protocol-module-not-loaded.json`)
- Bluetooth Service Not Running (`rules/linux/network_security/bluetooth-service-not-running.json`)
- Bluetooth Stack Not Loaded (`rules/linux/network_security/bluetooth-stack-not-loaded.json`)
- BSD r-Services Ports Not Listening (`rules/linux/network_security/bsd-r-services-ports-not-listening.json`)
- CAN Bus Protocol Module Not Loaded (`rules/linux/network_security/can-bus-protocol-module-not-loaded.json`)
- DHCP Server Not Running (`rules/linux/network_security/dhcp-server-not-running.json`)
- DNS Server (BIND) Not Running (`rules/linux/network_security/dns-server-bind-not-running.json`)
- Docker Engine Unencrypted TCP API Not Listening (`rules/linux/network_security/docker-engine-unencrypted-tcp-api-not-listening.json`)
- Elasticsearch Not Listening on Network Interfaces (`rules/linux/network_security/elasticsearch-not-listening-on-network-interfaces.json`)
- etcd Not Listening on Network Interfaces Outside Kubernetes Control Plane (`rules/linux/network_security/etcd-not-listening-on-network-interfaces-outside-kubernetes-control-plane.json`)
- firewalld Default Zone Not trusted (`rules/linux/network_security/firewalld-default-zone-not-trusted.json`)
- FTP Control Port Not Listening (`rules/linux/network_security/ftp-control-port-not-listening.json`)
- HTTP Proxy Server Not Running (`rules/linux/network_security/http-proxy-server-not-running.json`)
- IMAP and POP3 Servers Not Running (`rules/linux/network_security/imap-and-pop3-servers-not-running.json`)
- Kubelet Read-Only Port Not Listening (`rules/linux/network_security/kubelet-read-only-port-not-listening.json`)
- LDAP Server Not Running (`rules/linux/network_security/ldap-server-not-running.json`)
- Linux IPv6 Firewall Default Deny Policy (ip6tables) (`rules/linux/network_security/linux-ipv6-firewall-default-deny-policy-ip6tables.json`)
- Linux IPv6 Router Advertisement Default Route Not Accepted (`rules/linux/network_security/linux-ipv6-router-advertisement-default-route-not-accepted.json`)
- Linux TCP SYN-ACK Retries 5 or Fewer (`rules/linux/network_security/linux-tcp-syn-ack-retries-5-or-fewer.json`)
- LLMNR Not Listening (`rules/linux/network_security/llmnr-not-listening.json`)
- mDNS Responder Not Listening on Servers (`rules/linux/network_security/mdns-responder-not-listening-on-servers.json`)
- Memcached Not Listening on Network Interfaces (TCP) (`rules/linux/network_security/memcached-not-listening-on-network-interfaces-tcp.json`)
- Memcached Not Listening on UDP (`rules/linux/network_security/memcached-not-listening-on-udp.json`)
- MongoDB Not Listening on Network Interfaces (`rules/linux/network_security/mongodb-not-listening-on-network-interfaces.json`)
- MySQL or MariaDB Not Listening on Network Interfaces (`rules/linux/network_security/mysql-or-mariadb-not-listening-on-network-interfaces.json`)
- NFS Not Listening on Hosts That Are Not NFS Servers (`rules/linux/network_security/nfs-not-listening-on-hosts-that-are-not-nfs-servers.json`)
- NFS Server Kernel Module Not Loaded (`rules/linux/network_security/nfs-server-kernel-module-not-loaded.json`)
- NFS Server Not Running (`rules/linux/network_security/nfs-server-not-running.json`)
- nftables Input Chain Default Policy Drop (`rules/linux/network_security/nftables-input-chain-default-policy-drop.json`)
- No Active Wireless Interfaces on Servers (`rules/linux/network_security/no-active-wireless-interfaces-on-servers.json`)
- PostgreSQL Not Listening on Network Interfaces (`rules/linux/network_security/postgresql-not-listening-on-network-interfaces.json`)
- RDS Protocol Module Not Loaded (`rules/linux/network_security/rds-protocol-module-not-loaded.json`)
- Redis Not Listening on Network Interfaces (`rules/linux/network_security/redis-not-listening-on-network-interfaces.json`)
- RPC Portmapper Not Listening (`rules/linux/network_security/rpc-portmapper-not-listening.json`)
- rsync Daemon Not Listening (`rules/linux/network_security/rsync-daemon-not-listening.json`)
- Samba File Server Not Running (`rules/linux/network_security/samba-file-server-not-running.json`)
- SMB Not Listening on Linux Hosts That Are Not File Servers (`rules/linux/network_security/smb-not-listening-on-linux-hosts-that-are-not-file-servers.json`)
- SNMP Not Listening on UDP (`rules/linux/network_security/snmp-not-listening-on-udp.json`)
- systemd-resolved LLMNR and mDNS Disabled (`rules/linux/network_security/systemd-resolved-llmnr-and-mdns-disabled.json`)
- talk Server Not Running (`rules/linux/network_security/talk-server-not-running.json`)
- Telnet Server Process Not Running (`rules/linux/network_security/telnet-server-process-not-running.json`)
- TFTP Not Listening on UDP (`rules/linux/network_security/tftp-not-listening-on-udp.json`)
- TIPC Protocol Module Not Loaded (`rules/linux/network_security/tipc-protocol-module-not-loaded.json`)
- UFW Default Forward Policy Deny (`rules/linux/network_security/ufw-default-forward-policy-deny.json`)
- UFW Default Incoming Policy Deny (`rules/linux/network_security/ufw-default-incoming-policy-deny.json`)
- VNC Server Not Listening on Network Interfaces (`rules/linux/network_security/vnc-server-not-listening-on-network-interfaces.json`)
- Web Server Not Running (`rules/linux/network_security/web-server-not-running.json`)
- X Window Server Not Running on Servers (`rules/linux/network_security/x-window-server-not-running-on-servers.json`)
- X11 Server Not Listening on TCP (`rules/linux/network_security/x11-server-not-listening-on-tcp.json`)

#### linux/password_policy

- Last Password Change Dates Not in the Future (`rules/linux/password_policy/last-password-change-dates-not-in-the-future.json`)
- PAM Password Quality Module Enabled (pam_pwquality) (`rules/linux/password_policy/pam-password-quality-module-enabled-pam-pwquality.json`)
- PAM Uses Strong Password Hashing (pam_unix sha512 or yescrypt) (`rules/linux/password_policy/pam-uses-strong-password-hashing-pam-unix-sha512-or-yescrypt.json`)
- Password Changes Require at Least 2 Different Characters (difok) (`rules/linux/password_policy/password-changes-require-at-least-2-different-characters-difok.json`)
- Password Dictionary Check Not Disabled (pwquality) (`rules/linux/password_policy/password-dictionary-check-not-disabled-pwquality.json`)
- Password Expiration Applied to Existing Accounts (365 Days or Less) (`rules/linux/password_policy/password-expiration-applied-to-existing-accounts-365-days-or-less.json`)
- Password History Enforced for Root (pwhistory) (`rules/linux/password_policy/password-history-enforced-for-root-pwhistory.json`)
- Password Minimum Age Applied to Existing Accounts (`rules/linux/password_policy/password-minimum-age-applied-to-existing-accounts.json`)
- Password Quality Enforced for Root (pwquality) (`rules/linux/password_policy/password-quality-enforced-for-root-pwquality.json`)
- Password Repeated Characters Limited (maxrepeat 1-3) (`rules/linux/password_policy/password-repeated-characters-limited-maxrepeat-1-3.json`)
- Password Sequential Characters Limited (maxsequence 1-3) (`rules/linux/password_policy/password-sequential-characters-limited-maxsequence-1-3.json`)

#### linux/system_hardening

- /etc/shells Permissions 644 or Stricter (`rules/linux/system_hardening/etc-shells-permissions-644-or-stricter.json`)
- /home Is a Separate Mount (`rules/linux/system_hardening/home-is-a-separate-mount.json`)
- /home Mount Options Hardened (nodev, nosuid) (`rules/linux/system_hardening/home-mount-options-hardened-nodev-nosuid.json`)
- /var Is a Separate Mount (`rules/linux/system_hardening/var-is-a-separate-mount.json`)
- /var Mount Options Hardened (nodev, nosuid) (`rules/linux/system_hardening/var-mount-options-hardened-nodev-nosuid.json`)
- /var/log Is a Separate Mount (`rules/linux/system_hardening/var-log-is-a-separate-mount.json`)
- /var/log Mount Options Hardened (nodev, nosuid, noexec) (`rules/linux/system_hardening/var-log-mount-options-hardened-nodev-nosuid-noexec.json`)
- /var/log/audit Is a Separate Mount (`rules/linux/system_hardening/var-log-audit-is-a-separate-mount.json`)
- /var/log/audit Mount Options Hardened (nodev, nosuid, noexec) (`rules/linux/system_hardening/var-log-audit-mount-options-hardened-nodev-nosuid-noexec.json`)
- /var/tmp Is a Separate Mount (`rules/linux/system_hardening/var-tmp-is-a-separate-mount.json`)
- APT Package Lists Refreshed Automatically (`rules/linux/system_hardening/apt-package-lists-refreshed-automatically.json`)
- Automounter (autofs) Not Running (`rules/linux/system_hardening/automounter-autofs-not-running.json`)
- Backup passwd and group Files Permissions 644 or Stricter (`rules/linux/system_hardening/backup-passwd-and-group-files-permissions-644-or-stricter.json`)
- Backup shadow and gshadow Files Permissions Restricted (`rules/linux/system_hardening/backup-shadow-and-gshadow-files-permissions-restricted.json`)
- Cron Directories Permissions Restricted (`rules/linux/system_hardening/cron-directories-permissions-restricted.json`)
- Ctrl-Alt-Delete Reboot Disabled (`rules/linux/system_hardening/ctrl-alt-delete-reboot-disabled.json`)
- cups-browsed Not Running (`rules/linux/system_hardening/cups-browsed-not-running.json`)
- Default Shell umask 027 or Stricter (`rules/linux/system_hardening/default-shell-umask-027-or-stricter.json`)
- dnf-automatic Timer Enabled (`rules/linux/system_hardening/dnf-automatic-timer-enabled.json`)
- dnsmasq Not Running (`rules/linux/system_hardening/dnsmasq-not-running.json`)
- FTP Client Not Installed (`rules/linux/system_hardening/ftp-client-not-installed.json`)
- GDM XDMCP Disabled (`rules/linux/system_hardening/gdm-xdmcp-disabled.json`)
- GNOME Automount of Removable Media Disabled (`rules/linux/system_hardening/gnome-automount-of-removable-media-disabled.json`)
- LDAP Client Tools Not Installed (`rules/linux/system_hardening/ldap-client-tools-not-installed.json`)
- NIS Client Not Installed (`rules/linux/system_hardening/nis-client-not-installed.json`)
- No Pending Reboot After Package Updates (`rules/linux/system_hardening/no-pending-reboot-after-package-updates.json`)
- No Ungrouped Files on Local Filesystems (`rules/linux/system_hardening/no-ungrouped-files-on-local-filesystems.json`)
- Password History File (opasswd) Permissions Restricted (`rules/linux/system_hardening/password-history-file-opasswd-permissions-restricted.json`)
- prelink Not Installed (`rules/linux/system_hardening/prelink-not-installed.json`)
- Process Information Hidden from Other Users (hidepid) (`rules/linux/system_hardening/process-information-hidden-from-other-users-hidepid.json`)
- Removable Media Mounted with noexec, nosuid and nodev (`rules/linux/system_hardening/removable-media-mounted-with-noexec-nosuid-and-nodev.json`)
- rpcbind Not Running (`rules/linux/system_hardening/rpcbind-not-running.json`)
- rsh Client Not Installed (`rules/linux/system_hardening/rsh-client-not-installed.json`)
- Running Kernel Is the Newest Installed Kernel (`rules/linux/system_hardening/running-kernel-is-the-newest-installed-kernel.json`)
- SELinux Troubleshooting Daemons Not Installed (`rules/linux/system_hardening/selinux-troubleshooting-daemons-not-installed.json`)
- talk Client Not Installed (`rules/linux/system_hardening/talk-client-not-installed.json`)
- Telnet Client Not Installed (`rules/linux/system_hardening/telnet-client-not-installed.json`)
- TFTP Client Not Installed (`rules/linux/system_hardening/tftp-client-not-installed.json`)
- Time Synchronization Source Configured (`rules/linux/system_hardening/time-synchronization-source-configured.json`)
- World-Writable Directories Have the Sticky Bit (`rules/linux/system_hardening/world-writable-directories-have-the-sticky-bit.json`)

#### macos/access_control

- macOS Home Folders Not Accessible by Other Users (`rules/macos/access_control/macos-home-folders-not-accessible-by-other-users.json`)
- macOS Login Window Banner Configured (`rules/macos/access_control/macos-login-window-banner-configured.json`)
- macOS Remote Management (ARD) Not Running (`rules/macos/access_control/macos-remote-management-ard-not-running.json`)
- macOS Screen Lock Requires Password Immediately (Effective Policy) (`rules/macos/access_control/macos-screen-lock-requires-password-immediately-effective-policy.json`)
- macOS Screen Saver Starts Within 20 Minutes (`rules/macos/access_control/macos-screen-saver-starts-within-20-minutes.json`)
- macOS SMB Guest Access Disabled (`rules/macos/access_control/macos-smb-guest-access-disabled.json`)
- macOS Sudo Timeout Set to Zero (`rules/macos/access_control/macos-sudo-timeout-set-to-zero.json`)
- macOS Sudo Timestamp Separated per Terminal (`rules/macos/access_control/macos-sudo-timestamp-separated-per-terminal.json`)
- macOS System Preferences Require Administrator Authentication (`rules/macos/access_control/macos-system-preferences-require-administrator-authentication.json`)
- macOS System-Wide Applications Not World-Writable (`rules/macos/access_control/macos-system-wide-applications-not-world-writable.json`)

#### macos/audit

- macOS Audit Flags Capture Logins, Administrative and Authorization Events (`rules/macos/audit/macos-audit-flags-capture-logins-administrative-and-authorization-events.json`)
- macOS Audit Records Retained for 60 Days or 5 GB (`rules/macos/audit/macos-audit-records-retained-for-60-days-or-5-gb.json`)
- macOS Install Log Retained for 365 Days (`rules/macos/audit/macos-install-log-retained-for-365-days.json`)
- macOS Security Auditing Enabled (`rules/macos/audit/macos-security-auditing-enabled.json`)

#### macos/authentication

- macOS Account Lockout After 5 or Fewer Failed Logins (`rules/macos/authentication/macos-account-lockout-after-5-or-fewer-failed-logins.json`)
- macOS Account Lockout Duration At Least 15 Minutes (`rules/macos/authentication/macos-account-lockout-duration-at-least-15-minutes.json`)
- macOS iCloud Keychain Sync Disabled (`rules/macos/authentication/macos-icloud-keychain-sync-disabled.json`)
- macOS Login Window Shows Name and Password Fields (`rules/macos/authentication/macos-login-window-shows-name-and-password-fields.json`)
- macOS Password Hints Disabled (`rules/macos/authentication/macos-password-hints-disabled.json`)

#### macos/identity_management

- macOS Guest Account Disabled (Effective Policy) (`rules/macos/identity_management/macos-guest-account-disabled-effective-policy.json`)
- macOS Guest Home Folder Removed (`rules/macos/identity_management/macos-guest-home-folder-removed.json`)
- macOS Root Account Disabled (`rules/macos/identity_management/macos-root-account-disabled.json`)
- macOS Root Is the Only UID 0 Account (`rules/macos/identity_management/macos-root-is-the-only-uid-0-account.json`)

#### macos/integrity

- macOS Authenticated Root Volume Enabled (`rules/macos/integrity/macos-authenticated-root-volume-enabled.json`)
- macOS Gatekeeper Override Disallowed (`rules/macos/integrity/macos-gatekeeper-override-disallowed.json`)
- macOS Library Validation Not Disabled (`rules/macos/integrity/macos-library-validation-not-disabled.json`)
- macOS System Data Files and XProtect Updates Installed Automatically (`rules/macos/integrity/macos-system-data-files-and-xprotect-updates-installed-automatically.json`)

#### macos/kernel_security

- macOS Secure Boot Full Security (`rules/macos/kernel_security/macos-secure-boot-full-security.json`)

#### macos/network_security

- macOS AirDrop Disabled (`rules/macos/network_security/macos-airdrop-disabled.json`)
- macOS Bonjour Advertising Disabled (`rules/macos/network_security/macos-bonjour-advertising-disabled.json`)
- macOS Built-in Web Server Disabled (`rules/macos/network_security/macos-built-in-web-server-disabled.json`)
- macOS Content Caching Disabled (`rules/macos/network_security/macos-content-caching-disabled.json`)
- macOS File Sharing (SMB) Disabled (`rules/macos/network_security/macos-file-sharing-smb-disabled.json`)
- macOS Firewall Blocks All Incoming Connections (Optional Strict Mode) (`rules/macos/network_security/macos-firewall-blocks-all-incoming-connections-optional-strict-mode.json`)
- macOS Internet Sharing Disabled (`rules/macos/network_security/macos-internet-sharing-disabled.json`)
- macOS NFS Server Disabled (`rules/macos/network_security/macos-nfs-server-disabled.json`)
- macOS Printer Sharing Disabled (`rules/macos/network_security/macos-printer-sharing-disabled.json`)
- macOS Screen Sharing Disabled (`rules/macos/network_security/macos-screen-sharing-disabled.json`)
- macOS TFTP Server Disabled (`rules/macos/network_security/macos-tftp-server-disabled.json`)
- macOS UUCP Service Disabled (`rules/macos/network_security/macos-uucp-service-disabled.json`)

#### macos/password_policy

- macOS Password History At Least 15 (`rules/macos/password_policy/macos-password-history-at-least-15.json`)
- macOS Password Maximum Age 365 Days or Less (`rules/macos/password_policy/macos-password-maximum-age-365-days-or-less.json`)
- macOS Password Requires a Special Character (`rules/macos/password_policy/macos-password-requires-a-special-character.json`)
- macOS Password Requires Alphabetic and Numeric Characters (`rules/macos/password_policy/macos-password-requires-alphabetic-and-numeric-characters.json`)

#### macos/system_hardening

- macOS App Store Apps Updated Automatically (`rules/macos/system_hardening/macos-app-store-apps-updated-automatically.json`)
- macOS Diagnostic Data Submission Disabled (`rules/macos/system_hardening/macos-diagnostic-data-submission-disabled.json`)
- macOS Enrolled in MDM (`rules/macos/system_hardening/macos-enrolled-in-mdm.json`)
- macOS iCloud Drive Document Sync Disabled (`rules/macos/system_hardening/macos-icloud-drive-document-sync-disabled.json`)
- macOS Personalized Advertising Disabled (`rules/macos/system_hardening/macos-personalized-advertising-disabled.json`)
- macOS Siri Disabled (`rules/macos/system_hardening/macos-siri-disabled.json`)
- macOS Updates Downloaded Automatically (`rules/macos/system_hardening/macos-updates-downloaded-automatically.json`)
- macOS Updates Installed Automatically (`rules/macos/system_hardening/macos-updates-installed-automatically.json`)
- macOS Wake for Network Access Disabled (`rules/macos/system_hardening/macos-wake-for-network-access-disabled.json`)

#### multi/access_control

- SSH Access Restricted to Allowed Users or Groups (`rules/multi/access_control/ssh-access-restricted-to-allowed-users-or-groups.json`)
- SSH Agent Forwarding Disabled (`rules/multi/access_control/ssh-agent-forwarding-disabled.json`)
- SSH Maximum Sessions per Connection 10 or Fewer (`rules/multi/access_control/ssh-maximum-sessions-per-connection-10-or-fewer.json`)
- SSH Strict Modes Enabled (`rules/multi/access_control/ssh-strict-modes-enabled.json`)
- SSH TCP Forwarding Disabled (`rules/multi/access_control/ssh-tcp-forwarding-disabled.json`)
- SSH Tunnel Device Forwarding Disabled (`rules/multi/access_control/ssh-tunnel-device-forwarding-disabled.json`)
- Unapproved Remote Access and Tunneling Tools Not Running (`rules/multi/access_control/unapproved-remote-access-and-tunneling-tools-not-running.json`)

#### multi/audit

- SSH Log Level INFO or VERBOSE (`rules/multi/audit/ssh-log-level-info-or-verbose.json`)
- Sudo Logs Every Command Input and Output (log_input/log_output) (`rules/multi/audit/sudo-logs-every-command-input-and-output-log-input-log-output.json`)

#### multi/authentication

- SSH GSSAPI Authentication Disabled (`rules/multi/authentication/ssh-gssapi-authentication-disabled.json`)
- SSH Kerberos Password Authentication Disabled (`rules/multi/authentication/ssh-kerberos-password-authentication-disabled.json`)
- SSH User Known Hosts Ignored for Host-Based Authentication (`rules/multi/authentication/ssh-user-known-hosts-ignored-for-host-based-authentication.json`)
- SSH Uses PAM (`rules/multi/authentication/ssh-uses-pam.json`)

#### multi/integrity

- Cryptocurrency Miners Not Running (`rules/multi/integrity/cryptocurrency-miners-not-running.json`)

#### multi/network_security

- SSH MaxStartups Limits Unauthenticated Connections (`rules/multi/network_security/ssh-maxstartups-limits-unauthenticated-connections.json`)

#### windows/access_control

- Windows Anonymous Enumeration of SAM Accounts and Shares Restricted (`rules/windows/access_control/windows-anonymous-enumeration-of-sam-accounts-and-shares-restricted.json`)
- Windows Anonymous SID/Name Translation Disabled (`rules/windows/access_control/windows-anonymous-sid-name-translation-disabled.json`)
- Windows Everyone Permissions Not Applied to Anonymous Users (`rules/windows/access_control/windows-everyone-permissions-not-applied-to-anonymous-users.json`)
- Windows Installer Always Install Elevated Disabled (`rules/windows/access_control/windows-installer-always-install-elevated-disabled.json`)
- Windows Installer User Control Over Installs Disabled (`rules/windows/access_control/windows-installer-user-control-over-installs-disabled.json`)
- Windows Local Accounts Restricted on Network Logons (UAC Remote Restrictions) (`rules/windows/access_control/windows-local-accounts-restricted-on-network-logons-uac-remote-restrictions.json`)
- Windows Logon Legal Notice Caption Configured (`rules/windows/access_control/windows-logon-legal-notice-caption-configured.json`)
- Windows Logon Legal Notice Text Configured (`rules/windows/access_control/windows-logon-legal-notice-text-configured.json`)
- Windows Point and Print Driver Installation Restricted to Administrators (`rules/windows/access_control/windows-point-and-print-driver-installation-restricted-to-administrators.json`)
- Windows Point and Print Requires Elevation Prompts (`rules/windows/access_control/windows-point-and-print-requires-elevation-prompts.json`)
- Windows RDP Always Prompts for Password (`rules/windows/access_control/windows-rdp-always-prompts-for-password.json`)
- Windows RDP Client Password Saving Disabled (`rules/windows/access_control/windows-rdp-client-password-saving-disabled.json`)
- Windows RDP Clipboard Redirection Disabled (`rules/windows/access_control/windows-rdp-clipboard-redirection-disabled.json`)
- Windows RDP Drive Redirection Disabled (`rules/windows/access_control/windows-rdp-drive-redirection-disabled.json`)
- Windows RDP Idle Session Limit 15 Minutes or Less (`rules/windows/access_control/windows-rdp-idle-session-limit-15-minutes-or-less.json`)
- Windows RDP Requires Secure RPC Communication (`rules/windows/access_control/windows-rdp-requires-secure-rpc-communication.json`)
- Windows RDP Temporary Folders Deleted on Exit (`rules/windows/access_control/windows-rdp-temporary-folders-deleted-on-exit.json`)
- Windows Remote Assistance Solicitation Disabled (`rules/windows/access_control/windows-remote-assistance-solicitation-disabled.json`)
- Windows Remote SAM Calls Restricted to Administrators (`rules/windows/access_control/windows-remote-sam-calls-restricted-to-administrators.json`)
- Windows Screen Saver Grace Period 5 Seconds or Less (`rules/windows/access_control/windows-screen-saver-grace-period-5-seconds-or-less.json`)
- Windows Smart Card Removal Locks the Workstation (`rules/windows/access_control/windows-smart-card-removal-locks-the-workstation.json`)
- Windows SMB Server Null Session Shares and Pipes Empty (`rules/windows/access_control/windows-smb-server-null-session-shares-and-pipes-empty.json`)
- Windows SMB Server Restricts Null Session Access (`rules/windows/access_control/windows-smb-server-restricts-null-session-access.json`)
- Windows UAC Admin Approval Mode for Built-in Administrator (`rules/windows/access_control/windows-uac-admin-approval-mode-for-built-in-administrator.json`)
- Windows UAC Automatically Denies Standard User Elevation (`rules/windows/access_control/windows-uac-automatically-denies-standard-user-elevation.json`)
- Windows UAC Detects Application Installations (`rules/windows/access_control/windows-uac-detects-application-installations.json`)
- Windows UAC Elevates Only UIAccess Apps in Secure Locations (`rules/windows/access_control/windows-uac-elevates-only-uiaccess-apps-in-secure-locations.json`)
- Windows UAC File and Registry Virtualization Enabled (`rules/windows/access_control/windows-uac-file-and-registry-virtualization-enabled.json`)
- Windows UAC Prompts on the Secure Desktop (`rules/windows/access_control/windows-uac-prompts-on-the-secure-desktop.json`)
- Windows User Right 'Access Credential Manager as a Trusted Caller' Restricted (`rules/windows/access_control/windows-user-right-access-credential-manager-as-a-trusted-caller-restricted.json`)
- Windows User Right 'Access This Computer from the Network' Excludes Everyone and Guests (`rules/windows/access_control/windows-user-right-access-this-computer-from-the-network-excludes-everyone-and-guests.json`)
- Windows User Right 'Act as Part of the Operating System' Restricted (`rules/windows/access_control/windows-user-right-act-as-part-of-the-operating-system-restricted.json`)
- Windows User Right 'Adjust Memory Quotas for a Process' Restricted (`rules/windows/access_control/windows-user-right-adjust-memory-quotas-for-a-process-restricted.json`)
- Windows User Right 'Allow Log On Through Remote Desktop Services' Restricted (`rules/windows/access_control/windows-user-right-allow-log-on-through-remote-desktop-services-restricted.json`)
- Windows User Right 'Back Up Files and Directories' Restricted (`rules/windows/access_control/windows-user-right-back-up-files-and-directories-restricted.json`)
- Windows User Right 'Create a Pagefile' Restricted (`rules/windows/access_control/windows-user-right-create-a-pagefile-restricted.json`)
- Windows User Right 'Create a Token Object' Restricted (`rules/windows/access_control/windows-user-right-create-a-token-object-restricted.json`)
- Windows User Right 'Create Global Objects' Restricted (`rules/windows/access_control/windows-user-right-create-global-objects-restricted.json`)
- Windows User Right 'Create Permanent Shared Objects' Restricted (`rules/windows/access_control/windows-user-right-create-permanent-shared-objects-restricted.json`)
- Windows User Right 'Create Symbolic Links' Restricted (`rules/windows/access_control/windows-user-right-create-symbolic-links-restricted.json`)
- Windows User Right 'Debug Programs' Restricted (`rules/windows/access_control/windows-user-right-debug-programs-restricted.json`)
- Windows User Right 'Deny Access to This Computer from the Network' Includes Guests (`rules/windows/access_control/windows-user-right-deny-access-to-this-computer-from-the-network-includes-guests.json`)
- Windows User Right 'Deny Log On as a Batch Job' Includes Guests (`rules/windows/access_control/windows-user-right-deny-log-on-as-a-batch-job-includes-guests.json`)
- Windows User Right 'Deny Log On as a Service' Includes Guests (`rules/windows/access_control/windows-user-right-deny-log-on-as-a-service-includes-guests.json`)
- Windows User Right 'Deny Log On Locally' Includes Guests (`rules/windows/access_control/windows-user-right-deny-log-on-locally-includes-guests.json`)
- Windows User Right 'Deny Log On Through Remote Desktop Services' Includes Guests (`rules/windows/access_control/windows-user-right-deny-log-on-through-remote-desktop-services-includes-guests.json`)
- Windows User Right 'Force Shutdown from a Remote System' Restricted (`rules/windows/access_control/windows-user-right-force-shutdown-from-a-remote-system-restricted.json`)
- Windows User Right 'Impersonate a Client After Authentication' Restricted (`rules/windows/access_control/windows-user-right-impersonate-a-client-after-authentication-restricted.json`)
- Windows User Right 'Increase Scheduling Priority' Restricted (`rules/windows/access_control/windows-user-right-increase-scheduling-priority-restricted.json`)
- Windows User Right 'Load and Unload Device Drivers' Restricted (`rules/windows/access_control/windows-user-right-load-and-unload-device-drivers-restricted.json`)
- Windows User Right 'Lock Pages in Memory' Restricted (`rules/windows/access_control/windows-user-right-lock-pages-in-memory-restricted.json`)
- Windows User Right 'Manage Auditing and Security Log' Restricted (`rules/windows/access_control/windows-user-right-manage-auditing-and-security-log-restricted.json`)
- Windows User Right 'Modify Firmware Environment Values' Restricted (`rules/windows/access_control/windows-user-right-modify-firmware-environment-values-restricted.json`)
- Windows User Right 'Perform Volume Maintenance Tasks' Restricted (`rules/windows/access_control/windows-user-right-perform-volume-maintenance-tasks-restricted.json`)
- Windows User Right 'Profile Single Process' Restricted (`rules/windows/access_control/windows-user-right-profile-single-process-restricted.json`)
- Windows User Right 'Replace a Process Level Token' Restricted (`rules/windows/access_control/windows-user-right-replace-a-process-level-token-restricted.json`)
- Windows User Right 'Restore Files and Directories' Restricted (`rules/windows/access_control/windows-user-right-restore-files-and-directories-restricted.json`)
- Windows User Right 'Take Ownership of Files or Other Objects' Restricted (`rules/windows/access_control/windows-user-right-take-ownership-of-files-or-other-objects-restricted.json`)
- Windows Users Cannot Install Printer Drivers (`rules/windows/access_control/windows-users-cannot-install-printer-drivers.json`)

#### windows/audit

- Sysmon Running (`rules/windows/audit/sysmon-running.json`)
- Windows Application Event Log Size At Least 32 MB (`rules/windows/audit/windows-application-event-log-size-at-least-32-mb.json`)
- Windows Audit Account Lockout (Failure) (`rules/windows/audit/windows-audit-account-lockout-failure.json`)
- Windows Audit Application Group Management (Success and Failure) (`rules/windows/audit/windows-audit-application-group-management-success-and-failure.json`)
- Windows Audit Authentication Policy Change (Success) (`rules/windows/audit/windows-audit-authentication-policy-change-success.json`)
- Windows Audit Authorization Policy Change (Success) (`rules/windows/audit/windows-audit-authorization-policy-change-success.json`)
- Windows Audit Computer Account Management (Success) (`rules/windows/audit/windows-audit-computer-account-management-success.json`)
- Windows Audit Detailed File Share (Failure) (`rules/windows/audit/windows-audit-detailed-file-share-failure.json`)
- Windows Audit Directory Service Access (Failure) (`rules/windows/audit/windows-audit-directory-service-access-failure.json`)
- Windows Audit Directory Service Changes (Success) (`rules/windows/audit/windows-audit-directory-service-changes-success.json`)
- Windows Audit File Share (Success and Failure) (`rules/windows/audit/windows-audit-file-share-success-and-failure.json`)
- Windows Audit Group Membership (Success) (`rules/windows/audit/windows-audit-group-membership-success.json`)
- Windows Audit IPsec Driver (Success and Failure) (`rules/windows/audit/windows-audit-ipsec-driver-success-and-failure.json`)
- Windows Audit Kerberos Authentication Service (Success and Failure) (`rules/windows/audit/windows-audit-kerberos-authentication-service-success-and-failure.json`)
- Windows Audit Kerberos Service Ticket Operations (Success and Failure) (`rules/windows/audit/windows-audit-kerberos-service-ticket-operations-success-and-failure.json`)
- Windows Audit Logoff (Success) (`rules/windows/audit/windows-audit-logoff-success.json`)
- Windows Audit MPSSVC Rule-Level Policy Change (Success and Failure) (`rules/windows/audit/windows-audit-mpssvc-rule-level-policy-change-success-and-failure.json`)
- Windows Audit Other Account Management Events (Success) (`rules/windows/audit/windows-audit-other-account-management-events-success.json`)
- Windows Audit Other Logon/Logoff Events (Success and Failure) (`rules/windows/audit/windows-audit-other-logon-logoff-events-success-and-failure.json`)
- Windows Audit Other Object Access Events (Success and Failure) (`rules/windows/audit/windows-audit-other-object-access-events-success-and-failure.json`)
- Windows Audit Other Policy Change Events (Failure) (`rules/windows/audit/windows-audit-other-policy-change-events-failure.json`)
- Windows Audit Other System Events (Success and Failure) (`rules/windows/audit/windows-audit-other-system-events-success-and-failure.json`)
- Windows Audit PNP Activity (Success) (`rules/windows/audit/windows-audit-pnp-activity-success.json`)
- Windows Audit Process Termination (Success) (`rules/windows/audit/windows-audit-process-termination-success.json`)
- Windows Audit Removable Storage (Success and Failure) (`rules/windows/audit/windows-audit-removable-storage-success-and-failure.json`)
- Windows Audit Security Group Management (Success) (`rules/windows/audit/windows-audit-security-group-management-success.json`)
- Windows Audit Security State Change (Success) (`rules/windows/audit/windows-audit-security-state-change-success.json`)
- Windows Audit Security System Extension (Success) (`rules/windows/audit/windows-audit-security-system-extension-success.json`)
- Windows Audit Special Logon (Success) (`rules/windows/audit/windows-audit-special-logon-success.json`)
- Windows Audit Subcategory Settings Override Category Settings (`rules/windows/audit/windows-audit-subcategory-settings-override-category-settings.json`)
- Windows Audit System Integrity (Success and Failure) (`rules/windows/audit/windows-audit-system-integrity-success-and-failure.json`)
- Windows Event Log Service Running (`rules/windows/audit/windows-event-log-service-running.json`)
- Windows Firewall Log Size At Least 16 MB (All Profiles) (`rules/windows/audit/windows-firewall-log-size-at-least-16-mb-all-profiles.json`)
- Windows Firewall Logs Dropped Packets (All Profiles) (`rules/windows/audit/windows-firewall-logs-dropped-packets-all-profiles.json`)
- Windows PowerShell Operational Event Log Size At Least 64 MB (`rules/windows/audit/windows-powershell-operational-event-log-size-at-least-64-mb.json`)
- Windows PowerShell Transcription Enabled (`rules/windows/audit/windows-powershell-transcription-enabled.json`)
- Windows Process Creation Events Include Command Line (`rules/windows/audit/windows-process-creation-events-include-command-line.json`)
- Windows Security Event Log Warning at 90% Capacity (`rules/windows/audit/windows-security-event-log-warning-at-90-capacity.json`)
- Windows Setup Event Log Size At Least 32 MB (`rules/windows/audit/windows-setup-event-log-size-at-least-32-mb.json`)
- Windows System Event Log Size At Least 32 MB (`rules/windows/audit/windows-system-event-log-size-at-least-32-mb.json`)

#### windows/authentication

- Windows Account Lockout Counter Reset After 15 Minutes or More (`rules/windows/authentication/windows-account-lockout-counter-reset-after-15-minutes-or-more.json`)
- Windows Account Lockout Threshold 1-5 Attempts (`rules/windows/authentication/windows-account-lockout-threshold-1-5-attempts.json`)
- Windows Automatic Logon Disabled (`rules/windows/authentication/windows-automatic-logon-disabled.json`)
- Windows Automatic Sign-in After Restart Disabled (`rules/windows/authentication/windows-automatic-sign-in-after-restart-disabled.json`)
- Windows Blank Passwords Limited to Console Logon (`rules/windows/authentication/windows-blank-passwords-limited-to-console-logon.json`)
- Windows Cached Logons Limited to 4 or Fewer (`rules/windows/authentication/windows-cached-logons-limited-to-4-or-fewer.json`)
- Windows Convenience PIN Sign-in Disabled (`rules/windows/authentication/windows-convenience-pin-sign-in-disabled.json`)
- Windows Credential Guard Running (`rules/windows/authentication/windows-credential-guard-running.json`)
- Windows CredSSP Encryption Oracle Remediation Forced (`rules/windows/authentication/windows-credssp-encryption-oracle-remediation-forced.json`)
- Windows Kerberos Encryption Types Exclude DES and RC4 (`rules/windows/authentication/windows-kerberos-encryption-types-exclude-des-and-rc4.json`)
- Windows Last Signed-in User Name Not Displayed (`rules/windows/authentication/windows-last-signed-in-user-name-not-displayed.json`)
- Windows Local System Uses Computer Identity for NTLM (`rules/windows/authentication/windows-local-system-uses-computer-identity-for-ntlm.json`)
- Windows Machine Account Password Changes Enabled (30 Days or Less) (`rules/windows/authentication/windows-machine-account-password-changes-enabled-30-days-or-less.json`)
- Windows Network Credentials Not Stored (DisableDomainCreds) (`rules/windows/authentication/windows-network-credentials-not-stored-disabledomaincreds.json`)
- Windows NTLM Null Session Fallback Disabled (`rules/windows/authentication/windows-ntlm-null-session-fallback-disabled.json`)
- Windows NTLM SSP Client Requires NTLMv2 and 128-bit Encryption (`rules/windows/authentication/windows-ntlm-ssp-client-requires-ntlmv2-and-128-bit-encryption.json`)
- Windows NTLM SSP Server Requires NTLMv2 and 128-bit Encryption (`rules/windows/authentication/windows-ntlm-ssp-server-requires-ntlmv2-and-128-bit-encryption.json`)
- Windows PKU2U Online Identity Authentication Disabled (`rules/windows/authentication/windows-pku2u-online-identity-authentication-disabled.json`)
- Windows Remote Host Delegation of Non-Exportable Credentials Allowed (`rules/windows/authentication/windows-remote-host-delegation-of-non-exportable-credentials-allowed.json`)
- Windows Secure Attention Sequence (Ctrl+Alt+Del) Required (`rules/windows/authentication/windows-secure-attention-sequence-ctrlplusaltplusdel-required.json`)
- Windows Winlogon Clear-Text DefaultPassword Not Stored (`rules/windows/authentication/windows-winlogon-clear-text-defaultpassword-not-stored.json`)

#### windows/identity_management

- Windows Built-in Administrator Account Disabled (`rules/windows/identity_management/windows-built-in-administrator-account-disabled.json`)
- Windows Local Administrator Password Solution (LAPS) Enabled (`rules/windows/identity_management/windows-local-administrator-password-solution-laps-enabled.json`)
- Windows Microsoft Accounts Blocked (`rules/windows/identity_management/windows-microsoft-accounts-blocked.json`)

#### windows/integrity

- Microsoft Edge SmartScreen Enabled (`rules/windows/integrity/microsoft-edge-smartscreen-enabled.json`)
- Microsoft Edge SmartScreen Warnings Cannot Be Bypassed (`rules/windows/integrity/microsoft-edge-smartscreen-warnings-cannot-be-bypassed.json`)
- Windows ASR Rule: Block Abuse of Exploited Vulnerable Signed Drivers (`rules/windows/integrity/windows-asr-rule-block-abuse-of-exploited-vulnerable-signed-drivers.json`)
- Windows ASR Rule: Block Adobe Reader from Creating Child Processes (`rules/windows/integrity/windows-asr-rule-block-adobe-reader-from-creating-child-processes.json`)
- Windows ASR Rule: Block All Office Applications from Creating Child Processes (`rules/windows/integrity/windows-asr-rule-block-all-office-applications-from-creating-child-processes.json`)
- Windows ASR Rule: Block Credential Stealing from LSASS (`rules/windows/integrity/windows-asr-rule-block-credential-stealing-from-lsass.json`)
- Windows ASR Rule: Block Executable Content from Email Client and Webmail (`rules/windows/integrity/windows-asr-rule-block-executable-content-from-email-client-and-webmail.json`)
- Windows ASR Rule: Block Executables Unless They Meet Prevalence, Age or Trusted List Criteria (`rules/windows/integrity/windows-asr-rule-block-executables-unless-they-meet-prevalence-age-or-trusted-list-criteria.json`)
- Windows ASR Rule: Block Execution of Potentially Obfuscated Scripts (`rules/windows/integrity/windows-asr-rule-block-execution-of-potentially-obfuscated-scripts.json`)
- Windows ASR Rule: Block JavaScript or VBScript from Launching Downloaded Executable Content (`rules/windows/integrity/windows-asr-rule-block-javascript-or-vbscript-from-launching-downloaded-executable-content.json`)
- Windows ASR Rule: Block Office Applications from Creating Executable Content (`rules/windows/integrity/windows-asr-rule-block-office-applications-from-creating-executable-content.json`)
- Windows ASR Rule: Block Office Applications from Injecting Code into Other Processes (`rules/windows/integrity/windows-asr-rule-block-office-applications-from-injecting-code-into-other-processes.json`)
- Windows ASR Rule: Block Office Communication Application from Creating Child Processes (`rules/windows/integrity/windows-asr-rule-block-office-communication-application-from-creating-child-processes.json`)
- Windows ASR Rule: Block Persistence Through WMI Event Subscription (`rules/windows/integrity/windows-asr-rule-block-persistence-through-wmi-event-subscription.json`)
- Windows ASR Rule: Block Process Creations from PSExec and WMI Commands (`rules/windows/integrity/windows-asr-rule-block-process-creations-from-psexec-and-wmi-commands.json`)
- Windows ASR Rule: Block Rebooting Machine in Safe Mode (`rules/windows/integrity/windows-asr-rule-block-rebooting-machine-in-safe-mode.json`)
- Windows ASR Rule: Block Untrusted and Unsigned Processes That Run from USB (`rules/windows/integrity/windows-asr-rule-block-untrusted-and-unsigned-processes-that-run-from-usb.json`)
- Windows ASR Rule: Block Webshell Creation for Servers (`rules/windows/integrity/windows-asr-rule-block-webshell-creation-for-servers.json`)
- Windows ASR Rule: Block Win32 API Calls from Office Macros (`rules/windows/integrity/windows-asr-rule-block-win32-api-calls-from-office-macros.json`)
- Windows ASR Rule: Use Advanced Protection Against Ransomware (`rules/windows/integrity/windows-asr-rule-use-advanced-protection-against-ransomware.json`)
- Windows Defender Antivirus in Active Mode (`rules/windows/integrity/windows-defender-antivirus-in-active-mode.json`)
- Windows Defender Behavior Monitoring Enabled (`rules/windows/integrity/windows-defender-behavior-monitoring-enabled.json`)
- Windows Defender Cannot Be Turned Off by Policy (`rules/windows/integrity/windows-defender-cannot-be-turned-off-by-policy.json`)
- Windows Defender Cloud-Delivered Protection Enabled (`rules/windows/integrity/windows-defender-cloud-delivered-protection-enabled.json`)
- Windows Defender Download Scanning (IOAV) Enabled (`rules/windows/integrity/windows-defender-download-scanning-ioav-enabled.json`)
- Windows Defender Email Scanning Enabled (`rules/windows/integrity/windows-defender-email-scanning-enabled.json`)
- Windows Defender Network Protection Blocks Malicious Sites (`rules/windows/integrity/windows-defender-network-protection-blocks-malicious-sites.json`)
- Windows Defender On-Access Protection Enabled (`rules/windows/integrity/windows-defender-on-access-protection-enabled.json`)
- Windows Defender PUA Protection Enabled (`rules/windows/integrity/windows-defender-pua-protection-enabled.json`)
- Windows Defender Real-Time Protection Not Disabled by Policy (`rules/windows/integrity/windows-defender-real-time-protection-not-disabled-by-policy.json`)
- Windows Defender Scan Performed Within 7 Days (`rules/windows/integrity/windows-defender-scan-performed-within-7-days.json`)
- Windows Defender Scans Removable Drives (`rules/windows/integrity/windows-defender-scans-removable-drives.json`)
- Windows Defender Script Scanning Enabled (`rules/windows/integrity/windows-defender-script-scanning-enabled.json`)
- Windows SmartScreen for Explorer Set to Warn and Prevent Bypass (`rules/windows/integrity/windows-smartscreen-for-explorer-set-to-warn-and-prevent-bypass.json`)

#### windows/kernel_security

- Windows DEP Policy OptOut or AlwaysOn (`rules/windows/kernel_security/windows-dep-policy-optout-or-alwayson.json`)
- Windows Early Launch Antimalware Boot-Start Driver Policy (`rules/windows/kernel_security/windows-early-launch-antimalware-boot-start-driver-policy.json`)
- Windows Memory Integrity (HVCI) Running (`rules/windows/kernel_security/windows-memory-integrity-hvci-running.json`)
- Windows SEHOP Enabled (`rules/windows/kernel_security/windows-sehop-enabled.json`)
- Windows Virtualization-Based Security Running (`rules/windows/kernel_security/windows-virtualization-based-security-running.json`)

#### windows/network_security

- Domain Controller LDAP Channel Binding Required (`rules/windows/network_security/domain-controller-ldap-channel-binding-required.json`)
- Domain Controller LDAP Server Signing Required (`rules/windows/network_security/domain-controller-ldap-server-signing-required.json`)
- Windows Domain Member Secure Channel Signed and Sealed (`rules/windows/network_security/windows-domain-member-secure-channel-signed-and-sealed.json`)
- Windows Firewall Service Running (`rules/windows/network_security/windows-firewall-service-running.json`)
- Windows FTP Service Disabled (`rules/windows/network_security/windows-ftp-service-disabled.json`)
- Windows Hardened UNC Paths for SYSVOL and NETLOGON (`rules/windows/network_security/windows-hardened-unc-paths-for-sysvol-and-netlogon.json`)
- Windows IPv6 Source Routing Disabled (`rules/windows/network_security/windows-ipv6-source-routing-disabled.json`)
- Windows IRDP Router Discovery Disabled (`rules/windows/network_security/windows-irdp-router-discovery-disabled.json`)
- Windows LDAP Client Signing Required or Negotiated (`rules/windows/network_security/windows-ldap-client-signing-required-or-negotiated.json`)
- Windows NetBIOS Name Release on Demand Ignored (`rules/windows/network_security/windows-netbios-name-release-on-demand-ignored.json`)
- Windows NetBIOS Node Type P-node (`rules/windows/network_security/windows-netbios-node-type-p-node.json`)
- Windows Netlogon Secure Channel Protection Enforced (Zerologon) (`rules/windows/network_security/windows-netlogon-secure-channel-protection-enforced-zerologon.json`)
- Windows Non-Domain Network Connections Blocked While on Domain (`rules/windows/network_security/windows-non-domain-network-connections-blocked-while-on-domain.json`)
- Windows Print Spooler Disabled on Servers (`rules/windows/network_security/windows-print-spooler-disabled-on-servers.json`)
- Windows Print Spooler RPC Packet Privacy Required (`rules/windows/network_security/windows-print-spooler-rpc-packet-privacy-required.json`)
- Windows RPC Endpoint Mapper Client Authentication Enabled (`rules/windows/network_security/windows-rpc-endpoint-mapper-client-authentication-enabled.json`)
- Windows SChannel NULL, DES and RC2 Ciphers Not Enabled (`rules/windows/network_security/windows-schannel-null-des-and-rc2-ciphers-not-enabled.json`)
- Windows SMB Client Does Not Send Plain-Text Passwords (`rules/windows/network_security/windows-smb-client-does-not-send-plain-text-passwords.json`)
- Windows SMB Server Disconnects Clients When Logon Hours Expire (`rules/windows/network_security/windows-smb-server-disconnects-clients-when-logon-hours-expire.json`)
- Windows SMB Server Idle Session Disconnect 15 Minutes or Less (`rules/windows/network_security/windows-smb-server-idle-session-disconnect-15-minutes-or-less.json`)
- Windows SMB Server SPN Target Name Validation Enabled (`rules/windows/network_security/windows-smb-server-spn-target-name-validation-enabled.json`)
- Windows SSL 2.0 Server Protocol Disabled (`rules/windows/network_security/windows-ssl-2-0-server-protocol-disabled.json`)
- Windows SSL 3.0 Client Protocol Disabled (`rules/windows/network_security/windows-ssl-3-0-client-protocol-disabled.json`)
- Windows SSL 3.0 Server Protocol Disabled (`rules/windows/network_security/windows-ssl-3-0-server-protocol-disabled.json`)
- Windows Telnet Service Disabled (`rules/windows/network_security/windows-telnet-service-disabled.json`)
- Windows TLS 1.0 Client Protocol Disabled (`rules/windows/network_security/windows-tls-1-0-client-protocol-disabled.json`)
- Windows TLS 1.1 Client Protocol Disabled (`rules/windows/network_security/windows-tls-1-1-client-protocol-disabled.json`)
- Windows Unauthenticated RPC Clients Restricted (`rules/windows/network_security/windows-unauthenticated-rpc-clients-restricted.json`)
- Windows WinRM Client Basic Authentication Disabled (`rules/windows/network_security/windows-winrm-client-basic-authentication-disabled.json`)
- Windows WinRM Client Digest Authentication Disabled (`rules/windows/network_security/windows-winrm-client-digest-authentication-disabled.json`)
- Windows WinRM Client Unencrypted Traffic Disabled (`rules/windows/network_security/windows-winrm-client-unencrypted-traffic-disabled.json`)
- Windows WinRM Service Basic Authentication Disabled (`rules/windows/network_security/windows-winrm-service-basic-authentication-disabled.json`)
- Windows WinRM Service RunAs Credential Storage Disabled (`rules/windows/network_security/windows-winrm-service-runas-credential-storage-disabled.json`)
- Windows WinRM Service Unencrypted Traffic Disabled (`rules/windows/network_security/windows-winrm-service-unencrypted-traffic-disabled.json`)

#### windows/password_policy

- Windows Maximum Password Age 365 Days or Less (Not Unlimited) (`rules/windows/password_policy/windows-maximum-password-age-365-days-or-less-not-unlimited.json`)
- Windows Password Complexity Enabled (Local Policy) (`rules/windows/password_policy/windows-password-complexity-enabled-local-policy.json`)
- Windows Password Expiry Warning 5-14 Days (`rules/windows/password_policy/windows-password-expiry-warning-5-14-days.json`)
- Windows Password History At Least 24 (`rules/windows/password_policy/windows-password-history-at-least-24.json`)
- Windows Password Minimum Length At Least 14 (`rules/windows/password_policy/windows-password-minimum-length-at-least-14.json`)
- Windows Reversible Password Encryption Disabled (`rules/windows/password_policy/windows-reversible-password-encryption-disabled.json`)

#### windows/system_hardening

- Windows .NET Framework Uses System Default TLS Versions (32-bit) (`rules/windows/system_hardening/windows-net-framework-uses-system-default-tls-versions-32-bit.json`)
- Windows .NET Framework Uses System Default TLS Versions (64-bit) (`rules/windows/system_hardening/windows-net-framework-uses-system-default-tls-versions-64-bit.json`)
- Windows App Notifications Hidden on Lock Screen (`rules/windows/system_hardening/windows-app-notifications-hidden-on-lock-screen.json`)
- Windows Automatic Updates Configured to Install Automatically (`rules/windows/system_hardening/windows-automatic-updates-configured-to-install-automatically.json`)
- Windows AutoPlay Disabled for Non-Volume Devices (`rules/windows/system_hardening/windows-autoplay-disabled-for-non-volume-devices.json`)
- Windows Case Insensitivity for Non-Windows Subsystems (`rules/windows/system_hardening/windows-case-insensitivity-for-non-windows-subsystems.json`)
- Windows Computer Browser Service Disabled (`rules/windows/system_hardening/windows-computer-browser-service-disabled.json`)
- Windows Connected Users Not Enumerated on Domain-Joined Computers (`rules/windows/system_hardening/windows-connected-users-not-enumerated-on-domain-joined-computers.json`)
- Windows Diagnostic Data Limited to Required (`rules/windows/system_hardening/windows-diagnostic-data-limited-to-required.json`)
- Windows IIS Web Services Disabled on Non-Web Hosts (`rules/windows/system_hardening/windows-iis-web-services-disabled-on-non-web-hosts.json`)
- Windows Infrared Monitor Service Disabled (`rules/windows/system_hardening/windows-infrared-monitor-service-disabled.json`)
- Windows Internet Connection Sharing Disabled (`rules/windows/system_hardening/windows-internet-connection-sharing-disabled.json`)
- Windows Link-Layer Topology Discovery Mapper Disabled (`rules/windows/system_hardening/windows-link-layer-topology-discovery-mapper-disabled.json`)
- Windows Local Users Not Enumerated on Domain-Joined Computers (`rules/windows/system_hardening/windows-local-users-not-enumerated-on-domain-joined-computers.json`)
- Windows Lock Screen Camera Disabled (`rules/windows/system_hardening/windows-lock-screen-camera-disabled.json`)
- Windows Lock Screen Slide Show Disabled (`rules/windows/system_hardening/windows-lock-screen-slide-show-disabled.json`)
- Windows Media Player Network Sharing Disabled (`rules/windows/system_hardening/windows-media-player-network-sharing-disabled.json`)
- Windows Mobile Hotspot Service Disabled (`rules/windows/system_hardening/windows-mobile-hotspot-service-disabled.json`)
- Windows Network Selection UI Hidden on Logon Screen (`rules/windows/system_hardening/windows-network-selection-ui-hidden-on-logon-screen.json`)
- Windows OpenSSH Server Disabled (`rules/windows/system_hardening/windows-openssh-server-disabled.json`)
- Windows Peer Networking Services Disabled (`rules/windows/system_hardening/windows-peer-networking-services-disabled.json`)
- Windows PowerShell 2.0 Engine Disabled (`rules/windows/system_hardening/windows-powershell-2-0-engine-disabled.json`)
- Windows Print Driver Download over HTTP Disabled (`rules/windows/system_hardening/windows-print-driver-download-over-http-disabled.json`)
- Windows Print Spooler Redirection Guard Enabled (`rules/windows/system_hardening/windows-print-spooler-redirection-guard-enabled.json`)
- Windows Remote Registry Service Disabled (`rules/windows/system_hardening/windows-remote-registry-service-disabled.json`)
- Windows Routing and Remote Access Service Disabled (`rules/windows/system_hardening/windows-routing-and-remote-access-service-disabled.json`)
- Windows RPC Locator Service Disabled (`rules/windows/system_hardening/windows-rpc-locator-service-disabled.json`)
- Windows Safe DLL Search Mode Enabled (`rules/windows/system_hardening/windows-safe-dll-search-mode-enabled.json`)
- Windows Shutdown Without Logon Disabled (`rules/windows/system_hardening/windows-shutdown-without-logon-disabled.json`)
- Windows Simple TCP/IP Services Disabled (`rules/windows/system_hardening/windows-simple-tcp-ip-services-disabled.json`)
- Windows SNMP Service Disabled (`rules/windows/system_hardening/windows-snmp-service-disabled.json`)
- Windows SSDP and UPnP Services Disabled (`rules/windows/system_hardening/windows-ssdp-and-upnp-services-disabled.json`)
- Windows Strengthened Default Permissions of Internal System Objects (`rules/windows/system_hardening/windows-strengthened-default-permissions-of-internal-system-objects.json`)
- Windows Subsystem for Linux Manager Disabled on Servers (`rules/windows/system_hardening/windows-subsystem-for-linux-manager-disabled-on-servers.json`)
- Windows Time Synchronized from a Network Source (`rules/windows/system_hardening/windows-time-synchronized-from-a-network-source.json`)
- Windows Update Service Not Disabled (`rules/windows/system_hardening/windows-update-service-not-disabled.json`)
- Windows Xbox Services Disabled (`rules/windows/system_hardening/windows-xbox-services-disabled.json`)

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
