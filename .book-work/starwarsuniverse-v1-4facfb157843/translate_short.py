import json
from pathlib import Path

root = Path(__file__).parent / 'translations/ro/short/chunks'
translations = {
    't000001': 'Universul Star Wars — Ediția de zece minute',
    't000002': 'Universul Star Wars',
    't000003': 'Universul Star Wars cercetează o saga spațială cunoscută prin câteva întrebări legate între ele: ce înseamnă Forța, cum împart galaxia societăți diferite, cum schimbă tehnologia puterea și de ce povestea a rămas vie. Cartea pornește de la familia Skywalker și trece prin știința imaginară, filosofie, organizare socială și influența culturală a filmelor. Îi invită pe cititori să privească dincolo de spectacol, păstrând totodată limpede deosebirea dintre o lume fictivă și afirmațiile despre lumea noastră.',
    't000004': 'O galaxie ținută laolaltă de povești',
    't000005': 'Introducerea prezintă povestea familiei Skywalker și o galaxie de specii, instituții și conflicte. Loialitățile de familie și alegerile politice dau poveștii greutatea ei emoțională. Planetele și culturile sale deschid întrebări mai largi despre apartenență, alegere morală și folosirea puterii. Autorul tratează aceste elemente ca pe un limbaj imaginar comun, nu ca pe o dovadă că o singură interpretare ar fi definitivă.',
    't000006': 'Citește integral secțiunea 1',
    't000007': 'Forța ca întrebare',
    't000008': 'Primul capitol imaginează cum ar reacționa oamenii de astăzi dacă s-ar descoperi ceva asemănător Forței sau midiclorienilor. Oamenii de știință ar putea căuta o măsurătoare; instituțiile ar putea căuta controlul; oamenii obișnuiți s-ar putea întreba ce spune o asemenea descoperire despre sens și libertate. Sunt întrebări speculative în cadrul experimentului de gândire al cărții. Valoarea lor stă în faptul că arată cum o nouă capacitate poate deveni o problemă etică înainte ca oamenii să se înțeleagă asupra rostului ei.',
    't000009': 'Citește integral secțiunea 2',
    't000010': 'Filosofie și cumpătare',
    't000011': 'Al doilea capitol examinează latura luminoasă și latura întunecată ale Forței, codul Jedi, profeția și primejdia puterii fără limite. El compară ideile ficționale cu teme din mai multe tradiții filosofice reale. Disciplina unui Jedi îi poate ocroti pe ceilalți, dar certitudinea unei profeții poate îngusta judecata. Alegerile lui Anakin arată cum teama și dorința de control pot submina intențiile bune. Capitolul invită la comparații fără să reducă saga la o singură morală.',
    't000012': 'Citește integral secțiunea 3',
    't000013': 'Societatea de la o lume la alta',
    't000014': 'Al treilea capitol privește diferențele culturale, clasele sociale, guvernarea și reprezentarea. Speciile extraterestre și comunitățile umane au obiceiuri și istorii distincte. Bogăția de pe Coruscant și lumile periferice aflate în dificultate formează o economie politică inegală, iar prăbușirea Republicii arată cum instituțiile pot fi slăbite din interior. Cartea analizează și rolurile femeilor, precum și stereotipurile care reapar. Întrebarea ei largă este cum pot oamenii cu resurse inegale să construiască totuși o lume politică comună.',
    't000015': 'Citește integral secțiunea 4',
    't000016': 'Știința imaginară și limitele ei',
    't000017': 'Capitolul despre tehnologie trece în revistă hipermotorul, săbiile laser, droizii, protezele, orașele care acoperă planete întregi și Steaua Morții. Unele dispozitive amintesc de întrebări reale ale ingineriei; altele țin deschis de fantezie. Deosebirea contează, fiindcă în poveste tehnologia nu este niciodată neutră. Poate susține viața, vindeca și conecta, sau poate concentra violența și controlul. Coruscant ridică întrebări despre limitele ecologice, iar mâna protetică a lui Luke și armura lui Darth Vader complică granița dintre om și mașină.',
    't000018': 'Citește integral secțiunea 5',
    't000019': 'Momentele de cotitură ale sagăi',
    't000020': 'Capitolul despre intrigă străbate trilogiile originală, prequel și sequel. Drumul lui Luke, căderea lui Anakin, transformarea Republicii, căutarea identității de către Rey și revoltele succesive dau formă narativă temelor cărții. În loc să trateze fiecare eveniment ca pe o aventură izolată, autorul urmărește tiparele moștenirii, loialității și rezistenței. Lupta repetată împotriva puterii concentrate leagă personaje despărțite de generații.',
    't000021': 'Citește integral secțiunea 6',
    't000022': 'De ce povestea rămâne prezentă',
    't000023': 'Ultimul capitol și concluzia privesc Star Wars ca fenomen cultural. Efectele vizuale, creativitatea fanilor și întrebările recurente despre eroism au influențat poveștile de mai târziu. Răspândirea sagăi invită și la criticarea formulelor și a reprezentărilor familiare. Cea mai puternică invitație a cărții este să revizităm o scenă cunoscută cu o întrebare mai precisă: ce alegere are de făcut un personaj și ce îi permite ori îi îngreunează societatea din jur? Această întrebare deschide drumul spre capitolele integrale.',
    't000024': 'Citește integral secțiunea 7',
}
for path in sorted(root.glob('*.json')):
    data = json.loads(path.read_text())
    for segment in data['segments']:
        segment['translation'] = translations[segment['id']]
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')
