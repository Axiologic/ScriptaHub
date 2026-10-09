import json
from pathlib import Path
p=Path('.book-work/toswipeornottoswipehamletsdilemma-v1-3525e277956a/translations/ro/full/chunks/0005.json')
d=json.loads(p.read_text())
t=[
"Imaginați-vă că Hamlet nu își rostește discursul «A fi sau a nu fi» pe o scenă goală, ci în fața abonaților săi de pe YouTube. «Ce faceți, danezilor? Sunt eu, HamletPrince99, cu un nou videoclip despre criza mea existențială. Nu uitați să apreciați, să comentați și să vă abonați... la viața aceasta trecătoare.»",
"În Hamlet 2.0, prințul nu trebuie să angajeze o trupă de actori ca să prindă conștiința regelui. Nici vorbă! Îi trimite lui Claudius mesaje private cu o selecție atentă de meme-uri «Tu versus tipul despre care ți-a spus să nu-ți faci griji», avându-i în imagini pe bătrânul Hamlet și pe Claudius. Șah mat, unchi-tată.",
"Dar de ce să ne oprim aici? Să reimaginăm întreaga distribuție pentru epoca rețelelor sociale. Ofelia devine o creatoare de videoclipuri ASMR despre aranjarea florilor sub apă. Polonius e tipul care comentează «Primul!» la fiecare videoclip, apoi oferă sfaturi nesolicitate în paragrafe întregi. Iar Rosencrantz și Guildenstern? Două vedete TikTok gemene, imposibil de deosebit, faimoase pentru seria lor de farse «E asta trădare?»",
"Să vorbim despre fantoma tatălui lui Hamlet. În versiunea actualizată, nu mai trebuie să străbată meterezele; bântuie pur și simplu mențiunile lui Hamlet pe Twitter. «Unchiu tău ma omorât. Răzbunămă. #ȚeluriDeRăzbunare #AmintiriDeJoi» Ezitarea lui Hamlet capătă brusc sens. Cum să ai încredere într-o fantomă care nici măcar nu scrie corect?",
"Dar adevărata schimbare în Hamlet 2.0 este apariția telefoanelor inteligente. Dintr-odată, toate problemele prințului au soluții prin aplicații. Nu te poți hotărî? Există o aplicație. Trebuie să afli dacă unchiul tău este ucigaș? Există și pentru asta. Vrei să organizezi o lovitură de stat fără toate acele dueluri murdare? Ai ghicit: există o aplicație.",
"Imaginați-vă: în locul unui monolog lung, Hamlet deschide aplicația sa de decizii «A fi sau a nu fi». Aceasta îi pune o serie de întrebări:",
"1. Ești în prezent prinț?",
"2. S-a căsătorit unchiul tău recent cu mama ta?",
"3. Pe o scară de la 1 la 10, cât de fantomatică a fost ultima interacțiune cu tatăl tău?",
"Pe baza răspunsurilor, aplicația creează un plan de acțiune personalizat, cu un calendar al răzbunării și hashtaguri sugerate pentru cel mai mare impact pe rețelele sociale.",
"Nu putem uita scena piesei din interiorul piesei. În Hamlet 2.0 nu mai e o reprezentație teatrală, ci o provocare virală pe TikTok. «Provocarea: prinde conștiința regelui» se răspândește prin Elsinore mai repede decât poți spune «E ceva putred în Danemarca». Reacția vinovată a lui Claudius? Filmata în 4K și în tendințe în toată lumea în câteva minute.",
"Poate că latura cea mai revoluționară a lui Hamlet 2.0 este integrarea economiei muncii la cerere. De ce să depinzi de un singur gropar când poți folosi «Digr», aplicația care te pune în legătură cu profesioniști locali independenți ai săpatului de morminte? Trebuie să-ți trimită cineva mesajele în Norvegia? Scapă de bătaia de cap cu «Messengr»: e ca Uber, dar pentru diplomație internațională.",
"Să nu uităm celebra nehotărâre a lui Hamlet. În versiunea actualizată nu trebuie să oscileze cinci acte; creează un sondaj în poveștile de pe Instagram. «Să-l ucid pe Claudius? Glisează în sus ca să votezi!» Democrație în acțiune, oameni buni.",
"Desigur, nicio reinterpretare modernă nu ar fi completă fără o călătorie în spațiu. Imaginați-vă «Hamlet: Ultima frontieră», unde ceva este putred în Imperiul Galactic. Hamlet este un tânăr Jedi, sfâșiat între răzbunarea tatălui și fidelitatea față de partea luminoasă a Forței. Claudius? A devenit un lord Sith în toată regula. Fantoma bătrânului Hamlet? Firește, o hologramă a Forței. «Luke, eu sunt tatăl tău» nu se compară cu «Hamlet, fratele meu m-a ucis».",
"Poate cea mai importantă actualizare din Hamlet 2.0 este însă un terapeut bun. Imaginați-vă cât de repede s-ar încheia tragedia dacă Hamlet ar avea acces la îngrijire psihologică de calitate. «Doctore, îl văd mereu pe tatăl meu mort.» «Interesant. V-ați gândit că asta ar putea ține de o durere neprocesată, nu de o chemare la răzbunare violentă?» Gata. Cinci acte comprimate într-o ședință de 50 de minute, cu coplată inclusă."
]
assert len(t)==len(d['segments']),(len(t),len(d['segments']))
for x,v in zip(d['segments'],t):x['translation']=v
p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
