import json
from pathlib import Path

root = Path(__file__).parent / 'translations/ro/short/chunks'
translations = {
    't000001': 'O explorare a universului Warhammer 40.000 — Ediția de zece minute',
    't000002': 'O explorare a universului Warhammer 40.000',
    't000003': 'Această carte prezintă Warhammer 40.000 ca pe o galaxie fictivă în care războiul modelează aproape fiecare instituție. Ea trece de la sistemul de credințe al Imperiului și facțiunile cu care luptă la tehnologie, viața obișnuită și Erezia lui Horus. Dincolo de catalogul de armate și mașini revine mereu o întrebare: ce rămâne din judecata, compasiunea și memoria omenească atunci când supraviețuirea devine scopul mai presus de toate? Ghidul explică termenii importanți ai acestui univers și îi invită pe cititori să-i examineze alegerile morale întunecate.',
    't000004': 'Un univers organizat pentru război',
    't000005': 'Introducerea așază Imperiul Omenirii într-o galaxie ostilă. Împăratul stă nemișcat pe Tronul de Aur, iar Imperiul se întinde peste lumi pe care cu greu le poate guverna. Călătoriile și comunicarea depind de forțe psihice periculoase și de tehnologii pe care mulți le folosesc fără să le înțeleagă pe deplin. Această scară uriașă este o parte din atracția universului, dar explică și de ce frica, ritualul și birocrația modelează hotărârile de fiecare zi. Războiul este mai mult decât un eveniment de fundal: este condiția în care au crescut aceste societăți.',
    't000006': 'Citește integral secțiunea 1',
    't000007': 'Ce se întâmplă cu omenia?',
    't000008': 'Primul capitol întreabă dacă o civilizație dedicată conflictului neîncetat își poate păstra empatia. Supraviețuirea poate justifica sacrificii, dar o stare de urgență repetată poate face și cruzimea să pară normală. Textul pune aceste presiuni în contrast cu dorințele omenești obișnuite de a crea, de a-și iubi familia și de a construi ceva mai bun. Chiar și în acest univers sumbru, posibilitatea speranței contează. Capitolul nu oferă o ieșire ușoară din război; le cere cititorilor să observe cum fiecare invocare a necesității îi schimbă pe cei care o acceptă.',
    't000009': 'Citește integral secțiunea 2',
    't000010': 'Marile puteri',
    't000011': 'Capitolul al doilea descrie Imperiul și rivalii săi. Împăratul, Pușcașii Spațiali și Adeptus Mechanicus stau alături de instituții umane care depind de credință și de cunoștințe pierdute. Haosul, orcii, eldarii, tiranizii, necronii și alte forțe aduc amenințări și ambiții foarte diferite. Facțiunile fac galaxia să pară imensă, dar contrastul dintre ele limpezește și tema centrală: fiecare își imaginează ordinea sau supraviețuirea în felul său și niciuna nu poate evita costurile puterii.',
    't000012': 'Citește integral secțiunea 3',
    't000013': 'Instituții de protecție și control',
    't000014': 'Al treilea capitol urmărește Inchiziția și alte organizații însărcinate să apere omenirea. Ele detectează erezia, aplică legea, adună informații și mențin comunicarea peste distanțe uriașe. Ghidul descrie ordine specializate, asasini și astropați. Aceste organizații pot ține în funcțiune un imperiu fragil, dar secretomania și metodele lor aspre ridică o altă întrebare: cum deosebește o societate apărarea necesară de mecanismul opresiunii?',
    't000015': 'Citește integral secțiunea 4',
    't000016': 'Tehnologie fără progres ușor',
    't000017': 'Capitolul al patrulea trece în revistă nave stelare, armuri de putere, arme, oameni cu puteri psihice și tehnologiile stranii ale facțiunilor rivale. O mare parte din cunoașterea tehnică a Imperiului este păstrată prin ritual, ceea ce face întreținerea posibilă, dar limitează înțelegerea. Mașinile pot proteja oameni, pot prelungi viața sau pot devasta lumi întregi. Contrastul dintre dispozitivele avansate și stagnarea tehnică arată că a deține un instrument puternic nu este același lucru cu a ști să-i stăpânești folosirea.',
    't000018': 'Citește integral secțiunea 5',
    't000019': 'Viața de zi cu zi în Imperiu',
    't000020': 'Capitolul al cincilea părăsește câmpurile de luptă pentru a examina munca, religia, clasele sociale, educația și cultura. Lumile-stup, lumile-forjă și lumile agricole le dau locuitorilor vieți foarte diferite, dar datoria și supravegherea sunt teme comune. Arta și poveștile întăresc adesea credința oficială, deși răspunsurile individuale rămân diverse. Ghidul îi invită pe cititori să-și imagineze costul omenesc al unui imperiu a cărui supraviețuire depinde de o muncă vastă și inegală.',
    't000021': 'Citește integral secțiunea 6',
    't000022': 'Erezia lui Horus',
    't000023': 'Ultimul capitol urmărește Marea Cruciadă, coruperea lui Horus, războiul civil și Asediul Terrei. Soarta Împăratului și urmările evenimentelor explică de ce Imperiul de mai târziu este temător, rigid și bântuit de posibilități pierdute. Cartea nu tratează Erezia ca pe o listă de bătălii, ci ca pe o poveste despre încredere, trădare și instituții construite ca răspuns la traumă. Cititorii care vor să înțeleagă acest univers pot începe cu acest capitol și apoi se pot întoarce la cele anterioare ca să-i vadă consecințele îndelungate.',
    't000024': 'Citește integral secțiunea 7',
    't000025': 'Un motiv pentru a continua',
    't000026': 'Concluzia revine la puterea universului Warhammer 40.000 ca loc pentru povești. Războaiele, credințele și tehnologiile sale fac posibile multe istorii despre rezistență și sacrificiu. Cea mai folositoare intrare în cartea integrală este să urmărim o întrebare de-a lungul capitolelor: când oamenii luptă ca să supraviețuiască, ce hotărăsc că merită încă salvat?',
    't000027': 'Citește integral secțiunea 8',
}
for path in sorted(root.glob('*.json')):
    data = json.loads(path.read_text())
    for segment in data['segments']:
        segment['translation'] = translations[segment['id']]
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')
