from pathlib import Path
from html import escape
root=Path('.book-work/hitchhikersguidetothegalaxy-v1-a51bfc42457d/book/en')
title='Hitchhiker’s Guide to the Galaxy'
sections=[
('introduction','An Ordinary Traveler in an Absurd Cosmos',[
'The introduction follows Arthur Dent from the destruction of Earth into Douglas Adams’s comic universe. Ford Prefect rescues him, a towel becomes essential equipment, and a guidebook advises travelers not to panic. Aliens, improbable technology and a vast mystery turn one person’s disorientation into a space adventure.',
'The book treats this journey as more than a sequence of jokes. Friendship gives Arthur a foothold while cosmic absurdity makes room for questions about meaning, survival and our place in a strange universe.'
]),
('babel-fish','The Babel Fish and Communication',[
'The first chapter examines the Babel Fish, a creature that translates any language instantly. It compares this invention with translation software and wearable devices, asking how frictionless communication could change diplomacy, culture and everyday relationships.',
'Removing language barriers can bring people together, yet differences in speech also carry identity and context. The chapter considers misunderstanding, power and the risk of treating translation as a complete substitute for listening.'
]),
('adams-influence','A New Comic Shape for Science Fiction',[
'The second chapter argues that Adams widened the possibilities of science fiction by pairing large ideas with ordinary irritation and sharp wit. Bureaucratic aliens, unreliable machines and recognizable human habits overturn familiar genre expectations.',
'His accessible humor helped other writers and audiences imagine science fiction as playful as well as thoughtful. The chapter follows his influence through comedy, worldbuilding and the genre’s willingness to laugh at itself.'
]),
('cosmic-comedy','How Cosmic Comedy Works',[
'The third chapter begins with Earth destroyed for a hyperspace bypass. A planetary catastrophe becomes a bureaucratic inconvenience, and Vogon paperwork and terrible poetry make the joke darker. Adams repeatedly sets enormous stakes beside everyday pettiness.',
'Unexpected reversals, understatement and improbable characters keep that contrast alive. The humor does not erase the troubling ideas beneath it: institutions can be indifferent, knowledge can be incomplete, and humanity may not occupy the center of the universe.'
]),
('philosophy','Forty-Two and the Search for Meaning',[
'The fourth chapter considers the answer of forty-two that Deep Thought gives to life, the universe and everything. The absurd result exposes the weakness of asking for a precise answer without understanding the question. Arthur’s journey keeps inquiry alive despite that failure.',
'The Infinite Improbability Drive also challenges familiar ideas about causality and possibility. Characters such as Slartibartfast invite curiosity about creation and purpose. The chapter suggests that meaning may be made through attention, relationships and humor rather than found as one final formula.'
]),
('technology','Useful Tools, Unreliable Systems',[
'The fifth chapter treats technology as a double-edged source of progress. The Babel Fish enables communication, while the Heart of Gold crosses vast distances through improbability. The Guide offers travelers vast information in portable form.',
'Yet devices and systems can fail, mislead or create new dependence. The chapter uses Adams’s inventions to ask whether technical power makes people wiser, and how human judgment can remain active amid convenience and complexity.'
]),
('key-events','The Journey’s Key Events',[
'The sixth chapter maps the opening story: the Vogons destroy Earth, Arthur and Ford escape, and the Heart of Gold rescues them. Zaphod, Trillian and Marvin join the journey toward Magrathea, a planet known for building worlds.',
'There Arthur learns Earth’s hidden purpose in the search for the Ultimate Question. Deep Thought’s answer is forty-two, but the question remains unknown. Mice who commissioned Earth pursue Arthur’s brain, and he escapes without a final explanation.'
]),
('conclusion','Keep Curiosity and a Towel',[
'The conclusion gathers the book’s readings of comedy, philosophy and technology. Adams’s universe asks readers to doubt simple answers and meet uncertainty with curiosity. Its practical advice, “Don’t Panic,” does not solve the mystery; it helps travelers continue through it.'
])]
out=['<!doctype html>','<html lang="en"><head><meta charset="utf-8"><title>%s — Ten-minute edition</title></head><body><article>'%escape(title),'<h1>%s</h1>'%escape(title)]
for sid,heading,paras in sections:
 out+=['<section id="%s"><h2>%s</h2>'%(sid,escape(heading))]
 out+=['<p>%s</p>'%escape(p) for p in paras]
 out+=['<p><a href="full_content.html#%s">Read this part in the complete edition</a></p></section>'%sid]
out+=['</article></body></html>']
(root/'short_content.html').write_text('\n'.join(out)+'\n')
print(sum(len(p.split()) for _,_,ps in sections for p in ps),'words')
