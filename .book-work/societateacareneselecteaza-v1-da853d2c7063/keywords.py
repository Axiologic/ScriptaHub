from pathlib import Path
import sys,json,hashlib
sys.path.insert(0,'tools');import build_books as b
w=Path(__file__).parent;mp=w/'book/manifest.json';m=json.loads(mp.read_text());p=w/'book/en/short_content.html';text=b.keyword_source_text(p)
terms='''fertility|personality|genetic selection|cultural selection|social filtering|demographic selection|reproductive success|heritable variation|family norms|local demographic decline|species extinction|age structures|migration|cultural pluralism|partner markets|opportunity cost|care infrastructure|prestige|assortative mating|first birth|cooperative care|grandparents|after-school care|housing|transport policy|professional mobility|family formation|reproductive consequences|flexible working hours|personal reputation|bureaucracies|audits|cultural norms|nonconformity|heritability|genetic differences|measurement invariance|national stereotypes|China|India|rice agriculture|cooperation hypothesis|clan research|institutional persistence|genetic causation|family systems|self-selection|socialization|occupational niches|evidence appendix|cross-cultural instruments|longitudinal changes|niche diversity|Big Five|Tsimane|subsistence community|statistical personality dimensions|institutional complexity|reproductive continuity|psychopathy|paranoia|psychiatric diagnoses|clinical assessment|reproductive effects|accountability|transparency|reputational feedback|threat calibration|persecutory beliefs|mental-health risks|minority communities|urbanicity|residential selection|polygenic architecture|mutation|genetic composition|reproductive freedom|disabilities|mental disorders|meritocratic megacity|neo-tribal archipelago|metropolis of proximity|algorithmic reproduction|ranking systems|genetic scoring|care|intermediate communities|reproductive preferences|desired and realized fertility|childlessness'''.split('|')
assert len(terms)==90,len(terms)
for t in terms:assert b.keyword_normalise(t) in b.keyword_normalise(text),t
m['keywordReview']={'sourceHash':hashlib.sha256(p.read_bytes()).hexdigest(),'phrases':terms,'method':'Active-LLM reviewed source phrases after NLTK candidate extraction; no topic vocabulary added to shared code.'};mp.write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n')
# Keep incremental localisation isolated from other agents' global generated cache.
cache=w/'keyword-translations.json'
if not cache.exists():cache.write_bytes(b.KEYWORD_TRANSLATION_CACHE.read_bytes())
b.KEYWORD_TRANSLATION_CACHE=cache
print('Reviewed 90 source phrases; rebuilding only own staged manifest',flush=True)
b.rebuild_keywords([mp])
