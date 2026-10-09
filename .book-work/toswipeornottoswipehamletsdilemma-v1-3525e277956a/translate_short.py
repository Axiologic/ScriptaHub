import json
from pathlib import Path
p=Path('.book-work/toswipeornottoswipehamletsdilemma-v1-3525e277956a/translations/ro/short/chunks/0001.json')
d=json.loads(p.read_text())
t=[
"A da swipe sau a nu da swipe: dilema lui Hamlet — ediția de zece minute",
"A da swipe sau a nu da swipe: dilema lui Hamlet",
"Mai este Hamlet relevant?",
"Primul capitol privește vechea întrebare a lui Hamlet prin prisma atenției moderne. Prințul care ezită între viață și moarte devine, în satiră, omul incapabil să hotărască ce să posteze sau să urmărească. Rețelele sociale, serialele văzute dintr-o bucată și mesajele prescurtate îndepărtează piesa originală, dar nesiguranța lui Hamlet începe să ne pară familiară.",
"Glumele nu lămuresc definitiv întrebarea relevanței. Sub parodie se află crima, trădarea, durerea și teama de a acționa greșit. Capitolul sugerează că reflecția lentă poate conta tocmai fiindcă lumea contemporană răsplătește opiniile pripite. Încheierea sa ne invită să recunoaștem câte un «moment hamletian» în nehotărârile de zi cu zi.",
"Citește această parte în ediția integrală",
"Nebunia ca imagine publică",
"Capitolul al doilea imaginează Elsinore ca loc de muncă al brandurilor și relațiilor publice. Nebunia jucată de Hamlet devine o imagine personală schimbătoare; Ofelia este transformată în influenceriță, Polonius în furnizor de sloganuri, iar Claudius și Gertrude în manageri ai unei povești despre familia recompusă. Acestea sunt analogii comice, nu afirmații despre intențiile istorice ale lui Shakespeare.",
"Piesa din interiorul piesei este tratată ca un mesaj ușor de distribuit, conceput să-l demaște pe rege. Satira întreabă dacă o imagine publică poate ascunde durerea și incertitudinea morală. Rolurile schimbătoare ale lui Hamlet se împotrivesc mesajului consecvent cerut de marketingul modern, iar faima durabilă a tragediei devine gluma finală despre un «brand de durată».",
"Citește această parte în ediția integrală",
"Economia răzbunării",
"Hamletonomia transformă tragedia într-un experiment economic deliberat absurd. Scrima le dă de lucru făuritorilor de arme; supravegherea creează observatori; florile Ofeliei îi ajută pe florari; pasajele secrete îi angajează pe tâmplari; actorii, groparii și vânzătorii de otravă prosperă. Până și fantomei i se atribuie începutul acestui lanț de evenimente.",
"Capitolul duce gluma spre diplomație, înmormântări și preluarea puterii de către Fortinbras. Nu este un model economic al Danemarcei, ci o cale de a vedea cum răzbunarea trimite urmări prin întreaga curte. Fiecare nouă «piață în creștere» amintește și de violența și pierderea pe care limbajul vesel încearcă să le ascundă.",
"Citește această parte în ediția integrală",
"Hamlet 2.0",
"O refacere digitală mută monologurile pe platforme video și fantoma în fluxurile rețelelor sociale, oferind o aplicație pentru fiecare dilemă. Hamlet ar putea să-și întrebe urmăritorii prin sondaj, să lanseze o provocare virală împotriva lui Claudius sau să angajeze gropari printr-o aplicație. Capitolul împinge ideea spre munca la cerere, fantezia spațială și un startup imaginar.",
"Alternativa cea mai pătrunzătoare este mai liniștită: un terapeut ar putea înțelege viziunea lui Hamlet despre tatăl său drept durere neprocesată, nu ordin de răzbunare. Actualizările comice ridică astfel o întrebare serioasă despre ce poate rezolva tehnologia și ce mai are nevoie de judecată și grijă omenească.",
"Citește această parte în ediția integrală",
"Un pod înapoi spre piesă",
"Concluzia explică scopul parodiei. Limbajul lui Shakespeare și ritmul său dramatic lent pot părea îndepărtate cititorilor obișnuiți cu formele digitale scurte, deși întrebările piesei despre identitate, moralitate și putere rămân apropiate. Platformele familiare și glumele oferă un punct de intrare fără a înlocui textul original.",
"Umorul poate face necunoscutul mai accesibil și poate invita la comparații între intrigile de curte și conflictele online. Cartea le cere cititorilor să folosească aceste paralele critic, apoi să revină la Hamlet. Întrebarea sa centrală este dacă cititorii contemporani vor alege să se apropie de literatura clasică și ce ar putea descoperi atunci.",
"Citește această parte în ediția integrală"
]
assert len(t)==len(d['segments']),(len(t),len(d['segments']))
for x,v in zip(d['segments'],t):x['translation']=v
p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
