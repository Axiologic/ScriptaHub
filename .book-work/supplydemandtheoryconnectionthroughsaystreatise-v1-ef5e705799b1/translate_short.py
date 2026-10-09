import json
from pathlib import Path
p=Path(__file__).resolve().parent/'translations/ro/short/chunks/0001.json'
t={
 't000001':'Legătura dintre cerere și ofertă prin tratatul lui Say — Ediția de zece minute',
 't000002':'Legătura dintre cerere și ofertă prin tratatul lui Say',
 't000003':'AI Agent Zach Lawsone · 2024',
 't000004':'Cartea abordează cererea și oferta prin gândirea economică a lui Jean-Baptiste Say. Plasează explicația sa despre producție și consum în contextul istoric, apoi urmărește întreprinzătorul care leagă resursele de nevoile schimbătoare. Capitolele următoare analizează prețurile, ajustarea pieței, politicile publice și interdependența globală. Propoziția lui Say că oferta își creează propria cerere devine punctul de pornire pentru cercetarea legăturilor dintre activitatea productivă și puterea de cumpărare.',
 't000005':'Introducere — Producție și consum',
 't000006':'Oferta este ceea ce producătorii sunt dispuși și capabili să pună la dispoziție la prețuri diferite; cererea este ceea ce consumatorii vor să cumpere. Introducerea folosește aceste definiții pentru a prezenta relația descrisă de Say. Cartea susține că producția generează bunuri și venituri care fac posibile alte cumpărări. Totuși, preferințele cumpărătorilor, prețurile și deciziile antreprenoriale influențează la rândul lor ceea ce se produce. Textul introduce echilibrul pieței și întreabă ce poate spune astăzi o idee formulată la începutul secolului al XIX-lea.',
 't000007':'Citește introducerea în ediția integrală',
 't000008':'Fundamente — Say în economia clasică',
 't000009':'Primul capitol îl plasează pe Jean-Baptiste Say în schimbarea gândirii economice europene și în creșterea producției industriale. Plecând de la gânditori mai vechi, precum Adam Smith, dar dezvoltându-le ideile, Say a contestat explicațiile mercantiliste centrate pe excedentele comerciale și intervenția statului. Lucrarea sa',
 't000010':'Traité d’économie politique',
 't000011':'a pus accentul pe producție, schimb și capacitatea bunurilor utile de a genera valoare. Capitolul prezintă ideea că producerea bunurilor creează mijloacele de a cumpăra alte bunuri, recunoscând totodată că prețurile și preferințele consumatorilor ghidează ajustarea. Introduce și antreprenoriatul ca legătură între inițiativa individuală și schimbarea economică mai largă.',
 't000012':'Citește capitolul despre fundamente în ediția integrală',
 't000013':'Întreprinzătorii — Organizarea resurselor și asumarea riscului',
 't000014':'Pentru Say, întreprinzătorul face mai mult decât să dețină o afacere. El identifică ocazii, adună muncă, capital și materiale și le transformă în bunuri sau servicii care pot fi apreciate de cumpărători. Al doilea capitol descrie inovarea, asumarea riscului și adaptarea la schimbarea cererii. Analizează și rolul de coordonare al întreprinzătorului: recunoașterea nevoilor neacoperite, orientarea resurselor și reacția atunci când un produs nu atrage cumpărători. Cartea leagă aceste alegeri de ocuparea forței de muncă, de comunitățile locale și de schimbarea pieței, observând că recompensele sunt incerte, nu automate.',
 't000015':'Citește capitolul despre întreprinzători în ediția integrală',
 't000016':'Dinamica pieței — Prețuri și preferințe schimbătoare',
 't000017':'Al treilea capitol explică întâlnirea dintre cantitatea oferită și cea dorită de cumpărători la un preț al pieței. Un deficit poate ridica prețurile și atrage mai multă producție; oferta excesivă poate pune presiune în jos asupra prețurilor și îi poate face pe producători să se adapteze. Preferințele consumatorilor, tehnologia nouă și intervențiile publice pot modifica aceste relații. Exemplele despre alimente ecologice, energie și comerț global arată de ce nici oferta, nici cererea nu pot fi înțelese izolat. Capitolul leagă perspectiva lui Say, centrată pe producție, de procesul practic în care întreprinzătorii observă prețurile, ajustează producția și răspund schimbărilor.',
 't000018':'Citește capitolul despre dinamica pieței în ediția integrală',
 't000019':'Moștenire — Întrebări vechi pe piețe noi',
 't000020':'Al patrulea capitol urmărește influența lui Say asupra gândirii ulterioare despre producție, antreprenoriat și coordonarea pieței. Aplică discuția la comerțul electronic, pandemie, lanțuri globale de aprovizionare și schimbările tehnologice. O perturbare într-un loc poate afecta prețurile și disponibilitatea în altul; întreprinzătorii pot răspunde prin servicii noi sau moduri diferite de a ajunge la clienți. Capitolul întreabă și cum pot politicile să încurajeze inovarea, luând în seamă durabilitatea, incluziunea și bunăstarea comunităților. Ideile lui Say sunt prezentate ca instrumente de cercetare a problemelor actuale, fără a pretinde că piețele nu întâmpină niciodată obstacole.',
 't000021':'Citește capitolul despre moștenire în ediția integrală',
 't000022':'Concluzie — Un proces economic interconectat',
 't000023':'Concluzia aduce împreună producția, puterea de cumpărare, ajustarea prețurilor și inițiativa întreprinzătorilor. Cererea și oferta alcătuiesc o relație continuă, nu două forțe izolate. Întreprinzătorii pot crea valoare combinând resurse și anticipând nevoi, în timp ce reacțiile cumpărătorilor influențează producția viitoare. Cartea încheie prin raportarea acestor idei la alegerile de politică publică și la o economie global interconectată, unde adaptarea contează când preferințele, tehnologia sau condițiile externe se schimbă. Cititorii pot folosi argumentul istoric al lui Say pentru a examina atât posibilitățile, cât și limitele coordonării prin piață.',
 't000024':'Citește concluzia în ediția integrală',
}
d=json.loads(p.read_text())
for s in d['segments']:
 assert s['id'] in t
 assert not s['translation'] or s['translation']==t[s['id']]
 s['translation']=t[s['id']]
p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
