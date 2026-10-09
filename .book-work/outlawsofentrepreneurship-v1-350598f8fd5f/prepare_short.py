from bs4 import BeautifulSoup
from pathlib import Path

base = Path(__file__).parent / 'book/en'
soup = BeautifulSoup('<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Outlaws of Entrepreneurship — Ten-minute edition</title></head><body><article data-reader-content></article></body></html>', 'html.parser')
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
        a = soup.new_tag('a', href=f'full_content.html#chapter-{chapter}')
        a.string = f'Read chapter {chapter} in full'
        tag.append(a)
        tag.append('.')
    article.append(tag)

h(1, 'Outlaws of Entrepreneurship')
p('This book asks how enterprise changes when people work at the edge of accepted rules. Its four chapters move from pirates, smugglers and fraudsters to political rebels, less celebrated innovators, and spectacular business failures. The figures are not all models to imitate. Some exploit gaps in a system; others try to change the system itself; still others show how ambition collapses without sound judgment. By placing these stories together, the book treats entrepreneurship as a source of both possibility and harm. The question running through it is what separates useful disruption from exploitation.')

h(2, 'Shadow entrepreneurs')
p('The opening chapter challenges the familiar image of a lawful founder building a company in a boardroom. Pirates and smugglers also had to organize people, assess risk, move goods, and find customers. They operated in the gaps between formal rules and actual demand. The chapter compares their adaptability with that of later entrepreneurs, while keeping fraud and coercion in view. Their inventiveness could reshape trade, yet their methods could also depend on taking what belonged to others or avoiding obligations that supported a community.')
p('The common feature is not heroism but action under uncertainty. Where large institutions moved slowly or protected narrow interests, shadow operators noticed routes and markets that others ignored. The same skill can serve very different ends. The book invites readers to examine the systems that produce these openings without treating lawbreaking itself as proof of innovation.', 1)

h(2, 'Subversive enterprise')
p('The second chapter shifts to entrepreneurs who deliberately challenge an established order. It discusses political and industrial figures who see existing institutions as obstacles to a different future. The examples include the French revolutionary tradition and Andrew Carnegie’s reorganization of steel production through vertical integration. In each case, the book is interested in the ability to assemble resources, alter production, and spread a new model on a scale that established actors did not expect.')
p('Yet the chapter also resists a simple celebration of disruption. Industrial power can be used to exploit workers and narrow competition, even when it increases output. The “subversive” label therefore describes an effect on the old order, not a moral verdict. Readers are asked to separate the challenge to a stagnant system from the question of who benefits and who bears the cost.', 2)

h(2, 'Quiet innovators')
p('Chapter three argues that change need not arrive through a loud founder or a dramatic public revolt. George Washington Carver’s agricultural work provides one example. He shared practical knowledge with farmers, linking improved crops and soil care to the lives of people who depended on the land. Gordon Moore offers another route: methodical technical work and a view of the future of microprocessors that helped guide an industry. Neither story depends on theatrical rebellion.')
p('These cases broaden the book’s idea of entrepreneurship. A person can alter an economic system by teaching, designing, organizing, or steadily solving a problem. Impact may be distributed across many small decisions rather than concentrated in a single public triumph. The chapter gives space to work that is easy to overlook because its methods are quiet.', 3)

h(2, 'Comeback and collapse')
p('The fourth chapter turns to failure. The South Sea Company becomes an example of speculation detached from productive activity: a privileged trading venture drew investors into a rising share price that its actual business could not justify. When the bubble burst, many lost money. The modern example of WeWork likewise raises questions about rapid growth, valuation, governance, and the limits of a founder’s vision. These episodes sit beside accounts of recovery to show that failure can teach, but it can also cause damage that determination alone cannot undo.')
p('The chapter’s lesson is less about fearing risk than about examining its structure. What claims support an investment? Who can challenge a leader’s assumptions? Does a company create value beyond an exciting story about its future? Resilience matters, but oversight, evidence and accountability shape whether a comeback is possible or a collapse spreads its costs to others.', 4)

h(2, 'Hope, risk and change')
p('The conclusion returns to entrepreneurship as a path marked by uncertainty and potential. It names examples of historic change, then points out that many people who tried to build something new never became famous. It recommends further reading on creative destruction, capitalism, outlaws, debt, inequality and state power; those references widen the frame beyond individual success stories. The book ends by encouraging ambition and learning from mistakes, while its case studies leave readers with a necessary qualification: the promise of change has to be judged alongside its consequences for workers, customers and the wider public.', 5)

(base / 'short_content.html').write_text(str(soup) + '\n', encoding='utf-8')
print(len(article.get_text(' ', strip=True).split()), 'words')
