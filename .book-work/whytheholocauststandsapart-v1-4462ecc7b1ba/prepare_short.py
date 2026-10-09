"""Ten-minute synthesis of the authored preface and all six chapters."""

from pathlib import Path
from bs4 import BeautifulSoup

root=Path(__file__).resolve().parent
full=BeautifulSoup((root/'book/en/full_content.html').read_text(), 'html.parser')
out=BeautifulSoup('<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Why the Holocaust Stands Apart — Read in 10 Min</title></head><body><article data-reader-content></article></body></html>', 'html.parser')
article=out.article
h=out.new_tag('h1',id='book-title');h.string='Why the Holocaust Stands Apart — Read in 10 Min';article.append(h)
sections=[
 ('The book’s question', [
  'The book asks why the Holocaust occupies a distinctive place in global memory while other genocides receive unequal attention. Its preface presents remembrance as both a historical and an ethical question: how can societies learn from the Holocaust without neglecting other victims of mass violence? The six chapters compare atrocities, trace European and colonial histories, examine the Holocaust itself, and consider education, law, and public memory.',
  'The author does not argue that one group’s suffering matters more than another’s. Instead, the book examines why evidence, survivor testimony, cultural representation, political choices, and institutions affect which histories become widely known. Its central concern is how remembrance might support vigilance and a more inclusive understanding of genocide.',
 ]),
 ('I. Major genocides of history', [
  'The opening chapter places the Holocaust beside mass atrocities associated with Armenia, Cambodia, Rwanda, Bosnia, and other cases. It looks for recurring mechanisms such as dehumanization, propaganda, organized violence, and failures of outside intervention, while recognizing that each event has its own history. It also asks why some atrocities have entered international consciousness and others remain contested, denied, or poorly documented.',
  'The chapter connects recognition to records, survivors’ voices, political advocacy, courts, and education. It treats prevention as more than the repeated promise of “never again”: institutions and publics must identify warning signs, respond to them, and confront the political reasons for inaction.',
 ]),
 ('II. Europe, values, and risk', [
  'The second chapter asks how European history created conditions that could be exploited by genocidal movements. It discusses empire, nationalism, racial ideology, bureaucracy, and the misuse of ideas presented as scientific or rational. It does not portray genocide as uniquely European; its narrower claim is that particular histories and institutions helped make certain forms of organized persecution possible.',
  'The comparison also tests a tension in the idea of progress. Administrative capacity and technological development can support public welfare, but they can also be turned toward exclusion and violence when political authority rejects the equal humanity of targeted people.',
 ]),
 ('III. Colonial practices', [
  'The third chapter traces how colonial rule normalized racial hierarchies, dispossession, forced labor, and administrative control over subject populations. It presents these practices as relevant background for understanding later forms of mass violence, while keeping the distinct histories of colonial atrocities in view. The author argues that confronting this legacy requires more than naming past crimes: societies must consider how old hierarchies shape present institutions and remembrance.',
 ]),
 ('IV. The Holocaust', [
  'The fourth chapter focuses on Nazi antisemitism, the exclusion of Jews from German civic life, escalating persecution, mass murder, and the bureaucratic organization of the genocide. It discusses the Nuremberg Laws, killing operations, extermination camps, and the Nuremberg trials. The chapter’s emphasis is on how ideology, state authority, administration, and obedience were combined against the targeted population.',
  'The book also considers the postwar influence of the Holocaust on human-rights language, legal accountability, and genocide prevention. It asks readers to examine not only the perpetrators’ decisions but also failures to protect people facing systematic persecution.',
 ]),
 ('V. Why its memory is prominent', [
  'The fifth chapter turns from the event to its public memory. It points to perpetrator records, survivor accounts, diaries, books, museums, films, school teaching, legal proceedings, and sustained advocacy as factors in the Holocaust’s exceptional visibility. It also discusses the role of postwar politics and the creation of Israel in shaping that visibility.',
  'The chapter discusses how testimony, documentation, institutions, and cultural works carry remembrance across generations. It raises a difficult comparison: broad knowledge of the Holocaust can sharpen attention to genocide, yet other atrocities often lack comparable resources for documentation and commemoration.',
 ]),
 ('VI. Lessons and global responsibility', [
  'The final chapter asks what remembrance should demand in practice. It points to the gap between international commitments and continued mass atrocities after the Holocaust. It calls for education that includes different genocides, credible documentation, support for survivor testimony, legal accountability, and responses to denial. Its proposed goal is neither competition among victims nor an easy universal formula, but a broader culture of historical attention and prevention.',
  'The book closes by returning to the preface’s question: societies should preserve the specificity of the Holocaust while recognizing the suffering of other victimized communities. Remembering one atrocity responsibly should strengthen, not narrow, concern for people threatened elsewhere.',
 ]),
]
for idx,(title,paragraphs) in enumerate(sections,1):
 h=out.new_tag('h2',id=f'section-{idx}');h.string=title;article.append(h)
 for value in paragraphs:
  p=out.new_tag('p');p.string=value;article.append(p)
text=article.get_text(' ',strip=True)
assert 700<=len(text.split())<=1200,len(text.split())
source=full.article.get_text(' ',strip=True).lower()
for phrase in ['nuremberg laws','rwanda','colonial','survivor','museums','education']:
 assert phrase in source,phrase
(root/'book/en/short_content.html').write_text(str(out)+'\n')
print('Prepared',len(text.split()),'words in',len(sections),'sections')
