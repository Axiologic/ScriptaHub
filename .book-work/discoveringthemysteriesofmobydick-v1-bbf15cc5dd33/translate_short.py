from pathlib import Path
import json
p=Path('.book-work/discoveringthemysteriesofmobydick-v1-bbf15cc5dd33/translations/ro/short/chunks/0001.json')
d=json.loads(p.read_text())
t=[
'Descoperind misterele din Moby Dick — Ediția de zece minute',
'Descoperind misterele din Moby Dick',
'Această explorare concisă citește ',
'Moby-Dick',
' prin căutarea sensului de către Ishmael, urmărirea mistuitoare a balenei albe de către Ahab și lupta echipajului cu marea. Întrebarea centrală este dacă ambiția îi ajută pe oameni să înfrunte necunoscutul sau îi orbește față de viețile celor de lângă ei. Cartea pornește de la chemarea oceanului, trece prin obsesie și furtuni și se încheie cu o reflecție asupra rezistenței și autocunoașterii.',
'Chemarea mării',
'În ',
'introducerea',
', oceanul devine o imagine a incertitudinii vieții. El poate trezi curiozitatea și dorința de autocunoaștere, dar întinderea lui dezvăluie și teama și limitele omului. În ',
'capitolul întâi',
', Ishmael caută să scape de monotonia vieții obișnuite. Plecarea pe mare îi promite libertate, aventură și o cale spre înțelegerea de sine. Pe Pequod, poveștile și tovărășia celorlalți marinari îi dau sentimentul apartenenței. Aceeași călătorie îl duce însă spre un căpitan al cărui scop personal îi va domina în curând pe toți.',
'Frumusețea și primejdia acestui capitol nu pot fi despărțite. Oceanul deschide un orizont larg, apoi îi amintește lui Ishmael cât de puțin poate controla. Neliniștea tot mai mare transformă drumul exterior într-unul interior: el trebuie să cântărească bucuria descoperirii în raport cu teama de ceea ce va cere urmărirea lui Ahab.',
'Obsesia lui Ahab și prețul ei',
'În ',
'capitolul al doilea',
', căpitanul Ahab schimbă atmosfera de pe Pequod. Rana și furia sa concentrează voiajul asupra răzbunării împotriva lui Moby Dick. Echipajul este atras de voința lui puternică, dar Ishmael vede cum o întreprindere comună poate ajunge prizoniera fixației unui singur om. Loialitatea față de căpitan începe să se ciocnească de instinctul de conservare și de grija pentru ceilalți.',
'Întâlnirea cu vasul Rachel face limpede acest preț moral. Căpitanul lui cere ajutor pentru marinarii dispăruți, iar Ahab refuză, fiindcă o căutare i-ar întrerupe vânătoarea. Alegerea arată că obsesia înseamnă mai mult decât suferință privată: ea poate îngusta atenția morală până când nevoile altora nu mai contează. Respectul lui Ishmael pentru curajul lui Ahab devine inseparabil de teama de nesăbuința sa.',
'Furtuni, solidaritate și primejdie',
'Capitolul al treilea',
' îi așază pe marinari în mijlocul vremii violente. Furtunile le încearcă puterea de a acționa împreună, iar hotărârea lui Ahab le încearcă judecata. Ishmael găsește putere în munca împărtășită și în legăturile formate în primejdie. Marea reflectă atât vulnerabilitatea echipajului, cât și capacitatea lui de a rezista. Supraviețuirea unei furtuni aduce ușurare, dar nu înlătură amenințarea căutării lui Ahab.',
'Capitolul al patrulea',
' revine mai pe larg la puterea naturii. Apa liniștită lasă loc altei vijelii, iar marinarii de pe Pequod trebuie să apere corabia și să se apere unii pe alții. Poruncile lui Ahab îi pot însufleți, dar Ishmael se întreabă unde se termină curajul și începe nesăbuința. Oceanul nu devine niciodată un simplu obstacol de învins. Rămâne vast, schimbător și indiferent la planurile omului. În fața lui, marinarii își recunosc limitele și valoarea acțiunii comune.',
'Ce dezvăluie călătoria',
'În ',
'concluzie',
', cartea adună misterele recurente: de ce îl cheamă marea pe Ishmael, de ce nu poate Ahab să renunțe la vendetă și ce învață echipajul în fața unor forțe pe care nu le poate controla. Balena devine un centru al ambiției și fricii, iar voiajul întreabă ce sacrifică oamenii când urmăresc un singur sens cu orice preț. Înțelegerea durabilă a cărții ține mai puțin de stăpânirea oceanului și mai mult de recunoașterea dependenței reciproce, a alegerii morale și a solidarității fragile care face posibilă rezistența.',
]
assert len(t)==len(d['segments'])
for s,x in zip(d['segments'],t):s['translation']=x or ' '
p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
