import json
from pathlib import Path

path=Path(__file__).parent/'chunks/0003.json'
data=json.loads(path.read_text())
translations=[
 'Într-o seară, pe când stăteau împreună în camera ei modestă, Raskolnikov a simțit un impuls copleșitor de a mărturisi. Cuvintele îi atârnau greu pe limbă, dar frica îl ținea în loc. Se temea nu doar de urmările mărturisirii, ci și de vulnerabilitatea pe care și-ar fi arătat-o. Sonia i-a simțit lupta lăuntrică și l-a îndemnat cu blândețe să spună adevărul. „Nu trebuie să te ascunzi de păcatele tale”, i-a spus ea. „Numai mărturisind poți găsi pacea.”',
 'Cuvintele ei au răsunat adânc în el, aprinzând o licărire de speranță în întunericul care îl învăluia. Raskolnikov a început să înțeleagă că adevărata izbăvire putea veni numai prin recunoașterea vinei și acceptarea pedepsei. Gândul îl îngrozea; se convinsese de mult că este mai presus de o asemenea judecată morală. Totuși, credința neclintită a Soniei în mila lui Dumnezeu a început să-i înmoaie apărarea.',
 'Zilele au devenit săptămâni, iar Raskolnikov oscila între disperare și scurte clipe de limpezime. Se întorcea mereu cu gândul la locul crimei și retrăia fiecare detaliu — atingerea toporului în mână, tăcerea înfiorătoare de după faptă și sângele care îi păta nu doar mâinile, ci și sufletul. Fiecare amintire îi întețea suferința; nu mai putea nega că nu era doar un ucigaș, ci un om care se desprinsese de ceilalți oameni.',
 'Punctul de cotitură a venit într-o noapte, după o zi grea, plină de paranoia și groază, când Raskolnikov a rămas singur cu Sonia. A privit-o în ochi — ochi care păreau plini de o milă fără sfârșit — și a simțit nevoia copleșitoare de a-și descărca întreaga povară. „Eu le-am ucis”, a mărturisit în cele din urmă, cuvintele rostogolindu-se ca niște pietre de pe inima lui.',
 'Sonia a reacționat pe loc; nu s-a dat înapoi și nu a arătat groază, ci s-a apropiat cu blândețe. „Atunci trebuie să mărturisești”, a spus încet, cu lacrimi în ochi. „Trebuie să cauți iertarea.” În clipa aceea, Raskolnikov a fost cuprins de un val de emoții — ușurare amestecată cu frică, ca și cum s-ar fi rupt un zăgaz înlăuntrul lui.',
 'Copleșit de emoție și, pentru prima dată de la crimă, de limpezime, Raskolnikov a înțeles că adevărata eliberare nu stătea în fuga de pedeapsă, ci în primirea ei ca drum spre izbăvire. A priceput că suferința nu era doar o piedică de evitat, ci o călătorie necesară către renașterea spirituală.',
 'A doua zi a marcat o schimbare în viața lui Raskolnikov: a pornit spre secția de poliție, un loc de care se temuse multă vreme, dar pe care acum îl vedea ca pe un adăpost pentru sufletul său tulburat. Fiecare pas părea însemnat; nu mergea doar spre închisoare, ci spre eliberarea de lanțurile vinovăției care îl ținuseră captiv.',
 'Intrând în secție, neliniștea i-a străbătut trupul ca un curent electric; fiecare privire părea să-l cerceteze de parcă i-ar fi văzut până în adâncul sufletului. Și totuși, în mijlocul fricii se afla o pace neașteptată — își dădea seama că, înfruntând adevărul, începea în sfârșit să-și ia destinul în mâini.',
 'Când l-a întâlnit pe Porfiri Petrovici, anchetatorul perspicace care îl observase în tăcere de-a lungul încercării sale, Raskolnikov a simțit o stranie apropiere, nu dușmănie. Înțelegerea pătrunzătoare a firii omenești pe care o avea Porfiri găsea ecou în propriile lupte lăuntrice ale lui Raskolnikov; amândoi căutau o cale prin apele tulburi ale moralei și consecințelor.',
 '„Mărturisesc”, a rostit în sfârșit Raskolnikov, simțind cum o mare povară i se ridică de pe umeri. Cuvintele au răsunat în încăpere ca un clopot care vestea un nou început, nu un sfârșit.',
 'În acea clipă a mărturisirii se aflau deopotrivă tragedia și speranța — recunoașterea că îl aștepta pedeapsa, dar și posibilitatea izbăvirii prin suferință și iubire. Stând înaintea lui Porfiri și sub privirea neclintită a Soniei, plină de credință și milă, Raskolnikov a înțeles că nu era doar un sfârșit, ci o transformare adâncă — o renaștere morală născută din acceptare și iubire.',
 'Astfel a început drumul lui Raskolnikov spre ispășire — un drum plin de încercări, dar luminat de o nouă limpezime și de un țel: el căuta nu doar iertarea societății, ci și împăcarea cu sine și cu cei ale căror vieți le schimbase pentru totdeauna.',
 'CONCLUZIE',
 'Romanul rămâne actual, fiindcă abordează dezbaterile filosofice despre moralitate într-o lume în care relativismul și subiectivitatea domină adesea. Opera lui Dostoievski critică puternic aceste idei și arată că încălcarea normelor morale are urmări psihologice și spirituale profunde. Cercetarea izolării, disperării și izbăvirii vorbește cititorilor de azi care se confruntă cu provocări existențiale și legate de sănătatea mintală.',
 'BIBLIOGRAFIE',
 'Dostoievski, Fiodor. Crimă și pedeapsă.',
 'Bloom, Harold, editor. Fyodor Dostoevsky’s Crime and Punishment: Bloom’s Modern Critical Interpretations.',
]
assert len(translations)==len(data['segments']),(len(translations),len(data['segments']))
for segment,translation in zip(data['segments'],translations):segment['translation']=translation
path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
