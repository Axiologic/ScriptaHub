import json
from pathlib import Path

p=Path('tools/keyword-translations.generated.json')
d=json.loads(p.read_text())
t=d['translations']
fix={
 'ro':{
  'escape from poverty':'ieșirea din sărăcie','private choices':'alegeri personale','removal of restraints':'înlăturarea constrângerilor','changed identity':'identitate schimbată','social stigma':'stigmat social','mercy and sacrifice':'milă și sacrificiu','chains to redemption':'de la lanțuri la izbăvire','stealing bread':'furtul unei pâini','hungry family':'familie înfometată','ex-convict':'fost deținut','work and shelter':'muncă și adăpost','food and lodging':'hrană și găzduire','candlesticks':'sfeșnice','unexpected forgiveness':'iertare neașteptată','new name':'nume nou','respected life':'viață respectată','shadow of judgment':'umbra judecății','movement toward redemption':'drumul spre izbăvire','daughter Cosette':'fiica Cosette','factory job':'slujbă la fabrică','double standard':'dublă măsură','vulnerable woman':'femeie vulnerabilă','system of injustice':'sistem de nedreptate','Paris barricades':'baricadele Parisului','equality':'egalitate','democratic future':'viitor democratic','youthful idealism':'idealismul tinereții','moral choice':'alegere morală','rebellion':'revoltă','sewers of Paris':'canalele Parisului','price of revolt':'prețul revoltei','strict belief':'convingere rigidă','absolute view of law':'viziune absolută despre lege','inflexible mind':'minte inflexibilă','quieter sacrifice':'sacrificiu mai tăcut','convict past':'trecut de condamnat','withdraws from Cosette':'se retrage din viața lui Cosette','peaceful end':'sfârșit pașnic','cycles of punishment':'cicluri ale pedepsei','failed rebellion':'revoltă eșuată','compassion matters':'compasiunea contează','humanity beyond labels':'omul dincolo de etichete','society':'societate','law':'lege','redemption':'izbăvire',
 },
 'fr':{'removal of restraints':'levée des contraintes','chains to redemption':'des chaînes à la rédemption','Bishop Myriel':'évêque Myriel','candlesticks':'chandeliers d’argent','convict past':'passé de bagnard','strict belief':'conviction rigide','absolute view of law':'vision absolue de la loi','compassion matters':'la compassion compte','law':'loi','vulnerable woman':'femme vulnérable'},
 'de':{'chains to redemption':'von Ketten zur Erlösung','candlesticks':'Kerzenleuchter','convict past':'Vergangenheit als Sträfling','private choices':'persönliche Entscheidungen','strict belief':'starre Überzeugung','absolute view of law':'absolutes Rechtsverständnis','law':'Gesetz','removal of restraints':'Befreiung von Zwängen'},
 'es':{'removal of restraints':'eliminación de las restricciones','chains to redemption':'de las cadenas a la redención','candlesticks':'candelabros','convict past':'pasado de presidiario','strict belief':'convicción rígida','absolute view of law':'visión absoluta de la ley','law':'ley','private choices':'decisiones personales'},
 'pt':{'removal of restraints':'remoção das restrições','chains to redemption':'das correntes à redenção','candlesticks':'castiçais','convict past':'passado de condenado','strict belief':'convicção rígida','absolute view of law':'visão absoluta da lei','law':'lei','private choices':'escolhas pessoais'},
 'it':{'removal of restraints':'rimozione dei vincoli','chains to redemption':'dalle catene alla redenzione','candlesticks':'candelabri','convict past':'passato da detenuto','strict belief':'convinzione rigida','absolute view of law':'visione assoluta della legge','law':'legge','private choices':'scelte personali'},
 'pl':{'chains to redemption':'od kajdan do odkupienia','candlesticks':'świeczniki','convict past':'przeszłość skazańca','strict belief':'sztywne przekonanie','absolute view of law':'bezwzględna wizja prawa','law':'prawo','private choices':'osobiste wybory','removal of restraints':'usunięcie ograniczeń','escape from poverty':'wyjście z ubóstwa'},
}
for lang,m in fix.items():
 for en,localized in m.items():
  assert en in t[lang],(lang,en)
  t[lang][en]=localized
p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
