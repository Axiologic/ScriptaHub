import hashlib, importlib.util, json
from pathlib import Path

w=Path(__file__).parent
p=w/'book/manifest.json';s=w/'book/en/short_content.html'
spec=importlib.util.spec_from_file_location('build_books','tools/build_books.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
phrases='''release from prison|escape from poverty|political liberation|rigid moral code|private choices|social structures|removal of restraints|changed identity|social stigma|collective action|immediate victory|mercy and sacrifice|punishment and judgment|chains to redemption|stealing bread|hungry family|justice without compassion|ex-convict|work and shelter|Bishop Myriel|food and lodging|candlesticks|unexpected forgiveness|new name|respected life|Inspector Javert|transformation|new identity|generosity|shadow of judgment|cost of poverty|movement toward redemption|daughter Cosette|invented expenses|child outside marriage|factory job|double standard|sale of her hair|cruel social order|vulnerable woman|desperate acts|personal resilience|system of injustice|Paris barricades|young revolutionaries|justice|equality|democratic future|youthful idealism|skepticism|solidarity|moral choice|rebellion|adopted daughter|wounded Marius|sewers of Paris|personal rescue|collective struggle|immediate political change|later generations|price of revolt|final sacrifice|criminals cannot change|strict belief|absolute view of law|form of captivity|inflexible mind|moral complexity|quieter sacrifice|convict past|withdraws from Cosette|isolation|peaceful end|selflessness|cycles of punishment|cost imposed by shame|failed rebellion|compassion matters|humanity beyond labels|social change|love for Cosette|sacrifices|society|law|freedom|political freedom|forgiveness|redemption|poverty|sacrifice'''.split('|')
norm=m.keyword_normalise(m.keyword_source_text(s))
missing=[x for x in phrases if m.keyword_normalise(x) not in norm]
dups=[x for x in phrases if phrases.count(x)>1]
print('count',len(phrases),'distinct',len(set(phrases)),'missing',missing,'dups',dups)
if len(phrases)!=90 or len(set(phrases))!=90 or missing:raise SystemExit(1)
d=json.loads(p.read_text());d['keywordReview']={'sourceHash':hashlib.sha256(s.read_bytes()).hexdigest(),'phrases':phrases,'status':'reviewed-source-grounded'}
p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
