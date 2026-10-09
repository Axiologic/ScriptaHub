import json
from pathlib import Path

cache_path=Path('tools/keyword-translations.generated.json')
cache=json.loads(cache_path.read_text())
langs=('ro','fr','de','es','pt','it','pl')
fixes={
 'Shelley’s novel': ('romanul lui Shelley','le roman de Shelley','Shelleys Roman','la novela de Shelley','o romance de Shelley','il romanzo di Shelley','powieść Shelley'),
 'William Frankenstein': ('William Frankenstein','William Frankenstein','William Frankenstein','William Frankenstein','William Frankenstein','William Frankenstein','William Frankenstein'),
 'De Lacey cottage': ('căsuța familiei De Lacey','la maison des De Lacey','das Haus der Familie De Lacey','la casa de los De Lacey','a casa dos De Lacey','la casa dei De Lacey','dom rodziny De Lacey'),
 'Safie': ('Safie','Safie','Safie','Safie','Safie','Safie','Safie'),
 'Geneva': ('Geneva','Genève','Genf','Ginebra','Genebra','Ginevra','Genewa'),
 'Scottish island': ('insulă scoțiană','île écossaise','schottische Insel','isla escocesa','ilha escocesa','isola scozzese','szkocka wyspa'),
 'gothic novel': ('roman gotic','roman gothique','gotischer Roman','novela gótica','romance gótico','romanzo gotico','powieść gotycka'),
 'comic voice': ('voce comică','voix comique','komischer Erzählton','voz cómica','voz cômica','voce comica','komiczny ton narracji'),
 'comic narration': ('narațiune comică','narration comique','komische Erzählweise','narración cómica','narração cômica','narrazione comica','komiczna narracja'),
 'comic comparisons': ('comparații comice','comparaisons comiques','komische Vergleiche','comparaciones cómicas','comparações cômicas','paragoni comici','komiczne porównania'),
 'underlying pattern': ('tipar de fond','schéma sous-jacent','zugrunde liegendes Muster','patrón subyacente','padrão subjacente','schema sottostante','ukryty wzorzec'),
 'gothic': ('gotic','gothique','gotisch','gótico','gótico','gotico','gotycki'),
 'television, pop culture': ('televiziune și cultură pop','télévision et culture populaire','Fernsehen und Popkultur','televisión y cultura pop','televisão e cultura pop','televisione e cultura pop','telewizja i popkultura'),
 'macabre arts and crafts': ('meșteșuguri macabre','bricolage macabre','makabres Kunsthandwerk','manualidades macabras','artesanato macabro','lavoretti macabri','makabryczne rękodzieło'),
 'creation': ('creație','création','Schöpfung','creación','criação','creazione','stworzenie'),
 'abandonment': ('abandon','abandon','Verlassenwerden','abandono','abandono','abbandono','porzucenie'),
 'responsibility': ('responsabilitate','responsabilité','Verantwortung','responsabilidad','responsabilidade','responsabilità','odpowiedzialność'),
 'scientific ambition': ('ambiție științifică','ambition scientifique','wissenschaftlicher Ehrgeiz','ambición científica','ambição científica','ambizione scientifica','ambicja naukowa'),
 'scientific hubris': ('trufie științifică','démesure scientifique','wissenschaftliche Hybris','soberbia científica','arrogância científica','hybris scientifica','pycha naukowa'),
 'electrical contraption': ('dispozitiv electric','dispositif électrique','elektrische Vorrichtung','artilugio eléctrico','engenhoca elétrica','congegno elettrico','urządzenie elektryczne'),
 'animate them': ('a le însufleți','leur donner vie','sie zum Leben erwecken','darles vida','dar-lhes vida','dar loro vita','ożywić je'),
 'sentient creation': ('creație conștientă','création douée de conscience','bewusste Schöpfung','creación consciente','criação consciente','creazione senziente','świadome stworzenie'),
 'newborn mind': ('minte de nou-născut','esprit de nouveau-né','Geist eines Neugeborenen','mente de recién nacido','mente de recém-nascido','mente di neonato','umysł noworodka'),
 'adult body': ('corp adult','corps adulte','erwachsener Körper','cuerpo adulto','corpo adulto','corpo adulto','ciało dorosłego'),
 'duty': ('datorie','devoir','Pflicht','deber','dever','dovere','obowiązek'),
 'family servant Justine': ('servitoarea familiei Justine','Justine, servante de la famille','Justine, die Bedienstete der Familie','Justine, la sirvienta de la familia','Justine, a criada da família','Justine, la domestica di famiglia','Justine, służąca rodziny'),
 'wrongly accused': ('acuzată pe nedrept','accusée à tort','zu Unrecht beschuldigt','acusada injustamente','acusada injustamente','accusata ingiustamente','niesłusznie oskarżona'),
 'wrongly accused and executed': ('acuzată pe nedrept și executată','accusée et exécutée à tort','zu Unrecht beschuldigt und hingerichtet','acusada injustamente y ejecutada','acusada injustamente e executada','accusata ingiustamente e giustiziata','niesłusznie oskarżona i stracona'),
 'female companion': ('tovarășă','compagne','weibliche Gefährtin','compañera','companheira','compagna','towarzyszka'),
 'creature’s experience': ('experiența creaturii','l’expérience de la créature','Erfahrung des Geschöpfs','experiencia de la criatura','experiência da criatura','esperienza della creatura','doświadczenie istoty'),
 'human feeling': ('sentimente omenești','sentiments humains','menschliche Gefühle','sentimientos humanos','sentimentos humanos','sentimenti umani','ludzkie uczucia'),
 'attempts to belong': ('încercări de a-și găsi locul','tentatives de trouver sa place','Versuche, dazuzugehören','intentos de encontrar su lugar','tentativas de encontrar seu lugar','tentativi di trovare il proprio posto','próby znalezienia swojego miejsca'),
 'companionship': ('companie','compagnie','Gesellschaft','compañía','companhia','compagnia','towarzystwo'),
 'saves a girl': ('salvează o fată','sauve une fille','rettet ein Mädchen','salva a una niña','salva uma menina','salva una ragazza','ratuje dziewczynkę'),
 'framing of an innocent woman': ('învinovățirea unei femei nevinovate','accusation montée contre une innocente','das Anhängen einer Schuld an eine Unschuldige','incriminación de una mujer inocente','incriminação de uma mulher inocente','incastrare una donna innocente','wrobienie niewinnej kobiety'),
 'independent being': ('ființă independentă','être indépendant','eigenständiges Wesen','ser independiente','ser independente','essere indipendente','niezależna istota'),
 'unfinished work': ('lucrare neterminată','œuvre inachevée','unfertige Arbeit','obra inacabada','obra inacabada','opera incompiuta','niedokończona praca'),
 'wedding night': ('noaptea nunții','nuit de noces','Hochzeitsnacht','noche de bodas','noite de núpcias','notte di nozze','noc poślubna'),
 'ethical relevance': ('actualitate etică','pertinence éthique','ethische Relevanz','vigencia ética','relevância ética','rilevanza etica','aktualność etyczna'),
 'unchecked scientific ambition': ('ambiție științifică neînfrânată','ambition scientifique sans frein','ungezügelter wissenschaftlicher Ehrgeiz','ambición científica descontrolada','ambição científica desenfreada','ambizione scientifica sfrenata','niepohamowana ambicja naukowa'),
 'seek connection': ('caută apropiere','chercher le lien','Nähe suchen','buscar vínculos','buscar vínculos','cercare legami','szukać więzi'),
 'understanding an injury': ('înțelegerea unei răni','comprendre une blessure','eine Verletzung verstehen','comprender una herida','compreender uma ferida','comprendere una ferita','zrozumienie krzywdy'),
 'ethical prompts': ('întrebări etice','questions éthiques','ethische Denkanstöße','preguntas éticas','questões éticas','spunti etici','pytania etyczne'),
 'analogies': ('analogii','analogies','Analogien','analogías','analogias','analogie','analogie'),
}
for phrase, values in fixes.items():
 assert len(values)==len(langs)
 for lang, value in zip(langs,values):
  cache['translations'][lang][phrase]=value
cache_path.write_text(json.dumps(cache,ensure_ascii=False,indent=2)+'\n')
print('Corrected',len(fixes),'keyword translations in',len(langs),'languages')
