import json
from pathlib import Path

path = Path(__file__).parent / 'chunks/0001.json'
data = json.loads(path.read_text())
translations = [
    'O interpretare plină de umor a romanului Frankenstein de Mary Shelley — Ediția de zece minute',
    'O interpretare plină de umor a romanului Frankenstein de Mary Shelley',
    'Ediția de zece minute',
    'Această carte repovestește romanul',
    'Frankenstein',
    'al lui Mary Shelley pe un ton comic, punând în același timp întrebări serioase despre creație, abandon și responsabilitate. Glumele ei nu șterg suferința din povestea lui Victor Frankenstein. Ele scot în evidență cât de des un om strălucit evită consecințele propriilor alegeri. În patru capitole, cititorul urmărește crearea monstrului, încercările creaturii de a-și găsi un loc, confruntarea lor distrugătoare și actualitatea etică a romanului.',
    'Ambiție și consecințe',
    'La Geneva, Victor Frankenstein are familie, afecțiune și un interes mistuitor pentru știință. La Universitatea din Ingolstadt urmărește secretul vieții atât de intens, încât relațiile obișnuite și grija față de sine dispar din vedere. Repovestirea transformă laboratorul său într-un atelier macabru: Victor adună părți de corp, le coase laolaltă și folosește un dispozitiv electric pentru a le însufleți. Comparațiile comice subliniază ambiția nechibzuită, fără a prezenta experimentul ca admirabil.',
    'Când creatura își deschide ochii galbeni, Victor vede un rezultat de aproape doi metri și jumătate pe care nu-l poate suporta. Fuge și lasă o minte nou-născută într-un corp adult să descopere singură lumea. Fuga lui fixează întrebarea centrală a cărții: ce datorează un creator unei ființe conștiente pe care a creat-o? Victor consideră reușita din laborator drept sfârșitul datoriei sale, deși ea marchează începutul unei responsabilități mult mai grele.',
    'După uciderea fratelui mai mic al lui Victor, William, Victor își bănuiește creatura abandonată. Nu spune nimic, iar servitoarea familiei, Justine, este acuzată pe nedrept și executată. Povestea alătură orgoliul științific și tăcerea morală: refuzul lui Victor de a vorbi are consecințe pentru oameni care n-au ales niciodată să participe la experimentul său. Căutând alinare în Alpi, o întâlnește în schimb pe creatură pe un ghețar. Aceasta îi cere să-i creeze o tovarășă și promite să trăiască departe de omenire dacă el acceptă.',
    'Citește integral primul capitol',
    'Respingere și furie',
    'Capitolul al doilea urmărește experiența creaturii din interior. Se trezește singură, descoperă lumina, focul, hrana și limbajul și întâlnește repetat frică în loc de bun-venit. Glumele despre statura și înfățișarea ei însoțesc un tipar dureros: oamenii o judecă drept monstru înainte de a o auzi vorbind. Dorința ei de a avea pe cineva alături este obișnuită, chiar dacă trupul îi este neobișnuit.',
    'Ascunsă lângă căsuța familiei De Lacey, creatura îi privește pe tatăl orb, Felix, Agatha și Safie. Viața lor zilnică o învață să citească și să înțeleagă sentimentele oamenilor. Speră că bătrânul orb o va primi fără să-i judece înfățișarea, dar familia se întoarce, intră în panică și o alungă. După ce creatura salvează o fată de la înec, tatăl speriat al acesteia o împușcă. Bunătatea aduce încă o rană. Repovestirea invită la compasiune fără a scuza ceea ce urmează.',
    'Creatura se apropie de William Frankenstein, sperând că un copil se va teme mai puțin, dar și William o respinge. Furioasă, îl ucide și plantează dovezi împotriva lui Justine. Capitolul ține împreună ambele laturi ale problemei morale: respingerea ajută la înțelegerea furiei creaturii, dar crima și învinuirea unei femei nevinovate rămân greșite. Pe ghețar, își înfruntă creatorul pentru abandon și îi cere o tovarășă. Victor acceptă, lăsând deschisă întrebarea dacă o a doua creație poate îndrepta primul său eșec.',
    'Citește integral al doilea capitol',
    'Răzbunare și regret',
    'Victor călătorește în Anglia și apoi pe o insulă scoțiană îndepărtată pentru a crea ființa promisă. Înainte s-o termine, se teme de urmările existenței unei alte ființe independente și distruge lucrarea neterminată. Prima lui creație îl vede încălcându-și promisiunea și jură să fie prezentă în noaptea nunții sale. Prudența târzie a lui Victor oprește al doilea experiment, dar nu-i repară relația cu creatura și nici nu-i apără pe cei din jur.',
    'Creatura îl ucide pe Henry Clerval, prietenul lui Victor, iar Victor este acuzat pentru scurt timp. El se căsătorește cu Elizabeth în ciuda amenințării; creatura o ucide. Tatăl lui Victor moare de durere. Urmărirea străbate apoi Europa până în Arctica. Victor îi istorisește viața sa exploratorului Robert Walton și îi cere să distrugă creatura. Curând după moartea lui Victor, creatura apare, vorbește despre remușcare și arată că și creatorul ei poartă vină. Plănuiește să dispară în Arctica și să moară.',
    'Narațiunea comică asemuiește adesea acest șir de pierderi cu divertismentul popular, dar tiparul de dedesubt este sumbru. Fiecare act de răzbunare sporește distrugerea. Creatorul și creatura iau fiecare decizii dăunătoare, iar niciunul nu poate readuce viețile pierdute. Întâlnirea lor finală nu îngăduie o împărțire simplă între om nevinovat și monstru rău.',
    'Citește integral al treilea capitol',
    'Ce ne întreabă încă povestea',
    'Capitolul final dezvoltă temele repovestirii. Ambiția științifică neînfrânată a lui Victor arată pericolul căutării puterii fără grijă pentru ceilalți. Singurătatea creaturii întreabă dacă umanitatea se măsoară prin înfățișare sau prin capacitatea de a simți, a învăța și a căuta apropiere. Abandonul lui Victor și violența creaturii fac din responsabilitate o întrebare comună, dar inegală: înțelegerea unei răni nu justifică orice răspuns la ea.',
    'Cartea compară romanul lui Shelley cu povești ulterioare despre experimente și creații care scapă de sub controlul creatorilor. Leagă aceste întrebări și de inteligența artificială și ingineria genetică. Acestea sunt analogii și provocări etice, nu afirmații că tehnologiile de azi sunt literalmente ființe vii. Dacă oamenii creează sisteme cu efecte ample, povestea le cere să se gândească la consecințe înainte și după momentul invenției.',
    'Umorul este poarta de intrare a cărții. Referințele la televiziune, cultura populară, proasta creștere a copiilor și deciziile uimitor de neinspirate ale lui Victor fac un roman gotic mai accesibil. Râsul revine mereu la o cerință serioasă: nu confunda capacitatea de a crea cu pregătirea de a îngriji ceea ce ai creat. Cititorul care caută întreaga interpretare comică a cărții poate începe cu primul experiment al lui Victor și poate urmări cum se dezvoltă această întrebare în fiecare capitol.',
    'Citește integral al patrulea capitol',
]
assert len(translations) == len(data['segments']), (len(translations), len(data['segments']))
for segment, translation in zip(data['segments'], translations):
    segment['translation'] = translation
path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')
