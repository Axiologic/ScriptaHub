import json
from pathlib import Path
p=Path('.book-work/hitchhikersguidetothegalaxy-v1-a51bfc42457d/translations/ro/short/chunks/0001.json');d=json.loads(p.read_text())
t=[
'Ghidul autostopistului galactic — ediția de zece minute',
'Ghidul autostopistului galactic',
'Un călător obișnuit într-un cosmos absurd',
'Introducerea îl urmărește pe Arthur Dent de la distrugerea Pământului până în universul comic al lui Douglas Adams. Ford Prefect îl salvează, prosopul devine un obiect indispensabil, iar un ghid le recomandă călătorilor să nu intre în panică. Extratereștrii, tehnologia improbabilă și un mister uriaș transformă dezorientarea unui om într-o aventură spațială.',
'Cartea tratează călătoria ca pe mai mult decât o înșiruire de glume. Prietenia îi oferă lui Arthur un punct de sprijin, iar absurdul cosmic lasă loc întrebărilor despre sens, supraviețuire și locul nostru într-un univers straniu.',
'Citește această parte în ediția integrală',
'Peștele Babel și comunicarea',
'Primul capitol examinează Peștele Babel, o creatură care traduce instantaneu orice limbă. Îl compară cu programele de traducere și dispozitivele purtabile, întrebând cum ar putea comunicarea fără piedici să schimbe diplomația, cultura și relațiile zilnice.',
'Eliminarea barierelor lingvistice poate apropia oamenii, dar diferențele de vorbire poartă și identitate și context. Capitolul cercetează neînțelegerea, puterea și riscul de a considera traducerea un înlocuitor deplin al ascultării.',
'Citește această parte în ediția integrală',
'O nouă formă comică pentru science-fiction',
'Al doilea capitol susține că Adams a lărgit posibilitățile science-fictionului, alăturând ideilor mari micile supărări cotidiene și spiritul ascuțit. Extratereștrii birocratici, mașinile nesigure și obiceiurile omenești recognoscibile răstoarnă așteptările genului.',
'Umorul său accesibil i-a ajutat pe scriitori și pe cititori să își imagineze science-fictionul ca pe un gen jucăuș și reflexiv. Capitolul îi urmărește influența în comedie, construcția lumilor și disponibilitatea genului de a râde de sine.',
'Citește această parte în ediția integrală',
'Cum funcționează comedia cosmică',
'Al treilea capitol începe cu distrugerea Pământului pentru o șosea hiperspațială. Catastrofa planetară devine un inconvenient birocratic, iar hârțogăria vogonilor și poezia lor groaznică întunecă gluma. Adams pune mereu mize uriașe lângă meschinăriile zilnice.',
'Răsturnările neașteptate, subestimarea și personajele improbabile susțin contrastul. Umorul nu șterge ideile tulburătoare de dedesubt: instituțiile pot fi indiferente, cunoașterea poate fi incompletă, iar omenirea s-ar putea să nu fie centrul universului.',
'Citește această parte în ediția integrală',
'Patruzeci și doi și căutarea sensului',
'Al patrulea capitol privește răspunsul „42” dat de Deep Thought la întrebarea despre viață, univers și tot restul. Rezultatul absurd arată slăbiciunea căutării unui răspuns precis fără înțelegerea întrebării. Călătoria lui Arthur păstrează vie cercetarea, în ciuda acestui eșec.',
'Motorul Improbabilității Infinite pune la încercare ideile familiare despre cauzalitate și posibilitate. Personaje precum Slartibartfast trezesc curiozitatea despre creație și scop. Capitolul sugerează că sensul poate fi construit prin atenție, relații și umor, nu descoperit într-o formulă finală.',
'Citește această parte în ediția integrală',
'Unelte folositoare, sisteme nesigure',
'Al cincilea capitol tratează tehnologia ca pe o sursă de progres cu două tăișuri. Peștele Babel face posibilă comunicarea, iar Heart of Gold străbate distanțe uriașe prin improbabilitate. Ghidul oferă călătorilor vaste informații într-o formă portabilă.',
'Totuși, dispozitivele și sistemele pot eșua, induce în eroare sau crea dependențe noi. Capitolul folosește invențiile lui Adams pentru a întreba dacă puterea tehnică îi face pe oameni mai înțelepți și cum poate rămâne activă judecata omenească într-o lume a confortului și complexității.',
'Citește această parte în ediția integrală',
'Evenimentele-cheie ale călătoriei',
'Al șaselea capitol trasează începutul poveștii: vogonii distrug Pământul, Arthur și Ford scapă, iar Heart of Gold îi salvează. Zaphod, Trillian și Marvin li se alătură în drumul spre Magrathea, planeta cunoscută pentru construirea altor lumi.',
'Acolo Arthur află scopul ascuns al Pământului în căutarea Întrebării Ultime. Răspunsul lui Deep Thought este 42, dar întrebarea rămâne necunoscută. Șoarecii care comandaseră Pământul urmăresc creierul lui Arthur, iar acesta scapă fără o explicație finală.',
'Citește această parte în ediția integrală',
'Păstrează-ți curiozitatea și prosopul',
'Concluzia reunește lecturile despre comedie, filosofie și tehnologie. Universul lui Adams îi invită pe cititori să se îndoiască de răspunsurile simple și să întâmpine incertitudinea cu curiozitate. Sfatul practic „Nu intra în panică” nu rezolvă misterul; îi ajută pe călători să meargă mai departe.',
'Citește această parte în ediția integrală'
]
assert len(t)==len(d['segments']),(len(t),len(d['segments']))
for x,v in zip(d['segments'],t):x['translation']=v
p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
