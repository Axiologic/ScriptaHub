import json
from pathlib import Path

w=Path(__file__).resolve().parents[1]
base=w/'translations/ro/short/chunks'
values=[
"Crimă și ispită în haosul fraților Karamazov — Ediția de zece minute",
"Crimă și ispită în haosul fraților Karamazov",
"Ediția de zece minute",
"Acest eseu însoțitor discută uciderea și crizele ulterioare din romanul lui Dostoevsky",
"Frații Karamazov",
". Cititorii care doresc să descopere singuri evenimentele centrale ale romanului ar trebui să îl citească mai întâi. Eseul îi urmărește pe Fyodor Pavlovich și pe fiii săi Dmitri, Ivan și Alyosha prin conflictele familiei, ispită, vină și căutarea izbăvirii. Răspunsurile lor diferite la suferință sunt privite ca o înfruntare între pasiune, rațiune și credință.",
"Introducere: ispită și răspundere",
"Introducerea pornește de la lupta dintre dorință și cumpătare. Ispita poate ține de plăcere sau putere, dar poate fi și intelectuală: dorința de a pune la îndoială orice limită morală. Eseul definește crima în sens larg, incluzând trădarea propriei persoane și a celorlalți, pe lângă încălcarea legii. Întrebarea centrală este dacă un om care a făcut rău își poate asuma răspunderea, poate căuta iertarea și poate găsi o cale prin haosul rezultat. Aceste teme pregătesc lectura familiei Karamazov, ale cărei conflicte private ajung la o tragedie publică.",
"Capitolul întâi: o familie dezbinată",
"Fyodor Pavlovich Karamazov este prezentat drept un tată egoist, a cărui lăcomie și desfrânare modelează viețile fiilor săi. Dmitri este impulsiv și pătimaș, atras de plăcere, dar dornic și de ceva mai bun. Ivan se încrede în intelect și se îndoiește de certitudinea religioasă, însă întrebările morale îl izolează. Alyosha alege credința și compasiunea fără a ignora suferința. Eseul îi privește pe frați ca pe trei răspunsuri diferite la moștenirea tatălui lor: exces, revoltă și grijă spirituală.",
"Deosebirile dintre ei nu îi feresc de tensiunile familiei. Purtarea lui Fyodor adâncește rivalitatea și resentimentul, iar fiecare fiu trebuie să hotărască în ce măsură acceptă exemplul tatălui. Capitolul transformă relația lor într-o întrebare despre răul moștenit: pot copiii scăpa de vătămarea morală produsă de un părinte? Se încheie în timp ce conflictele nerezolvate se îndreaptă spre uciderea lui Fyodor.",
"Capitolul doi: crimă și vină împărțită",
"Dmitri este suspectul evident după uciderea lui Fyodor. Și-a amenințat tatăl, se ceartă cu el pentru moștenire și îi este rival pentru afecțiunea Grushenkăi. Totuși, eseul întreabă dacă violența și nesăbuința lui echivalează cu uciderea. Arestarea și procesul îl obligă să înfrunte atât acuzația, cât și răul provocat de alegerile sale anterioare.",
"Ivan nu a comis fizic crima, dar eseul leagă detașarea și îndoiala lui filosofică de întrebarea mai largă a răspunderii morale. Încercarea sa de a rămâne în afara suferinței eșuează când urmările crimei îl ajung din urmă. Alyosha nu este nici suspect, nici judecător. Încearcă să înțeleagă ce s-a întâmplat și caută iertarea în mijlocul destrămării familiei. Și Grushenka este mai mult decât obiectul unei rivalități: relația ei cu Dmitri îi poate adânci ispita sau îi poate deschide o cale spre schimbare. Capitolul distinge între cel care săvârșește o faptă și numeroșii oameni ale căror alegeri au creat condițiile ei.",
"Capitolul trei: Ivan, Alyosha și Marele Inchizitor",
"Revolta lui Ivan împotriva suferinței inocenților formează centrul filosofic al capitolului. Nu poate accepta o armonie viitoare care ar justifica durerea copiilor. În parabola Marelui Inchizitor, Hristos revine în timpul Inchiziției spaniole și este acuzat că a dat omenirii o libertate pe care nu o poate purta. Inchizitorul susține că oamenii preferă siguranța și certitudinea poverii de a alege între bine și rău. Eseul vede aici întrebarea lui Ivan: cere credința mai multă libertate decât pot îndura oamenii?",
"Alyosha îi răspunde lui Ivan printr-un sărut, nu printr-un contraargument, repetând gestul lui Hristos din parabolă. Eseul îl prezintă ca pe un răspuns întemeiat pe compasiune, nu pe demonstrație intelectuală. Dezacordul lor rămâne nerezolvat. Întâlnirea ulterioară a lui Ivan cu diavolul arată cum rațiunea se întoarce împotriva lui, în timp ce vina, suferința și îndoiala îl împing spre nebunie. Alyosha continuă să caute speranță și legături umane. Contrastul îi invită pe cititori să se întrebe cum pot coexista gândirea și iubirea atunci când niciuna nu poate șterge suferința.",
"Capitolul patru: trei căi prin haos",
"Ultimul capitol numește romanul un ghid de supraviețuire și îi folosește pe frați ca exemple, nu ca modele perfecte. Drumul lui Dmitri constă în recunoașterea greșelilor și asumarea răspunderii chiar în timp ce contestă o acuzație nedreaptă. Prăbușirea lui Ivan avertizează împotriva transformării intelectului în izolare de trăirea omenească. Alyosha întruchipează grija răbdătoare, iertarea și rezistența spirituală. Fiecare răspuns are limite, dar împreună arată de ce supraviețuirea cere mai mult decât autoprotecție.",
"Concluzia revine la legătura dintre ispită, crimă și izbăvire. Eseul susține că vina nu primește răspuns doar prin pedeapsă, iar îndoiala nu dispare prin certitudini facile. Legăturile cu ceilalți, recunoașterea propriilor limite și compasiunea oferă o cale înainte prin confuzia morală. Conflictele familiei îi invită pe cititori să își examineze alegerile: cum răspund dorinței, cum echilibrează credința cu rațiunea și ce este necesar pentru a repara răul făcut.",
"Citește pasajele corespunzătoare din ediția completă",
"Introducere: ispită și răspundere",
"Capitolul întâi: o familie dezbinată",
"Capitolul doi: crimă și vină",
"Capitolul trei: credință și rațiune",
"Capitolul patru: răspunsuri la haos",
"Concluzie",
]
segments=[]
for path in sorted(base.glob('*.json')):
    data=json.loads(path.read_text());segments.extend(data['segments'])
assert len(segments)==len(values),(len(segments),len(values))
lookup=dict(zip((s['id'] for s in segments),values))
for path in sorted(base.glob('*.json')):
    data=json.loads(path.read_text())
    for s in data['segments']:s['translation']=lookup[s['id']]
    path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
print(len(values),'short segments translated')
