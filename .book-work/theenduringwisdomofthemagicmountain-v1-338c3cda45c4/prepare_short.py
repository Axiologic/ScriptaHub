from pathlib import Path

from bs4 import BeautifulSoup

root = Path(__file__).parent / 'book/en'
soup = BeautifulSoup(
    '<!doctype html><html lang="en"><head><meta charset="utf-8">'
    '<meta name="viewport" content="width=device-width,initial-scale=1">'
    '<title>The Enduring Wisdom of The Magic Mountain — Ten-minute edition</title>'
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


heading(1, 'The Enduring Wisdom of The Magic Mountain')
paragraph('This book reads Thomas Mann’s The Magic Mountain as a set of questions that remain useful in a digital age. The Berghof sanatorium becomes a place to examine rival ideologies, the experience of time, illness, social habits, culture and the search for meaning. The author draws parallels to contemporary life without treating the novel as a prediction or a simple manual. The central invitation is to test familiar ideas against Mann’s complicated characters and to resist easy answers.')

heading(2, 'Why return to the Berghof?')
paragraph('The introduction places Hans Castorp in the isolated mountain sanatorium, where conversation and illness interrupt ordinary expectations about work and time. This setting allows Mann to stage debates about progress, authority, mortality and Europe before war. The book asks what readers can learn from that arrangement today. The strongest connection is a method of reading: listen to incompatible positions, notice how institutions shape experience, and ask whether a comfortable retreat sharpens thought or encourages withdrawal.', 1)

heading(2, 'A battlefield of ideas')
paragraph('Chapter one focuses on arguments associated with Settembrini and Naphta. Liberal faith in reason and progress faces an attraction to certainty, authority and more extreme claims. Castorp listens, hesitates and changes, which keeps the debate from turning into a simple contest with one tidy winner. The author compares this tension to polarized public discussion today. The novel suggests that critical thinking requires engagement with difficult ideas, yet engagement need not mean surrendering judgment. The Berghof’s distance from the wider world makes these conversations vivid and also exposes their limits.', 2)

heading(2, 'Time on the mountain')
paragraph('The second chapter examines the strange tempo of Castorp’s stay. Days repeat; illness and routine stretch or compress the sense of passing years. The book sets this beside modern habits of scheduling, measuring and seeking escape from constant demands. A clock can count time precisely without describing how a person lives through it. Mann’s narrative pace invites readers to notice that difference. The chapter asks whether apparent leisure creates reflection or merely another way to avoid decisions waiting beyond the mountain.', 3)

heading(2, 'Illness and social symptoms')
paragraph('Chapter three treats the sanatorium as more than a medical setting. Its rules, hierarchies and rituals reveal how a community gives meaning to illness and expertise. The author draws parallels to modern debates about health, information and identity, while the novel’s characters remain rooted in their own historical world. The chapter’s point is not that today repeats the Berghof exactly. It is that societies can turn diagnoses, routines and confident explanations into stories about who belongs, who knows and who deserves attention.', 4)

heading(2, 'A changing human condition')
paragraph('The fourth chapter follows Castorp’s search for identity, education, love and a way to face death. His stay removes him from familiar roles without giving him a stable replacement. The book compares that uncertainty with modern changes in relationships and sources of knowledge. Access to more information does not guarantee understanding; a person still needs to decide what matters and how to live with others. Mann’s value here lies in his refusal to resolve every question too quickly.', 5)

heading(2, 'Art, culture and belonging')
paragraph('Chapter five looks at music, stories and cultural life in the novel. Art can deepen attention and create shared experience, but it can also become a possession or diversion. The author compares the Berghof’s cultural habits with the abundance and speed of digital media. The comparison asks readers to distinguish access from engagement: having endless works available is different from allowing one to change how we think. Culture can make room for complexity when it does not flatten every disagreement into a slogan.', 6)

heading(2, 'Descending with questions')
paragraph('The sixth chapter and conclusion return to the wider world. The mountain cannot protect Castorp or his contemporaries from history; reflection eventually meets action. The book gathers its themes—ideology, time, illness, identity and art—into an argument for attentive, critical living. It does not claim that Mann provides solutions to digital-age problems. He offers a demanding space in which to notice competing values and examine our responses. A reader can start with Castorp’s conversations, then ask which voices guide their own choices and which questions they have postponed.', 7)

(root / 'short_content.html').write_text(str(soup) + '\n', encoding='utf-8')
print(len(article.get_text(' ', strip=True).split()), 'words')
