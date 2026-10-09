import json
from pathlib import Path

path=Path('tools/keyword-translations.generated.json');cache=json.loads(path.read_text())
fix={
 'speculative retellings':{'fr':'réécritures spéculatives','de':'spekulative Neuerzählungen','es':'recreaciones especulativas','pt':'recontagens especulativas','it':'riscritture speculative','ro':'repovestiri speculative','pl':'spekulatywne opowieści na nowo'},
 'different futures':{'fr':'différents futurs','de':'verschiedene Zukünfte'},
 'wasteland':{'fr':'terre désolée','es':'páramo','pt':'terra desolada','it':'terra desolata','ro':'pustiu'},
 'armor from scrap':{'de':'Rüstung aus Schrott'},
 'battered bicycle':{'fr':'vieux vélo abîmé','de':'ramponiertes Fahrrad','es':'bicicleta maltrecha','pt':'bicicleta maltratada','it':'bicicletta malridotta','ro':'bicicletă uzată','pl':'zniszczony rower'},
 'repair tires':{'fr':'réparer les pneus','de':'Reifen reparieren','es':'reparar neumáticos','pt':'reparar pneus','it':'riparare gli pneumatici','ro':'repararea anvelopelor','pl':'naprawa opon'},
 'abandoned wind turbine':{'ro':'turbină eoliană abandonată'},
 'dragon':{'pl':'smok'},
 'crowded city':{'ro':'oraș aglomerat','de':'überfüllte Stadt'},
 'comic books':{'ro':'benzi desenate'},
 'improvised mask':{'ro':'mască improvizată'},
 'cape':{'it':'mantello','ro':'pelerină'},
 'urban vigilante':{'fr':'justicier urbain','de':'städtischer Selbstjustizler','ro':'justițiar urban','pl':'miejski samozwańczy obrońca'},
 'heroic frame':{'it':'prospettiva eroica','ro':'perspectivă eroică','pl':'bohaterska perspektywa'},
 'wish for justice':{'ro':'dorință de dreptate','pl':'pragnienie sprawiedliwości'},
 'imagined monsters':{'pl':'wyimaginowane potwory'},
 'squire':{'de':'Knappe','pl':'giermek'},
 'finds supplies':{'pl':'zdobywa zapasy'},
 'negotiates with strangers':{'ro':'negociază cu străinii','pl':'negocjuje z nieznajomymi'},
 'immersive game':{'ro':'joc imersiv','pl':'gra immersyjna'},
 'headset':{'fr':'casque de réalité virtuelle','es':'visor de realidad virtual','pt':'auscultadores de realidade virtual','it':'visore di realtà virtuale','ro':'cască de realitate virtuală','pl':'gogle VR'},
 'controllers':{'ro':'controlere','pl':'kontrolery'},
 'haptic suit':{'es':'traje háptico','pt':'fato háptico','it':'tuta aptica','pl':'kombinezon haptyczny'},
 'security guard':{'ro':'agent de pază'},
 'chivalric books':{'fr':'livres de chevalerie','es':'libros de caballerías','pt':'livros de cavalaria','it':'libri di cavalleria','ro':'cărți cavalerești','pl':'księgi rycerskie'},
 'worn starship':{'de':'abgenutztes Raumschiff','it':'astronave logora','ro':'navă spațială uzată','pl':'zużyty statek kosmiczny'},
 'practical judgment':{'es':'juicio práctico','pt':'bom senso prático','ro':'judecată practică','pl':'praktyczny osąd'},
 'dangerous':{'ro':'periculos'},
 'material demands':{'de':'materielle Bedürfnisse','pl':'potrzeby materialne'},
 'human need to hope':{'pl':'ludzka potrzeba nadziei'},
}
for phrase,labels in fix.items():
 for lang,label in labels.items():
  assert phrase in cache['translations'][lang],(phrase,lang)
  cache['translations'][lang][phrase]=label
path.write_text(json.dumps(cache,ensure_ascii=False,indent=2)+'\n')
print('Curated',sum(map(len,fix.values())),'labels')
