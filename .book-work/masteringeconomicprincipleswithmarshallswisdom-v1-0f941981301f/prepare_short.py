from pathlib import Path

from bs4 import BeautifulSoup

root = Path(__file__).parent / 'book/en'
soup = BeautifulSoup(
    '<!doctype html><html lang="en"><head><meta charset="utf-8">'
    '<meta name="viewport" content="width=device-width,initial-scale=1">'
    '<title>Mastering Economic Principles with Marshall’s Wisdom — Ten-minute edition</title>'
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


heading(1, 'Mastering Economic Principles with Marshall’s Wisdom')
paragraph('This book introduces Alfred Marshall’s tools for understanding choices made under scarcity. It moves from supply and demand through market equilibrium and theories of value, then asks how these ideas can inform decisions in business and public policy. The author treats economic models as useful explanations, while noting that human behavior and social conditions complicate simple diagrams. The point is to ask what changes when prices, costs, preferences or institutions shift, and who experiences those changes.')

heading(2, 'Starting with ordinary choices')
paragraph('The introduction places economics in daily life: households choose what to buy, firms decide what to produce, and governments weigh competing uses of limited resources. Rather than presenting a market as an abstract machine, it asks readers to notice the trade-offs behind visible prices. Marshall’s framework offers a vocabulary for those choices. The book also asks readers to consider ethical and social effects, since an efficient transaction does not settle every question about access or fairness.', 1)

heading(2, 'Supply, demand and elasticity')
paragraph('Chapter one explains the two familiar sides of a market. Demand describes how much buyers are willing to purchase at different prices; supply describes how much sellers are willing to offer. A change in either can move the price and quantity of a good. The chapter introduces elasticity to show that not every response has the same size. People may sharply reduce purchases of one item when its price rises, while changing their use of a necessity only a little. Businesses can use these patterns to plan production, and consumers can use them to interpret changing prices.')
paragraph('Marginal thinking adds another layer. A decision often turns on the benefit and cost of one additional unit, not on the total value of everything already bought or produced. The book uses this idea to connect personal choices with market behavior.', 2)

heading(2, 'Equilibrium as a moving relationship')
paragraph('The second chapter describes market equilibrium as the point where planned purchases and sales meet at a price. When a price is too high, unsold goods may push sellers to adjust; when it is too low, shortages may prompt buyers to compete. The price mechanism can coordinate many separate choices, though real markets may respond slowly or unevenly. The chapter also considers consumer and producer surplus as ways to describe gains from exchange. Competition matters because the number and power of market participants shape how those gains are divided.', 3)

heading(2, 'What gives something value?')
paragraph('Chapter three turns to the difference between usefulness, scarcity and market price. A good may be useful yet cheap when plentiful, while a rare object may command a high price. Preferences and marginal utility influence what buyers will pay; production costs affect what sellers can offer. The author uses Marshall’s approach to avoid reducing value to a single cause. A market price emerges from interacting conditions, so understanding it requires attention to both sides of the exchange.')
paragraph('This makes the model more useful for actual decisions. A business cannot set a durable price by looking only at its costs, and a buyer cannot infer intrinsic worth from price alone. Both need to understand alternatives, constraints and changes in demand.', 4)

heading(2, 'Applying principles beyond a diagram')
paragraph('Chapter four applies the framework to business choices, public policy and social problems. Firms may use demand and cost information when choosing output or prices. Policymakers can examine how taxes, rules or assistance programs change incentives and access. The book points out that economic reasoning is helpful precisely because interventions can have effects beyond their first target. It also urges readers to consider distribution: a market outcome can benefit participants unequally, and some people may be left without essential resources.')
paragraph('The chapter does not present a single policy recipe. It encourages readers to identify assumptions, examine evidence and ask which groups bear costs or receive benefits.', 5)

heading(2, 'Why the framework endures')
paragraph('The conclusion argues that Marshall’s principles remain useful even as technology and institutions change. Scarcity, incentives and trade-offs still appear in new industries, but their specific forms must be studied rather than assumed. The book closes by linking economic literacy to better questions: what caused a price to change, who can adapt, which costs are hidden and what a proposed solution might change elsewhere? Those questions make the framework a tool for judgment, not a substitute for it.', 6)

(root / 'short_content.html').write_text(str(soup) + '\n', encoding='utf-8')
print(len(article.get_text(' ', strip=True).split()), 'words')
