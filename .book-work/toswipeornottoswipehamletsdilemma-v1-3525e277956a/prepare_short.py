from pathlib import Path
from html import escape

root = Path('.book-work/toswipeornottoswipehamletsdilemma-v1-3525e277956a/book/en')
title = 'To Swipe or Not to Swipe: Hamlet’s Dilemma'
sections = [
('relevance','Is Hamlet Still Relevant?',[
"The opening chapter treats Hamlet’s old question as a problem of modern attention. A prince who hesitates over life and death becomes, in the satire, a person unable to choose what to post or stream. Social media, binge watching and abbreviated messages make the original play seem remote, yet Hamlet’s uncertainty begins to look familiar.",
"The jokes do not settle the question of relevance. Beneath the parody lie murder, betrayal, grief and the fear of acting wrongly. The chapter suggests that slow reflection may matter precisely because contemporary culture rewards quick opinions. Its closing invitation is to notice a ‘Hamlet moment’ in everyday indecision."
]),
('madness-or-marketing','Madness as a Public Image',[
"The second chapter imagines Elsinore as a workplace of brands and public relations. Hamlet’s performed madness becomes a changing personal image; Ophelia is recast as an influencer, Polonius as a dispenser of slogans, and Claudius with Gertrude as managers of a blended-family narrative. These are comic analogies, not claims about Shakespeare’s historical intentions.",
"The play within the play is treated as shareable media designed to expose the king. The satire asks whether a public persona can obscure grief and moral uncertainty. Hamlet’s shifting roles resist the consistent message that modern marketing demands, while the lasting fame of the tragedy becomes the final joke about a ‘legacy brand.’"
]),
('hamletonomics','The Revenge Economy',[
"Hamletonomics turns the tragedy into an intentionally absurd economic thought experiment. Fencing supplies weapons makers; surveillance creates watchers; Ophelia’s flowers help florists; hidden passages employ carpenters; actors, grave diggers and sellers of poison all gain business. Even the ghost is credited with starting the chain of events.",
"The chapter extends the joke to diplomacy, funerals and Fortinbras’s takeover. It is not an economic model of Denmark but a way to inspect how revenge sends consequences through an entire court. Every new ‘growth market’ also reminds the reader of the violence and loss that the cheerful language tries to hide."
]),
('hamlet-2','Hamlet 2.0',[
"A digital remake puts soliloquies on video platforms, moves the ghost into social feeds and offers an app for every dilemma. Hamlet could poll his followers, launch a viral challenge against Claudius or outsource grave digging. The chapter pushes the conceit through gig work, space fantasy and a fictional startup.",
"Its sharpest alternative is quieter: a therapist might understand Hamlet’s vision of his father as unresolved grief rather than an order for revenge. The comic upgrades therefore raise a serious question about what technology can solve and what still requires human judgment and care."
]),
('conclusion','A Bridge Back to the Play',[
"The conclusion explains the purpose of the parody. Shakespeare’s language and slow dramatic rhythm can feel distant to readers accustomed to short digital forms, although the play’s concerns with identity, morality and power remain close. Familiar platforms and jokes offer a point of entry without replacing the original text.",
"Humor can make the unfamiliar approachable and invite comparison between court intrigue and online conflict. The book asks readers to use these parallels critically, then return to Hamlet itself. Its central question is whether contemporary readers will choose to engage with classical literature—and what they may discover when they do."
]),
]
out=['<!doctype html>','<html lang="en"><head><meta charset="utf-8"><title>%s — Ten-minute edition</title></head><body><article>'%escape(title),'<h1>%s</h1>'%escape(title)]
for sid,heading,paras in sections:
 out += ['<section id="%s"><h2>%s</h2>'%(sid,escape(heading))]
 out += ['<p>%s</p>'%escape(p) for p in paras]
 out += ['<p><a href="full_content.html#%s">Read this part in the complete edition</a></p></section>'%sid]
out += ['</article></body></html>']
(root/'short_content.html').write_text('\n'.join(out)+'\n')
print(sum(len(p.split()) for _,_,ps in sections for p in ps),'words')
