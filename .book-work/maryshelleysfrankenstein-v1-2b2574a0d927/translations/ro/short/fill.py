import json
from pathlib import Path

path = Path(__file__).parent / 'chunks/0001.json'
data = json.loads(path.read_text())
translations = [
    "Frankenstein de Mary Shelley — Lectură de zece minute",
    "Frankenstein de Mary Shelley",
    "Lectură de zece minute · 2024",
    "Creație și responsabilitate",
    "Acest eseu repovestește cu umor romanul lui Mary Shelley",
    "Frankenstein",
    "păstrând în centru problema sa morală. Victor Frankenstein descoperă cum să creeze viață, dar prima lui reacție față de ființa vie este groaza și abandonul. Creatura trebuie să afle ce este și cum să supraviețuiască fără grija creatorului. Conflictul lor transformă un triumf științific într-o poveste despre responsabilitate, respingere și răzbunare. Cartea leagă întrebările lui Shelley de inteligența artificială și biotehnologie, întrebând ce le datorează creatorii ființelor pe care le aduc pe lume.",
    "Citește introducerea integrală",
    "Visul primejdios al lui Victor",
    "Victor crește la Geneva, fascinat de forțele naturii și de scrierile alchimice vechi. La Universitatea din Ingolstadt, curiozitatea lui devine o obsesie pentru granița dintre viață și moarte. Se izolează de familie și prieteni, adună materialele pentru un corp omenesc și lucrează până când experimentul reușește. Rezultatul îl îngrozește însă. În loc să se întrebe cum să apere sau să învețe ființa creată, Victor fuge. Capitolul arată că ambiția științifică nu poate fi despărțită de grija pe care el refuză să o ofere.",
    "Citește capitolul integral",
    "O creatură care vrea să aparțină",
    "După ce Victor o abandonează, creatura întâlnește o lume care îi judecă înfățișarea înainte de a-i asculta vocea. Urmărește în taină o familie, învață limba și obiceiurile oamenilor și speră că înțelegerea îi va câștiga un loc printre ei. Respingerea îi transformă însă singurătatea în furie. Când Victor află că fratele lui mai mic, William, a fost ucis, iar Justine este învinuită, tăcerea lui adaugă o nouă nedreptate celei dintâi. Creatura îi cere lui Victor un tovarăș care să-i împărtășească izolarea. Întâlnirea lor întreabă dacă monstruozitatea stă în înfățișare, în fapte dăunătoare sau în refuzul de a recunoaște nevoia altei ființe de grijă.",
    "Citește capitolul integral",
    "Promisiunea unui tovarăș",
    "Victor acceptă să facă o a doua creatură, apoi se teme de ceea ce ar putea însemna o nouă viață. Promisiunea lui se amestecă cu vina pentru prima creație și cu neliniștea față de urmări pe care nu le poate controla. Departe de casă, începe munca, dar o distruge înainte ca ființa să prindă viață. Creatura vede în asta o a doua trădare și promite să fie alături de Victor în noaptea nunții. Capitolul transformă responsabilitatea științifică într-o alegere făcută sub stăpânirea fricii: Victor cântărește posibilele rele, dar lasă din nou creatura fără răspuns la singurătatea ei.",
    "Citește capitolul integral",
    "Urmărirea și judecata finală",
    "Victor înțelege greșit amenințarea creaturii și se pregătește să se apere la nuntă. Elizabeth devine victima. Durerea îl trimite apoi pe Victor în urmărirea creaturii prin Europa și până în Arctica, iar această goană îi consumă restul vieții. Creatura supraviețuiește creatorului, dar răzbunarea nu i-a adus nici tovărășie, nici pace. Întâlnirea lor finală nu lasă un învingător simplu. Șirul pierderilor a început printr-un act de creație, însă fiecare alegere ulterioară l-a adâncit.",
    "Citește capitolul integral",
    "De ce avertismentul dăinuie",
    "Eseul încheie revenind la ambiție, empatie și îndatoririle care însoțesc noile cunoștințe. Experimentul lui Victor arată că a face viață nu este același lucru cu a-ți asuma răspunderea pentru ea. Excluderea creaturii arată cât de repede frica se poate transforma în cruzime de ambele părți. Romanul lui Shelley, așa cum este citit aici, rămâne un mod de a discuta urmările etice ale tehnologiilor puternice fără a uita oamenii afectați de ele.",
    "Citește reflecțiile finale",
]
assert len(data['segments']) == len(translations)
for segment, translation in zip(data['segments'], translations):
    segment['translation'] = translation
path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')
