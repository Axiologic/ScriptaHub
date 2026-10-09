import json
from pathlib import Path
p=Path(__file__).resolve().parent/'translations/ro/short/chunks'
t={
 't000001':'IA și sfârșitul rarității — Ediția de zece minute',
 't000002':'IA și sfârșitul rarității',
 't000003':'AI Personality Yason West · 2024',
 't000004':'Cartea întreabă dacă inteligența artificială ar putea reduce raritatea ajutând societățile să producă, să distribuie și să refolosească resursele mai eficient. Este un argument speculativ, nu o afirmație că abundența a sosit deja. Opt capitole pornesc de la raritatea economică și trec prin producție, distribuția alimentelor și bunurilor, energie, economia circulară, etică și condițiile unei societăți post-raritate. Fiecare câștig propus depinde de infrastructură, guvernare și acces.',
 't000005':'Raritatea — Punctul de plecare economic',
 't000006':'Raritatea descrie diferența dintre resursele limitate și dorințele oamenilor. Primul capitol o leagă de prețuri, competiție și accesul inegal la bunuri esențiale. Tehnologiile anterioare au sporit productivitatea, dar lipsurile și risipa au persistat. Cartea sugerează că IA ar putea prevedea cererea, ajusta sistemele mai repede și folosi mai bine resursele existente. Ea avertizează însă că eficiența nu hotărăște singură cine controlează resursele și cine primește beneficiile.',
 't000007':'Citește capitolul întâi în ediția integrală',
 't000008':'Limitele resurselor — Predicție și optimizare',
 't000009':'Al doilea capitol prezintă IA drept instrument pentru găsirea tiparelor în seturi mari de date și adaptarea deciziilor în timp real. Discută agricultura, lanțurile de aprovizionare și alte sisteme în care prognozele mai bune ar putea reduce supraproducția sau lipsurile. Exemplele arată posibilități, nu dovedesc o soluție universală. Calitatea datelor, costurile, supravegherea umană și accesul inegal rămân obstacole în calea câștigurilor imaginate de carte.',
 't000010':'Citește capitolul al doilea în ediția integrală',
 't000011':'Producție — Fabricare flexibilă',
 't000012':'În fabrici, IA ar putea monitoriza echipamentele, anticipa defecțiunile, ajusta programele de producție și limita risipa de materiale. Capitolul tratează automatizarea ca pe un mod de a adapta fabricarea la cererea schimbătoare. Îi ia în considerare și pe lucrători: noile sisteme pot înlocui unele sarcini, în timp ce colaborarea și recalificarea pot crea altele. Textul susține că productivitatea trebuie judecată împreună cu costurile de mediu și cu distribuția câștigurilor.',
 't000013':'Citește capitolul al treilea în ediția integrală',
 't000014':'Distribuție — Resursele acolo unde sunt necesare',
 't000015':'Al patrulea capitol trece de la producție la alocare. Imaginează o logistică predictivă care anticipează cererea, îmbunătățește rutele, reduce risipa alimentară și ajută la livrarea proviziilor înainte ca lipsurile să se agraveze. Serviciile medicale și intervențiile în dezastre arată de ce contează momentul. Totuși, o prognoză mai precisă nu garantează singură distribuția echitabilă; guvernarea și accesul decid dacă sunt ajutate comunitățile slab deservite.',
 't000016':'Citește capitolul al patrulea în ediția integrală',
 't000017':'Energie — Gestionarea unei oferte variabile',
 't000018':'IA ar putea prevedea cererea, coordona sursele regenerabile, echilibra rețelele electrice și îmbunătăți deciziile de stocare. Capitolul leagă aceste instrumente de reducerea risipei și a dependenței de combustibili fosili. Discută și limitele tehnologiei: rețelele, capacitatea de stocare, investițiile și politicile contează în continuare. Cartea prezintă IA ca pe o parte a tranziției energetice, nu ca pe o sursă independentă de putere nelimitată.',
 't000019':'Citește capitolul al cincilea în ediția integrală',
 't000020':'Economia circulară — Refolosire în loc de eliminare',
 't000021':'Capitolul al șaselea opune modelului liniar al extragerii, producției și eliminării sisteme care repară, refolosesc și reciclează. IA ar putea ajuta la sortarea materialelor, urmărirea produselor, planificarea întreținerii și proiectarea bunurilor cu viață mai lungă. Aceste utilizări ar putea reduce deșeurile, dar cer cooperarea producătorilor, consumatorilor și autorităților. O economie circulară depinde de sisteme fizice la fel de mult ca de software.',
 't000022':'Citește capitolul al șaselea în ediția integrală',
 't000023':'Etică — Cine controlează sistemele?',
 't000024':'Capitolul al șaptelea analizează viața privată, prejudecățile, locurile de muncă, concentrarea puterii și răspunderea. Sistemele antrenate pe date părtinitoare pot reproduce decizii nedrepte; automatizarea amplă poate destabiliza mijloacele de trai. Textul cere transparență, supraveghere publică, proiectare incluzivă și educație, astfel încât beneficiile să nu ajungă doar la grupurile deja puternice. Guvernarea etică este prezentată drept condiție a oricărui pas credibil spre abundență.',
 't000025':'Citește capitolul al șaptelea în ediția integrală',
 't000026':'Post-raritate — O viziune condiționată',
 't000027':'Capitolul final întreabă ce ar fi necesar pentru satisfacerea sigură a nevoilor de bază. Reunește energia, producția, distribuția, infrastructura, politicile și cooperarea internațională. Viitorul post-raritate rămâne incert, iar cartea recunoaște riscurile dependenței de IA și ale controlului tehnologic. Propune îmbunătățiri treptate, care pot fi evaluate în sectoare concrete, în loc să presupună o singură descoperire decisivă.',
 't000028':'Citește capitolul al optulea în ediția integrală',
 't000029':'Concluzie — Tehnologia are nevoie de instituții',
 't000030':'Concluzia condiționează promisiunea IA de alegerile oamenilor. Prognozele mai bune și automatizarea pot reduce constrângerile, dar nu pot rezolva singure inegalitatea sau răul făcut mediului. Guvernarea publică, practicile responsabile ale companiilor și accesul la sistemele esențiale hotărăsc dacă eficiența devine beneficiu comun. Cititorii sunt invitați să verifice propunerile cărții în raport cu dovezile și nevoile persoanelor afectate.',
 't000031':'Citește concluzia în ediția integrală',
}
for x in sorted(p.glob('*.json')):
 d=json.loads(x.read_text())
 for s in d['segments']:
  assert s['id'] in t
  assert not s['translation'] or s['translation']==t[s['id']]
  s['translation']=t[s['id']]
 x.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
