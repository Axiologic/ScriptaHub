from pathlib import Path

from bs4 import BeautifulSoup

root = Path(__file__).parent / 'book/en'
soup = BeautifulSoup(
    '<!doctype html><html lang="en"><head><meta charset="utf-8">'
    '<meta name="viewport" content="width=device-width,initial-scale=1">'
    '<title>An Exploration of the Warhammer 40,000 Universe — Ten-minute edition</title>'
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


heading(1, 'An Exploration of the Warhammer 40,000 Universe')
paragraph('This book introduces Warhammer 40,000 as a fictional galaxy in which war shapes nearly every institution. It moves from the Imperium’s belief system and the factions it fights to technology, ordinary life and the Horus Heresy. Beneath the catalog of armies and machines lies a repeated question: what remains of human judgment, compassion and memory when survival becomes the overriding aim? The guide explains the setting’s major terms while inviting readers to examine its grim moral choices.')

heading(2, 'A universe organized for war')
paragraph('The introduction places the Imperium of Man within a hostile galaxy. The Emperor sits immobile on the Golden Throne; the Imperium stretches across worlds it struggles to govern. Travel and communication depend on dangerous psychic forces and technologies that many people use without fully understanding. This scale is part of the setting’s appeal, but it also explains why fear, ritual and bureaucracy shape daily decisions. War is more than a background event: it is the condition under which its societies have grown.', 1)

heading(2, 'What happens to humanity?')
paragraph('The first chapter asks whether a civilization devoted to constant conflict can preserve empathy. Survival can justify sacrifices, but repeated emergency can also normalize cruelty. The text contrasts those pressures with ordinary human desires to create, love and build something better. Even in this bleak setting, the possibility of hope matters. The chapter does not offer an easy escape from war; it asks readers to notice how every claim of necessity changes the people who accept it.', 2)

heading(2, 'The major powers')
paragraph('Chapter two maps the Imperium and its rivals. The Emperor, Space Marines and Adeptus Mechanicus stand beside human institutions that depend on faith and lost knowledge. Chaos, Orks, Eldar, Tyranids, Necrons and other forces present very different threats and ambitions. The factions make the galaxy feel vast, yet their contrast also sharpens the central theme: each imagines order or survival in its own way, and none can avoid the costs of power.', 3)

heading(2, 'Institutions of protection and control')
paragraph('The third chapter follows the Inquisition and other organizations charged with defending humanity. Their roles include detecting heresy, enforcing law, gathering intelligence and maintaining communication across enormous distances. The guide describes specialized orders, assassins and astropaths. These organizations can keep a fragile empire functioning, while their secrecy and harsh methods raise another question: how does a society distinguish necessary defense from the machinery of oppression?', 4)

heading(2, 'Technology without easy progress')
paragraph('Chapter four surveys starships, power armor, weapons, psykers and the strange technologies of rival factions. Much Imperial knowledge is preserved through ritual, making maintenance possible while limiting understanding. Machinery can protect people, extend life or devastate entire worlds. The chapter’s contrast between advanced devices and technical stagnation shows that possessing a powerful tool is different from knowing how to govern its use.', 5)

heading(2, 'Daily life in the Imperium')
paragraph('The fifth chapter steps away from battlefields to examine work, religion, class, education and culture. Hive worlds, forge worlds and agricultural worlds give their inhabitants very different lives, but duty and surveillance are common themes. Art and stories often reinforce official belief, although individual responses remain varied. The guide asks readers to imagine the human cost of an empire whose survival depends on vast, unequal labor.', 6)

heading(2, 'The Horus Heresy')
paragraph('The final chapter traces the Great Crusade, Horus’s corruption, civil war and the Siege of Terra. The Emperor’s fate and the aftermath explain why the later Imperium is fearful, rigid and haunted by lost possibilities. Rather than treating the Heresy as a battle list, the book presents it as a story about trust, betrayal and institutions built in response to trauma. Readers who want to understand the setting can begin with this chapter, then return to the earlier ones to see its long consequences.', 7)

heading(2, 'A reason to continue')
paragraph('The conclusion returns to Warhammer 40,000’s power as a storytelling setting. Its wars, faiths and technologies create many possible stories of endurance and sacrifice. The most useful way into the full book is to follow one question across the chapters: when people fight to survive, what do they decide is still worth saving?', 8)

(root / 'short_content.html').write_text(str(soup) + '\n', encoding='utf-8')
print(len(article.get_text(' ', strip=True).split()), 'words')
