#!/usr/bin/env python3
"""Parse the supplied Word file into an ordered block list (source.json).
Each block: {i, k:'p'|'t', text, ...}. Text is the exact concatenation of w:t runs of the paragraph.
Run: python3 -I parse_docx.py  (reads source/sawti-arabi-source.docx, writes data/source.json)
"""
import json, re, sys, zipfile, os
from lxml import etree
HERE=os.path.dirname(os.path.abspath(__file__))
W='http://schemas.openxmlformats.org/wordprocessingml/2006/main'
R='http://schemas.openxmlformats.org/officeDocument/2006/relationships'
A='http://schemas.openxmlformats.org/drawingml/2006/main'
V='urn:schemas-microsoft-com:vml'
def q(ns,t): return '{%s}%s'%(ns,t)
z=zipfile.ZipFile(os.path.join(HERE,'source','sawti-arabi-source.docx'))
doc=etree.fromstring(z.read('word/document.xml'))
rels={e.get('Id'):(e.get('Target'),e.get('TargetMode')) for e in etree.fromstring(z.read('word/_rels/document.xml.rels'))}
body=doc.find(q(W,'body'))

def ptext(p):
    out=[]
    for el in p.iter():
        if el.tag==q(W,'t'): out.append(el.text or '')
        elif el.tag==q(W,'tab'): out.append('\t')
        elif el.tag==q(W,'br'): out.append('\n')
    return ''.join(out)

def pimgs(p):
    res=[]
    for b in p.iter(q(A,'blip')):
        t=rels.get(b.get(q(R,'embed')))
        if t: res.append(t[0])
    for im in p.iter(q(V,'imagedata')):
        t=rels.get(im.get(q(R,'id')))
        if t: res.append(t[0])
    return res

def pfmt(p):
    rs=p.findall('.//'+q(W,'r'))
    b=u=False; col=set()
    for r in rs:
        pr=r.find(q(W,'rPr'))
        if pr is None: continue
        if pr.find(q(W,'b')) is not None: b=True
        if pr.find(q(W,'u')) is not None: u=True
        c=pr.find(q(W,'color'))
        if c is not None: col.add(c.get(q(W,'val')))
    ppr=p.find(q(W,'pPr'))
    num=ppr is not None and ppr.find(q(W,'numPr')) is not None
    link=[rels[h.get(q(R,'id'))][0] for h in p.iter(q(W,'hyperlink')) if h.get(q(R,'id')) in rels]
    return dict(bold=b,underline=u,colors=sorted(col),listed=num,links=link)

def cell_text(tc):
    return '\n'.join(ptext(p) for p in tc.findall(q(W,'p')))

def table(tbl):
    bidi=tbl.find('.//'+q(W,'bidiVisual')) is not None
    rows=[]
    for tr in tbl.findall(q(W,'tr')):
        cells=[]
        for tc in tr.findall(q(W,'tc')):
            pr=tc.find(q(W,'tcPr')); span=1; vm=None
            if pr is not None:
                gs=pr.find(q(W,'gridSpan'))
                if gs is not None: span=int(gs.get(q(W,'val')))
                v=pr.find(q(W,'vMerge'))
                if v is not None: vm=v.get(q(W,'val')) or 'cont'
            cells.append(dict(text=cell_text(tc),span=span,vmerge=vm,imgs=[i for p in tc.findall(q(W,'p')) for i in pimgs(p)]))
        rows.append(cells)
    return dict(bidi=bidi,rows=rows)

blocks=[]
for i,el in enumerate(body):
    tag=el.tag.split('}')[1]
    if tag=='p':
        d=dict(i=i,k='p',text=ptext(el),imgs=pimgs(el)); d.update(pfmt(el)); blocks.append(d)
    elif tag=='tbl':
        d=dict(i=i,k='t'); d.update(table(el)); blocks.append(d)
json.dump(blocks,open(os.path.join(HERE,'data','source.json'),'w',encoding='utf8'),ensure_ascii=False,indent=0)
print(len(blocks),'blocks;',sum(1 for b in blocks if b['k']=='t'),'tables')
