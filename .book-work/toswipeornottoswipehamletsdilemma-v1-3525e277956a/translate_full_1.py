import json
from pathlib import Path
p=Path('.book-work/toswipeornottoswipehamletsdilemma-v1-3525e277956a/translations/ro/full/chunks/0001.json')
d=json.loads(p.read_text())
t=[
"A da swipe sau a nu da swipe: dilema lui Hamlet",
"A da swipe sau a nu da swipe: dilema lui Hamlet",
"Capitolul întâi — A fi sau a nu fi... relevant?",
"Bine ați venit, dragi cititori, într-o incursiune ireverențioasă prin încăperile venerabile ale tragediei shakespeariene! Astăzi îl luăm în vizor pe elefantul din teatru: Hamlet, prințul danez melancolic care ține reflectorul ocupat de peste patru secole. Dar mai merită el toată această atenție? Să vedem!",
"Imaginați-vă o lume în care, în loc să țină monologuri despre natura existenței, protagonistul nostru este mai preocupat de numărul urmăritorilor de pe Instagram. «Să postez sau să nu postez, aceasta-i întrebarea», cugetă Hamlet, cu degetul suspendat deasupra telefonului. Dintr-odată, cele cinci ore ale piesei nu mai par atât de greu de suportat, nu-i așa?",
"Știu ce gândiți: «Dar, profesore, Hamlet este o capodoperă eternă!» La fel este și arta rupestră, răspund eu, dar nu ne vedeți cărând bolovani ca să desenăm pe ei, nu? Adevărul e că Hamlet al nostru ar putea suferi de un caz grav de decalaj cultural.",
"Să ne gândim de ce tinerii de azi ar prefera să deruleze TikTok decât să urmărească încă o montare a lui Hamlet. Oare capacitatea lor de atenție a ajuns la nivelul unui peștișor auriu dopat cu cofeină? Posibil. Mai probabil însă, cineva care se învârte și mimează versurile ultimului hit pop li se pare mult mai apropiat decât un prinț care dezbate dacă să-și ucidă unchiul.",
"Imaginați-vă că Shakespeare ar fi scris Hamlet pentru generația Netflix. Episodul 1: moare tatăl lui Hamlet. Episodul 2: apare fantoma tatălui. Episoadele 3–8: Hamlet amână. Finalul sezonului: mor cu toții. Merită văzut dintr-o bucată? Poate că nu. Dar măcar l-ai putea urmări la viteză de 1,5 și termina într-o după-amiază.",
"Dar să fim drepți cu prințul nostru nehotărât. Poate nu e lipsit de relevanță, ci doar neînțeles. La urma urmei, criza lui existențială nu este metafora perfectă pentru încercarea de a decide ce să vezi pe Netflix? Paralizia opțiunilor, teama de alegerea greșită: deodată, «A fi sau a nu fi» nu mai sună atât de diferit de «Stranger Things sau The Crown?»",
"Să nu uităm nici plăcerea lui Hamlet de a simula nebunia. În lumea de azi, i-am spune «construirea unui brand personal». Dacă ar trăi acum, ar fi tipul acela de pe YouTube care face videoclipuri «MĂ PREFAC NEBUN (A IEȘIT PROST!) (APROAPE AM MURIT!)». Numărul abonaților ar exploda!",
"Dar aici prințul nostru poate că a înțeles ceva. Într-o epocă a personajelor atent construite pe rețelele sociale, lupta lui pentru autenticitate ne atinge surprinzător de aproape. «Fii sincer cu propriul selfie», ar spune Bardul dacă ar trăi și ar încerca disperat să rămână relevant.",
"Apropo de relevanță, să vorbim despre celebrele monologuri ale lui Hamlet. Într-o lume în care comunicarea zilnică folosește mai ales emojiuri și abrevieri, discursurile lui lungi par la fel de practice ca pana și călimara pentru trimiterea unui tweet. Vă imaginați cum și-ar exprima frământările interioare în limbajul de azi?",
"«2B sau nu 2B, asta este????»",
"«Vai, sărmanul Yorick! L-am cunoscut. #AmintiriDeJoi»",
"«E ceva putred în Danemarca. #VibrațiiProaste #AmNevoieDeVacanță»",
"Dintr-odată, lucrurile profunde par ceva mai puțin... profunde.",
"Poate că suntem totuși prea aspri cu melancolicul danez. Se confruntă cu lucruri grele: crimă, trădare, incest (totul rămâne în familie, nu?). Aceste teme sunt universale, chiar eterne. Dar eternă e și povestea unui băiat și a câinelui său, iar Old Yeller nu primește adaptări teatrale de cinci ore, nu-i așa?",
"Întrebarea adevărată este aceasta: într-o lume preocupată de schimbările climatice, frământările politice și de faptul dacă ananasul are ce căuta pe pizza, mai poate Hamlet contribui cu ceva semnificativ la conversație? Sau este doar tipul de la petrecere care nu încetează să vorbească despre anul său sabatic în Europa?"
]
assert len(t)==len(d['segments']),(len(t),len(d['segments']))
for x,v in zip(d['segments'],t):x['translation']=v
p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
