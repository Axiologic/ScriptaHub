from html import escape
from pathlib import Path

root = Path('.book-work/thenikolateslastorythealternatingcurrentofdestiny-v1-26cc062649aa')
sections = [
('introduction', 'A life at the intersection of invention and ambition', [
"Nikola Tesla changed how electricity could be generated, transmitted, and used. This book follows his alternating-current system alongside his experiments, rivalries, hopes, and personal difficulties. It treats the celebrated inventor as a person whose ideas required machines, funding, public demonstrations, and sometimes years of struggle to become practical.",
"The chapters move from a thought experiment about a world without Tesla to his childhood, technical breakthroughs, social impact, conflict with Edison, controversies, philosophy, and private life. The story asks how imagination and scientific work can serve society without losing sight of the limits and costs of innovation."
]),
('no-tesla-no-progress', 'What if Tesla had not contributed?', [
"The opening chapter imagines modern life without Tesla's work. Direct current might have remained dominant longer, limiting efficient transmission over great distances and slowing the spread of large electrical grids. The account also connects his work to motors, wireless experiments, and technologies that later shaped industry and daily life.",
"This counterfactual is a way to assess influence, not a claim that one person created every later advance. Tesla's ideas mattered because they offered workable paths for distributing power and because others could build upon them. The chapter uses that dependence to ask how invention becomes shared infrastructure."
]),
('early-life', 'From Smiljan to New York', [
"Tesla was born in Smiljan in a Serbian family. His father was a priest; his mother had a remarkable memory and practical inventive skill. Education in the Austrian Empire strengthened his fascination with electricity, and demonstrations by a physics professor helped direct his interests.",
"Work and study took him through several European cities before he arrived in New York with a recommendation addressed to Thomas Edison. The chapter shows the formation of a mind that could visualize devices in detail while seeking a place to test those visions."
]),
('scientific-breakthroughs', 'Rotating fields and wireless experiments', [
"Tesla's polyphase alternating-current system produced rotating magnetic fields and made efficient induction motors possible. Its use at Niagara Falls in 1895 marked a turning point in large-scale electricity distribution. The book also describes his high-frequency work, the Tesla coil, radio-related experiments, wireless lighting, and a remotely controlled boat.",
"Wardenclyffe embodied his ambition to transmit energy wirelessly, but financial problems stopped its completion. Other ideas, from the bladeless turbine to aircraft and directed-energy concepts, show the breadth of his interests. The chapter separates practical achievements from proposals that remained unrealized."
]),
('impact-on-society', 'Electric power changes ordinary life', [
"Alternating-current networks helped bring electric lighting and appliances into homes while supplying more reliable power to factories. Induction motors changed industrial processes, and transmission over distance expanded where factories and communities could be built. The chapter links electrical engineering to daily convenience, work, and urban growth.",
"Tesla also pursued wireless communication and power. Some ideas inspired later research; others could not be completed as he imagined. The social impact of invention lies partly in the systems and institutions that turn a device into a service used by many people."
]),
('war-of-currents', 'Tesla, Edison, and competing systems', [
"Edison's direct-current system worked over shorter distances but lost efficiency across long routes. Tesla's alternating current could be transformed between voltages, carried farther, and distributed more widely. The conflict between the systems involved technical arguments, business interests, and fierce public campaigns about safety.",
"Edison's side used demonstrations that portrayed AC as dangerous, while Tesla and Westinghouse continued to develop and promote its advantages. AC ultimately became the standard for broad power distribution. The chapter also contrasts Edison's incremental practice with Tesla's more visionary style, without making the outcome a simple contest between two personalities."
]),
('challenges', 'Funding, credit, and controversy', [
"Tesla often struggled to finance his work. His ambitions for wireless power, especially Wardenclyffe, exceeded what investors would sustain. Disputes over radio patents and public credit added to his frustration; recognition of some claims came only after his death. The book also examines his proposed particle-beam weapon and the gap between publicity and a working device.",
"In later years, compulsive habits, isolation, and debt became more prominent. Tesla died in New York in 1943. The chapter refuses to reduce his life to either triumph or failure: extraordinary inventions coexisted with unrealized projects and the practical difficulty of bringing bold ideas into use."
]),
('philosophies', 'The imagination behind the machines', [
"Tesla described invention as a process of intense mental visualization before building a prototype. Solitude and relentless work shaped his method, while public performances helped draw attention to his ideas. He imagined cleaner, abundant energy, wireless communication, automation, and an expanded role for women in society.",
"The chapter also traces his reverence for nature, spiritual language, and belief in broad education. Some predictions were prescient; other ideas remain speculative. His philosophy joined scientific curiosity to a hope that technology could reduce labor and improve human life, even when financial and technical realities resisted him."
]),
('personal-life', 'Family, habits, and solitude', [
"Tesla credited his mother Đuka Mandić's memory and inventiveness as an influence. His father Milutin hoped he would enter the clergy, but Tesla chose engineering. The account presents his extraordinary concentration alongside personal routines, phobias, and a preference for solitude.",
"His private life complicates the familiar image of an effortless genius. Relationships, health, habits, and money shaped what he could accomplish. He spent his final years alone in a New York hotel, a stark contrast with the enormous public reach of the electrical systems associated with his name."
]),
('conclusion', 'What Tesla’s story leaves us', [
"Tesla's legacy is visible in electrical systems and in the habit of asking what technology might become. The book shows how his imagination helped transform energy distribution, while his unfinished projects reveal the need for resources, cooperation, testing, and restraint.",
"His life invites admiration without requiring a flawless hero. The conclusion asks readers to balance scientific ambition with ethical judgment and to remember the human circumstances behind technical change."
]),
]
title = 'The Nikola Tesla Story: The Alternating Current of Destiny'
parts = []
for slug, heading, paras in sections:
    body = '\n'.join(f'<p>{escape(para)}</p>' for para in paras)
    parts.append(f'<section id="{slug}"><h2>{escape(heading)}</h2>\n{body}\n<p><a href="full_content.html#{slug}">Read this chapter in the complete edition</a></p></section>')
output = f'<!doctype html>\n<html lang="en"><head><meta charset="utf-8"><title>{escape(title)} — Ten-minute edition</title></head><body><article>\n<h1>{escape(title)} — Ten-minute edition</h1>\n' + '\n'.join(parts) + '\n</article></body></html>\n'
(root / 'book/en/short_content.html').write_text(output, encoding='utf-8')
print(sum(len(p.split()) for _, _, paras in sections for p in paras), 'words')
