import json
from pathlib import Path
p=Path('tools/keyword-translations.generated.json');d=json.loads(p.read_text());t=d['translations']
fix={
'store of value':{'ro':'rezervă de valoare','fr':'réserve de valeur','de':'Wertspeicher','es':'reserva de valor','pt':'reserva de valor','it':'riserva di valore','pl':'środek przechowywania wartości'},
'central gatekeeper':{'ro':'controlor central','fr':'contrôleur central','de':'zentrale Kontrollinstanz','es':'controlador central','pt':'controlador central','it':'controllore centrale','pl':'centralny strażnik dostępu'},
'lightning network':{'ro':'Lightning Network','fr':'Lightning Network','de':'Lightning Network','es':'Lightning Network','pt':'Lightning Network','it':'Lightning Network','pl':'Lightning Network'},
'fixed supply':{'ro':'ofertă fixă','fr':'offre fixe','de':'festes Angebot','es':'oferta fija','pt':'oferta fixa','it':'offerta fissa','pl':'stała podaż'},
'public blockchain':{'ro':'blockchain public','fr':'blockchain public','de':'öffentliche Blockchain','es':'cadena de bloques pública','pt':'blockchain pública','it':'blockchain pubblica','pl':'publiczny łańcuch bloków'},
'everyday global currency':{'de':'globale Alltagswährung'},
'electronic cash system':{'ro':'sistem de numerar electronic','fr':'système de monnaie électronique','de':'elektronisches Bargeldsystem','es':'sistema de efectivo electrónico','pt':'sistema de dinheiro eletrónico','it':'sistema di contante elettronico','pl':'system elektronicznej gotówki'},
'groups of transactions':{'fr':'groupes de transactions','it':'gruppi di transazioni'},
'electronic cash':{'fr':'monnaie électronique','pt':'dinheiro eletrónico','it':'contante elettronico'},
'limited coin supply':{'ro':'ofertă limitată de monede','fr':'offre limitée de pièces','de':'begrenztes Münzangebot','es':'oferta limitada de monedas','pt':'oferta limitada de moedas','it':'offerta limitata di monete','pl':'ograniczona podaż monet'},
'low-cost payments':{'pl':'płatności o niskim koszcie'},
'new issuance':{'fr':'nouvelle émission monétaire','de':'Neuemission','es':'nueva emisión','pt':'nova emissão','it':'nuova emissione','ro':'emisiune nouă','pl':'nowa emisja'},
'proof of stake':{'ro':'dovada mizei','fr':'preuve d’enjeu','de':'Proof of Stake','es':'prueba de participación','pt':'prova de participação','it':'prova di partecipazione','pl':'dowód stawki'},
'decentralized ledger':{'de':'dezentrales Register','es':'registro descentralizado','pt':'registo descentralizado','it':'registro decentralizzato'},
'distributed ledger':{'ro':'registru distribuit','fr':'registre distribué','de':'verteiltes Register','es':'registro distribuido','pt':'registo distribuído','it':'registro distribuito','pl':'rejestr rozproszony'},
'payment processors':{'fr':'prestataires de traitement des paiements','it':'operatori di pagamento','pl':'operatorzy płatności'},
'central authority':{'pl':'władza centralna'},
'wallet addresses':{'ro':'adrese de portofel','fr':'adresses de portefeuille','de':'Wallet-Adressen','es':'direcciones de monedero','pt':'endereços de carteira','it':'indirizzi dei portafogli','pl':'adresy portfeli'},
'currency supply':{'ro':'oferta monetară','fr':'offre monétaire','de':'Geldmenge','es':'oferta monetaria','pt':'oferta monetária','it':'offerta monetaria','pl':'podaż pieniądza'},
'fiat currencies':{'ro':'monede fiduciare','fr':'monnaies fiduciaires','de':'Fiatwährungen','es':'monedas fiduciarias','pt':'moedas fiduciárias','it':'valute fiat','pl':'waluty fiducjarne'},
'public records':{'ro':'înregistrări publice','fr':'registres publics','de':'öffentliche Aufzeichnungen','es':'registros públicos','pt':'registos públicos','it':'registri pubblici','pl':'publiczne rejestry'},
'shared ledger':{'ro':'registru comun','fr':'registre partagé','de':'gemeinsames Register','es':'registro compartido','pt':'registo partilhado','it':'registro condiviso','pl':'wspólny rejestr'},
'mining power':{'ro':'putere de minerit','fr':'puissance de minage','de':'Mining-Leistung','es':'potencia de minería','pt':'poder de mineração','it':'potenza di mining','pl':'moc obliczeniowa kopania'},
'periodic halving':{'ro':'înjumătățire periodică','fr':'réduction périodique de moitié','de':'periodische Halbierung','es':'reducción periódica a la mitad','pt':'redução periódica para metade','it':'dimezzamento periodico','pl':'okresowe zmniejszanie o połowę'},
'supply cap':{'ro':'plafon al ofertei','fr':'plafond de l’offre','de':'Angebotsobergrenze','es':'límite de la oferta','pt':'limite da oferta','it':'limite dell’offerta','pl':'limit podaży'},
'peer-to-peer electronic cash system':{'fr':'système de monnaie électronique pair à pair','de':'elektronisches Peer-to-Peer-Bargeldsystem','es':'sistema de efectivo electrónico entre pares','pt':'sistema de dinheiro eletrónico ponto a ponto','it':'sistema di contante elettronico peer-to-peer','ro':'sistem P2P de numerar electronic','pl':'system elektronicznej gotówki P2P'},
'block':{'de':'Block'},
'pseudonymous':{'es':'seudónimo'},
'regulation':{'fr':'réglementation','de':'Regulierung','es':'regulación','pt':'regulação','it':'regolamentazione'},
'transaction':{'es':'transacción','it':'transazione'},
'daily medium of exchange':{'ro':'mijloc de schimb cotidian','de':'alltägliches Tauschmittel','es':'medio de intercambio cotidiano','pt':'meio de troca quotidiano','it':'mezzo di scambio quotidiano','pl':'codzienny środek wymiany'},
'blockchain records transactions':{'ro':'blockchainul înregistrează tranzacții','fr':'la blockchain enregistre les transactions','de':'Blockchain zeichnet Transaktionen auf','es':'la cadena de bloques registra transacciones','pt':'a blockchain regista transações','it':'la blockchain registra transazioni','pl':'łańcuch bloków zapisuje transakcje'},
'newly issued bitcoins':{'ro':'bitcoini nou emiși','pl':'nowo wyemitowane bitcoiny'},
'fully anonymous':{'es':'totalmente anónimo','pt':'totalmente anónimo','it':'completamente anonimo','ro':'complet anonim'},
'quick':{'ro':'rapid','es':'rápido','pt':'rápido','it':'rapido'},
'blockchain records':{'ro':'înregistrări blockchain','fr':'enregistrements de la blockchain','de':'Blockchain-Aufzeichnungen','es':'registros de la cadena de bloques','pt':'registos da blockchain','it':'registrazioni blockchain','pl':'zapisy w łańcuchu bloków'},
}
for phrase,localized in fix.items():
 for lang,label in localized.items():
  assert phrase in t[lang],(lang,phrase)
  t[lang][phrase]=label
p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
