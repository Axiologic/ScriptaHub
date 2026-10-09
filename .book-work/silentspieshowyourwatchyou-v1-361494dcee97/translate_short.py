import json
from pathlib import Path

t = {
't000001': 'Spioni tăcuți: cum te urmăresc dispozitivele tale? — Ediția de zece minute',
't000002': 'Spioni tăcuți: cum te urmăresc dispozitivele tale?',
't000003': 'Telefoanele, aplicațiile și dispozitivele conectate din locuință pot colecta mai multe informații decât se așteaptă proprietarii lor. Cartea întreabă unde ajung aceste date, ce pot deduce companiile din ele și cum poate cineva limita colectarea nedorită. Trece de la microfoane și permisiunile aplicațiilor la rețeaua Wi-Fi de acasă, profilarea comercială și alegerile zilnice privind confidențialitatea. Unele scenarii din sursă sunt prezentate ca îngrijorări sau posibilități, nu ca fapte demonstrate despre fiecare dispozitiv. Firul practic este să înțelegem permisiunile, conexiunile și folosirea datelor înainte de a hotărî ce schimbăm.',
't000004': 'De ce începe cartea cu viața privată digitală',
't000005': 'Introducerea descrie dispozitivele care ne însoțesc zi de zi: telefoane inteligente, brățări de fitness, difuzoare inteligente, televizoare și alte aparate conectate. Comoditatea creează și fluxuri de informații despre comportament. O aplicație poate cunoaște o locație, un dispozitiv poate raporta cum este folosit, iar o platformă poate combina multe semnale mici într-un profil detaliat. Autorul leagă aceste semnale de publicitate și întreabă dacă utilizatorii înțeleg ce au acceptat să împărtășească. Deschiderea prezintă viața privată ca problemă de vizibilitate și control, nu ca cerere de abandonare a tehnologiei.',
't000006': 'Citește integral secțiunea 1',
't000007': 'Telefoane, microfoane și permisiuni',
't000008': 'Primul capitol se concentrează asupra telefonului. Descrie microfoane, asistenți vocali și aplicații care cer acces la sunet, locație și alte date. Sursa folosește experiența familiară a unei reclame apărute după o conversație pentru a ridica suspiciunea unei ascultări pasive. Exemplul ilustrează îngrijorarea cărții; capitolul nu demonstrează că fiecare asemenea reclamă a fost produsă de o conversație înregistrată pe ascuns. Mai general, permisiunile stabilesc ce funcții poate folosi o aplicație, iar activitatea din fundal poate face acea folosire greu de observat.',
't000009': 'Cititorul este încurajat să vadă ce poate colecta un telefon și de ce are cu adevărat nevoie fiecare aplicație. Accesul la microfon, accesul la locație și identificatorii publicitari sunt căi diferite către informații. Deosebirea lor face problema mai precisă decât tratarea întregului dispozitiv ca pe un singur observator ascuns.',
't000010': 'Citește integral secțiunea 2',
't000011': 'Rețeaua tăcută de acasă',
't000012': 'Capitolul al doilea se îndreaptă către Wi-Fi și numărul tot mai mare de obiecte conectate din locuință. Un difuzor inteligent, televizor, termostat sau aparat de filmat poate schimba date cu un serviciu ori alt dispozitiv chiar când proprietarul nu îl folosește activ. Capitolul descrie atât comoditatea rețelei, cât și riscurile de securitate create de parole slabe, software neactualizat sau dispozitive insuficient separate. Recomandă schimbarea datelor de acces implicite, instalarea actualizărilor și luarea în calcul a unei rețele separate pentru aparatele conectate în care avem mai puțină încredere.',
't000013': 'Ideea esențială este că o rețea casnică este un mediu, nu doar un router și un telefon. Fiecare dispozitiv conectat în plus poate deveni o altă sursă de date sau un alt punct care cere întreținere. Să știm ce este conectat constituie primul pas în alegerea a ceea ce ar trebui să rămână în rețea.',
't000014': 'Citește integral secțiunea 3',
't000015': 'Ce pot face companiile cu datele',
't000016': 'Al treilea capitol urmărește informațiile colectate în sistemele comerciale. Aplicațiile și platformele pot analiza interese, deplasări, navigare și folosirea dispozitivelor pentru a construi profiluri destinate publicității personalizate. Cartea susține că profilarea poate influența și mesajele pe care oamenii le văd despre chestiuni publice. Exemplele ei invită la cercetarea modului în care datele sunt împărtășite, deduse și vândute; trebuie citite ca argument despre o posibilă influență, nu ca afirmație că o singură companie controlează fiecare decizie personală.',
't000017': 'Permisiunile se află la intrarea în acest sistem, dar efectele pot apărea departe de aplicația care a adunat informațiile. Cititorul care înțelege lanțul de la colectare la profilare poate pune întrebări mai bune despre oportunitatea accesului cerut de un serviciu.',
't000018': 'Citește integral secțiunea 4',
't000019': 'Controlul practic și argumentul final',
't000020': 'Capitolul al patrulea și concluzia se îndreaptă spre alegerile pe care le poate face cineva: să verifice permisiunile pentru microfon și locație, să limiteze activitatea inutilă din fundal, să elimine aplicațiile care cer prea mult acces, să întărească setările rețelei de acasă și să actualizeze dispozitivele. Cartea sugerează și instrumente de căutare sau mesagerie care pun accent pe confidențialitate și amintește drepturi legale prin care o persoană poate cere acces la datele sale ori ștergerea lor. Drepturile și setările exacte depind de loc, serviciu și dispozitiv, așa că obiceiul util este inspectarea opțiunilor disponibile în realitate.',
't000021': 'Cartea se încheie respingând o alegere absolută între comoditate și viață privată. Le cere cititorilor să devină participanți activi la deciziile despre datele lor: să observe compromisurile, să schimbe ce pot controla și să revină asupra alegerilor pe măsură ce dispozitivele și serviciile se schimbă. Conștientizarea este primul pas; întreținerea repetată îi dă efect practic.',
't000022': 'Citește integral secțiunea 5',
}

base = Path(__file__).parent / 'translations/ro/short/chunks'
for path in sorted(base.glob('*.json')):
    data = json.loads(path.read_text(encoding='utf-8'))
    for segment in data['segments']:
        segment['translation'] = t[segment['id']]
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
