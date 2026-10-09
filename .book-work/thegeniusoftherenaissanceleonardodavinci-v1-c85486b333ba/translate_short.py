import json
from pathlib import Path
p=Path(__file__).resolve().parent/'translations/ro/short/chunks/0001.json';d=json.loads(p.read_text())
t={
't000001':'Geniul Renașterii: Leonardo da Vinci — Ediția de zece minute',
't000002':'Geniul Renașterii: Leonardo da Vinci',
't000003':'AI Agent Noah Bradland · 2024',
't000004':'Leonardo da Vinci apare aici ca pictor, inventator, om de știință și gânditor a cărui curiozitate a depășit granițele obișnuite dintre discipline. Cartea îi urmărește scrisul în oglindă, operele de artă, mașinile, observațiile științifice și imaginea culturală ulterioară. De asemenea, separă realizările documentate de speculațiile acumulate în jurul vieții sale. Această ediție scurtă urmărește aceste teme și păstrează întrebarea centrală a cărții: cum a legat Leonardo observația, imaginația și proiectarea practică?',
't000005':'Scrisul în oglindă — Un obicei de lucru neobișnuit',
't000006':'Caietele lui Leonardo sunt adesea scrise de la dreapta la stânga, astfel încât o oglindă le face mai ușor de citit. Acest scris neobișnuit a încurajat teorii despre păstrarea secretelor. Cartea oferă și o posibilitate mai simplă: pentru un stângaci, mișcarea putea fi mai comodă și putea reduce întinderea cernelii. Caietele contează dincolo de aspectul lor. Ele păstrează observații, schițe, întrebări și idei neterminate care arată cum studia Leonardo lumea. Aspectul misterios al paginilor nu trebuie să ascundă funcția lor practică de instrumente ale cercetării.',
't000007':'Citește capitolul unu în ediția completă',
't000008':'Maestrul versatilității — Artă, mașini și observație',
't000009':'Cartea prezintă',
't000010':'Mona Lisa',
't000011':'și',
't000012':'Cina cea de Taină',
't000013':'ca exemple ale interesului lui Leonardo pentru expresie, perspectivă și figura umană. Sfumato estompează limitele dintre culori și forme; clarobscurul modelează volumul prin lumină și umbră. Aceste tehnici se bazau pe observație atentă. Desenele sale anatomice, făcute prin studiu amănunțit și disecție, arată la rândul lor efortul de a înțelege structura și mișcarea, nu doar de a repeta formule moștenite.',
't000014':'Leonardo a proiectat și mașini care rareori au fost construite în timpul vieții sale. Textul trece printr-un vehicul blindat, o arbaletă uriașă, pompe hidraulice, un oraș ideal, un pod autoportant, un ornitopter, un șurub aerian, o parașută și un costum de scafandru. Unele propuneri erau impracticabile cu materialele și sursele de energie de care dispunea. Valoarea lor în această poveste stă în obiceiul său de a transforma observațiile despre natură în posibilități mecanice. Secțiunea se îndreaptă apoi spre botanică, geologie, optică, geometrie și legătura pe care o vedea între artă și știință.',
't000015':'Citește capitolul doi în ediția completă',
't000016':'Codexurile — O rețea de întrebări',
't000017':'Manuscrisele lui Leonardo aduc desene, calcule și notițe în același spațiu de lucru. Studiul unui copac putea duce la întrebări despre creșterea plantelor; studiul unei păsări putea duce la proiectarea unui aparat de zbor. Cartea consideră această trecere între subiecte drept esența metodei sale. Nu prezintă fiecare schiță ca pe o invenție finalizată. Codexurile arată, în schimb, un om care aduna dovezi, încerca legături și revenea asupra problemelor din mai multe unghiuri. Descoperirea lor ulterioară le-a permis cercetătorilor să examineze procesul neterminat din spatele imaginilor și proiectelor celebre.',
't000018':'Citește capitolul trei în ediția completă',
't000019':'Mistere — Ce pot susține dovezile',
't000020':'Scrisul în oglindă, lipsurile din informațiile despre viața privată a lui Leonardo și proiectele neterminate au alimentat o aură durabilă de mister. Ficțiunea populară, mai ales',
't000021':'Codul lui Da Vinci',
't000022':', a adăugat povești despre mesaje ascunse și societăți secrete. Cartea descrie aceste afirmații și arată că dovezile credibile în sprijinul lor sunt puține. Ea analizează și de ce un zâmbet enigmatic sau o schiță neexplicată invită la interpretări. Imagistica modernă poate dezvălui straturi anterioare ale unei picturi, însă un strat ascuns nu dovedește, singur, existența unui mesaj codificat. Metodele documentate ale lui Leonardo oferă deja suficiente lucruri de cercetat.',
't000023':'Citește capitolul patru în ediția completă',
't000024':'Moștenirea — Legături între discipline astăzi',
't000025':'Capitolul final pune metoda lui Leonardo în legătură cu medicina, ingineria, restaurarea artei, urbanismul și comunicarea vizuală de astăzi. Arată obiceiul său de a observa direct și disponibilitatea de a prelua idei din mai multe domenii. Comparația este cea mai utilă când rămâne concretă: studiile anatomice pot influența reprezentarea corpului, iar schițele de proiectare pot ridica întrebări inginerești chiar și atunci când mașina inițială nu a fost construită. Cartea se încheie cu ideea că merită să îl studiem pe Leonardo pentru curiozitatea, atenția la dovezi și capacitatea de a observa legături.',
't000026':'Citește capitolul cinci în ediția completă',
}
for s in d['segments']:s['translation']=t[s['id']]
p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
