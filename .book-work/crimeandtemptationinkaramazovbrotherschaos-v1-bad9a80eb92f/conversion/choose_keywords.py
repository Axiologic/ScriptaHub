"""Review ninety source-occurring search concepts from the short reader."""
import hashlib, importlib.util, json
from pathlib import Path

spec=importlib.util.spec_from_file_location('b','tools/build_books.py')
b=importlib.util.module_from_spec(spec);spec.loader.exec_module(b)
w=Path(__file__).resolve().parents[1];reader=w/'book/en/short_content.html';mp=w/'book/manifest.json'
source=b.keyword_normalise(b.keyword_source_text(reader))
phrases='''Fyodor Pavlovich Karamazov
Dmitri
Ivan
Alyosha
Grushenka
Karamazov family
family conflict
rivalry and resentment
Fyodor’s murder
murder
shared guilt
moral responsibility
passion
reason
faith
suffering
redemption
desire and restraint
pleasure
power
moral limit
crime
betrayal
violation of law
responsibility
forgiveness
moral confusion
private conflicts
public tragedy
selfish father
greed and lust
religious certainty
spiritual care
inherited wrongdoing
moral damage
inheritance
Grushenka’s affection
violence and recklessness
arrest and trial
false accusation
philosophical doubt
detachment
family’s collapse
Grand Inquisitor
innocent suffering
pain of children
future harmony
Spanish Inquisition
freedom
security and certainty
good or evil
compassion
intellectual proof
the devil
guilt
doubt
madness
human feeling
connection
survival guide
patient care
spiritual resilience
self-protection
repair after harm
temptation
tensions
father’s example
novel’s central events
moral questions
passion, reason, and faith
search for redemption
competing responses to suffering
person who performs an act
consequences
rebellion
wish to question every moral limit
intellect
earlier choices
thought and love
thought
love
faith and reason
faith and compassion
hope and connection
seek forgiveness
trial
family
rebellion against innocent suffering
encounter with the devil
three ways through chaos'''.splitlines()
assert len(phrases)==90,len(phrases)
missing=[p for p in phrases if b.keyword_normalise(p) not in source]
assert not missing,missing
m=json.loads(mp.read_text());m['keywordReview']={'sourceHash':hashlib.sha256(reader.read_bytes()).hexdigest(),'phrases':phrases,'reviewedOn':'2026-10-08','method':'editorial source-occurrence review of English ten-minute reader'}
mp.write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n')
print('selected',len(phrases),'source-derived keywords')
