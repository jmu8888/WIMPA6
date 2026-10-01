import os
H=os.path.dirname(os.path.abspath(__file__)); S=os.path.dirname(H)
head=open(os.path.join(H,'head.html'),encoding='utf-8').read()
titles={'index':'6th WIMPA · Washington International Mobile Photography Awards','winners':'5th WIMPA Winners · 6th WIMPA','archive':'Past Winners · 6th WIMPA','enter':'Categories & Rules · 6th WIMPA','jury':'Jury · 6th WIMPA','about':'About · 6th WIMPA'}
for p,t in titles.items():
    body=open(os.path.join(H,p+'.body.html'),encoding='utf-8').read()
    open(os.path.join(S,p+'.html'),'w',encoding='utf-8').write(head.replace('__TITLE__',t.replace('&','&amp;'))+body)
print('ok')
