import json
from pathlib import Path

path = Path(__file__).parent / 'chunks/0006.json'
data = json.loads(path.read_text())
translations = [
    "Într-o noapte, pe când lucrează la ființă, îl lovește o înțelegere bruscă și puternică: nu poate merge mai departe. Cuprins de panică și dezgust, Victor sfâșie trupul pe jumătate terminat, distrugând toată munca depusă. Refuză să se mai joace de-a Dumnezeu. Dar, tocmai când aruncă rămășițele, simte pe cineva în apropiere. Este creatura, care îl urmărește din umbră.",
    "Creatura nu este deloc încântată, ca să spunem prea puțin. Avusese încredere că Victor își va ține promisiunea și îi va da șansa la tovărășie și pace. Acum, văzându-l distrugându-i posibila pereche, este mistuită de furie. Într-o confruntare înfiorătoare, jură să-l facă să plătească. «Voi fi cu tine în noaptea nunții», șuieră înainte de a dispărea în întuneric.",
    "Victor, aflat deja la marginea nebuniei, este împins și mai adânc în disperare. Știe că amenințarea creaturii este serioasă, iar gândul la ceea ce i-ar putea face lui sau, și mai rău, lui Elizabeth îi sporește teama. Hotărăște să părăsească imediat insula, lăsând în urmă laboratorul și toate urmele experimentului eșuat. Dar povara a ceea ce a făcut, sau mai curând nu a făcut, îl urmărește peste tot.",
    "Întors pe continent, Victor are mintea răvășită de vină, groază și regret. Se reîntâlnește cu Henry, dar lucrurile iau aproape imediat o întorsătură tragică. Fragilitatea lui psihică își spune cuvântul, se îmbolnăvește din nou și se prăbușește sub greutatea propriilor fapte. Henry, prieten loial ca întotdeauna, îl îngrijește iar până se însănătoșește, dar nici el nu îl poate salva pe Victor de ceea ce urmează.",
    "Într-o zi, pe când călătorește, Victor primește vestea devastatoare: Henry Clerval a fost găsit mort, ucis. Cea mai mare teamă a lui s-a adeverit. Creatura și-a împlinit promisiunea de a distruge tot ce îi este drag, iar acum unul dintre prietenii cei mai apropiați a plătit prețul. Ca și cum nu ar fi destul, Victor este acuzat de crimă. Este arestat și aruncat în închisoare, cu mintea și trupul împinse până la limită.",
    "Abia prin intervenția tatălui său, venit să-i dovedească nevinovăția, Victor este eliberat în cele din urmă. Dar acum nu mai este decât umbra omului de altădată. Obsesia, ambiția, refuzul de a-și asuma răspunderea: toate au adus moarte și distrugere. Iar cu amenințarea creaturii atârnând deasupra lui, știe că se apropie confruntarea finală.",
    "Întoarcerea lui Victor la Geneva este apăsătoare. Încearcă să pregătească nunta cu Elizabeth, dar promisiunea creaturii îi stăruie în minte. Știe că noaptea nunții va fi clipa adevărului și, deși încearcă să o ocrotească pe Elizabeth, în adâncul sufletului știe că nu poate opri ce va urma.",
    "La sfârșitul capitolului vedem un om mistuit de propria trufie și bântuit de urmările faptelor sale. Coborârea lui Victor în nebunie este aproape deplină, iar furia creaturii e departe de a se fi stins. Ceea ce a început ca o căutare a gloriei științifice s-a prefăcut într-un coșmar de moarte și disperare. Când actul final se apropie, e limpede că nici Victor, nici creatura nu vor ieși nevătămați.",
    "Rămâneți alături de noi pentru capitolul următor, în care povestea se grăbește spre deznodământul tragic. Va înfrunta Victor, în sfârșit, creatura abandonată? Sau promisiunea răzbunării va face totul să se prăbușească?",
    "Capitolul patru — Noaptea nunții și socoteala finală",
    "Pe când Victor Frankenstein revine la Geneva, presimțirea nenorocirii îl apasă ca un nor de furtună gata să se rupă. Promisiunea înfiorătoare a creaturii, «Voi fi cu tine în noaptea nunții», îi răsună în minte și umbrește ziua care ar trebui să fie cea mai fericită din viață. Dar, în stilul său obișnuit, Victor hotărăște să meargă înainte cu planurile de căsătorie cu Elizabeth, în ciuda amenințării. Nimic nu spune «nuntă perfectă» ca teama că un monstru ucigaș va apărea la petrecere.",
]
assert len(data['segments']) == len(translations)
for segment, translation in zip(data['segments'], translations):
    segment['translation'] = translation
path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')
