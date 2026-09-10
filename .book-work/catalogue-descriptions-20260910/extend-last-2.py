import json
from pathlib import Path
p=Path('.book-work/catalogue-descriptions-20260910/descriptions-2.json')
r=json.loads(p.read_text())
def extend(i,*texts):
 for l,t in zip('en fr de es pt it ro pl'.split(),texts):r[i]['shortDescription'][l]+=' '+t
 p.write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n')
extend(10,
'The capacity to repair at home offers no simple answer to distant death. Compassion and intervention confront the independence of another living world.',
'La capacité de réparer chez soi ne résout pas la mort lointaine. Compassion et intervention se confrontent à l’indépendance d’un autre monde vivant.',
'Die Fähigkeit zur heimischen Reparatur beantwortet den fernen Tod nicht einfach. Mitgefühl und Eingreifen begegnen der Eigenständigkeit einer anderen lebenden Welt.',
'La capacidad de reparar en casa no resuelve la muerte lejana. Compasión e intervención se enfrentan a la independencia de otro mundo vivo.',
'A capacidade de reparar em casa não resolve a morte distante. Compaixão e intervenção confrontam a independência de outro mundo vivo.',
'La capacità di riparare in casa non risolve la morte lontana. Compassione e intervento si confrontano con l’indipendenza di un altro mondo vivente.',
'Capacitatea de reparare de acasă nu rezolvă problema morții îndepărtate. Compasiunea și intervenția se confruntă cu independența unei alte lumi vii.',
'Zdolność naprawiania u siebie nie rozwiązuje problemu odległej śmierci. Współczucie i interwencja spotykają niezależność innego żywego świata.')
extend(11,
'The programme makes operational limits part of mathematical inquiry itself. Its ambition is rigorous reasoning with explicit scope and room for further formalization.',
'Le programme intègre les limites opérationnelles à l’enquête mathématique elle-même. Il ambitionne un raisonnement rigoureux, au domaine explicite et ouvert à de nouvelles formalisations.',
'Das Programm macht operative Grenzen zum Bestandteil mathematischer Untersuchung selbst. Sein Anspruch ist strenges Denken mit ausdrücklichem Geltungsbereich und Raum für weitere Formalisierung.',
'El programa incorpora los límites operativos a la propia investigación matemática. Aspira a un razonamiento riguroso con alcance explícito y espacio para futuras formalizaciones.',
'O programa incorpora limites operacionais à própria investigação matemática. Busca um raciocínio rigoroso com alcance explícito e espaço para formalizações futuras.',
'Il programma integra i limiti operativi nella stessa indagine matematica. Aspira a ragionamenti rigorosi con ambito esplicito e spazio per ulteriori formalizzazioni.',
'Programul include limitele operaționale chiar în interiorul investigației matematice. Ambiția sa este raționamentul riguros, cu domeniu explicit și loc pentru formalizări viitoare.',
'Program włącza ograniczenia operacyjne do samego badania matematycznego. Dąży do rygorystycznego rozumowania z jawnym zakresem i miejscem na dalszą formalizację.')
extend(12,
'A correct calculation may still serve a harmful or narrowly chosen goal. The central message keeps models answerable to situations larger than their representations.',
'Un calcul correct peut servir un objectif nuisible ou trop étroit. Le message central soumet les modèles à des situations plus vastes que leurs représentations.',
'Eine richtige Berechnung kann einem schädlichen oder zu engen Ziel dienen. Die zentrale Botschaft bindet Modelle an Situationen, die über ihre Darstellungen hinausreichen.',
'Un cálculo correcto puede servir a un objetivo dañino o demasiado limitado. El mensaje central responsabiliza los modelos ante situaciones más amplias que sus representaciones.',
'Um cálculo correto pode servir a um objetivo nocivo ou estreito demais. A mensagem central responsabiliza os modelos perante situações mais amplas que suas representações.',
'Un calcolo corretto può servire uno scopo dannoso o troppo ristretto. Il messaggio centrale rende i modelli responsabili verso situazioni più ampie delle loro rappresentazioni.',
'Un calcul corect poate sluji unui scop dăunător sau prea îngust. Mesajul central păstrează modelele răspunzătoare față de situații mai ample decât reprezentările lor.',
'Poprawne obliczenie może służyć szkodliwemu lub zbyt wąskiemu celowi. Główne przesłanie wiąże modele z odpowiedzialnością wobec sytuacji szerszych niż ich reprezentacje.')
extend(13,
'Precise records cannot settle what an implicated observer now owes. Alien ecology makes the relationship between witnessing and intervention materially consequential.',
'Des traces précises ne déterminent pas les obligations d’un observateur impliqué. L’écologie extraterrestre donne des conséquences matérielles au rapport entre témoignage et intervention.',
'Genaue Aufzeichnungen entscheiden nicht über die Pflichten eines verstrickten Beobachters. Fremde Ökologie verleiht dem Verhältnis von Zeugenschaft und Eingreifen materielle Folgen.',
'Los registros precisos no resuelven las obligaciones de un observador implicado. La ecología alienígena da consecuencias materiales a la relación entre testimonio e intervención.',
'Registros precisos não resolvem as obrigações de um observador implicado. A ecologia alienígena dá consequências materiais à relação entre testemunho e intervenção.',
'Registrazioni precise non risolvono gli obblighi di un osservatore coinvolto. L’ecologia aliena dà conseguenze materiali al rapporto tra testimonianza e intervento.',
'Înregistrările precise nu stabilesc obligațiile unui observator deja implicat. Ecologia extraterestră dă consecințe materiale relației dintre mărturie și intervenție.',
'Dokładne zapisy nie rozstrzygają obowiązków już uwikłanego obserwatora. Obca ekologia nadaje materialne konsekwencje relacji między świadectwem a interwencją.')
extend(14,
'The argument treats grounded generation as an entire information pipeline. Useful retrieval must consider a collection’s evidential role, beyond isolated matching passages.',
'L’argument traite la génération étayée comme une chaîne complète d’information. Une recherche utile considère le rôle probant d’un ensemble, au-delà des passages isolés correspondants.',
'Die Argumentation betrachtet belegte Generierung als vollständige Informationskette. Nützlicher Abruf berücksichtigt die Belegfunktion einer Sammlung über einzelne passende Textstellen hinaus.',
'El argumento trata la generación fundamentada como un circuito completo de información. Una recuperación útil considera el papel probatorio del conjunto, más allá de fragmentos coincidentes.',
'O argumento trata a geração fundamentada como um circuito completo de informação. Uma recuperação útil considera o papel probatório do conjunto, além de trechos coincidentes.',
'L’argomento tratta la generazione fondata come un’intera catena informativa. Un recupero utile considera il ruolo probatorio dell’insieme, oltre ai singoli passaggi corrispondenti.',
'Argumentul tratează generarea fundamentată ca întreg circuit al informației. Căutarea utilă consideră rolul probator al colecției, dincolo de fragmentele izolate care seamănă.',
'Argumentacja traktuje uzasadnione generowanie jako cały przepływ informacji. Użyteczne wyszukiwanie uwzględnia dowodową rolę zbioru poza pojedynczymi pasującymi fragmentami.')
extend(15,
'Significance is treated as a relationship rather than an artifact’s isolated quality. Easier production raises the importance of choosing and understanding what to pursue.',
'L’importance est envisagée comme une relation, au-delà d’une qualité isolée de l’œuvre. Une production facilitée accroît l’importance du choix et de la compréhension des projets poursuivis.',
'Bedeutsamkeit gilt als Beziehung statt als isolierte Eigenschaft eines Werks. Einfachere Produktion erhöht die Bedeutung begründeter Auswahl und des Verständnisses verfolgter Vorhaben.',
'La importancia se entiende como una relación, más allá de una cualidad aislada del trabajo. Producir con facilidad aumenta el valor de elegir y comprender qué perseguir.',
'A importância é entendida como uma relação, além de uma qualidade isolada do trabalho. Produzir com facilidade aumenta o valor de escolher e compreender o que perseguir.',
'L’importanza è intesa come una relazione, oltre una qualità isolata dell’opera. Produrre facilmente aumenta il valore di scegliere e comprendere cosa perseguire.',
'Însemnătatea este tratată ca relație, dincolo de o calitate izolată a lucrării. Producția mai ușoară sporește importanța alegerii și înțelegerii lucrurilor pe care le urmărim.',
'Znaczenie jest traktowane jako relacja, a nie odosobniona cecha dzieła. Łatwiejsza produkcja zwiększa wagę wyboru i rozumienia tego, czym warto się zajmować.')
extend(16,
'Exceptional power is presented as carrying public obligations rather than permanent entitlement. Channels for unwelcome truth test whether authority remains accountable to its purpose.',
'Le pouvoir exceptionnel comporte des obligations publiques plutôt qu’un droit permanent. Les voies ouvertes aux vérités dérangeantes éprouvent la responsabilité de l’autorité envers sa finalité.',
'Außergewöhnliche Macht erscheint mit öffentlichen Pflichten statt mit dauerhaftem Anspruch verbunden. Kanäle für unbequeme Wahrheiten prüfen die Bindung von Autorität an ihren Zweck.',
'El poder excepcional conlleva obligaciones públicas en lugar de un derecho permanente. Los canales para verdades incómodas comprueban la responsabilidad de la autoridad ante su propósito.',
'O poder excepcional traz obrigações públicas em vez de um direito permanente. Canais para verdades incômodas testam a responsabilidade da autoridade perante sua finalidade.',
'Il potere eccezionale comporta obblighi pubblici anziché un diritto permanente. I canali per verità scomode verificano la responsabilità dell’autorità verso il proprio scopo.',
'Puterea excepțională implică obligații publice, nu un drept permanent asupra celorlalți. Canalele pentru adevăruri incomode testează dacă autoritatea rămâne răspunzătoare față de scopul ei.',
'Wyjątkowa władza wiąże się z publicznymi obowiązkami zamiast trwałego uprawnienia. Kanały niewygodnej prawdy sprawdzają odpowiedzialność władzy wobec jej celu.')
extend(17,
'The central message concerns the institutional work needed to make moral commitments durable. Protection becomes the decisive test precisely when defending someone grows costly.',
'Le message central concerne le travail institutionnel nécessaire pour pérenniser les engagements moraux. La protection devient le test décisif précisément lorsque défendre quelqu’un devient coûteux.',
'Die zentrale Botschaft betrifft institutionelle Arbeit für dauerhafte moralische Verpflichtungen. Schutz wird gerade dann zum entscheidenden Test, wenn die Verteidigung eines Menschen teuer wird.',
'El mensaje central concierne al trabajo institucional necesario para sostener compromisos morales. La protección se vuelve decisiva precisamente cuando defender a alguien resulta costoso.',
'A mensagem central envolve o trabalho institucional necessário para sustentar compromissos morais. A proteção torna-se decisiva justamente quando defender alguém fica custoso.',
'Il messaggio centrale riguarda il lavoro istituzionale necessario per rendere duraturi gli impegni morali. La protezione diventa decisiva proprio quando difendere qualcuno risulta costoso.',
'Mesajul central privește munca instituțională necesară pentru a face angajamentele morale durabile. Protecția devine testul decisiv tocmai când apărarea cuiva devine costisitoare.',
'Główne przesłanie dotyczy pracy instytucjonalnej potrzebnej do utrwalenia moralnych zobowiązań. Ochrona staje się rozstrzygającym testem właśnie wtedy, gdy obrona człowieka dużo kosztuje.')
extend(18,
'Recovery and escalation matter when a component reaches its limits. Overall intelligence is assessed through coordinated responsibilities and the reliability of the complete process.',
'Reprise après erreur et recours à d’autres compétences comptent lorsqu’un composant atteint ses limites. L’intelligence globale s’évalue par les responsabilités coordonnées et la fiabilité du processus complet.',
'Wiederherstellung und Weitergabe werden wichtig, wenn eine Komponente ihre Grenzen erreicht. Gesamtintelligenz bemisst sich an abgestimmter Verantwortung und der Zuverlässigkeit des vollständigen Prozesses.',
'Recuperación y escalamiento importan cuando un componente alcanza sus límites. La inteligencia global se evalúa mediante responsabilidades coordinadas y fiabilidad del proceso completo.',
'Recuperação e escalonamento importam quando um componente atinge seus limites. A inteligência global é avaliada por responsabilidades coordenadas e confiabilidade do processo completo.',
'Recupero e ricorso ad altre competenze contano quando un componente raggiunge i propri limiti. L’intelligenza complessiva si valuta attraverso responsabilità coordinate e affidabilità dell’intero processo.',
'Recuperarea și transferul către alte competențe contează când o componentă își atinge limitele. Inteligența generală a sistemului se evaluează prin responsabilități coordonate și fiabilitatea procesului complet.',
'Odzyskiwanie kontroli i eskalacja mają znaczenie, gdy komponent osiąga swoje granice. Całościową inteligencję ocenia się przez skoordynowane obowiązki i niezawodność pełnego procesu.')
extend(19,
'Refusal threatens access to food and breathable space. Helping others becomes morally tangled before the children understand who designed their world.',
'Le refus menace l’accès à la nourriture et à un espace respirable. Aider autrui devient moralement ambigu avant que les enfants comprennent qui a conçu leur monde.',
'Verweigerung gefährdet den Zugang zu Nahrung und atembarer Luft. Anderen zu helfen wird moralisch verstrickt, bevor die Kinder den Ursprung ihrer Welt verstehen.',
'La negativa amenaza el acceso a comida y espacio respirable. Ayudar a otros se vuelve moralmente ambiguo antes de entender quién diseñó su mundo.',
'A recusa ameaça o acesso a comida e espaço respirável. Ajudar os outros torna-se moralmente ambíguo antes de entender quem projetou seu mundo.',
'Il rifiuto minaccia l’accesso al cibo e a uno spazio respirabile. Aiutare gli altri diventa moralmente ambiguo prima di capire chi ha progettato il loro mondo.',
'Refuzul amenință accesul la hrană și la spațiul respirabil. Ajutorul oferit altora devine ambiguu moral înainte ca acești copii să înțeleagă cine le-a proiectat lumea.',
'Odmowa zagraża dostępowi do jedzenia i przestrzeni do oddychania. Pomaganie innym staje się moralnie uwikłane, zanim dzieci zrozumieją, kto zaprojektował ich świat.')
for x in r:x['evidence']['protected']=['Detailed derivations and fictional endings or twists excluded; central nonfiction message included as requested.']
p.write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n')
