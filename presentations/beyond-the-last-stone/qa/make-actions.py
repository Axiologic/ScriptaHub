from PIL import Image,ImageDraw
from pathlib import Path
p=Path(__file__).parent;d=p/'action-screenshots'
for theme in ['color','paper','night']:
 sheet=Image.new('RGB',(1800,960),'#ddd');draw=ImageDraw.Draw(sheet)
 for i,name in enumerate(['remembered-wait','packed','track','stone-held','stone-released','record','received']):
  im=Image.open(d/(theme+'-'+name+'.png')).crop((62,170,1138,630));im.thumbnail((580,285));x=(i%3)*600;y=(i//3)*320;sheet.paste(im,(x,y+25));draw.text((x+8,y+5),theme+' / '+name,fill='black')
 sheet.save(p/('actions-'+theme+'.jpg'))
