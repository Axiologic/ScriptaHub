from html import escape
from pathlib import Path

root = Path('.book-work/aristotlethephilosopherwhoshapedwesternthought-v1-255163137d22')
sections = [
('introduction', 'A thinker across disciplines', [
"Aristotle's work reached biology, physics, ethics, politics, logic, and metaphysics. The introduction asks why ideas formed in ancient Greece still matter after many particular scientific claims have been revised. The book follows the methods as well as the conclusions: observation, classification, argument, and a search for causes.",
"The chapters place those ideas within his life before tracing their influence on later thought. They invite readers to see how one thinker could cross fields that modern institutions usually separate."
]),
('life', 'Stagira, Athens, and the Lyceum', [
"Born in Stagira in 384 BCE, Aristotle studied in Plato's Academy and later tutored Alexander. He departed from Plato's emphasis on abstract forms by giving direct observation of the world a larger role. In Athens he founded the Lyceum, where students investigated nature, politics, and reasoning.",
"His career unfolded amid Macedonian power and Athenian suspicion. The chapter presents his institutions and political circumstances alongside his intellectual development, showing that philosophical work had a social setting."
]),
('science', 'Observing nature and explaining change', [
"Aristotle classified living things and studied their structures and habits through observation. His natural philosophy also sought explanations of motion, matter, and celestial order. Many conclusions were later displaced, but his attempt to organize evidence and ask systematic questions shaped centuries of inquiry.",
"The four causes distinguish material, form, agent, and purpose in an explanation. The chapter uses them to show what Aristotle meant by understanding a thing, while noting how later science changed the answers to many of his questions."
]),
('ethics-politics', 'Virtue within a community', [
"In ethics, Aristotle connects human flourishing, or eudaimonia, with habits of character and practical wisdom. Virtue is learned through repeated action, not merely known as a rule. The good life therefore depends on judgment about particular situations and on the communities in which people live.",
"His political writing compares forms of government and asks which serve a common good. Education, citizenship, and the limits of different constitutions link personal character to public institutions."
]),
('metaphysics', 'What makes a thing what it is?', [
"The metaphysics chapter asks about substance, change, potentiality, and actuality. Aristotle seeks to explain how things can become different while remaining intelligible. Form and matter are not treated as separate worlds; they help account for particular objects and living beings.",
"His account of an unmoved mover extends the inquiry toward ultimate explanation. The book treats these concepts as parts of a sustained attempt to make reality understandable through connected principles."
]),
('logic', 'From propositions to conclusions', [
"Aristotle's logical work examines propositions, categories, syllogisms, and the conditions under which a conclusion follows from premises. It gave later thinkers a formal vocabulary for testing arguments. He also asked how knowledge begins with perception and develops through reason.",
"Modern logic has moved beyond syllogisms, but the book shows why the discipline's earlier questions still matter: what makes an inference valid, how does evidence support knowledge, and where can reasoning fail?"
]),
('conclusion', 'A durable method of questioning', [
"Aristotle's answers were not all lasting answers. The conclusion instead emphasizes the scale of his inquiries and the long history of responses to them. His legacy includes both ideas that endured and claims later investigators had to challenge.",
"Readers can follow that tension through the five chapters: a philosopher who shaped Western thought precisely because his questions, classifications, and arguments gave others something substantial to test and revise."
]),
]
title = 'Aristotle: The Philosopher Who Shaped Western Thought'
parts = []
for slug, heading, paras in sections:
    body = '\n'.join(f'<p>{escape(para)}</p>' for para in paras)
    parts.append(f'<section id="{slug}"><h2>{escape(heading)}</h2>\n{body}\n<p><a href="full_content.html#{slug}">Read this chapter in the complete edition</a></p></section>')
output = f'<!doctype html>\n<html lang="en"><head><meta charset="utf-8"><title>{escape(title)} — Ten-minute edition</title></head><body><article>\n<h1>{escape(title)} — Ten-minute edition</h1>\n' + '\n'.join(parts) + '\n</article></body></html>\n'
(root / 'book/en/short_content.html').write_text(output, encoding='utf-8')
print(sum(len(p.split()) for _, _, paras in sections for p in paras), 'words')
