import json
from pathlib import Path
root=Path('.book-work/thematrixuniverseajourneythroughrealityandbeyond-v1-28c4be91976c/translations/ro/short/chunks')
chunks={
'0001.json':[
'Universul Matrix: o călătorie prin realitate și dincolo de ea — ediția de zece minute',
'Universul Matrix: o călătorie prin realitate și dincolo de ea',
'Întrebarea din spatele simulării',
'Introducerea intră în Matrix printr-o posibilitate tulburătoare: lumea familiară ar putea fi o iluzie construită. Mașinile susțin o realitate virtuală comună, în timp ce oamenii rămân neștiutori de captivitatea lor. Neo se alătură unei mici rezistențe care trece între Pământul fizic devastat și orașul simulat, încercând să îi trezească pe ceilalți.',
'Povestea dă premisei științifico-fantastice o latură filosofică. Neo, Morpheus, Trinity și Agent Smith îl conduc pe cititor spre întrebări despre percepție, conștiință, liber arbitru și granița dintre oameni și mașini. Pastilele roșie și albastră transformă o întrebare grea într-o alegere: să înfrunți adevărul nesigur sau să rămâi în aparența liniștitoare.',
'Citește această parte în ediția integrală',
'Controlul într-un secol conectat',
'Primul capitol întreabă ce ar însemna o simulare asemenea Matricei într-o societate deja modelată de inteligența artificială, supraveghere și medii virtuale. Primejdia ei nu este doar un peisaj artificial, ci controlul informației și percepției. Oamenii ar putea accepta un sistem care le spune ce este normal, de dorit și posibil.',
'Capitolul privește și dependența dintre oameni și mașini, precum și rezistența. Dispozitivele inteligente și serviciile digitale pot extinde capacitățile omenești, dar și vulnerabilitatea la control. Hackerii și activiștii pentru drepturi digitale devin analogii contemporane ale rebelilor care apără gândirea independentă și memoria culturală.',
'Citește această parte în ediția integrală',
'Matricea și Zion',
'Al doilea capitol citește lumea simulată și Zion ca două societăți contrastante. Munca repetitivă și consumul din Matrice ascund controlul sistemic. Condițiile materiale aspre din Zion cer, dimpotrivă, cooperare, adaptare și o luptă comună pentru supraviețuire.',
'Privirea antropologică întreabă cum rolurile, miturile și ritualurile formează fiecare comunitate. Alesul și Oracolul dau rezistenței profeție și conducere, dar ridică și întrebări despre credință, alegere și responsabilitate colectivă. Niciuna dintre societăți nu poate fi înțeleasă doar prin tehnologia ei.',
'Citește această parte în ediția integrală',
'Să înveți că lumea este cod',
'Al treilea capitol pornește de la șocul descoperirii că senzațiile obișnuite sunt semnale generate. Pastila roșie sfărâmă încrederea în lumea familiară; antrenamentul din simulare arată că legile ei fizice aparent ferme pot fi îndoite. Creșterea lui Neo face percepția și credința centrale pentru ceea ce pot face personajele.',
'Cartea leagă premisa de vechi îndoieli despre cunoaștere. Dacă simțurile pot fi manipulate, realitatea nu poate fi stabilită doar prin senzație. Totuși, trezirea costă: adevărul cere un nou fel de viață, nu doar deținerea unor informații secrete.',
'Citește această parte în ediția integrală',
'Lanțurile minții',
'Al patrulea capitol tratează controlul ca pe un fenomen psihologic și fizic. Locuitorii Matricei cred că aleg liber, în timp ce sistemul le îngustează opțiunile pe care și le pot imagina. Rebelii trebuie să înfrunte obiceiuri implantate, teamă și condiționare socială, nu doar Agenți și mașini.',
'Eliberarea ridică și întrebări etice. Trezirea cuiva poate răsturna o viață care i se părea plină de sens. Chemarea lui Morpheus de a elibera mintea descrie, prin urmare, efortul de a vedea limitele ascunse, de a cântări urmările și de a alege în pofida nesiguranței.',
'Citește această parte în ediția integrală',
'Dincolo de văl',
'Al cincilea capitol compară Matricea cu peștera lui Platon: umbrele devin cod digital, iar aparențele familiare ascund o structură mai profundă. El întreabă cum pot oamenii cunoaște ceva când simțurile și așteptările îi pot înșela. Cypher întruchipează ispita întoarcerii într-o iluzie confortabilă.',
'Arhitectul prezintă cunoașterea din punctul de vedere al proiectării sistemului și al controlului. Contrastul dintre perspectiva sa calculată și experiența trăită a rebelilor ține întrebarea deschisă: a înțelege un sistem nu înseamnă a-i înțelege și pe oamenii din interior.',
'Citește această parte în ediția integrală',
'Patru aventuri speculative',
'Al șaselea capitol trece de la analiză la povești propuse în universul Matrix. Un oraș virtual uitat îndoaie spațiul și timpul; un labirint digital schimbător ține captiv un hacker capabil să rescrie codul. O răscoală a programelor întreabă dacă ființele artificiale merită libertate, iar o eroare temporală îl trimite pe Neo prin versiuni mai vechi ale simulării.'
],
'0002.json':[
'Un ultim scenariu trimite echipajul după un program ascuns, legat de Sursă, prin medii digitale instabile. Acestea sunt extinderi imaginare ale universului, nu evenimente prezentate drept canon. Fiecare aventură duce mai departe întrebările cărții despre libertate, control și natura realității.',
'Citește această parte în ediția integrală',
'De ce persistă întrebările',
'Concluzia revine de la acțiune și aventurile inventate la cercetarea centrală. Matrix oferă mai mult decât spectacol, fiindcă lumile sale fac tehnologia, trezirea, rebeliunea și cunoașterea să pară urgente pentru fiecare. Cartea îi invită pe cititori să pună sub semnul întrebării presupunerile și sistemele care le modelează propria viață.',
'Citește această parte în ediția integrală'
]}
for name,values in chunks.items():
 p=root/name;d=json.loads(p.read_text());assert len(values)==len(d['segments']),(name,len(values),len(d['segments']))
 for x,v in zip(d['segments'],values):x['translation']=v
 p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
