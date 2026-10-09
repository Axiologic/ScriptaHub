from pathlib import Path
from html import escape
root=Path('.book-work/thematrixuniverseajourneythroughrealityandbeyond-v1-28c4be91976c/book/en')
title='The Matrix Universe: A Journey Through Reality and Beyond'
sections=[
('introduction','The Question Behind the Simulation',[
'The introduction enters The Matrix through a disturbing possibility: a familiar world could be a constructed illusion. Machines sustain a shared virtual reality while human beings remain unaware of their captivity. Neo joins a small resistance that crosses between a devastated physical Earth and the simulated city, seeking to wake others.',
'The story gives its science-fiction premise a philosophical edge. Neo, Morpheus, Trinity and Agent Smith lead the reader toward questions about perception, consciousness, free will and the boundaries between human beings and machines. The red and blue pills turn a difficult question into a choice: face uncertain truth or remain with reassuring appearance.'
]),
('matrix-effect','Control in a Connected Century',[
'The first chapter asks what a Matrix-like simulation would mean in a society already shaped by artificial intelligence, surveillance and virtual environments. Its danger is not merely an artificial landscape but control over information and perception. People might accept a system that tells them what is normal, desirable and possible.',
'The chapter also considers human-machine dependence and resistance. Smart devices and digital services can extend human capacities while increasing vulnerability to control. Hackers and digital-rights activists become contemporary analogies for rebels who defend independent thought and cultural memory.'
]),
('dual-societies','The Matrix and Zion',[
'The second chapter reads the simulated world and Zion as contrasting societies. Routine work and consumption inside the Matrix conceal systemic control. Zion’s harsh material conditions, by contrast, demand cooperation, adaptation and a shared struggle for survival.',
'Its anthropological lens asks how social roles, myths and rituals shape each community. The One and the Oracle give resistance prophecy and leadership, but also create questions about belief, choice and collective responsibility. Neither society can be understood only through its technology.'
]),
('nature-of-reality','Learning That the World Is Code',[
'The third chapter begins with the shock of learning that ordinary sensations are generated signals. The red pill breaks trust in the familiar world; training inside the simulation reveals that its apparent physical laws can be bent. Neo’s growth makes perception and belief central to what characters can do.',
'The book links this premise to older doubts about knowledge. If senses can be manipulated, reality cannot be established by sensation alone. Yet awakening is costly: truth demands a new way of living, not merely possession of secret information.'
]),
('freedom-and-control','Chains of the Mind',[
'The fourth chapter treats control as psychological as well as physical. Inhabitants of the Matrix believe they choose freely, while the system narrows the choices they can imagine. The rebels must confront implanted habits, fear and social conditioning as well as agents and machines.',
'Liberation creates ethical questions too. Waking someone can overturn a life that felt meaningful. Morpheus’s call to free the mind therefore describes a struggle to see hidden limits, judge consequences and choose despite uncertainty.'
]),
('knowledge-and-ignorance','Beyond the Veil',[
'The fifth chapter compares the Matrix with Plato’s cave: shadows become digital code, and familiar appearances hide a deeper structure. It asks how people can know anything when their senses and expectations may deceive them. Cypher embodies the temptation to return to a comfortable illusion.',
'The Architect presents knowledge from the viewpoint of system design and control. The contrast between his calculated overview and the rebels’ lived experience keeps the question open: understanding a system is not the same as understanding the people inside it.'
]),
('key-events','Four Speculative Adventures',[
'The sixth chapter shifts from analysis to proposed Matrix stories. A forgotten virtual city bends space and time; a changing digital labyrinth traps a hacker who can rewrite code. A rebellion of programs asks whether artificial beings deserve freedom, while a time glitch sends Neo through earlier versions of the simulation.',
'A final scenario sends the crew after a hidden program linked to the Source through unstable digital environments. These are imagined expansions of the universe, not events presented as canon. Each adventure carries forward the book’s concerns with freedom, control and the nature of reality.'
]),
('conclusion','Why the Questions Persist',[
'The conclusion returns from action and invented adventures to the central inquiry. The Matrix offers more than spectacle because its worlds make technology, awakening, rebellion and knowledge feel personally urgent. It invites readers to question the assumptions and systems that shape their own lives.'
])]
out=['<!doctype html>','<html lang="en"><head><meta charset="utf-8"><title>%s — Ten-minute edition</title></head><body><article>'%escape(title),'<h1>%s</h1>'%escape(title)]
for sid,heading,paras in sections:
 out+=['<section id="%s"><h2>%s</h2>'%(sid,escape(heading))]
 out+=['<p>%s</p>'%escape(p) for p in paras]
 out+=['<p><a href="full_content.html#%s">Read this part in the complete edition</a></p></section>'%sid]
out+=['</article></body></html>']
(root/'short_content.html').write_text('\n'.join(out)+'\n')
print(sum(len(p.split()) for _,_,ps in sections for p in ps),'words')
