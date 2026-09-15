import io, re, os, sys, unicodedata, difflib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from spec import STORIES

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "texts")

def norm(s):
    s = unicodedata.normalize('NFKD', s)
    s = ''.join(c for c in s if not unicodedata.combining(c))
    s = s.replace('’', "'").replace('‘', "'")
    s = re.sub(r'[^a-z0-9]+', ' ', s.lower()).strip()
    return s

GUT = re.compile(r'\*\*\* *(START|END) OF TH', re.I)

def raw(path, a, b):
    lines = io.open(os.path.join(ROOT, path), encoding='utf-8', errors='replace').read().replace('\r','').split('\n')
    seg = lines[a-1:min(b-1, len(lines))]
    out = []
    for l in seg:
        if GUT.search(l):
            break
        out.append(l.rstrip())
    return out

TRANS = re.compile(r'^\s*\[?(Transcriber|Illustration|Frontispiece|Footnote)', re.I)

def clean_head(lines, title, author):
    """Drop heading/byline/epigraph-blurb lines at the top of a segment."""
    nt, na = norm(title), norm(author)
    i = 0
    n = len(lines)
    while i < n:
        s = lines[i].strip()
        ns = norm(s)
        if not s:
            i += 1; continue
        if ns == nt or ns == na or ns == 'by ' + na or ns == na.replace(' ', ' '):
            i += 1; continue
        if re.fullmatch(r'by .{0,50}', ns) and len(s) < 60:
            i += 1; continue
        if re.fullmatch(r'\(?\d{4}\)?\.?', s):
            i += 1; continue
        if re.fullmatch(r'(published|first published)\s*:?\s*\d{4}\.?', ns):
            i += 1; continue
        if re.fullmatch(r'by .{0,60}\d{4}.{0,10}', ns):
            i += 1; continue
        if nt.startswith(ns) and len(ns) >= 4 and len(s) < 50:   # title split over lines
            i += 1; continue
        if len(s) < 60 and s.upper() == s and            difflib.SequenceMatcher(None, ns, nt).ratio() > 0.75:   # misspelt heading
            i += 1; continue
        break
    # bracketed transcriber/illustration blocks and centred pulp blurbs
    while i < n:
        s = lines[i].strip()
        if not s:
            i += 1; continue
        if re.match(r'(From _|Copyright|By permission)', s) or 'By permission of the publisher' in s:
            while i < n and lines[i].strip():
                i += 1
            continue
        if s.startswith('[') or TRANS.match(s):
            while i < n and ']' not in lines[i]:
                i += 1
            i += 1
            continue
        break
    return lines[i:]

SECT = re.compile(r'^(?:[IVXLC]{1,7}|\d{1,3})\.?$')
CHAP = re.compile(r'^(?:CHAPTER|PART|PORTION|PROLOGUE|EPILOGUE|CONCLUSION)\b.{0,60}$', re.I)
STARS = re.compile(r'^[\s*.\-–—_]{3,}$')

def paragraphs(lines):
    """-> list of ('p'|'sect'|'break', text)"""
    out, buf = [], []
    def flush():
        if buf:
            out.append(('p', ' '.join(x.strip() for x in buf).strip()))
            buf.clear()
    for l in lines:
        s = l.strip()
        if not s:
            flush(); continue
        if STARS.fullmatch(s):
            flush(); out.append(('break', '')); continue
        if not buf and SECT.fullmatch(s):
            flush(); out.append(('sect', s.rstrip('.'))); continue
        if not buf and CHAP.match(s) and len(s) < 62 and s.upper() == s:
            flush(); out.append(('sect', s.rstrip('.'))); continue
        buf.append(s)
    flush()
    # collapse a 'sect' immediately followed by a short all-caps title line
    merged = []
    for kind, txt in out:
        if kind == 'p' and merged and merged[-1][0] == 'sect' and len(txt) < 60 \
           and txt.upper() == txt and not txt.endswith(('.', '!', '?', '"', '”')):
            merged[-1] = ('sect', merged[-1][1] + '. ' + txt.rstrip('.'))
            continue
        merged.append((kind, txt))
    while merged and merged[0][0] == 'break':
        merged.pop(0)
    while merged and merged[-1][0] == 'break':
        merged.pop()
    JUNK = re.compile(r'^(THE END\.?|END OF VOL.*|END OF VOLUME.*|PRINTED BY .*|<[^>]*>|FINIS\.?)$', re.I)
    while merged and (merged[-1][0] != 'p' or JUNK.match(merged[-1][1].strip())):
        merged.pop()
    return merged

def build():
    books = []
    for path, a, b, title, author, year in STORIES:
        lines = clean_head(raw(path, a, b), title, author)
        paras = paragraphs(lines)
        words = sum(len(t.split()) for k, t in paras if k == 'p')
        books.append(dict(path=path, title=title, author=author, year=year,
                          paras=paras, words=words))
    return books

if __name__ == '__main__':
    bs = build()
    total = 0
    for b in bs:
        total += b['words']
        first = next((t for k, t in b['paras'] if k == 'p'), '')
        last  = [t for k, t in b['paras'] if k == 'p'][-1] if b['paras'] else ''
        print(f"{b['words']:>7,}  {b['author'][:24]:<24} {b['title'][:42]:<42}")
        print(f"         OPEN | {first[:110]}")
        print(f"         SHUT | {last[-110:]}")
    print(f"\nTOTAL {total:,} words across {len(bs)} stories  (~{total//350:,} pages of text)")
