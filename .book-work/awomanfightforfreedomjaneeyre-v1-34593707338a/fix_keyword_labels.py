import json
from pathlib import Path
p=Path('tools/keyword-translations.generated.json');d=json.loads(p.read_text());t=d['translations']
fix={
'helen burns':{'fr':'Helen Burns','de':'Helen Burns','es':'Helen Burns','pt':'Helen Burns','it':'Helen Burns','ro':'Helen Burns','pl':'Helen Burns'},
'gateshead and lowood':{'fr':'Gateshead et Lowood','de':'Gateshead und Lowood','es':'Gateshead y Lowood','pt':'Gateshead e Lowood','it':'Gateshead e Lowood','ro':'Gateshead și Lowood','pl':'Gateshead i Lowood'},
'thornfield in ruins':{'fr':'Thornfield en ruines','de':'Thornfield in Ruinen','es':'Thornfield en ruinas','pt':'Thornfield em ruínas','it':'Thornfield in rovina','ro':'Thornfield în ruine','pl':'Thornfield w ruinie'},
'rivers family':{'fr':'famille Rivers','de':'Familie Rivers','es':'familia Rivers','pt':'família Rivers','it':'famiglia Rivers','ro':'familia Rivers','pl':'rodzina Riversów'},
'victorian expectations':{'fr':'attentes victoriennes','de':'viktorianische Erwartungen','es':'expectativas victorianas','pt':'expectativas vitorianas','it':'aspettative vittoriane','ro':'așteptări victoriene','pl':'oczekiwania epoki wiktoriańskiej'},
'st. john rivers':{'fr':'St. John Rivers','de':'St. John Rivers','es':'St. John Rivers','pt':'St. John Rivers','it':'St. John Rivers','ro':'St. John Rivers','pl':'St. John Rivers'},
'leaving thornfield':{'fr':'quitter Thornfield','de':'Thornfield verlassen','es':'dejar Thornfield','pt':'deixar Thornfield','it':'lasciare Thornfield','ro':'plecarea de la Thornfield','pl':'opuszczenie Thornfield'},
'lowood institution':{'fr':'institution de Lowood','de':'Lowood-Institut','es':'institución de Lowood','pt':'instituição de Lowood','it':'istituto di Lowood','ro':'Institutul Lowood','pl':'instytut Lowood'},
'victorian society':{'fr':'société victorienne','de':'viktorianische Gesellschaft','es':'sociedad victoriana','pt':'sociedade vitoriana','it':'società vittoriana','ro':'societate victoriană','pl':'społeczeństwo wiktoriańskie'},
'gateshead hall':{'fr':'Gateshead Hall','de':'Gateshead Hall','es':'Gateshead Hall','pt':'Gateshead Hall','it':'Gateshead Hall','ro':'Gateshead Hall','pl':'Gateshead Hall'},
'bertha mason':{'fr':'Bertha Mason','de':'Bertha Mason','es':'Bertha Mason','pt':'Bertha Mason','it':'Bertha Mason','ro':'Bertha Mason','pl':'Bertha Mason'},
'mr. brocklehurst':{'fr':'M. Brocklehurst','de':'Herr Brocklehurst','es':'señor Brocklehurst','pt':'Sr. Brocklehurst','it':'signor Brocklehurst','ro':'domnul Brocklehurst','pl':'pan Brocklehurst'},
'edward rochester':{'fr':'Edward Rochester','de':'Edward Rochester','es':'Edward Rochester','pt':'Edward Rochester','it':'Edward Rochester','ro':'Edward Rochester','pl':'Edward Rochester'},
'individuality for duty':{'fr':'individualité sacrifiée au devoir','de':'Individualität für die Pflicht opfern','es':'individualidad sacrificada al deber','pt':'individualidade sacrificada ao dever','it':'individualità sacrificata al dovere','ro':'individualitate sacrificată datoriei','pl':'indywidualność poświęcona obowiązkowi'},
'respect and self-direction':{'fr':'respect et autonomie de décision','de':'Respekt und Selbstbestimmung','es':'respeto y autodeterminación','pt':'respeito e autodeterminação','it':'rispetto e autodeterminazione','ro':'respect și autodeterminare','pl':'szacunek i samostanowienie'},
'feminist reimagining':{'ro':'reimaginare feministă','it':'reinterpretazione femminista','pl':'feministyczna reinterpretacja'},
'shift in power':{'fr':'changement du rapport de force','de':'Verschiebung des Machtverhältnisses','es':'cambio en la relación de poder','pt':'mudança na relação de poder','it':'cambiamento nei rapporti di potere','ro':'schimbare în raportul de putere','pl':'zmiana układu sił'},
'servant and upper class':{'fr':'domesticité et haute société','de':'Dienstboten und Oberschicht','es':'servicio doméstico y clase alta','pt':'criados e classe alta','it':'servitù e classe alta','ro':'slujitori și clasa de sus','pl':'służba i klasa wyższa'},
'money and social power':{'pl':'pieniądze i władza społeczna'},
'abandoning comfort':{'de':'Verzicht auf Komfort'},
'harsh guardianship':{'fr':'tutelle sévère','de':'harte Vormundschaft','es':'tutela severa','pt':'tutela severa','it':'tutela severa','ro':'tutelă aspră','pl':'surowa opieka'},
'inner strength':{'fr':'force intérieure','pt':'força interior','it':'forza interiore','ro':'putere interioară','pl':'siła wewnętrzna'},
'orphaned jane':{'fr':'Jane devenue orpheline','de':'die verwaiste Jane','es':'Jane huérfana','pt':'Jane órfã','it':'Jane orfana','ro':'Jane rămasă orfană','pl':'osierocona Jane'},
'gender':{'fr':'genre','ro':'gen'},
'confinement':{'de':'Einschließung','ro':'izolare forțată','pl':'zamknięcie'},
'livelihood':{'it':'mezzi di sostentamento','ro':'mijloace de trai','pl':'środki utrzymania'},
'personhood':{'es':'condición de persona','ro':'condiția de persoană'},
'solitary struggle':{'ro':'luptă solitară'},
'unequal authority':{'fr':'autorité inégale','de':'ungleiche Autorität','es':'autoridad desigual','pt':'autoridade desigual','it':'autorità diseguale','ro':'autoritate inegală','pl':'nierówna władza'},
'unwanted outsider':{'fr':'étrangère indésirable','de':'unerwünschte Außenseiterin','es':'extraña no deseada','pt':'estranha indesejada','it':'estranea indesiderata','ro':'străină nedorită','pl':'niechciana outsiderka'},
'sense of self':{'ro':'conștiință de sine'},
'marginalized orphan':{'es':'huérfana marginada','it':'orfana emarginata','ro':'orfană marginalizată','pl':'marginalizowana sierota'},
}
for phrase,localized in fix.items():
 for lang,label in localized.items():
  assert phrase in t[lang],(lang,phrase)
  t[lang][phrase]=label
p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
