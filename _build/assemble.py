import os
H=os.path.dirname(os.path.abspath(__file__)); S=os.path.dirname(H)
head=open(os.path.join(H,'head.html'),encoding='utf-8').read()
titles={'index':'6th WIMPA · Washington International Mobile Photography Awards','winners':'5th WIMPA Winners · 6th WIMPA','archive':'Past Winners · 6th WIMPA','enter':'Categories & Rules · 6th WIMPA','jury':'Jury · 6th WIMPA','about':'About · 6th WIMPA'}
for p,t in titles.items():
    body=open(os.path.join(H,p+'.body.html'),encoding='utf-8').read()
    open(os.path.join(S,p+'.html'),'w',encoding='utf-8').write(head.replace('__TITLE__',t.replace('&','&amp;'))+body)
print('ok')

# Chinese pages -> zh/
zh = {'index':'第六届华盛顿国际手机摄影大赛 · 6th WIMPA','winners':'第五届获奖作品 · 第六届 WIMPA','archive':'往届获奖作品 · 第六届 WIMPA','enter':'参赛类别与规则 · 第六届 WIMPA','jury':'评委 · 第六届 WIMPA','about':'关于大赛 · 第六届 WIMPA'}
os.makedirs(os.path.join(S,'zh'),exist_ok=True)
zhead=open(os.path.join(H,'zh','head.html'),encoding='utf-8').read()
for p,t in zh.items():
    body=open(os.path.join(H,'zh',p+'.body.html'),encoding='utf-8').read()
    open(os.path.join(S,'zh',p+'.html'),'w',encoding='utf-8').write(zhead.replace('__TITLE__',t)+body)
print('zh ok')
