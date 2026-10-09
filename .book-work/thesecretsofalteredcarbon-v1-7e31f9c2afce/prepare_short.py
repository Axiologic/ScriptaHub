from pathlib import Path

from bs4 import BeautifulSoup

root = Path(__file__).parent / 'book/en'
soup = BeautifulSoup(
    '<!doctype html><html lang="en"><head><meta charset="utf-8">'
    '<meta name="viewport" content="width=device-width,initial-scale=1">'
    '<title>The Secrets of Altered Carbon — Ten-minute edition</title>'
    '</head><body><article data-reader-content></article></body></html>',
    'html.parser',
)
article = soup.article


def heading(level, value):
    node = soup.new_tag(f'h{level}')
    node.string = value
    article.append(node)


def paragraph(value, section=None):
    node = soup.new_tag('p')
    node.append(value)
    if section:
        node.append(' ')
        link = soup.new_tag('a', href=f'full_content.html#chapter-{section}')
        link.string = f'Read section {section} in full'
        node.append(link)
        node.append('.')
    article.append(node)


heading(1, 'The Secrets of Altered Carbon')
paragraph('This guide uses Richard K. Morgan’s Altered Carbon to ask what happens when a person’s mind can be stored and placed in another body. The technology promises longer lives, but its benefits are distributed unequally. The chapters move from the threat to stored minds through identity, social power and the moral choices faced by Takeshi Kovacs. The central question is whether escaping ordinary death also changes what people owe one another.')

heading(2, 'A new vulnerability')
paragraph('The introduction explains cortical stacks and resleeving, the transfer of a stored consciousness into a new body. The first chapter then examines the Rawling virus, a danger to minds that exist as data. When a backup can be damaged, copied or stolen, survival depends on systems that others may control. The threat makes digital immortality less secure than it first appears and raises questions about privacy, access and technological dependence.', 2)

heading(2, 'Living beyond one body')
paragraph('Chapter two considers how stored consciousness changes risk, family and time. A person may survive the death of one body, but cannot assume every replacement is available or equal. Long lives might alter commitments between generations and change the meaning of memory. The book treats these possibilities as features of Morgan’s fictional world, not as a present scientific achievement.', 3)

heading(2, 'Who is the same person?')
paragraph('The third chapter explores the separation of mind and body. If consciousness can move or be copied, what makes someone the same person? A new body may change how others respond, while stored experiences may not capture every part of a life. The guide uses the series to examine philosophical questions about continuity, ownership and the relation between memory and physical experience.', 4)

heading(2, 'Identity as a social fact')
paragraph('Chapter four asks how body swapping affects culture, family and prejudice. People may move between appearances, ages and social positions, yet inequality can persist through access to better sleeves. New forms of shame or status arise around bodies. The chapter shows that a technology that makes identity more flexible need not make society more accepting.', 5)

heading(2, 'Power behind the machinery')
paragraph('The fifth chapter surveys the science-fiction technologies that support this world: stacks, transmitted consciousness, virtual spaces, medical advances and alien artifacts. Each capability creates another question about control. Who can repair or replace a body? Who owns a stored mind? The guide connects technical possibility with institutions and incentives instead of assuming that an invention alone determines its use.', 6)

heading(2, 'The Meths and the rest')
paragraph('Chapter six focuses on inequality. The very wealthy Meths can repeatedly renew themselves, accumulate power and insulate themselves from consequences. Others face inferior bodies, insecure work and the threat of permanent death. In Bay City, the height of a building mirrors the distance between social classes. The book asks whether an extended life becomes another resource that wealth can monopolize.', 7)

heading(2, 'Ethics after ordinary death')
paragraph('Chapter seven considers punishment, consent, autonomy and the treatment of artificial intelligence in a society where minds can be stored. Imprisonment or exploitation can last much longer when a person can be held as data. The guide also asks whether removing the shared limit of mortality changes moral responsibility. Its questions reach beyond the plot without claiming simple answers.', 8)

heading(2, 'Kovacs and the larger system')
paragraph('The plot chapter follows Kovacs as he is placed in a new body and hired to investigate Laurens Bancroft’s death. His inquiry exposes corruption and the unequal power of people who can live for centuries. Memories of the Envoys and Quellcrist Falconer shape his choices. The conclusion invites readers to follow those choices into the complete book, then ask whose freedom the technology actually protects.', 9)

(root / 'short_content.html').write_text(str(soup) + '\n', encoding='utf-8')
print(len(article.get_text(' ', strip=True).split()), 'words')
