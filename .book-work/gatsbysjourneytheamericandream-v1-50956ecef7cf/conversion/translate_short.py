import json
from pathlib import Path
w=Path(__file__).resolve().parents[1];base=w/'translations/ro/short/chunks'
values=[
"Drumul lui Gatsby: visul american demascat — Ediția de zece minute",
"Drumul lui Gatsby: visul american demascat",
"Ediția de zece minute",
"Acest eseu însoțitor al romanului lui F. Scott Fitzgerald",
"Marele Gatsby",
"povestește evenimente importante și finalul romanului. Cititorii care vor să evite dezvăluirile ar trebui să citească mai întâi romanul. Cele patru capitole urmăresc căutarea lui Daisy Buchanan de către Gatsby, averea care îl face vizibil, dar nu acceptat, excesele anilor 1920 și prețul unui vis clădit pe un trecut idealizat.",
"Introducere: prețul unui vis",
"Jay Gatsby pare să aibă avere, un conac măreț și admirația străinilor. Totuși, viața lui se organizează în jurul unei speranțe pe care banii nu o pot împlini: recâștigarea lui Daisy. Introducerea prezintă visul american deopotrivă ca promisiune și capcană. Gatsby crede că succesul îi poate remodela identitatea și recupera o relație pierdută. Nick Carraway observă spectacolul, dar vede și fragilitatea de dedesubt. Eseul întreabă dacă urmărirea unui ideal justifică sacrificiile făcute pe drum.",
"Capitolul întâi: bani și apartenență",
"Primul capitol îl examinează pe Gatsby ca om care s-a ridicat singur și pare să dovedească faptul că efortul aduce prosperitate. Petrecerile, conacul și mașina îi etalează succesul, dar nu îi oferă trecutul social al cercului lui Tom Buchanan. Averea moștenită a lui Tom aparține unei elite vechi care refuză să îl socotească pe Gatsby egalul ei. Eseul deosebește posesia banilor de acceptarea în rândul celor care i-au moștenit. Această barieră face din visul lui Gatsby mai mult decât o poveste de dragoste: este și o luptă pentru clasă și statut.",
"Daisy, acum soția lui Tom, stă în centrul idealului lui Gatsby. El își imaginează că destulă avere și devotament vor reface iubirea tinereții. Dar Daisy s-a schimbat, iar confortul o leagă de lumea lui Tom. Încrederea lui Gatsby în muncă și bani ascunde faptul că trecutul nu poate fi răscumpărat. Capitolul îi prezintă ambiția ca emoționantă, dar atașată fatal de o iluzie.",
"Capitolul doi: strălucitorii ani 1920",
"Al doilea capitol citește petrecerile aglomerate ale lui Gatsby ca emblemă a anilor nebuni. Jazzul, dansul, Prohibiția, barurile ascunse și averile noi creează o atmosferă de libertate și exces. Oaspeții se bucură de ospitalitatea lui, dar abia îl cunosc. Nick, naratorul, observă distanța dintre strălucirea publică și singurătatea privată. Când Gatsby are nevoie de ajutor, lumea socială atrasă de bogăția lui îi oferă prea puțină loialitate.",
"Eseul îi așază pe Daisy și Tom în această cultură a aparențelor. Averea veche îi dă lui Tom siguranță și putere; banii noi îl fac pe Gatsby vizibil, dar suspect. Daisy pare modernă, însă rămâne atașată de siguranța căsătoriei și a clasei sale. Mașina galbenă a lui Gatsby, asemenea conacului, anunță succesul, dar ascunde golul de sub etalare. Capitolul susține că prosperitatea materială nu poate crea singură prietenie, iubire sau profunzime morală.",
"Capitolul trei: Daisy și trecutul imaginat",
"Gatsby s-a îndrăgostit de Daisy înainte de a avea avere. După plecarea la război, a găsit-o căsătorită cu Tom. Apoi a făcut din bogăție și spectacol un plan pentru a o recâștiga. Capitolul al treilea susține că Gatsby iubește o Daisy idealizată la fel de mult ca femeia reală. Pentru el, ea reprezintă acceptarea, viața perfectă și dovada că își poate depăși originile. Refuză avertismentul lui Nick că trecutul nu poate fi pur și simplu repetat.",
"Daisy nu este nici premiul imaginat de Gatsby, nici dispusă să renunțe la siguranța cunoscută. Obligată să aleagă, rămâne cu Tom. Visul lui Gatsby depinde de transformarea ei într-o figură din amintirile lui, nu de persoana care este. Eseul leagă această eroare de visul american mai larg: credința că efortul poate aduce orice rezultat dorit poate ascunde limite pe care banii nu le pot șterge.",
"Capitolul patru: prăbușire și urmări",
"Tom îl înfruntă pe Gatsby cu privire la originea averii lui, inclusiv contrabanda cu alcool. Daisy se retrage, dar Gatsby așteaptă în fața casei ei, convins că îl va alege. Mai târziu, Daisy conduce mașina lui Gatsby și o ucide pe Myrtle Wilson. Gatsby își asumă vina. Tom îl face pe George, soțul lui Myrtle, să creadă că Gatsby era la volan; George îl ucide pe Gatsby, apoi se sinucide. Eseul prezintă devotamentul lui Gatsby ca emoționant și distrugător deopotrivă, fiindcă îl împiedică să vadă limpede alegerea lui Daisy.",
"Aproape niciunul dintre oaspeții petrecerilor lui Gatsby nu vine la înmormântare. Nick trebuie să o organizeze, dezvăluind cât de puțin le păsa mulțimilor de gazda lor. Concluzia revine la prăpastia dintre aparență și realitate: averea lui Gatsby putea înscena apartenența, dar nu putea cumpăra iubirea, repara timpul sau depăși clasa moștenită. Hotărârea lui este, într-un sens, admirabilă, însă devine distrugătoare când urmărește o versiune imposibilă a trecutului. Eseul îi invită pe cititori să își cerceteze propriile ambiții și să recunoască momentul în care un vis a devenit iluzie.",
"Citește pasajele corespunzătoare din ediția completă",
"Introducere: prețul unui vis",
"Capitolul întâi: bani și apartenență",
"Capitolul doi: anii nebuni",
"Capitolul trei: Daisy și Gatsby",
"Capitolul patru: prăbușirea",
"Concluzie",
]
segs=[]
for f in sorted(base.glob('*.json')):segs.extend(json.loads(f.read_text())['segments'])
assert len(segs)==len(values),(len(segs),len(values))
lookup=dict(zip((s['id'] for s in segs),values))
for f in sorted(base.glob('*.json')):
 d=json.loads(f.read_text())
 for s in d['segments']:s['translation']=lookup[s['id']]
 f.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
print(len(values),'short segments translated')
