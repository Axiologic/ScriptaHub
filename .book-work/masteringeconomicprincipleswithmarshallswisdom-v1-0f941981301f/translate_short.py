import json
from pathlib import Path

root = Path(__file__).parent / 'translations/ro/short/chunks'
translations = {
    't000001': 'Stăpânirea principiilor economice prin înțelepciunea lui Marshall — ediția de zece minute',
    't000002': 'Stăpânirea principiilor economice prin înțelepciunea lui Marshall',
    't000003': 'Această carte introduce instrumentele lui Alfred Marshall pentru înțelegerea alegerilor făcute în condiții de raritate. Trece de la cerere și ofertă prin echilibrul pieței și teoriile valorii, apoi întreabă cum pot informa aceste idei deciziile din afaceri și politicile publice. Autorul tratează modelele economice drept explicații utile, observând totodată că comportamentul uman și condițiile sociale complică diagramele simple. Scopul este să întrebăm ce se schimbă când se modifică prețurile, costurile, preferințele sau instituțiile și cine resimte aceste schimbări.',
    't000004': 'Pornind de la alegerile obișnuite',
    't000005': 'Introducerea așază economia în viața de zi cu zi: gospodăriile aleg ce cumpără, firmele decid ce produc, iar guvernele cântăresc utilizări concurente ale resurselor limitate. În loc să prezinte piața ca pe o mașinărie abstractă, îi invită pe cititori să observe compromisurile din spatele prețurilor vizibile. Cadrul lui Marshall oferă un vocabular pentru aceste alegeri. Cartea cere și luarea în considerare a efectelor etice și sociale, deoarece o tranzacție eficientă nu rezolvă fiecare întrebare despre acces sau echitate.',
    't000006': 'Citește integral secțiunea 1',
    't000007': 'Cerere, ofertă și elasticitate',
    't000008': 'Primul capitol explică cele două laturi cunoscute ale unei piețe. Cererea descrie cât sunt dispuși cumpărătorii să achiziționeze la prețuri diferite; oferta descrie cât sunt dispuși vânzătorii să pună la dispoziție. Schimbarea uneia dintre ele poate modifica prețul și cantitatea unui bun. Capitolul introduce elasticitatea pentru a arăta că nu toate reacțiile au aceeași amploare. Oamenii pot reduce brusc cumpărarea unui produs când prețul lui crește, schimbând însă foarte puțin consumul unui bun necesar. Firmele pot folosi aceste tipare pentru a planifica producția, iar consumatorii pentru a interpreta prețurile în schimbare.',
    't000009': 'Gândirea marginală adaugă un alt strat. O decizie depinde adesea de beneficiul și costul unei unități suplimentare, nu de valoarea totală a ceea ce a fost deja cumpărat sau produs. Cartea folosește această idee pentru a lega alegerile personale de comportamentul pieței.',
    't000010': 'Citește integral secțiunea 2',
    't000011': 'Echilibrul ca relație în mișcare',
    't000012': 'Al doilea capitol descrie echilibrul pieței drept punctul în care cumpărările și vânzările planificate se întâlnesc la un anumit preț. Când prețul este prea mare, bunurile nevândute îi pot împinge pe vânzători să îl ajusteze; când este prea mic, lipsurile îi pot face pe cumpărători să concureze. Mecanismul prețurilor poate coordona numeroase alegeri separate, deși piețele reale pot reacționa lent sau inegal. Capitolul examinează și surplusul consumatorului și al producătorului ca moduri de a descrie câștigurile schimbului. Concurența contează deoarece numărul și puterea participanților la piață influențează împărțirea acestor câștiguri.',
    't000013': 'Citește integral secțiunea 3',
    't000014': 'Ce dă valoare unui lucru?',
    't000015': 'Al treilea capitol tratează diferența dintre utilitate, raritate și prețul pieței. Un bun poate fi util, dar ieftin când se găsește din abundență, în vreme ce un obiect rar poate avea un preț ridicat. Preferințele și utilitatea marginală influențează cât sunt dispuși cumpărătorii să plătească; costurile de producție influențează ce pot oferi vânzătorii. Autorul folosește abordarea lui Marshall pentru a evita reducerea valorii la o singură cauză. Prețul pieței apare din interacțiunea mai multor condiții, așa că înțelegerea lui cere atenție la ambele părți ale schimbului.',
    't000016': 'Astfel, modelul devine mai util pentru deciziile reale. O firmă nu poate stabili un preț durabil uitându-se doar la costuri, iar un cumpărător nu poate deduce valoarea intrinsecă numai din preț. Ambele părți trebuie să înțeleagă alternativele, constrângerile și schimbările cererii.',
    't000017': 'Citește integral secțiunea 4',
    't000018': 'Aplicarea principiilor dincolo de diagramă',
    't000019': 'Al patrulea capitol aplică acest cadru la alegeri de afaceri, politici publice și probleme sociale. Firmele pot folosi informații despre cerere și costuri când aleg producția sau prețurile. Responsabilii de politici publice pot examina cum impozitele, regulile sau programele de sprijin schimbă stimulentele și accesul. Cartea arată că raționamentul economic este util tocmai fiindcă intervențiile pot avea efecte dincolo de prima lor țintă. Îi îndeamnă pe cititori să se gândească și la distribuție: un rezultat al pieței poate aduce beneficii inegale, iar unii oameni pot rămâne fără resurse esențiale.',
    't000020': 'Capitolul nu propune o singură rețetă de politică publică. Îi încurajează pe cititori să identifice presupunerile, să examineze dovezile și să întrebe cine suportă costurile sau primește beneficiile.',
    't000021': 'Citește integral secțiunea 5',
    't000022': 'De ce rezistă acest cadru',
    't000023': 'Concluzia susține că principiile lui Marshall rămân utile chiar dacă tehnologia și instituțiile se schimbă. Raritatea, stimulentele și compromisurile apar și în industriile noi, dar formele lor concrete trebuie cercetate, nu presupuse. Cartea se încheie legând alfabetizarea economică de întrebări mai bune: ce a provocat schimbarea unui preț, cine se poate adapta, ce costuri sunt ascunse și ce ar putea modifica în altă parte o soluție propusă? Aceste întrebări fac din acest cadru un instrument al judecății, nu un înlocuitor al ei.',
    't000024': 'Citește integral secțiunea 6',
}
seen = set()
for path in sorted(root.glob('*.json')):
    data = json.loads(path.read_text(encoding='utf-8'))
    for item in data['segments']:
        item['translation'] = translations[item['id']]
        seen.add(item['id'])
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
assert seen == set(translations)
