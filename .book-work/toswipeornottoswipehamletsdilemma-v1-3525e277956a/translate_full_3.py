import json
from pathlib import Path
p=Path('.book-work/toswipeornottoswipehamletsdilemma-v1-3525e277956a/translations/ro/full/chunks/0003.json')
d=json.loads(p.read_text())
t=[
"Să nu-l uităm pe adevăratul maestru al marketingului din Elsinore: Polonius. Omul înțelesese puterea brandului personal înainte să fie la modă. «Fii credincios ție însuți»? Mai degrabă «Fii credincios propriului brand». Polonius nu dădea doar sfaturi, ci lansa sloganuri. Dacă LinkedIn ar fi existat în Danemarca medievală, sigur ar fi postat zilnic citate inspiraționale și s-ar fi lăudat cu modestie cu stilul său de «lider care îi slujește pe ceilalți».",
"Desigur, nu putem vorbi despre mașinăria de relații publice din Elsinore fără cuplul de putere inițial: Claudius și Gertrude. Cei doi înțelegeau importanța unui front unit. Poate că la mijloc au fost puțină trădare și un fratricid, dar să le apreciem devotamentul față de povestea «familiei recompuse și fericite». Nu este crimă; este «despărțire conștientă» dusă până la consecința ei logică.",
"Știu ce gândiți: «Dar, profesore, nu interpretați prea mult? Shakespeare sigur nu se gândea la gestionarea brandurilor când a scris Hamlet!» Dragul meu student, ai văzut câte piese a scris omul? Shakespeare nu era doar dramaturg, ci o mașină de produs conținut. Teatrul Globe nu era teatru; era primul spațiu de coworking din lume.",
"Luați piesa din interiorul piesei. Îi spunem «Capcana de șoareci», dar, să fim sinceri, e echivalentul medieval al unei aluzii răutăcioase postate online. Hamlet nu încearcă doar să «prindă conștiința regelui», ci să devină viral. Dacă ar fi avut TikTok, spectacolul ar fi fost un dans de trei minute pe muzica «Tată ucis: verificat».",
"Poate însă că geniul de marketing al lui Hamlet nu stă în personaje, ci în piesa însăși. Shakespeare a luat o poveste clasică despre răzbunare și a transformat-o într-o meditație în cinci acte despre natura existenței. Asta nu este doar scriere, ci vânzare de opțiuni suplimentare. Ne-a promis povestea simplă «ucide-l pe cel rău» și ne-a oferit echivalentul teatral al unei diplome în filosofie. Asta da depășire a așteptărilor clientului!",
"La urma urmei, poate adevărata nebunie a lui Hamlet nu stă în purtarea sa, ci în refuzul de a se dedica pe deplin brandului personal. Într-un moment este fiul îndurerat, în următorul ucigașul cu sânge rece. Hotărăște-te, Hamlet! În lumea nemiloasă a politicii de curte, un mesaj de brand consecvent este esențial.",
"Așa că, data viitoare când urmărești Hamlet și te întrebi de ce nu-l înjunghie odată pe Claudius, amintește-ți: nu destinația contează, ci călătoria. Mai exact, conținutul pe care îl produci pe parcurs. La ce bun o răzbunare dacă nu scoți din ea câteva monologuri reușite?",
"În concluzie, era Hamlet nebun, un geniu al marketingului sau doar un om care avea nevoie disperată de o echipă bună de relații publice? Ca la orice brand mare, poate răspunsul depinde de privitor. Un lucru e sigur: în jocul tronurilor, fie câștigi, fie mori; dacă ești Hamlet, le faci pe amândouă și rămâi totuși imaginea orelor de literatură engleză pentru generații întregi.",
"Asta numesc eu un brand de durată.",
"Capitolul al treilea — Hamletonomia: economia răzbunării",
"Bine ați revenit, stimați cercetători ai poznelor shakespeariene! E timpul să ne punem pălăriile de economiști (sugerez un tricorn șic) și să pătrundem în lumea fascinantă a hamletonomiei. Da, explorăm cum criza existențială a unui prinț a devenit un boom economic pentru Danemarca. Cine ar fi crezut că răzbunarea poate fi atât de profitabilă?",
"Să începem cu elementele de bază: tatăl lui Hamlet a murit, unchiul său este rege, iar PIB-ul Danemarcei e pe cale să explodeze. Cum, întrebați? Simplu: răzbunarea este o industrie în creștere.",
"Mai întâi, cursa înarmării. Interesul brusc al lui Hamlet pentru scrimă nu e doar un hobby; stimulează economia locală. Gândiți-vă câte săbii, pumnale și cupe cu otravă plasate convenabil trebuie fabricate. Numai Laertes probabil ținea ocupată o întreagă breaslă de fierari, cerând spade tot mai ascuțite. Este echivalentul medieval al complexului militar-industrial, iar afacerile înfloresc!"
]
assert len(t)==len(d['segments']),(len(t),len(d['segments']))
for x,v in zip(d['segments'],t):x['translation']=v
p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
