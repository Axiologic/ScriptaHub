from pathlib import Path
from bs4 import BeautifulSoup

w = Path(__file__).resolve().parent
out = BeautifulSoup('<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Revealing the Tains of Ender’s Game Saga — Ten-minute edition</title></head><body><article data-reader-content></article></body></html>', 'html.parser')
a = out.article
h = out.new_tag('h1'); h.string = 'Revealing the Tains of Ender’s Game Saga'; a.append(h)
intro = ("This guide reads the Ender’s Game saga through its cultural influence, ethical questions, imagined science, social structure and ideas about leadership. "
"It distinguishes the fictional setting from present-day science while asking why stories of child soldiers, alien contact and military necessity remain troubling. "
"The following route through its eight chapters offers a starting point for the full text; its bibliography identifies the works discussed.")
p = out.new_tag('p'); p.string = intro; a.append(p)
sections = [
('A saga beyond the novel', "The introduction identifies Orson Scott Card’s Ender’s Game as the starting point of a larger fictional universe. It outlines the series’ recurring problems: the treatment of children, justified violence, interspecies conflict and the psychological price of survival. These questions connect its imagined future to debates readers recognize in their own world.", 1),
('Cultural influence', "Chapter one follows the story beyond its original publication into film, education, games, fan culture and military reading. The book describes both creative responses and disputes over the author’s public positions. Its account of influence is therefore about reception as well as invention: readers reuse a story while continuing to argue about the ideas and circumstances attached to it.", 2),
('Philosophy and other species', "Chapter two examines the moral problem of judging minds unlike our own. Encounters with alien species raise questions about consciousness, personhood and the limits of empathy. The chapter also considers cultural relativism and human adaptation under pressure. Its central invitation is to examine the assumptions that turn difference into danger before deciding what counts as a moral response.", 3),
('Science in the imagined future', "Chapter three surveys the scientific concepts that make the setting plausible within its fiction. Space travel, relativistic time, alien intelligence, suspended animation and planetary engineering appear as possibilities to think through. The guide treats them as bridges between current knowledge and speculation, rather than as predictions established by the novels.", 4),
('How society is organized', "Chapter four looks at a humanity organized around an external threat. Battle School trains gifted children for military service, while political unity conceals old rivalries. Institutions manage education, information and security on a vast scale. The book asks what happens to freedom and public knowledge when an emergency becomes the permanent basis of government.", 5),
('Leadership under pressure', "Chapter five follows Ender’s training to explore adaptability, strategy, cooperation and the burden of command. It sets individual brilliance beside trust in a team and considers the loneliness of a child pushed toward authority. The difficult decisions here are not abstract exercises: the series links leadership to responsibility for lives and to the costs borne by the leader.", 6),
('The ethics and psychology of war', "Chapter six turns to the moral injury of conflict. It asks whether annihilation can be justified as self-defense and how fear changes moral judgment. Ender’s empathy is both a tactical strength and a source of anguish. The chapter extends that psychological focus from one child to families and societies shaped by long anticipation of war.", 7),
('The plot in sequence', "Chapter seven provides a compact account of Ender Wiggin’s selection, training, isolation and growing command. It follows the Formic conflict through its decisive events and the aftermath. Readers seeking the narrative framework can begin there, then return to the thematic chapters with a clearer sense of what each argument refers to.", 8),
('Why the legacy persists', "Chapter eight and the conclusion connect the saga to later debates about technology, education, otherness, reconciliation and trauma. They argue that its usefulness lies not only in battle strategy or spectacle, but in the questions its imagined society keeps open. The full book is most rewarding when read with one question in mind: whose humanity is preserved when institutions say survival requires sacrifice?", 9),
]
for heading, body, chapter in sections:
    h = out.new_tag('h2'); h.string = heading; a.append(h)
    p = out.new_tag('p'); p.string = body; a.append(p)
    linkp = out.new_tag('p'); link = out.new_tag('a', href=f'full_content.html#chapter-{chapter}'); link.string = f'Read section {chapter} in full'; linkp.append(link); a.append(linkp)
target = w / 'book/en/short_content.html'
target.parent.mkdir(parents=True, exist_ok=True)
target.write_text(str(out) + '\n')
print('Short reader:', len(a.get_text(' ',strip=True).split()), 'words')
