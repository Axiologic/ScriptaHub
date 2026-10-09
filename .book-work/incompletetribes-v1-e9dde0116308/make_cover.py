from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

root = Path('.book-work/incompletetribes-v1-e9dde0116308')
out = root / 'qa/cover-revised.png'
out.parent.mkdir(exist_ok=True)
size = (1000, 1500)
image = Image.new('RGB', size, '#112c36')
draw = ImageDraw.Draw(image)
bold = '/usr/share/fonts/redhat/RedHatDisplay-Bold.otf'
regular = '/usr/share/fonts/redhat/RedHatDisplay-Regular.otf'
title_font = ImageFont.truetype(bold, 96)
sub_font = ImageFont.truetype(regular, 37)

# Three open, overlapping forms visualize strong communities that leave exits.
for box, start, end, color, width in [
    ((82, 463, 705, 1086), 22, 315, '#70b8ae', 21),
    ((305, 508, 930, 1133), 196, 486, '#d2a969', 21),
    ((191, 614, 783, 1206), 52, 310, '#e3e9d5', 13),
]:
    draw.arc(box, start, end, fill=color, width=width)

draw.text((74, 104), 'INCOMPLETE', font=title_font, fill='#f4f0e4')
draw.text((74, 216), 'TRIBES', font=title_font, fill='#f4f0e4')
draw.text((75, 1320), 'BELONGING, CONFLICT, AND THE HOPE OF', font=sub_font, fill='#e4e4d9')
draw.text((75, 1372), 'BUILDING A CIVILIZATION FOR', font=sub_font, fill='#e4e4d9')
draw.text((75, 1424), 'IMPERFECT HUMANS', font=sub_font, fill='#e4e4d9')
image.save(out, optimize=True)
print(out)
