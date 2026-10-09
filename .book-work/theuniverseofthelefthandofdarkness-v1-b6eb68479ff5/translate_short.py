import json
from pathlib import Path

root = Path(__file__).parent / 'translations/ro/short/chunks'
translations = {
    't000001': 'Universul romanului Mâna stângă a întunericului — Ediția de zece minute',
    't000002': 'Universul romanului Mâna stângă a întunericului',
    't000003': 'Acest ghid citește romanul Mâna stângă a întunericului de Ursula K. Le Guin prin prisma genului, politicii, culturii și a muncii lente de a înțelege o altă persoană. Pe Gethen, Genly Ai caută să aducă o lume în Ekumen, învățând în același timp cum propriile presupuneri îi deformează percepția. Cartea întreabă ce se schimbă când lipsesc categoriile fixe de gen și ce rămâne: rivalitatea, ierarhia, frica și nevoia de încredere continuă să modeleze societatea.',
    't000004': 'Sosirea cu propriile presupuneri',
    't000005': 'Introducerea îl așază pe Genly între Karhide și Orgoreyn, două națiuni rivale cu forme diferite de guvernare. Gethenienii nu au identități permanente masculine sau feminine; caracteristicile lor sexuale se schimbă în timpul kemmerului. Misiunea lui Genly este diplomatică, dar și o școală a ascultării. Ghidul urmărește tensiunea dintre ceea ce un străin crede că știe și ceea ce fac de fapt oamenii de pe Gethen.',
    't000006': 'Citește integral secțiunea 1',
    't000007': 'Putere fără gen fix',
    't000008': 'Primul capitol întreabă dacă lipsa unor roluri permanente de gen produce o lume politică mai dreaptă. Ea poate înlătura anumite forme cunoscute de ierarhie, dar nu șterge ambiția sau controlul. Instituțiile continuă să împartă autoritatea, iar relațiile personale poartă încă așteptări inegale. Capitolul tratează Gethenul ca pe un mod de a pune la încercare presupunerile despre originile puterii, nu ca pe o utopie simplă.',
    't000009': 'Citește integral secțiunea 2',
    't000010': 'Androginie și relații',
    't000011': 'Al doilea capitol privește mai atent kemmerul și sensurile sociale ale sexului fluid. Familia, intimitatea și rolul de părinte funcționează altfel când oricine poate îndeplini roluri reproductive diferite. Genly îi înțelege inițial pe gethenieni prin categoriile aduse din propria lume, ceea ce îi limitează cunoașterea. Ghidul leagă această problemă de lecturile feministe și taoiste ale romanului, mai ales de interesul lui pentru forțe pereche care nu trebuie să fie opuse pentru totdeauna.',
    't000012': 'Citește integral secțiunea 3',
    't000013': 'Două națiuni, două feluri de presiune',
    't000014': 'Al treilea capitol compară monarhia și tradițiile din Karhide cu birocrația și supravegherea din Orgoreyn. Ambele guverne au mijloace de a modela ceea ce cetățenii pot spune și face. Mândria națională, frica și neînțelegerile îngreunează încercarea lui Genly de a construi încredere diplomatică. Religia și memoria culturală influențează și ele alegerile politice. Capitolul întreabă dacă înțelegerea altei culturi poate trece peste o ruptură pe care instituțiile puternice au interesul să o păstreze.',
    't000015': 'Citește integral secțiunea 4',
    't000016': 'Traversarea gheții',
    't000017': 'Capitolul al patrulea îi urmărește pe Genly și Estravan în călătoria lor grea peste întinderea înghețată. Supraviețuirea cere cooperare, iar riscul împărtășit schimbă felul în care Genly își vede tovarășul. Aici cunoașterea înseamnă mai mult decât observarea de la distanță; ea crește prin dependență reciprocă, vulnerabilitate și experiență. Traversarea gheții oferă ghidului cel mai limpede exemplu al unei relații care depășește suspiciunea moștenită.',
    't000018': 'Citește integral secțiunea 5',
    't000019': 'Forme ale controlului',
    't000020': 'Al cincilea capitol examinează puterea la mai multe scări. Regele Argaven domnește prin autoritate personală și imprevizibilitate; Orgoreyn se sprijină pe control administrativ și constrângere ascunsă. Genly și Estravan trebuie și ei să negocieze încrederea și influența în propria relație. Ghidul arată cum romanul pune alături puterea personală și cea politică, întrebând dacă vreuna dintre ele poate fi exercitată fără a trata o altă persoană ca pe un obiect.',
    't000021': 'Citește integral secțiunea 6',
    't000022': 'De ce să citești studiul integral?',
    't000023': 'Concluzia revine la gen, autoritate și înțelegere culturală. Lumea fictivă a lui Le Guin nu oferă o rețetă pentru societate, dar zdruncină presupuneri familiare și răsplătește atenția răbdătoare. Cititorii interesați de gen pot începe cu primele două capitole; cei atrași de diplomație pot porni de la Karhide și Orgoreyn, apoi pot urmări traversarea gheții. De la un capăt la altul, cartea întreabă cum învățăm să recunoaștem o persoană dincolo de categoriile pe care le-am adus cu noi.',
    't000024': 'Citește integral secțiunea 7',
}
for path in sorted(root.glob('*.json')):
    data = json.loads(path.read_text())
    for segment in data['segments']:
        segment['translation'] = translations[segment['id']]
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')
