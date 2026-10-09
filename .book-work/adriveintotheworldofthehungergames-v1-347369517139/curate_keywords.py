import json
from pathlib import Path

cache_path = Path('tools/keyword-translations.generated.json')
cache = json.loads(cache_path.read_text())
languages = ('fr', 'de', 'es', 'pt', 'it', 'ro', 'pl')
replacements = {
    'wealthy Capitol': ('Capitole prospère', 'wohlhabendes Kapitol', 'Capitolio próspero', 'Capital próspera', 'Capitol City prospera', 'Capitoliul bogat', 'bogaty Kapitol'),
    'poorer districts': ('districts plus pauvres', 'ärmere Distrikte', 'distritos más pobres', 'distritos mais pobres', 'distretti più poveri', 'districte mai sărace', 'biedniejsze dystrykty'),
    'private act of protection': ('geste privé de protection', 'private Schutzhandlung', 'acto privado de protección', 'ato privado de proteção', 'gesto privato di protezione', 'gest privat de protecție', 'prywatny akt ochrony'),
    'public challenge': ('défi public', 'öffentliche Herausforderung', 'desafío público', 'desafio público', 'sfida pubblica', 'sfidare publică', 'publiczne wyzwanie'),
    'defeated rebellion': ('rébellion écrasée', 'niedergeschlagene Rebellion', 'rebelión derrotada', 'rebelião derrotada', 'ribellione sconfitta', 'rebeliune înfrântă', 'stłumiony bunt'),
    'solidarity': ('solidarité', 'Solidarität', 'solidaridad', 'solidariedade', 'solidarietà', 'solidaritate', 'solidarność'),
    'Panem': ('Panem', 'Panem', 'Panem', 'Panem', 'Panem', 'Panem', 'Panem'),
    'Katniss': ('Katniss', 'Katniss', 'Katniss', 'Katniss', 'Katniss', 'Katniss', 'Katniss'),
    'Mockingjay': ('Mockingjay', 'Mockingjay', 'Sinsajo', 'Tordo', 'Ghiandaia imitatrice', 'Gaița zeflemitoare', 'Kosogłos'),
    'Prim': ('Prim', 'Prim', 'Prim', 'Prim', 'Prim', 'Prim', 'Prim'),
    'arena': ('arène', 'Arena', 'arena', 'arena', 'arena', 'arenă', 'arena'),
    'Tributes': ('tributs', 'Tribute', 'tributos', 'tributos', 'tributi', 'tributuri', 'trybuci'),
    'muttations': ('créatures mutantes', 'Mutationen', 'mutaciones', 'mutações', 'mutazioni', 'mutații', 'mutacje'),
    'annual reaping': ('tirage annuel au sort', 'jährliche Auslosung', 'sorteo anual', 'sorteio anual', 'sorteggio annuale', 'selecția anuală', 'coroczne losowanie'),
    'prequel': ('préquelle', 'Vorgeschichte', 'precuela', 'prequela', 'prequel', 'prequel', 'prequel'),
    'dystopian fiction': ('fiction dystopique', 'dystopische Literatur', 'ficción distópica', 'ficção distópica', 'narrativa distopica', 'ficțiune distopică', 'literatura dystopijna'),
    'reluctant resistance': ('résistance hésitante', 'widerwilliger Widerstand', 'resistencia reticente', 'resistência relutante', 'resistenza riluttante', 'rezistență ezitantă', 'niechętny opór'),
    'fan discussion': ('discussion entre fans', 'Fandiskussion', 'debate de aficionados', 'discussão entre fãs', 'discussione tra fan', 'discuție între fani', 'dyskusja fanów'),
    'rigid district system': ('système rigide de districts', 'starres Distriktsystem', 'sistema rígido de distritos', 'sistema rígido de distritos', 'rigido sistema dei distretti', 'sistem rigid de districte', 'sztywny system dystryktów'),
    'controlled memory': ('mémoire contrôlée', 'kontrollierte Erinnerung', 'memoria controlada', 'memória controlada', 'memoria controllata', 'memorie controlată', 'kontrolowana pamięć'),
    'engineered contest': ('compétition organisée', 'inszenierter Wettbewerb', 'competición diseñada', 'competição planejada', 'competizione orchestrata', 'competiție orchestrată', 'zaprojektowane zawody'),
    'engineered creatures': ('créatures conçues artificiellement', 'künstlich erschaffene Kreaturen', 'criaturas creadas artificialmente', 'criaturas criadas artificialmente', 'creature create artificialmente', 'creaturi create artificial', 'sztucznie stworzone istoty'),
    'broadcast spectacle': ('spectacle télévisé', 'Fernsehspektakel', 'espectáculo televisado', 'espetáculo transmitido', 'spettacolo televisivo', 'spectacol televizat', 'telewizyjne widowisko'),
    'Capitol luxury': ('luxe du Capitole', 'Luxus des Kapitols', 'lujo del Capitolio', 'luxo da Capital', 'lusso di Capitol City', 'luxul Capitoliului', 'luksus Kapitolu'),
    'district hardship': ('difficultés des districts', 'Not in den Distrikten', 'penurias de los distritos', 'privações dos distritos', 'difficoltà dei distretti', 'greutățile districtelor', 'trudności w dystryktach'),
    'uneven access': ('accès inégal', 'ungleicher Zugang', 'acceso desigual', 'acesso desigual', 'accesso diseguale', 'acces inegal', 'nierówny dostęp'),
    'environmental disaster': ('catastrophe environnementale', 'Umweltkatastrophe', 'desastre ambiental', 'catástrofe ambiental', 'catastrofe ambientale', 'dezastru ecologic', 'katastrofa ekologiczna'),
    'work': ('travail', 'Arbeit', 'trabajo', 'trabalho', 'lavoro', 'muncă', 'praca'),
    'regime': ('régime', 'Regime', 'régimen', 'regime', 'regime', 'regim', 'reżim'),
    'history': ('histoire', 'Geschichte', 'historia', 'história', 'storia', 'istorie', 'historia'),
    'compulsory terror': ('terreur imposée', 'erzwungener Terror', 'terror impuesto', 'terror imposto', 'terrore imposto', 'teroare impusă', 'narzucony terror'),
    'fellow children': ('autres enfants', 'andere Kinder', 'otros niños', 'outras crianças', 'altri bambini', 'alți copii', 'inne dzieci'),
    'labour': ('main-d’œuvre', 'Arbeitskraft', 'mano de obra', 'mão de obra', 'manodopera', 'forță de muncă', 'siła robocza'),
    'monitor': ('surveiller', 'überwachen', 'vigilar', 'vigiar', 'sorvegliare', 'a monitoriza', 'monitorować'),
    'resist': ('résister', 'Widerstand leisten', 'resistir', 'resistir', 'resistere', 'a rezista', 'stawiać opór'),
}
for phrase, labels in replacements.items():
    for language, label in zip(languages, labels):
        assert phrase in cache['translations'][language]
        cache['translations'][language][phrase] = label
cache_path.write_text(json.dumps(cache, ensure_ascii=False, indent=2) + '\n')
