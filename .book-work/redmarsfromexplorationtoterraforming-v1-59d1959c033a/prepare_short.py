from pathlib import Path

from bs4 import BeautifulSoup

root = Path(__file__).parent / 'book/en'
soup = BeautifulSoup(
    '<!doctype html><html lang="en"><head><meta charset="utf-8">'
    '<meta name="viewport" content="width=device-width,initial-scale=1">'
    '<title>Red Mars: From Exploration to Terraforming — Ten-minute edition</title>'
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


heading(1, 'Red Mars: From Exploration to Terraforming')
paragraph('Kim Stanley Robinson’s Red Mars gives this book a way to examine a settlement that must make decisions before it understands all their consequences. The author follows the scientific, political and ethical problems of reaching Mars, building a society there and attempting to transform the planet. The central question is who gets to decide what Mars becomes. Technology can sustain settlers, but it cannot by itself settle conflicts over resources, independence or the value of an untouched world.')

heading(2, 'Beyond the first landing')
paragraph('The opening chapter places Martian settlement within a wider solar-system future. Reusable launch systems, robotics and local resource use could support permanent communities, while distance, radiation and scarce supplies impose hard limits. The text also considers the Moon, asteroids and outer-world destinations. Exploration becomes colonization only when people can build durable habitats and agree on fair ways to govern them. The chapter warns that extending humanity’s reach could repeat Earth’s patterns of exploitation unless cooperation shapes the work from the start.', 2)

heading(2, 'Building a Martian society')
paragraph('The second chapter uses Robinson’s colonists to ask what makes a civilization possible in a hostile environment. They need air, water, food, shelter and dependable local production. They also need institutions, economic rules and a shared account of why their community exists. Scientists, engineers and settlers disagree about the purpose of the colony. Some see Mars as a laboratory or a new home; others see resources and power. These disagreements make social design as important as engineering.', 3)

heading(2, 'Should Mars be transformed?')
paragraph('The terraforming chapter explains proposals to warm Mars, thicken its atmosphere and eventually support more familiar forms of life. Such proposals face enormous timescales and uncertainties. The ethical argument is just as difficult: does humanity have a right to alter another planet, and what might be lost before its environment is fully understood? In the novel, advocates of transformation face those who want Mars protected in its existing state. The book leaves the tension open, asking readers to weigh survival and expansion against restraint and stewardship.', 4)

heading(2, 'Power travels with the settlers')
paragraph('The fourth chapter follows corporate influence on a colony that still depends on Earth for equipment and supply chains. Whoever controls those essentials can influence research, work and political choices. The text contrasts the scientists’ ambitions with organizations seeking returns on investment. It asks whether a new society can preserve public purpose when vital infrastructure is owned elsewhere. Mars may be physically distant from Earth, yet its institutions can inherit the same inequalities and conflicts.', 5)

heading(2, 'Earth and Mars pull apart')
paragraph('The fifth chapter examines dependence and emerging independence. Earth supplies expertise and materials; Mars develops local knowledge, culture and interests. Terraforming itself becomes a dispute between those who benefit from rapid change and those who bear its risks. Technical breakthroughs can flow both ways, but they do not erase political differences. The relationship becomes a test of whether two connected worlds can cooperate without one treating the other as a possession.', 6)

heading(2, 'The story’s turning points')
paragraph('The final chapter traces the First Hundred, the first colony, the struggle over terraforming, growing corporate power and Martian resistance. John Boone’s assassination and the revolution show how personal conflict and institutional pressure converge. The book does not treat these events as a simple prediction of future space travel. They make the earlier questions concrete: who may shape a planet, who controls the means of survival, and what kind of society can survive a break with its origins?', 7)

heading(2, 'A reason to read further')
paragraph('The conclusion returns to responsibility. Mars offers the possibility of a new beginning but no escape from human judgment. Readers interested in the science of settlement can begin with the first three chapters; readers drawn to power and independence can follow the later ones. Across both paths, the book asks whether the ambition to remake a world can be matched by the wisdom to care for it.', 8)

(root / 'short_content.html').write_text(str(soup) + '\n', encoding='utf-8')
print(len(article.get_text(' ', strip=True).split()), 'words')
