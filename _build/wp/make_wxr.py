# Build the WordPress import file (WXR) for the merged site:
# new English and Chinese WIMPA pages, the converted pages from the earlier site, two old news posts, and the menus.
import json, os, re, html
from datetime import datetime, timezone

H = os.path.dirname(os.path.abspath(__file__))
B = os.path.dirname(H)                      # _build
BK = r"G:\2027第六届手机摄影大赛\gwmpa-backup"
IMG = 'https://jmu8888.github.io/WIMPA6/images/'
OUT = os.path.join(H, 'wimpa6-content.xml')
NOW = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')

# file in the static site -> page slug
SLUG = {'index': None, 'winners': 'winners', 'archive': 'past-winners', 'enter': 'rules', 'jury': 'jury', 'about': 'about'}
KIND = {'index': 'home', 'winners': 'winners', 'archive': 'archive', 'enter': 'enter', 'jury': 'jury', 'about': 'about'}
TITLES = {
    'en': {'index': '6th WIMPA Home', 'winners': '5th WIMPA Winners', 'archive': 'Past Winners', 'enter': 'Categories & Rules', 'jury': 'Jury', 'about': 'About WIMPA'},
    'zh': {'index': '中文', 'winners': '第五届获奖作品', 'archive': '往届获奖作品', 'enter': '参赛类别与规则', 'jury': '评委', 'about': '关于大赛'},
}

def page_url(lang, f, anchor=''):
    s = SLUG[f]
    if lang == 'en':
        return ('/' if s is None else '/?pagename=' + s) + anchor
    return '/?pagename=zh' + ('' if s is None else '/' + s) + anchor

def body_of(lang, f):
    src = os.path.join(B, 'zh' if lang == 'zh' else '', f + '.body.html')
    s = open(src, encoding='utf-8').read()
    s = re.sub(r'^\s*<body[^>]*>', '', s)
    s = re.sub(r'<script[^>]*></script>\s*', '', s)
    s = re.sub(r'</body>\s*</html>\s*$', '', s)
    s = re.sub(r'(?:\.\./)?images/', IMG, s)
    s = re.sub(r'href="(index|winners|archive|enter|jury|about)\.html(#[\w-]+)?"', lambda m: 'href="%s"' % page_url(lang, m.group(1), m.group(2) or ''), s)
    return s.strip()

def cdata(s):
    return '<![CDATA[' + s.replace(']]>', ']]]]><![CDATA[>') + ']]>'

items, nid = [], [9000]
def new_id():
    nid[0] += 1; return nid[0]

def add_page(title, slug, content, parent=0, meta=None, order=0, date=NOW, ptype='page'):
    pid = new_id()
    items.append(dict(id=pid, title=title, slug=slug, content=content, parent=parent, meta=meta or {}, order=order, date=date, type=ptype))
    return pid

# ---- new WIMPA pages
ids = {'en': {}, 'zh': {}}
zh_root = add_page(TITLES['zh']['index'], 'zh', '<!-- wp:html -->\n' + body_of('zh', 'index') + '\n<!-- /wp:html -->',
                   meta={'wimpa_page': 'home', 'wimpa_pair': 'home'})
ids['zh']['index'] = zh_root
ids['en']['index'] = add_page(TITLES['en']['index'], 'wimpa-home', '<!-- wp:html -->\n' + body_of('en', 'index') + '\n<!-- /wp:html -->',
                              meta={'wimpa_page': 'home', 'wimpa_pair': 'zh'})
for k, f in enumerate(['winners', 'archive', 'enter', 'jury', 'about']):
    ids['en'][f] = add_page(TITLES['en'][f], SLUG[f], '<!-- wp:html -->\n' + body_of('en', f) + '\n<!-- /wp:html -->',
                            meta={'wimpa_page': KIND[f], 'wimpa_pair': 'zh/' + SLUG[f]}, order=k + 1)
    ids['zh'][f] = add_page(TITLES['zh'][f], SLUG[f], '<!-- wp:html -->\n' + body_of('zh', f) + '\n<!-- /wp:html -->',
                            parent=zh_root, meta={'wimpa_page': KIND[f], 'wimpa_pair': SLUG[f]}, order=k + 1)

# ---- pages from the earlier site
legacy = {}
for p in json.load(open(os.path.join(H, 'legacy.json'), encoding='utf-8')):
    legacy[p['slug']] = add_page(p['title'], p['slug'], '<!-- wp:html -->\n' + p['content'] + '\n<!-- /wp:html -->', date=p['date'].replace('T', ' '))

# ---- the two real news posts from 2023
for post in json.load(open(os.path.join(BK, 'api', 'posts.json'), encoding='utf-8')):
    if post['id'] not in (5795, 5785):
        continue
    c = re.sub(r'https?://(?:www\.|new\.)?gwmpa\.org/wp-content/', 'https://www.gwmpa.org/wp-content/', post['content']['rendered'])
    add_page(html.unescape(post['title']['rendered']), post['slug'], '<!-- wp:html -->\n' + c + '\n<!-- /wp:html -->', date=post['date'].replace('T', ' '), ptype='post')

# ---- menus
menus = {'wimpa-main': 'WIMPA Main', 'wimpa-zh': 'WIMPA 中文'}
def M(menu, label, target, parent=0, order=0):
    """target: page id, or an absolute/relative URL."""
    mid = new_id()
    meta = {'_menu_item_menu_item_parent': str(parent), '_menu_item_target': '', '_menu_item_classes': '', '_menu_item_xfn': ''}
    if isinstance(target, int):
        meta.update({'_menu_item_type': 'post_type', '_menu_item_object': 'page', '_menu_item_object_id': str(target), '_menu_item_url': ''})
    else:
        meta.update({'_menu_item_type': 'custom', '_menu_item_object': 'custom', '_menu_item_object_id': str(mid), '_menu_item_url': target})
    items.append(dict(id=mid, title=label, slug='menu-item-%d' % mid, content='', parent=0, meta=meta, order=order, date=NOW, type='nav_menu_item', menu=menu))
    return mid

o = iter(range(1, 999))
E, L = ids['en'], legacy
m = M('wimpa-main', '5th Winners', E['winners'], order=next(o))
for t, s in [('2025 Awards (5th)', '2025-awards'), ('Theme · Photo Series', '2025-awards-theme-series'), ('Theme · Single Photo', '2025-awards-theme-single'),
             ('People & Documentary', '2025-awards-people'), ('Art & Creativity', '2025-awards-art'), ('Nature & Landscape', '2025-awards-nature'),
             ('Winners List of the 5th Awards', '5th-winners-list'), ('2025 Judges', '2025-judges')]:
    M('wimpa-main', t, L[s], m, next(o))
m = M('wimpa-main', 'Past Winners', E['archive'], order=next(o))
M('wimpa-main', 'Past Winners Gallery', E['archive'], m, next(o))
M('wimpa-main', 'Previous Awards', L['previous-awards'], m, next(o))
for year, sub in [('2024 Awards (4th)', [('awards-2024', None), ('2024-awards-theme-series', 'Theme Life · Series'), ('2024-awards-theme-single', 'Theme Life · Single'),
                                         ('2024-awards-people', 'People & Documentary'), ('2024-awards-art', 'Art & Creativity'), ('2024-awards-nature', 'Nature & Landscape'),
                                         ('4th-winners-list', 'Winners List'), ('judges-2024', '2024 Judges')]),
                  ('2023 Awards (3rd)', [('awards-2023', None), ('2023-awards-trip', 'Theme: The Journey'), ('awards-2023-landscape', 'Landscape'),
                                         ('awards-2023-art', 'Art'), ('awards-2023-documentary', 'Documentary'), ('3rd-winners-list', 'Winners List')]),
                  ('2022 Awards (2nd)', [('2022-awards', None), ('2022-awards-landscape', 'Landscape'), ('2022-awards-art', 'Art'), ('2022-awards-documentary', 'Documentary')]),
                  ('2021 Awards (1st)', [('2021-awards', None), ('2021-awards-landscape', 'Landscape'), ('2021-awards-art', 'Art'), ('2021-awards-documentary', 'Documentary')])]:
    y = M('wimpa-main', year, L[sub[0][0]], m, next(o))
    for s, t in sub[1:]:
        M('wimpa-main', t, L[s], y, next(o))
M('wimpa-main', 'Categories & Rules', E['enter'], order=next(o))
M('wimpa-main', 'Jury', E['jury'], order=next(o))
m = M('wimpa-main', 'About', E['about'], order=next(o))
for t, s in [('About WIMPA', None), ('About Us', 'about-us'), ('Co-Organizers', 'co-organizer-list'), ('Sponsors', 'sponsors'), ('Donation', 'donation'), ('View / Submit Entries', 'view-submit')]:
    M('wimpa-main', t, E['about'] if s is None else L[s], m, next(o))

Z = ids['zh']; o = iter(range(1, 999))
m = M('wimpa-zh', '第五届获奖作品', Z['winners'], order=next(o))
for t, s in [('第五届获奖作品（原页面）', '2025-awards'), ('第五届获奖名单', '5th-winners-list'), ('2025 评委', '2025-judges')]:
    M('wimpa-zh', t, L[s], m, next(o))
m = M('wimpa-zh', '往届获奖作品', Z['archive'], order=next(o))
for t, s in [('往届作品图库', None), ('往届摄影大赛', 'previous-awards'), ('第四届（2024）', 'awards-2024'), ('第三届（2023）', 'awards-2023'), ('第二届（2022）', '2022-awards'), ('首届（2021）', '2021-awards')]:
    M('wimpa-zh', t, Z['archive'] if s is None else L[s], m, next(o))
M('wimpa-zh', '参赛类别与规则', Z['enter'], order=next(o))
m = M('wimpa-zh', '评委', Z['jury'], order=next(o))
M('wimpa-zh', '第六届评委', Z['jury'], m, next(o)); M('wimpa-zh', '评委介绍（往届）', L['judges-cn'], m, next(o))
m = M('wimpa-zh', '关于大赛', Z['about'], order=next(o))
for t, s in [('关于大赛', None), ('协办单位', 'co-organizer-list'), ('赞助商', 'sponsors'), ('捐款支持', 'donation'), ('查看／提交作品', 'view-submit')]:
    M('wimpa-zh', t, Z['about'] if s is None else L[s], m, next(o))

# ---- write WXR 1.2
def item_xml(it):
    meta = ''.join('<wp:postmeta><wp:meta_key>%s</wp:meta_key><wp:meta_value>%s</wp:meta_value></wp:postmeta>' % (k, cdata(v)) for k, v in it['meta'].items())
    cat = '<category domain="nav_menu" nicename="%s">%s</category>' % (it['menu'], cdata(menus[it['menu']])) if it.get('menu') else ''
    return f'''<item>
<title>{cdata(it['title'])}</title>
<dc:creator>{cdata('admin')}</dc:creator>
<content:encoded>{cdata(it['content'])}</content:encoded>
<excerpt:encoded>{cdata('')}</excerpt:encoded>
<wp:post_id>{it['id']}</wp:post_id>
<wp:post_date>{cdata(it['date'])}</wp:post_date>
<wp:post_date_gmt>{cdata(it['date'])}</wp:post_date_gmt>
<wp:comment_status>{cdata('closed')}</wp:comment_status>
<wp:ping_status>{cdata('closed')}</wp:ping_status>
<wp:post_name>{cdata(it['slug'])}</wp:post_name>
<wp:status>{cdata('publish')}</wp:status>
<wp:post_parent>{it['parent']}</wp:post_parent>
<wp:menu_order>{it['order']}</wp:menu_order>
<wp:post_type>{cdata(it['type'])}</wp:post_type>
<wp:post_password>{cdata('')}</wp:post_password>
<wp:is_sticky>0</wp:is_sticky>
{cat}{meta}
</item>'''

terms = ''.join(f'<wp:term><wp:term_id>{i + 1}</wp:term_id><wp:term_taxonomy>{cdata("nav_menu")}</wp:term_taxonomy><wp:term_slug>{cdata(s)}</wp:term_slug><wp:term_name>{cdata(n)}</wp:term_name></wp:term>'
                for i, (s, n) in enumerate(menus.items()))
xml = f'''<?xml version="1.0" encoding="UTF-8" ?>
<rss version="2.0" xmlns:excerpt="http://wordpress.org/export/1.2/excerpt/" xmlns:content="http://purl.org/rss/1.0/modules/content/"
 xmlns:wfw="http://wellformedweb.org/CommentAPI/" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:wp="http://wordpress.org/export/1.2/">
<channel>
<title>WIMPA</title>
<link>https://www.gwmpa.org</link>
<description>Washington International Mobile Photography Awards</description>
<language>en-US</language>
<wp:wxr_version>1.2</wp:wxr_version>
<wp:base_site_url>https://www.gwmpa.org</wp:base_site_url>
<wp:base_blog_url>https://www.gwmpa.org</wp:base_blog_url>
<wp:author><wp:author_id>1</wp:author_id><wp:author_login>{cdata('admin')}</wp:author_login><wp:author_email>{cdata('')}</wp:author_email><wp:author_display_name>{cdata('admin')}</wp:author_display_name></wp:author>
{terms}
{''.join(item_xml(it) for it in items)}
</channel>
</rss>
'''
open(OUT, 'w', encoding='utf-8').write(xml)
print(len(items), 'items ->', OUT, round(len(xml) / 1e6, 2), 'MB')
