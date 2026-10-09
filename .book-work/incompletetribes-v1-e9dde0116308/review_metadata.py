import json
import re
from pathlib import Path

root = Path('.book-work/incompletetribes-v1-e9dde0116308')
path = root / 'book/manifest.json'
data = json.loads(path.read_text(encoding='utf-8'))
copy = {
    'en': [
        'Human beings need belonging, yet loyalty can turn neighbors into enemies.',
        'This essay proposes incomplete tribes: demanding communities that refuse total authority over their members.',
        'It traces how social identity, conflicting ideals, and institutional rules shape cooperation.',
        'Overlapping affiliations and protected dissent limit the power of any single group.',
        'Polycentric governance lets imperfect communities solve shared problems without claiming one final order.',
        'The closing chapters test this hope against artificial intelligence, technological risk, and the fear of failure.',
    ],
    'ro': [
        'Oamenii au nevoie de apartenență, însă loialitatea îi poate transforma pe vecini în dușmani.',
        'Eseul propune triburi incomplete: comunități exigente care refuză autoritatea totală asupra membrilor lor.',
        'Urmărește felul în care identitatea socială, idealurile contradictorii și regulile instituționale modelează cooperarea.',
        'Afilierea la mai multe grupuri și dreptul protejat la dezacord limitează puterea fiecăruia.',
        'Guvernanța policentrică ajută comunități imperfecte să rezolve probleme comune fără să pretindă o ordine finală.',
        'Ultimele capitole confruntă această speranță cu inteligența artificială, riscul tehnologic și teama de eșec.',
    ],
    'fr': [
        'Les humains ont besoin d’appartenir à un groupe, mais la loyauté peut transformer des voisins en ennemis.',
        'Cet essai propose des tribus incomplètes : des communautés exigeantes qui refusent toute autorité totale sur leurs membres.',
        'Il examine comment l’identité sociale, les idéaux contradictoires et les règles institutionnelles façonnent la coopération.',
        'Les appartenances multiples et le droit protégé à la dissidence limitent le pouvoir de chaque groupe.',
        'Une gouvernance polycentrique aide des communautés imparfaites à résoudre leurs problèmes communs sans imposer un ordre définitif.',
        'Les derniers chapitres confrontent cet espoir à l’intelligence artificielle, aux risques technologiques et à la peur de l’échec.',
    ],
    'de': [
        'Menschen brauchen Zugehörigkeit, doch Loyalität kann Nachbarn zu Feinden machen.',
        'Dieser Essay entwirft unvollständige Stämme: anspruchsvolle Gemeinschaften, die keine vollständige Herrschaft über ihre Mitglieder beanspruchen.',
        'Er untersucht, wie soziale Identität, widersprüchliche Ideale und institutionelle Regeln Zusammenarbeit prägen.',
        'Mehrfache Zugehörigkeiten und geschützter Widerspruch begrenzen die Macht jeder einzelnen Gruppe.',
        'Polyzentrische Ordnung hilft unvollkommenen Gemeinschaften, gemeinsame Probleme ohne Anspruch auf eine endgültige Ordnung zu lösen.',
        'Die letzten Kapitel prüfen diese Hoffnung angesichts künstlicher Intelligenz, technologischer Risiken und der Angst vor dem Scheitern.',
    ],
    'es': [
        'Las personas necesitan pertenecer, pero la lealtad puede convertir a los vecinos en enemigos.',
        'Este ensayo propone tribus incompletas: comunidades exigentes que rechazan la autoridad total sobre sus miembros.',
        'Examina cómo la identidad social, los ideales contradictorios y las reglas institucionales moldean la cooperación.',
        'Las pertenencias múltiples y el derecho protegido a disentir limitan el poder de cualquier grupo.',
        'La gobernanza policéntrica ayuda a comunidades imperfectas a resolver problemas compartidos sin imponer un orden definitivo.',
        'Los capítulos finales ponen a prueba esta esperanza frente a la inteligencia artificial, el riesgo tecnológico y el miedo al fracaso.',
    ],
    'pt': [
        'As pessoas precisam de pertença, mas a lealdade pode transformar vizinhos em inimigos.',
        'Este ensaio propõe tribos incompletas: comunidades exigentes que recusam autoridade total sobre os seus membros.',
        'Examina como a identidade social, os ideais contraditórios e as regras institucionais moldam a cooperação.',
        'As pertenças múltiplas e o direito protegido à discordância limitam o poder de cada grupo.',
        'A governação policêntrica ajuda comunidades imperfeitas a resolver problemas comuns sem impor uma ordem definitiva.',
        'Os capítulos finais testam esta esperança perante a inteligência artificial, o risco tecnológico e o medo do fracasso.',
    ],
    'it': [
        'Le persone hanno bisogno di appartenenza, ma la lealtà può trasformare i vicini in nemici.',
        'Questo saggio propone tribù incomplete: comunità esigenti che rifiutano un’autorità totale sui propri membri.',
        'Esamina come identità sociale, ideali contrastanti e regole istituzionali plasmino la cooperazione.',
        'Appartenenze multiple e diritto tutelato al dissenso limitano il potere di ogni gruppo.',
        'Una governance policentrica aiuta comunità imperfette a risolvere problemi comuni senza imporre un ordine definitivo.',
        'Gli ultimi capitoli mettono alla prova questa speranza davanti all’intelligenza artificiale, al rischio tecnologico e alla paura del fallimento.',
    ],
    'pl': [
        'Ludzie potrzebują przynależności, lecz lojalność może zmienić sąsiadów we wrogów.',
        'Ten esej proponuje niekompletne plemiona: wymagające wspólnoty, które odmawiają sobie pełnej władzy nad członkami.',
        'Bada, jak tożsamość społeczna, sprzeczne ideały i reguły instytucjonalne kształtują współpracę.',
        'Wielorakie przynależności i chronione prawo do sprzeciwu ograniczają władzę każdej grupy.',
        'Policentryczne zarządzanie pomaga niedoskonałym wspólnotom rozwiązywać wspólne problemy bez narzucania ostatecznego porządku.',
        'Końcowe rozdziały konfrontują tę nadzieję ze sztuczną inteligencją, ryzykiem technologicznym i lękiem przed porażką.',
    ],
}

assert set(copy) == set(data['title'])
for lang, sentences in copy.items():
    assert len(sentences) == 6
    for sentence in sentences:
        assert len(sentence.split()) <= 22, (lang, sentence)
    data['shortDescription'][lang] = ' '.join(sentences)
    data['aboutBook'][lang] = [' '.join(sentences[:3]), ' '.join(sentences[3:])]
data['shortDescriptionEditorial'] = {
    'status': 'reviewed',
    'source': 'complete English manuscript and ten-minute edition',
    'sentencesPerLanguage': 6,
    'date': '2026-10-09',
}
path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
release_path = root / 'release.json'
release = json.loads(release_path.read_text(encoding='utf-8'))
release['changes'] = {
    'en': 'Initial ScriptaHub edition with complete and ten-minute English and Romanian readers, a clean English PDF, and a revised cover.',
    'ro': 'Ediția inițială ScriptaHub, cu versiuni integrale și de zece minute în engleză și română, un PDF englez curat și o copertă refăcută.',
}
release_path.write_text(json.dumps(release, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print('Reviewed metadata in eight interface languages')
