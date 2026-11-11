from pathlib import Path
from html import escape
from hashlib import sha256
import json
from PIL import Image, ImageDraw, ImageFont

WORK=Path('.book-work/swm-v1-7e813050a033')
ASSETS=WORK/'book/en/assets'
ASSETS.mkdir(parents=True,exist_ok=True)
FONT='/usr/share/fonts/liberation-sans-fonts/LiberationSans-Regular.ttf'
INK='#172b33'; STROKE='#546e7a'
receipts=[]

def svg(name,width,height,nodes,edges,labels,source):
    parts=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" lang="en" role="img"><title>{escape(name)}</title><rect width="100%" height="100%" fill="white"/><defs><marker id="arrow" markerWidth="12" markerHeight="10" refX="10" refY="5" orient="auto" markerUnits="strokeWidth"><path d="M0 0 L10 5 L0 10 Z" fill="{STROKE}"/></marker></defs>']
    for edge in edges:parts.append(f'<path d="{edge}" fill="none" stroke="{STROKE}" stroke-width="2.5" marker-end="url(#arrow)"/>')
    for x,y,w,h,lines in nodes:
        parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="28" fill="white" stroke="{STROKE}" stroke-width="2.5"/>')
        size=30
        while max(ImageFont.truetype(FONT,size).getlength(line) for line in lines)>w-28:size-=1
        for i,line in enumerate(lines):
            baseline=y+h/2+(i-(len(lines)-1)/2)*size*1.12+size*.34
            parts.append(f'<text x="{x+w/2}" y="{baseline:.2f}" text-anchor="middle" font-family="Liberation Sans, Arial, sans-serif" font-size="{size}" fill="{INK}">{escape(line)}</text>')
    for x,y,text,size in labels:parts.append(f'<text x="{x}" y="{y}" font-family="Liberation Sans, Arial, sans-serif" font-size="{size}" fill="{INK}">{escape(text)}</text>')
    parts.append('</svg>')
    destination=ASSETS/f'{name}.svg';destination.write_text('\n'.join(parts)+'\n')
    receipts.append({'source':f'assets/{source}','localized':f'assets/{destination.name}','sourceSha256':sha256((WORK/'book/ro/assets'/source).read_bytes()).hexdigest(),'localizedSha256':sha256(destination.read_bytes()).hexdigest(),'nodes':[n[4] for n in nodes],'edges':edges,'edgeLabels':[l[2] for l in labels]})

svg('diagram-1-architecture',1668,622,[
 (421,20,352,85,['Message or observation']),(20,178,248,85,['World pattern']),
 (413,178,369,85,['Formalization and validation']),(132,360,294,85,['World instance']),
 (724,360,388,85,['Agenda and interpreters']),(763,518,310,85,['Response and decision']),
 (1240,518,410,85,['Executor and external system'])],
 ['M597 105 L597 177','M268 220 L412 220','M266 360 Q245 285 411 246',
  'M578 263 Q540 330 426 374','M268 262 Q430 340 724 383','M426 403 L723 403',
  'M724 432 Q565 450 427 430','M918 445 L918 517','M1055 518 Q1215 430 1120 348 Q1090 335 1070 330 L677 106',
  'M1073 560 L1239 560','M1414 518 Q1120 180 759 105'],
 [(296,207,'conditions',24),(276,318,'context',24),(425,318,'operations',24),(565,318,'adopted change',24),
  (455,390,'affected dependencies',23),(465,428,'verified results',23),(1075,318,'clarification',24),(1270,318,'observed result',24),(1103,547,'command',24)],'swm_html_73dfcdd8.png')

svg('diagram-2-interpretation',1019,604,[
 (668,20,281,85,['Message and context']),(379,164,360,85,['Candidate formalizations']),
 (27,332,345,85,['Checking the instance']),(609,332,248,85,['World pattern']),
 (20,500,359,85,['Adopted interpretation']),(510,500,197,85,['Clarification'])],
 ['M734 105 L629 163','M470 249 L284 331','M609 374 L373 374','M199 417 L199 499',
  'M304 417 L517 499','M707 524 Q1030 435 834 106'],
 [(387,360,'relations and conditions',20),(200,464,'sufficient support',23),(450,464,'relevant ambiguity',23),(915,296,'answer',23)],'swm_html_83aa8833.png')

svg('diagram-3-connected-worlds',1288,530,[
 (20,20,350,104,['Bicycle preparation','Estimate for B17']),(433,20,364,104,["Customer’s goal",'What they want to try']),
 (866,20,337,104,['Research','Corrected measurement']),(441,226,338,104,['Scheduling the visit','Unit and time slot']),
 (842,226,414,104,['Presenting the product','Supported claims']),(600,407,440,104,['Explained options','Trial and information offered'])],
 ['M220 124 Q280 220 440 253','M615 124 L610 225','M1034 124 L1034 225',
  'M669 330 L761 406','M973 330 L879 406'],
 [(280,181,'conditional availability',23),(617,181,'appropriate alternative',23),(1050,181,'justification revision',22)],'swm_html_1b72d131.png')

# Same authored composition as the original cover; English typography is newly drawn.
im=Image.new('RGB',(1200,1800),'#eee8dc');d=ImageDraw.Draw(im)
bold='/usr/share/fonts/redhat/RedHatDisplay-Bold.otf';regular='/usr/share/fonts/redhat/RedHatDisplay-Regular.otf'
f=lambda n:ImageFont.truetype(bold,n)
fr=lambda n:ImageFont.truetype(regular,n)
ink='#123e43';muted='#4d6767'
d.text((92,85),'SWM',font=f(34),fill=muted)
for y,t in [(200,'SYMBOLIC'),(315,'WORLD'),(430,'MODELS')]:d.text((85,y),t,font=f(100),fill=ink)
d.text((92,615),'How an AI system preserves',font=fr(36),fill=ink)
d.text((92,665),'the meaning of a situation',font=fr(36),fill=ink)
for box,color in [((125,860,700,1435),'#c8d7cf'),((485,995,1060,1570),'#aac6c3'),((330,790,905,1365),'#dfbda2')]:d.ellipse(box,fill=color)
pts=[(340,1060),(510,970),(700,1130),(475,1280),(820,1360),(625,1450)]
for a,b in [(0,1),(1,2),(0,3),(2,3),(2,4),(3,5),(4,5)]:d.line([pts[a],pts[b]],fill=ink,width=8)
for i,(x,y) in enumerate(pts):d.ellipse((x-20,y-20,x+20,y+20),fill='#d56639' if i==2 else ink)
d.text((92,1650),'PATTERNS · INSTANCES · REASONING',font=f(30),fill=ink)
d.text((92,1710),'FOURTH EDITION',font=fr(25),fill=muted)
d.rectangle((0,0,1199,29),fill=ink);d.rectangle((0,1770,1199,1799),fill=ink)
im.save(ASSETS/'pdf-cover.png')
job=WORK/'translations/en/full/manifest.json';manifest=json.loads(job.read_text());manifest['localizedAssets']=[{k:v for k,v in a.items() if k in {'source','localized','sourceSha256','localizedSha256'}} for a in receipts];job.write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
p=WORK/'book/manifest.json';manifest=json.loads(p.read_text());manifest['pdfCover']={'en':'en/assets/pdf-cover.png','ro':'ro/cover.png'};p.write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
(WORK/'repairs/pdf-cover-and-diagrams/asset-review.json').write_text(json.dumps({'language':'en','sourceDiagramsPreserved':True,'translationMethod':'Direct active-LLM review of the three source diagrams and their chapter context; native SVG reconstruction preserves node identities, edge direction and labels. No OCR or external translator.','diagrams':receipts,'cover':'New English typography using the existing authored composition; Romanian source cover unchanged.'},ensure_ascii=False,indent=2)+'\n')
print('Generated three localized SVG diagrams and the English PDF cover; recorded hashes in stable translation manifest.')
