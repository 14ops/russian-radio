"""Writes files.json: every file the app ships, with its size and SHA-256.

"Update Povtori FM.cmd" downloads this list, compares it with the files on the USB stick,
and downloads only what changed or is missing. Run this before every commit that changes
a shipped file:  python3 tools/make_manifest.py        (add --check to only verify)
"""
import hashlib
import json
import os
import re
import subprocess
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
OUT = os.path.join(ROOT, 'files.json')
SKIP_DIRS = ('tools/', '.github/')
SKIP_FILES = {'files.json', '.gitattributes', '.gitignore', '.nojekyll'}


def shipped():
    out = subprocess.run(['git', 'ls-files', '--cached', '--others', '--exclude-standard', '-z'],
                         cwd=ROOT, check=True, capture_output=True).stdout.decode('utf-8')
    paths = sorted({p for p in out.split('\0') if p})
    return [p for p in paths if not p.startswith(SKIP_DIRS) and p not in SKIP_FILES
            and os.path.isfile(os.path.join(ROOT, p))]


def build():
    page = open(os.path.join(ROOT, 'Povtori FM.html'), encoding='utf-8').read()
    m = re.search(r"const VERSION = '([^']+)'", page)
    files = []
    for p in shipped():
        h, size = hashlib.sha256(), 0
        with open(os.path.join(ROOT, p), 'rb') as f:
            for chunk in iter(lambda: f.read(1 << 20), b''):
                h.update(chunk)
                size += len(chunk)
        files.append({'path': p, 'size': size, 'sha256': h.hexdigest()})
    return {'app': 'Povtori FM', 'version': m.group(1) if m else '?', 'files': files}


def render(data):
    rows = ',\n'.join('  ' + json.dumps(f, ensure_ascii=False) for f in data['files'])
    return '{"app": %s, "version": %s, "files": [\n%s\n]}\n' % (json.dumps(data['app']), json.dumps(data['version']), rows)


def main():
    text = render(build())
    if '--check' in sys.argv:
        old = open(OUT, encoding='utf-8').read() if os.path.exists(OUT) else ''
        if old != text:
            sys.exit('files.json is out of date. Run: python3 tools/make_manifest.py')
        print('files.json is current')
        return
    with open(OUT, 'w', encoding='utf-8', newline='\n') as f:
        f.write(text)
    data = json.loads(text)
    print('wrote files.json: version %s, %d files, %.1f MB' % (data['version'], len(data['files']), sum(f['size'] for f in data['files']) / 1e6))


if __name__ == '__main__':
    main()
