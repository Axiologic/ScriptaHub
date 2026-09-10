from pathlib import Path
from html import escape
import re
from bs4 import BeautifulSoup, NavigableString
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle, Image, KeepTogether
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_CENTER
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from PIL import Image as PILImage
root=Path(__file__).resolve().parent
for name,file in [('Novel','Regular'),('Novel-Bold','Bold'),('Novel-Italic','Italic'),('Novel-BoldItalic','BoldItalic')]:
 pdfmetrics.registerFont(TTFont(name,f'/usr/share/fonts/liberation-serif-fonts/LiberationSerif-{file}.ttf'))
pdfmetrics.registerFontFamily('Novel',normal='Novel',bold='Novel-Bold',italic='Novel-Italic',boldItalic='Novel-BoldItalic')
page=(148*mm,210*mm);margin=18*mm;width=page[0]-2*margin;height=page[1]-2*margin
base=ParagraphStyle('Body',fontName='Novel',fontSize=10.5,leading=14,spaceAfter=5,alignment=TA_JUSTIFY,allowWidows=0,allowOrphans=0)
head=ParagraphStyle('Heading',parent=base,fontName='Novel-Bold',fontSize=17,leading=20,spaceBefore=12,spaceAfter=14,alignment=TA_LEFT,keepWithNext=True)
part=ParagraphStyle('Part',parent=head,fontSize=23,leading=27,spaceBefore=30)
kicker=ParagraphStyle('Kicker',parent=base,fontSize=9,leading=12,spaceAfter=8,keepWithNext=True,alignment=TA_LEFT)
cell=ParagraphStyle('Cell',parent=base,fontSize=9,leading=11.5,spaceAfter=0,alignment=TA_LEFT)
cover=ParagraphStyle('Title',parent=head,fontSize=22,leading=27,alignment=TA_CENTER,spaceAfter=15)
def markup(node):
 if isinstance(node,NavigableString):return escape(str(node))
 if node.name=='br':return '<br/>'
 inner=''.join(markup(c) for c in node.children)
 if node.name in ['b','strong']:return '<b>'+inner+'</b>'
 if node.name in ['em','i']:return '<i>'+inner+'</i>'
 return inner
soup=BeautifulSoup((root/'book/en/full_content.html').read_text(),'html.parser')
story=[];in_story=False;first_image=True;next_location=False
for tag in soup.article.find_all(recursive=False):
 text=tag.get_text(' ',strip=True)
 if tag.find('img'):
  src=(root/'book/en'/tag.img['src']).resolve();iw,ih=PILImage.open(src).size
  scale=min((width-2)/iw,(height-4)/ih)
  story.extend([Image(str(src),width=iw*scale,height=ih*scale),PageBreak()]);first_image=False;continue
 if tag.name=='table':
  rows=[]
  for tr in tag.find_all('tr'):
   rows.append([Paragraph(markup(td),cell) for td in tr.find_all(['td','th'],recursive=False)])
  table=Table(rows,colWidths=[width*.3,width*.7],repeatRows=1,hAlign='LEFT')
  table.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'),('GRID',(0,0),(-1,-1),.35,colors.HexColor('#aaaeb5')),('BACKGROUND',(0,0),(-1,0),colors.HexColor('#eef0f3')),('LEFTPADDING',(0,0),(-1,-1),6),('RIGHTPADDING',(0,0),(-1,-1),6),('TOPPADDING',(0,0),(-1,-1),6),('BOTTOMPADDING',(0,0),(-1,-1),6)]))
  story.extend([table,Spacer(1,12)]);continue
 if not text:
  if not in_story:story.append(Spacer(1,7))
  continue
 if re.fullmatch(r'PART [IVX]+',text):
  story.extend([PageBreak(),Paragraph(markup(tag),kicker)]);in_story=True;continue
 if re.fullmatch(r'CHAPTER [IVX]+',text):
  story.extend([PageBreak(),Paragraph(markup(tag),kicker)]);next_location=True;continue
 if tag.name in ['h1','h2']:
  story.append(Paragraph(markup(tag),part if tag.name=='h1' else head));continue
 if next_location:
  story.append(Paragraph(markup(tag),kicker));next_location=False;continue
 if not in_story and text.startswith('THOSE WHO'):
  story.append(Paragraph(markup(tag),cover));continue
 # Keep frontmatter labels with their first entry.
 style=kicker if not in_story and tag.find('strong') and len(text)<60 else base
 story.append(Paragraph(markup(tag),style))
def decorate(c,doc):
 if doc.page==1:return
 c.saveState();c.setFillColor(colors.HexColor('#69707b'));c.setFont('Novel',8)
 c.drawCentredString(page[0]/2,10*mm,str(doc.page))
 c.setFont('Novel-Italic',7.5);c.drawCentredString(page[0]/2,page[1]-10*mm,'Those Who No Longer Run')
 c.restoreState()
doc=SimpleDocTemplate(str(root/'book/en/book.pdf'),pagesize=page,leftMargin=margin,rightMargin=margin,topMargin=margin,bottomMargin=margin,title='Those Who No Longer Run',author='ScriptaHub',subject='A science-fiction novel',pageCompression=1)
doc.build(story,onFirstPage=decorate,onLaterPages=decorate)
print(root/'book/en/book.pdf')
