import json
from pathlib import Path

path=Path(__file__).parent/'chunks/0001.json'
data=json.loads(path.read_text())
translations=[
 'Viziunea lui Dostoievski asupra moralității: Crimă și pedeapsă — Ediția de zece minute',
 'Viziunea lui Dostoievski asupra moralității: Crimă și pedeapsă',
 'Ediția de zece minute',
 'Această repovestire a romanului',
 'Crimă și pedeapsă',
 'de Fiodor Dostoievski îl urmărește pe Rodion Raskolnikov de la teoria oamenilor excepționali la crimă, vinovăție, mărturisire și o posibilă renaștere morală. Întrebarea centrală este dacă un argument intelectual poate așeza pe cineva mai presus de legea morală. Cele patru capitole alternează întâmplările exterioare cu schimbările din mintea lui Raskolnikov. Sărăcia și căldura apăsătoare din Sankt Petersburg oferă conflictului un cadru fizic.',
 'O minte pe marginea prăpastiei',
 'Raskolnikov este un fost student care trăiește într-o sărăcie grea la Sankt Petersburg. A adoptat o teorie potrivit căreia oamenii extraordinari pot încălca hotarele morale pentru un bine mai mare. Ideea îi măgulește dorința de a se ridica deasupra neînsemnătății. Își îndreaptă furia spre Aliona Ivanovna, o cămătăreasă despre care crede că exploatează clienții disperați. Își imaginează că ar ucide-o, i-ar lua averea, i-ar ajuta pe săraci și ar dovedi că el însuși face parte dintre cei extraordinari.',
 'Primul capitol urmărește justificările lui fără să le primească drept adevăr. Raskolnikov pregătește o vizită la casa de amanet a Alionei, oferind un ceas și câteva mărunțișuri în timp ce își ascunde intenția. Oferta ei mică îl umilește și îi întărește ura. Totuși pleacă fără s-o atace. Între luminile străzii și prăvălie, omorul plănuit rămâne o alegere, iar groaza lui arată cât de nesigură este deja teoria sa încrezătoare.',
 'Citește integral primul capitol',
 'O lovitură calculată, o faptă disperată',
 'Înarmat cu un topor, Raskolnikov se întoarce în clădirea Alionei. Scările și vecinii fac ca fiecare zgomot să pară amenințător, dar planul atent îl duce până la ușa ei. O ucide pe cămătăreasă când aceasta îi întoarce spatele. Lizaveta, sora ei nevinovată, intră pe neașteptate și vede scena. În panică, o ucide și pe ea. Al doilea omor distruge ficțiunea unui gest precis făcut pentru un scop superior: a murit cineva pe care nici nu intenționa să-l atace.',
 'Raskolnikov caută lucruri de preț, dar monedele și mărunțișurile par neînsemnate pe lângă ce a făcut. Fuge din apartament și ascunde obiectele furate în camera sa fără să se gândească la valoarea lor. Capitolul privește omorurile atât ca fapte fizice, cât și ca o cădere morală. Eliberarea de sărăcie pe care și-o închipuise este înlocuită de frică, confuzie și primele apăsări ale vinei. Fuga din clădire nu îl poate elibera de crimă.',
 'Citește integral al doilea capitol',
 'Povara conștiinței',
 'În dimineața următoare, Raskolnikov speră că omorurile au fost un coșmar. În schimb, amintirile revin: sângele, chipul Lizavetei și certitudinea că a trecut un hotar moral. Teoria sa despre oamenii extraordinari nu mai sună ca o explicație sigură. Se teme că va fi descoperit la fiecare bătaie în ușă și la fiecare pas, își închipuie martori pretutindeni și nu poate dormi. Străzile obișnuite devin ostile, fiindcă fiecare chip pare capabil să-l dea de gol.',
 'Capitolul arată vinovăția prin febră, paranoia și izolare, nu doar o numește. Raskolnikov își spune că deține încă controlul, în timp ce gândurile îi amestecă realitatea și închipuirea. Străzile aglomerate și căldura apăsătoare a Sankt Petersburgului îi oglindesc sufocarea. Narațiunea îl așază mereu pe cititor înlăuntrul fricii sale. La sfârșit, certitudinea filosofică a lăsat locul unei conștiințe captive în consecințele propriilor fapte.',
 'Citește integral al treilea capitol',
 'Căință și renaștere morală',
 'Familia lui Raskolnikov și prietenul său Razumihin îi simt izolarea, dar nu reușesc să se apropie de el. Sonia Semyonovna Marmeladov, care își întreține familia prin prostituție, îi ascultă teoriile și îi arată milă. Credința și suferința ei o deosebesc de raționamentul detașat cu care el justificase omorul. Este atras de ea, dar se teme să recunoască atât crima, cât și propria vulnerabilitate.',
 'În camera Soniei, el spune în cele din urmă că le-a ucis pe Aliona și Lizaveta. Ea îl îndeamnă să mărturisească public și să caute iertarea. Repovestirea prezintă dorința lui de a accepta pedeapsa ca pe un drum spre împăcare, nu ca pe o ștergere a victimelor. Raskolnikov merge la secția de poliție și mărturisește în fața anchetatorului Porfiri Petrovici. Sfârșitul ține împreună tragedia și speranța: nu poate anula niciuna dintre crime, dar poate înceta să se ascundă și poate începe un drum nesigur al ispășirii.',
 'Concluzia leagă această poveste psihologică de dezbateri despre relativismul moral, izolare și izbăvire. Cea mai puternică afirmație a cărții este una trăită: teoria lui Raskolnikov promitea libertate, dar punerea ei în faptă l-a legat de vinovăție. Mila Soniei îi oferă un alt mod de a înfrunta suferința și responsabilitatea. Cititorii pot reveni la repovestirea completă pentru a urmări fiecare pas al conflictului.',
 'Citește integral al patrulea capitol',
]
assert len(translations)==len(data['segments']),(len(translations),len(data['segments']))
for segment,translation in zip(data['segments'],translations):segment['translation']=translation
path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
