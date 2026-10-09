import json
from pathlib import Path
p=Path('tools/keyword-translations.generated.json');d=json.loads(p.read_text());t=d['translations']
for l in ('fr','de','es','pt','it','ro','pl'):
 for x in ('Maycomb','Atticus Finch','Scout','Jem','Tom Robinson'):t[l][x]=x
 t[l]['Boo Radley’s life']={'fr':'la vie de Boo Radley','de':'Boo Radleys Leben','es':'la vida de Boo Radley','pt':'a vida de Boo Radley','it':'la vita di Boo Radley','ro':'viața lui Boo Radley','pl':'życie Boo Radleya'}[l]
fix={
'ro':{'fictional town':'oraș fictiv','ordinary relationships':'relații obișnuite','justice demands':'cerințele dreptății','children learn social rules':'copiii învață reguli sociale','listening across differences':'ascultare dincolo de diferențe','noticing bias':'observarea părtinirii','stories':'povești','classroom':'sală de clasă','students':'elevi','teachers':'profesori','racial hierarchy':'ierarhie rasială','social cost':'preț social','legal ideals':'idealuri juridice','present-day evidence':'dovezi actuale','novel’s afterlife':'viața ulterioară a romanului'},
'fr':{'Maycomb':'Maycomb','justice demands':'exigences de la justice','listening across differences':'écouter au-delà des différences','noticing bias':'repérer les préjugés','classroom':'salle de classe','students':'élèves','Boo Radley’s life':'la vie de Boo Radley'},
'de':{'ordinary relationships':'alltägliche Beziehungen','justice demands':'Forderungen der Gerechtigkeit','listening across differences':'über Unterschiede hinweg zuhören','students':'Schüler','Boo Radley’s life':'Boo Radleys Leben'},
'es':{'listening across differences':'escuchar más allá de las diferencias','noticing bias':'detectar sesgos','Boo Radley’s life':'la vida de Boo Radley','stories':'historias'},
'pt':{'listening across differences':'ouvir para além das diferenças','noticing bias':'perceber preconceitos','Boo Radley’s life':'a vida de Boo Radley'},
'it':{'noticing bias':'riconoscere i pregiudizi','listening across differences':'ascoltare oltre le differenze','Boo Radley’s life':'la vita di Boo Radley'},
'pl':{'defense of Tom Robinson':'obrona Toma Robinsona','justice demands':'wymogi sprawiedliwości','listening across differences':'słuchanie ponad podziałami','students':'uczniowie','Boo Radley’s life':'życie Boo Radleya'},
}
for l,vals in fix.items():
 for en,loc in vals.items():
  assert en in t[l],(l,en)
  t[l][en]=loc
p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
