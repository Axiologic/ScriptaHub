import json
from pathlib import Path
p=Path('tools/keyword-translations.generated.json');d=json.loads(p.read_text())
fix={
'ro':{
'commodity-backed money':'bani susținuți de mărfuri','currencies and cryptocurrencies':'monede și criptomonede','quantitative easing':'relaxare cantitativă','fractional-reserve banking':'sistem bancar cu rezerve fracționare','difficult timing problem':'problemă dificilă de sincronizare','budgets on necessities':'bugete pentru bunuri esențiale','currencies and prices':'monede și prețuri','free-banking proposal':'propunere privind băncile libere','savers and households':'persoane care economisesc și gospodării','central-bank tools':'instrumente ale băncilor centrale','money supply':'masa monetară','reserve requirements':'rezerve obligatorii','global spillovers':'efecte de propagare globale','history of exchange':'istoria schimburilor','structure of banks':'structura băncilor','spending power':'putere de cumpărare','bank lending':'creditare bancară','policy response':'răspuns de politică economică','crisis support':'sprijin în criză','monetary stability':'stabilitate monetară','free-banking proposal and commodity-backed money':'propunere de bănci libere și bani susținuți de mărfuri','uneven burden':'povară inegală','low-income households':'gospodării cu venituri mici','open-market operations':'operațiuni pe piața liberă','lasting monetary stability':'stabilitate monetară durabilă','digital currencies':'monede digitale'},
'pl':{
'commodity-backed money':'pieniądz oparty na surowcach','currencies and cryptocurrencies':'waluty i kryptowaluty','quantitative easing':'luzowanie ilościowe','fractional-reserve banking':'bankowość z rezerwą cząstkową','difficult timing problem':'trudność z doborem momentu','savers and households':'oszczędzający i gospodarstwa domowe','money supply':'podaż pieniądza','global spillovers':'globalne efekty uboczne','free-banking proposal':'propozycja wolnej bankowości','bank lending':'kredytowanie przez banki','depositors':'deponenci','unnecessary':'zbędny'},
'de':{
'commodity-backed money':'rohstoffgedecktes Geld','fractional-reserve banking':'Bankwesen mit Teilreserven','free-banking proposal':'Vorschlag für freies Bankwesen','global spillovers':'globale Übertragungseffekte','bank lending':'Kreditvergabe der Banken','spending power':'Kaufkraft','monetary policy':'Geldpolitik'},
'fr':{'commodity-backed money':'monnaie adossée aux matières premières','quantitative easing':'assouplissement quantitatif','fractional-reserve banking':'banque à réserves fractionnaires','free-banking proposal':'proposition de banque libre','savers and households':'épargnants et ménages'},
'es':{'quantitative easing':'expansión cuantitativa','fractional-reserve banking':'banca de reserva fraccionaria','free-banking proposal':'propuesta de banca libre','global spillovers':'efectos de propagación mundiales'},
'pt':{'commodity-backed money':'moeda apoiada em mercadorias','quantitative easing':'flexibilização quantitativa','fractional-reserve banking':'banca de reservas fracionárias','free-banking proposal':'proposta de banca livre','savers and households':'poupadores e famílias'},
'it':{'commodity-backed money':'moneta garantita da materie prime','quantitative easing':'allentamento quantitativo','fractional-reserve banking':'banca a riserva frazionaria','free-banking proposal':'proposta di banca libera','global spillovers':'effetti di propagazione globali'},
}
for lang,items in fix.items():
 for phrase,label in items.items():
  if phrase=='unnecessary':continue
  assert phrase in d['translations'][lang],(lang,phrase)
  d['translations'][lang][phrase]=label
p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
