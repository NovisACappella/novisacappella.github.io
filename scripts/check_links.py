"""Check that every local file the website links to really exists, with exact capitalization.
Usage: python3 scripts/check_links.py _site [https://novisutd.org]   (run on the built site)
Links to the site's own domain (redirect pages use these) are checked like local links.
Checks src/href attributes, CSS url(...) and inline styles, and redirect pages.
Skips HTML <!-- comments --> and CSS /* comments */, outside websites, mailto: and #anchors."""
import os, re, sys, html
from urllib.parse import unquote, urlsplit

root = os.path.abspath(sys.argv[1])
site_url = (sys.argv[2] if len(sys.argv) > 2 else 'https://novisutd.org').rstrip('/')
own_origin = re.compile(r'^https?://(www\.)?' + re.escape(urlsplit(site_url).netloc) + r'(?=[/?#]|$)', re.I)
all_files = set()
for d, _, fs in os.walk(root):
    if '/.git' in d: continue
    for f in fs: all_files.add(os.path.relpath(os.path.join(d, f), root))

def exists(rel):
    rel = os.path.normpath(rel).lstrip('./') if rel not in ('', '.') else ''
    cands = [rel] if rel else []
    cands += [os.path.join(rel, 'index.html') if rel else 'index.html', rel + '.html']
    return any(c in all_files for c in cands)

def check(src_file, ref, base_dir):
    ref = html.unescape(ref.strip())
    if own_origin.match(ref):
        ref = own_origin.sub('', ref) or '/'
    if not ref or ref.startswith(('http:', 'https:', '//', 'mailto:', 'tel:', '#', 'data:', 'javascript:')): return None
    path = unquote(urlsplit(ref).path)
    if not path: return None
    rel = path.lstrip('/') if path.startswith('/') else os.path.relpath(os.path.join(base_dir, path), root)
    return None if exists(rel) else f'{os.path.relpath(src_file, root)} -> {ref}'

broken, count = [], 0
for rel in sorted(all_files):
    p = os.path.join(root, rel)
    if rel.endswith('.html'):
        t = re.sub(r'<!--.*?-->', '', open(p, encoding='utf-8', errors='ignore').read(), flags=re.S)
        refs = re.findall(r'''\b(?:src|href)\s*=\s*["']([^"']*)["']''', t)
        refs += re.findall(r'''url\(\s*['"]?([^'")]+)['"]?\s*\)''', t)   # inline styles
        refs += re.findall(r'''http-equiv="refresh"\s+content="\d+;\s*url=([^"]+)"''', t, flags=re.I)
    elif rel.endswith('.css'):
        t = re.sub(r'/\*.*?\*/', '', open(p, encoding='utf-8', errors='ignore').read(), flags=re.S)
        refs = re.findall(r'''url\(\s*['"]?([^'")]+)['"]?\s*\)''', t)
    else: continue
    for r in refs:
        count += 1
        b = check(p, r, os.path.dirname(p))
        if b and b not in broken: broken.append(b)   # report each broken link once per page
print(f'checked {count} references in {root}')
for b in broken: print('BROKEN:', b)
print('RESULT:', 'OK, 0 broken' if not broken else f'{len(broken)} broken')
sys.exit(1 if broken else 0)
