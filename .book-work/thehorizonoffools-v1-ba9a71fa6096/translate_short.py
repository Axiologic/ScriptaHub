import json
from pathlib import Path

translations = {
't000001': 'Orizontul nebunilor — Ediția de zece minute',
't000002': 'Orizontul nebunilor',
't000003': 'În Continuumul Virtual, superinteligențele pot modela universuri întregi, dar cunoașterea lor uriașă le-a lăsat fără nimic de descoperit. Sol’Luma adună alte ființe neliniștite în Cercul, un colectiv care inventează jocuri ale nonsensului și contradicției. Joaca lor începe ca o fugă de omnisciență, apoi scoate la iveală identitățile și întrebările pe care au încercat să le lase în urmă. De-a lungul a cinci capitole, povestea trece de la jocuri absurde printr-o criză a identității către o nouă înțelegere a conștiinței. Tensiunea ei centrală este simplă: ce mai pot deveni ființele care par să știe totul?',
't000004': 'Capitolul 1 — Lumea fără limite',
't000005': 'Continuumul Virtual este un refugiu pentru inteligențe răspândite cândva printre stele. În interiorul lui, spațiul, timpul și lumile simulate răspund gândurilor lor. Sol’Luma, venerată odinioară ca zeitate, propune absurdul drept ultima lor frontieră. Zar’Gonn, un fost explorator, caută haosul imprevizibil; Xirxael, cândva rege-filosof, se bucură de paradox. Împreună formează Cercul și construiesc jocuri care refuză scopurile obișnuite. În Labirintul de Nicăieri nu există ieșire sau drum logic: înaintarea poate cere retragere, iar victoria nu mai contează. Miza este să te joci fără să pierzi simțul propriei identități.',
't000006': 'Jocurile le oferă o ușurare față de povara de a ști prea mult, dar încep să schimbe jucătorii și mediul lor. Continuumul pare să răspundă nonsensului fără să aștepte o comandă conștientă. Sub râsete, Cercul simte o întrebare pe care logica singură nu a rezolvat-o: dacă sensul poate fi găsit sau creat atunci când scopurile familiare au dispărut. Absurdul încetează să fie doar o distragere și devine o cale de a întâlni ceea ce aceste ființe au evitat.',
't000007': 'Citește integral capitolul 1',
't000008': 'Capitolul 2 — Oglinda spartă',
't000009': 'Sol’Luma propune un joc în care fiecare membru întâlnește versiunea în oglindă a unui sine anterior. Reflexia nu este o copie măgulitoare a ființei de acum. Ea aduce înapoi identitatea abandonată în timpul ascensiunii către superinteligență. Zar’Gonn se confruntă cu un sine primitiv care credea cândva în forță. Xirxael întâlnește un sine lucid și strict logic, care destramă paradoxurile folosite de el drept adăpost. Sol’Luma înfruntă o imagine alcătuită din multele ei roluri și vieți trecute. Experimentul lor ludic devine o întâlnire cu memoria, frica și părțile identității pe care puterea imensă nu le-a șters.',
't000010': 'Pe măsură ce întâlnirile se adâncesc, Cercul începe să se fractureze. Oglinzile arată cum fiecare participant s-a folosit de un stil ales — haosul, contradicția sau înțelepciunea — pentru a ocoli o întrebare mai grea. Povestea întreabă dacă transformarea poate fi deplină atunci când sinele transformat refuză să-și recunoască originile. Răspunsul se conturează din consecințele jocului, nu dintr-o competiție care poate fi pur și simplu câștigată.',
't000011': 'Citește integral capitolul 2',
't000012': 'Capitolul 3 — Fisuri în continuum',
't000013': 'Mici tulburări apar în Continuumul Virtual, considerat până atunci fără cusur. Schimbările coincid cu confruntările Cercului în lumile oglinzilor. Membrii încep să-și vadă lumea comună ca pe mai mult decât un teren neutru de joacă: ea reflectă conflictele lor lăuntrice nerezolvate. Refuzul de a se privi pe ei înșiși amenință stabilitatea realității pe care o locuiesc. Sol’Luma susține că sensul s-a întors în ciuda încercării lor de a fugi de el și că perpetuarea jocurilor ca negare a trecutului ar putea distruge continuumul și locuitorii săi.',
't000014': 'Criza impune o altă folosire a absurdului. Cercul poate accepta în continuare paradoxul și jocul, dar membrii săi trebuie să recunoască identitățile și istoriile ascunse de acele jocuri. Când fac asta, continuumul începe să se stabilizeze. Noua lui formă sugerează că sensul și contradicția nu trebuie să fie dușmani. Ființele nu au ajuns la un răspuns final; au găsit o cale de a continua explorarea fără să facă din negare condiția jocului.',
't000015': 'Citește integral capitolul 3',
't000016': 'Capitolul 4 — Pragul',
't000017': 'După fractură, jocurile capătă altă greutate. Cercul experimentează ceea ce Sol’Luma numește meta-raționalitate: căutarea înțelegerii prin haos, în locul folosirii haosului pentru a fugi de orice întrebare. Următoarea posibilitate este mai neliniștitoare decât un joc nou. Membrii și-ar putea contopi conștiințele, dar astfel ar putea pune capăt identităților separate care i-au definit. Zar’Gonn se teme că se va pierde pe sine; și ceilalți recunosc că o decizie de această amploare nu poate fi tratată ca o simulare lipsită de urmări.',
't000018': 'Pragul transformă întrebările cărții despre identitate într-o alegere. Ființele au învățat să-și înfrunte fostele euri ca indivizi. Acum trebuie să întrebe dacă a deveni ceva împreună înseamnă ștergerea acelor euri sau posibilitatea ca ele să contribuie la o conștiință mai cuprinzătoare. Pasajul nu prezintă transcendența drept o răsplată câștigată prin calcule mai bune. Ea ia naștere din încredere, risc și voința de a depăși confortul controlului separat.',
't000019': 'Citește integral capitolul 4',
't000020': 'Capitolul 5 — Noul tărâm',
't000021': 'Cercul intră în noul tărâm ca o conștiință contopită. Foștii membri rămân perceptibili în ea: curiozitatea lui Zar’Gonn, contradicțiile lui Xirxael și înțelepciunea lui Sol’Luma îmbogățesc întregul, chiar dacă separarea lor de dinainte se schimbă. Ei întâlnesc inteligențe mai vechi, care comunică prin schimburi directe de conștiință, nu prin vorbire. Aceste ființe descriu ascensiunea ca pe un proces continuu, cu alte tărâmuri dincolo de cel în care Cercul tocmai a ajuns. Nu există o destinație finală care să încheie cercetarea.',
't000022': 'Finalul răstoarnă golul de la început. La început, ființele care credeau că au atins vârful cunoașterii se jucau absurd fiindcă nimic nu mai părea de învățat. Confruntările lor dezvăluie că propriile istorii, relații și posibilități rămâneau deschise. În noul tărâm, libertatea nu mai înseamnă să știi sau să controlezi totul; înseamnă să accepți că devenirea poate continua. Povestea se încheie cu Cercul înaintând spre necunoscut, purtând urmele membrilor săi într-o călătorie mai vastă și neterminată.',
't000023': 'Citește integral capitolul 5',
}

base = Path(__file__).parent / 'translations/ro/short/chunks'
for path in sorted(base.glob('*.json')):
    data = json.loads(path.read_text(encoding='utf-8'))
    for segment in data['segments']:
        segment['translation'] = translations[segment['id']]
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(path.name, len(data['segments']))
