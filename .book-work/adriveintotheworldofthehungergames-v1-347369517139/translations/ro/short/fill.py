import json
from pathlib import Path

path = Path(__file__).parent / 'chunks/0001.json'
data = json.loads(path.read_text())
translations = [
    "O călătorie în lumea Jocurilor foamei — Lectură de zece minute",
    "O călătorie în lumea Jocurilor foamei",
    "Lectură de zece minute · 2024",
    "Panem și arena",
    "În Panem, lumea fictivă a lui Suzanne Collins, un Capitoliu bogat conduce districte sărace prin frică, lipsuri și un concurs anual televizat în care copiii trebuie să ucidă sau să fie uciși. Hotărârea lui Katniss Everdeen de a lua locul surorii sale transformă un gest privat de ocrotire într-o sfidare publică a sistemului. Eseul explorează politica, structura socială, tehnologia și locul durabil al poveștii în cultura populară. Întrebarea centrală este cum transformă un stat supraviețuirea în spectacol și cum învață oamenii să reziste.",
    "Citește introducerea integrală",
    "Un simbol cultural",
    "Cărțile și filmele au contribuit la reînnoirea interesului pentru ficțiunea distopică. Katniss a devenit o figură ușor de recunoscut a rezistenței reticente, iar Gaița Zeflemitoare, un simbol al speranței și revoltei. Eseul leagă această influență de discuțiile despre inegalitate, violență ca divertisment și capacitatea publicului de a recunoaște controlul chiar în timp ce îi urmărește spectacolul. Discuțiile fanilor și un prequel ulterior au menținut Panemul în atenție după trilogia inițială.",
    "Citește secțiunea integrală",
    "Putere, opresiune și sacrificiu",
    "Puterea Capitoliului se sprijină pe mai mult decât arme. Jocurile le amintesc districtelor de o rebeliune înfrântă, abat atenția spre competiție și fac fiecare comunitate să se teamă pentru copiii săi. Lipsurile slăbesc solidaritatea, în timp ce sacrificiul poate răsturna logica dominației. Katniss se oferă voluntară în locul lui Prim, iar alegerile ei în arenă fac vizibilă compasiunea acolo unde regulile cer brutalitate. Eseul citește supraviețuirea ca pe o problemă morală și fizică: la ce trebuie să renunțe un om și ce trebuie să refuze să cedeze?",
    "Citește secțiunea integrală",
    "Cum este construit Panemul",
    "Dezastrele de mediu, războiul și prăbușirea preced sistemul rigid al districtelor din Panem. Capitoliul păstrează bogăția și informația aproape de sine, atribuie districtelor roluri economice și le exploatează munca. Districtul 13 pierdut și secerișul anual întrețin o poveste publică despre rebeliune și pedeapsă. Lăsându-și istoria neclară, regimul limitează și ceea ce cetățenii își pot imagina că ar putea schimba. Eseul arată cum geografia, munca, foamea și memoria controlată susțin puterea politică.",
    "Citește secțiunea integrală",
    "Ce le cere spectacolul oamenilor",
    "Arena transformă suferința în divertisment pentru unii și în teroare obligatorie pentru alții. Tributurile sunt silite să-i trateze pe ceilalți copii drept dușmani, dar alianțele și gesturile de grijă dezvăluie posibilități dincolo de scenariul Capitoliului. Eseul întreabă cum schimbă frica supunerea, cum răspund comunitățile la lipsuri și cum poate supraviețui demnitatea într-un concurs construit artificial. Aceste întrebări leagă instituțiile fictive ale Panemului de preocupări mai largi despre constrângere, inegalitate și valoarea vieții omenești.",
    "Citește secțiunea integrală",
    "Instrumente de control și rezistență",
    "Tehnologia Capitoliului produce supravegherea arenei, spectacolul transmis public, intervențiile medicale și ființe proiectate numite mutații. Același acces inegal la puterea tehnică arată prăpastia dintre luxul Capitoliului și greutățile districtelor. În eseu, tehnologia nu are un singur sens moral: poate monitoriza și pedepsi, dar comunicarea și cunoștințele practice pot sprijini și rezistența. Întrebarea este cine îi conduce folosirea și cine îi plătește prețul.",
    "Citește secțiunea integrală",
    "Lumea din spatele concursului",
    "Panem face vizibil un concurs extrem, astfel încât sistemele mai tăcute de control devin mai ușor de văzut. Povestea lui Katniss leagă supraviețuirea de empatie și alegere morală, nu doar de victoria în arenă. Eseul îi invită pe cititori să examineze instituțiile din jurul Jocurilor și alegerile oamenilor din interiorul lor.",
    "Citește concluzia",
]
assert len(data['segments']) == len(translations)
for segment, translation in zip(data['segments'], translations):
    segment['translation'] = translation
path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')
