import json
from pathlib import Path
p=Path('.book-work/toswipeornottoswipehamletsdilemma-v1-3525e277956a/translations/ro/full/chunks/0002.json')
d=json.loads(p.read_text())
t=[
"Să fim sinceri: dacă Hamlet ar fi student astăzi, ar fi tânărul de la filosofie care te prinde la petreceri ca să-ți vorbească despre Nietzsche. În primele cinci minute e stimulativ intelectual; din minutul șase cauți ieșirea și te întrebi dacă poți pretinde că te sună cineva.",
"Dar poate, numai poate, tocmai de aceea avem nevoie de Hamlet. Într-o lume a opiniilor grăbite și a satisfacției imediate, poate că o poveste care ne obligă să încetinim, să reflectăm și să punem întrebările mari are valoare. Chiar dacă întrebările vin în pentametru iambic și sunt însoțite de atâtea cadavre încât George R. R. Martin ar roși.",
"Așadar, mai este Hamlet relevant? Fiecare trebuie să răspundă singur. Dar dacă stai treaz noaptea, paralizat de nehotărâre, fără să știi dacă să acționezi sau să tot amâni... felicitări! S-ar putea să treci prin propriul moment hamletian. Încearcă doar să nu înjunghii pe nimeni ascuns după perdea, bine?",
"În concluzie, fie că Hamlet este o capodoperă eternă, fie că se pricepe de minune să se promoveze, un lucru e sigur: ne face pe toți să discutăm. Nu acesta este rostul artei mari? Să stârnească discuții, dezbateri și, din când în când, câte un eseu la literatura engleză?",
"Așa că, data viitoare când cineva te întreabă dacă Hamlet mai este relevant, amintește-ți: a fi relevant sau a nu fi relevant, aceasta-i întrebarea. Oare e mai nobil pentru minte să îndure praștiile și săgețile criticii literare dezlănțuite ori să ia armele împotriva unei mări de distrageri moderne...",
"La urma urmei, poate e mai simplu să le spui să citească SparkNotes. Așa ar face Hamlet.",
"Capitolul al doilea — Nebunie sau marketing?",
"Bine v-am regăsit, cititori curajoși! După ce am supraviețuit călătoriei prin relevanța discutabilă a lui Hamlet, ne îndreptăm privirea spre o chestiune cu adevărat presantă: era «nebunia» lui Hamlet prima campanie de marketing viral din lume? Țineți-vă bine: coborâm în apele tulburi ale gestionării medievale a brandurilor.",
"Imaginați-vă curtea daneză ca mediul corporatist suprem. Elsinore nu este doar un castel, ci un startup, iar Hamlet este directorul său nemulțumit, în hanorac, care tocmai a descoperit o fraudă serioasă în conturi. Ce face un prinț pus în fața unui asemenea coșmar de relații publice? Firește, simulează o cădere nervoasă!",
"Să vedem geniul strategiei lui Hamlet. Dintr-o singură mișcare (sau să spunem, dintr-un singur surtuc lăsat să cadă), prințul trece de la «tipul posac care poartă prea mult negru» la «cel mai râvnit burlac al Danemarcei: ediția artist chinuit». Deodată nu mai e doar moștenitorul tronului; este un brand. Dă-te la o parte, Kanye: Hamlet a mers ca tu să poți alerga.",
"Dar stați, vă aud protestând: comportamentul lui Hamlet era cu siguranță într-adevăr haotic! Vă întreb atunci: ați intrat pe Twitter în ultima vreme? Într-o lume în care Elon Musk își poate prăbuși cotația acțiunilor printr-un singur tweet, gesturile lui Hamlet par chiar cuminți. «Vai, sărmanul Yorick» este aproape o lecție de conținut ușor de distribuit. Dacă ar trăi acum, craniul acela ar avea propriul cont de Instagram, vă garantez.",
"Să vorbim acum despre Ofelia. Biata și dulcea Ofelia, sau, cum îi spun eu, prima influenceriță din lume. Gândiți-vă: e tânără, frumoasă și îi plac coronițele de flori atât de mult încât participanții la Coachella ar plânge de invidie. «Nebunia» ei nu este o coborâre tragică în pierderea minții, ci o estetică atent construită. Ofelia a deschis drumul pentru cottagecore.",
"Imaginați-vă profilul Ofeliei pe rețelele sociale: «Doar o fată daneză, trăind într-o lume daneză 🌸 #PutereaFlorilor #VibrațiiDeRâu #ÎnecCuStil». Sfârșitul ei tragic? Doar o cale de a-și asigura moștenirea. Nimic nu crește numărul urmăritorilor ca o dispariție misterioasă și prematură. Ofelia n-a murit; și-a schimbat doar direcția, devenind fantomă influenceriță cu normă întreagă."
]
assert len(t)==len(d['segments']),(len(t),len(d['segments']))
for x,v in zip(d['segments'],t):x['translation']=v
p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
