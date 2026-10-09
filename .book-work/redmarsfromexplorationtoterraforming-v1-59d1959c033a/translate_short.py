import json
from pathlib import Path

root = Path(__file__).parent / 'translations/ro/short/chunks'
translations = {
    't000001': 'Marte Roșie: De la explorare la terraformare — Ediția de zece minute',
    't000002': 'Marte Roșie: De la explorare la terraformare',
    't000003': 'Romanul Marte Roșie al lui Kim Stanley Robinson îi oferă acestei cărți un cadru pentru a examina o așezare nevoită să ia hotărâri înainte de a le înțelege toate consecințele. Autorul urmărește problemele științifice, politice și etice ale călătoriei spre Marte, ale construirii unei societăți acolo și ale încercării de a transforma planeta. Întrebarea centrală este cine poate decide ce va deveni Marte. Tehnologia îi poate susține pe coloniști, dar nu poate rezolva singură conflictele privind resursele, independența sau valoarea unei lumi neatinse.',
    't000004': 'Dincolo de prima asolizare',
    't000005': 'Capitolul de deschidere așază colonizarea marțiană în perspectiva mai largă a viitorului sistemului solar. Lansatoarele reutilizabile, robotica și folosirea resurselor locale ar putea susține comunități permanente, dar distanța, radiațiile și proviziile limitate impun constrângeri severe. Textul ia în considerare și Luna, asteroizii și destinațiile din sistemul solar exterior. Explorarea devine colonizare numai atunci când oamenii pot construi adăposturi durabile și se pot înțelege asupra unor forme drepte de guvernare. Capitolul avertizează că extinderea prezenței umane ar putea repeta tiparele de exploatare de pe Pământ dacă această muncă nu este modelată de la început prin cooperare.',
    't000006': 'Citește integral secțiunea 2',
    't000007': 'Construirea unei societăți marțiene',
    't000008': 'Al doilea capitol folosește coloniștii lui Robinson pentru a întreba ce face posibilă o civilizație într-un mediu ostil. Ei au nevoie de aer, apă, hrană, adăpost și o producție locală pe care se pot baza. Au nevoie și de instituții, reguli economice și o înțelegere comună a rostului comunității lor. Oamenii de știință, inginerii și coloniștii nu sunt de acord asupra scopului coloniei. Unii văd în Marte un laborator sau o casă nouă; alții văd resurse și putere. Aceste neînțelegeri fac organizarea societății la fel de importantă ca ingineria.',
    't000009': 'Citește integral secțiunea 3',
    't000010': 'Ar trebui transformat Marte?',
    't000011': 'Capitolul despre terraformare explică propunerile de a încălzi Marte, de a-i îngroșa atmosfera și de a susține, în cele din urmă, forme de viață mai familiare. Aceste propuneri se lovesc de durate imense și de mari incertitudini. Argumentul etic este la fel de dificil: are omenirea dreptul să modifice o altă planetă și ce s-ar putea pierde înainte de a-i înțelege pe deplin mediul? În roman, susținătorii transformării se confruntă cu cei care vor să păstreze Marte în starea sa actuală. Cartea lasă tensiunea deschisă și îi invită pe cititori să cântărească supraviețuirea și expansiunea în raport cu cumpătarea și grija față de mediu.',
    't000012': 'Citește integral secțiunea 4',
    't000013': 'Puterea călătorește odată cu coloniștii',
    't000014': 'Al patrulea capitol urmărește influența companiilor asupra unei colonii care depinde încă de Pământ pentru echipamente și aprovizionare. Cine controlează aceste lucruri esențiale poate influența cercetarea, munca și deciziile politice. Textul pune ambițiile oamenilor de știință față în față cu organizațiile care urmăresc recuperarea investițiilor. Se întreabă dacă o societate nouă își poate păstra scopul public atunci când infrastructura vitală este deținută în altă parte. Marte poate fi departe de Pământ, dar instituțiile sale pot moșteni aceleași inegalități și conflicte.',
    't000015': 'Citește integral secțiunea 5',
    't000016': 'Pământul și Marte se îndepărtează',
    't000017': 'Al cincilea capitol examinează dependența și independența care prinde contur. Pământul furnizează cunoștințe și materiale; Marte dezvoltă experiență, cultură și interese locale. Terraformarea însăși devine un motiv de dispută între cei care câștigă din schimbarea rapidă și cei care îi suportă riscurile. Descoperirile tehnice pot circula în ambele sensuri, dar nu șterg deosebirile politice. Relația devine o încercare a capacității a două lumi legate între ele de a coopera fără ca una să o trateze pe cealaltă ca pe o proprietate.',
    't000018': 'Citește integral secțiunea 6',
    't000019': 'Momentele de cotitură ale poveștii',
    't000020': 'Ultimul capitol urmărește Primii O Sută, prima colonie, lupta privind terraformarea, creșterea puterii corporațiilor și rezistența marțiană. Asasinarea lui John Boone și revoluția arată cum se întâlnesc conflictele personale cu presiunile instituționale. Cartea nu tratează aceste întâmplări ca pe o simplă previziune a viitoarelor călătorii spațiale. Ele fac concrete întrebările de mai devreme: cine poate modela o planetă, cine controlează mijloacele supraviețuirii și ce fel de societate poate rezista rupturii de locul din care a pornit?',
    't000021': 'Citește integral secțiunea 7',
    't000022': 'Un motiv pentru a citi mai departe',
    't000023': 'Concluzia revine la responsabilitate. Marte oferă posibilitatea unui nou început, dar nu și o cale de a evita judecata omenească. Cititorii interesați de știința colonizării pot începe cu primele trei capitole; cei atrași de putere și independență pot urmări capitolele următoare. Ambele drumuri duc la aceeași întrebare: poate ambiția de a reface o lume să fie însoțită de înțelepciunea de a avea grijă de ea?',
    't000024': 'Citește integral secțiunea 8',
}
for path in sorted(root.glob('*.json')):
    data = json.loads(path.read_text())
    for segment in data['segments']:
        segment['translation'] = translations[segment['id']]
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')
