import json
from pathlib import Path

cache_path = Path('tools/keyword-translations.generated.json')
cache = json.loads(cache_path.read_text())
fixes = {
    'Liesel Meminger': {'de': 'Liesel Meminger'},
    "Death's narration": {'fr': 'narration de la Mort', 'de': 'Erzählung des Todes', 'es': 'narración de la Muerte', 'pt': 'narração da Morte', 'it': 'narrazione della Morte', 'ro': 'narațiunea Morții', 'pl': 'narracja Śmierci'},
    'Himmel Street': {'de': 'Himmelstraße', 'it': 'via Himmel', 'pl': 'ulica Himmel'},
    'Hubermann household': {'fr': 'famille Hubermann', 'de': 'Familie Hubermann', 'es': 'familia Hubermann', 'pt': 'família Hubermann', 'it': 'famiglia Hubermann', 'ro': 'familia Hubermann', 'pl': 'rodzina Hubermannów'},
    'Hubermann home': {'fr': 'maison des Hubermann', 'de': 'Haus der Hubermanns', 'es': 'casa de los Hubermann', 'pt': 'casa dos Hubermann', 'it': 'casa degli Hubermann', 'ro': 'casa familiei Hubermann', 'pl': 'dom Hubermannów'},
    'foster family': {'fr': "famille d'accueil", 'pt': 'família de acolhimento', 'it': 'famiglia affidataria', 'ro': 'familie de plasament', 'pl': 'rodzina zastępcza'},
    'foster father': {'fr': "père d'accueil", 'es': 'padre de acogida', 'pt': 'pai de acolhimento', 'it': 'padre affidatario', 'ro': 'tată de plasament'},
    'foster home': {'fr': "foyer d'accueil", 'de': 'Pflegefamilie', 'es': 'hogar de acogida', 'pt': 'lar de acolhimento', 'it': 'casa della famiglia affidataria', 'ro': 'cămin de plasament'},
    'power of language': {'de': 'Macht der Sprache', 'it': 'potere del linguaggio', 'ro': 'puterea limbajului', 'pl': 'siła języka'},
    'Nazi book burnings': {'fr': 'autodafés nazis', 'es': 'quema nazi de libros', 'it': 'roghi nazisti di libri', 'ro': 'arderile naziste de cărți', 'pl': 'nazistowskie palenie książek'},
    'book burnings': {'fr': 'autodafés de livres', 'it': 'roghi di libri', 'ro': 'arderea cărților', 'pl': 'palenie książek'},
    'private grief': {'fr': 'deuil intime', 'de': 'persönliche Trauer', 'es': 'duelo íntimo', 'pt': 'luto íntimo', 'it': 'lutto privato', 'ro': 'durere intimă', 'pl': 'osobista żałoba'},
    'preserve memory': {'de': 'Erinnerung bewahren'},
    'cost of survival': {'de': 'Preis des Überlebens', 'pl': 'cena przetrwania'},
    'bombing of Himmel Street': {'de': 'Bombardierung der Himmelstraße', 'it': 'bombardamento di via Himmel', 'ro': 'bombardarea străzii Himmel', 'pl': 'bombardowanie ulicy Himmel'},
    'air-raid sirens': {'fr': "sirènes d'alerte aérienne", 'de': 'Luftschutzsirenen', 'es': 'sirenas antiaéreas', 'pt': 'sirenes de alerta aéreo', 'it': 'sirene antiaeree', 'ro': 'sirene de raid aerian', 'pl': 'syreny alarmu lotniczego'},
    'quiet acts of care': {'fr': 'gestes discrets de sollicitude', 'de': 'stille Gesten der Fürsorge', 'es': 'gestos discretos de cuidado', 'pt': 'gestos discretos de cuidado', 'it': 'gesti discreti di cura', 'ro': 'gesturi discrete de grijă', 'pl': 'ciche gesty troski'},
    'Jewish man': {'ro': 'bărbat evreu', 'pl': 'Żyd'},
    'hiding place': {'fr': 'cachette', 'ro': 'ascunzătoare', 'pl': 'kryjówka'},
    'Hans shelters Max': {'ro': 'Hans îl adăpostește pe Max', 'pl': 'Hans ukrywa Maxa'},
    'resist silence': {'fr': 'résister au silence', 'de': 'dem Schweigen widerstehen', 'es': 'resistir al silencio', 'ro': 'a rezista tăcerii'},
    'enforced silence': {'pl': 'narzucone milczenie'},
    'material link': {'de': 'materielle Verbindung', 'pl': 'materialna więź'},
    'shared reading': {'de': 'gemeinsames Lesen', 'ro': 'lectură împreună'},
    'public hostility toward Jews': {'pl': 'publiczna wrogość wobec Żydów'},
    'public hostility': {'pl': 'publiczna wrogość'},
    'swastikas': {'it': 'svastiche', 'ro': 'svastici', 'pl': 'swastyki'},
    'connection and hope': {'fr': 'liens et espoir', 'it': 'legami e speranza', 'ro': 'legături și speranță', 'pl': 'więzi i nadzieja'},
    'interpretive companion': {'fr': 'guide de lecture', 'de': 'Lektürebegleiter', 'es': 'guía de lectura', 'pt': 'guia de leitura', 'it': 'guida alla lettura', 'ro': 'ghid de lectură', 'pl': 'przewodnik po lekturze'},
    'literacy': {'pl': 'umiejętność czytania i pisania'},
    "Liesel's reading": {'de': 'Liesels Lektüre', 'pt': 'leitura de Liesel', 'ro': 'lecturile lui Liesel', 'pl': 'lektura Liesel'},
    "Death's perspective": {'fr': 'perspective de la Mort', 'es': 'perspectiva de la Muerte', 'pt': 'perspectiva da Morte', 'it': 'prospettiva della Morte', 'ro': 'perspectiva Morții', 'pl': 'perspektywa Śmierci'},
    'limits of silence': {'de': 'Grenzen des Schweigens', 'pt': 'limites do silêncio', 'it': 'limiti del silenzio', 'ro': 'limitele tăcerii', 'pl': 'granice milczenia'},
    'life under Nazism': {'ro': 'viața sub nazism', 'pl': 'życie pod nazizmem'},
    'acts of care': {'fr': 'gestes de sollicitude', 'de': 'Gesten der Fürsorge', 'es': 'gestos de cuidado', 'ro': 'gesturi de grijă'},
    'advancing war': {'fr': 'progression de la guerre', 'de': 'Vorrücken des Krieges', 'es': 'avance de la guerra', 'pt': 'avanço da guerra', 'it': 'avanzata della guerra', 'ro': 'înaintarea războiului', 'pl': 'postępująca wojna'},
    'stolen handbook': {'it': 'manuale rubato', 'ro': 'manual furat'},
    'rough manner': {'fr': 'manière rude', 'de': 'raue Art', 'es': 'manera brusca', 'pt': 'maneira rude', 'it': 'modo brusco', 'ro': 'fire aspră', 'pl': 'szorstkie zachowanie'},
    'collecting laundry': {'fr': 'ramassage du linge', 'de': 'Wäsche abholen', 'es': 'recoger la ropa para lavar', 'pt': 'recolher roupa para lavar', 'it': 'ritiro della biancheria', 'ro': 'strângerea rufelor', 'pl': 'odbieranie prania'},
    'laundry for Rosa': {'fr': 'linge à laver pour Rosa', 'es': 'ropa para lavar para Rosa', 'pt': 'roupa para lavar para Rosa', 'it': 'biancheria da lavare per Rosa', 'ro': 'rufe de spălat pentru Rosa'},
    'swastikas and public hostility': {'fr': 'svastikas et hostilité publique', 'it': 'svastiche e ostilità pubblica', 'ro': 'svastici și ostilitate publică', 'pl': 'swastyki i publiczna wrogość'},
    'death and Liesel': {'fr': 'la Mort et Liesel', 'de': 'der Tod und Liesel', 'es': 'la Muerte y Liesel', 'pt': 'a Morte e Liesel', 'it': 'la Morte e Liesel', 'ro': 'Moartea și Liesel', 'pl': 'Śmierć i Liesel'},
}
for phrase, translations in fixes.items():
    for lang, value in translations.items():
        assert phrase in cache['translations'][lang], (phrase, lang)
        cache['translations'][lang][phrase] = value
cache_path.write_text(json.dumps(cache, ensure_ascii=False, indent=2) + '\n')
print(sum(map(len, fixes.values())), 'keyword labels reviewed')
