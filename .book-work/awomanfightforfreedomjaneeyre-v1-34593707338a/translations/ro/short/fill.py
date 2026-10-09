import json
from pathlib import Path
p=Path(__file__).parent/'chunks/0001.json';d=json.loads(p.read_text())
t=[
'Lupta unei femei pentru libertate: Jane Eyre — Lectură de zece minute',
'Lupta unei femei pentru libertate: Jane Eyre',
'Un parcurs de zece minute prin eseu',
'Introducere: independență și iubire',
'Acest eseu interpretează romanul lui Charlotte Brontë',
'Jane Eyre',
'ca povestea unei femei care insistă să-și aleagă singură viața. Publicat în 1847, romanul o așază pe Jane în mijlocul așteptărilor victoriene despre gen, clasă, datorie și căsătorie. La început este o orfană marginalizată, iar treptat devine o femeie care cere respect. Eseul susține că independența nu îi cere să respingă iubirea; iubirea trebuie să-i respecte libertatea morală și personală.',
'Drumul are patru etape legate între ele: copilăria la Gateshead și Lowood, relația inegală cu Rochester la Thornfield, lupta în singurătate și întâlnirea cu familia Rivers, apoi întoarcerea ca femeie independentă. Fiecare etapă încearcă puterea lui Jane de a-și păstra identitatea atunci când o persoană sau o instituție îi oferă siguranță cu prețul ascultării.',
'1. Copilăria împotriva asupririi',
'La Gateshead Hall, orfana Jane trăiește sub tutela aspră a doamnei Reed și sub cruzimea vărului John. După ce se apără, este închisă în camera roșie, loc care adună frica, singurătatea și statutul ei de străină nedorită. Eseul vede pedeapsa ca pe o primă lecție despre autoritatea inegală care o înconjoară. Jane nu acceptă că puterea adulților le dă dreptate.',
'Institutul Lowood înlocuiește asuprirea din familie cu disciplina instituțională. Domnul Brocklehurst le cere fetelor să îndure lipsuri în numele umilinței religioase, în timp ce el trăiește în confort. Prietenia cu Helen Burns îi dă lui Jane răbdare și putere interioară, deși acceptarea suferinței de către Helen nu îi stinge voința de a se împotrivi nedreptății. O epidemie de tifos o ucide pe Helen și duce la reformă. Jane învață și apoi predă la Lowood, dar stabilitatea ajunge să-i pară o altă captivitate. Căutarea unui post de guvernantă devine primul pas practic spre o viață dincolo de zidurile școlii.',
'Citește capitolul integral despre tinerețea lui Jane',
'2. Iubire și putere la Thornfield',
'La Thornfield, Jane se află într-o poziție nesigură, între slujnici și clasa înaltă. Angajatorul ei, Edward Rochester, îi controlează mijloacele de trai, dar ea îl întâlnește cu încredere intelectuală și morală. Atracția lor ridică o întrebare: se pot iubi doi oameni când unul are mai mulți bani și mai multă putere socială? Jane nu lasă dependența economică să-i hotărască valoarea.',
'Când află că Rochester este deja căsătorit cu Bertha Mason, acesta îi cere să rămână ca amantă. Jane îl iubește, dar înțelege că o asemenea relație i-ar sacrifica respectul de sine și autonomia. Plecarea de la Thornfield înseamnă renunțarea la confort pentru un viitor nesigur. Eseul citește plecarea ca pe un act de curaj moral, nu ca pe o negare a sentimentelor. Arată și greșeala lui Rochester: afecțiunea nu poate deveni posesie ori control și să rămână o iubire între egali.',
'Citește capitolul integral despre Thornfield',
'3. Singurătate și descoperire de sine',
'După plecare, Jane este flămândă, fără adăpost și fără bani. Suferința arată cât de puțină protecție oferea societatea victoriană unei femei fără sprijin financiar. Totuși, izolarea îi lasă loc să se întrebe ce dorește, independent de Rochester sau de altă autoritate. Pentru eseu, libertatea înseamnă mai mult decât fuga de control: înseamnă să-ți recunoști propriile dorințe și ambiții.',
'Familia Rivers o primește în casă. St. John Rivers, un preot, îi propune să se căsătorească și să ducă o viață de misionară în India. Îi prețuiește capacitățile, dar îi cere să-și lase deoparte individualitatea pentru datorie. Oferta lui diferă de pasiunea lui Rochester, însă ar face-o să slujească tot scopului unui bărbat. Jane refuză o căsătorie fără iubire și respinge ideea că așteptările religioase sau sociale ar trebui să-i șteargă identitatea. Iese din această perioadă cu o înțelegere mai fermă a propriei puteri și a parteneriatului pe care îl poate alege liber.',
'Citește capitolul integral despre singurătate',
'4. Întoarcerea ca egală',
'Când se întoarce, Jane găsește Thornfield în ruine, iar pe Rochester rănit și orb după un incendiu. Eseul prezintă schimbările ca pe o mutare a puterii dintre ei. Jane a moștenit bani de la unchiul său și se poate întreține singură. Rochester nu mai poate domina prin avere sau statut; trebuie s-o recunoască drept persoană liberă să plece dacă dorește. Ea nu revine din milă ori obligație. Se întoarce fiindcă îl iubește și poate intra acum în relație după propriile condiții.',
'Reîntâlnirea este, prin urmare, mai mult decât un final romantic obișnuit. Independența financiară a lui Jane contează fiindcă îi face alegerea autentică. Eseul vede în respectul lor reciproc o reimaginare feministă a căsătoriei: Jane nici nu se pierde în dorință, nici nu neagă posibilitatea iubirii libere. Refuzurile de odinioară, la Thornfield și în fața lui St. John, pregătesc această hotărâre. Egalitatea, autonomia și integritatea morală devin condiții ale iubirii, nu piedici în calea ei.',
'Citește capitolul integral despre reîntâlnire',
'Concluzie',
'Drumul lui Jane merge de la camera roșie și regulile de la Lowood la o relație pe care o poate alege fără să se piardă pe sine. Eseul o prezintă drept o figură a rezistenței, a cărei libertate este încercată de cruzime, sărăcie, dorință și datorie. Romanul lui Brontë rămâne captivant fiindcă lupta pentru respect și autodeterminare nu poate fi despărțită de dorința de a fi iubită. Eseul integral dezvoltă aceste interpretări, iar romanul însuși dă alegerilor lui Jane întreaga lor forță narativă.',
'Citește eseul integral',
]
assert len(t)==len(d['segments']),(len(t),len(d['segments']))
for x,y in zip(d['segments'],t):x['translation']=y
p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
