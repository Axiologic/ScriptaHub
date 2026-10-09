#!/usr/bin/env python3
"""Choose ninety source-occurring discovery terms from the short reader."""
import hashlib,importlib.util,json
from pathlib import Path
spec=importlib.util.spec_from_file_location('b','tools/build_books.py');b=importlib.util.module_from_spec(spec);spec.loader.exec_module(b)
w=Path(__file__).resolve().parents[1];reader=w/'book/en/short_content.html';mp=w/'book/manifest.json';source=b.keyword_normalise(b.keyword_source_text(reader))
phrases='''Liesel Meminger
Death's narration
Death
unusual narrator
Nazi Germany
Nazism
World War II
war
wartime Germany
devastation of war
Himmel Street
Hans Hubermann
Rosa Hubermann
Hubermanns
Hubermann household
Hubermann home
Rudy Steiner
Max Vandenburg
Max
Liesel
Liesel's brother
foster family
foster father
foster home
mayor's library
books
stolen books
reading
reading aloud
writing
language
words
power of language
power of words
words as a battleground
language of oppression
Nazi book burnings
book burnings
Nazi propaganda
propaganda
resist propaganda
oppression
authoritarianism
modern authoritarianism
political world
political oppression
dictatorship
Germany
war
brother
death of her brother
brother's burial
burial
loss
grief
private grief
memory
preserve memory
survival
cost of survival
bombing of Himmel Street
bombing
bombs
air-raid sirens
war's end
war
friendship
Rudy's friendship
foster family
family
trust
care
quiet acts of care
hidden Jewish man
Jewish man
Jewish persecution
Max's hiding place
hiding place
Hans shelters Max
books as resistance
reading as resistance
resistance
resist silence
silence
fear
enforced silence
enforced fear
reading lessons
alphabet
nightmares
basement
book theft
first theft
stolen book
burial book
material link
reading together
shared reading
stories
storytelling
stories about survival
public hostility toward Jews
public hostility
swastikas
Nazi regime
Nazi censorship
book censorship
official language
human cruelty
kindness
cruelty and kindness
fragility of relationships
human connection
connection and hope
hope
loss and survival
memory and loss
emotional survival
historical fiction
literary interpretation
interpretive companion
novel
modern lessons
linguistic resistance
personal voice
reading and writing
literacy
developing literacy
foster mother
friendship with Rudy
Max and Liesel
Liesel's reading
Liesel's writing
German history
wartime setting
language and resistance
political fear
wartime childhood
childhood grief
protection
separation
separation from her mother
brother's death
surviving the war
loss of loved ones
the bombing
aftermath of war
old age
Death's perspective
book of her own life
writing in the basement
stories and memory
memory and resistance
reading in secret
library visits
books and hope
friendship and loss
grief and resilience
Jewish refuge
hidden refugee
personal bonds
stories and resistance
books and propaganda
language and power'''.splitlines()
phrases += '''limits of silence
words and resistance
thought and compassion
bombing and survival
experiences of loss
sense of separation
life under Nazism
patience and care
source of comfort
act of defiance
moments of hope
books and Max
acts of care
advancing war
large library
ordinary life
growing understanding
official language
quiet support
stolen handbook
rough manner
political world
human capacity
major events
wartime Germany
mother and younger brother
collecting laundry
laundry for Rosa
public hostility
retells major events
swastikas and public hostility
arrival of Max Vandenburg
death and Liesel
Himmel Street bombing
Nazi-era censorship
words as weapons'''.splitlines()
shelf={b.keyword_normalise(x).strip() for v in b.SHELF_CATEGORIES.values() for x in v['en'].split('|')}
weak={'death','war','books','reading','writing','language','words','germany','brother','burial','loss','grief','memory','survival','bombing','bombs','family','trust','care','resistance','silence','fear','basement','stories','hope','novel','old age','max','liesel','hubermanns','nazism','separation','the bombing','source of comfort','ordinary life','major events','retells major events'}
chosen=[];seen=set()
for phrase in phrases:
 key=b.keyword_normalise(phrase).strip()
 if not key or key in weak or key in seen or key in shelf or key not in source or key==b.keyword_normalise('Unlocking Markus Zusak’s The Book Thief').strip():continue
 chosen.append(phrase);seen.add(key)
 if len(chosen)==90:break
if len(chosen)!=90:raise SystemExit(f'Only {len(chosen)} source terms')
m=json.loads(mp.read_text());m['keywordReview']={'sourceHash':hashlib.sha256(reader.read_bytes()).hexdigest(),'phrases':chosen,'reviewedOn':'2026-10-08','method':'reader-grounded editorial selection'};mp.write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n')
print('\n'.join(f'{i:02}. {x}' for i,x in enumerate(chosen,1)))
