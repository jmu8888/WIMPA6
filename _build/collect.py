# Collect winner entries (no contact info) from the past-winners folders into entries.json
import os, re, json, glob, openpyxl, difflib
ROOT = r"E:\Data2020\Community\2026第五届《华盛顿手机摄影大赛》\历届获奖作品"
AW = {'1等奖':'gold','一等奖':'gold','2等奖':'silver','二等奖':'silver','3等奖':'bronze','三等奖':'bronze','优秀奖':'hm'}
def norm(s): return re.sub(r'[\W_]+','',str(s or '')).lower()
def sim(a,b):
    a,b=norm(a),norm(b)
    if a and b and (a in b or b in a): return 1.0
    return difflib.SequenceMatcher(None,a,b).ratio()
def series_base(fn):
    b=os.path.splitext(fn)[0]
    b=re.sub(r'_\d+(\(\d+\))?$','',b)
    return b
entries=[]
def add(ed,cat,aw,title,name,state,files,desc=None):
    entries.append(dict(edition=ed,category=cat,award=aw,title=(title or '').strip(),name=(name or '').strip(),state=(state or '').strip(),desc=(desc or '').strip(),files=files))

# ---- 5th
cats5={'命题-单图':'everyday-single','命题-组图':'everyday-series','人物纪实':'people','自然风光':'nature','艺术创意':'art'}
for zh,cat in cats5.items():
    d=os.path.join(ROOT,'第五届获奖作品',zh)
    rows=[]
    for x in glob.glob(os.path.join(d,'*.xlsx')):
        ws=openpyxl.load_workbook(x).active
        for r in ws.iter_rows(values_only=True):
            if r[0] and r[0]!='作品名称': rows.append(dict(title=str(r[0]),desc=r[1],award=AW.get(r[3]),name=r[4],state=r[5]))
    groups={}
    for awdir in os.listdir(d):
        p=os.path.join(d,awdir)
        if not os.path.isdir(p): continue
        for f in sorted(os.listdir(p)):
            if not f.lower().endswith('.jpg'): continue
            key=series_base(f) if cat=='everyday-series' else os.path.splitext(f)[0]
            groups.setdefault((AW[awdir],key),[]).append(os.path.join(p,f))
    used=set()
    for (aw,key),files in groups.items():
        cand=[i for i,r in enumerate(rows) if r['award']==aw and i not in used] or [i for i in range(len(rows)) if i not in used]
        best=max(cand,key=lambda i: sim(rows[i]['title'],key),default=None)
        sc=sim(rows[best]['title'],key) if best is not None else 0
        if sc<0.6: print('NOMATCH',cat,aw,key,'~',rows[best]['title'] if best is not None else None,round(sc,2)); r={}
        else: used.add(best); r=rows[best]
        add(5,cat,aw,key,r.get('name'),r.get('state'),files,r.get('desc'))

# ---- 1st (no categories)
for awdir in ['一等奖','二等奖','三等奖']:
    for sub in os.listdir(os.path.join(ROOT,'第一届获奖作品',awdir)):
        p=os.path.join(ROOT,'第一届获奖作品',awdir,sub)
        for f in os.listdir(p):
            add(1,'open',AW[awdir],os.path.splitext(f)[0],sub.split('-',1)[1],'',[os.path.join(p,f)])
# ---- 2nd
cats2={'人物纪实':'people','自然风光':'nature','艺术创意类':'art'}
for zh,cat in cats2.items():
    d=os.path.join(ROOT,'第二届获奖作品',zh)
    ws=openpyxl.load_workbook(glob.glob(os.path.join(d,'*.xlsx'))[0]).active
    byid={str(r[0]):r for r in list(ws.iter_rows(values_only=True))[1:] if r[0]}
    for awdir in ['一等奖','二等奖','三等奖']:
        for f in os.listdir(os.path.join(d,awdir)):
            i,t=os.path.splitext(f)[0].split('_',1); r=byid.get(i)
            add(2,cat,AW[awdir],r[2] if r else t,r[6] if r else '',r[7] if r else '',[os.path.join(d,awdir,f)],r[3] if r else None)
# ---- 3rd
cats3={'人物、纪实类':'people','命题《旅途》':'theme-journey','自然、风光类':'nature','艺术、创意类':'art'}
for zh,cat in cats3.items():
    for awdir in ['一等奖','二等奖','三等奖']:
        b=os.path.join(ROOT,'第三届获奖作品',zh,awdir)
        for sub in os.listdir(b):
            for f in os.listdir(os.path.join(b,sub)):
                add(3,cat,AW[awdir],os.path.splitext(f)[0],sub.split('-',1)[1],'',[os.path.join(b,sub,f)])
# ---- 4th
cats4={'人物纪实类':'people','命题生命单图':'theme-life-single','命题生命组图':'theme-life-series','自然风光类':'nature','艺术创意类':'art'}
for zh,cat in cats4.items():
    for awdir in ['一等奖','二等奖','三等奖']:
        b=os.path.join(ROOT,'第四届获奖作品',zh,awdir); groups={}
        for f in sorted(os.listdir(b)):
            s=os.path.splitext(f)[0]; name=''
            m=re.match(r'^(\d+)_(?:(\d+)_)?(.+)$',s)
            if m: key=m.group(3); gid=m.group(1)
            else:
                parts=s.split('_'); name=parts[0]; key=parts[1] if len(parts)>1 else s
                key=re.sub(r'-\d+$','',key); gid=name+key
            groups.setdefault(gid,dict(key=key,name=name,files=[]))['files'].append(os.path.join(b,f))
        for g in groups.values(): add(4,cat,AW[awdir],g['key'],g['name'],'',g['files'])
json.dump(entries,open(os.path.join(os.path.dirname(__file__),'entries.json'),'w',encoding='utf-8'),ensure_ascii=False,indent=1)
from collections import Counter
print(Counter((e['edition'],e['award']) for e in entries))
