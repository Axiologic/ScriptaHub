from PIL import Image,ImageDraw
from pathlib import Path
import hashlib
p=Path(__file__).resolve().parents[1];sha=hashlib.sha256((p/'review-revision/staged/the-museum-of-good-reasons-introduction.shf').read_bytes()).hexdigest()[:8]
for theme in ['color','paper','night']:
 canvas=Image.new('RGB',(1800,1260),'#dddddd');d=ImageDraw.Draw(canvas)
 for i in range(4):
  for j,f in enumerate(['first','middle','last']):
   im=Image.open(p/f'qa/supported-screenshots/{theme}-{i:02}-{f}.png').crop((60,20,1140,705));im.thumbnail((595,290));canvas.paste(im,(j*600,i*315+20));d.text((j*600+8,i*315+4),f'{theme}/{i}/{f}',fill='black')
 canvas.save(p/f'qa/material-{sha}-{theme}.jpg',quality=91)
 names=['cutaway','separation','followed','retraced','bench-lift','bench-carry','bench-set','page-fold','reading'];canvas=Image.new('RGB',(1800,950),'#ddd');d=ImageDraw.Draw(canvas)
 for i,name in enumerate(names):
  im=Image.open(p/f'qa/action-screenshots/{theme}-{name}.png').crop((110,130,1095,620));im.thumbnail((595,285));canvas.paste(im,((i%3)*600,(i//3)*315+20));d.text(((i%3)*600+8,(i//3)*315+4),f'{theme}/{name}',fill='black')
 canvas.save(p/f'qa/actions-{sha}-{theme}.jpg',quality=91)
print(sha)
