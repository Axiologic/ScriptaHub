import json
from pathlib import Path

p = Path('tools/keyword-translations.generated.json')
c = json.loads(p.read_text())
langs = ('fr', 'de', 'es', 'pt', 'it', 'ro', 'pl')
fix = {
    'Arrakis': ('Arrakis', 'Arrakis', 'Arrakis', 'Arrakis', 'Arrakis', 'Arrakis', 'Arrakis'),
    'desert planet': ('planète désertique', 'Wüstenplanet', 'planeta desértico', 'planeta desértico', 'pianeta desertico', 'planetă deșertică', 'pustynna planeta'),
    'spice melange': ('épice mélange', 'Melange-Gewürz', 'especia melange', 'especiaria melange', 'spezia melange', 'mirodenia melanj', 'przyprawa melanż'),
    'spice': ('épice', 'Gewürz', 'especia', 'especiaria', 'spezia', 'mirodenie', 'przyprawa'),
    'Paul Atreides': ('Paul Atréides', 'Paul Atreides', 'Paul Atreides', 'Paul Atreides', 'Paul Atreides', 'Paul Atreides', 'Paul Atryda'),
    'prescience': ('prescience', 'Vorauswissen', 'presciencia', 'presciência', 'preveggenza', 'precogniție', 'prekognicja'),
    'possible futures': ('avenirs possibles', 'mögliche Zukünfte', 'futuros posibles', 'futuros possíveis', 'futuri possibili', 'viitoruri posibile', 'możliwe przyszłości'),
    'Golden Path': ('Sentier d’Or', 'Goldener Pfad', 'Senda Dorada', 'Caminho Dourado', 'Sentiero d’Oro', 'Calea de Aur', 'Złota Ścieżka'),
    'humanity’s survival': ('survie de l’humanité', 'Überleben der Menschheit', 'supervivencia de la humanidad', 'sobrevivência da humanidade', 'sopravvivenza dell’umanità', 'supraviețuirea omenirii', 'przetrwanie ludzkości'),
    'stillsuits': ('distilles', 'Destillanzüge', 'destiltrajes', 'trajes destiladores', 'tute distillanti', 'distilcostume', 'filtrfraki'),
    'desert’s ecology': ('écologie du désert', 'Ökologie der Wüste', 'ecología del desierto', 'ecologia do deserto', 'ecologia del deserto', 'ecologia deșertului', 'ekologia pustyni'),
    'sandworms': ('vers des sables', 'Sandwürmer', 'gusanos de arena', 'vermes da areia', 'vermi delle sabbie', 'viermi de nisip', 'czerwie pustyni'),
    'spice cycle': ('cycle de l’épice', 'Gewürzzyklus', 'ciclo de la especia', 'ciclo da especiaria', 'ciclo della spezia', 'ciclul mirodeniei', 'cykl przyprawy'),
    'demanding environment': ('milieu hostile', 'anspruchsvolle Umwelt', 'entorno exigente', 'ambiente hostil', 'ambiente ostile', 'mediu aspru', 'wymagające środowisko'),
    'Missionaria Protectiva': ('Missionaria Protectiva', 'Missionaria Protectiva', 'Missionaria Protectiva', 'Missionaria Protectiva', 'Missionaria Protectiva', 'Missionaria Protectiva', 'Missionaria Protectiva'),
    'Butlerian Jihad': ('Jihad Butlérien', 'Butlerianischer Dschihad', 'Yihad Butleriano', 'Jihad Butleriano', 'Jihad Butleriano', 'Jihadul Butlerian', 'Dżihad Butleriański'),
    'Mentats': ('Mentats', 'Mentaten', 'Mentats', 'Mentats', 'Mentat', 'Mentați', 'Mentaci'),
    'Guild Navigators': ('Navigateurs de la Guilde', 'Navigatoren der Gilde', 'Navegantes de la Cofradía', 'Navegadores da Guilda', 'Navigatori della Gilda', 'Navigatorii Ghildei', 'Nawigatorzy Gildii'),
    'spice-induced prescience': ('prescience induite par l’épice', 'durch Gewürz ausgelöstes Vorauswissen', 'presciencia inducida por la especia', 'presciência induzida pela especiaria', 'preveggenza indotta dalla spezia', 'precogniție indusă de mirodenie', 'prekognicja wywołana przyprawą'),
    'Tleilaxu': ('Tleilaxu', 'Tleilaxu', 'Tleilaxu', 'Tleilaxu', 'Tleilaxu', 'Tleilaxu', 'Tleilaxu'),
    'Great Houses': ('Grandes Maisons', 'Große Häuser', 'Grandes Casas', 'Grandes Casas', 'Grandi Case', 'Marile Case', 'Wielkie Rody'),
    'Padishah Emperor': ('Empereur Padishah', 'Padischah-Imperator', 'Emperador Padishah', 'Imperador Padishah', 'Imperatore Padishah', 'Împăratul Padișah', 'Imperator Padyszach'),
    'Spacing Guild': ('Guilde Spatiale', 'Raumgilde', 'Cofradía Espacial', 'Guilda Espacial', 'Gilda Spaziale', 'Ghilda Spațială', 'Gildia Kosmiczna'),
    'CHOAM': ('CHOAM', 'CHOAM', 'CHOAM', 'CHOAM', 'CHOAM', 'CHOAM', 'CHOAM'),
    'imperial influence': ('influence impériale', 'imperialer Einfluss', 'influencia imperial', 'influência imperial', 'influenza imperiale', 'influență imperială', 'wpływy imperialne'),
    'resource scarcity': ('pénurie de ressources', 'Ressourcenknappheit', 'escasez de recursos', 'escassez de recursos', 'scarsità di risorse', 'penurie de resurse', 'niedobór zasobów'),
    'series’ conflicts': ('conflits de la série', 'Konflikte der Reihe', 'conflictos de la saga', 'conflitos da saga', 'conflitti della saga', 'conflictele seriei', 'konflikty sagi'),
    'Paul’s ascent': ('ascension de Paul', 'Pauls Aufstieg', 'ascenso de Paul', 'ascensão de Paul', 'ascesa di Paul', 'ascensiunea lui Paul', 'awans Paula'),
    'Leto II’s long rule': ('long règne de Leto II', 'lange Herrschaft Letos II.', 'largo reinado de Leto II', 'longo reinado de Leto II', 'lungo regno di Leto II', 'lunga domnie a lui Leto al II-lea', 'długie panowanie Leto II'),
    'Scattering': ('Dispersion', 'Zerstreuung', 'Dispersión', 'Dispersão', 'Dispersione', 'Dispersie', 'Rozproszenie'),
    'invented terms': ('termes inventés', 'erfundene Begriffe', 'términos inventados', 'termos inventados', 'termini inventati', 'termeni inventați', 'wymyślone terminy'),
    'chapter epigraphs': ('épigraphes des chapitres', 'Kapitel-Epigraphen', 'epígrafes de capítulos', 'epígrafes de capítulos', 'epigrafi dei capitoli', 'epigrafele capitolelor', 'epigrafy rozdziałów'),
    'environmental thinking': ('pensée écologique', 'ökologisches Denken', 'pensamiento ecológico', 'pensamento ecológico', 'pensiero ecologico', 'gândire ecologică', 'myślenie ekologiczne'),
}
for phrase, labels in fix.items():
    for lang, label in zip(langs, labels):
        assert phrase in c['translations'][lang], (lang, phrase)
        c['translations'][lang][phrase] = label
p.write_text(json.dumps(c, ensure_ascii=False, indent=2) + '\n')
