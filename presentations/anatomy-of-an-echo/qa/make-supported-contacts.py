from PIL import Image,ImageDraw
from pathlib import Path
p=Path(__file__).parent
for theme in ['color','paper','night']:
 sheet=Image.new('RGB',(1800,1260),'#ddd');d=ImageDraw.Draw(sheet)
 for f in sorted((p/'supported-screenshots').glob(theme+'-*.png')):
  i=int(f.name.split('-')[1]);frame=f.stem.split('-')[2];col={'first':0,'middle':1,'last':2}[frame];im=Image.open(f).crop((62,24,1138,706));im.thumbnail((465,294));sheet.paste(im,(col*600,i*315+20));d.text((col*600+8,i*315+3),f.name,fill='black')
 sheet.save(p/('support-final-'+theme+'.jpg'))
