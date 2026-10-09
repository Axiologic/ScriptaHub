from pathlib import Path

from bs4 import BeautifulSoup

root = Path(__file__).parent / 'book/en'
soup = BeautifulSoup(
    '<!doctype html><html lang="en"><head><meta charset="utf-8">'
    '<meta name="viewport" content="width=device-width,initial-scale=1">'
    '<title>The Universe of The Left Hand of Darkness — Ten-minute edition</title>'
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


heading(1, 'The Universe of The Left Hand of Darkness')
paragraph('This guide reads Ursula K. Le Guin’s The Left Hand of Darkness through gender, politics, culture and the slow work of understanding another person. On Gethen, Genly Ai seeks to bring a world into the Ekumen while learning how his own assumptions distort what he sees. The book asks what changes when fixed gender categories are absent and what does not change: rivalry, hierarchy, fear and the need for trust still shape society.')

heading(2, 'Arriving with assumptions')
paragraph('The introduction places Genly between Karhide and Orgoreyn, two rival nations with different ways of governing. Gethenians do not hold permanent male or female identities; their sexual characteristics change during kemmer. Genly’s mission is diplomatic, but it is also an education in listening. The guide follows the tension between what an outsider thinks he knows and what people on Gethen actually do.', 1)

heading(2, 'Power without fixed gender')
paragraph('Chapter one asks whether the absence of permanent gender roles produces a fairer political world. It may remove some familiar forms of hierarchy, but it does not erase ambition or control. Institutions still distribute authority, and personal relationships still carry unequal expectations. The chapter treats Gethen as a way to test assumptions about the origins of power rather than as a simple utopia.', 2)

heading(2, 'Androgyny and relationship')
paragraph('Chapter two looks more closely at kemmer and at the social meanings of fluid sex. Family, intimacy and parenthood work differently when anyone may occupy different reproductive roles. Genly initially reads Gethenians through categories brought from his own world, which limits his understanding of them. The guide connects this problem to feminist and Taoist readings of the novel, especially its interest in paired forces that need not be permanent opposites.', 3)

heading(2, 'Two nations, two kinds of pressure')
paragraph('The third chapter compares Karhide’s monarchy and traditions with Orgoreyn’s bureaucracy and surveillance. Both governments have ways of shaping what citizens may say and do. National pride, fear and miscommunication complicate Genly’s attempt to build diplomatic trust. Religion and cultural memory also influence political choices. The chapter asks whether understanding another culture can bridge a divide that powerful institutions have an interest in maintaining.', 4)

heading(2, 'Crossing the ice')
paragraph('Chapter four follows Genly and Estravan on their difficult journey across the frozen landscape. Survival demands cooperation, and shared risk changes how Genly sees his companion. Knowledge here is more than observation from a distance; it grows through dependence, vulnerability and experience. The ice crossing gives the guide its clearest example of a relationship moving beyond inherited suspicion.', 5)

heading(2, 'Forms of control')
paragraph('The fifth chapter examines power at several scales. King Argaven rules through personal authority and unpredictability; Orgoreyn relies on administrative control and hidden coercion. Genly and Estravan must also negotiate trust and influence within their own relationship. The guide shows how the novel places personal and political power beside one another, asking whether either can be exercised without treating another person as an object.', 6)

heading(2, 'Why read the full study?')
paragraph('The conclusion returns to gender, authority and cultural understanding. Le Guin’s fictional world does not provide a formula for society, but it unsettles familiar assumptions and rewards patient attention. Readers interested in gender can begin with the first two chapters; those drawn to diplomacy can begin with Karhide and Orgoreyn, then follow the crossing of the ice. Across the book, the question is how we learn to recognize a person beyond the categories we brought with us.', 7)

(root / 'short_content.html').write_text(str(soup) + '\n', encoding='utf-8')
print(len(article.get_text(' ', strip=True).split()), 'words')
