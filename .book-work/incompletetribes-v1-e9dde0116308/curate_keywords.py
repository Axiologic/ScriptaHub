import json
from pathlib import Path

p = Path('tools/keyword-translations.generated.json')
c = json.loads(p.read_text())
langs = ('fr', 'de', 'es', 'pt', 'it', 'ro', 'pl')
fix = {
    'close groups': ('groupes soudés', 'enge Gruppen', 'grupos unidos', 'grupos próximos', 'gruppi uniti', 'grupuri apropiate', 'zżyte grupy'),
    'total authority': ('autorité totale', 'umfassende Autorität', 'autoridad total', 'autoridade total', 'autorità totale', 'autoritate totală', 'władza całkowita'),
    'human psychology': ('psychologie humaine', 'menschliche Psychologie', 'psicología humana', 'psicologia humana', 'psicologia umana', 'psihologie umană', 'psychologia człowieka'),
    'cynical resignation': ('résignation cynique', 'zynische Resignation', 'resignación cínica', 'resignação cínica', 'rassegnazione cinica', 'resemnare cinică', 'cyniczna rezygnacja'),
    'bounded community': ('communauté délimitée', 'begrenzte Gemeinschaft', 'comunidad delimitada', 'comunidade delimitada', 'comunità delimitata', 'comunitate delimitată', 'wspólnota o granicach'),
    'cooperation': ('coopération', 'Zusammenarbeit', 'cooperación', 'cooperação', 'cooperazione', 'cooperare', 'współpraca'),
    'insiders and outsiders': ('membres et personnes extérieures', 'Insider und Außenstehende', 'miembros y personas externas', 'membros e pessoas externas', 'membri e persone esterne', 'membri și persoane din afară', 'członkowie i osoby spoza grupy'),
    'intimacy and privacy': ('intimité et vie privée', 'Nähe und Privatsphäre', 'intimidad y privacidad', 'intimidade e privacidade', 'intimità e riservatezza', 'apropiere și viață privată', 'bliskość i prywatność'),
    'negotiated settlements': ('accords négociés', 'ausgehandelte Einigungen', 'acuerdos negociados', 'acordos negociados', 'accordi negoziati', 'înțelegeri negociate', 'wynegocjowane porozumienia'),
    'restrained sanctions': ('sanctions mesurées', 'maßvolle Sanktionen', 'sanciones moderadas', 'sanções moderadas', 'sanzioni moderate', 'sancțiuni moderate', 'umiarkowane sankcje'),
    'survivable': ('surmontable', 'überstehbar', 'superable', 'superável', 'superabile', 'suportabil', 'możliwy do przetrwania'),
    'common civic floor': ('socle civique commun', 'gemeinsame zivile Grundlage', 'base cívica común', 'base cívica comum', 'base civica comune', 'fundament civic comun', 'wspólna podstawa obywatelska'),
    'plural society': ('société pluraliste', 'pluralistische Gesellschaft', 'sociedad plural', 'sociedade plural', 'società pluralista', 'societate pluralistă', 'społeczeństwo pluralistyczne'),
    'craft': ('métier', 'Handwerk', 'oficio', 'ofício', 'mestiere', 'meșteșug', 'rzemiosło'),
    'routes for correction': ('voies de correction', 'Wege zur Korrektur', 'vías de corrección', 'vias de correção', 'vie di correzione', 'căi de corectare', 'drogi korekty'),
    'constitutional': ('constitutionnel', 'verfassungsmäßig', 'constitucional', 'constitucional', 'costituzionale', 'constituțional', 'konstytucyjny'),
    'mixed memberships': ('appartenances mixtes', 'gemischte Mitgliedschaften', 'pertenencias mixtas', 'pertenças mistas', 'appartenenze miste', 'apartenențe mixte', 'mieszane przynależności'),
    'voluntary departure': ('départ volontaire', 'freiwilliges Ausscheiden', 'salida voluntaria', 'saída voluntária', 'uscita volontaria', 'plecare voluntară', 'dobrowolne odejście'),
    'exit': ('sortie', 'Austritt', 'salida', 'saída', 'uscita', 'ieșire', 'odejście'),
    'polycentric order': ('ordre polycentrique', 'polyzentrische Ordnung', 'orden policéntrico', 'ordem policêntrica', 'ordine policentrico', 'ordine policentrică', 'ład policentryczny'),
    'rules of conflict': ('règles du conflit', 'Regeln für Konflikte', 'reglas del conflicto', 'regras de conflito', 'regole del conflitto', 'reguli ale conflictului', 'zasady prowadzenia konfliktu'),
    'law of history': ('loi de l’histoire', 'Gesetz der Geschichte', 'ley de la historia', 'lei da história', 'legge della storia', 'lege a istoriei', 'prawo historii'),
    'legitimate opposition': ('opposition légitime', 'legitime Opposition', 'oposición legítima', 'oposição legítima', 'opposizione legittima', 'opoziție legitimă', 'legalna opozycja'),
}
for phrase, labels in fix.items():
    for lang, label in zip(langs, labels):
        assert phrase in c['translations'][lang], (lang, phrase)
        c['translations'][lang][phrase] = label
p.write_text(json.dumps(c, ensure_ascii=False, indent=2) + '\n')
