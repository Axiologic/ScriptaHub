from html import escape
from pathlib import Path

root = Path('.book-work/lightsofdystopiaunveilingthecyberpunk2077universe-v1-1b33462f1b5e')
sections = [
('introduction', 'Night City as a test of identity', [
"The book reads Cyberpunk 2077 as more than a futuristic setting. Night City makes visible a collision between corporate power, bodily modification, and the search for a self that remains recognizably human. Its streets juxtapose wealth and exclusion, possibility and danger. Every change to a body or mind raises the question of who controls that change and who bears its cost.",
"The introduction frames the game as a way to examine digital consciousness, unequal access to technology, and freedom under corporate rule. The people of Night City live with extraordinary tools, but those tools do not settle the old questions of dignity, connection, or choice. The following chapters move from Soulkiller's promise of digital survival to the institutions and relationships that shape ordinary life."
]),
('soulkiller', 'Soulkiller and the price of digital survival', [
"Arasaka's Soulkiller can preserve a person's memories and personality as data. That possibility invites hope for survival beyond the body, but it also makes identity uncertain. Is an engram the same person, a copy, or something else? Johnny Silverhand's prolonged existence as a digital construct turns the question into a lived problem: he survives, yet lacks the ordinary freedoms of embodied life.",
"The chapter argues that technical capacity cannot answer the ethical questions. A corporation able to store consciousness might also own, alter, or delete it. Digital persons would need rights and protection, while access to the technology could deepen inequality. The prospect of immortality also changes how people understand loss, urgency, and the meaning of finite lives. Soulkiller therefore tests the limits of both technology and the social order that controls it."
]),
('night-city', 'Corporate rule and unequal streets', [
"Night City's corporations do more than sell products. They occupy roles associated with government, shaping work, security, medicine, and everyday opportunity. Arasaka and other powerful firms offer benefits while demanding loyalty and dependence. Their reach makes apparent choices less free than they seem, especially for people who must trade autonomy for survival.",
"The city's visible splendor conceals a sharp class divide. The elite can buy protection and enhancement; marginalized residents face unstable work, violence, and exclusion. V's path through markets, factions, and informal networks shows why people sometimes operate outside formal law. The chapter treats black markets and gang ties as responses to failed institutions, while also acknowledging their dangers. This world exaggerates current concerns about inequality and concentrated economic power."
]),
('identity', 'Bodies, engrams, and personhood', [
"Cybernetic upgrades turn the body into something editable. Minor implants can help people function, while extensive modification raises questions about pressure, autonomy, and unequal access. Viktor Vector's caution contrasts with Militech's treatment of bodies as equipment for combat. The Maelstrom gang shows how far modification can go before familiar ideas of human appearance and identity break down.",
"Johnny's presence in V's mind complicates the boundary between self and other. Delamain and Brendan complicate it again by behaving like beings with feelings and growth, despite being artificial. Doll technology, which lets an AI direct a human body, raises a different problem of consent. Soulkiller promises continuity beyond death, yet its price and corporate ownership can turn existence itself into a commodity. The chapter asks readers to judge personhood by more than biological material alone."
]),
('power', 'Who governs a fragmented society?', [
"The book next studies power after democratic institutions have weakened. Corporations allocate resources and define a person's value through usefulness. Gangs such as Maelstrom and the Voodoo Boys form alternative communities for people left outside corporate protection. They can offer belonging and survival, but violence and exploitation remain part of the same landscape.",
"AI adds another layer of authority. Predictive policing and automated urban planning might promise efficiency, yet their decisions can carry hidden biases and reduce public accountability. When a system classifies, monitors, and directs people, it matters who designed it and who can challenge it. Night City asks whether any part of governance should be delegated to machines when the people affected have little power to object."
]),
('experience', 'Freedom, alienation, and connection', [
"V's choices about skills, implants, and alliances make self-definition a practical struggle. Modification can extend ability, but endless pressure to upgrade can also erode a stable sense of self. Corporate surveillance narrows private life, while Johnny Silverhand's rebellion shows the appeal and limits of resistance. Even rebellion can be sold back as a product by the institutions it opposes.",
"Night City is crowded and hyperconnected, yet its residents often feel isolated. Dollhouses and other services turn intimacy into a transaction; shifting bodies and identities complicate trust. The chapter nevertheless finds friendships, kindness, and communities among the dispossessed. These relationships offer moments of care that cannot be reduced to price or performance. Holding onto imperfect human connection becomes an answer to the city's demand that every person be optimized, categorized, and sold."
]),
('conclusion', 'The dark mirror', [
"The conclusion presents Cyberpunk 2077 as a dark mirror for present tendencies rather than a prediction. Its characters reveal the personal cost of corporate concentration, digital control, and unequal enhancement. Its choices invite players to ask where technology expands agency and where it weakens dignity or intimacy.",
"The book's central question is how to direct technological change while preserving meaningful freedom and connection. It asks readers to notice whose interests shape a tool, whose body or data becomes a resource, and which people are excluded from its benefits. Night City's neon spectacle matters because it makes these human questions difficult to ignore."
]),
]
title = 'Lights of Dystopia: Unveiling the Cyberpunk 2077 Universe'
parts = []
for slug, heading, paras in sections:
    body = '\n'.join(f'<p>{escape(para)}</p>' for para in paras)
    parts.append(f'<section id="{slug}"><h2>{escape(heading)}</h2>\n{body}\n<p><a href="full_content.html#{slug}">Read this chapter in the complete edition</a></p></section>')
output = f'<!doctype html>\n<html lang="en"><head><meta charset="utf-8"><title>{escape(title)} — Ten-minute edition</title></head><body><article>\n<h1>{escape(title)} — Ten-minute edition</h1>\n' + '\n'.join(parts) + '\n</article></body></html>\n'
(root / 'book/en/short_content.html').write_text(output, encoding='utf-8')
print(sum(len(p.split()) for _, _, paras in sections for p in paras), 'words')
