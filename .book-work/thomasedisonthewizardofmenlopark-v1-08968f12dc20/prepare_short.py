from pathlib import Path

from bs4 import BeautifulSoup

root = Path(__file__).parent / 'book/en'
soup = BeautifulSoup(
    '<!doctype html><html lang="en"><head><meta charset="utf-8">'
    '<meta name="viewport" content="width=device-width,initial-scale=1">'
    '<title>Thomas Edison: The Wizard of Menlo Park — Ten-minute edition</title>'
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


heading(1, 'Thomas Edison: The Wizard of Menlo Park')
paragraph('This book examines Thomas Edison as an inventor, organizer of research and entrepreneur whose work affected electric light, recorded sound and moving images. It follows his early experiments, the collaborative Menlo Park laboratory, the commercialization of inventions and the controversies around competition and credit. The author presents Edison’s persistence as a useful model while acknowledging that innovation also depends on teams, resources and institutions. The result is a portrait of a working method and its social consequences, not simply a list of patents.')

heading(2, 'Why Edison remains a useful case')
paragraph('The introduction connects familiar objects—lighting, audio recording and film—to the systems of work that made them practical. Edison’s public image as a solitary genius is only part of the story. The book asks how observation, experimentation, organization and commercial judgment combined to turn ideas into technologies people could use. It also prepares the reader to consider costs and disputes alongside achievements.', 1)

heading(2, 'Menlo Park and organized invention')
paragraph('Chapter one describes Edison’s Menlo Park laboratory, established as a place for systematic research. People with different skills worked on related problems, tested alternatives and documented results. The chapter treats this arrangement as a change in the scale and rhythm of invention: a laboratory could pursue several connected projects and refine a device through many small improvements. The model also linked research to patents, production and markets. Edison did not create an invention alone whenever his name appeared on it; the chapter’s account makes the team and its routines visible.', 2)

heading(2, 'Early curiosity and technical practice')
paragraph('The second chapter traces Edison’s interest in experiments and telegraphy. Work as a telegraph operator exposed him to electrical systems and gave him practical problems to solve. Repeated tinkering helped him learn from failures and recognize where an improved device could matter. The author uses these early years to show skill forming through practice rather than arriving fully developed. Curiosity becomes productive when it is paired with sustained attention to a problem.', 3)

heading(2, 'Light, sound and images')
paragraph('Chapter three follows the better-known inventions. The practical incandescent lamp required more than a filament: it depended on materials, a suitable bulb and an electrical system for supplying power. The phonograph made sound recording and playback possible in a new form. Moving-picture devices and studios contributed to the early film industry. The chapter repeatedly turns from the celebrated object to the supporting system, where an invention becomes usable at scale.', 4)

heading(2, 'How the work was done')
paragraph('Chapter four examines Edison’s methods: long trials, detailed records, iterative changes and collaboration. The book describes his determination and willingness to test many materials or configurations. It also shows the competitive side of commercialization, where patents, investment and public persuasion could shape the fate of a technology. Persistence alone does not decide which invention succeeds; resources, timing and markets influence the result.', 5)

heading(2, 'Effects on industry and daily life')
paragraph('The fifth chapter asks what changed after the laboratory. Electric power and lighting altered businesses, homes and urban routines. Recording created new ways to distribute music and speech, while film helped form a new kind of entertainment industry. These effects were not confined to the first device sold: infrastructure, companies and habits developed around each technology. The book uses these examples to connect invention with broader social change.', 6)

heading(2, 'Disputes and the later legacy')
paragraph('Chapters six and seven complicate the heroic portrait. Edison’s disputes over alternating and direct current, aggressive business tactics and questions about credit show that technological change has ethical and competitive dimensions. The book does not erase his accomplishments; it asks how to judge them alongside the work of collaborators and rivals. His lasting legacy includes an organized approach to experimentation, a model for research laboratories and a reminder that an inventor’s public name often stands over a much wider network of labor.', 7)
paragraph('The legacy chapter follows Edison’s influence beyond his lifetime, from research routines to the public image of an inventor. It invites readers to examine the contrast between the famous individual and the many people and systems behind durable technology.', 8)

heading(2, 'The conclusion')
paragraph('The conclusion returns to the relation between curiosity and structure. Edison’s career illustrates how disciplined trials, capable colleagues and a route to practical use can move an idea beyond the laboratory. It also warns against treating success as proof that every method was fair or every credit complete. Readers can take from this story both the value of patient experimentation and the need to examine who contributes to an invention, who benefits from it and what it changes.', 9)

(root / 'short_content.html').write_text(str(soup) + '\n', encoding='utf-8')
print(len(article.get_text(' ', strip=True).split()), 'words')
