from pathlib import Path

from bs4 import BeautifulSoup


root = Path(__file__).parent / 'book/en'
soup = BeautifulSoup(
    '<!doctype html><html lang="en"><head><meta charset="utf-8">'
    '<meta name="viewport" content="width=device-width,initial-scale=1">'
    '<title>Are We Alone? Imagining Life with Aliens — Ten-minute edition</title>'
    '</head><body><article data-reader-content></article></body></html>',
    'html.parser',
)
article = soup.article


def heading(level, value):
    node = soup.new_tag(f'h{level}')
    node.string = value
    article.append(node)


def paragraph(value, chapter=None):
    node = soup.new_tag('p')
    node.append(value)
    if chapter:
        node.append(' ')
        link = soup.new_tag('a', href=f'full_content.html#chapter-{chapter}')
        link.string = f'Read section {chapter} in full'
        node.append(link)
        node.append('.')
    article.append(node)


heading(1, 'Are We Alone? Imagining Life with Aliens')
paragraph('This book follows two questions that are often treated separately: where might life exist beyond Earth, and how would people respond if they found it? It begins with stars and exoplanets, uses Earth’s extremophiles to widen the idea of a habitable environment, then examines telescopes, rovers and possible contact. The author asks readers to distinguish the search for evidence from imagination about its social consequences. No extraterrestrial discovery is presented as established; the scenarios are possibilities that help frame the scientific and human stakes.')

heading(2, 'The opening question')
paragraph('The introduction looks up at a crowded sky and asks whether another world might support life, perhaps even intelligent life. A confirmed detection would raise immediate questions about communication, identity, fear and coexistence. The author deliberately moves beyond the narrower question of whether life exists. If the answer is yes, what assumptions about humanity would change, and what would respectful contact require? These questions give the scientific chapters a human purpose.', 1)

heading(2, 'A universe of possible homes')
paragraph('Chapter one places the search against the scale of the universe. Stars have planets, and some exoplanets lie in regions where liquid water could persist. The book introduces the habitable zone and the TRAPPIST-1 system as ways to think about candidate worlds. Astronomers can study an atmosphere for gases associated with particular processes, but a promising atmosphere is not proof of organisms. The chapter also faces the great silence: a large universe may offer many chances for life, yet no unambiguous contact has been confirmed.')
paragraph('That tension matters. Vast numbers make the question worth asking, but they cannot by themselves answer it. The author treats uncertainty as a reason to keep looking and to improve the tools used to observe distant worlds.', 2)

heading(2, 'What Earth’s extremes teach us')
paragraph('Chapter two turns from distant planets to life in environments once considered inhospitable. Microbes near hydrothermal vents, organisms in acidic or salty places, and hardy tardigrades show that life on Earth can tolerate conditions outside ordinary human experience. The lesson is not that every harsh world is inhabited. It is that our assumptions about where to search should reflect what living systems have actually done.')
paragraph('Europa and Enceladus appear as examples of icy moons with subsurface oceans that may merit investigation. Mars remains another candidate for traces of earlier or sheltered microbial life. These worlds broaden the search beyond a simple Earth-like planet, while leaving the decisive question—whether anything lives there—to observation.', 3)

heading(2, 'Tools that turn possibility into evidence')
paragraph('Chapter three explains why technology is central to the search. Spectroscopy reads light passing through or reflected from an atmosphere and can reveal chemical clues. Powerful telescopes can examine distant exoplanets; robotic explorers can inspect nearby worlds more directly. The book discusses the James Webb Space Telescope, Mars rovers and ideas for future instruments and missions. Each tool answers a different part of the problem: where to look, what a planet or moon contains, and whether an apparent sign of life survives careful testing.')
paragraph('The distinction between a biosignature and a confirmed organism runs through this chapter. Oxygen or methane can be interesting, yet chemistry and geology can produce misleading signals. Samples and multiple kinds of evidence matter. The book’s mission examples reflect its 2024 source context; the reader should treat launch plans and mission status as historical statements in that edition.', 4)

heading(2, 'If discovery becomes real')
paragraph('Chapter four imagines what a reliable discovery could mean. Even microbial life elsewhere would change our understanding of biology and Earth’s place in a wider universe. Evidence of intelligence would bring harder questions about language, power, religion, culture and political decisions. The author does not claim to know how humanity would react. Instead, the chapter uses possible reactions—wonder, fear, cooperation and conflict—to ask what preparation might look like.')
paragraph('The historical record of encounters between human societies provides a warning about inequality and misunderstanding, though it cannot tell us what contact with nonhuman life would be like. The book asks readers to approach uncertainty with curiosity, humility and care rather than assuming either a utopia or a threat.', 5)

heading(2, 'The conclusion')
paragraph('The conclusion returns to the link between outward exploration and self-understanding. Exoplanets, extremophiles and instruments have changed what people can investigate, but they have not settled the central question. Searching for life also tests how we define life, how we handle ambiguous evidence and how we imagine sharing a universe. The book invites a reader to begin with the scientific clues, then carry their uncertainty into the deeper question of coexistence.')

(root / 'short_content.html').write_text(str(soup) + '\n', encoding='utf-8')
print(len(article.get_text(' ', strip=True).split()), 'words')
