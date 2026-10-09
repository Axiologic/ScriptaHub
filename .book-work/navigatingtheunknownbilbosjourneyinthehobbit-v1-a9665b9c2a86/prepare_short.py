from pathlib import Path

from bs4 import BeautifulSoup

root = Path(__file__).parent / 'book/en'
soup = BeautifulSoup(
    '<!doctype html><html lang="en"><head><meta charset="utf-8">'
    '<meta name="viewport" content="width=device-width,initial-scale=1">'
    '<title>Navigating the Unknown: Bilbo’s Journey in The Hobbit — Ten-minute edition</title>'
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


heading(1, 'Navigating the Unknown: Bilbo’s Journey in The Hobbit')
paragraph('This book follows Bilbo Baggins as a reader’s guide to courage, growth and the pull between comfort and adventure in J.R.R. Tolkien’s The Hobbit. It moves from Bilbo’s reluctant departure through encounters with trolls, goblins and Smaug to his choices near the end of the journey. The author pays attention to Bilbo’s humor and hesitation as well as his bravery. These chapters discuss important turns in the novel, including its later conflict, so they are best read by someone who welcomes story details.')

heading(2, 'A reluctant traveler')
paragraph('The introduction begins with Bilbo’s settled life in the Shire. Gandalf and the dwarves interrupt a world ordered around familiar meals, routines and safety. Bilbo does not immediately become a fearless adventurer; the possibility of leaving home unsettles him. The book treats this hesitation as part of his appeal. Tolkien’s journey asks whether growth requires leaving comfort behind, and whether a person can discover capabilities they had no reason to use at home.', 1)

heading(2, 'The first step beyond home')
paragraph('Chapter one follows the surprise gathering at Bilbo’s door and the pressure to join Thorin’s company. The dwarves expect a burglar; Bilbo has little evidence that he can be one. His departure is therefore a choice made under uncertainty, not the simple unveiling of a hero. The author emphasizes the comic mismatch between Bilbo’s domestic habits and the wild journey before him. That mismatch gives the story its early energy and allows every later act of courage to feel earned.', 2)

heading(2, 'Trolls, goblins and a sharper mind')
paragraph('The second chapter follows Bilbo into a world where size and strength do not settle every problem. Trolls and goblins expose how vulnerable the company can be, and Gollum’s riddles make thinking under pressure decisive. Bilbo is frightened and makes mistakes, yet he learns to observe, improvise and act when help is not close at hand. The author reads these scenes as a change in Bilbo’s relationship to danger. He does not stop fearing it; he begins to find a response besides retreat.', 3)

heading(2, 'Facing Smaug')
paragraph('Chapter three concentrates on Bilbo’s encounter with the dragon. Entering Smaug’s lair calls for stealth, but the conversation also demands careful speech. Bilbo must gather information without giving away too much. The chapter explores the boldness and risk of that exchange: clever words can create an opening, yet they can provoke a powerful enemy. The book presents Bilbo’s confidence as developing through the encounter, while showing that his actions have consequences beyond himself and the dwarves.', 4)

heading(2, 'Wisdom amid conflict')
paragraph('The fourth chapter turns to what Bilbo does after the dragon. Competing claims over treasure threaten to turn an achieved quest into another disaster. Bilbo’s choices reveal a different kind of bravery: he tries to prevent violence even when his friends may dislike his method. The author contrasts loyalty to companions with responsibility to people outside the group. Bilbo’s strength is no longer measured only by how far he can travel or what danger he can survive, but by the judgment he brings to a tense situation.', 5)

heading(2, 'Returning changed')
paragraph('The conclusion sees Bilbo’s journey as more than a trip from the Shire to a mountain and back. His courage grows alongside his understanding of limits, friendship and the cost of greed. The familiar home remains meaningful, yet Bilbo returns with a wider sense of what the world contains and what he can do within it. The book invites readers to notice how Tolkien uses a small, reluctant figure to make large questions about change feel personal.', 6)

(root / 'short_content.html').write_text(str(soup) + '\n', encoding='utf-8')
print(len(article.get_text(' ', strip=True).split()), 'words')
