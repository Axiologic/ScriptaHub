import json
from pathlib import Path

p = Path(__file__).parent / 'chunks/0001.json'
d = json.loads(p.read_text())
t = [
    'Prețul libertății în Mizerabilii — Lectură de zece minute',
    'Prețul libertății în Mizerabilii',
    'Un parcurs de zece minute prin eseu',
    'Introducere: Libertatea are un preț',
    'Acest eseu citește romanul lui Victor Hugo',
    'Mizerabilii',
    'prin mai multe forme ale libertății: eliberarea din închisoare, ieșirea din sărăcie, emanciparea politică și desprinderea de un cod moral rigid. Întrebarea centrală este ce trebuie să sacrifice fiecare om pentru a căuta libertatea. Răspunsul diferă în poveștile lui Jean Valjean, Fantine, ale studenților de la baricadele Parisului și ale inspectorului Javert. Destinele lor leagă alegerile personale de legile și structurile sociale care modelează ceea ce oamenii pot deveni.',
    'Libertatea nu înseamnă în eseu doar înlăturarea constrângerilor. O identitate schimbată poate purta în continuare stigmatul social; iubirea poate cere să lași pe cineva să plece; acțiunea colectivă poate costa vieți fără să aducă imediat victoria. Personajele lui Hugo arată cum mila și sacrificiul pot deschide posibilități pe care pedeapsa și judecata le închid.',
    '1. Valjean: De la lanțuri la izbăvire',
    'Jean Valjean petrece 19 ani în închisoare după ce fură pâine pentru o familie înfometată. Pedeapsa dezvăluie o justiție lipsită de compasiune. Eliberarea nu îi aduce libertatea: eticheta de fost deținut îl împiedică să găsească lucru și adăpost. Episcopul Myriel îi oferă hrană și găzduire, apoi răspunde cu milă când Valjean fură argintăria. Le spune polițiștilor că i-a dăruit-o și adaugă sfeșnicele. Această iertare neașteptată zdruncină convingerea lui Valjean că societatea nu poate decât să îl condamne.',
    'Valjean își ia un nume nou, își clădește o viață respectată și devine primar. Inspectorul Javert îl urmărește, fiindcă legea continuă să îl definească prin trecut. Eseul întreabă dacă transformarea poate conta atunci când societatea refuză să o recunoască. Lupta lui Valjean pentru o identitate nouă este, așadar, fizică, morală și socială. Libertatea lui depinde de alegerea repetată a generozității sub umbra judecății.',
    'Citește capitolul integral despre Valjean',
    '2. Fantine: Prețul sărăciei',
    'Povestea lui Fantine inversează drumul lui Valjean spre izbăvire. Rămasă singură cu fiica ei, Cosette, ea o lasă în grija familiei Thénardier în timp ce caută de lucru. Aceștia o maltratează pe Cosette și cer bani pentru cheltuieli inventate. Când colegele află că Fantine are un copil în afara căsătoriei, își pierde slujba de la fabrică. Sărăcia și dubla măsură îi restrâng alegerile până când supraviețuirea o obligă să își vândă părul, dinții și, în cele din urmă, trupul.',
    'Fantine se sacrifică din iubire pentru Cosette, însă sacrificiile ei nu le pot apăra pe niciuna de o ordine socială crudă. Critica lui Hugo, așa cum o prezintă eseul, este că societatea poate condamna o femeie vulnerabilă pentru fapte disperate, refuzându-i totodată sprijinul care le-ar putea preveni. Valjean promite să aibă grijă de Cosette, dar Fantine moare înainte de a se putea desprinde de răul suferit. Soarta ei arată că rezistența individuală nu poate învinge singură orice sistem nedrept.',
    'Citește capitolul integral despre Fantine',
    '3. Baricadele și libertatea politică',
    'Marius Pontmercy, Enjolras, Grantaire și alți tineri revoluționari ridică baricade în Paris. Ei luptă pentru dreptate, egalitate și un viitor mai democratic, deși șansele le sunt potrivnice. Enjolras întruchipează idealismul tinereții; scepticismul lui Grantaire arată posibilitatea ca sacrificiul să fie zadarnic. Cu toate acestea, el li se alătură tovarășilor, transformând solidaritatea într-o alegere morală.',
    'Revolta este înăbușită și mulți studenți mor. Valjean ajunge la baricade mai ales pentru a-l salva pe Marius, tânărul iubit de fiica sa adoptivă, Cosette. Îl poartă pe Marius rănit prin canalele Parisului. Eseul așază salvarea personală lângă lupta colectivă: ambele caută eliberarea, dar numai una poate izbuti în acel moment. Moartea revoluționarilor nu produce imediat o schimbare politică. Idealurile lor îi pot totuși inspira pe cei de mai târziu, lăsând deschisă judecata asupra valorii și prețului revoltei.',
    'Citește capitolul integral despre revoluție',
    '4. Iubirea, mila și sacrificiul final',
    'Javert l-a urmărit pe Valjean, convins că infractorii nu se pot schimba. Când Valjean îi cruță viața, inspectorul nu poate împăca mila cu viziunea sa absolută despre lege. Moartea lui arată o altă formă de captivitate: o minte inflexibilă, incapabilă să trăiască în mijlocul complexității morale. Valjean scapă de urmărire, dar alege un sacrificiu mai tăcut. Îi mărturisește lui Marius trecutul său de condamnat și se retrage din viața lui Cosette, crezând că ea va fi mai fericită fără el.',
    'Valjean slăbește în izolare, până când Marius află ce a făcut și se întoarce împreună cu Cosette. Revederea lor aduce un sfârșit pașnic unei vieți marcate de judecată, iubire și altruism. Eseul prezintă mila, de la episcopul Myriel la Valjean, ca pe o forță care poate întrerupe ciclurile pedepsei. Întreabă și dacă retragerea lui era necesară sau reprezenta un alt preț impus de rușine.',
    'Citește capitolul integral despre ultimii ani ai lui Valjean',
    'Concluzie',
    'Izbăvirea lui Valjean, sărăcia lui Fantine, revolta eșuată și prăbușirea lui Javert dau libertății prețuri diferite. Eseul susține că mila contează la fel de mult ca legea, deoarece regulile singure pot păstra condițiile care îi închid pe oameni. Povestea lui Hugo le cere cititorilor să vadă omul dincolo de etichete și să cântărească sacrificiul personal față de schimbarea socială pe care o poate face posibilă.',
    'Citește eseul integral',
]
assert len(t) == len(d['segments'])
for seg, tr in zip(d['segments'], t):
    seg['translation'] = tr
p.write_text(json.dumps(d, ensure_ascii=False, indent=2) + '\n')
