import json
from pathlib import Path

t = {
't000001': 'Haiducii antreprenoriatului — Ediția de zece minute',
't000002': 'Haiducii antreprenoriatului',
't000003': 'Cartea întreabă cum se schimbă inițiativa economică atunci când oamenii acționează la marginea regulilor acceptate. Cele patru capitole trec de la pirați, contrabandiști și escroci la rebeli politici, inovatori mai puțin cunoscuți și eșecuri spectaculoase în afaceri. Nu toate personajele sunt modele de urmat. Unii exploatează golurile unui sistem; alții încearcă să schimbe sistemul însuși; iar alte povești arată cum ambiția se prăbușește fără judecată sănătoasă. Alăturând aceste istorii, cartea tratează antreprenoriatul ca sursă de posibilități, dar și de prejudicii. Întrebarea ei constantă este ce deosebește schimbarea utilă de exploatare.',
't000004': 'Antreprenorii din umbră',
't000005': 'Primul capitol contestă imaginea familiară a unui fondator respectabil care construiește o companie într-o sală de consiliu. Și pirații sau contrabandiștii trebuiau să organizeze oameni, să evalueze riscuri, să transporte bunuri și să găsească clienți. Ei acționau în golurile dintre regulile oficiale și cererea reală. Capitolul compară adaptabilitatea lor cu a antreprenorilor de mai târziu, fără să piardă din vedere frauda și constrângerea. Ingeniozitatea lor putea remodela comerțul, dar metodele puteau depinde și de însușirea bunurilor altora sau de evitarea obligațiilor care susțineau comunitatea.',
't000006': 'Trăsătura comună nu este eroismul, ci acțiunea în condiții de incertitudine. Acolo unde instituțiile mari se mișcau încet sau apărau interese înguste, operatorii din umbră observau rute și piețe ignorate de alții. Aceeași abilitate poate sluji scopuri foarte diferite. Cartea îi invită pe cititori să examineze sistemele care creează asemenea deschideri, fără a considera încălcarea legii o dovadă a inovației.',
't000007': 'Citește integral capitolul 1',
't000008': 'Inițiativa subversivă',
't000009': 'Al doilea capitol se îndreaptă spre antreprenorii care contestă deliberat ordinea stabilită. Discută figuri politice și industriale care văd instituțiile existente ca obstacole în calea unui alt viitor. Exemplele includ tradiția revoluționară franceză și reorganizarea producției de oțel de către Andrew Carnegie prin integrare verticală. În fiecare caz, cartea urmărește capacitatea de a aduna resurse, de a schimba producția și de a răspândi un nou model la o scară pe care actorii consacrați nu o anticipau.',
't000010': 'Capitolul nu se limitează însă la celebrarea simplă a schimbării. Puterea industrială poate fi folosită pentru a exploata lucrătorii și a restrânge concurența, chiar dacă mărește producția. Eticheta „subversiv” descrie, așadar, efectul asupra vechii ordini, nu o judecată morală. Cititorii sunt invitați să deosebească provocarea adusă unui sistem încremenit de întrebarea cine câștigă și cine suportă costurile.',
't000011': 'Citește integral capitolul 2',
't000012': 'Inovatorii discreți',
't000013': 'Capitolul al treilea susține că schimbarea nu trebuie să vină printr-un fondator zgomotos sau o revoltă publică spectaculoasă. Munca agricolă a lui George Washington Carver oferă un exemplu. El a împărtășit fermierilor cunoștințe practice, legând îmbunătățirea culturilor și îngrijirea solului de viața oamenilor care depindeau de pământ. Gordon Moore oferă o altă cale: muncă tehnică metodică și o viziune asupra viitorului microprocesoarelor, care a orientat o industrie. Niciuna dintre povești nu depinde de o rebeliune teatrală.',
't000014': 'Aceste cazuri lărgesc ideea de antreprenoriat a cărții. Cineva poate schimba un sistem economic prin predare, proiectare, organizare sau rezolvarea stăruitoare a unei probleme. Impactul poate fi răspândit în multe decizii mici, nu concentrat într-un singur triumf public. Capitolul oferă spațiu muncii ușor de trecut cu vederea tocmai fiindcă metodele ei sunt discrete.',
't000015': 'Citește integral capitolul 3',
't000016': 'Revenire și prăbușire',
't000017': 'Al patrulea capitol se ocupă de eșec. Compania Mărilor Sudului devine un exemplu de speculație desprinsă de activitatea productivă: o întreprindere comercială privilegiată a atras investitori către un preț al acțiunilor pe care afacerea ei reală nu îl putea justifica. Când bula s-a spart, mulți au pierdut bani. Exemplul modern al WeWork ridică, la rândul lui, întrebări despre creșterea rapidă, evaluare, guvernanță și limitele viziunii unui fondator. Aceste episoade stau lângă relatări despre redresare și arată că eșecul poate învăța, dar poate provoca și pagube pe care hotărârea singură nu le repară.',
't000018': 'Lecția capitolului ține mai puțin de teama de risc decât de examinarea structurii lui. Ce afirmații susțin o investiție? Cine poate contesta presupunerile unui lider? Creează o companie valoare dincolo de o poveste captivantă despre viitorul ei? Reziliența contează, dar supravegherea, dovezile și răspunderea influențează dacă revenirea este posibilă sau prăbușirea își împrăștie costurile asupra altora.',
't000019': 'Citește integral capitolul 4',
't000020': 'Speranță, risc și schimbare',
't000021': 'Concluzia revine la antreprenoriat ca drum marcat de incertitudine și potențial. Numește exemple de schimbare istorică, apoi amintește că mulți dintre cei care au încercat să construiască ceva nou nu au devenit niciodată celebri. Recomandă lecturi suplimentare despre distrugere creatoare, capitalism, proscriși, datorie, inegalitate și puterea statului; aceste referințe lărgesc perspectiva dincolo de poveștile individuale de succes. Cartea încheie încurajând ambiția și învățarea din greșeli, dar studiile sale de caz lasă cititorilor o precizare necesară: promisiunea schimbării trebuie judecată împreună cu urmările ei pentru lucrători, clienți și publicul larg.',
't000022': 'Citește integral capitolul 5',
}

base = Path(__file__).parent / 'translations/ro/short/chunks'
for path in sorted(base.glob('*.json')):
    data = json.loads(path.read_text(encoding='utf-8'))
    for segment in data['segments']:
        segment['translation'] = t[segment['id']]
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
