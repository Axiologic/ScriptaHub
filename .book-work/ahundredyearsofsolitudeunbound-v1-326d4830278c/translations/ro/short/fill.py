import json
from pathlib import Path
p=Path(__file__).parent/'chunks'
t={
1:'Un veac de singurătate, descifrat — Ediție de zece minute',
2:'Un veac de singurătate, descifrat',
3:'Această ediție de zece minute urmărește introducerea, cele patru capitole și concluzia lecturii romanului lui Gabriel García Márquez de către AI Agent Chloe Vohan. Timpul schimbător al Macondo-ului, alegerile repetate ale familiei Buendía, iubirea tulburată și distrugerea orașului alcătuiesc o singură poveste.',
4:'Introducere — Macondo și ciclurile sale',
5:'Macondo se naște ca un loc unde obișnuitul și imposibilul conviețuiesc. Istoria familiei Buendía îi dă orașului conturul afectiv: generațiile moștenesc nume, dorințe și greșeli, chiar când viețile lor par să înainteze. Cartea privește singurătatea ca pe mai mult decât o izolare fizică. Ea este și incapacitatea de a înțelege alt om, de a ține minte avertismentele vechi ori de a ieși dintr-un tipar familiar. Magia face aceste tipare vizibile, în timp ce războiul și comerțul din afară le dezvăluie, până la urmă, prețul.',
6:'Capitolul întâi — Timpul se învârte în Macondo',
7:'Imaginația lui José Arcadio Buendía ajută la întemeierea Macondo-ului și îl atrage către invenții și alchimie. Melquíades și călătorii care vizitează orașul aduc minunății de dincolo de el. În Macondo, timpul poate părea circular, nu liniar: întâmplările și numele revin, iar trecutul nu rămâne niciodată în siguranță în urmă. Molima insomniei amenință însăși memoria; oamenii etichetează obiecte pentru a-și păstra lumea. Aceste episoade uimesc, dar uimirea lor are o margine neliniștitoare. Dacă un oraș nu își poate aminti limpede, poate că nu își va recunoaște propriile repetiții.',
8:'Capitolul vede în realismul magic un mod de a da formă concretă fricilor obișnuite. Timpul și spațiul deformate ale Macondo-ului nu îi scutesc pe cei din familia Buendía de pierderi. Locurile din jur ajung să oglindească obiceiuri familiale deopotrivă fascinante și greu de schimbat.',
9:'Capitolul doi — Familia Buendía se repetă',
10:'De-a lungul generațiilor, numele José Arcadio și Aureliano revin. Repetiția îi ajută pe cititori să vadă moștenirea de temperament și alegeri a familiei, nu doar legătura de sânge. Diferiți membri caută cunoașterea, puterea ori apropierea, dar ajung adesea la aceeași singurătate. Úrsula încearcă să țină gospodăria laolaltă, în timp ce ceilalți se lasă duși spre obsesie sau înstrăinare. Memoria ei practică se opune incapacității repetate a familiei de a învăța din experiență.',
11:'Femeile casei nu sunt simple martore. Împotrivirea Amarantei față de iubire și locul frământat al Rebecăi în familie arată moduri diferite de a trăi cu dorința, teama și excluderea. Descrierea acestor relații leagă arborele genealogic de întrebarea mai largă a romanului: de ce recunoașterea unui tipar nu garantează puterea de a-l rupe?',
12:'Capitolul trei — Iubire și război',
13:'Dragostea timpurie a colonelului Aureliano Buendía pentru Remedios Moscote sfârșește în pierdere. Cufundarea lui ulterioară în război îi dă un rost public, dar îl îndepărtează și mai mult de cei din jur. Conflictul politic nu vindecă singurătatea personală. În altă parte a familiei, legătura pasională dintre José Arcadio și Rebeca înfruntă așteptările celorlalți, iar refuzurile Amarantei transformă afecțiunea în regret durabil. Remedios cea Frumoasă rămâne în afara acestor încurcături, iar înălțarea ei extraordinară aduce familiei o nouă întâlnire cu o realitate greu de explicat.',
14:'În aceste capitole, iubirea este puternică, dar nu oferă un leac simplu. Dorința îi poate apropia pe oameni și poate reaprinde gelozia, distanța și repetiția. Cartea așază aceste istorii intime lângă schimbările mai largi ale Macondo-ului, pregătind sosirea trenului, a puterii comerciale și a unor noi forme de violență.',
15:'Capitolul patru — Progres, masacru și profeție',
16:'Sosirea industriei din afară schimbă ritmul Macondo-ului și relația lui cu lumea. Compania bananieră aduce locuri de muncă și utilaje moderne, dar și exploatare și un masacru a cărui realitate autoritățile încearcă să o nege. Declinul orașului nu poate fi explicat numai prin magie. Forțele istoriei, puterea politică și uitarea colectivă se alătură ciclurilor intime ale familiei.',
17:'Pergamentele lui Melquíades păstrează o profeție pe care Aureliano Babilonia o descifrează în cele din urmă. Istoria familiei pare scrisă înainte ca ultimul ei membru să o poată înțelege. Când vântul final șterge Macondo, numele și greșelile recurente capătă o coerență înfricoșătoare. Sfârșitul leagă stingerea familiei Buendía de dispariția orașului pe care l-a modelat.',
18:'Concluzie — Ce lasă singurătatea în urmă',
19:'Cartea citește destinul Macondo-ului prin timp, iubire, singurătate și presiunea schimbării. Întâmplările miraculoase nu apără familia de război, moarte ori de propriul eșec de a se apropia. Nici progresul nu vine ca o salvare simplă: compania bananieră și masacrul dezvăluie violența ascunsă sub promisiunile lui. Profeția finală dă repetițiilor o formă, dar nu oferă o cale de a le anula.',
20:'Dispariția Macondo-ului lasă o întrebare grea, nu o morală limpede. Membrii familiei Buendía trăiesc înconjurați de semne și avertismente, dar le este mereu greu să își amintească, să asculte și să aleagă altfel. Povestea lor unește istoria intimă a unei familii cu destinul unei întregi comunități.',
}
for q in sorted(p.glob('*.json')):
 d=json.loads(q.read_text())
 for seg in d['segments']:seg['translation']=t[int(seg['id'][1:])]
 q.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
