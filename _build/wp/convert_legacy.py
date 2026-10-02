# Convert the old gwmpa.org pages (built with the "photography" theme's page builder)
# into clean HTML that the new WIMPA theme can render. Output: legacy.json
import json, os, re, html
from bs4 import BeautifulSoup, NavigableString, Tag, Comment

BK = r"G:\2027第六届手机摄影大赛\gwmpa-backup"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'legacy.json')

# Real (non-demo) pages kept from the old site; slug is the new page slug
KEEP = {
    8588: '2025-awards', 8602: '2025-awards-theme-series', 8603: '2025-awards-theme-single',
    8601: '2025-awards-people', 8558: '2025-awards-art', 8594: '2025-awards-nature',
    8630: '5th-winners-list', 7987: '2025-judges',
    7426: 'awards-2024', 7391: '2024-awards-theme-series', 7388: '2024-awards-theme-single',
    7338: '2024-awards-people', 7318: '2024-awards-art', 7321: '2024-awards-nature',
    7644: '4th-winners-list', 6765: 'judges-2024',
    6671: 'awards-2023', 6757: '2023-awards-trip', 6693: 'awards-2023-landscape',
    6752: 'awards-2023-art', 6675: 'awards-2023-documentary', 6545: '3rd-winners-list',
    5776: '2022-awards', 6018: '2022-awards-landscape', 6029: '2022-awards-art', 6024: '2022-awards-documentary',
    5768: '2021-awards', 6071: '2021-awards-landscape', 6090: '2021-awards-art', 6083: '2021-awards-documentary',
    5765: 'previous-awards', 6777: 'co-organizer-list', 6464: 'sponsors', 6181: 'donation', 18: 'about-us',
    5781: 'view-submit', 6561: 'awards-rules-2024', 5869: 'judges-cn',
}
TEXT_TAGS = {'h1': 'h2', 'h2': 'h2', 'h3': 'h3', 'h4': 'h4', 'h5': 'h4', 'h6': 'h4'}
UPL = re.compile(r'-\d+x\d+(?=\.\w+$)')

def full_size(src):
    return UPL.sub('', src)

def inline_html(node):
    """Inner HTML of a text block, keeping only simple inline tags."""
    out = []
    for c in node.children:
        if isinstance(c, NavigableString):
            out.append(html.escape(str(c), quote=False))
        elif isinstance(c, Tag):
            if c.name in ('a',) and c.get('href') and not c.find('img'):
                out.append('<a href="%s">%s</a>' % (html.escape(c['href']), inline_html(c)))
            elif c.name in ('strong', 'b', 'em', 'i', 'br', 'span', 'sup', 'sub', 'u'):
                out.append('<br>' if c.name == 'br' else ('<%s>%s</%s>' % (c.name, inline_html(c), c.name) if c.name in ('strong', 'b', 'em', 'i') else inline_html(c)))
            elif c.name == 'img':
                continue
            else:
                out.append(inline_html(c))
    return ''.join(out)

def walk(node, items, seen):
    for c in list(node.children):
        if isinstance(c, Comment):
            continue
        if isinstance(c, NavigableString):
            t = str(c).strip()
            if t and node.name in ('div', 'section', 'td'):
                items.append(('p', html.escape(t, quote=False)))
            continue
        if not isinstance(c, Tag):
            continue
        cls = ' '.join(c.get('class') or [])
        if c.name in ('script', 'style', 'noscript', 'form', 'button', 'input'):
            continue
        if c.name == 'a' and 'fancy-gallery' in cls:
            href = c.get('href', ''); im = c.find('img')
            if href in seen: continue
            seen.add(href)
            items.append(('img', im['src'] if im else href, href, html.unescape(c.get('data-title', '')).strip()))
            continue
        if 'image_classic_frame' in cls or c.name == 'figure':
            im = c.find('img'); cap = c.find(class_='image_caption') or c.find('figcaption')
            a = c.find('a')
            if im and im.get('src'):
                href = a['href'] if a and a.get('href', '').startswith('http') else full_size(im['src'])
                if href not in seen:
                    seen.add(href)
                    items.append(('img', im['src'], href, cap.get_text(' ', strip=True) if cap else (im.get('alt') or '')))
                continue
        if c.name == 'img' and c.get('src'):
            href = full_size(c['src'])
            if href not in seen and 'logo' not in c['src']:
                seen.add(href); items.append(('img', c['src'], href, c.get('alt') or ''))
            continue
        if c.name == 'iframe' and c.get('src'):
            if 'embed=true' in c['src']: continue           # WordPress link-preview embeds; the link itself is kept
            if c['src'].rstrip('/').endswith('gwmpa.org/login'):
                items.append(('p', '<a class="wl-button" href="https://www.gwmpa.org/login">Go to the submission system / 进入投稿系统</a>')); continue
            items.append(('embed', c['src'])); continue
        if c.name in TEXT_TAGS:
            t = c.get_text(' ', strip=True)
            if t and not (items and items[-1] == ('h', TEXT_TAGS[c.name], t)):   # the old builder repeats headings
                items.append(('h', TEXT_TAGS[c.name], t))
            continue
        if c.name in ('p', 'blockquote', 'pre'):
            if c.find('img') or c.find('iframe'):
                walk(c, items, seen)
            h = inline_html(c).strip()
            if re.sub(r'(<br>|&nbsp;|\s|\xa0)+', '', h):
                items.append(('p', h))
            continue
        if c.name in ('ul', 'ol'):
            lis = ''.join('<li>%s</li>' % inline_html(li) for li in c.find_all('li', recursive=False))
            if lis: items.append(('list', '<%s>%s</%s>' % (c.name, lis, c.name)))
            continue
        if c.name == 'table':
            rows = []
            for tr in c.find_all('tr'):
                rows.append('<tr>%s</tr>' % ''.join('<td>%s</td>' % inline_html(td) for td in tr.find_all(['td', 'th'])))
            items.append(('table', '<table>%s</table>' % ''.join(rows))); continue
        if c.name == 'a' and c.get('href') and c.get_text(strip=True):
            items.append(('p', '<a href="%s">%s</a>' % (html.escape(c['href']), html.escape(c.get_text(' ', strip=True)))))
            continue
        walk(c, items, seen)

def render(items):
    out, gal = [], []
    def flush():
        if not gal: return
        cls = 'wimpa-legacy-gallery' + (' single' if len(gal) == 1 else '')
        out.append('<div class="%s">%s</div>' % (cls, ''.join(
            '<figure><a href="%s" class="wl-img"><img loading="lazy" src="%s" alt="%s"></a>%s</figure>' % (
                html.escape(f), html.escape(s), html.escape(c), ('<figcaption>%s</figcaption>' % html.escape(c)) if c else '')
            for s, f, c in gal)))
        gal.clear()
    for it in items:
        if it[0] == 'img':
            gal.append(it[1:]); continue
        flush()
        if it[0] == 'h': out.append('<%s>%s</%s>' % (it[1], html.escape(it[2]), it[1]))
        elif it[0] == 'p': out.append('<p>%s</p>' % it[1])
        elif it[0] in ('list', 'table'): out.append(it[1])
        elif it[0] == 'embed': out.append('<div class="wl-embed"><iframe src="%s" loading="lazy" allowfullscreen></iframe></div>' % html.escape(it[1]))
    flush()
    return '\n'.join(out)

pages = {p['id']: p for p in json.load(open(os.path.join(BK, 'api', 'pages.json'), encoding='utf-8'))}
result = []
for pid, slug in KEEP.items():
    p = pages[pid]
    raw = open(os.path.join(BK, 'html', 'pages', f'{pid}.html'), encoding='utf-8').read()
    a = raw.find('class="page_title_wrapper"'); a = raw.find('</h1>', a) + 5 if a >= 0 else raw.find('<body')
    b = raw.find('class="footer_bar', a); b = raw.rfind('<div', 0, b)
    region = BeautifulSoup(raw[a:b], 'html.parser')
    items = []; walk(region, items, set())
    body = render(items)
    body = re.sub(r'https?://(?:www\.|new\.)?gwmpa\.org/wp-content/', 'https://www.gwmpa.org/wp-content/', body)
    body = re.sub(r'https?://(?:www\.|new\.)?gwmpa\.org/\?page_id=(\d+)', lambda m: ('/?pagename=' + KEEP[int(m.group(1))]) if int(m.group(1)) in KEEP else m.group(0), body)
    imgs = sorted(set(re.findall(r'https?://www\.gwmpa\.org/wp-content/uploads/[^"\s)]+', body)))
    result.append(dict(old_id=pid, slug=slug, title=html.unescape(p['title']['rendered']), date=p['date'], content=body, images=imgs))
    print(pid, slug, len(body), 'chars,', len(imgs), 'images')
json.dump(result, open(OUT, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
