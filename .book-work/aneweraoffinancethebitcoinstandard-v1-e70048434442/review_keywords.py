import json
from pathlib import Path

work=Path(__file__).resolve().parent
p=work/'book/manifest.json';m=json.loads(p.read_text())
swap={'familiar way':'cowry shells','money remain':'limits trade','agent adria':'early money','older forms':'blocks exchanges and limits trade','shared recognition and trust help':'social trust','past money':'acceptance and confidence'}
m['keywordReview']['phrases']=[swap.get(x,x) for x in m['keywordReview']['phrases']]
assert len(set(m['keywordReview']['phrases']))==90
p.write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n')
p=Path('tools/keyword-translations.generated.json');c=json.loads(p.read_text());t=c['translations']
manual={
 'cowry shells':['coquillages cauris','Kaurimuscheln','conchas cauri','conchas cauri','conchiglie cauri','scoici cauri','muszle kauri'],
 'limits trade':['limite le commerce','begrenzt den Handel','limita el comercio','limita o comércio','limita gli scambi','limitează comerțul','ogranicza handel'],
 'early money':['premières formes de monnaie','frühe Geldformen','primeras formas de dinero','primeiras formas de dinheiro','prime forme di denaro','forme timpurii de bani','wczesne formy pieniądza'],
 'blocks exchanges and limits trade':['bloque les échanges et limite le commerce','blockiert Tausch und Handel','bloquea los intercambios y limita el comercio','bloqueia as trocas e limita o comércio','blocca gli scambi e limita il commercio','blochează schimburile și limitează comerțul','blokuje wymianę i ogranicza handel'],
 'social trust':['confiance sociale','gesellschaftliches Vertrauen','confianza social','confiança social','fiducia sociale','încredere socială','zaufanie we wspólnocie'],
 'acceptance and confidence':['acceptation et confiance','Akzeptanz und Vertrauen','aceptación y confianza','aceitação e confiança','accettazione e fiducia','acceptare și încredere','akceptacja i zaufanie'],
 'fiat currency':['monnaie fiduciaire','Fiatwährung','moneda fiduciaria','moeda fiduciária','moneta fiduciaria','monedă fiduciară','waluta fiducjarna'],
 'tangible value':['valeur tangible','greifbarer Wert','valor tangible','valor tangível','valore tangibile','valoare tangibilă','wartość materialna'],
 'beads and livestock':['perles et bétail','Perlen und Vieh','cuentas y ganado','contas e gado','perline e bestiame','mărgele și animale domestice','paciorki i bydło'],
 'scarcity and independence':['rareté et indépendance','Knappheit und Unabhängigkeit','escasez e independencia','escassez e independência','scarsità e indipendenza','raritate și independență','rzadkość i niezależność'],
 'scarcity and trust':['rareté et confiance','Knappheit und Vertrauen','escasez y confianza','escassez e confiança','scarsità e fiducia','raritate și încredere','rzadkość i zaufanie'],
 'government-issued fiat':['monnaie fiduciaire émise par l’État','staatlich ausgegebenes Fiatgeld','dinero fiduciario emitido por el Estado','moeda fiduciária emitida pelo Estado','moneta fiduciaria emessa dallo Stato','monedă fiduciară emisă de stat','pieniądz fiducjarny emitowany przez państwo'],
 'metal-backed currency':['monnaie adossée aux métaux','metallgedeckte Währung','moneda respaldada por metales','moeda lastreada em metais','valuta garantita da metalli','monedă garantată prin metale','waluta oparta na metalach'],
 'early exchange goods':['premiers biens d’échange','frühe Tauschgüter','primeros bienes de intercambio','primeiros bens de troca','primi beni di scambio','primele bunuri de schimb','wczesne dobra wymiany'],
 'history of barter':['histoire du troc','Geschichte des Tauschhandels','historia del trueque','história da troca direta','storia del baratto','istoria trocului','historia barteru'],
 'media of exchange':['moyens d’échange','Tauschmittel','medios de intercambio','meios de troca','mezzi di scambio','mijloace de schimb','środki wymiany'],
 'limits on supply':['limites de l’offre monétaire','Grenzen des Geldangebots','límites de la oferta monetaria','limites da oferta monetária','limiti dell’offerta monetaria','limitele ofertei monetare','limity podaży pieniądza'],
 'predetermined supply':['offre prédéterminée','vorab festgelegtes Angebot','oferta predeterminada','oferta predeterminada','offerta prestabilita','ofertă prestabilită','z góry określona podaż'],
 'maximum supply':['offre maximale','maximales Angebot','oferta máxima','oferta máxima','offerta massima','ofertă maximă','maksymalna podaż'],
 'properties of past money':['propriétés des monnaies anciennes','Eigenschaften früherer Geldformen','propiedades del dinero antiguo','propriedades do dinheiro antigo','proprietà delle monete antiche','proprietățile banilor din trecut','właściwości dawnych pieniędzy'],
 'double coincidence':['double coïncidence des besoins','doppelte Übereinstimmung der Bedürfnisse','doble coincidencia de necesidades','dupla coincidência de necessidades','doppia coincidenza dei bisogni','dubla coincidență a nevoilor','podwójna zbieżność potrzeb'],
 'gold standard':['étalon-or','Goldstandard','patrón oro','padrão-ouro','sistema aureo','etalonul-aur','standard złota'],
 'fiat money':['monnaie fiduciaire','Fiatgeld','dinero fiduciario','dinheiro fiduciário','denaro fiduciario','bani fiduciari','pieniądz fiducjarny'],
 'appeal of tangible value':['attrait de la valeur tangible','Reiz greifbaren Werts','atractivo del valor tangible','atrativo do valor tangível','richiamo del valore tangibile','atracția valorii tangibile','atrakcyjność namacalnej wartości'],
}
for phrase, values in manual.items():
 for lang,value in zip(('fr','de','es','pt','it','ro','pl'),values):t[lang][phrase]=value
p.write_text(json.dumps(c,ensure_ascii=False,indent=2)+'\n')
