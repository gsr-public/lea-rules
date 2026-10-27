#!/usr/bin/env python3
"""Build a LEA rule pack (lea-rules-<version>.tgz + manifest + optional ed25519 signature) from a rules/ tree.

  python3 tools/build_pack.py --version 1.2.0 [--rules rules] [--retired retired.json] [--key signing.key] [--out dist] [--pack-id lea-open-rules]

Writes <out>/lea-rules-<version>.tgz, <out>/lea-rules-<version>.tgz.sig (with --key) and <out>/latest.json.
Signing needs the Python 'cryptography' package and an ed25519 private key in PEM (openssl genpkey -algorithm ed25519).
"""
import argparse
import base64
import gzip
import hashlib
import io
import json
import pathlib
import sys
import tarfile
import uuid


def fail(msg):
    sys.exit(f'build_pack: {msg}')


def collect(rules_dir):
    entries, files, uids, names = [], {}, set(), set()
    for path in sorted(rules_dir.glob('*/*/*.json')):
        rel = 'rules/' + path.relative_to(rules_dir).as_posix()
        data = path.read_bytes()
        try:
            rule = json.loads(data)
        except ValueError as e:
            fail(f'{rel}: invalid JSON: {e}')
        if not isinstance(rule, dict):
            fail(f'{rel}: must contain one rule object')
        try:
            uid = str(uuid.UUID(str(rule.get('uid'))))
        except ValueError:
            fail(f'{rel}: missing or invalid uid')
        if uid in uids:
            fail(f'{rel}: duplicate uid {uid}')
        if rule.get('name') in names:
            fail(f"{rel}: duplicate name {rule.get('name')}")
        uids.add(uid)
        names.add(rule.get('name'))
        files[rel] = data
        entries.append({'uid': uid, 'name': rule['name'], 'path': rel, 'sha256': hashlib.sha256(data).hexdigest(),
                        'former_names': rule.get('former_names') or []})
    if not entries:
        fail(f'no rules found under {rules_dir}')
    return entries, files, uids


def tgz(files):
    raw = io.BytesIO()
    with tarfile.open(fileobj=raw, mode='w', format=tarfile.PAX_FORMAT) as tar:
        for name in sorted(files):
            info = tarfile.TarInfo(name)
            info.size, info.mtime, info.mode, info.uid, info.gid, info.uname, info.gname = len(files[name]), 0, 0o644, 0, 0, '', ''
            tar.addfile(info, io.BytesIO(files[name]))
    out = io.BytesIO()
    with gzip.GzipFile(fileobj=out, mode='wb', mtime=0) as gz:
        gz.write(raw.getvalue())
    return out.getvalue()


def sign(data, key_path):
    from cryptography.hazmat.primitives import serialization
    from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
    key = serialization.load_pem_private_key(pathlib.Path(key_path).read_bytes(), password=None)
    if not isinstance(key, Ed25519PrivateKey):
        fail(f'{key_path} is not an ed25519 private key')
    public = key.public_key().public_bytes(serialization.Encoding.Raw, serialization.PublicFormat.Raw)
    return {'alg': 'ed25519', 'key': hashlib.sha256(public).hexdigest()[:16], 'public_key': base64.b64encode(public).decode(),
            'sig': base64.b64encode(key.sign(data)).decode()}


def main():
    ap = argparse.ArgumentParser(description='Build a LEA rule pack')
    ap.add_argument('--version', required=True)
    ap.add_argument('--rules', default='rules')
    ap.add_argument('--retired', default='retired.json')
    ap.add_argument('--key')
    ap.add_argument('--out', default='dist')
    ap.add_argument('--pack-id', default='lea-open-rules')
    args = ap.parse_args()

    entries, files, uids = collect(pathlib.Path(args.rules))
    retired_path = pathlib.Path(args.retired)
    retired = json.loads(retired_path.read_text()) if retired_path.exists() else []
    for r in retired:
        if r['uid'] in uids:
            fail(f"retired uid {r['uid']} ({r.get('name')}) is still in {args.rules}")
    manifest = {'format': 1, 'pack_id': args.pack_id, 'version': args.version, 'rules': entries, 'retired': [r['uid'] for r in retired]}
    files['manifest.json'] = (json.dumps(manifest, indent=1, sort_keys=True) + '\n').encode()
    data = tgz(files)
    out = pathlib.Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    name = f'lea-rules-{args.version}.tgz'
    (out / name).write_bytes(data)
    latest = {'pack_id': args.pack_id, 'version': args.version, 'url': name, 'sha256': hashlib.sha256(data).hexdigest(), 'rules': len(entries)}
    if args.key:
        (out / f'{name}.sig').write_text(json.dumps(sign(data, args.key), indent=1) + '\n')
        latest['sig'] = f'{name}.sig'
    (out / 'latest.json').write_text(json.dumps(latest, indent=1) + '\n')
    print(f"{out / name}: {len(entries)} rules, {len(retired)} retired, sha256 {latest['sha256']}{', signed' if args.key else ', unsigned'}")


if __name__ == '__main__':
    main()
