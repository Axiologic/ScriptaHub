import json
from pathlib import Path

w = Path(__file__).parent
p = w / 'book/manifest.json'
m = json.loads(p.read_text())
m['title'] = {
    'en': 'A Glimpse into Frank Herbert’s Dune',
    'fr': 'Un aperçu de Dune de Frank Herbert',
    'de': 'Ein Einblick in Frank Herberts Dune',
    'es': 'Una mirada a Dune de Frank Herbert',
    'pt': 'Um olhar sobre Dune de Frank Herbert',
    'it': 'Uno sguardo a Dune di Frank Herbert',
    'ro': 'O privire asupra universului Dune al lui Frank Herbert',
    'pl': 'Spojrzenie na Diunę Franka Herberta',
}
m['subtitle'] = {
    'en': 'Power, ecology, religion, and technology across the Dune saga',
    'fr': 'Pouvoir, écologie, religion et technologie dans la saga Dune',
    'de': 'Macht, Ökologie, Religion und Technik in der Dune-Saga',
    'es': 'Poder, ecología, religión y tecnología en la saga Dune',
    'pt': 'Poder, ecologia, religião e tecnologia na saga Dune',
    'it': 'Potere, ecologia, religione e tecnologia nella saga Dune',
    'ro': 'Putere, ecologie, religie și tehnologie în saga Dune',
    'pl': 'Władza, ekologia, religia i technologia w sadze Diuna',
}
s = {
    'en': [
        'Arrakis alone supplies the spice that sustains interstellar travel.',
        'Paul’s prescience challenges freedom, leadership, and moral responsibility.',
        'Fremen customs show a culture shaped by scarce water.',
        'Bene Gesserit plans connect faith, breeding, and political power.',
        'Guild navigation and Mentats reveal technology without thinking machines.',
        'The essay follows six original novels and their wider legacy.',
    ],
    'fr': [
        'Arrakis fournit seule l’épice indispensable aux voyages interstellaires.',
        'La prescience de Paul interroge liberté, pouvoir et responsabilité morale.',
        'Les coutumes fremen montrent une culture façonnée par la rareté de l’eau.',
        'Les projets Bene Gesserit lient foi, sélection génétique et pouvoir politique.',
        'Navigateurs et Mentats révèlent une technologie sans machines pensantes.',
        'L’essai suit les six romans originaux et leur vaste héritage.',
    ],
    'de': [
        'Nur Arrakis liefert das Gewürz für interstellare Reisen.',
        'Pauls Vorherwissen stellt Freiheit, Führung und moralische Verantwortung infrage.',
        'Die Bräuche der Fremen zeigen eine vom Wassermangel geprägte Kultur.',
        'Bene-Gesserit-Pläne verbinden Glauben, Zuchtprogramm und politische Macht.',
        'Navigatoren und Mentaten zeigen Technik ohne denkende Maschinen.',
        'Der Essay betrachtet sechs Originalromane und ihr weitreichendes Erbe.',
    ],
    'es': [
        'Solo Arrakis produce la especia que sostiene los viajes interestelares.',
        'La presciencia de Paul cuestiona libertad, liderazgo y responsabilidad moral.',
        'Las costumbres fremen muestran una cultura moldeada por la escasez de agua.',
        'Los planes Bene Gesserit relacionan fe, selección genética y poder político.',
        'Navegantes y Mentats revelan tecnología sin máquinas pensantes.',
        'El ensayo recorre las seis novelas originales y su amplio legado.',
    ],
    'pt': [
        'Só Arrakis produz a especiaria necessária às viagens interestelares.',
        'A presciência de Paul questiona liberdade, liderança e responsabilidade moral.',
        'Os costumes fremen mostram uma cultura moldada pela escassez de água.',
        'Os planos Bene Gesserit ligam fé, seleção genética e poder político.',
        'Navegadores e Mentats revelam tecnologia sem máquinas pensantes.',
        'O ensaio percorre os seis romances originais e o seu legado.',
    ],
    'it': [
        'Solo Arrakis produce la spezia necessaria ai viaggi interstellari.',
        'La preveggenza di Paul interroga libertà, guida e responsabilità morale.',
        'Le usanze Fremen mostrano una cultura plasmata dalla scarsità d’acqua.',
        'I piani Bene Gesserit legano fede, selezione genetica e potere politico.',
        'Navigatori e Mentat mostrano una tecnologia senza macchine pensanti.',
        'Il saggio segue i sei romanzi originali e la loro eredità.',
    ],
    'ro': [
        'Numai Arrakis produce mirodenia necesară călătoriilor interstelare.',
        'Precogniția lui Paul pune în discuție libertatea, conducerea și răspunderea morală.',
        'Obiceiurile Fremenilor arată o cultură modelată de lipsa apei.',
        'Planurile Bene Gesserit leagă credința, selecția genetică și puterea politică.',
        'Navigatorii și Mentații dezvăluie o tehnologie fără mașini gânditoare.',
        'Eseul urmărește cele șase romane originale și influența lor.',
    ],
    'pl': [
        'Tylko Arrakis dostarcza przyprawę potrzebną do podróży międzygwiezdnych.',
        'Przewidywanie Paula stawia pytania o wolność, władzę i odpowiedzialność moralną.',
        'Zwyczaje Fremenów pokazują kulturę ukształtowaną przez brak wody.',
        'Plany Bene Gesserit łączą wiarę, dobór genetyczny i władzę polityczną.',
        'Nawigatorzy i Mentaci ukazują technologię bez myślących maszyn.',
        'Esej omawia sześć oryginalnych powieści i ich dziedzictwo.',
    ],
}
m['shortDescription'] = {lang: ' '.join(lines) for lang, lines in s.items()}
m['aboutBook'] = {
    'en': [
        'This essay introduces Frank Herbert’s Dune universe through Arrakis and its spice economy, then examines free will, power, ecological adaptation and religious myth-making. It explains how Paul Atreides, the Fremen and the Bene Gesserit connect these themes.',
        'Further chapters examine the ban on thinking machines, Mentats, Guild navigation, Great Houses and CHOAM. The essay follows the six original novels, later continuations and Dune’s influence on literature, film and environmental thought.',
    ],
    'fr': [
        'Cet essai présente l’univers de Dune à travers Arrakis et l’économie de l’épice, puis examine libre arbitre, pouvoir, adaptation écologique et construction religieuse. Paul Atréides, les Fremen et les Bene Gesserit relient ces thèmes.',
        'Les chapitres suivants étudient l’interdit des machines pensantes, les Mentats, les Navigateurs, les Grandes Maisons et CHOAM. L’essai suit six romans originaux, les continuations et l’influence de Dune sur littérature, cinéma et pensée écologique.',
    ],
    'de': [
        'Dieser Essay führt über Arrakis und die Gewürzwirtschaft in Frank Herberts Dune-Welt ein. Er untersucht freien Willen, Macht, ökologische Anpassung und religiöse Mythen anhand von Paul Atreides, den Fremen und Bene Gesserit.',
        'Weitere Kapitel behandeln das Verbot denkender Maschinen, Mentaten, Gildennavigation, Große Häuser und CHOAM. Der Essay verfolgt sechs Originalromane, spätere Fortsetzungen und Dunes Einfluss auf Literatur, Film und Umweltdenken.',
    ],
    'es': [
        'Este ensayo presenta el universo Dune mediante Arrakis y la economía de la especia. Examina libre albedrío, poder, adaptación ecológica y creación de mitos religiosos a través de Paul Atreides, los fremen y Bene Gesserit.',
        'Otros capítulos tratan la prohibición de máquinas pensantes, Mentats, Navegantes, Grandes Casas y CHOAM. El ensayo recorre las seis novelas originales, las continuaciones y la influencia de Dune en literatura, cine y pensamiento ambiental.',
    ],
    'pt': [
        'Este ensaio apresenta o universo Dune através de Arrakis e da economia da especiaria. Examina livre-arbítrio, poder, adaptação ecológica e mitos religiosos com Paul Atreides, os Fremen e Bene Gesserit.',
        'Outros capítulos abordam a proibição de máquinas pensantes, Mentats, Navegadores, Grandes Casas e CHOAM. O ensaio acompanha os seis romances originais, as continuações e a influência de Dune na literatura, cinema e pensamento ambiental.',
    ],
    'it': [
        'Questo saggio presenta l’universo Dune attraverso Arrakis e l’economia della spezia. Esamina libero arbitrio, potere, adattamento ecologico e miti religiosi con Paul Atreides, i Fremen e Bene Gesserit.',
        'Altri capitoli trattano il divieto delle macchine pensanti, Mentat, Navigatori, Grandi Case e CHOAM. Il saggio segue i sei romanzi originali, le continuazioni e l’influenza di Dune su letteratura, cinema e pensiero ambientale.',
    ],
    'ro': [
        'Eseul prezintă universul Dune prin Arrakis și economia mirodeniei, apoi examinează liberul arbitru, puterea, adaptarea ecologică și construirea miturilor religioase. Paul Atreides, Fremenii și Bene Gesserit leagă aceste teme.',
        'Alte capitole discută interdicția mașinilor gânditoare, Mentații, navigația Ghildei, Marile Case și CHOAM. Eseul urmărește cele șase romane originale, continuările ulterioare și influența Dune asupra literaturii, filmului și gândirii ecologice din lumea contemporană.',
    ],
    'pl': [
        'Esej przedstawia świat Diuny przez Arrakis i gospodarkę przyprawy, a następnie bada wolną wolę, władzę, adaptację ekologiczną i religijne mity. Paul Atryda, Fremeni i Bene Gesserit łączą te tematy.',
        'Kolejne rozdziały omawiają zakaz myślących maszyn, Mentatów, Nawigatorów, Wielkie Rody i CHOAM. Esej śledzi sześć oryginalnych powieści, późniejsze kontynuacje oraz trwały wpływ Diuny na literaturę, kino i współczesną myśl ekologiczną na świecie.',
    ],
}
rpath = w / 'release.json'
r = json.loads(rpath.read_text())
m['shortDescriptionEditorial'] = {'method': 'active-LLM-authored', 'sourceSha256': r['sha256'], 'sentencesPerLanguage': 6, 'status': 'reviewed-intake'}
m.pop('metadataDraft', None)
p.write_text(json.dumps(m, ensure_ascii=False, indent=2) + '\n')
r['changes'] = {
    'en': 'Cleaned source essay with complete and ten-minute English and Romanian readers, a new English PDF, cover and reviewed discovery metadata.',
    'ro': 'Eseu sursă curățat, cu lecturi integrale și de zece minute în engleză și română, PDF nou în engleză, copertă și metadate revizuite.',
}
rpath.write_text(json.dumps(r, ensure_ascii=False, indent=2) + '\n')
