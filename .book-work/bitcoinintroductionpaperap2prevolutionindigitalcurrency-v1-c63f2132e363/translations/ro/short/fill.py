import json
from pathlib import Path
p=Path(__file__).parent/'chunks/0001.json';d=json.loads(p.read_text())
t=[
'Studiu introductiv despre Bitcoin: o revoluție P2P a monedei digitale — Lectură de zece minute',
'Studiu introductiv despre Bitcoin: o revoluție P2P a monedei digitale',
'Un parcurs de zece minute prin eseu',
'Introducere: bani fără un paznic central',
'Eseul prezintă Bitcoin drept răspunsul propus de Satoshi Nakamoto în 2008 la neîncrederea în băncile tradiționale după criza financiară globală. Propunerea descria un sistem de numerar electronic P2P: oamenii puteau transfera valoare direct, fără ca băncile sau procesatorii de plăți să decidă dacă transferul poate avea loc. Blockchainul public consemnează tranzacțiile, iar nodurile independente întrețin un registru comun. Promisiunea era autonomia financiară prin descentralizare, nu dependența de o autoritate centrală.',
'Eseul urmărește și o schimbare de accent. Bitcoin a fost propus ca numerar electronic pentru plăți peste granițe. Mai târziu, mulți l-au descris drept aur digital, o rezervă de valoare cu o ofertă fixă de 21 de milioane de monede. Dacă poate deveni și o monedă globală de uz zilnic rămâne o întrebare deschisă în text.',
'1. De ce conta descentralizarea',
'Criza financiară din 2008 a arătat slăbiciunile instituțiilor centralizate și a zdruncinat încrederea publicului. Lucrarea lui Nakamoto a propus un sistem în care participanții puteau face tranzacții fără a depinde de o singură bancă, un procesator sau un guvern. Blockchainul este un registru distribuit, păstrat de computere independente numite noduri. Minerii verifică grupuri de tranzacții și adaugă blocuri prin dovada muncii. Odată adăugate, înregistrările sunt concepute să reziste modificării.',
'Eliminarea intermediarului urmărea să reducă riscul adus de terți, comisioanele mari, procesarea lentă, cenzura și manipularea. Niciun participant nu ar controla singur rețeaua sau oferta monedei. Capitolul prezintă Bitcoin drept o alternativă fără granițe, rezistentă la cenzură, și o revendicare a unei suveranități financiare mai mari.',
'Citește capitolul integral despre descentralizare',
'2. Tranzacții, minerit și raritate',
'Un utilizator transmite o tranzacție rețelei. Minerii adună tranzacțiile într-un bloc și concurează pentru rezolvarea unui puzzle criptografic. Alte noduri verifică soluția propusă; un bloc valid intră în lanț și confirmă transferul. Bitcoin nou emis îl răsplătește pe miner. Procesul numit dovadă a muncii ajută la protejarea registrului, distribuind verificarea între mulți participanți în loc să o încredințeze unei singure instituții.',
'Eseul explică faptul că rescrierea unei tranzacții ar cere controlul a peste jumătate din puterea de minerit a rețelei. Deosebește și înregistrările publice de identitatea publică: adresele portofelelor sunt vizibile, dar proprietarii nu trebuie să-și dezvăluie numele. Bitcoin este așadar pseudonim, nu complet anonim. Un plafon de 21 de milioane de monede și înjumătățirea periodică încetinesc emisia nouă. Aceste trăsături susțin interpretarea ca „aur digital”, deși nu stabilesc singure cât de util este Bitcoin pentru plățile cotidiene.',
'Citește capitolul integral despre funcționarea Bitcoin',
'3. Rezervă de valoare sau monedă globală?',
'Eseul pune Bitcoin în contrast cu monedele fiduciare, a căror ofertă poate crește prin deciziile băncilor centrale. Raritatea lui atrage investitori care caută protecție împotriva inflației și instabilității economice. Totuși, volatilitatea prețului și comisioanele îngreunează ambiția inițială de a-l folosi ca mijloc zilnic de schimb. Lightning Network, construită ca nivel secund, încearcă să facă plățile mici, rapide și ieftine mai practice.',
'Dovada muncii consumă și multă energie, provocând o dezbatere despre mediu. Susținătorii invocă energia regenerabilă și valoarea atribuită rețelei, iar criticii îi pun la îndoială sustenabilitatea. Alte mecanisme de consens, precum dovada mizei, ar schimba construcția descrisă aici. Supravegherea reglementară, scalabilitatea și adoptarea instituțională modelează de asemenea viitorul Bitcoin. Capitolul lasă deschisă întrebarea centrală: aur digital, bani folosiți pe scară largă sau o combinație între cele două.',
'Citește capitolul integral despre viitorul Bitcoin',
'Concluzie',
'Propunerea distinctivă a Bitcoin îmbină transferul direct de valoare, registrul descentralizat, dovada muncii și o ofertă limitată de monede. Eseul vede în aceste trăsături o provocare la adresa presupunerilor despre cine controlează banii și în cine trebuie să avem încredere pentru a-i transfera. Viitorul practic depinde de limitele tehnice, costurile de mediu, reglementare și alegerile utilizatorilor și instituțiilor. Ediția integrală dezvoltă fiecare mecanism și dezbatere din textul sursă.',
'Citește eseul integral',
]
assert len(t)==len(d['segments']),(len(t),len(d['segments']))
for x,y in zip(d['segments'],t):x['translation']=y
p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
