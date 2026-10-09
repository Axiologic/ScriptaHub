import hashlib,json,sys
from pathlib import Path
sys.path.insert(0,'tools')
from build_books import keyword_normalise, keyword_source_text, SHELF_CATEGORIES

root=Path(__file__).parent
p=root/'book/manifest.json'
d=json.loads(p.read_text())
source=root/'book/en/short_content.html'
text=keyword_normalise(keyword_source_text(source))
broad={keyword_normalise(x).strip() for v in SHELF_CATEGORIES.values() for x in v['en'].split('|')}
phrases=[
 'Rodion Raskolnikov','Alyona Ivanovna','Lizaveta','Sonia Semyonovna Marmeladov','Razumikhin','Porfiry Petrovich',
 'St. Petersburg','pawnbroker','former student','severe poverty','desperate customers','wealth',
 'theory of exceptional people','extraordinary individuals','extraordinary men','moral boundaries','moral law','greater good',
 'intellectual argument','murder','guilt','confession','moral rebirth','central question',
 'changing condition of Raskolnikov’s mind','burden of conscience','rationalizations','higher purpose','proposed murder','dread',
 'axe','careful plan','nearby tenants','Alyona’s building','innocent sister','second murder',
 'precise act','coins and trinkets','stolen items','moral descent','liberation from poverty','fear, confusion',
 'crime','nightmare','blood','moral line','theory about extraordinary men','fears discovery',
 'witnesses','ordinary streets','fever','paranoia','isolation','reality and imagination',
 'oppressive summer heat','philosophical certainty','consequences of his actions','suffocation','psychological story','consciousness',
 'suffering','compassion','faith','prostitution','Raskolnikov’s family','vulnerability',
 'public confession','forgiveness','accept punishment','reconciliation','victims','police station',
 'investigator','atonement','tragedy and hope','moral relativism','redemption','responsibility',
 'detached reasoning','used to justify murder','theory promised freedom','bound him to guilt','Sonia’s compassion','uncertain journey',
 'choice','outward events','murder, guilt','poverty and oppressive heat','low offer','Sonia’s room',
]
assert len(phrases)==90,len(phrases)
assert len({keyword_normalise(x) for x in phrases})==90
bad=[x for x in phrases if keyword_normalise(x) not in text or keyword_normalise(x).strip() in broad or keyword_normalise(x)==keyword_normalise(d['title']['en'])]
assert not bad,bad
d['keywordReview']={'sourceHash':hashlib.sha256(source.read_bytes()).hexdigest(),'phrases':phrases}
p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
print('Reviewed',len(phrases),'phrases')
