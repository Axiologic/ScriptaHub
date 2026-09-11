from pathlib import Path
import subprocess,json
from PIL import Image,ImageDraw
w=Path(__file__).parent;books=json.loads((w/'books.json').read_text());sheet=Image.new('RGB',(1200,1800),'#d8d8d8');d=ImageDraw.Draw(sheet)
for i,b in enumerate(books):
 work=Path(b['workdir']);pdf=w/'source-pdfs'/Path(b['filename']).with_suffix('.pdf').name;out=work/'delivered-cover'
 subprocess.run(['pdftoppm','-f','1','-singlefile','-scale-to','1800','-png',str(pdf),str(out)],check=True)
 im=Image.open(out.with_suffix('.png')).convert('RGB');im.thumbnail((280,405));x=(i%4)*300;y=(i//4)*450;sheet.paste(im,(x,y+35));d.text((x+4,y+5),b['title'][:38],fill='black')
sheet.save(w/'covers-contact.jpg')
