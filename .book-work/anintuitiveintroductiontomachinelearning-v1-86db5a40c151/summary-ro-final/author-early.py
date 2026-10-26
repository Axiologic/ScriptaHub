import json
from pathlib import Path
root=Path(__file__).parent
entries={
1: ('Învățarea automată poate fi înțeleasă pornind de la bucla ghicește, măsoară, ajustează, cu limitele fiecărei metafore explicate.', 'Prefața stabilește publicul, metoda intuitivă și traseul cărții; cuprinsul nu intră în selecția de idei.', [
 ('Bucla predicție, eroare și ajustare unește majoritatea metodelor, fără să descrie toate metodele.',[133,134],.99,.8,'bucla'),
 ('Metaforele cotidiene preced vocabularul tehnic și trebuie abandonate unde încetează să explice.',[137,147],.85,.8,'metafore')], [('Reglarea unui cache oferă o intrare concretă în mecanismul învățării.',[131,134])], [('Vecinii nu au aceeași buclă de antrenare; nicio analogie nu este identitate.',[133,147])]),
2: ('Calitatea învățării depinde de exemple, etichete și evaluare separată, nu doar de algoritm.', 'Fundamentul întregii cărți: probleme, ținte, date și generalizare.', [
 ('Supervizarea învață o funcție din exemple etichetate, iar alegerea loss-ului exprimă costurile umane ale erorilor.',[155,158,165,168,169,170],1,.8,'obiectiv'),
 ('Clustering-ul și reducerea dimensionalității propun structură, fără să certifice că grupurile au semnificație.',[177,179,182,184,185,186],.85,.7,'structură'),
 ('Antrenarea, validarea și testarea au roluri distincte; ajustarea după test consumă independența măsurii.',[190,192,193,194,195],.99,.8,'evaluare'),
 ('Datele temporale cer testare pe viitorul simulat, iar schimbarea lumii cere monitorizare.',[197,198],.9,.7,'derivă')], [('Farfuria albă poate deveni un indiciu fals; etichetele flaky pot reproduce graba echipei.',[160,172,173])], [('Regulile exacte rămân preferabile când problema le permite; gruparea produce ipoteze.',[159,186])]),
3: ('Metodele clasice fac compromisuri diferite între presupuneri, interpretabilitate, instabilitate și cost.', 'Prezintă repertoriul de bază și motivul alegerii lui pe date tabelare.', [
 ('Regresia liniară minimizează erori pătratice, iar regresia logistică transformă un scor în probabilitate ce necesită verificarea calibrării.',[205,206,209,211],.85,.6,'modele-clasice'),
 ('Vecinii folosesc exemplele păstrate, cu cost și sensibilitate la scară și dimensionalitate.',[220,221,223,224],.8,.6,'vecini'),
 ('Arborii aleg împărțiri locale informative și pot memora; pădurile reduc variația prin diversitate, boosting-ul corectează succesiv erorile.',[232,235,236,243,245,249,251],.95,.8,'ansambluri'),
 ('SVM, Bayes și procesele gaussiene oferă alte presupuneri și alte raporturi între precizie, încredere și calcul.',[256,257,258,259,260],.7,.6,'alte-metode')], [('Rigla și arcurile explică sensibilitatea la puncte extreme; editarea succesivă explică boosting-ul.',[203,206,248,249])], [('Corelația nu arată cauza; erorile comune ale datelor nu se anulează prin agregare.',[214,252])]),
4: ('Rețelele învață reprezentări intermediare prin compunerea de operații neliniare și ajustarea ponderilor cu gradientul.', 'Face trecerea de la metode clasice la arhitecturi care construiesc trăsături.', [
 ('Un singur neuron are limite geometrice; straturile și activările neliniare extind ce poate reprezenta rețeaua.',[275,276,278,279],.95,.75,'compoziție'),
 ('Gradient descent schimbă ponderile, iar backpropagation calculează contribuțiile locale prin regula lanțului.',[285,286,289,290,293],1,.8,'învățare'),
 ('Convoluțiile folosesc filtre învățate și ponderi partajate pentru structura locală a imaginilor.',[301,302,303],.85,.7,'arhitectură'),
 ('Recurența comprimă trecutul într-o stare fixă; porțile ajută memoria fără să elimine toate limitele secvențiale.',[310,311,313,314,316],.8,.7,'memorie')], [('Muntele în ceață și inspectorul din atelier separă direcția ajustării de atribuirea erorii.',[283,284,289,291])], [('Rețeaua poate învăța zăpada în locul lupului; datele trebuie să rupă corelațiile accidentale.',[305])]),
5: ('Un model este aritmetică organizată în tensori; pregătirea și reprezentarea datelor îi fixează posibilitățile.', 'Deschide mecanismul fizic și clarifică ce înseamnă importanța unei trăsături.', [
 ('Neuronul artificial este o operație numerică, nu o celulă biologică, iar metafora creierului poate induce așteptări greșite.',[324,325,328,329,330],.9,.8,'aritmetică'),
 ('Curățarea, codificarea, scalarea și construcția trăsăturilor sunt parte a modelului practic; pașii ajustați din date văd numai antrenarea.',[337,338,340,341,342,344,345,346],1,.8,'date'),
 ('Tensorii au forme, straturile fac produse de matrice, iar loturile și GPU-urile exploatează calcule paralele.',[351,352,353,355,356,357,358],.95,.8,'calcul'),
 ('Importanța depinde de model, scară și corelații; permutarea măsoară dependența predicției fără să demonstreze cauzalitate.',[366,367,368,369,371,372],.85,.8,'interpretare')], [('Fișierul de ponderi al detectorului de suduri conține grile numerice, iar cuantizarea le reduce precizia și memoria.',[349,351,360])], [('Feature-urile corelate pot împărți arbitrar meritul; cuantizarea cere retestare.',[366,368,360])]),
6: ('Trimiterea la mecanismul de atenție leagă dependența de intrare de discuția despre importanță.', 'Segment final scurt de legătură din capitolul despre materialul modelului.', [
 ('Atenția diferă de ponderile fixe ale unui scor: fiecare caz influențează unde se citește.',[373],.5,.5,'atenție')], [('Trimiterile leagă embeddings, temperatura și attention de capitolul despre limbaj.',[373])], [('Acest segment este o legătură, nu o dovadă suplimentară pentru o capacitate.',[373])]),
8: ('Arhitecturile exprimă presupuneri despre date, iar costurile trebuie judecate separat pentru antrenare și inferență.', 'Leagă piesele rețelelor, economia utilizării și memoria vectorială alternativă.', [
 ('Normalizarea și conexiunile reziduale susțin antrenarea; dropout-ul combate dependențele fragile.',[380,381,382,384,385],.9,.7,'arhitectură'),
 ('Antrenarea actualizează ponderile și păstrează gradient și stări; inferența execută modelul cu ponderile fixate.',[392,393,394,395,397,399],.95,.8,'două-vieți'),
 ('Arhitecturile vectorial-simbolice compun și recuperează informații prin bundling și binding fără aceeași buclă de gradient.',[404,405,407,408,409,412,414,415],.85,.95,'memorie-vectorială'),
 ('Curbele de învățare disting foamea de date de capacitatea insuficientă, iar calitatea și acoperirea sunt esențiale.',[421,422,423,424,425],.95,.8,'scară')], [('Restaurantul separă pregătirea rețetelor de servire; vectorii pot ține perechi cheie-valoare.',[390,392,409])], [('Vectorii aleatorii nu descoperă singuri semnificații în date brute; scaling laws nu garantează abilități.',[414,415,424])]),
9: ('Scalarea are limite empirice și costuri pe durata utilizării, iar mai multe date cer selecție și verificare.', 'Încheie dimensiunea economică și critică a capitolului despre construirea modelelor.', [
 ('Optimul costului de antrenare poate diferi de optimul servirii, iar legile de scalare nu promit salturi de capacitate.',[426],.9,.8,'scară'),
 ('Datele sintetice sunt mai utile când rezultatele pot fi verificate; repetarea ieșirilor modelelor poate îngusta distribuția.',[427],.85,.8,'date-sintetice'),
 ('Necesitatea concretă se măsoară prin curba proprie de învățare și acoperirea cazurilor dificile.',[429],.9,.7,'măsurare')], [('Exemplele de cost separă cheltuiala unei antrenări de suma cererilor de inferență.',[428])], [('Estimările de resurse au incertitudine, iar regularitățile empirice pot înceta să se păstreze.',[426,427,428])]),
10: ('Teoriile creierului propun învățare prin predicție, mișcare, sisteme de referință și memorii complementare, fără să fie o explicație finală.', 'Interludiu care arată atât inspirațiile posibile, cât și limitele analogiei cu rețelele.', [
 ('Thousand Brains propune modele de obiecte în coloane și consens între observații parțiale, dar ipotezele rămân disputate.',[435,438,439,442,443,445],.8,.95,'creier'),
 ('Procesarea predictivă descrie predicții descendente și erori ascendente; paralela cu modelele de limbaj are limite.',[450,452,454],.8,.85,'predicție'),
 ('Învățarea locală și sistemele de memorie rapidă/lentă oferă alte contraste cu optimizarea globală și învățarea înghețată.',[455,456,457,458],.85,.85,'învățare-continuă')], [('Cana recunoscută prin atingere și oprirea zumzetului frigiderului explică ideile de hartă și surpriză.',[433,434,448,449])], [('Nici Thousand Brains, nici procesarea predictivă nu sunt teorii definitive și nici nu coincid peste tot.',[445,458])])
}
# The only unit in batch 0007 is the concluding cross-reference.
entries[7]=entries.pop(6)
entries[6]=entries.pop(5)
entries[5]=entries.pop(4)
entries[4]=('Les méthodes complémentaires élargissent les hypothèses, mais leurs sorties exigent toujours un jugement humain.', 'Încheierea trusei clasice: alternative de grupare și învățare cu etichete limitate.', [('DBSCAN și gruparea ierarhică schimbă modul de a delimita grupuri; hărțile t-SNE și UMAP pot deforma distanțe și insule.',[261,262],.7,.65,'structură'),('Supervizarea slabă și semi-supervizată folosesc etichete imperfecte sau puține, cu risc de întărire a erorilor.',[263],.75,.7,'supervizare'),('Reponderarea și reeșantionarea ajută clasele rare și cer recalibrarea probabilităților.',[264],.8,.7,'evaluare')], [('Festivalul văzut de sus explică gruparea după densitate.',[261])], [('Setările pot crea grupuri artificiale, iar clasele rare distorsionează încrederea după reeșantionare.',[261,262,264])])
entries[4]=('Metodele complementare extind presupunerile, dar rezultatele cer în continuare judecată umană.', *entries[4][1:])
for number,(thesis,role,ideas,evidence,qualifications) in entries.items():
 batch=json.loads((root/'batches'/f'batch-{number:04d}.json').read_text())
 def ids(values): return [f'u{x:06d}' for x in values]
 result={'batch':batch['batch'],'chapterId':batch['chapterId'],'segment':batch['segment'],'thesis':thesis,'role':role,'ideas':[{'id':f'batch-{number:04d}-idea-{i:03d}','statement':t,'centrality':c,'originality':o,'recurrenceCandidate':r,'sourceUnitIds':ids(refs)} for i,(t,refs,c,o,r) in enumerate(ideas,1)],'evidenceAndExamples':[{'statement':t,'sourceUnitIds':ids(refs)} for t,refs in evidence],'objectionsAndQualifications':[{'statement':t,'sourceUnitIds':ids(refs)} for t,refs in qualifications],'audit':{'chapterCovered':True,'meaningPreserved':True,'factsPreserved':True,'notes':'Analiză LLM a întregului segment; cuprinsul și trimiterile de navigare nu sunt tratate drept argumente.'}}
 (root/'analyses'/batch['batch']).write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
