import json
from pathlib import Path
p=Path('tools/keyword-translations.generated.json');d=json.loads(p.read_text());t=d['translations']
names={'Federation':{'fr':'Fédération','de':'Föderation','es':'Federación','pt':'Federação','it':'Federazione','ro':'Federație','pl':'Federacja'},'Prime Directive':{'fr':'Directive Première','de':'Oberste Direktive','es':'Primera Directiva','pt':'Primeira Diretiva','it':'Prima Direttiva','ro':'Directiva Primară','pl':'Pierwsza Dyrektywa'},'Dominion War':{'fr':'guerre du Dominion','de':'Dominion-Krieg','es':'Guerra del Dominio','pt':'Guerra do Dominion','it':'guerra del Dominio','ro':'Războiul Dominion','pl':'wojna z Dominium'},'Borg':{l:'Borg' for l in ('fr','de','es','pt','it','ro','pl')}}
for en,vals in names.items():
 for l,v in vals.items():t[l][en]=v
fix={
'ro':{'starships':'nave stelare','alien encounters':'întâlniri cu extratereștri','future societies':'societăți viitoare','Federation':'Federație','cooperation across differences':'cooperare dincolo de diferențe','Klingons':'klingonieni','Romulans':'romulani','pivotal stories':'povești esențiale','hopeful vision':'viziune plină de speranță','scarcity':'lipsuri','Prime Directive':'Directiva Primară','ethical choices':'alegeri etice','frontier':'frontieră','conflict':'conflict','Klingon heritage':'moștenire klingoniană','Federation upbringing':'educație în Federație','imagined technologies':'tehnologii imaginate'},
'fr':{'starships':'vaisseaux spatiaux','alien encounters':'rencontres extraterrestres','cooperation across differences':'coopération au-delà des différences','pivotal stories':'récits majeurs','Prime Directive':'Directive Première','frontier':'frontière'},
'de':{'starships':'Raumschiffe','Federation':'Föderation','cooperation across differences':'Zusammenarbeit über Unterschiede hinweg','Prime Directive':'Oberste Direktive','frontier':'Grenzgebiet','pivotal stories':'entscheidende Geschichten','Dominion War':'Dominion-Krieg'},
'es':{'alien encounters':'encuentros extraterrestres','cooperation across differences':'cooperación entre diferencias','Klingons':'klingon','Prime Directive':'Primera Directiva'},
'pt':{'starships':'naves estelares','alien encounters':'encontros extraterrestres','cooperation across differences':'cooperação entre diferenças','Prime Directive':'Primeira Diretiva','Dominion War':'Guerra do Dominion'},
'it':{'cooperation across differences':'cooperazione oltre le differenze','Klingons':'Klingon','Prime Directive':'Prima Direttiva','frontier':'frontiera'},
'pl':{'alien encounters':'spotkania z obcymi','cooperation across differences':'współpraca mimo różnic','Romulans':'Romulanie','hopeful vision':'pełna nadziei wizja','Prime Directive':'Pierwsza Dyrektywa','Dominion War':'wojna z Dominium'},
}
for l,vals in fix.items():
 for en,v in vals.items():
  assert en in t[l],(l,en)
  t[l][en]=v
p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
