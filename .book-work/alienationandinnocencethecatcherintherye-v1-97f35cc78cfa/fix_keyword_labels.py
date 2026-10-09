import json
from pathlib import Path
p=Path('tools/keyword-translations.generated.json');d=json.loads(p.read_text());t=d['translations']
fix={
'alienation':{'pl':'wyobcowanie'},
'phoniness':{'fr':'fausseté','de':'Verlogenheit','es':'falsedad','ro':'falsitate'},
'adult institutions':{'fr':'institutions du monde adulte','de':'Institutionen der Erwachsenenwelt','es':'instituciones del mundo adulto','pt':'instituições do mundo adulto','it':'istituzioni del mondo adulto','ro':'instituțiile lumii adulte','pl':'instytucje świata dorosłych'},
'feeling misunderstood':{'fr':'sentiment d’être incompris','de':'Gefühl des Unverstandenseins','es':'sentirse incomprendido','pt':'sentir-se incompreendido','it':'sentirsi incompresi','ro':'sentimentul de a fi neînțeles','pl':'poczucie niezrozumienia'},
'human contact':{'ro':'contact uman'},
'pencey prep':{'fr':'Pencey Prep','de':'Pencey Prep','es':'Pencey Prep','pt':'Pencey Prep','it':'Pencey Prep','ro':'Pencey Prep','pl':'Pencey Prep'},
'hollywood work':{'fr':'travail à Hollywood','de':'Arbeit in Hollywood','es':'trabajo en Hollywood','pt':'trabalho em Hollywood','it':'lavoro a Hollywood','ro':'munca la Hollywood','pl':'praca w Hollywood'},
'football game':{'es':'partido de fútbol','ro':'meci de fotbal','pl':'mecz futbolowy'},
'mr. spencer':{'fr':'M. Spencer','de':'Herr Spencer','es':'señor Spencer','pt':'Sr. Spencer','it':'signor Spencer','ro':'domnul Spencer','pl':'pan Spencer'},
'harsh judgment':{'ro':'judecată aspră','it':'giudizio aspro'},
'sally hayes':{'fr':'Sally Hayes','de':'Sally Hayes','es':'Sally Hayes','pt':'Sally Hayes','it':'Sally Hayes','ro':'Sally Hayes','pl':'Sally Hayes'},
'sunny':{'fr':'Sunny','de':'Sunny','es':'Sunny','pt':'Sunny','it':'Sunny','ro':'Sunny','pl':'Sunny'},
'ordinary awkwardness':{'ro':'stângăcie obișnuită','es':'torpeza cotidiana','pt':'constrangimento comum','it':'imbarazzo ordinario'},
'carl luce':{'fr':'Carl Luce','de':'Carl Luce','es':'Carl Luce','pt':'Carl Luce','it':'Carl Luce','ro':'Carl Luce','pl':'Carl Luce'},
'childhood and adult responsibility':{'fr':'enfance et responsabilité adulte','de':'Kindheit und Verantwortung der Erwachsenen','es':'infancia y responsabilidad adulta','pt':'infância e responsabilidade adulta','it':'infanzia e responsabilità adulta','ro':'copilărie și responsabilitate adultă','pl':'dzieciństwo i odpowiedzialność dorosłych'},
'rejecting compromise':{'es':'rechazar los compromisos'},
'children at play':{'fr':'enfants qui jouent','de':'spielende Kinder','es':'niños jugando','pt':'crianças brincando','it':'bambini che giocano','ro':'copii la joacă','pl':'bawiące się dzieci'},
'field of rye':{'de':'Roggenfeld','ro':'lan de secară'},
'children playing':{'ro':'copii care se joacă'},
'phoebe':{'fr':'Phoebe','de':'Phoebe','es':'Phoebe','pt':'Phoebe','it':'Phoebe','ro':'Phoebe','pl':'Phoebe'},
'central park carousel':{'fr':'carrousel de Central Park','de':'Karussell im Central Park','es':'carrusel de Central Park','pt':'carrossel do Central Park','it':'giostra di Central Park','ro':'caruselul din Central Park','pl':'karuzela w Central Parku'},
'misunderstood':{'pl':'niezrozumiany'},
'contempt':{'fr':'mépris','es':'desprecio'},
'adult responsibility':{'fr':'responsabilité adulte','de':'Verantwortung im Erwachsenenalter','es':'responsabilidad adulta','pt':'responsabilidade adulta','it':'responsabilità adulta','ro':'responsabilitatea maturității','pl':'odpowiedzialność dorosłych'},
'displays':{'fr':'expositions du musée','de':'Museumsvitrinen','es':'vitrinas del museo','pt':'exposições do museu','it':'esposizioni del museo','ro':'exponate de muzeu','pl':'eksponaty muzealne'},
'conformity':{'de':'Konformität','pl':'konformizm'},
'protecting':{'ro':'ocrotire'},
'city of disappearing dreams':{'ro':'orașul visurilor care dispar'},
'dream of saving innocence':{'ro':'visul de a salva inocența'},
'preserve innocence':{'ro':'păstrarea inocenței'},
'unfiltered struggle':{'ro':'luptă nefiltrată'},
}
for phrase,localized in fix.items():
 for lang,label in localized.items():
  assert phrase in t[lang],(lang,phrase)
  t[lang][phrase]=label
p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
