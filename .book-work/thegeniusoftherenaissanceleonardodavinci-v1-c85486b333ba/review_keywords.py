import json
from pathlib import Path
work=Path(__file__).resolve().parent
p=work/'book/manifest.json';m=json.loads(p.read_text())
m['keywordReview']['phrases']=[('habit of translating observations' if v=='vinci code' else v) for v in m['keywordReview']['phrases']]
assert len(set(m['keywordReview']['phrases']))==90
p.write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n')
p=Path('tools/keyword-translations.generated.json');c=json.loads(p.read_text());t=c['translations']
manual={
'mirror writing':['écriture en miroir','Spiegelschrift','escritura especular','escrita em espelho','scrittura speculare','scriere în oglindă','pismo lustrzane'],
'crossing disciplines':['croiser les disciplines','Disziplinen verbinden','cruzar disciplinas','cruzar disciplinas','attraversare le discipline','legături între discipline','łączenie dyscyplin'],
'crossing disciplines today':['croiser les disciplines aujourd’hui','Disziplinen heute verbinden','cruzar disciplinas hoy','cruzar disciplinas hoje','attraversare le discipline oggi','legături între discipline astăzi','łączenie dyscyplin dzisiaj'],
'movement between subjects':['passage entre les domaines','Wechsel zwischen Fachgebieten','paso entre disciplinas','passagem entre áreas de estudo','passaggio tra discipline','trecere între domenii','przechodzenie między dziedzinami'],
'self-supporting bridge':['pont autoportant','selbsttragende Brücke','puente autoportante','ponte autoportante','ponte autoportante','pod autoportant','most samonośny'],
'study and dissection':['étude et dissection','Studium und Sektion','estudio y disección','estudo e dissecação','studio e dissezione','studiu și disecție','badania i sekcje anatomiczne'],
'left-handed writer':['auteur gaucher','linkshändiger Schreiber','escritor zurdo','escritor canhoto','scrittore mancino','autor stângaci','leworęczny pisarz'],
'tools of inquiry':['outils de recherche','Werkzeuge der Forschung','herramientas de investigación','ferramentas de investigação','strumenti di ricerca','instrumente de cercetare','narzędzia badawcze'],
'da vinci code':['Da Vinci Code','Da Vinci Code','El código Da Vinci','O Código Da Vinci','Il codice da Vinci','Codul lui Da Vinci','Kod Leonarda da Vinci'],
'habit of translating observations':['habitude de traduire les observations en projets','Gewohnheit, Beobachtungen in Entwürfe umzusetzen','hábito de convertir observaciones en diseños','hábito de transformar observações em projetos','abitudine a trasformare osservazioni in progetti','obiceiul de a transforma observațiile în proiecte','zwyczaj przekładania obserwacji na projekty'],
'chiaroscuro models':['modelé par clair-obscur','Modellierung durch Hell-Dunkel','modelado mediante claroscuro','modelação por claro-escuro','modellazione chiaroscurale','modelare prin clarobscur','modelowanie światłocieniem'],
'reduced smudging':['réduction des taches d’encre','weniger verwischte Tinte','menos manchas de tinta','menos borrões de tinta','meno sbavature d’inchiostro','mai puțină cerneală întinsă','mniejsze rozmazywanie atramentu'],
'giant crossbow':['arbalète géante','riesige Armbrust','ballesta gigante','besta gigante','balestra gigante','arbaletă uriașă','olbrzymia kusza'],
'mona lisa':['Mona Lisa']*7,
'aerial screw':['vis aérienne','Luftschraube','tornillo aéreo','parafuso aéreo','vite aerea','șurub aerian','śruba powietrzna'],
'plant growth':['croissance des plantes','Pflanzenwachstum','crecimiento de las plantas','crescimento das plantas','crescita delle piante','creșterea plantelor','wzrost roślin'],
}
for phrase,values in manual.items():
 for lang,value in zip(('fr','de','es','pt','it','ro','pl'),values):t[lang][phrase]=value
p.write_text(json.dumps(c,ensure_ascii=False,indent=2)+'\n')
