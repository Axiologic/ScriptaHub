from bs4 import BeautifulSoup
from pathlib import Path

base = Path(__file__).parent / 'book/en'
soup = BeautifulSoup('<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>A Cheeky Guide to Ancient Greek Philosophy — Ten-minute edition</title></head><body><article data-reader-content></article></body></html>', 'html.parser')
article = soup.article

def h(level, text):
    tag = soup.new_tag(f'h{level}')
    tag.string = text
    article.append(tag)

def p(text, chapter=None):
    tag = soup.new_tag('p')
    tag.append(text)
    if chapter:
        tag.append(' ')
        link = soup.new_tag('a', href=f'full_content.html#chapter-{chapter}')
        link.string = f'Read section {chapter} in full'
        tag.append(link)
        tag.append('.')
    article.append(tag)

h(1, 'A Cheeky Guide to Ancient Greek Philosophy')
p('This brisk, deliberately irreverent guide follows Greek philosophy from the Pre-Socratics through the classical and Hellenistic schools, then tracks its later echoes in European thought. Its jokes and invented scenes are a teaching style, not historical evidence. The philosophical questions beneath them are serious: what is the world made of, what can we know, how should we live, and how do old arguments keep changing form? The book uses four chapters and a recap to make those questions approachable without pretending that a single school settled them.')

h(2, 'The Pre-Socratic search for nature')
p('The first chapter opens with early thinkers trying to explain the world through principles rather than inherited stories. Thales proposes water as a basic element. Anaximander answers with the apeiron, a boundless source that cannot be reduced to one familiar material. Heraclitus directs attention toward change and the image of a river that cannot be entered twice in exactly the same way. The chapter’s jokes exaggerate their personalities, but the contrast between proposed substances, the boundless, and constant change gives readers a route into their disputes.')
p('The Pre-Socratics matter here because they ask what underlies the many things we see. Even answers that now sound strange turn a basic observation into a question that can be argued about. The book treats their competing proposals as the beginning of a continuing conversation, not a sequence of facts to memorize.', 1)

h(2, 'Socrates, Plato and Aristotle')
p('The second chapter gathers the classical “Big Three.” Socrates appears as a relentless questioner who tests people’s confidence in what they claim to know. His method makes conversation an instrument of examination, and his refusal to give easy answers is part of the lesson. Plato develops a distinction between the world as it appears and a more stable reality of Forms. The cave image asks what education would mean if familiar appearances were only shadows of something deeper.')
p('Aristotle challenges parts of Plato’s approach by attending more closely to the observable world. The guide presents his wide-ranging interests, from natural inquiry and politics to ethics, and introduces the Golden Mean as a way of thinking about proportion between extremes. Their differences matter as much as their shared influence: questioning, abstract explanation and observation offer different ways to seek understanding.', 2)

h(2, 'Philosophy as a way of life')
p('After Alexander, the Hellenistic schools move the guide from theories about reality toward the problem of living well. Cynics challenge convention through radical simplicity, with Diogenes supplying the book’s most comic examples. Stoics focus on how to respond to events beyond one’s control. Epicureans seek pleasure through moderation rather than endless indulgence. Skeptics question claims to certainty and keep inquiry open.')
p('The chapter’s contemporary comparisons are intentionally playful. Underneath them lies a practical disagreement: should freedom come from shedding social expectations, disciplining judgment, choosing modest satisfactions, or refusing premature conclusions? Each school offers a different answer to a question that readers can still apply to their own habits and decisions.', 3)

h(2, 'The long philosophical hangover')
p('The fourth chapter takes a rapid, comic tour of how Greek arguments reappear after antiquity. Renaissance readers return to ancient texts; the Scientific Revolution renews disputes about mathematical form and observation. Later philosophers such as Descartes, Spinoza, Leibniz, Locke and Hume revisit questions of mind, experience, substance and knowledge. The book then moves through Nietzsche, existentialism, phenomenology, analytic philosophy, postmodernism and contemporary debates. Its aim is to show a chain of recurring questions, not to make these distinct thinkers interchangeable.')
p('The links to modern ethics, technology and politics bring the tour back to everyday life. What counts as evidence? How does language shape a problem? Is identity given or made? How should people respond when new technologies change the conditions of choice? The chapter’s pace invites readers to recognize old philosophical tensions in new settings and then return to the fuller discussions of thinkers that interest them.', 4)

h(2, 'What the guide asks readers to keep')
p('The conclusion revisits the three ancient periods. Pre-Socratics ask what the world is made of; the classical thinkers test knowledge, reality and ethics; the Hellenistic schools make philosophy practical. The book refuses to turn that history into a final answer. Its lasting invitation is to question familiar claims, compare possible ways of living, and use curiosity without losing a sense of humor. The jokes can be set aside; the questions remain worth asking.', 5)

(base / 'short_content.html').write_text(str(soup) + '\n', encoding='utf-8')
print(len(article.get_text(' ', strip=True).split()), 'words')
