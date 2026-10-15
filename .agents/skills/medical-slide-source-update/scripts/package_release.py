#!/usr/bin/env python3
"""Package a curated release directory with verified SHA256s; standard library only."""
import argparse, hashlib, json, os, tempfile, zipfile
from pathlib import Path

def package(source, output):
    raw = Path(source).expanduser()
    if raw.is_symlink():
        raise ValueError('Source directory must not be a symlink')
    src = raw.resolve(strict=True)
    dest = Path(output).expanduser().absolute()
    if not src.is_dir():
        raise ValueError('Source must be a directory')
    if dest.exists() or dest.is_symlink():
        raise FileExistsError(dest)
    if src == dest.resolve() or src in dest.resolve().parents:
        raise ValueError('Output must be outside the source directory')
    files = []
    for p in sorted(src.rglob('*')):
        if p.is_symlink():
            raise ValueError('Symlink is not allowed: ' + str(p))
        if p.is_file():
            name = p.relative_to(src).as_posix()
            if name == 'release-manifest.json':
                raise ValueError('Reserved file name: release-manifest.json')
            files.append((p, name))
    if not files:
        raise ValueError('Source is empty')
    dest.parent.mkdir(parents=True, exist_ok=True)
    fd, temp = tempfile.mkstemp(prefix='.release-', suffix='.zip', dir=dest.parent)
    os.close(fd)
    try:
        manifest = []
        with zipfile.ZipFile(temp, 'w', zipfile.ZIP_DEFLATED) as z:
            for p, name in files:
                data = p.read_bytes()
                manifest.append({'path': name, 'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()})
                z.writestr(name, data)
            z.writestr('release-manifest.json', json.dumps({'files': manifest}, ensure_ascii=False, indent=2))
        with zipfile.ZipFile(temp) as z:
            assert z.testzip() is None, 'ZIP integrity check failed'
            for row in manifest:
                data = z.read(row['path'])
                assert len(data) == row['bytes'] and hashlib.sha256(data).hexdigest() == row['sha256']
        # Exclusive creation: a concurrent job cannot be overwritten.
        os.link(temp, dest)
        return {'output': str(dest), 'files': len(files), 'bytes': dest.stat().st_size, 'verified': True}
    finally:
        Path(temp).unlink(missing_ok=True)

if __name__ == '__main__':
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('source')
    ap.add_argument('output')
    args = ap.parse_args()
    print(json.dumps(package(args.source, args.output), ensure_ascii=False))
