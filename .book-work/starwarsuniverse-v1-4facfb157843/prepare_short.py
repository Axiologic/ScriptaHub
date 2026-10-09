from pathlib import Path

from bs4 import BeautifulSoup

root = Path(__file__).parent / 'book/en'
soup = BeautifulSoup(
    '<!doctype html><html lang="en"><head><meta charset="utf-8">'
    '<meta name="viewport" content="width=device-width,initial-scale=1">'
    '<title>Star Wars Universe — Ten-minute edition</title>'
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


heading(1, 'Star Wars Universe')
paragraph('Star Wars Universe studies a familiar space saga through several connected questions: what the Force means, how diverse societies share a galaxy, how technology changes power, and why the story has endured. The book moves from the Skywalker family to fictional science, philosophy, social organization and the films’ cultural influence. It asks readers to look beyond spectacle while keeping the difference between a fictional world and claims about our own clear.')

heading(2, 'A galaxy held together by stories')
paragraph('The introduction presents the Skywalker story and a galaxy of species, institutions and conflicts. Family loyalties and political choices give the saga its emotional weight. Its planets and cultures make room for larger questions about belonging, moral choice and the use of power. The author treats these elements as a shared imaginative language rather than as proof that any one interpretation is final.', 1)

heading(2, 'The Force as a question')
paragraph('The first chapter imagines how people today might respond if something like the Force or midichlorians were discovered. Scientists might seek a measurement; institutions might seek control; ordinary people might ask what such a discovery says about meaning and freedom. These are speculative questions within the book’s thought experiment. Their value lies in exposing how a new ability can become an ethical problem before anyone agrees what it is for.', 2)

heading(2, 'Philosophy and restraint')
paragraph('The second chapter examines the light and dark sides of the Force, the Jedi code, prophecy and the danger of unchecked power. It compares fictional ideas with themes from several real philosophical traditions. A Jedi’s discipline can protect others, but certainty about a prophecy can also narrow judgment. Anakin’s choices show how fear and a desire for control can undermine good intentions. The chapter invites comparison without flattening the saga into a single moral lesson.', 3)

heading(2, 'Society across worlds')
paragraph('The third chapter looks at cultural difference, social class, government and representation. Alien species and human communities have distinct customs and histories. Coruscant’s wealth and the struggling outer worlds create an uneven political economy, while the Republic’s collapse shows how institutions can be weakened from within. The book also considers women’s roles and recurring stereotypes. Its broad question is how people with unequal resources can still make a common political world.', 4)

heading(2, 'Science fiction and its limits')
paragraph('The technology chapter surveys hyperdrive, lightsabers, droids, prosthetics, planet-wide cities and the Death Star. Some devices echo real engineering questions; others belong openly to fantasy. The contrast matters because technology is never neutral in the story. It can sustain, heal and connect, or it can centralize violence and control. Coruscant raises questions about ecological scale, while Luke’s prosthetic hand and Darth Vader’s armor complicate the boundary between person and machine.', 5)

heading(2, 'The saga’s turning points')
paragraph('The plot chapter moves through the original, prequel and sequel trilogies. Luke’s journey, Anakin’s fall, the Republic’s transformation, Rey’s search for identity and successive rebellions bring the book’s themes into narrative form. Rather than treating every event as an isolated adventure, the author tracks patterns of inheritance, loyalty and resistance. The repeated struggle against concentrated power links characters separated by generations.', 6)

heading(2, 'Why the story remains visible')
paragraph('The final chapter and conclusion turn to Star Wars as a cultural phenomenon. Visual effects, fan creativity and its recurring questions about heroism have influenced later storytelling. Its reach also invites criticism of familiar formulas and representations. The book’s strongest invitation is to revisit a well-known scene with a more precise question: what kind of choice does a character face, and what does the surrounding society make possible or difficult? That question opens the way into the full chapters.', 7)

(root / 'short_content.html').write_text(str(soup) + '\n', encoding='utf-8')
print(len(article.get_text(' ', strip=True).split()), 'words')
