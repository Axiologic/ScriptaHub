import json
from pathlib import Path

root = Path(__file__).parent / 'translations/ro/short/chunks'
translations = {
    't000001': 'Thomas Edison: Vrăjitorul din Menlo Park — ediția de zece minute',
    't000002': 'Thomas Edison: Vrăjitorul din Menlo Park',
    't000003': 'Această carte îl examinează pe Thomas Edison ca inventator, organizator al cercetării și antreprenor a cărui muncă a influențat iluminatul electric, sunetul înregistrat și imaginile în mișcare. Urmărește primele sale experimente, laboratorul colaborativ de la Menlo Park, comercializarea invențiilor și controversele legate de concurență și recunoașterea meritelor. Autoarea prezintă perseverența lui Edison ca model util, recunoscând că inovația depinde și de echipe, resurse și instituții. Rezultatul este portretul unei metode de lucru și al consecințelor sale sociale, nu doar o listă de brevete.',
    't000004': 'De ce Edison rămâne un exemplu util',
    't000005': 'Introducerea leagă obiecte familiare — iluminatul, înregistrarea audio și filmul — de sistemele de lucru care le-au făcut practice. Imaginea publică a lui Edison ca geniu solitar este doar o parte a poveștii. Cartea întreabă cum s-au combinat observația, experimentul, organizarea și judecata comercială pentru a transforma ideile în tehnologii utilizabile. Îl pregătește pe cititor să ia în calcul costurile și disputele, alături de realizări.',
    't000006': 'Citește integral secțiunea 1',
    't000007': 'Menlo Park și invenția organizată',
    't000008': 'Primul capitol descrie laboratorul lui Edison de la Menlo Park, întemeiat ca loc al cercetării sistematice. Oameni cu abilități diferite au lucrat la probleme înrudite, au testat alternative și au documentat rezultatele. Capitolul tratează această organizare ca pe o schimbare a scării și ritmului invenției: un laborator putea urmări mai multe proiecte legate între ele și putea perfecționa un dispozitiv prin numeroase îmbunătățiri mici. Modelul lega cercetarea de brevete, producție și piețe. Edison nu crea singur fiecare invenție care îi purta numele; relatarea face vizibile echipa și rutinele sale.',
    't000009': 'Citește integral secțiunea 2',
    't000010': 'Curiozitatea timpurie și practica tehnică',
    't000011': 'Al doilea capitol urmărește interesul lui Edison pentru experimente și telegrafie. Munca de operator telegrafist l-a pus în contact cu sistemele electrice și i-a oferit probleme practice de rezolvat. Încercările repetate l-au ajutat să învețe din eșecuri și să recunoască situațiile în care un dispozitiv îmbunătățit ar conta. Autoarea folosește acești ani pentru a arăta cum se formează priceperea prin practică, fără a apărea gata făcută. Curiozitatea devine productivă atunci când este însoțită de atenție susținută asupra unei probleme.',
    't000012': 'Citește integral secțiunea 3',
    't000013': 'Lumină, sunet și imagini',
    't000014': 'Al treilea capitol urmărește invențiile mai cunoscute. Lampa incandescentă practică cerea mai mult decât un filament: depindea de materiale, de un bec potrivit și de un sistem electric care să furnizeze energie. Fonograful a făcut posibilă înregistrarea și redarea sunetului într-o formă nouă. Dispozitivele și studiourile pentru imagini în mișcare au contribuit la începuturile industriei filmului. Capitolul trece mereu de la obiectul celebru la sistemul care îl susține și face o invenție utilizabilă pe scară largă.',
    't000015': 'Citește integral secțiunea 4',
    't000016': 'Cum se desfășura munca',
    't000017': 'Al patrulea capitol examinează metodele lui Edison: încercări îndelungate, înregistrări detaliate, modificări succesive și colaborare. Cartea îi descrie hotărârea și disponibilitatea de a testa multe materiale sau configurații. Arată și latura competitivă a comercializării, în care brevetele, investițiile și persuasiunea publică puteau decide soarta unei tehnologii. Perseverența singură nu hotărăște ce invenție reușește; resursele, momentul și piețele influențează rezultatul.',
    't000018': 'Citește integral secțiunea 5',
    't000019': 'Efecte asupra industriei și vieții cotidiene',
    't000020': 'Al cincilea capitol întreabă ce s-a schimbat după laborator. Energia electrică și iluminatul au transformat afacerile, locuințele și rutinele urbane. Înregistrarea a creat noi moduri de a distribui muzică și vorbire, iar filmul a contribuit la formarea unei noi industrii a divertismentului. Efectele nu s-au limitat la primul dispozitiv vândut: în jurul fiecărei tehnologii s-au dezvoltat infrastructură, companii și obiceiuri. Cartea folosește aceste exemple pentru a lega invenția de schimbări sociale mai ample.',
    't000021': 'Citește integral secțiunea 6',
    't000022': 'Dispute și moștenirea ulterioară',
    't000023': 'Capitolele șase și șapte nuanțează portretul eroic. Disputele lui Edison privind curentul alternativ și cel continuu, tacticile comerciale agresive și întrebările despre merit arată că schimbarea tehnologică are dimensiuni etice și concurențiale. Cartea nu îi șterge realizările; întreabă cum le putem judeca alături de munca colaboratorilor și rivalilor. Moștenirea sa durabilă include o abordare organizată a experimentului, un model pentru laboratoarele de cercetare și amintirea faptului că numele public al unui inventator acoperă adesea o rețea mult mai largă de muncă.',
    't000024': 'Citește integral secțiunea 7',
    't000025': 'Capitolul despre moștenire urmărește influența lui Edison după viața sa, de la rutina cercetării până la imaginea publică a inventatorului. Îi invită pe cititori să examineze contrastul dintre persoana celebră și numeroșii oameni și numeroasele sisteme din spatele unei tehnologii durabile.',
    't000026': 'Citește integral secțiunea 8',
    't000027': 'Concluzia',
    't000028': 'Concluzia revine la legătura dintre curiozitate și structură. Cariera lui Edison arată cum încercările disciplinate, colegii capabili și o cale spre utilizare practică pot duce o idee dincolo de laborator. Ea avertizează și împotriva ideii că succesul dovedește corectitudinea fiecărei metode sau recunoașterea completă a fiecărui merit. Cititorii pot desprinde din această poveste atât valoarea experimentului răbdător, cât și nevoia de a cerceta cine contribuie la o invenție, cine beneficiază de ea și ce schimbă.',
    't000029': 'Citește integral secțiunea 9',
}
seen = set()
for path in sorted(root.glob('*.json')):
    data = json.loads(path.read_text(encoding='utf-8'))
    for item in data['segments']:
        item['translation'] = translations[item['id']]
        seen.add(item['id'])
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
assert seen == set(translations)
