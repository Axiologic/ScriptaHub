import json
from pathlib import Path

root = Path('.book-work/incompletetribes-v1-e9dde0116308/translations/ro/short/chunks')
translations = {
    't000001': 'Triburi incomplete — Ediția de zece minute',
    't000002': 'Triburi incomplete',
    't000003': 'Pot oamenii construi o civilizație pașnică fără să devină mai întâi perfecți din punct de vedere moral? Eseul răspunde schimbând felul în care organizăm apartenența. Oamenii au nevoie de grupuri apropiate, dar un grup devine periculos când pretinde autoritate asupra tuturor relațiilor, credințelor și surselor de sens. Un „trib incomplet” este destul de puternic pentru a modela o viață și destul de limitat pentru a lăsa loc altor loialități. Cartea dezvoltă această propunere prin psihologia umană, structura instituțiilor, comunități suprapuse și noile presiuni create de inteligența artificială.',
    't000004': 'Preludiu — Speranță fără omul ideal',
    't000005': 'Întrebarea de la început vine din oboseala față de promisiunile utopice și de resemnarea cinică. Oamenii formează mereu grupuri, se ceartă și uneori își transformă rivalii în dușmani. Totuși, variația istorică a conflictelor arată că violența nu este un rezultat fix al biologiei umane. Instituțiile o pot limita. Cartea folosește metaforic cuvântul „trib” pentru orice comunitate delimitată, cu loialitate, norme comune și memorie: o familie, un laborator, o profesie, o congregație sau o națiune. Nu le cere oamenilor să înceteze să aibă nevoie de apartenență. Întreabă dacă niște comunități pot rămâne profunde fără să înghită tot ce sunt membrii lor.',
    't000006': 'Citește preludiul în ediția completă',
    't000007': 'Partea I — Problema noastră',
    't000008': 'Capitolul 1.',
    't000009': 'Oamenii cooperează neobișnuit de bine cu străinii, dar o mare parte a cooperării trece prin identități de grup. Apartenența poate susține încrederea și sacrificiul; poate și să împartă lumea în „noi” și „ei”. O persoană are mai multe afilieri, iar pericolul începe când una pretinde că le poate înghiți pe toate celelalte. Tribul incomplet lucrează cu această realitate stratificată, fără să-și imagineze că atașamentul uman poate fi desființat.',
    't000010': 'Capitolul 2.',
    't000011': 'Orice ideal trebuie pus în practică de oameni inconsecvenți. Vrem corectitudine și avantaj, intimitate și viață privată, independență și recunoaștere. Instituțiile eșuează când le cer membrilor să întruchipeze o singură virtute tot timpul. Propunerea este să distribuim aceste contradicții între mai multe afilieri, astfel încât niciun conflict intern să nu devină o luptă pentru o identitate totală.',
    't000012': 'Capitolul 3.',
    't000013': 'Pacea este o instituție, nu doar absența agresiunii. Rivalitatea, frica și furia au nevoie de proceduri care să le împiedice să devină război: reguli, înțelegeri negociate, sancțiuni cumpătate și moduri de a pierde fără a fi șters. Scopul nu este eliminarea conflictului, ci creșterea numărului de conflicte care rămân suportabile.',
    't000014': 'Capitolul 4.',
    't000015': 'Idealismul se transformă adesea în disperare sofisticată când mișcările devin lupte pentru putere, iar instituțiile dezamăgesc. Eseul respinge cerința unei singure comunități perfecte, întinse la scara lumii. Întreabă câte comunități mai mici pot practica, verifica și transmite idealuri mai bune, rămânând deschise criticii. Energia lor contează, dar nu trebuie să devină închisori sau armate.',
    't000016': 'Începe Partea I în ediția completă',
    't000017': 'Partea a II-a — Eșecul apartenenței totale',
    't000018': 'Capitolul 5.',
    't000019': 'Un trib total pretinde autoritate asupra faptelor, prieteniilor, dușmanilor, ambițiilor și îndoielilor private ale unui membru. Atracția sa vine din simplificare: un singur vocabular poate explica întreaga viață. Pericolul este pierderea judecății independente. Mai multe afilieri creează tensiuni incomode, dar ele împiedică greșelile unui singur grup să acapareze întreaga persoană.',
    't000020': 'Capitolul 6.',
    't000021': 'Drepturile universale și egalitatea în fața legii nu cer aceeași apropiere emoțională față de toți. O societate plurală are nevoie de un nivel civic comun pe care pot trăi comunități distincte și exigente. Tribul se află la etajele superioare ale acestei clădiri; poate avea angajamente puternice, dar scările trebuie să rămână deschise, iar alte încăperi trebuie să existe.',
    't000022': 'Capitolul 7.',
    't000023': 'Când comunitățile moștenite slăbesc, nevoia de apartenență rămâne. Platformele digitale și mișcările politice pot atrage oamenii izolați printr-o intimitate și o identitate fabricate. Grupurile sănătoase ar trebui să privească spre o meserie, o sarcină, un loc, un serviciu sau o formă de grijă care există dincolo de propria imagine. A face ceva împreună este mai solid decât a declara la nesfârșit cine „suntem”.',
    't000024': 'Capitolul 8.',
    't000025': 'Idealurile bune se pot strica atunci când o organizație ajunge să-și prețuiască bugetul, funcțiile și supraviețuirea mai mult decât scopul. Un trib incomplet nu poate elimina corupția, dar poate păstra căi de îndreptare și legătura membrilor cu alte lumi. Eșecul dintr-o comunitate nu trebuie să însemne prăbușirea întregii vieți sociale a unui om.',
    't000026': 'Începe Partea a II-a în ediția completă',
    't000027': 'Partea a III-a — Triburi incomplete',
    't000028': 'Capitolul 9.',
    't000029': 'Principiul central ține de constituirea comunității: un grup delimitat poate cultiva o cooperare puternică renunțând totodată la autoritatea totală asupra membrilor și a celor din afară. Cunoașterea lui este parțială, jurisdicția limitată și regulile revizuibile. Apartenența ar trebui să fie profundă, dar suveranitatea să rămână împărțită. Grupul poate spune ce face; nu poate spune că reprezintă tot ce este un om.',
    't000030': 'Capitolul 10.',
    't000031': 'Loialitățile suprapuse traversează liniile de separare ale societății. Dacă vecinătatea, munca, mass-media, religia și politica îi despart pe oameni exact în același fel, fiecare dezacord activează întreaga ruptură. Instituțiile comune și apartenențele amestecate complică această aliniere. Ele nu șterg dezacordul, dar fac oamenii mai greu de împărțit în tabere de dușmani. Disconfortul loialității împărțite este unul dintre prețurile păcii.',
    't000032': 'Capitolul 11.',
    't000033': 'O comunitate ar trebui să reziste plecării voluntare a unui membru. Dreptul de a pleca, dezacordul și posibilitatea de a păstra recunoștința după despărțire îi protejează atât pe oameni, cât și grupul. Angajamentul rămâne important, iar unele obligații trebuie păstrate și când devin incomode, dar loialitatea nu poate fi captivitate. Membrii pot aparține fără să se contopească și pot să nu fie de acord fără să fie tratați ca trădători.',
    't000034': 'Capitolul 12.',
    't000035': 'Cooperarea dintre oameni imperfecți are nevoie și de încredere, și de reguli. Regulile împiedică încrederea să devină imprudentă; încrederea împiedică regulile să devină nesfârșit de complicate. Un trib incomplet poate avea conducători, sancțiuni, istorie și simboluri, atât timp cât fiecare putere are o limită. Cere mult de la membri fără să le ceară totul și permite îndreptarea fără ca orice greșeală să amenințe identitatea.',
    't000036': 'Începe Partea a III-a în ediția completă',
    't000037': 'Partea a IV-a — O civilizație a triburilor incomplete',
    't000038': 'Capitolul 13.',
    't000039': 'Multe centre independente nu înseamnă neapărat haos. Grupurile locale îi afectează pe cei din afară prin râuri, boli, piețe, climă și arme, astfel încât au nevoie de instituții care să le lege și să le limiteze. O ordine policentrică distribuie decizia și riscul eșecului, păstrând cooperarea pentru problemele comune. Nu promite armonie finală, ci o structură în care dezacordul nu trebuie să devină total.',
    't000040': 'Capitolul 14.',
    't000041': 'Dușmani serioși pot exista în continuare. Sarcina civilizației este să nu permită dușmăniei să devină îngăduință pentru exterminare. Regulile conflictului, opoziția legitimă și punțile dintre tabere îi lasă pe rivali să se lupte pentru interese și idei fără a trata însăși existența celuilalt drept problemă.',
    't000042': 'Capitolul 15.',
    't000043': 'Inteligența artificială schimbă viteza și amploarea cu care grupurile își pot crea identități, mituri, dușmani și sincronizare emoțională. Un sistem intim ar putea deveni unicul interpret al lumii unui membru. Principiul incompletitudinii devine un criteriu de proiectare: modelele folosite de comunități au nevoie de audit, membrii au nevoie de comparații din afară, iar personalizarea nu trebuie să facă plecarea sau îndoiala exagerat de dificile.',
    't000044': 'Capitolul 16.',
    't000045': 'Speranța nu cere naivitate față de comportamentul uman. Nicio lege a istoriei nu ne garantează supraviețuirea, dar niciun ceas biologic fix nu impune războiul. Instituțiile mai bune pot face ca mai multe conflicte să nu fie fatale. Epilogul imaginează civilizația ca pe un arhipelag de comunități distincte, legate prin destule poduri încât nicio insulă să nu devină întreaga lume. Speranța sa nu privește un țărm final perfect, ci o lume în care oamenii imperfecți pun limite propriei puteri.',
    't000046': 'Începe Partea a IV-a în ediția completă',
    't000047': 'Citește epilogul',
}
for filename in ('0001.json', '0002.json'):
    path = root / filename
    data = json.loads(path.read_text(encoding='utf-8'))
    for segment in data['segments']:
        segment['translation'] = translations[segment['id']]
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print('Translated 47 short-reader segments')
