import json
from pathlib import Path
p=Path(__file__).parent/'chunks/0001.json';d=json.loads(p.read_text())
translations={
 't000001':'Top 15 seriale TV de acțiune de urmărit — ediția de zece minute',
 't000002':'Top 15 seriale TV de acțiune de urmărit',
 't000003':'''Ghidul cuprinde drame criminale, evadări din închisoare, intrigi politice, fantezie, conflicte istorice și mistere ale supraviețuirii. Cele cincisprezece prezentări principale introduc pe scurt situațiile și personajele, urmate de încă douăzeci și opt de titluri. Lista folosește „acțiunea” într-un sens larg: unele alegeri pun accentul pe luptă sau urmărire, iar altele creează tensiune prin putere, investigație și compromis moral.''',
 't000004':'Criminalitate, ambiție și schimbare morală',
 't000006':'''îl urmărește pe Walter White de la meseria de profesor de chimie la producția de droguri după un diagnostic de cancer. Parteneriatul său cu Jesse Pinkman devine o poveste despre bani, putere și corupție.''',
 't000008':'''urmărește transformarea treptată a lui Jimmy McGill în Saul Goodman, concentrându-se pe munca sa juridică, relații și compromisuri etice înaintea evenimentelor din''',
 't000011':'''îi plasează pe Thomas Shelby și familia sa în Birminghamul de după război, unde ambiția criminală întâlnește bande rivale și presiune politică.''',
 't000013':'''mută povestea în Los Angelesul anilor 1980 și leagă ascensiunea lui Franklin Saint în comerțul cu cocaină de urmări sociale și politice mai largi.''',
 't000015':'''îl are în centru pe Pablo Escobar, cartelurile columbiene și agenții care îi urmăresc. Fiecare prezentare pune la altă scară aceeași întrebare: ce le face oamenilor implicați urmărirea puterii?''',
 't000017':'''mută întrebarea în interiorul unei închisori de maximă siguranță, unde violența și alianțele schimbătoare organizează viața de zi cu zi.''',
 't000019':'''urmărește un analist al urmelor de sânge care ucide în secret infractori despre care crede că au scăpat de justiție. Tensiunea vine din viața sa dublă și instabilitatea morală a codului propriu.''',
 't000020':'Evadări, jafuri și urmăriri',
 't000022':'''începe cu Michael Scofield, care intră în închisoare pentru a-și elibera fratele Lincoln Burrows, condamnat pe nedrept potrivit ghidului. Planul de evadare tatuat pe corpul său întâlnește gardieni corupți și o conspirație mai amplă.''',
 't000024':'''urmărește grupul condus de Profesor în încercarea de a tipări bani la Monetăria Regală a Spaniei, în timp ce gestionează presiunea poliției și conflictele din echipă.''',
 't000026':'''îl are în centru pe fostul lunetist al pușcașilor marini Bob Lee Swagger, căruia i se înscenează o tentativă de asasinare a președintelui. El trebuie să-și dovedească nevinovăția și să descopere o conspirație politică. Aceste trei seriale pornesc de la un plan urgent, tot mai greu de controlat pe măsură ce apar adversari și interese ascunse.''',
 't000027':'Tronuri, instituții și lumi istorice',
 't000029':'''trece între familiile nobile care concurează pentru Tronul de Fier în Westeros și Essos. Supraviețuirea depinde de alianțe, rivalități și pretenții la domnie.''',
 't000031':'''aduce ambiția politică la Washington prin Frank Underwood, ale cărui manipulări și trădări îi conduc ascensiunea. Ghidul alătură dinastiile fantastice instituțiilor moderne și găsește conflict strategic în ambele.''',
 't000033':'''îl urmărește pe Ragnar Lothbrok de la războinic la rege, apoi se extinde către urmașii lui. Prezentarea pune accentul pe război, rivalități familiale și lumea culturală a cuceririlor. Împreună, aceste trei alegeri tratează acțiunea ca pe o luptă pentru autoritate, în care ambiția personală este legată de ordini politice mai mari.''',
 't000034':'Mister, observație și supraviețuire',
 't000036':'''începe după ce un accident aviatic lasă supraviețuitori pe o insulă misterioasă. Pericolele vin din mediu, de la locuitori necunoscuți și din trecutul personajelor.''',
 't000038':'''îl urmărește pe Patrick Jane, consultant în investigații care folosește observația, nu presupuse puteri paranormale, pentru a rezolva crime în timp ce îl caută pe ucigașul familiei sale. Un serial folosește misterul insulei și un grup de personaje; celălalt construiește investigațiile în jurul unui singur observator.''',
 't000039':'Ghidul se încheie cu încă douăzeci și opt de sugestii, de la',
 't000041':'și',
 't000043':'la',
 't000045':'și',
 't000047':'. Ediția integrală oferă descrierea separată, originală, a fiecărui serial principal și lista suplimentară completă.',
 't000048':'Prezentările sursă',
 't000049':'Introducere',
 't000065':'Alte sugestii',
}
for seg in d['segments']:seg['translation']=translations.get(seg['id'],seg['source'])
p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
print('translated or preserved',len(d['segments']),'custom',len(translations))
