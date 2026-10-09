import json
from pathlib import Path

p=Path('tools/keyword-translations.generated.json')
d=json.loads(p.read_text())
t=d['translations']
overrides={
 'protective measures':{'pl':'działania ochronne'},
 'social welfare':{'ro':'bunăstare socială','fr':'bien-être social'},
 'freedom with responsibility':{'fr':'liberté et responsabilité'},
 'economic freedom':{'pl':'wolność gospodarcza'},
 'economic freedom with social responsibility':{'pl':'wolność gospodarcza i odpowiedzialność społeczna'},
 'freedom and protection':{'pl':'wolność i ochrona'},
 'protective responses':{'pl':'reakcje ochronne'},
 'great depression':{'ro':'Marea Criză Economică','pl':'Wielki Kryzys','fr':'Grande Dépression'},
 'depression and keynesian':{'ro':'Marea Criză și ideile keynesiene','fr':'dépression et idées keynésiennes','pl':'kryzys i idee keynesowskie'},
 'great depression and keynesian ideas':{'ro':'Marea Criză și gândirea keynesiană','pl':'Wielki Kryzys i idee keynesowskie'},
 'keynesian ideas':{'ro':'idei keynesiene','pl':'idee keynesowskie'},
 'pre-market communities':{'ro':'comunități anterioare economiei de piață','fr':'communautés avant l’économie de marché','pl':'społeczności przed gospodarką rynkową'},
 'self-regulating market':{'ro':'piață autoreglată','pl':'samoregulujący się rynek'},
 'bonds of reciprocity':{'ro':'legături de reciprocitate','pl':'więzi wzajemności'},
 'stakeholder capitalism':{'ro':'capitalismul părților interesate','fr':'capitalisme des parties prenantes','pl':'kapitalizm interesariuszy'},
 'labor and environmental standards':{'fr':'normes du travail et de l’environnement','pl':'standardy pracy i ochrony środowiska'},
 'trade and industrialization':{'pl':'handel i uprzemysłowienie'},
 'search for efficiency':{'pl':'poszukiwanie efektywności'},
 'vulnerability in economic crises':{'pl':'podatność na kryzysy gospodarcze'},
 'markets with social oversight':{'pl':'rynki pod nadzorem społecznym'},
 'revenue with social missions':{'pl':'przychody i misje społeczne'},
 'dignity and social welfare':{'fr':'dignité et bien-être social'},
 'ethical settings':{'pl':'konteksty etyczne'},
 'market advocates':{'ro':'susținători ai pieței'},
 'platform work':{'ro':'muncă pe platforme','pl':'praca platformowa'},
 'green investment and worker retraining':{'ro':'investiții verzi și recalificarea lucrătorilor','fr':'investissements verts et reconversion des travailleurs'},
 'worker retraining':{'fr':'reconversion des travailleurs'},
 'treating labor':{'pl':'traktowanie pracy jako towaru'},
 'fair labor':{'ro':'condiții de muncă echitabile','pl':'uczciwe warunki pracy'},
 'community ties':{'pl':'więzi wspólnotowe'},
 'collective bargaining':{'pl':'negocjacje zbiorowe'},
 'reasonable hours':{'pl':'rozsądne godziny pracy'},
 'embedded in cooperation':{'ro':'integrate în cooperare','pl':'zakorzenione we współpracy'},
 'social oversight':{'fr':'surveillance sociale'},
 'unemployment insurance':{'pl':'ubezpieczenie od bezrobocia'},
}
for phrase,labels in overrides.items():
    for lang,label in labels.items():
        assert phrase in t[lang]
        t[lang][phrase]=label
p.write_text(json.dumps(d,ensure_ascii=False,indent=2,sort_keys=True)+'\n')
