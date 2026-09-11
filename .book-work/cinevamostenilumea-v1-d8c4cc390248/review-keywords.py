from pathlib import Path
import json
w=Path(__file__).parent;p=w/'keyword-translations.json';c=json.loads(p.read_text())
rows='''evolutionary fitness|valoare adaptativă|valeur sélective|evolutionäre Fitness|aptitud evolutiva|aptidão evolutiva|fitness evolutiva|dostosowanie ewolucyjne
cultural retention|păstrarea culturii|maintien culturel|kultureller Fortbestand|conservación cultural|preservação cultural|conservazione culturale|zachowanie kultury
heritability|ereditabilitate|héritabilité|Heritabilität|heredabilidad|herdabilidade|ereditabilità|odziedziczalność
genetic inheritance|moștenire genetică|hérédité génétique|genetische Vererbung|herencia genética|herança genética|ereditarietà genetica|dziedziczenie genetyczne
conscientiousness|conștiinciozitate|conscienciosité|Gewissenhaftigkeit|responsabilidad personal|conscienciosidade|coscienziosità|sumienność
parenting|creșterea copiilor|parentalité|Kindererziehung|crianza de los hijos|parentalidade|genitorialità|rodzicielstwo
housing|locuințe|logement|Wohnraum|vivienda|habitação|alloggi|mieszkalnictwo
generation lengths|intervale între generații|intervalles entre générations|Generationenabstände|intervalos generacionales|intervalos entre gerações|intervalli generazionali|odstępy międzypokoleniowe
statistical significance|semnificație statistică|significativité statistique|statistische Signifikanz|significación estadística|significância estatística|significatività statistica|istotność statystyczna
psychological measures|măsurători psihologice|mesures psychologiques|psychologische Messungen|mediciones psicológicas|medições psicológicas|misurazioni psicologiche|pomiary psychologiczne
completed fertility|descendență finală|descendance finale|abgeschlossene Fertilität|descendencia final|descendência final|discendenza finale|dzietność zrealizowana
founder effects|efecte de fondator|effets fondateurs|Gründereffekte|efectos fundadores|efeitos fundadores|effetti del fondatore|efekty założyciela
patrilineal organization|organizare patriliniară|organisation patrilinéaire|patrilineare Organisation|organización patrilineal|organização patrilinear|organizzazione patrilineare|organizacja patrylinearna
paternal-lineage bottleneck|gât de sticlă al liniilor paterne|goulot d’étranglement des lignées paternelles|Flaschenhals der väterlichen Abstammungslinien|cuello de botella de los linajes paternos|gargalo das linhagens paternas|collo di bottiglia delle linee paterne|wąskie gardło linii ojcowskich
kinship|rudenie|parenté|Verwandtschaft|parentesco|parentesco|parentela|pokrewieństwo
matching platform|platformă de găsire a partenerilor|plateforme de rencontres|Partnervermittlungsplattform|plataforma de búsqueda de pareja|plataforma de encontros|piattaforma di incontri|platforma doboru partnerów
artificial companionship|companie artificială|compagnie artificielle|künstliche Gefährten|compañía artificial|companhia artificial|compagnia artificiale|sztuczne towarzystwo
eugenics|eugenie|eugénisme|Eugenik|eugenesia|eugenia|eugenetica|eugenika'''
for line in rows.splitlines():
 term,*labels=line.split('|')
 for lang,label in zip(['ro','fr','de','es','pt','it','pl'],labels):c['translations'][lang][term]=label
fixes={'ro':{'reproductive success':'succes reproductiv','genetic correlations':'corelații genetice','psychiatric diagnoses':'diagnostice psihiatrice','shared environment':'mediu comun','schooling':'școlarizare','knowledge mediation':'medierea cunoașterii','neo-tribal archipelago':'arhipelag neotribal','defensive power':'putere defensivă'},'pl':{'reputation systems':'systemy reputacji','relational thinking':'myślenie relacyjne','schooling':'edukacja szkolna','Pluralism':'pluralizm','endogamy':'endogamia'},'de':{'pronatalist enclaves':'pronatalistische Enklaven'},'pt':{'impersonal institutions':'instituições impessoais'},'it':{'psychiatric diagnoses':'diagnosi psichiatriche'}}
for lang,values in fixes.items():c['translations'][lang].update(values)
p.write_text(json.dumps(c,ensure_ascii=False,indent=2)+'\n')
