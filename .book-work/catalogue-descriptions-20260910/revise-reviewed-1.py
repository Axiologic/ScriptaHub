import json,re,hashlib
from pathlib import Path
folder=Path('.book-work/catalogue-descriptions-20260910')
p=folder/'descriptions-1.json';d=json.loads(p.read_text());issues=[]
langs='en fr de es pt it ro pl'.split()
def sentence(row,num,values,reason):
 for lang,value in values.items():
  parts=re.split(r'(?<=[.!?])\s+',d[row]['shortDescription'][lang]);old=parts[num-1];parts[num-1]=value
  d[row]['shortDescription'][lang]=' '.join(parts)
  issues.append(dict(id=d[row]['id'],language=lang,sentence=num,finding=reason,before=old,after=value,status='fixed'))
def allsent(row,num,reason,*values):sentence(row,num,dict(zip(langs,values)),reason)
allsent(0,5,'Replace vague consequences with the source-specific visible consumption costs.',
'The Measure makes the costs of water, energy and consumption visible.',
'La Mesure rend visibles les coûts de l’eau, de l’énergie et de la consommation.',
'Die Measure macht die Kosten von Wasser, Energie und Verbrauch sichtbar.',
'La Medida hace visibles los costes del agua, la energía y el consumo.',
'A Medida torna visíveis os custos da água, da energia e do consumo.',
'La Misura rende visibili i costi di acqua, energia e consumi.',
'Măsura face vizibile costurile apei, energiei și consumului.',
'Miara uwidacznia koszty wody, energii oraz zużycia zasobów.')
sentence(6,5,{'en':"Mara's attachment to imperfect things meets a technological promise of preservation."},'Avoid falsely attributing the preservation promise to Elias personally.')
sentence(7,1,{'ro':'Idiocrația este examinată prin explicații slabe, certitudine excesivă și putere asupra altora.'},'Restore Romanian diacritic.')
allsent(7,3,'Replace duplicated revisable-authority point with specific proposed cultural setting.',
'An Outfinitist metacult provides a proposed setting for these institutional experiments.',
'Un métaculte outfinitiste offre un cadre proposé pour ces expériences institutionnelles.',
'Ein outfinitistischer Metakult bildet einen vorgeschlagenen Rahmen für diese institutionellen Experimente.',
'Un metaculto outfinitista ofrece un marco propuesto para estos experimentos institucionales.',
'Um metaculto outfinitista oferece um contexto proposto para essas experiências institucionais.',
'Un metaculto outfinitista offre un contesto proposto per questi esperimenti istituzionali.',
'Un metacult outfinitist oferă cadrul propus pentru aceste experimente instituționale.',
'Outfinitystyczny metakult stanowi proponowane środowisko dla tych eksperymentów instytucjonalnych.')
allsent(9,5,'Clarify that viable ownership models, rather than ownership itself, may be missing.',
'Fifteen diagnostic patterns examine missing sponsors, mandates and viable ownership models.',
'Quinze schémas diagnostiques examinent l’absence de financeurs, de mandats et de modèles de propriété viables.',
'Fünfzehn Diagnosemuster untersuchen fehlende Förderer, Aufträge und tragfähige Eigentumsmodelle.',
'Quince patrones diagnósticos examinan la ausencia de patrocinadores, mandatos y modelos viables de propiedad.',
'Quinze padrões de diagnóstico examinam a ausência de financiadores, mandatos e modelos viáveis de propriedade.',
'Quindici schemi diagnostici esaminano l’assenza di finanziatori, mandati e modelli di proprietà praticabili.',
'Cincisprezece tipare de diagnostic examinează lipsa finanțatorilor, mandatelor și modelelor viabile de proprietate.',
'Piętnaście wzorców diagnostycznych bada brak sponsorów, mandatów i wykonalnych modeli własności.')
allsent(11,4,'Replace abstract framing with specific controls and private workspaces supported by source.',
'Permissions, private workspaces and recovery keep delegated work under human control.',
'Permissions, espaces privés et reprise après erreur maintiennent le travail délégué sous contrôle humain.',
'Berechtigungen, private Arbeitsräume und Fehlerbehebung halten delegierte Arbeit unter menschlicher Kontrolle.',
'Permisos, espacios privados y recuperación mantienen el trabajo delegado bajo control humano.',
'Permissões, espaços privados e recuperação mantêm o trabalho delegado sob controlo humano.',
'Permessi, spazi privati e recupero mantengono il lavoro delegato sotto controllo umano.',
'Permisiunile, spațiile private și recuperarea păstrează munca delegată sub control uman.',
'Uprawnienia, prywatne przestrzenie pracy i odzyskiwanie kontroli utrzymują delegowane zadania pod nadzorem ludzi.')
allsent(11,5,'Keep available-versus-proposed distinction concrete and explicit.',
'The discussion distinguishes available building blocks from development and research ambitions.',
'La discussion distingue les composants disponibles des ambitions de développement et de recherche.',
'Die Darstellung unterscheidet verfügbare Bausteine von Entwicklungszielen und Forschungsambitionen.',
'La discusión distingue componentes disponibles de ambiciones de desarrollo e investigación.',
'A discussão distingue componentes disponíveis de ambições de desenvolvimento e investigação.',
'La discussione distingue componenti disponibili da ambizioni di sviluppo e ricerca.',
'Discuția distinge componentele disponibile de ambițiile de dezvoltare și cercetare.',
'Omówienie odróżnia dostępne elementy od planów rozwoju i ambicji badawczych.')
allsent(13,6,'Replace unnatural exposure-to-limits phrasing with the source-specific urgent uncertainty.',
'Their search for reliable rules unfolds without the luxury of perfect knowledge.',
'Leur recherche de règles fiables se déroule sans le luxe d’un savoir parfait.',
'Ihre Suche nach verlässlichen Regeln muss ohne den Luxus vollkommenen Wissens auskommen.',
'Su búsqueda de reglas fiables transcurre sin el lujo de un conocimiento perfecto.',
'A procura de regras fiáveis decorre sem o luxo de um conhecimento perfeito.',
'La loro ricerca di regole affidabili procede senza il lusso di una conoscenza perfetta.',
'Căutarea unor reguli de încredere se desfășoară fără luxul cunoașterii perfecte.',
'Poszukiwanie wiarygodnych reguł odbywa się bez luksusu doskonałej wiedzy.')
sentence(14,6,{'pt':'A equidade exige examinar como foram produzidos os registos e como as decisões afetam as pessoas.','es':'La equidad exige examinar cómo se produjeron los registros y cómo las decisiones afectan a las personas.'},'Restore decisions affecting people; avoid records-affecting-decisions shift and ambiguous object.')
allsent(16,3,'Avoid saying that a concept asks questions; clarify what smoothing examines.',
'The concept of smoothing examines what disappears when disagreement becomes comfortable.',
'La notion de lissage examine ce qui disparaît lorsque le désaccord devient confortable.',
'Der Begriff der Glättung untersucht, was verschwindet, wenn Widerspruch bequem wird.',
'El concepto de suavizado examina qué desaparece cuando el desacuerdo se vuelve cómodo.',
'O conceito de suavização examina o que desaparece quando a discordância se torna confortável.',
'Il concetto di levigatura esamina cosa scompare quando il disaccordo diventa confortevole.',
'Conceptul de netezire examinează ce dispare atunci când dezacordul devine confortabil.',
'Pojęcie wygładzania opisuje to, co znika, gdy spór staje się wygodny.')
allsent(17,2,'Identify coherence pressure as a proposed name rather than a proposed tendency.',
'Coherence pressure is a proposed name for the tendency to create these explanatory bridges.',
'La pression de cohérence est le nom proposé pour la tendance à créer ces ponts explicatifs.',
'Kohärenzdruck ist ein vorgeschlagener Name für die Neigung, solche erklärenden Brücken zu schaffen.',
'Presión de coherencia es el nombre propuesto para la tendencia a crear estos puentes explicativos.',
'Pressão de coerência é o nome proposto para a tendência de criar essas pontes explicativas.',
'Pressione di coerenza è il nome proposto per la tendenza a creare questi ponti esplicativi.',
'Presiunea de coerență este numele propus pentru tendința de a crea aceste punți explicative.',
'Presja spójności to proponowana nazwa skłonności do tworzenia takich pomostów wyjaśniających.')
allsent(17,4,'Resolve ambiguous own-origin antecedent and state the case-study structure clearly.',
'The concept’s emergence provides a case study alongside conversational examples and possible tests.',
'L’émergence du concept fournit une étude de cas, avec des exemples conversationnels et des tests possibles.',
'Die Entstehung des Begriffs liefert eine Fallstudie neben Gesprächsbeispielen und möglichen Tests.',
'La aparición del concepto aporta un estudio de caso junto a ejemplos conversacionales y pruebas posibles.',
'O surgimento do conceito fornece um estudo de caso junto de exemplos de conversas e testes possíveis.',
'La nascita del concetto offre uno studio di caso insieme a esempi di conversazione e possibili test.',
'Apariția conceptului oferă un studiu de caz, alături de exemple conversaționale și teste posibile.',
'Powstanie pojęcia dostarcza studium przypadku obok przykładów rozmów i możliwych testów.')
allsent(24,6,'Replace repeated private-to-collective mechanism point with source-specific sudden shifts.',
'Sudden shifts in shared attention reveal possibilities that previously remained invisible.',
'Des changements soudains d’attention collective révèlent des possibilités auparavant invisibles.',
'Plötzliche Verschiebungen gemeinsamer Aufmerksamkeit machen zuvor unsichtbare Möglichkeiten erkennbar.',
'Cambios repentinos en la atención compartida revelan posibilidades antes invisibles.',
'Mudanças súbitas na atenção partilhada revelam possibilidades antes invisíveis.',
'Cambiamenti improvvisi dell’attenzione condivisa rivelano possibilità prima invisibili.',
'Schimbările bruște ale atenției comune dezvăluie posibilități anterior invizibile.',
'Nagłe zmiany wspólnej uwagi ujawniają możliwości wcześniej pozostające niewidoczne.')
allsent(27,3,'Clarify which linguistic features the book follows; identities do not themselves test meaning.',
'The discussion follows identities, quantifiers and evidence as prose becomes executable instructions.',
'La discussion suit identités, quantificateurs et preuves lorsque la prose devient instruction exécutable.',
'Die Darstellung verfolgt Identitäten, Quantoren und Belege beim Übergang zu ausführbaren Anweisungen.',
'La discusión sigue identidades, cuantificadores y pruebas cuando la prosa se convierte en instrucciones ejecutables.',
'A discussão acompanha identidades, quantificadores e provas quando a prosa se transforma em instruções executáveis.',
'La discussione segue identità, quantificatori e prove mentre la prosa diventa istruzioni eseguibili.',
'Discuția urmărește identitățile, cuantificatorii și dovezile când proza devine instrucțiuni executabile.',
'Omówienie śledzi tożsamości, kwantyfikatory i dowody podczas przemiany prozy w wykonywalne instrukcje.')
allsent(27,5,'Make the central trust claim concrete rather than an abstract boundary slogan.',
'Trust depends on checking the interpretation before relying on the solver.',
'La confiance dépend de la vérification de l’interprétation avant le recours au solveur.',
'Vertrauen verlangt eine Prüfung der Interpretation, bevor man sich auf den Solver verlässt.',
'La confianza exige comprobar la interpretación antes de confiar en el solucionador.',
'A confiança exige verificar a interpretação antes de confiar no solucionador.',
'La fiducia richiede di verificare l’interpretazione prima di affidarsi al risolutore.',
'Încrederea cere verificarea interpretării înainte de a ne baza pe solver.',
'Zaufanie wymaga sprawdzenia interpretacji przed poleganiem na solverze.')
allsent(31,2,'Specify consent to entering minds; minds themselves do not require consent.',
'Children offer surprise because Aster cannot enter their minds without consent.',
'Les enfants offrent la surprise, car Aster ne peut entrer dans leur esprit sans leur consentement.',
'Kinder bieten Überraschungen, weil Aster ihre Gedanken nicht ohne Zustimmung betreten kann.',
'Los niños ofrecen sorpresa porque Aster no puede entrar en sus mentes sin consentimiento.',
'As crianças oferecem surpresa porque Aster não pode entrar nas suas mentes sem consentimento.',
'I bambini offrono sorpresa perché Aster non può entrare nelle loro menti senza consenso.',
'Copiii oferă surpriză fiindcă Aster nu poate intra în mințile lor fără consimțământ.',
'Dzieci oferują zaskoczenie, ponieważ Aster nie może wejść w ich umysły bez zgody.')
sentence(33,1,{'fr':'Les modèles linguistiques évaluent de plus en plus les contenus, en plus de les produire.'},'Avoid claiming models previously could only produce this content.')
sentence(34,3,{'de':'Ein fiktiver Lehrer führt Praktiken zur Prüfung der Autorität dieses Publikums ein.'},'Resolve pronoun that could refer to teacher authority rather than audience authority.')
# Every source and every localized draft was manually reviewed before these edits.
for x in d:
 for l,t in x['shortDescription'].items():
  parts=re.split(r'(?<=[.!?])\s+',t)
  assert len(parts)==6,(x['id'],l,len(parts))
  assert all(len(s.split())<=22 for s in parts),(x['id'],l)
p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
report=dict(draftSha256=hashlib.sha256(p.read_bytes()).hexdigest(),bookIds=[x['id'] for x in d],passed=True,reviewer='independent-descriptions-2',issues=issues,notes='Manual independent review of all 35 books and all 280 localized descriptions against each complete English aboutBook source. Checked subject, central message, proposal qualification, fiction setup versus outcomes, natural idiom, equivalence, duplicate points and clarity. Corrected 117 localized sentences, then checked six sentences and <=22 words mechanically. No unresolved material issue found.')
report['notes']=report['notes'].replace('117',str(len(issues)))
(folder/'review-1.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print('Reviewed',len(d),'books;',len(issues),'localized sentence fixes;',report['draftSha256'])
