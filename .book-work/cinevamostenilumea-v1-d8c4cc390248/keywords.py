from pathlib import Path
import sys,json,hashlib
sys.path.insert(0,'tools');import build_books as b
w=Path(__file__).parent;mp=w/'book/manifest.json';m=json.loads(mp.read_text());p=w/'book/en/short_content.html';text=b.keyword_source_text(p)
terms='''fertility|reproductive success|evolutionary fitness|cultural transmission|cultural retention|heritability|genetic inheritance|genetic correlations|clinical disorder|psychiatric diagnoses|psychopathic traits|impulsivity|manipulation|parental investment|reputation systems|long-term cooperation|empathy|conscientiousness|cognitive ability|family formation|parenting|housing|shared care|professional certification|migration|mixed marriages|fertility convergence|generation lengths|social monogamy|marriage rules|economic advantage|reproductive opportunities|cultural strategies|complex traits|statistical significance|effect sizes|psychological measures|completed fertility|three-generation test|shared environment|genetic structure|founder effects|endogamy|South Asian endogamy|China|agricultural coordination|relational thinking|natural experiment|patrilineal organization|paternal-lineage bottleneck|genetic continuity|ritual violence|Chichén Itzá|population replacement|impulsive aggression|religious communities|schooling|extended families|kinship|autonomy|loneliness|impersonal institutions|matching platform|digital communities|artificial companionship|personalized entertainment|AI curricula|tutoring|alignment|knowledge mediation|Pluralism|hypotheses|procedures for correction|Diversity|neo-tribal archipelago|pronatalist enclaves|family infrastructure|reproductive technology|genetic predictions|population ethics|eugenics|Formal freedom|reproductive neutrality of virtue|careers|information isolation|resilience|defensive power|voluntary exit|moral merit|cost of children'''.split('|')
print('count',len(terms));missing=[t for t in terms if b.keyword_normalise(t) not in b.keyword_normalise(text)];print('missing',missing)
if missing:raise SystemExit(1)
assert len(terms)==90
m['keywordReview']={'sourceHash':hashlib.sha256(p.read_bytes()).hexdigest(),'phrases':terms,'method':'Active-LLM phrase review after NLTK extraction from the final English short reader, including its source map; no title fragments, boilerplate or invented vocabulary.'};mp.write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n')
cache=w/'keyword-translations.json'
if not cache.exists():cache.write_bytes(b.KEYWORD_TRANSLATION_CACHE.read_bytes())
b.KEYWORD_TRANSLATION_CACHE=cache
print('Rebuilding own staged manifest only',flush=True);b.rebuild_keywords([mp])
