import os
H=os.path.dirname(os.path.abspath(__file__)); S=os.path.dirname(H)
head=open(os.path.join(H,'head.html'),encoding='utf-8').read()
titles={'index':'6th WMPA · Washington International Mobile Photography Awards','winners':'5th WMPA Winners · 6th WMPA','archive':'Winners’ Gallery · 6th WMPA','enter':'Categories & Rules · 6th WMPA','jury':'Jury · 6th WMPA','about':'About · 6th WMPA','ceremony':'Awards Ceremony · 6th WMPA'}
for p,t in titles.items():
    body=open(os.path.join(H,p+'.body.html'),encoding='utf-8').read()
    open(os.path.join(S,p+'.html'),'w',encoding='utf-8').write(head.replace('__TITLE__',t.replace('&','&amp;'))+body)
print('ok')

# Chinese pages -> zh/
zh = {'index':'第六届华盛顿国际手机摄影大赛 · 6th WMPA','winners':'第五届获奖作品 · 第六届 WMPA','archive':'历届获奖作品 · 第六届 WMPA','enter':'参赛类别与规则 · 第六届 WMPA','jury':'评委 · 第六届 WMPA','about':'关于大赛 · 第六届 WMPA','ceremony':'颁奖典礼 · 第六届 WMPA'}
os.makedirs(os.path.join(S,'zh'),exist_ok=True)
zhead=open(os.path.join(H,'zh','head.html'),encoding='utf-8').read()
for p,t in zh.items():
    body=open(os.path.join(H,'zh',p+'.body.html'),encoding='utf-8').read()
    open(os.path.join(S,'zh',p+'.html'),'w',encoding='utf-8').write(zhead.replace('__TITLE__',t)+body)
print('zh ok')
