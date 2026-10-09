import json
from pathlib import Path

t = {
't000093': 'Teoria evoluției a devenit parte integrantă a medicinei moderne, influențând felul în care înțelegem bolile și abordăm tratamentul.',
't000094': 'Înțelegerea evoluției bacteriilor a fost esențială în confruntarea cu rezistența la antibiotice. Modelele evolutive le permit cercetătorilor să anticipeze cum ar putea bacteriile dezvolta rezistență, oferind informații esențiale pentru strategiile de combatere a acestei amenințări la adresa sănătății mondiale.',
't000095': 'În cercetarea cancerului, boala este privită din ce în ce mai des ca un proces evolutiv desfășurat la nivel celular. Această perspectivă a dus la abordări inovatoare ale tratamentului, precum terapia adaptivă, care urmărește gestionarea tumorilor, nu eradicarea lor completă.',
't000096': 'Principiile evolutive au un rol important și în dezvoltarea vaccinurilor, mai ales pentru agenții patogeni care evoluează rapid, precum virusul gripal. Studiind evoluția virusurilor, cercetătorii pot anticipa ce tulpini ar putea deveni dominante, orientând compoziția vaccinurilor antigripale anuale.',
't000097': 'În medicina personalizată, biologia evolutivă contribuie la farmacogenomică, studiul felului în care variațiile genetice influențează răspunsul individual la medicamente. Aceste cunoștințe permit dezvoltarea unor tratamente medicale mai personalizate și mai eficiente.',
't000098': 'Ideile lui Darwin au inspirat tehnici computaționale care imită procesele evolutive pentru a rezolva probleme complexe.',
't000099': 'Algoritmii genetici sunt algoritmi de căutare inspirați de mecanismele selecției naturale și ale geneticii. Ei sunt folosiți pe scară largă pentru a găsi soluții de bună calitate la probleme de optimizare și căutare din domenii precum ingineria, economia și robotica.',
't000100': 'Domeniul mai larg al calculului evolutiv cuprinde mai multe tehnici de rezolvare a problemelor derivate din evoluția biologică. Printre ele se numără programarea genetică, strategiile evolutive și neuroevoluția, care implică evoluția rețelelor neuronale artificiale.',
't000101': 'În domeniul interdisciplinar al vieții artificiale, cercetătorii studiază viața și procesele asemănătoare ei prin simulări pe calculator, robotică și biochimie. Acest domeniu se bazează în mare măsură pe principii evolutive pentru a înțelege proprietățile fundamentale ale sistemelor vii.',
't000102': 'Inteligența de roi este inspirată de comportamentul colectiv al insectelor sociale și al altor societăți animale. Algoritmii bazați pe ea sunt aplicați în optimizare, robotică și inteligență artificială.',
't000103': 'Teoria evoluției a avut un rol crucial în dezvoltarea unor noi domenii interdisciplinare aflate la întâlnirea biologiei, informaticii și ingineriei.',
't000104': 'Bioinformatica aplică tehnici computaționale pentru analiza datelor biologice, în special a informațiilor genetice și genomice. Modelele evolutive au un rol crucial în bioinformatică, ajutând la alinierea secvențelor, construirea arborilor filogenetici și predicția structurii și funcției proteinelor.',
't000105': 'În biologia sintetică, obiectivul este proiectarea și construirea unor noi componente, dispozitive și sisteme biologice sau reproiectarea unor sisteme existente pentru scopuri practice. Principiile evolutive sunt esențiale în proiectarea sistemelor biologice sintetice și dezvoltarea protocoalelor de evoluție dirijată a biomoleculelor. Biologia sistemelor urmărește să înțeleagă sistemele biologice prin modelarea interacțiunilor lor complexe. Teoria evoluției oferă un cadru esențial pentru a înțelege cum s-au format și au evoluat aceste sisteme de-a lungul timpului.',
't000106': 'Biologia computațională, un domeniu larg ce folosește calculul în biologie, se bazează în mare măsură pe teoria evoluției în numeroase aplicații. Printre acestea se numără modelarea dinamicii populațiilor, predicția plierii proteinelor și studiul evoluției rețelelor de reglare genetică.',
't000107': 'În concluzie, teoria evoluției formulată de Darwin a avut un impact profund și extins asupra tehnologiei și științelor aplicate. De la agricultură la medicină și de la inteligență artificială la biologie sintetică, conceptele evolutive s-au dovedit instrumente puternice pentru înțelegerea sistemelor complexe și dezvoltarea unor soluții inovatoare la probleme dificile. Pe măsură ce tehnologia avansează, influența ideilor lui Darwin ar putea crește și mai mult, continuând să modeleze abordarea unora dintre cele mai presante provocări tehnologice și științifice ale vremii noastre.',
't000108': 'Concluzie',
't000109': 'Abordarea cercetării științifice de către Darwin — caracterizată prin observație atentă, gândire interdisciplinară și testarea riguroasă a ipotezelor — continuă să le servească drept model cercetătorilor din diferite domenii. Disponibilitatea lui de a înfrunta implicațiile filosofice și religioase ale teoriei sale arată legătura profundă dintre descoperirea științifică și gândirea umană în sens mai larg.',
't000110': 'Deși ideile lui Darwin au întâmpinat contestări și controverse, mai ales în sfera înțelegerii și acceptării lor publice, ele au rezistat în timp. Genomica modernă, biologia dezvoltării și alte domenii avansate au întărit și rafinat teoria evoluției, demonstrându-i puterea explicativă.',
't000111': 'Astăzi, când ne confruntăm cu provocări mondiale precum schimbările climatice, pierderea biodiversității și bolile emergente, observațiile lui Darwin despre interdependența vieții și puterea schimbării graduale rămân mai relevante ca oricând. Gândirea evolutivă oferă perspective și instrumente valoroase pentru abordarea acestor probleme complexe.',
't000112': 'În concluzie, moștenirea lui Charles Darwin nu este doar istorică. Ideile sale revoluționare continuă să modeleze înțelegerea lumii, să influențeze progresele științifice și tehnologice și să ne orienteze abordarea provocărilor contemporane. Pe măsură ce înaintăm în secolul XXI, relevanța durabilă a operei lui Darwin mărturisește puterea transformatoare a cercetării științifice și dialogul continuu dintre cunoașterea umană și lumea naturală.',
't000113': 'Bibliografie',
}

base = Path(__file__).parent / 'translations/ro/full/chunks'
for name in ('0009', '0010'):
    path = base / f'{name}.json'
    data = json.loads(path.read_text(encoding='utf-8'))
    for segment in data['segments']:
        segment['translation'] = t.get(segment['id'], segment['source'])
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(name, len(data['segments']))
