import json
from pathlib import Path
p=Path(__file__).parent/'chunks/0005.json';d=json.loads(p.read_text())
translations={
 't000051': '''Descrierea acestui proces de către Orwell ridică întrebări profunde despre limitele rezistenței umane și despre natura sinelui. Există un nucleu inviolabil al identității sau orice persoană poate fi schimbată fundamental prin presiune suficientă? Finalul sumbru al romanului sugerează că nimeni nu este în afara razei controlului totalitar.''',
 't000052': '''Rolul memoriei în formarea identității și în rezistența față de opresiune este o altă temă esențială. Lupta lui Winston de a-și aminti corect trecutul privește nu doar adevărul istoric, ci și păstrarea sentimentului de sine și a realității. Controlul Partidului asupra informațiilor și revizuirea permanentă a istoriei fac aproape imposibil ca oamenii să aibă încredere în propriile amintiri sau să-și formeze o înțelegere coerentă a lumii.''',
 't000053': '''De-a lungul romanului, limbajul joacă un rol central în controlul exercitat de Partid asupra gândirii și realității. Nouvorba este creată pentru ca anumite gânduri să devină literalmente de neconceput prin eliminarea cuvintelor necesare exprimării lor. Acest control al limbajului este un instrument puternic de modelare a peisajului cognitiv al cetățenilor Oceaniei.''',
 't000054': '''Mesajul lui Orwell din „1984” este un avertisment sever despre posibilitatea controlului totalitar și fragilitatea libertății individuale. Romanul sugerează că, fără vigilență permanentă, societățile pot ajunge într-o stare în care adevărul nu mai are sens, individualitatea este zdrobită, iar puterea devine un scop în sine.''',
 't000055': '''Influența durabilă a romanului „1984” stă în capacitatea de a-i face pe cititori să-și pună întrebări despre propriile societăți și despre riscul abuzului de putere. El încurajează examinarea critică a legăturii dintre limbaj, adevăr și putere, precum și păstrarea gândirii și exprimării individuale.''',
}
assert set(translations)=={x['id'] for x in d['segments']}
for seg in d['segments']:seg['translation']=translations[seg['id']]
p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
print('translated',len(d['segments']))
