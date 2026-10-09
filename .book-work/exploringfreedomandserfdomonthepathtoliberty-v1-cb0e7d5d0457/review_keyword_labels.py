import json
from pathlib import Path

work = Path(__file__).resolve().parent
manifest_path = work / 'book/manifest.json'
manifest = json.loads(manifest_path.read_text())
replacements = {
    'germany and stalinist': 'historical comparisons',
    'adria morgan': 'dilemmas of central planning',
    'goods people': 'knowledge limits planning',
    'primary work': 'role through civic engagement',
    'agent adria': 'decline of freedom',
    'state fixes': 'reclaiming liberty',
}
phrases = manifest['keywordReview']['phrases']
manifest['keywordReview']['phrases'] = [replacements.get(p, p) for p in phrases]
assert len(set(manifest['keywordReview']['phrases'])) == 90
manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')

cache_path = Path('tools/keyword-translations.generated.json')
cache = json.loads(cache_path.read_text())
translations = cache['translations']
labels = {
    'historical comparisons': ['comparaisons historiques', 'historische Vergleiche', 'comparaciones históricas', 'comparações históricas', 'confronti storici', 'comparații istorice', 'porównania historyczne'],
    'dilemmas of central planning': ['dilemmes de la planification centrale', 'Dilemmata der zentralen Planung', 'dilemas de la planificación central', 'dilemas do planeamento central', 'dilemmi della pianificazione centrale', 'dilemele planificării centrale', 'dylematy planowania centralnego'],
    'knowledge limits planning': ['les limites du savoir entravent la planification', 'Wissensgrenzen der Planung', 'los límites del conocimiento restringen la planificación', 'limites do conhecimento na planificação', 'limiti della conoscenza nella pianificazione', 'limitele cunoașterii în planificare', 'ograniczenia wiedzy w planowaniu'],
    'role through civic engagement': ['rôle de la participation civique', 'Rolle durch bürgerschaftliches Engagement', 'papel de la participación cívica', 'papel da participação cívica', 'ruolo della partecipazione civica', 'rolul implicării civice', 'rola zaangażowania obywatelskiego'],
    'decline of freedom': ['recul de la liberté', 'Rückgang der Freiheit', 'declive de la libertad', 'declínio da liberdade', 'declino della libertà', 'declinul libertății', 'zanik wolności'],
    'reclaiming liberty': ['reconquérir la liberté', 'Freiheit zurückgewinnen', 'recuperar la libertad', 'recuperar a liberdade', 'riconquistare la libertà', 'recâștigarea libertății', 'odzyskiwanie wolności'],
    'friedrich hayek': ['Friedrich Hayek'] * 7,
    'stalinist russia': ['Russie stalinienne', 'stalinistisches Russland', 'Rusia estalinista', 'Rússia stalinista', 'Russia stalinista', 'Rusia stalinistă', 'stalinowska Rosja'],
    'nazi germany': ['Allemagne nazie', 'NS-Deutschland', 'Alemania nazi', 'Alemanha nazista', 'Germania nazista', 'Germania nazistă', 'nazistowskie Niemcy'],
    'soviet union': ['Union soviétique', 'Sowjetunion', 'Unión Soviética', 'União Soviética', 'Unione Sovietica', 'Uniunea Sovietică', 'Związek Radziecki'],
    'soviet economy': ['économie soviétique', 'sowjetische Wirtschaft', 'economía soviética', 'economia soviética', 'economia sovietica', 'economia sovietică', 'gospodarka radziecka'],
    'nazi germany and stalinist russia': ['Allemagne nazie et Russie stalinienne', 'NS-Deutschland und stalinistisches Russland', 'Alemania nazi y Rusia estalinista', 'Alemanha nazista e Rússia stalinista', 'Germania nazista e Russia stalinista', 'Germania nazistă și Rusia stalinistă', 'nazistowskie Niemcy i stalinowska Rosja'],
    'state fixes prices': ['l’État fixe les prix', 'der Staat setzt Preise fest', 'el Estado fija los precios', 'o Estado fixa os preços', 'lo Stato fissa i prezzi', 'statul fixează prețurile', 'państwo ustala ceny'],
    'property and contracts': ['propriété et contrats', 'Eigentum und Verträge', 'propiedad y contratos', 'propriedade e contratos', 'proprietà e contratti', 'proprietate și contracte', 'własność i umowy'],
    'danger of concentrated power': ['danger du pouvoir concentré', 'Gefahr konzentrierter Macht', 'peligro del poder concentrado', 'perigo do poder concentrado', 'pericolo del potere concentrato', 'pericolul puterii concentrate', 'zagrożenie skoncentrowaną władzą'],
    'personal agency': ['capacité d’agir individuelle', 'persönliche Handlungsfähigkeit', 'capacidad de acción individual', 'capacidade de agir individual', 'capacità di agire individuale', 'capacitatea individuală de a acționa', 'indywidualna sprawczość'],
    'producing shortages': ['création de pénuries', 'Engpässe verursachen', 'generar escasez', 'criar escassez', 'generare carenze', 'producerea penuriei', 'powodowanie niedoborów'],
    'resistance harder': ['résistance plus difficile', 'Widerstand erschweren', 'dificultar la resistencia', 'dificultar a resistência', 'rendere più difficile la resistenza', 'îngreunarea rezistenței', 'utrudnianie oporu'],
    'form enterprises': ['créer des entreprises', 'Unternehmen gründen', 'crear empresas', 'criar empresas', 'fondare imprese', 'înființarea de întreprinderi', 'zakładanie przedsiębiorstw'],
}
for phrase, values in labels.items():
    for language, value in zip(('fr', 'de', 'es', 'pt', 'it', 'ro', 'pl'), values):
        translations[language][phrase] = value
cache_path.write_text(json.dumps(cache, ensure_ascii=False, indent=2) + '\n')
