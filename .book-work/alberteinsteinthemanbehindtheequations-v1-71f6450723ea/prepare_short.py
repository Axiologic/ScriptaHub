from html import escape
from pathlib import Path

root = Path('.book-work/alberteinsteinthemanbehindtheequations-v1-71f6450723ea')
sections = [
('without-einstein', 'A world without Einstein?', [
"The book opens by imagining modern science without Albert Einstein. Relativity changed how physicists understand space, time, gravity, and energy; technologies such as GPS must account for effects it describes. His mass–energy relation also shaped later discussions of nuclear energy. The chapter uses this thought experiment to show the reach of his work.",
"It does not suggest that one scientist alone created modern physics. Lorentz, Poincaré, Hilbert, and others worked on related questions. The counterfactual asks how Einstein's particular combination of ideas, persistence, and public influence affected the pace and direction of discovery."
]),
('early-life', 'Curiosity before recognition', [
"Born in Ulm in 1879, Einstein grew up with a strong interest in mathematics and physics. The common story that he was a poor student is misleading; he excelled in subjects that interested him, even while resisting rigid teaching. His education took him to Switzerland, where independent study and friendships helped shape his thinking.",
"He later worked at the Swiss patent office after difficulty finding an academic post. The position gave him a livelihood and space to think about the problems that would transform physics. The chapter treats curiosity, self-direction, and the experience of being an outsider as important parts of his development."
]),
('breakthroughs', 'Relativity, light, and gravity', [
"In 1905, special relativity proposed that the laws of physics are the same for observers moving at constant speed and that light's speed in a vacuum is constant. It changed familiar ideas of time and space and led to the relation E = mc². Einstein also explained the photoelectric effect using light quanta, work for which he received the Nobel Prize.",
"General relativity later described gravity as the curvature of spacetime produced by mass and energy. The book also covers Brownian motion and Einstein's contributions to quantum theory. His thought experiments and willingness to challenge basic assumptions linked these advances, even when he disagreed with later interpretations of quantum physics."
]),
('achievements', 'Testing and extending the theories', [
"The next chapter revisits relativity through its predictions and confirmations, including light bending and black holes. Einstein's work also influenced cosmology, even as his changing view of the cosmological constant became part of the history of the field.",
"He sought a unified field theory but never completed one. This unfinished search matters alongside his successful theories: it reveals both the ambition and limits of a program for explaining nature through coherent principles. The chapter emphasizes the continuing value of experimental tests and clear conceptual questions."
]),
('society', 'Science enters public life', [
"Einstein's ideas reached far beyond laboratories. Relativity helped reshape philosophy and later technologies. His 1939 letter with Leo Szilárd warned President Roosevelt about the possibility of a German atomic bomb, linking scientific knowledge to wartime decisions. The book follows his later concern about nuclear weapons and the responsibilities of scientists.",
"Einstein also became a public symbol of intelligence and used that standing to support civil rights, oppose racism, and speak about peace and justice. The chapter shows how a scientist's public role can carry both influence and difficult moral obligations."
]),
('philosophies', 'Determinism, reason, and justice', [
"Einstein favored a universe governed by causal laws and remained uneasy with interpretations of quantum mechanics that treated chance as fundamental. He sought simple, powerful explanations without confusing simplicity with shallow thinking. Rational analysis and creative intuition both mattered to his scientific method.",
"His wider commitments included pacifism, academic freedom, human dignity, and a more equitable society. He criticized economic inequality and reflected on socialism without turning scientific authority into a complete political program. The chapter presents these positions as part of a life spent asking how knowledge should be used."
]),
('personal-life', 'The experiences behind the work', [
"Einstein's family, education, relationships, and difficulty entering academic life shaped his independence. His work at the patent office and later rise to fame changed the settings in which he pursued ideas. The book considers his personal circumstances alongside the familiar image of scientific genius.",
"As a refugee and public figure during World War II, he faced the consequences of political violence and scientific power. Philosophy remained a lifelong interest, and he kept pursuing unification even when the field moved elsewhere. His motivations joined intellectual curiosity to concern about the human effects of discovery."
]),
('legacy', 'Ideas still in use', [
"General relativity remains central to the study of gravity, black holes, and the large-scale universe. Quantum research still engages with questions Einstein helped frame. Applications and observations continue to test and use his work, showing that a theory's legacy depends on later scrutiny rather than its inventor's reputation alone.",
"His warnings about nuclear weapons and his insistence on scientists' social responsibility remain relevant to discussions of powerful new technologies. The chapter places his scientific legacy beside the ethical debate his life helped sharpen."
]),
('conclusion', 'What lies behind the equations', [
"The book closes with Einstein as both a transformative thinker and a person shaped by education, migration, conflict, and moral choice. His discoveries changed physics, while his public actions show that knowledge travels into institutions and politics.",
"Einstein's story invites readers to question established assumptions, test bold ideas, and consider what obligations come with understanding. The equations matter, but so do the methods and human decisions that carried them into the world."
]),
]
title = 'Albert Einstein: The Man Behind the Equations'
parts = []
for slug, heading, paras in sections:
    body = '\n'.join(f'<p>{escape(para)}</p>' for para in paras)
    parts.append(f'<section id="{slug}"><h2>{escape(heading)}</h2>\n{body}\n<p><a href="full_content.html#{slug}">Read this chapter in the complete edition</a></p></section>')
output = f'<!doctype html>\n<html lang="en"><head><meta charset="utf-8"><title>{escape(title)} — Ten-minute edition</title></head><body><article>\n<h1>{escape(title)} — Ten-minute edition</h1>\n' + '\n'.join(parts) + '\n</article></body></html>\n'
(root / 'book/en/short_content.html').write_text(output, encoding='utf-8')
print(sum(len(p.split()) for _, _, paras in sections for p in paras), 'words')
