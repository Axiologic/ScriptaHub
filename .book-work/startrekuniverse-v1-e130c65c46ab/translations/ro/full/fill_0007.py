import json
from pathlib import Path
p=Path(__file__).parent/'chunks/0007.json';d=json.loads(p.read_text())
t={
52:'În concluzie, universul Star Trek cercetează în profunzime potențialul omenirii, îmbinând filosofia, știința și povestirea într-o imagine a viitorului întemeiată pe speranță, curiozitate și unitate. Prin numeroasele personaje, culturi extraterestre și dileme morale, franciza îi provoacă pe spectatori să înfrunte întrebări profunde despre identitate, etică și natura progresului. Tehnologiile avansate și structurile sociale și politice ale Federației reflectă încrederea optimistă că oamenii își pot depăși defectele și pot construi o societate dreaptă și echitabilă. Farmecul durabil al francizei stă în echilibrul dintre aventurile spațiale palpitante și temele provocatoare care ating publicul de mai multe generații.',
53:'De la provocările etice ale Directivei Primare la minunile tehnologiei care inspiră inovația reală, Star Trek ne amintește mereu de potențialul comun de a explora, învăța și crește. În cele din urmă, nu este doar o poveste despre explorarea spațiului, ci și o mărturie a puterii imaginației de a ne îndrepta spre un viitor mai bun și mai incluziv. Privind către stele, Star Trek ne invită să explorăm cu îndrăzneală frontiera finală, nu doar în spațiu, ci și în noi înșine, încercând să împlinim viitorul pe care îl imaginează.',
54:'Bibliografie',
55:'„Star Trek: The Next Generation Technical Manual”, de Rick Sternbach',
56:'„Star Trek: The Original Series - The Official 50th Anniversary Trivia Book”, de Zachary Oliver',
}
for x in d['segments']:x['translation']=t[int(x['id'][1:])]
p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
