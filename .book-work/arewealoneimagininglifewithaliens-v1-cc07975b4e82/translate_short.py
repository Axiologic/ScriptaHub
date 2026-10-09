import json
from pathlib import Path


root = Path(__file__).parent / 'translations/ro/short/chunks'
translations = {
    't000001': 'Suntem singuri? Imaginându-ne viața alături de extratereștri — ediția de zece minute',
    't000002': 'Suntem singuri? Imaginându-ne viața alături de extratereștri',
    't000003': 'Această carte urmărește două întrebări adesea tratate separat: unde ar putea exista viață dincolo de Pământ și cum ar reacționa oamenii dacă ar găsi-o? Începe cu stelele și exoplanetele, folosește extremofilele terestre pentru a lărgi ideea de mediu locuibil, apoi examinează telescoapele, roverele și un posibil contact. Autoarea îi invită pe cititori să deosebească dovezile căutate de imaginația privind consecințele sociale. Nicio descoperire extraterestră nu este prezentată ca fapt stabilit; scenariile sunt posibilități care conturează miza științifică și umană.',
    't000004': 'Întrebarea de la început',
    't000005': 'Introducerea privește spre un cer plin de stele și întreabă dacă o altă lume ar putea susține viață, poate chiar viață inteligentă. O detectare confirmată ar ridica imediat întrebări despre comunicare, identitate, teamă și coexistență. Autoarea trece intenționat dincolo de întrebarea mai restrânsă dacă viața există. Dacă răspunsul este da, ce presupuneri despre omenire s-ar schimba și ce ar cere un contact respectuos? Aceste întrebări dau capitolelor științifice un scop uman.',
    't000006': 'Citește integral secțiunea 1',
    't000007': 'Un univers de posibile cămine',
    't000008': 'Primul capitol așază căutarea în raport cu dimensiunea universului. Stelele au planete, iar unele exoplanete se află în regiuni unde apa lichidă ar putea persista. Cartea introduce zona locuibilă și sistemul TRAPPIST-1 ca moduri de a gândi despre lumi candidate. Astronomii pot studia o atmosferă pentru gaze asociate anumitor procese, dar o atmosferă promițătoare nu dovedește existența organismelor. Capitolul înfruntă și marea tăcere: un univers vast poate oferi multe șanse pentru viață, dar niciun contact neechivoc nu a fost confirmat.',
    't000009': 'Această tensiune contează. Numerele uriașe fac întrebarea demnă de pus, dar nu pot oferi singure răspunsul. Autoarea vede în incertitudine un motiv de a continua căutarea și de a îmbunătăți instrumentele cu care observăm lumile îndepărtate.',
    't000010': 'Citește integral secțiunea 2',
    't000011': 'Ce ne învață condițiile extreme de pe Pământ',
    't000012': 'Al doilea capitol trece de la planetele îndepărtate la viața din medii considerate cândva neospitaliere. Microbii de lângă izvoarele hidrotermale, organismele din locuri acide sau sărate și tardigradele rezistente arată că viața terestră poate suporta condiții dincolo de experiența obișnuită a omului. Lecția nu este că fiecare lume aspră este locuită. Presupunerile noastre despre locurile în care căutăm ar trebui să reflecte ceea ce sistemele vii au demonstrat deja.',
    't000013': 'Europa și Enceladus apar ca exemple de luni înghețate cu oceane sub suprafață, care merită investigate. Marte rămâne un alt candidat pentru urme de viață microbiană trecută sau adăpostită. Aceste lumi extind căutarea dincolo de o simplă planetă asemănătoare Pământului, lăsând observației întrebarea decisivă: trăiește ceva acolo?',
    't000014': 'Citește integral secțiunea 3',
    't000015': 'Instrumente care transformă posibilitatea în dovezi',
    't000016': 'Al treilea capitol explică de ce tehnologia este centrală pentru căutare. Spectroscopia citește lumina care trece printr-o atmosferă sau este reflectată de ea și poate dezvălui indicii chimice. Telescoapele puternice pot examina exoplanete îndepărtate; exploratorii robotici pot inspecta mai direct lumile apropiate. Cartea discută despre telescopul spațial James Webb, roverele marțiene și idei pentru instrumente și misiuni viitoare. Fiecare instrument răspunde unei părți diferite a problemei: unde să privim, ce conține o planetă sau o lună și dacă un posibil semn de viață rezistă verificărilor atente.',
    't000017': 'Deosebirea dintre o biosemnătură și un organism confirmat străbate acest capitol. Oxigenul sau metanul pot fi interesante, dar chimia și geologia pot produce semnale înșelătoare. Contează probele și mai multe tipuri de dovezi. Exemplele despre misiuni reflectă contextul sursei din 2024; cititorul ar trebui să trateze planurile de lansare și stadiul misiunilor ca afirmații istorice ale acelei ediții.',
    't000018': 'Citește integral secțiunea 4',
    't000019': 'Dacă descoperirea devine realitate',
    't000020': 'Al patrulea capitol își imaginează ce ar putea însemna o descoperire sigură. Chiar și viața microbiană găsită în altă parte ne-ar schimba înțelegerea biologiei și a locului Pământului într-un univers mai larg. Dovezile unei inteligențe ar aduce întrebări mai grele despre limbaj, putere, religie, cultură și decizii politice. Autoarea nu pretinde că știe cum ar reacționa omenirea. În schimb, capitolul folosește reacții posibile — uimire, teamă, cooperare și conflict — pentru a întreba cum ne-am putea pregăti.',
    't000021': 'Istoria întâlnirilor dintre societățile umane avertizează asupra inegalității și neînțelegerii, deși nu ne poate spune cum ar arăta contactul cu o viață nonumană. Cartea îi îndeamnă pe cititori să întâmpine incertitudinea cu curiozitate, modestie și grijă, fără să presupună nici o utopie, nici o amenințare.',
    't000022': 'Citește integral secțiunea 5',
    't000023': 'Concluzia',
    't000024': 'Concluzia revine la legătura dintre explorarea spre exterior și înțelegerea de sine. Exoplanetele, extremofilele și instrumentele au schimbat ce pot cerceta oamenii, dar nu au rezolvat întrebarea centrală. Căutarea vieții pune la încercare și felul în care definim viața, tratăm dovezile ambigue și ne imaginăm împărțirea universului. Cartea îl invită pe cititor să pornească de la indiciile științifice și să ducă incertitudinea mai departe, spre întrebarea profundă a coexistenței.',
}
seen = set()
for path in sorted(root.glob('*.json')):
    data = json.loads(path.read_text(encoding='utf-8'))
    for item in data['segments']:
        item['translation'] = translations[item['id']]
        seen.add(item['id'])
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
assert seen == set(translations)
