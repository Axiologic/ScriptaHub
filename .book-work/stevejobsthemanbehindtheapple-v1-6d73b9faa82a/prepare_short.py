from html import escape
from pathlib import Path

root = Path('.book-work/stevejobsthemanbehindtheapple-v1-6d73b9faa82a')
sections = [
('emerging-technologies', 'A speculative look at new technology', [
"The opening asks how Steve Jobs might have approached artificial intelligence, virtual reality, blockchain, and cryptocurrency. It treats these questions as speculation, not as positions he actually took. His established interest in intuitive interfaces provides the basis for imagining new forms of human–computer interaction.",
"The chapter also considers whether technological novelty alone would have persuaded him. Jobs repeatedly connected technical possibilities with a coherent experience for users. That tension between invention and usability frames the life story that follows."
]),
('youth', 'The education of an independent designer', [
"Adopted by Paul and Clara Jobs, Steve grew up near the emerging electronics industry of California. His father's craftsmanship and his own curiosity about machines helped shape his attention to how things worked and looked. Formal education proved a poor fit for some of his interests.",
"At Reed College he explored calligraphy, an influence he later connected with the Macintosh's typography. Friendships, countercultural experiences, and travel formed part of a search for meaning beyond conventional career paths."
]),
('birth-of-apple', 'Jobs, Wozniak, and the personal computer', [
"Steve Jobs and Steve Wozniak brought complementary strengths to their partnership: Jobs emphasized product direction and commercial possibility, while Wozniak built elegant circuits. They developed the Apple I and then the Apple II as personal computing began to move beyond hobbyist circles.",
"The company's growth depended on more than one founder or one machine. The chapter follows early financing, marketing, and organizational decisions that helped turn a small venture into a major computer business."
]),
('design', 'A computer people could approach', [
"The Macintosh made graphical interaction and carefully designed typography central to its appeal. Its mouse, windows, icons, and screen-to-print consistency helped make computing less intimidating to many users. Jobs pressed teams to integrate hardware and software into a single experience.",
"This design philosophy joined simplicity with strong control over details. The chapter follows how aesthetics, engineering, and the user's first impression shaped product choices, even when those choices caused friction inside the company."
]),
('leadership', 'Persuasion and pressure', [
"Jobs's leadership mixed ambitious product goals, compelling presentations, and intense demands on colleagues. His so-called reality distortion field could push teams beyond what they thought possible, but it could also strain working relationships and obscure practical limits.",
"The book examines how his business judgment served a distinctive product vision. It also leaves room for criticism: speed and perfectionism carried costs for the people who worked with him."
]),
('comeback', 'Departure, NeXT, and Pixar', [
"After conflict with Apple leadership, Jobs left the company in 1985. He founded NeXT and helped develop Pixar, building new experience in software, animation, and business leadership while Apple struggled to regain direction.",
"Apple's acquisition of NeXT brought him back. The chapter treats this return as a turning point shaped by failure and revision, not a simple restoration of his earlier role. His later decisions brought focus to a smaller product line."
]),
('industries', 'Products and ecosystems', [
"The iPod paired a portable music player with iTunes, making the surrounding service part of the product. Apple then reshaped mobile computing with the iPhone and extended its approach through the App Store and iPad.",
"The chapter connects these devices to broader changes in music, phones, software distribution, and publishing. Their success depended on coordinated hardware, software, content, and marketing rather than isolated inventions."
]),
('behind-the-myth', 'Family, illness, and contradictions', [
"The familiar public image of Jobs as a visionary can flatten a more complicated person. The book discusses his relationship with his daughter Lisa, his marriage to Laurene Powell Jobs, and the changing demands of family life.",
"It also examines his illness and the choices he made during treatment. His personal strengths and failings belong in the account alongside his products; they cannot be settled by the language of genius alone."
]),
('legacy', 'A wide cultural influence', [
"Jobs influenced entrepreneurship, product design, and the way technology companies speak to customers. His Stanford commencement address offered a public account of work, loss, and mortality that reached beyond the computer industry.",
"The book closes by considering both inspiration and controversy in that legacy. Readers can trace how a vision of accessible computing became a network of devices and services, while asking who helped build it and what it cost."
]),
]
title = 'Steve Jobs: The Man Behind the Apple'
parts = []
for slug, heading, paras in sections:
    body = '\n'.join(f'<p>{escape(para)}</p>' for para in paras)
    parts.append(f'<section id="{slug}"><h2>{escape(heading)}</h2>\n{body}\n<p><a href="full_content.html#{slug}">Read this chapter in the complete edition</a></p></section>')
output = f'<!doctype html>\n<html lang="en"><head><meta charset="utf-8"><title>{escape(title)} — Ten-minute edition</title></head><body><article>\n<h1>{escape(title)} — Ten-minute edition</h1>\n' + '\n'.join(parts) + '\n</article></body></html>\n'
(root / 'book/en/short_content.html').write_text(output, encoding='utf-8')
print(sum(len(p.split()) for _, _, paras in sections for p in paras), 'words')
