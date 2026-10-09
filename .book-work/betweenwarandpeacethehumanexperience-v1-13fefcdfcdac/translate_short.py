from pathlib import Path
import json
p=Path('.book-work/betweenwarandpeacethehumanexperience-v1-13fefcdfcdac/translations/ro/short/chunks/0001.json');d=json.loads(p.read_text())
t=[
'Între război și pace: experiența umană — Ediția de zece minute',
'Între război și pace: experiența umană',
'Această lectură tematică a romanului ',
'Război și pace',
' de Tolstoi îi urmărește pe Pierre Bezuhov, prințul Andrei Bolkonski și Natașa Rostova când războiul apasă asupra vieții aristocratice. Întreabă cum se schimbă iubirea, datoria, așteptările sociale și căutarea sensului atunci când speranțele personale întâlnesc violența publică. Cartea trece de la un argument pentru pacea activă prin baluri și câmpuri de luptă la o reflecție asupra compasiunii și responsabilității.',
'Alegerea păcii',
'În ',
'introducere',
', conflictul și cooperarea stau în centrul alegerii umane. Războiul poate crește din frică, neînțelegere și dorință de putere; poate scoate la iveală rezistență și sacrificiu, dar cu un preț omenesc uriaș. Pacea cere mai mult decât încetarea luptei. Cartea o leagă de dialog, dreptate, empatie și atenție la inegalitățile care hrănesc conflictele. Aceste idei pregătesc portretul personajelor lui Tolstoi.',
'Iubire și datorie înaintea furtunii',
'În ',
'capitolul întâi',
', strălucirea înaltei societăți ruse ascunde nesiguranța. Pierre, un moștenitor stângaci, dorește să aparțină unui grup dincolo de rang. Andrei caută sens în serviciul militar, dar începe să se îndoiască de promisiunea onoarei și gloriei. Natașa aduce energie tinerească și speranțe de iubire, deși tensiunea politică îi amenință viitorul alături de Andrei. Balurile și cinele oferă apropiere, dar vestea campaniilor lui Napoleon pătrunde în fiecare conversație. Capitolul arată că loialitățile intime nu pot rămâne separate de o societate care se îndreaptă spre război.',
'Capitolul al doilea',
' urmărește presiunea tot mai mare pe măsură ce conflictul se apropie. Neliniștea lui Pierre față de conversațiile superficiale se adâncește. Experiența lui Andrei pe front face idealurile nobile dureros de nepotrivite cu suferința și pierderea. Natașa trebuie să cântărească iubirea și loialitatea în mijlocul incertitudinii. Ritualurile familiare ale aristocrației devin goale când personajele înfruntă alegeri pe care nicio aparență socială nu le poate rezolva.',
'Dansând prin vremuri tulburi',
'Capitolul al treilea',
' revine la un bal din Sankt Petersburg. Pierre se simte un străin printre etalările de rang. Natașa găsește încă bucurie în dans, dar își face griji pentru Andrei și pentru război. Andrei stă între sentimentele pentru ea și datoria de soldat. Vulnerabilitatea împărtășită rupe pentru scurt timp aparențele când Natașa și Pierre vorbesc sincer, apoi dansează. Valsul devine imaginea unei frumuseți fragilizate de conflictul de dincolo de pereții sălii.',
'Câmpul de luptă și urmările lui',
'În ',
'capitolul al patrulea',
', Pierre merge pe front pentru a înțelege războiul direct. Suferința smulge strălucirea eroismului și îl îndreaptă spre compasiune. Loialitatea lui Andrei față de camarazi rămâne, dar el se întreabă dacă pierderile lor slujesc vreunui scop mai înalt. Natașa trăiește cu teama pentru Andrei și descoperă o iubire mai solicitantă prin grija pentru familie și prieteni. Cele trei drumuri se întâlnesc în recunoașterea pierderii, a vulnerabilității și a legăturii umane.',
'În ',
'concluzie',
', aceste teme trec dincolo de personaje. Pacea este înfățișată ca o alegere continuă, făcută prin dialog, empatie, cooperare și atenție la dreptate. Războiul poate dezvălui curaj, dar lasă și distrugere. Îndemnul final este să ducem lecțiile personajelor în alegerile obișnuite despre felul în care ascultăm, avem grijă și trăim împreună.',
]
assert len(t)==len(d['segments'])
for s,x in zip(d['segments'],t):s['translation']=x
p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
