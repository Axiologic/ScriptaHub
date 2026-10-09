import json
from pathlib import Path

t = {
't000001': 'Un ghid obraznic al filosofiei Greciei antice — Ediția de zece minute',
't000002': 'Un ghid obraznic al filosofiei Greciei antice',
't000003': 'Acest ghid alert și voit ireverențios urmărește filosofia greacă de la presocratici prin școlile clasice și elenistice, apoi caută ecourile ei ulterioare în gândirea europeană. Glumele și scenele inventate sunt un stil de predare, nu dovezi istorice. Întrebările filosofice de sub ele sunt serioase: din ce este alcătuită lumea, ce putem ști, cum ar trebui să trăim și cum își schimbă forma argumentele vechi? Cartea folosește patru capitole și o recapitulare pentru a apropia aceste întrebări de cititor, fără să pretindă că o singură școală le-a rezolvat.',
't000004': 'Căutarea presocratică a naturii',
't000005': 'Primul capitol începe cu gânditori timpurii care încearcă să explice lumea prin principii, nu prin povești moștenite. Thales propune apa drept element fundamental. Anaximandru răspunde prin apeiron, un izvor nelimitat care nu poate fi redus la un material familiar. Heraclit îndreaptă atenția spre schimbare și spre imaginea râului în care nu poți intra de două ori în exact același fel. Glumele capitolului le exagerează personalitățile, dar contrastul dintre substanțele propuse, nelimitat și schimbarea permanentă îi ajută pe cititori să pătrundă în disputele lor.',
't000006': 'Presocraticii contează aici pentru că întreabă ce stă la baza multitudinii de lucruri pe care le vedem. Chiar și răspunsurile care sună astăzi ciudat transformă o observație simplă într-o întrebare ce poate fi dezbătută. Cartea tratează propunerile lor rivale drept începutul unei conversații continue, nu ca pe o succesiune de fapte de memorat.',
't000007': 'Citește integral secțiunea 1',
't000008': 'Socrate, Platon și Aristotel',
't000009': 'Al doilea capitol îi adună pe cei „trei mari” ai perioadei clasice. Socrate apare ca un interlocutor neobosit, care verifică încrederea oamenilor în ceea ce pretind că știu. Metoda lui face din conversație un instrument de examinare, iar refuzul răspunsurilor facile este parte din lecție. Platon dezvoltă distincția dintre lumea așa cum apare și o realitate mai stabilă a Formelor. Imaginea peșterii întreabă ce ar însemna educația dacă aparențele familiare ar fi doar umbrele a ceva mai profund.',
't000010': 'Aristotel contestă părți ale abordării lui Platon acordând mai multă atenție lumii observabile. Ghidul prezintă interesele lui variate, de la studiul naturii și politică la etică, și introduce calea de mijloc drept mod de a gândi proporția dintre extreme. Diferențele lor contează la fel de mult ca influența comună: întrebarea, explicația abstractă și observația oferă căi diferite spre înțelegere.',
't000011': 'Citește integral secțiunea 2',
't000012': 'Filosofia ca mod de viață',
't000013': 'După Alexandru, școlile elenistice mută ghidul de la teoriile despre realitate la problema vieții bune. Cinicii contestă convențiile printr-o simplitate radicală, iar Diogene oferă cele mai comice exemple ale cărții. Stoicii se concentrează asupra răspunsului la evenimentele pe care nu le putem controla. Epicurienii caută plăcerea prin moderație, nu prin răsfăț fără sfârșit. Scepticii pun la îndoială pretențiile de certitudine și țin cercetarea deschisă.',
't000014': 'Comparațiile contemporane ale capitolului sunt intenționat jucăușe. Sub ele se află o neînțelegere practică: vine libertatea din renunțarea la așteptările sociale, disciplinarea judecății, alegerea unor satisfacții modeste sau refuzul concluziilor pripite? Fiecare școală oferă alt răspuns la o întrebare pe care cititorii o pot aplica încă propriilor obiceiuri și decizii.',
't000015': 'Citește integral secțiunea 3',
't000016': 'Lunga mahmureală filosofică',
't000017': 'Al patrulea capitol face un tur rapid și comic al felului în care argumentele grecești reapar după Antichitate. Cititorii Renașterii se întorc la textele vechi; Revoluția Științifică reînnoiește disputele despre forma matematică și observație. Filosofi ulteriori precum Descartes, Spinoza, Leibniz, Locke și Hume reiau întrebări despre minte, experiență, substanță și cunoaștere. Cartea trece apoi prin Nietzsche, existențialism, fenomenologie, filosofie analitică, postmodernism și dezbateri contemporane. Scopul ei este să arate un lanț de întrebări recurente, nu să confunde acești gânditori diferiți.',
't000018': 'Legăturile cu etica, tehnologia și politica moderne aduc turul înapoi la viața de zi cu zi. Ce contează ca dovadă? Cum modelează limbajul o problemă? Identitatea este dată sau construită? Cum ar trebui să răspundă oamenii când noile tehnologii schimbă condițiile alegerii? Ritmul capitolului îi invită pe cititori să recunoască tensiuni filosofice vechi în contexte noi și apoi să revină la discuțiile mai ample despre gânditorii care îi interesează.',
't000019': 'Citește integral secțiunea 4',
't000020': 'Ce îi invită ghidul pe cititori să păstreze',
't000021': 'Concluzia reia cele trei perioade antice. Presocraticii întreabă din ce este alcătuită lumea; gânditorii clasici examinează cunoașterea, realitatea și etica; școlile elenistice fac filosofia practică. Cartea refuză să transforme această istorie într-un răspuns final. Invitația ei durabilă este să punem la îndoială afirmațiile familiare, să comparăm moduri posibile de a trăi și să ne folosim curiozitatea fără să pierdem simțul umorului. Glumele pot fi lăsate deoparte; întrebările merită puse în continuare.',
't000022': 'Citește integral secțiunea 5',
}

base = Path(__file__).parent / 'translations/ro/short/chunks'
for path in sorted(base.glob('*.json')):
    data = json.loads(path.read_text(encoding='utf-8'))
    for segment in data['segments']:
        segment['translation'] = t[segment['id']]
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
