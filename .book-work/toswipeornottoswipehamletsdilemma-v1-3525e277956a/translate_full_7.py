import json
from pathlib import Path
p=Path('.book-work/toswipeornottoswipehamletsdilemma-v1-3525e277956a/translations/ro/full/chunks/0007.json')
d=json.loads(p.read_text())
t=[
"Pe măsură ce înfruntăm provocările păstrării culturii literare în epoca digitală, trebuie să rămânem deschiși către abordări noi, care vorbesc generațiilor următoare. Fie prin modernizări umoristice, adaptări digitale sau experiențe interactive, cheia este păstrarea esenței acestor opere durabile și prezentarea lor în forme care rezonează cu publicul contemporan.",
"În concluzie, călătoria noastră alături de Hamlet cel digital ne amintește că marea artă nu este statică, ci vie și mereu în schimbare. Așa cum Shakespeare a împrumutat și reimaginat poveștile timpului său, și noi putem reinterpreta și reînvia operele clasice pentru epoca noastră. Astfel, le facem mai accesibile și ne îmbogățim înțelegerea trecutului și a prezentului.",
"În timp ce derulăm, glisăm și distribuim prin secolul XXI, să nu uităm puterea cuvintelor, profunzimea experienței umane și relevanța durabilă a marii literaturi. În cele din urmă, fie că sunt exprimate printr-un monolog sfâșietor sau printr-un tweet atent formulat, întrebările fundamentale ale existenței rămân aceleași. A ne apropia sau a nu ne apropia de literatura clasică în era digitală — aceasta-i întrebarea. Iar prin abordări care îmbină clasicul cu contemporanul, sperăm că tot mai mulți cititori vor alege să se apropie de ea."
]
assert len(t)==len(d['segments']),(len(t),len(d['segments']))
for x,v in zip(d['segments'],t):x['translation']=v
p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
