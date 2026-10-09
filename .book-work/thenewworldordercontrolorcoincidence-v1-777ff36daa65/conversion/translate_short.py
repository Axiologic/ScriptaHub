#!/usr/bin/env python3
"""Direct Romanian translation of the stable short-reader chunk."""
import json
from pathlib import Path
w=Path(__file__).resolve().parents[1]
p=w/'translations/ro/short/chunks/0001.json';d=json.loads(p.read_text())
t=[
'Noua ordine mondială: control sau coincidență? — Ediția de zece minute',
'Noua ordine mondială: control sau coincidență?',
'Ediția de zece minute',
'Acest eseu explorează de ce poveștile despre Illuminati și o „nouă ordine mondială” au căpătat forță în timpul pandemiei de COVID-19. El întreabă dacă restricțiile de urgență, sistemele digitale și mesajele repetate în media ar putea deveni instrumente de control durabil. Capitolele trec de la Illuminati istorici din Bavaria la supravegherea din timpul pandemiei, apoi la știri și cultura populară. Suspiciunile și întrebările îi aparțin eseului; cartea nu demonstrează că un grup secret a orchestrat pandemia sau controlează guvernele.',
'Introducere: puterea ascunsă și restricțiile vizibile',
'Introducerea pornește de la atracția teoriilor despre societăți secrete. Ele explică evenimente complexe prin ideea unei elite nevăzute aflate în spatele guvernelor, economiilor și mass-mediei. Carantinele, supravegherea digitală și comunicarea în masă din timpul pandemiei au reaprins aceste temeri, fiindcă autoritățile publice au putut impune brusc măsuri cu efecte ample. Eseul întreabă cine a avut de câștigat, dacă restricțiile au fost doar un răspuns sanitar și cât de mult au modelat canalele de informare percepția publică. Acestea sunt întrebări formulate de autor, nu dovezi ale unui plan ascuns și coordonat.',
'Capitolul întâi: Illuminati, istorie și legendă modernă',
'Primul capitol identifică Illuminati istorici drept o societate bavareză fondată de Adam Weishaupt în 1776. El descrie idealurile iluministe, secretul ca mijloc de protecție și interzicerea grupului de către guvernul bavarez după aproximativ un deceniu. Capitolul separă apoi această origine cunoscută de speculația că societatea ar fi supraviețuit clandestin și ar fi pătruns în politică, finanțe, educație și mass-media. Întrebarea recurentă este dacă afirmațiile moderne despre Illuminati descriu o organizație încă activă sau un mit influent.',
'Pandemia este exemplul contemporan folosit de capitol. Unii adepți ai teoriilor conspirației au interpretat carantinele, munca online, urmărirea digitală și propunerile de pașapoarte de vaccinare ca posibile repetiții pentru supunerea maselor. Eseul susține și că izolarea și incertitudinea ar putea spori dependența de autorități. El examinează uniformitatea mesajelor de sănătate publică și puterea conglomeratelor media de a modela opinia, recunoscând totodată că aceste mesaje au fost importante pentru limitarea răspândirii virusului. Mai târziu, citează relațiile unor corporații cu Germania nazistă ca exemplu de instituții puternice care au acționat în spatele unei imagini publice respectabile. Această istorie nu demonstrează, prin ea însăși, legătura propusă de capitol cu o organizație Illuminati permanentă.',
'Capitolul al doilea: măsurile de urgență și teoria noii ordini mondiale',
'Al doilea capitol se îndreaptă spre „noua ordine mondială”, o teorie despre elite care ar urmări un guvern global unic. El descrie cum pandemia a mutat munca, educația și viața socială pe ecrane, în timp ce restricțiile de călătorie și interdicțiile de circulație limitau deplasarea fizică. Susținătorii teoriei au văzut aceste schimbări ca pe un test al lucrurilor pe care populațiile ar fi dispuse să le accepte. Capitolul pune întrebarea mai precisă dacă un control temporar în criză ușurează un control mai intruziv ulterior.',
'Urmărirea digitală a contactelor, pașapoartele de vaccinare și monitorizarea online devin principalele exemple. Eseul recunoaște scopul lor de sănătate publică, dar întreabă dacă sistemele construite pentru urgențe ar putea rămâne în funcțiune sau ar putea fi folosite în alte scopuri. Preocuparea lui este extinderea posibilă a supravegherii și pierderea autonomiei. Capitolul se încheie fără să dovedească un plan global deliberat. El lasă cititorilor două interpretări concurente: un efort coordonat de concentrare a puterii sau o serie de răspunsuri la criză care au produs efecte similare fără o conducere centrală.',
'Capitolul al treilea: știri, frică și cultură populară',
'Al treilea capitol întreabă cine modelează informația prin care oamenii înțeleg o criză. El descrie relatările intense despre pandemie, apelurile repetate de a rămâne acasă și de a avea încredere în experți, precum și posibilitatea ca frica să mărească disponibilitatea publicului de a accepta restricții. Eseul tratează rețelele sociale și instituțiile de presă drept canale care pot informa, influența sau îngusta dezbaterea publică. El întreabă dacă mesajele asemănătoare din mai multe țări au fost un răspuns sanitar necesar sau o formă de condiționare; nu oferă dovezi că o singură elită le-ar fi coordonat.',
'Cultura populară adaugă o a doua direcție. Poveștile despre supraveghere, viitoruri distopice și putere concentrată pot face familiare anumite posibilități politice. Capitolul se întreabă dacă imaginile ficționale repetate pregătesc publicul să accepte mai mult control. Revine apoi la o afirmație mai generală: narațiunile influențează comportamentul, iar cei care controlează canalele majore de comunicare au influență. Aceasta nu înseamnă că filmele sau serialele ar fi fost concepute în cadrul unui proiect secret de guvernare.',
'Concluzie: întrebarea rămâne deschisă',
'Concluzia revine la pandemie ca exemplu al vitezei cu care se pot schimba regulile sociale, munca și comunicarea. Ea leagă cele trei preocupări ale eseului: legendele despre societăți secrete, posibila supraviețuire a supravegherii de urgență și influența relatărilor media. Autorul îi îndeamnă pe cititori să urmărească echilibrul dintre siguranță și libertate, să examineze instituțiile puternice și să pună la îndoială poveștile venite din orice tabără. Poziția finală este un apel la vigilență în condiții de incertitudine. Eseul ridică probleme legate de control, dar nu stabilește dacă „noua ordine mondială” este o realitate organizată sau o explicație întemeiată pe teamă a unor evenimente suprapuse.',
'Citește pasajele corespunzătoare din ediția integrală',
'Introducere: puterea ascunsă',
'Capitolul întâi: Illuminati istorici și teoriile moderne',
'Capitolul al doilea: controlul de urgență și supravegherea',
'Capitolul al treilea: media și cultura populară',
'Concluzie',
'Bibliografie'
]
assert len(t)==len(d['segments'])
for s,v in zip(d['segments'],t):s['translation']=v
p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
