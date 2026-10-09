import json
from pathlib import Path

path = Path('tools/keyword-translations.generated.json')
cache = json.loads(path.read_text())
fix = {
 'evolution by natural selection': {'de':'Evolution durch natürliche Selektion','pl':'ewolucja przez dobór naturalny'},
 'Beagle voyage': {'fr':'voyage du Beagle','es':'viaje del Beagle','pt':'viagem do Beagle','it':'viaggio del Beagle','ro':'călătoria pe Beagle','pl':'podróż Beagle'},
 'physical account of inheritance': {'fr':'explication physique de l’hérédité','de':'physikalische Erklärung der Vererbung','es':'explicación física de la herencia','pt':'explicação física da hereditariedade','it':'spiegazione fisica dell’ereditarietà','ro':'explicația fizică a eredității','pl':'fizyczne wyjaśnienie dziedziczenia'},
 'present-day biology': {'pl':'współczesna biologia'},
 'genetic drift': {'ro':'derivă genetică','pl':'dryf genetyczny'},
 'evolutionary developmental biology': {'de':'evolutionäre Entwicklungsbiologie','pl':'ewolucyjna biologia rozwoju'},
 'variation and selection': {'de':'Variation und Selektion','pl':'zmienność i dobór'},
 'classical curriculum': {'ro':'programă clasică','pl':'klasyczny program nauczania'},
 'beetles': {'it':'coleotteri','ro':'gândaci'},
 'specimens and notes': {'de':'Exemplare und Notizen','pl':'okazy i notatki'},
 'vast time': {'de':'gewaltige Zeiträume','it':'tempi immensi','ro':'perioade uriașe','pl':'długie okresy czasu'},
 'fossils': {'pl':'skamieniałości'},
 'closely related forms': {'pt':'formas estreitamente aparentadas'},
 'fixity of species': {'de':'Unveränderlichkeit der Arten','ro':'caracterul fix al speciilor','pl':'niezmienność gatunków'},
 'Galápagos finches': {'fr':'pinsons des Galápagos','es':'pinzones de Galápagos','pt':'tentilhões de Galápagos','it':'fringuelli delle Galápagos','ro':'cintezele din Galápagos','pl':'zięby z Galápagos'},
 'inherited traits': {'es':'rasgos heredados'},
 'populations': {'de':'Populationen'},
 'On the Origin of Species': {'ro':'Despre originea speciilor','pl':'O powstawaniu gatunków'},
 'heredity': {'fr':'hérédité','de':'Vererbung','ro':'ereditate'},
 'natural selection': {'de':'natürliche Selektion','pl':'dobór naturalny'},
 'acquired traits': {'es':'rasgos adquiridos','it':'tratti acquisiti'},
 'eugenics': {'fr':'eugénisme','ro':'eugenie'},
 'crop and animal breeding': {'fr':'sélection des cultures et élevage','es':'mejora de cultivos y cría de animales','pt':'melhoramento de culturas e criação de animais','it':'miglioramento delle colture e allevamento','ro':'ameliorarea plantelor și creșterea animalelor'},
 'conservation': {'pl':'ochrona przyrody'},
 'swarm intelligence': {'fr':'intelligence en essaim','de':'Schwarmintelligenz','es':'inteligencia de enjambre','pt':'inteligência de enxame','it':'intelligenza di sciame','ro':'inteligență de roi','pl':'inteligencja rojowa'},
 'model of inquiry': {'fr':'modèle de recherche','de':'Modell wissenschaftlicher Forschung','es':'modelo de investigación','pt':'modelo de investigação','it':'modello di ricerca','ro':'model de cercetare','pl':'model badania naukowego'},
}
for phrase, labels in fix.items():
 for lang,label in labels.items():
  assert phrase in cache['translations'][lang],(phrase,lang)
  cache['translations'][lang][phrase]=label
path.write_text(json.dumps(cache,ensure_ascii=False,indent=2)+'\n')
print('Curated',sum(map(len,fix.values())),'labels')
