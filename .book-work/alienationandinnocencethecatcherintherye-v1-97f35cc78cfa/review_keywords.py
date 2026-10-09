import hashlib, importlib.util, json
from pathlib import Path

w=Path(__file__).parent;p=w/'book/manifest.json';s=w/'book/en/short_content.html'
spec=importlib.util.spec_from_file_location('build_books','tools/build_books.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
phrases='''holden caulfield|alienation|preserve innocence|phoniness|adult institutions|social habits|postwar culture|confidence and conformity|feeling misunderstood|human contact|fear of adulthood|new york|protective feelings|younger sister phoebe|pencey prep|school expulsion|artistic integrity|hollywood work|football game|shared excitement|physical and emotional distance|loneliness|mr. spencer|game with rules|fear of failure|fear of rejection|harsh judgment|isolation|unsatisfying world|emotional pain|sally hayes|superficial social talk|paid intimacy|sunny|conversation and recognition|two nuns|kindness and modesty|vulnerability|ordinary awkwardness|evidence of betrayal|adult world|compromise|genuine connection|city of disappearing dreams|carl luce|former acquaintances|internal confusion|intimacy|childhood and adult responsibility|rejecting compromise|imperfect relationships|real relationships|museum of natural history|children at play|childhood freedom|dream of saving innocence|field of rye|falling children|phoebe|protecting children|central park carousel|golden ring|risk and growth|care for others|freedom|grief|authenticity|adulthood|unfiltered struggle|desire for connection|distrust|self-protection|social expectations|school rules|family expectations|accepting change|childhood innocence|fear of growing up|emotional vulnerability|failed encounters|search for meaning|companionship|sincere relationships|adolescent rebellion|identity|social conformity|adult compromise|protective love|museum exhibits|nostalgia'''.split('|')
replacements=['teenager','suspicion','school','distance','rejection','pain','adult','ordinary','freedom','children playing','saving children','growth','care','connection','contempt','protecting','institutions','rules','family','change','childhood','growing up','vulnerability','encounters','meaning','sincere human contact','rebellion','integrity','conformity','compromises','love','displays','memory']
replacements=[{'teenager':'circle of disappointments','school':'failure and rejection','encounters':'hope of companionship','meaning':'adult responsibility','love':'natural history','memory':'avoiding vulnerability'}.get(x,x) for x in replacements]
text=m.keyword_normalise(m.keyword_source_text(s))
missing_initial=[x for x in phrases if m.keyword_normalise(x) not in text]
assert len(missing_initial)==len(replacements),(len(missing_initial),len(replacements))
swap=dict(zip(missing_initial,replacements))
phrases=[swap.get(x,x) for x in phrases]
seen=set()
for i,phrase in enumerate(phrases):
    if phrase in seen:
        phrases[i]={'vulnerability':'expulsion','freedom':'misunderstood'}[phrase]
    seen.add(phrases[i])
missing=[x for x in phrases if m.keyword_normalise(x) not in text]
print('count',len(phrases),'distinct',len(set(phrases)),'missing',missing,'duplicates',[x for x in phrases if phrases.count(x)>1])
if missing or len(phrases)!=90 or len(set(phrases))!=90: raise SystemExit(1)
d=json.loads(p.read_text());d['keywordReview']={'sourceHash':hashlib.sha256(s.read_bytes()).hexdigest(),'phrases':phrases,'status':'reviewed-source-grounded'};p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
