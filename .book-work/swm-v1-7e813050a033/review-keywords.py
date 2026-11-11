from pathlib import Path
import json,hashlib,sys
sys.path.insert(0,'tools')
from build_books import keyword_source_text,keyword_normalise,SHELF_CATEGORIES
w=Path('.book-work/swm-v1-7e813050a033');p=w/'book/manifest.json';m=json.loads(p.read_text());source=w/'book/en/short_content.html';text=keyword_normalise(keyword_source_text(source))
terms='''world pattern|world instance|neural model|symbolic components|interpreters|formalization|SOP Lang|identifier|references|matching|shared variables|bindings|semantic graph|dependency graph|execution plan|computational cycle|composition|interfaces|compatible units|validation|syntax|types|applicability conditions|provenance|local updating|indexes|temporal evaluations|interpreter|deduction|constraints|planning|preconditions and effects|fixed point|finite domain|finite search|abduction|possible explanations|statistical association|prediction|intervention|probability distribution|source dependence|calibration|justifications|premises|reverse indexes|independent observations|symbolic execution|counterexample|abstract interpreters|compact intervals|dependent values|semantics|perceptions|memory candidates|digital twin|observation time|heating simulation|reconciliation|dependencies|data versions|delayed measurement|physical effect|operations agenda|pattern version|domain|reusable pattern|contrasting cases|evaluation|ambiguous identities|delayed results|recovery after interruptions|repair effort|documents|claims|versions and approvals|cost|risk|identity|conditions|operations|alternatives|history|interpretation of intention|uncertainty|scenario|explanation and revision|execution order|transmitted result|observation'''.split('|')
print('Terms:',len(terms))
missing=[t for t in terms if keyword_normalise(t) not in text];print('Missing',missing)
assert len(terms)==90 and len(set(terms))==90 and not missing
m['keywordReview']={'sourceHash':hashlib.sha256(source.read_bytes()).hexdigest(),'phrases':terms,'reviewedOn':'2026-11-11','method':'Active-LLM source-occurrence and reader discovery review; concrete technical concepts instead of extracted sentence fragments.'}
p.write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n')
