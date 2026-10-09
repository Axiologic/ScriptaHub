from pathlib import Path
import json
p=Path('.book-work/theseekersjourneyofthealchemist-v1-f0a6f63716b2/translations/ro/short/chunks/0001.json');d=json.loads(p.read_text())
t=[
'Călătoria căutătorului din Alchimistul — Ediția de zece minute',
'Călătoria căutătorului din Alchimistul',
'Această lectură a romanului ',
'Alchimistul',
' de Paulo Coelho îl urmărește pe Santiago de la visul repetat al unui păstor la un drum prin ținuturi necunoscute. Cele patru capitole întreabă ce îi cere un vis omului care îl urmează. Aurul îl atrage pe Santiago spre piramidele egiptene, dar întâlnirile de pe drum transformă căutarea într-o lecție despre curaj, credință, iubire și schimbare.',
'Urmând visul',
'În ',
'capitolul întâi',
', Santiago visează o comoară lângă piramide. Viața familiară cu oile sale în Andaluzia îi oferă siguranță, în timp ce plecarea cere asumarea riscului. Melchisedec, regele Salemului, numește scopul mai adânc al lui Santiago „Legenda Personală” și îl îndeamnă să pornească. Santiago pleacă, dar este jefuit în Tanger. În loc să se întoarcă acasă, lucrează într-un magazin de cristal. Ideile sale îl ajută pe negustor, iar lovitura sorții devine o lecție de rezistență. Capitolul înfățișează drumul ca pe o schimbare a lui Santiago însuși, nu doar ca pe o cale spre bogăția îngropată.',
'Lecții de pe drum',
'Capitolul al doilea',
' transformă întâlnirile într-o educație spirituală. Santiago învață să citească prevestirile și să-și imagineze o limbă care leagă oamenii, vântul, stelele și deșertul. Negustorul de cristal își îmbunătățește prăvălia, dar refuză să-și urmeze vechiul vis de a merge în pelerinaj la Mecca. Alegerea lui dezvăluie teama atât de eșec, cât și de împlinire. Deșertul îi încearcă răbdarea lui Santiago în timp ce el învață să aibă încredere în proces, fără să ceară certitudine înainte de a acționa.',
'Alchimia devine o metaforă a schimbării interioare. Alchimistul îl învață că înțelepciunea trebuie trăită, nu doar adunată din cărți. Încercările îl ajută pe Santiago să se desprindă de frică și mulțumirea de sine. Legenda lui Personală este mai puțin o destinație fixă decât creșterea făcută posibilă prin urmarea ei.',
'Credință și iubire',
'Capitolul al treilea',
' întreabă ce înseamnă să crezi când drumul nu este limpede. Santiago întâlnește un englez care studiază alchimia din cărți; contrastul dintre ei așază experiența lângă cunoașterea formală. Într-o oază, o întâlnește pe Fatima. Ea îl încurajează să-și continue căutarea și arată că iubirea nu trebuie să devină posesie sau obstacol în calea creșterii. Alchimistul leagă apoi credința de acțiune: speranța singură nu îl poate duce înainte dacă nu acționează în ciuda îndoielii. Vântul, stelele, liniștea și asprimea deșertului devin semne de observat, iar încrederea lui Santiago crește prin alegeri repetate.',
'Comoara lăuntrică',
'În ',
'capitolul al patrulea',
', Santiago ajunge la piramide și recunoaște cât de mult l-a schimbat drumul. Melchisedec, negustorul de cristal, englezul, Fatima și alchimistul l-au învățat fiecare o altă parte a căutării. Apoi, niște tâlhari îi dezvăluie că adevărata comoară materială se află înapoi în Spania, sub un sicomor de lângă locul de unde a plecat. Santiago se întoarce atât cu o destinație, cât și cu o înțelegere schimbată a ei. Aurul îngropat este real, dar cartea acordă mai multă greutate înțelepciunii, curajului, încrederii și iubirii dobândite pe drum. Ideea finală este că sensul vieții se naște atât din călătorie, cât și din rezultat.',
]
assert len(t)==len(d['segments'])
for s,x in zip(d['segments'],t):s['translation']=x
p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
