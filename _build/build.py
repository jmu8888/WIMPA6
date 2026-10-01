# Build web images + assets/data.js from entries.json and translations.json
import os, re, json
from PIL import Image, ImageOps
Image.MAX_IMAGE_PIXELS = None
HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)
E = json.load(open(os.path.join(HERE, 'entries.json'), encoding='utf-8'))
T = json.load(open(os.path.join(HERE, 'translations.json'), encoding='utf-8'))
CJK = re.compile(r'[㐀-鿿＀-￯《》（）]')

CATS = {
 'everyday-single': 'Everyday Life · Single Photo',
 'everyday-series': 'Everyday Life · Photo Series',
 'people': 'People & Documentary',
 'nature': 'Nature & Landscape',
 'art': 'Art & Creativity',
 'open': 'Open Category',
 'theme-journey': 'Theme: The Journey',
 'theme-life-single': 'Theme: Life · Single Photo',
 'theme-life-series': 'Theme: Life · Photo Series',
}

def clean_title(t):
    t = t.strip()
    if t in T['titles']: return T['titles'][t]
    if CJK.search(t):
        en = re.sub(r'[㐀-鿿《》（）()「」]+', ' ', t).strip(' _-·|')
        if re.search(r'[A-Za-z]{3}', en): return re.sub(r'\s+', ' ', en)
        print('UNTRANSLATED TITLE', t); return ''
    t = t.replace('_', ' ')
    return t[:1].upper() + t[1:]

def clean_name(n):
    n = (n or '').strip()
    if n in T['names']: return T['names'][n]
    n = re.sub(r'[（(].*?[)）]', '', n).strip()
    if CJK.search(n):
        en = re.sub(r'[㐀-鿿]+', '', n).strip()
        if en: return en
        print('UNTRANSLATED NAME', n); return ''
    n = re.sub(r'(?<=[a-z])(?=[A-Z])', ' ', n)          # CatherineWang -> Catherine Wang
    if n.isupper() or n.islower(): n = n.title()
    return n

def clean_desc(e):
    d = (e['desc'] or '').strip()
    if e['title'] in T.get('descs', {}): return T['descs'][e['title']]
    if not d: return ''
    if not CJK.search(d): return d
    m = re.match(r'^([^㐀-鿿]{40,}?)(?=[㐀-鿿《])', d)   # English part before Chinese
    return m.group(1).strip() if m else ''

def zh_part(t):
    # keep the Chinese part of a bilingual string
    t = re.sub(r'[（(]已跟拍摄者沟通好可以发表[）)]?', '', t)
    z = re.sub(r"[A-Za-z][A-Za-z0-9 '’\-,.&!?]*", ' ', t)
    z = re.sub(r'[（(]\s*[)）]', '', z)
    z = re.sub(r'\s+', ' ', z).strip(' _-·|()（）')
    return z

def zh_title(e):
    t = e['title'].strip()
    if CJK.search(t):
        z = zh_part(t)
        return z if len(re.findall(r'[㐀-鿿]', z)) >= 2 else t
    return clean_title(t)

def zh_name(n):
    n = (n or '').strip()
    if re.search(r'[㐀-鿿]', n):
        m = re.search(r'[（(]([㐀-鿿]+)[）)]', n)
        return m.group(1) if m else zh_part(n)
    return clean_name(n)

def zh_desc(e):
    d = (e['desc'] or '').strip()
    if e['title'] in T.get('descs_zh', {}): return T['descs_zh'][e['title']]
    if not re.search(r'[㐀-鿿]', d): return ''
    i = re.search(r'[㐀-鿿《“]', d).start()
    return d[i:].strip() if i > 40 else d

os.makedirs(os.path.join(SITE, 'images', 'w'), exist_ok=True)
os.makedirs(os.path.join(SITE, 'images', 't'), exist_ok=True)
def save(src, rel, size, q):
    out = os.path.join(SITE, rel)
    if os.path.exists(out): return Image.open(out).size
    im = Image.open(src); im.draft('RGB', (size, size)); im = ImageOps.exif_transpose(im).convert('RGB')
    im.thumbnail((size, size), Image.LANCZOS)
    im.save(out, 'JPEG', quality=q, optimize=True, progressive=True)
    return im.size

order = {'gold': 0, 'silver': 1, 'bronze': 2, 'hm': 3}
E.sort(key=lambda e: (-e['edition'], list(CATS).index(e['category']), order[e['award']], e['title']))
out = []
for i, e in enumerate(E):
    eid = f"e{e['edition']}-{i:03d}"
    imgs = []
    for n, f in enumerate(sorted(e['files'])):
        w, h = save(f, f'images/w/{eid}-{n}.jpg', 1800, 84)
        save(f, f'images/t/{eid}-{n}.jpg', 720, 80)
        imgs.append([f'{eid}-{n}', w, h])
    out.append(dict(id=eid, ed=e['edition'], cat=e['category'], aw=e['award'],
                    title=clean_title(e['title']), name=clean_name(e['name']),
                    state=(e['state'] or '').strip(), desc=clean_desc(e), img=imgs,
                    tz=zh_title(e), nz=zh_name(e['name']), dz=zh_desc(e)))
js = 'window.WIMPA_CATS=' + json.dumps(CATS, ensure_ascii=False) + ';\nwindow.WIMPA=' + json.dumps(out, ensure_ascii=False, separators=(',', ':')) + ';\n'
open(os.path.join(SITE, 'assets', 'data.js'), 'w', encoding='utf-8').write(js)
print(len(out), 'entries,', sum(len(x['img']) for x in out), 'images')
