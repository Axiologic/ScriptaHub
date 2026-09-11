#!/usr/bin/env python3
"""Install the editor-approved generated artworks as polished ScriptaHub covers."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import json, shutil, textwrap

ROOT = Path(__file__).resolve().parents[1]
GENERATED = Path('/home/salboaie/.codex/generated_images/01a08f4c-889b-7011-8c77-d8bb3c133772')
ARCHIVE = ROOT / '.book-work/intake-20260911/generated-cover-art'
FONT = ROOT / '.book-work/.pdf-venv/lib/python3.14/site-packages/reportlab/fonts/VeraBd.ttf'

ITEMS = [
 ('The Architecture of Reality','exec-74f8cd87-1bdf-466a-b7e2-8506dcbe7890.png'),
 ('The Art of Knowing What Matters','exec-d8832bb6-b0c0-4105-8eb5-dc21760fffd7.png'),
 ('The Book Sends No Notifications','exec-dd692a4a-44b7-46e0-915f-ff7b9cba98bc.png'),
 ('From Rules, Worlds','exec-85ebf22c-0ecb-470b-937c-5befa27c7387.png'),
 ('Beauty: The Anatomy of Fascination','exec-c0f402fc-1b77-403e-9902-44d29121372a.png'),
 ('One More Try','exec-9e955b64-5106-48f9-a3c8-7715011904a3.png'),
 ('Between Faith and Evidence','exec-15af6a48-6104-4c02-be7a-b63e85904b11.png'),
 ('Freedom and Its Price','exec-5087fd51-af31-4f7f-9dbb-c5c6bb21a0ac.png'),
 ('The World Does Not Read Equations','exec-f2953118-f4f7-41ce-ba0b-5169e8c9fd30.png'),
 ('Machines of Understanding Through Circuits','exec-91f10076-e776-4c1b-bba5-98cb43e05f5d.png'),
 ('Meta-Rational Pragmatics','exec-af4fe323-063b-4623-b141-78a7dc50cc1b.png'),
 ('Novelty That Resembles the Past','exec-b4f50ae9-feb3-40e4-ac2c-ee323f668df7.png'),
 ('Responsibility','exec-e3de6981-eb62-486d-b43e-cbd706504912.png'),
 ('The Right to Copy','exec-08522dd9-e847-450d-b29e-60554bba4d5f.png'),
 ('The Network of Intent','exec-ec24a3c1-da67-4180-b9f1-885d60b3a89d.png'),
 ('The Last Naive Person','exec-a17de766-e604-4049-b6f2-c8b9f5bac7a6.png'),
 ('Before Explanation','exec-975fc805-2842-419d-a344-213695403570.png'),
]

def wrap(draw, title, font, width):
    words, lines, line = title.split(), [], ''
    for word in words:
        candidate = f'{line} {word}'.strip()
        if line and draw.textbbox((0,0), candidate, font=font)[2] > width:
            lines.append(line); line = word
        else: line = candidate
    lines.append(line)
    return lines

manifests = {}
for p in (ROOT/'docs/books').glob('**/manifest.json'):
    d=json.loads(p.read_text())
    manifests[d['title']['en']] = p.parent
ARCHIVE.mkdir(parents=True, exist_ok=True)

for title, filename in ITEMS:
    src = GENERATED / filename
    raw = ARCHIVE / (title.lower().replace(':','').replace(',','').replace(' ','-') + '.png')
    shutil.copy2(src, raw)
    im = Image.open(src).convert('RGB')
    target_ratio=2/3
    ratio=im.width/im.height
    if ratio > target_ratio:
        nw=int(im.height*target_ratio); left=(im.width-nw)//2; im=im.crop((left,0,left+nw,im.height))
    elif ratio < target_ratio:
        nh=int(im.width/target_ratio); top=(im.height-nh)//2; im=im.crop((0,top,im.width,top+nh))
    im=im.resize((1024,1536),Image.Resampling.LANCZOS)
    overlay=Image.new('RGBA',im.size,(0,0,0,0)); od=ImageDraw.Draw(overlay)
    for y in range(640):
        a=max(0,int(205*(1-y/640)))
        od.rectangle((0,y,1024,y+1),fill=(5,8,18,a))
    for y in range(1270,1536):
        a=int(160*((y-1270)/266))
        od.rectangle((0,y,1024,y+1),fill=(5,8,18,a))
    im=Image.alpha_composite(im.convert('RGBA'),overlay)
    draw=ImageDraw.Draw(im)
    # Cover titles default to uppercase and are composed over a deliberately
    # darkened title field so typography remains part of the artwork and stays
    # legible at both full-cover and catalogue-thumbnail sizes.
    display_title=title.upper()
    size=98 if len(display_title)<25 else 82 if len(display_title)<38 else 70
    font=ImageFont.truetype(str(FONT),size)
    lines=wrap(draw,display_title,font,860)
    while len(lines)>4 and size>54:
        size-=4; font=ImageFont.truetype(str(FONT),size); lines=wrap(draw,display_title,font,860)
    y=105
    for line in lines:
        draw.text((82,y),line,font=font,fill='white',stroke_width=2,stroke_fill=(0,0,0,140))
        y += int(size*1.08)
    brand=ImageFont.truetype(str(FONT),25)
    draw.text((82,1450),'SCRIPTAHUB',font=brand,fill=(255,255,255,225))
    root=manifests[title]
    out=root/'en/cover.png'; im.convert('RGB').save(out,optimize=True)
    for lang in ('fr','de','es','pt','it','ro','pl'):
        shutil.copy2(out,root/lang/'cover.png')
    print(title, out)
