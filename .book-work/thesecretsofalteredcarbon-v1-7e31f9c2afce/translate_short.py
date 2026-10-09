import json
from pathlib import Path

root = Path(__file__).parent / 'translations/ro/short/chunks'
translations = {
    't000001': 'Secretele din Altered Carbon — Ediția de zece minute',
    't000002': 'Secretele din Altered Carbon',
    't000003': 'Acest ghid folosește Altered Carbon de Richard K. Morgan pentru a întreba ce se întâmplă când mintea unei persoane poate fi stocată și așezată într-un alt corp. Tehnologia promite vieți mai lungi, dar avantajele ei sunt împărțite inegal. Capitolele trec de la amenințările la adresa minților stocate la identitate, putere socială și alegerile morale ale lui Takeshi Kovacs. Întrebarea centrală este dacă eliberarea de moartea obișnuită schimbă și ceea ce oamenii își datorează unii altora.',
    't000004': 'O nouă vulnerabilitate',
    't000005': 'Introducerea explică stivele corticale și transferul unei conștiințe stocate într-un corp nou. Primul capitol examinează apoi virusul Rawling, o amenințare pentru mințile care există ca date. Când o copie de rezervă poate fi stricată, copiată sau furată, supraviețuirea depinde de sisteme pe care le pot controla alții. Amenințarea face nemurirea digitală mai puțin sigură decât pare la început și ridică întrebări despre intimitate, acces și dependență tehnologică.',
    't000006': 'Citește integral secțiunea 2',
    't000007': 'Viața dincolo de un singur corp',
    't000008': 'Capitolul al doilea ia în considerare cum schimbă conștiința stocată riscul, familia și timpul. O persoană poate supraviețui morții unui corp, dar nu poate presupune că orice înlocuitor este disponibil sau egal cu celelalte. Viețile îndelungate ar putea schimba obligațiile dintre generații și sensul amintirilor. Cartea tratează aceste posibilități ca trăsături ale lumii fictive a lui Morgan, nu ca pe o realizare științifică a prezentului.',
    't000009': 'Citește integral secțiunea 3',
    't000010': 'Cine rămâne aceeași persoană?',
    't000011': 'Al treilea capitol explorează separarea minții de corp. Dacă o conștiință poate fi mutată sau copiată, ce face ca cineva să rămână aceeași persoană? Un corp nou poate schimba felul în care răspund ceilalți, iar experiențele stocate s-ar putea să nu cuprindă fiecare parte a unei vieți. Ghidul folosește seria pentru a examina întrebări filosofice despre continuitate, proprietate și relația dintre memorie și experiența trupească.',
    't000012': 'Citește integral secțiunea 4',
    't000013': 'Identitatea ca fapt social',
    't000014': 'Capitolul al patrulea întreabă cum afectează schimbarea corpului cultura, familia și prejudecățile. Oamenii se pot muta între înfățișări, vârste și poziții sociale, dar inegalitatea poate dăinui prin accesul la corpuri mai bune. În jurul corpurilor apar noi forme de rușine sau statut. Capitolul arată că o tehnologie care face identitatea mai flexibilă nu face neapărat societatea mai primitoare.',
    't000015': 'Citește integral secțiunea 5',
    't000016': 'Puterea din spatele mașinilor',
    't000017': 'Al cincilea capitol trece în revistă tehnologiile științifico-fantastice care susțin această lume: stive, conștiință transmisă, spații virtuale, progrese medicale și artefacte extraterestre. Fiecare capacitate creează o nouă întrebare despre control. Cine poate repara sau înlocui un corp? Cine deține o minte stocată? Ghidul leagă posibilitatea tehnică de instituții și interese, fără să presupună că o invenție singură îi hotărăște folosirea.',
    't000018': 'Citește integral secțiunea 6',
    't000019': 'Meths și ceilalți',
    't000020': 'Capitolul al șaselea se concentrează asupra inegalității. Meths, cei foarte bogați, se pot reînnoi mereu, pot acumula putere și se pot feri de consecințe. Ceilalți se confruntă cu corpuri inferioare, muncă nesigură și amenințarea morții definitive. În Bay City, înălțimea clădirilor oglindește distanța dintre clasele sociale. Cartea întreabă dacă viața prelungită devine încă o resursă pe care averea o poate monopoliza.',
    't000021': 'Citește integral secțiunea 7',
    't000022': 'Etica după moartea obișnuită',
    't000023': 'Capitolul al șaptelea ia în considerare pedeapsa, consimțământul, autonomia și tratarea inteligenței artificiale într-o societate în care mințile pot fi stocate. Încarcerarea sau exploatarea poate dura mult mai mult când o persoană poate fi ținută ca date. Ghidul întreabă și dacă înlăturarea limitei comune a mortalității schimbă responsabilitatea morală. Întrebările lui trec dincolo de intrigă fără a pretinde că au răspunsuri simple.',
    't000024': 'Citește integral secțiunea 8',
    't000025': 'Kovacs și sistemul mai larg',
    't000026': 'Capitolul despre intrigă îl urmărește pe Kovacs după ce este pus într-un corp nou și angajat să cerceteze moartea lui Laurens Bancroft. Ancheta scoate la iveală corupția și puterea inegală a oamenilor care pot trăi secole întregi. Amintirile despre Envoys și Quellcrist Falconer îi modelează alegerile. Concluzia îi invită pe cititori să urmărească aceste alegeri în cartea integrală și apoi să se întrebe a cui libertate o apără de fapt tehnologia.',
    't000027': 'Citește integral secțiunea 9',
}
for path in sorted(root.glob('*.json')):
    data = json.loads(path.read_text())
    for segment in data['segments']:
        segment['translation'] = translations[segment['id']]
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')
