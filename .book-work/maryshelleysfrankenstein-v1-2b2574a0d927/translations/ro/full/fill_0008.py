import json
from pathlib import Path

path = Path(__file__).parent / 'chunks/0008.json'
data = json.loads(path.read_text())
translations = [
    "În cele din urmă, Victor rămâne izolat în Arctica, aproape de moarte. Este salvat de Robert Walton, căpitanul unei nave, a cărui expediție a fost întreruptă când a văzut un om straniu și distrus rătăcind prin pustiul de gheață. Fascinat, Walton ascultă povestea tragică pe care Victor i-o spune de la început: creația, abandonul, morțile și vina neîncetată. Victor știe că viața lui se apropie de sfârșit, dar păstrează o ultimă speranță: dacă el moare înainte de a-și împlini scopul, Walton va continua urmărirea și va ucide creatura.",
    "În ciuda stării disperate, setea de răzbunare a lui Victor nu s-a stins. Îl avertizează pe Walton despre primejdiile ambiției neînfrânate, dar vorbele lui sună ca reflecțiile amare ale unui om care a pierdut totul. Sfatul este umbrit de propriile eșecuri și de neputința lui de a vedea urmările faptelor sale până când a fost prea târziu.",
    "În ultimele zile ale vieții, sănătatea lui Victor se înrăutățește. Moare la bordul navei lui Walton, încă chinuit de creatura pe care a făcut-o și de viețile pe care aceasta le-a luat. Este un sfârșit sumbru și tragic pentru omul care voia să învingă moartea, dar a devenit victima ei.",
    "După moartea lui Victor, creatura apare pentru ultima oară. Urcă pe navă și stă deasupra trupului său, cu un amestec ciudat de tristețe și triumf. Pe deplin conștientă acum de distrugerea provocată, îi vorbește lui Walton cu melancolie. Recunoaște durerea pricinuită altora, dar și pe cea îndurată de ea însăși. Dezvăluie că plănuise dintotdeauna să moară după Victor, ca să scape de mizeria existenței și să pună capăt suferinței amândurora.",
    "Apoi ființa dispare în sălbăticia înghețată, lăsându-i pe Walton și echipaj cu povestea tulburătoare a unui om care a îndrăznit să sfideze ordinea firească a vieții. Istoria lui Victor Frankenstein și a creaturii sale este un avertisment: ambiția fără responsabilitate și cunoașterea fără înțelepciune pot duce la distrugeri de necuprins.",
    "Astfel, povestea tragică din «Frankenstein» ajunge la încheierea amară, iar creatorul și creația își întâlnesc sfârșitul inevitabil. Căutarea măreției se termină în ruină, iar întrebările ridicate de experimentul lui Victor dăinuie după ultima pagină: ce înseamnă să creezi viață? Și ce responsabilități vin odată cu o asemenea putere?",
    "În cele din urmă, nici Victor, nici creatura nu pot scăpa de urmările propriilor alegeri; destinele lor rămân împletite într-o poveste despre ambiție, răzbunare și, mai presus de toate, pierdere.",
    "Cuvinte de încheiere",
    "Când închidem ultimele pagini din «Frankenstein», povestea lui Victor și a creaturii sale rămâne cu noi nu doar ca o istorie gotică de groază, ci ca o narațiune profund umană despre ambiție, responsabilitate și urmările împingerii limitelor cunoașterii. Deși Mary Shelley a scris romanul în 1818, temele lui centrale rămân surprinzător de actuale, mai ales într-o lume în care tehnologia, inteligența artificială și descoperirile științifice ne obligă să luăm în seamă implicațiile etice ale propriilor creații.",
    "În miezul său, «Frankenstein» vorbește despre primejdiile ambiției neînfrânate. Victor Frankenstein, împins de dorința de a dezlega tainele vieții, își abandonează răspunderea de creator și declanșează un șir de tragedii. Faptul că nu se gândește la urmările faptelor sale, creând viață fără să se întrebe cum o va îngriji, este un avertisment puternic și pentru secolul XXI. Pe măsură ce dezvoltăm tehnologii care pot schimba radical viața, prin inteligență artificială, inginerie genetică sau automatizare, romanul lui Shelley ne amintește de nevoia de prevedere, responsabilitate și modestie.",
]
assert len(data['segments']) == len(translations)
for segment, translation in zip(data['segments'], translations):
    segment['translation'] = translation
path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')
