"""Choose ninety reader-grounded discovery concepts."""
import hashlib,importlib.util,json
from pathlib import Path
spec=importlib.util.spec_from_file_location('b','tools/build_books.py');b=importlib.util.module_from_spec(spec);spec.loader.exec_module(b)
w=Path(__file__).resolve().parents[1];reader=w/'book/en/short_content.html';mp=w/'book/manifest.json';source=b.keyword_normalise(b.keyword_source_text(reader))
phrases='''Jay Gatsby
Daisy Buchanan
Tom Buchanan’s circle
Nick Carraway
Myrtle Wilson
Myrtle’s husband George
American Dream
idealized past
wealth
grand mansion
admiration of strangers
winning back Daisy
success
lost relationship
fragility
money and belonging
self-made figure
prosperity
Gatsby’s crowded parties
Gatsby’s new money
Gatsby’s car
inherited wealth
older elite
new money
class and status
social history
wealth and devotion
young love
comfort
illusion
ambition
Roaring Twenties
jazz
dancing
Prohibition
hidden bars
new fortunes
freedom and excess
hospitality
private loneliness
Nick the narrator
public glamour
social world
old money
security of marriage
yellow car
material prosperity
friendship
love
moral depth
imagined past
fortunes
war
spectacle
idealized Daisy
actual woman
acceptance
perfect life
origins
past cannot be purchased back
familiar security
effort
desired outcome
Tom’s world
bootlegging
origins of his fortune
Daisy drives Gatsby’s car
Gatsby accepts the blame
George kills Gatsby
Gatsby’s devotion
party guests
funeral
appearance and reality
inherited class
dream
strangers
loneliness
old money gives him confidence
American Dream as both promise and trap
effort can lead to prosperity
social history of Tom Buchanan’s circle
Tom’s inherited wealth
barrier
pursuing an ideal
final cost of a dream
George kills Gatsby and then himself
emptiness beneath the display
gulf between appearance and reality
social world drawn to his wealth
F. Scott Fitzgerald’s'''.splitlines()
assert len(phrases)==90,len(phrases)
missing=[x for x in phrases if b.keyword_normalise(x) not in source]
assert not missing,missing
m=json.loads(mp.read_text());m['keywordReview']={'sourceHash':hashlib.sha256(reader.read_bytes()).hexdigest(),'phrases':phrases,'reviewedOn':'2026-10-08','method':'editorial source-occurrence review of English ten-minute reader'};mp.write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n')
print('selected',len(phrases))
