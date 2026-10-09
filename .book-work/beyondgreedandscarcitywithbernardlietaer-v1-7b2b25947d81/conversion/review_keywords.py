import json
from pathlib import Path
p=Path('tools/keyword-translations.generated.json');c=json.loads(p.read_text())
langs=('fr','de','es','pt','it','ro','pl')
fix={
'historical and local currencies':('monnaies historiques et locales','historische und lokale Währungen','monedas históricas y locales','moedas históricas e locais','valute storiche e locali','monede istorice și locale','waluty historyczne i lokalne'),
'multiple currencies':('plusieurs monnaies','mehrere Währungen','varias monedas','várias moedas','più valute','mai multe monede','wiele walut'),
'state power':('pouvoir de l’État','Staatsmacht','poder del Estado','poder do Estado','potere dello Stato','puterea statului','władza państwa'),
'terra trc':('Terra TRC',)*7,
'medieval european bracteates':('bractéates européennes médiévales','mittelalterliche europäische Brakteaten','bracteatos europeos medievales','bracteatos europeus medievais','bratteati europei medievali','bracteate europene medievale','średniowieczne brakteaty europejskie'),
'exchange trading systems':('systèmes d’échange commercial','kommerzielle Tauschsysteme','sistemas de intercambio comercial','sistemas de troca comercial','sistemi di scambio commerciale','sisteme de schimb comercial','systemy wymiany handlowej'),
'ledgers and blockchain':('registres numériques et blockchain','digitale Register und Blockchain','registros digitales y blockchain','registos digitais e blockchain','registri digitali e blockchain','registre digitale și blockchain','rejestry cyfrowe i blockchain'),
'local exchange trading':('commerce d’échange local','lokaler Tauschhandel','comercio de intercambio local','comércio de troca local','commercio di scambio locale','comerț prin schimb local','lokalny handel wymienny'),
'modern digital ledgers':('registres numériques modernes','moderne digitale Register','registros digitales modernos','registos digitais modernos','registri digitali moderni','registre digitale moderne','nowoczesne rejestry cyfrowe'),
'universal basic income':('revenu de base universel','bedingungsloses Grundeinkommen','renta básica universal','rendimento básico universal','reddito di base universale','venit de bază universal','powszechny dochód podstawowy'),
'inequality and environmental strain':('inégalités et pression environnementale','Ungleichheit und Umweltbelastung','desigualdad y presión ambiental','desigualdade e pressão ambiental','disuguaglianza e pressione ambientale','inegalitate și presiune asupra mediului','nierówności i presja środowiskowa'),
'Yang qualities':('qualités Yang','Yang-Eigenschaften','cualidades Yang','qualidades Yang','qualità Yang','trăsături Yang','cechy Yang'),
'Yin qualities':('qualités Yin','Yin-Eigenschaften','cualidades Yin','qualidades Yin','qualità Yin','trăsături Yin','cechy Yin'),
'community currencies':('monnaies communautaires','Gemeinschaftswährungen','monedas comunitarias','moedas comunitárias','valute comunitarie','monede comunitare','waluty wspólnotowe'),
'environmental strain':('pression environnementale','Umweltbelastung','presión ambiental','pressão ambiental','pressione ambientale','presiune asupra mediului','presja środowiskowa'),
'demurrage':('fonte monétaire','Umlaufgebühr','oxidación monetaria','taxa de circulação','demurrage monetario','taxă de păstrare a banilor','opłata za przetrzymywanie pieniądza'),
'exchange trading':('échange commercial','Tauschhandel','intercambio comercial','troca comercial','scambio commerciale','schimb comercial','wymiana handlowa'),
'local exchange':('échange local','lokaler Austausch','intercambio local','troca local','scambio locale','schimb local','wymiana lokalna'),
'measurable law':('loi mesurable','messbares Gesetz','ley medible','lei mensurável','legge misurabile','lege măsurabilă','mierzalne prawo'),
'digital ledgers':('registres numériques','digitale Register','registros digitales','registos digitais','registri digitali','registre digitale','rejestry cyfrowe'),
'interoperable':('interopérable','interoperabel','interoperable','interoperável','interoperabile','interoperabil','interoperacyjny'),
'great mother archetype':('archétype de la Grande Mère','Archetyp der Großen Mutter','arquetipo de la Gran Madre','arquétipo da Grande Mãe','archetipo della Grande Madre','arhetipul Marii Mame','archetyp Wielkiej Matki'),
}
for phrase,labels in fix.items():
 for lang,label in zip(langs,labels):
  assert phrase in c['translations'][lang],(phrase,lang)
  c['translations'][lang][phrase]=label
p.write_text(json.dumps(c,ensure_ascii=False,indent=2)+'\n')
print('corrected',len(fix),'phrases')
