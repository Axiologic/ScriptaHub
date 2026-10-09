from html import escape
from pathlib import Path

root = Path('.book-work/sg1universe-v1-bfc743ba8543')
sections = [
('introduction', 'A gate into a fictional galaxy', [
"Stargate SG-1 begins with an ancient device that opens wormholes between distant worlds. A team from Earth uses it to meet alien societies, confront threats, and uncover a history that joins ancient mythology to science fiction. The book introduces the characters and the setting before examining its social and political ideas.",
"The Goa'uld pose as gods and control human populations, while the Asgard, the Jaffa, and the Ancients offer different models of power and knowledge. Interstellar travel becomes a way to ask how contact changes both visitors and the worlds they enter."
]),
('anthropology', 'Cultures carried across worlds', [
"The first chapter reads the series through anthropology. Human-descended societies retain echoes of Earth's languages, beliefs, and customs, yet develop differently under alien rule. The Goa'uld's use of religion to dominate people turns familiar myths into stories about enslavement and cultural manipulation.",
"The Jaffa struggle for identity after generations of service to false gods. Tollan restraint and Asgard protection raise another problem: how should a more advanced society relate to one that is still developing? The book connects these fictional encounters to colonialism, cultural preservation, and first contact."
]),
('science', 'Ancient devices and modern questions', [
"The Stargate itself joins lost engineering to wormhole travel. Naquadah powers weapons and other devices, while artifacts left by the Ancients invite the SG-1 team to combine archaeology, languages, physics, and engineering. Daniel Jackson and Samantha Carter show why no single discipline can solve every problem.",
"Alien technology can heal, transport, and defend, but it can also be weaponized or used before its consequences are understood. The chapter treats these inventions as science-fiction thought experiments about discovery, risk, secrecy, and scientific responsibility."
]),
('governance', 'Power after the gate opens', [
"Earth's secret Stargate program raises questions about who controls knowledge and who shares the benefits of alien technology. As the planet becomes more influential, its leaders must negotiate with the Tok'ra, Asgard, and Free Jaffa Nation while balancing self-interest against wider responsibilities.",
"The Goa'uld Empire represents rule by fear and religious manipulation. The Jaffa rebellion shows that overthrowing an oppressor is only the first step; self-government requires new institutions and a changed sense of identity. Asgard non-interference and Earth's emerging alliances keep the ethics of intervention unsettled."
]),
('adventures', 'The ideas inside the adventures', [
"The last chapter revisits story arcs involving Apophis, the Replicators, the Goa'uld System Lords, Daniel Jackson's ascension, the Ori, Atlantis, and time travel in 'Moebius.' Battles and discoveries give the series momentum, but each also tests loyalty, belief, technological control, or the use of power.",
"The conclusion brings anthropology, speculative science, and galactic diplomacy together. It presents SG-1 as an adventure setting that can prompt readers to consider how knowledge, freedom, and responsibility might travel with humanity beyond Earth."
]),
]
title = 'SG 1 Universe'
parts = []
for slug, heading, paras in sections:
    body = '\n'.join(f'<p>{escape(para)}</p>' for para in paras)
    parts.append(f'<section id="{slug}"><h2>{escape(heading)}</h2>\n{body}\n<p><a href="full_content.html#{slug}">Read this chapter in the complete edition</a></p></section>')
output = f'<!doctype html>\n<html lang="en"><head><meta charset="utf-8"><title>{escape(title)} — Ten-minute edition</title></head><body><article>\n<h1>{escape(title)} — Ten-minute edition</h1>\n' + '\n'.join(parts) + '\n</article></body></html>\n'
(root / 'book/en/short_content.html').write_text(output, encoding='utf-8')
print(sum(len(p.split()) for _, _, paras in sections for p in paras), 'words')
