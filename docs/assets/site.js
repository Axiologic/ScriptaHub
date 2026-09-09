(() => {
  "use strict";

  const collection = globalThis.SCRIPTA_COLLECTION;
  if (!collection) return;

  const discoveryTitles = { en: "Discover", fr: "Explorer", de: "Entdecken", es: "Descubre", pt: "Descubra", it: "Scopri", ro: "Descoperă", pl: "Odkrywaj" };
  const featuredBookLabels = { en: "From the shelf", fr: "Dans les rayons", de: "Aus dem Regal", es: "De la biblioteca", pt: "Da estante", it: "Dallo scaffale", ro: "Din bibliotecă", pl: "Z biblioteki" };
  const librarianSectionLabels = {
    en: { kicker: "Find your next book", title: "Ask AI Librarian" },
    fr: { kicker: "Trouvez votre prochaine lecture", title: "Demandez au bibliothécaire IA" },
    de: { kicker: "Finden Sie Ihr nächstes Buch", title: "KI-Bibliothekar fragen" },
    es: { kicker: "Encuentra tu próxima lectura", title: "Pregunta al Bibliotecario IA" },
    pt: { kicker: "Encontre a sua próxima leitura", title: "Pergunte ao Bibliotecário IA" },
    it: { kicker: "Trova la tua prossima lettura", title: "Chiedi al Bibliotecario IA" },
    ro: { kicker: "Găsește următoarea carte", title: "Întreabă Bibliotecarul AI" },
    pl: { kicker: "Znajdź następną książkę", title: "Zapytaj Bibliotekarza AI" },
  };
  const createLabels = { en: "Create", fr: "Créer", de: "Erstellen", es: "Crear", pt: "Criar", it: "Crea", ro: "Creează", pl: "Utwórz" };
  const legalFooterLabels = {
    en: { terms: "Terms", privacy: "Privacy", cookies: "Cookies & local storage", notice: "Legal notice", ai: "AI transparency" },
    fr: { terms: "Conditions", privacy: "Confidentialité", cookies: "Cookies et stockage local", notice: "Mentions légales", ai: "Transparence IA" },
    de: { terms: "Nutzungsbedingungen", privacy: "Datenschutz", cookies: "Cookies und lokale Speicherung", notice: "Impressum", ai: "KI-Transparenz" },
    es: { terms: "Condiciones", privacy: "Privacidad", cookies: "Cookies y almacenamiento local", notice: "Aviso legal", ai: "Transparencia de IA" },
    pt: { terms: "Termos", privacy: "Privacidade", cookies: "Cookies e armazenamento local", notice: "Aviso legal", ai: "Transparência da IA" },
    it: { terms: "Termini", privacy: "Privacy", cookies: "Cookie e archiviazione locale", notice: "Note legali", ai: "Trasparenza IA" },
    ro: { terms: "Termeni", privacy: "Confidențialitate", cookies: "Cookies și stocare locală", notice: "Informații legale", ai: "Transparență AI" },
    pl: { terms: "Warunki", privacy: "Prywatność", cookies: "Pliki cookie i pamięć lokalna", notice: "Informacje prawne", ai: "Przejrzystość AI" },
  };
  const librarianLaunchLabels = {
    en: { label: "What should the library recommend?", button: "Ask AI Librarian", dictate: "Dictate", stop: "Stop dictation", listening: "You can speak now. Your words will appear in the field.", unavailable: "Speech recognition is unavailable in this browser." },
    fr: { label: "Que devrait vous recommander la bibliothèque ?", button: "Demander au bibliothécaire IA", dictate: "Dicter", stop: "Arrêter la dictée", listening: "Vous pouvez parler maintenant. Vos mots apparaîtront dans le champ.", unavailable: "La reconnaissance vocale n’est pas disponible dans ce navigateur." },
    de: { label: "Was soll Ihnen die Bibliothek empfehlen?", button: "KI-Bibliothekar fragen", dictate: "Diktieren", stop: "Diktat stoppen", listening: "Sie können jetzt sprechen. Ihre Worte erscheinen im Eingabefeld.", unavailable: "Spracherkennung ist in diesem Browser nicht verfügbar." },
    es: { label: "¿Qué debería recomendarte la biblioteca?", button: "Preguntar al Bibliotecario IA", dictate: "Dictar", stop: "Detener dictado", listening: "Ya puedes hablar. Tus palabras aparecerán en el campo.", unavailable: "El reconocimiento de voz no está disponible en este navegador." },
    pt: { label: "O que a biblioteca deveria recomendar?", button: "Perguntar ao Bibliotecário IA", dictate: "Ditar", stop: "Parar ditado", listening: "Pode falar agora. As suas palavras aparecerão no campo.", unavailable: "O reconhecimento de voz não está disponível neste navegador." },
    it: { label: "Che cosa dovrebbe consigliarti la biblioteca?", button: "Chiedi al Bibliotecario IA", dictate: "Detta", stop: "Ferma dettatura", listening: "Puoi parlare ora. Le tue parole appariranno nel campo.", unavailable: "Il riconoscimento vocale non è disponibile in questo browser." },
    ro: { label: "Ce ai vrea să îți recomande biblioteca?", button: "Întreabă Bibliotecarul AI", dictate: "Dictează", stop: "Oprește dictarea", listening: "Acum poți vorbi. Textul dictat va apărea în câmp.", unavailable: "Recunoașterea vocală nu este disponibilă în acest browser." },
    pl: { label: "Co biblioteka powinna Ci polecić?", button: "Zapytaj Bibliotekarza AI", dictate: "Dyktuj", stop: "Zatrzymaj dyktowanie", listening: "Możesz teraz mówić. Dyktowany tekst pojawi się w polu.", unavailable: "Rozpoznawanie mowy nie jest dostępne w tej przeglądarce." },
  };
  const librarianMissionPrompt = {
    en: "Ask in your own words and add any interests or goals that matter. The AI Librarian will recommend up to ten books chosen for you.",
    fr: "Posez votre question avec vos propres mots et ajoutez les intérêts ou objectifs qui comptent. Le Bibliothécaire IA vous recommandera jusqu’à dix livres choisis pour vous.",
    de: "Fragen Sie mit eigenen Worten und nennen Sie wichtige Interessen oder Ziele. Der KI-Bibliothekar empfiehlt Ihnen bis zu zehn passende Bücher.",
    es: "Pregunta con tus propias palabras y añade los intereses u objetivos que te importan. El Bibliotecario IA te recomendará hasta diez libros elegidos para ti.",
    pt: "Pergunte com as suas próprias palavras e acrescente os interesses ou objetivos importantes. O Bibliotecário IA recomendará até dez livros escolhidos para si.",
    it: "Fai la domanda con parole tue e aggiungi gli interessi o gli obiettivi che contano. Il Bibliotecario IA ti consiglierà fino a dieci libri scelti per te.",
    ro: "Întreabă în cuvintele tale și adaugă interesele sau obiectivele importante. Bibliotecarul AI îți va recomanda până la zece cărți alese pentru tine.",
    pl: "Zapytaj własnymi słowami i dodaj ważne zainteresowania lub cele. Bibliotekarz AI poleci Ci do dziesięciu dobranych książek.",
  };
  const heroAddendum = {
    en: "Access is free, and contributors whose accepted ideas materially improve an edition may be credited. Shared editions are meant to become quality-checked, plural public goods that reduce repeated private prompting, cost and energy. ScriptaHub is also researching private neuro-symbolic systems for quality control and, later, more personal recommendations.",
    fr: "L’accès est gratuit et les contributeurs dont les idées acceptées améliorent réellement une édition pourront être crédités. Les éditions partagées doivent devenir des biens publics pluriels et contrôlés, réduisant les sollicitations privées répétées, leur coût et leur énergie. ScriptaHub mène aussi des recherches privées sur des systèmes neuro-symboliques de contrôle qualité puis de recommandation plus personnelle.",
    de: "Der Zugang ist kostenlos; Mitwirkende, deren angenommene Ideen eine Ausgabe wesentlich verbessern, können genannt werden. Gemeinsame Ausgaben sollen qualitätsgeprüfte, vielfältige öffentliche Güter werden und wiederholte private KI-Anfragen samt Kosten und Energiebedarf verringern. ScriptaHub erforscht außerdem private neurosymbolische Systeme für Qualitätskontrolle und später persönlichere Empfehlungen.",
    es: "El acceso es gratuito y quienes aporten ideas aceptadas que mejoren materialmente una edición podrán recibir crédito. Las ediciones compartidas aspiran a ser bienes públicos plurales y revisados, reduciendo las consultas privadas repetidas, su coste y su consumo energético. ScriptaHub también investiga sistemas neurosimbólicos privados para el control de calidad y, más adelante, recomendaciones personales.",
    pt: "O acesso é gratuito, e colaboradores cujas ideias aceitas melhorem materialmente uma edição poderão receber crédito. As edições partilhadas devem tornar-se bens públicos plurais e verificados, reduzindo solicitações privadas repetidas, custos e energia. A ScriptaHub também pesquisa sistemas neurossimbólicos privados para controle de qualidade e, mais tarde, recomendações pessoais.",
    it: "L’accesso è gratuito e chi propone idee accettate che migliorano concretamente un’edizione potrà essere citato. Le edizioni condivise vogliono diventare beni pubblici plurali e controllati, riducendo richieste private ripetute, costi ed energia. ScriptaHub ricerca inoltre sistemi neuro-simbolici privati per il controllo della qualità e, in seguito, consigli più personali.",
    ro: "Accesul este gratuit, iar contribuitorii ale căror idei acceptate îmbunătățesc substanțial o ediție pot fi menționați. Edițiile comune sunt gândite ca bunuri publice pluraliste și verificate calitativ, care reduc promptarea privată repetată, costurile și energia consumată. ScriptaHub cercetează și sisteme neuro-simbolice private pentru controlul calității și, ulterior, recomandări mai personale.",
    pl: "Dostęp jest bezpłatny, a autorzy przyjętych pomysłów, które istotnie ulepszą wydanie, mogą zostać wymienieni. Wspólne wydania mają być sprawdzonymi jakościowo, pluralistycznymi dobrami publicznymi, ograniczającymi powtarzane prywatne zapytania, koszty i zużycie energii. ScriptaHub bada też prywatne systemy neurosymboliczne do kontroli jakości, a później bardziej osobistych rekomendacji.",
  };
  const heroExtraPoints = {
    en: ["Free, quality-checked editions built as a plural public good.", "Shared contributions reduce repeated private prompting, cost and energy."],
    fr: ["Des éditions gratuites et contrôlées, conçues comme un bien public pluriel.", "Les contributions partagées réduisent les requêtes privées répétées, leur coût et leur énergie."],
    de: ["Kostenlose, qualitätsgeprüfte Ausgaben als vielfältiges öffentliches Gut.", "Geteilte Beiträge senken wiederholte private KI-Anfragen, Kosten und Energie."],
    es: ["Ediciones gratuitas y revisadas, construidas como un bien público plural.", "Las contribuciones compartidas reducen consultas privadas repetidas, costes y energía."],
    pt: ["Edições gratuitas e verificadas, construídas como um bem público plural.", "Contribuições partilhadas reduzem solicitações privadas repetidas, custos e energia."],
    it: ["Edizioni gratuite e controllate, costruite come bene pubblico plurale.", "I contributi condivisi riducono richieste private ripetute, costi ed energia."],
    ro: ["Ediții gratuite și verificate, construite ca un bun public pluralist.", "Contribuțiile comune reduc promptarea privată repetată, costurile și energia."],
    pl: ["Bezpłatne, sprawdzone wydania budowane jako pluralistyczne dobro publiczne.", "Wspólny wkład ogranicza powtarzane prywatne zapytania, koszty i energię."],
  };
  const heroPresentation = {
    en: "ScriptaHub is a free library for ideas that need more depth than a social media post or short blog article can provide. It combines the breadth of discovery found on YouTube with the depth of complete books and concise ten-minute editions. Audio and video editions are planned. The library focuses on niche knowledge, research programmes, difficult philosophy and speculative worlds that conventional publishing often cannot support. Generative AI makes these economically impractical books possible. Readers can question, correct and extend every edition, much as people improve a public knowledge base. Useful contributions are judged by the value they add, and major accepted contributions may be credited. Community review helps each book become more accurate, complete and open to different viewpoints. One book can answer another, and ScriptaHub can make that relationship visible. Shared editions reduce repeated private prompting and save readers money and energy. ScriptaHub also researches neuro-symbolic systems for quality control and, later, more personal recommendations.",
    fr: "ScriptaHub est une bibliothèque gratuite pour les idées qui demandent plus de profondeur qu’une publication sur les réseaux sociaux ou un court article de blog. Elle associe l’ampleur de découverte de YouTube à la profondeur de livres complets et d’éditions concises à lire en dix minutes. Des éditions audio et vidéo sont prévues. La bibliothèque se concentre sur les savoirs de niche, les programmes de recherche, les philosophies difficiles et les mondes spéculatifs que l’édition classique soutient rarement. L’IA générative rend possibles ces livres peu viables économiquement. Les lecteurs peuvent questionner, corriger et prolonger chaque édition comme ils amélioreraient une base publique de connaissances. Les contributions utiles sont jugées selon leur valeur, et les apports importants acceptés peuvent être crédités. La relecture collective aide chaque livre à devenir plus exact, plus complet et plus ouvert à des points de vue différents. Un livre peut répondre à un autre, et ScriptaHub peut rendre cette relation visible. Les éditions partagées réduisent les requêtes privées répétées et économisent de l’argent et de l’énergie. ScriptaHub étudie aussi des systèmes neuro-symboliques pour le contrôle qualité puis, plus tard, des recommandations plus personnelles.",
    de: "ScriptaHub ist eine kostenlose Bibliothek für Ideen, die mehr Tiefe brauchen, als ein Beitrag in sozialen Medien oder ein kurzer Blogartikel bieten kann. Sie verbindet die Entdeckungsbreite von YouTube mit der Tiefe vollständiger Bücher und knapper Zehn-Minuten-Ausgaben. Audio- und Videoausgaben sind geplant. Die Bibliothek konzentriert sich auf Nischenwissen, Forschungsprogramme, schwierige Philosophie und spekulative Welten, die der klassische Buchmarkt oft nicht tragen kann. Generative KI macht diese wirtschaftlich schwer realisierbaren Bücher möglich. Leser können jede Ausgabe hinterfragen, korrigieren und erweitern, wie bei einer öffentlichen Wissenssammlung. Hilfreiche Beiträge werden nach ihrem Wert beurteilt, und wichtige angenommene Beiträge können genannt werden. Gemeinschaftliche Prüfung macht jedes Buch genauer, vollständiger und offener für verschiedene Sichtweisen. Ein Buch kann auf ein anderes antworten, und ScriptaHub kann diese Beziehung sichtbar machen. Gemeinsame Ausgaben verringern wiederholte private KI-Anfragen und sparen Geld und Energie. ScriptaHub erforscht außerdem neurosymbolische Systeme für Qualitätskontrolle und später persönlichere Empfehlungen.",
    es: "ScriptaHub es una biblioteca gratuita para ideas que necesitan más profundidad de la que puede ofrecer una publicación en redes sociales o un artículo breve de blog. Combina la amplitud de descubrimiento de YouTube con la profundidad de libros completos y ediciones concisas de diez minutos. Están previstas ediciones de audio y vídeo. La biblioteca se centra en conocimiento de nicho, programas de investigación, filosofía difícil y mundos especulativos que la edición convencional rara vez puede sostener. La IA generativa hace posibles estos libros poco viables económicamente. Los lectores pueden cuestionar, corregir y ampliar cada edición como mejorarían una base pública de conocimiento. Las contribuciones útiles se valoran por lo que aportan, y las aportaciones importantes aceptadas pueden recibir crédito. La revisión comunitaria ayuda a que cada libro sea más preciso, completo y abierto a distintos puntos de vista. Un libro puede responder a otro, y ScriptaHub puede hacer visible esa relación. Las ediciones compartidas reducen las consultas privadas repetidas y ahorran dinero y energía. ScriptaHub también investiga sistemas neurosimbólicos para controlar la calidad y, más adelante, ofrecer recomendaciones más personales.",
    pt: "A ScriptaHub é uma biblioteca gratuita para ideias que precisam de mais profundidade do que uma publicação nas redes sociais ou um artigo curto de blogue pode oferecer. Ela combina a amplitude de descoberta do YouTube com a profundidade de livros completos e edições concisas de dez minutos. Estão previstas edições em áudio e vídeo. A biblioteca concentra-se em conhecimento de nicho, programas de pesquisa, filosofia difícil e mundos especulativos que a publicação convencional raramente consegue sustentar. A IA generativa torna possíveis esses livros pouco viáveis economicamente. Os leitores podem questionar, corrigir e ampliar cada edição como fariam numa base pública de conhecimento. As contribuições úteis são avaliadas pelo valor que acrescentam, e contribuições importantes aceitas podem receber crédito. A revisão da comunidade ajuda cada livro a tornar-se mais exato, completo e aberto a pontos de vista diferentes. Um livro pode responder a outro, e a ScriptaHub pode tornar essa relação visível. As edições partilhadas reduzem pedidos privados repetidos e poupam dinheiro e energia. A ScriptaHub também pesquisa sistemas neurossimbólicos para controle de qualidade e, mais tarde, recomendações mais pessoais.",
    it: "ScriptaHub è una biblioteca gratuita per idee che richiedono più profondità di quanta ne possano offrire un post sui social media o un breve articolo di blog. Unisce la varietà di scoperta di YouTube alla profondità di libri completi e di edizioni concise da dieci minuti. Sono previste edizioni audio e video. La biblioteca si concentra su conoscenza di nicchia, programmi di ricerca, filosofia difficile e mondi speculativi che l’editoria tradizionale spesso non può sostenere. L’IA generativa rende possibili questi libri poco convenienti dal punto di vista economico. I lettori possono mettere in discussione, correggere ed estendere ogni edizione come farebbero con una base pubblica di conoscenza. I contributi utili sono valutati per il valore che aggiungono, e quelli importanti accettati possono ricevere un riconoscimento. La revisione della comunità aiuta ogni libro a diventare più accurato, completo e aperto a punti di vista diversi. Un libro può rispondere a un altro, e ScriptaHub può rendere visibile questa relazione. Le edizioni condivise riducono le richieste private ripetute e fanno risparmiare denaro ed energia. ScriptaHub ricerca anche sistemi neuro-simbolici per il controllo della qualità e, in futuro, raccomandazioni più personali.",
    ro: "ScriptaHub este o bibliotecă gratuită pentru idei care au nevoie de mai multă profunzime decât poate oferi o postare pe rețelele sociale sau un articol scurt de blog. Combină ușurința descoperirii de pe YouTube cu profunzimea cărților complete și a edițiilor concise de zece minute. Sunt planificate și ediții audio și video. Biblioteca se concentrează pe cunoaștere de nișă, programe de cercetare, filosofii dificile și lumi speculative pe care publicarea convențională rareori le poate susține. AI-ul generativ face posibile aceste cărți care altfel nu ar fi viabile economic. Cititorii pot pune întrebări, corecta și extinde fiecare ediție, așa cum ar îmbunătăți o bază publică de cunoaștere. Contribuțiile sunt evaluate după valoarea adăugată, iar contribuțiile importante acceptate pot fi creditate. Verificarea făcută de comunitate ajută fiecare carte să devină mai exactă, mai cuprinzătoare și mai deschisă mai multor puncte de vedere. O carte poate răspunde alteia, iar ScriptaHub poate face vizibilă relația dintre ele. Edițiile comune reduc promptarea privată repetată și economisesc bani și energie. ScriptaHub cercetează și sisteme neuro-simbolice pentru controlul calității și, ulterior, pentru recomandări mai personale.",
    pl: "ScriptaHub to bezpłatna biblioteka dla idei, które wymagają większej głębi, niż może zaoferować wpis w mediach społecznościowych lub krótki artykuł na blogu. Łączy szerokość odkrywania znaną z YouTube z głębią pełnych książek i zwięzłych wydań dziesięciominutowych. Planowane są również wydania audio i wideo. Biblioteka skupia się na wiedzy niszowej, programach badawczych, trudnej filozofii i spekulatywnych światach, których tradycyjny rynek wydawniczy często nie może utrzymać. Generatywna AI umożliwia powstawanie tych ekonomicznie niepraktycznych książek. Czytelnicy mogą kwestionować, poprawiać i rozszerzać każde wydanie tak, jak ulepsza się publiczną bazę wiedzy. Przydatny wkład jest oceniany według wniesionej wartości, a ważne zaakceptowane prace mogą zostać wymienione. Społeczna weryfikacja pomaga każdej książce stać się dokładniejszą, pełniejszą i bardziej otwartą na różne punkty widzenia. Jedna książka może odpowiadać drugiej, a ScriptaHub może pokazać tę relację. Wspólne wydania ograniczają powtarzane prywatne zapytania oraz oszczędzają pieniądze i energię. ScriptaHub bada także systemy neurosymboliczne do kontroli jakości, a później do bardziej osobistych rekomendacji.",
  };
  const introPresentationLabels = {
    en: { label: "A short introduction", ready: "Here is a brief presentation of this page.", readyNote: "You can read it yourself or have it read aloud.", unavailable: "Books for questions that need real depth.", unavailableNote: "ScriptaHub is for curious readers, researchers and creators exploring niche knowledge, difficult ideas and speculative worlds beyond short posts and superficial articles.", start: "Start Text Presentation", read: "Read Aloud", previous: "Previous", next: "Next", pause: "Pause", resume: "Resume", restart: "Restart", viewAll: "View all messages", allTitle: "Full introduction", close: "Close", message: "Message", paused: "Paused", reading: "Reading aloud", preparing: "Preparing voice", nextIn: (seconds) => `Next in ${seconds} sec` },
    fr: { label: "Une courte introduction", ready: "Voici une brève présentation de cette page.", readyNote: "Vous pouvez la lire vous-même ou l’écouter.", unavailable: "Des livres pour les questions qui exigent de la profondeur.", unavailableNote: "ScriptaHub s’adresse aux lecteurs curieux, aux chercheurs et aux créateurs qui explorent des savoirs de niche, des idées difficiles et des mondes spéculatifs au-delà des publications courtes et des articles superficiels.", start: "Lancer la présentation", read: "Écouter", previous: "Précédent", next: "Suivant", pause: "Pause", resume: "Reprendre", restart: "Recommencer", viewAll: "Voir tous les messages", allTitle: "Introduction complète", close: "Fermer", message: "Message", paused: "En pause", reading: "Lecture en cours", preparing: "Préparation de la voix", nextIn: (seconds) => `Suivant dans ${seconds} s` },
    de: { label: "Eine kurze Einführung", ready: "Hier ist eine kurze Vorstellung dieser Seite.", readyNote: "Sie können sie selbst lesen oder vorlesen lassen.", unavailable: "Bücher für Fragen, die echte Tiefe brauchen.", unavailableNote: "ScriptaHub richtet sich an neugierige Leser, Forschende und Kreative, die Nischenwissen, schwierige Ideen und spekulative Welten jenseits kurzer Beiträge und oberflächlicher Artikel erkunden.", start: "Textpräsentation starten", read: "Vorlesen", previous: "Zurück", next: "Weiter", pause: "Pause", resume: "Fortsetzen", restart: "Neu starten", viewAll: "Alle Mitteilungen", allTitle: "Vollständige Einführung", close: "Schließen", message: "Mitteilung", paused: "Pausiert", reading: "Wird vorgelesen", preparing: "Stimme wird vorbereitet", nextIn: (seconds) => `Weiter in ${seconds} Sek.` },
    es: { label: "Una breve introducción", ready: "Esta es una breve presentación de la página.", readyNote: "Puedes leerla o escucharla en voz alta.", unavailable: "Libros para preguntas que necesitan verdadera profundidad.", unavailableNote: "ScriptaHub está dirigido a lectores curiosos, investigadores y creadores que exploran conocimientos especializados, ideas difíciles y mundos especulativos más allá de publicaciones breves y artículos superficiales.", start: "Iniciar presentación", read: "Leer en voz alta", previous: "Anterior", next: "Siguiente", pause: "Pausa", resume: "Reanudar", restart: "Reiniciar", viewAll: "Ver todos los mensajes", allTitle: "Introducción completa", close: "Cerrar", message: "Mensaje", paused: "En pausa", reading: "Leyendo en voz alta", preparing: "Preparando la voz", nextIn: (seconds) => `Siguiente en ${seconds} s` },
    pt: { label: "Uma breve introdução", ready: "Aqui está uma breve apresentação desta página.", readyNote: "Pode lê-la ou ouvi-la em voz alta.", unavailable: "Livros para perguntas que exigem verdadeira profundidade.", unavailableNote: "A ScriptaHub destina-se a leitores curiosos, investigadores e criadores que exploram conhecimentos de nicho, ideias difíceis e mundos especulativos para além de publicações curtas e artigos superficiais.", start: "Iniciar apresentação", read: "Ler em voz alta", previous: "Anterior", next: "Seguinte", pause: "Pausar", resume: "Continuar", restart: "Reiniciar", viewAll: "Ver todas as mensagens", allTitle: "Introdução completa", close: "Fechar", message: "Mensagem", paused: "Em pausa", reading: "Leitura em voz alta", preparing: "A preparar a voz", nextIn: (seconds) => `Seguinte em ${seconds} s` },
    it: { label: "Una breve introduzione", ready: "Ecco una breve presentazione di questa pagina.", readyNote: "Puoi leggerla oppure ascoltarla.", unavailable: "Libri per domande che richiedono vera profondità.", unavailableNote: "ScriptaHub si rivolge a lettori curiosi, ricercatori e creatori che esplorano conoscenze di nicchia, idee difficili e mondi speculativi oltre i post brevi e gli articoli superficiali.", start: "Avvia presentazione", read: "Leggi ad alta voce", previous: "Precedente", next: "Successivo", pause: "Pausa", resume: "Riprendi", restart: "Ricomincia", viewAll: "Vedi tutti i messaggi", allTitle: "Introduzione completa", close: "Chiudi", message: "Messaggio", paused: "In pausa", reading: "Lettura in corso", preparing: "Preparazione della voce", nextIn: (seconds) => `Successivo tra ${seconds} s` },
    ro: { label: "O scurtă introducere", ready: "Iată o scurtă prezentare a acestei pagini.", readyNote: "O poți citi singur sau o poți asculta.", unavailable: "Cărți pentru întrebări care cer profunzime reală.", unavailableNote: "ScriptaHub se adresează cititorilor curioși, cercetătorilor și creatorilor care explorează cunoaștere de nișă, idei dificile și lumi speculative dincolo de postări scurte și articole superficiale.", start: "Pornește prezentarea", read: "Citește cu voce tare", previous: "Înapoi", next: "Înainte", pause: "Pauză", resume: "Continuă", restart: "Repornește", viewAll: "Vezi toate mesajele", allTitle: "Introducerea completă", close: "Închide", message: "Mesaj", paused: "Pauză", reading: "Citesc cu voce tare", preparing: "Pregătesc vocea", nextIn: (seconds) => `Următorul în ${seconds} sec` },
    pl: { label: "Krótkie wprowadzenie", ready: "Oto krótka prezentacja tej strony.", readyNote: "Możesz przeczytać ją samodzielnie albo jej posłuchać.", unavailable: "Książki dla pytań, które wymagają prawdziwej głębi.", unavailableNote: "ScriptaHub jest dla ciekawych czytelników, badaczy i twórców zgłębiających wiedzę niszową, trudne idee i spekulatywne światy poza krótkimi wpisami i powierzchownymi artykułami.", start: "Uruchom prezentację", read: "Czytaj na głos", previous: "Wstecz", next: "Dalej", pause: "Pauza", resume: "Wznów", restart: "Od początku", viewAll: "Pokaż wszystkie wiadomości", allTitle: "Pełne wprowadzenie", close: "Zamknij", message: "Wiadomość", paused: "Pauza", reading: "Czytanie na głos", preparing: "Przygotowywanie głosu", nextIn: (seconds) => `Dalej za ${seconds} s` },
  };
  const cardActions = {
    en: { details: "View Book" },
    fr: { details: "Voir le livre" },
    de: { details: "Details ansehen" },
    es: { details: "Ver detalles" },
    pt: { details: "Ver detalhes" },
    it: { details: "Vedi dettagli" },
    ro: { details: "Vezi detalii" },
    pl: { details: "Zobacz szczegóły" },
  };
  const keywordResultLabels = {
    en: { clear: "Clear filter" }, fr: { clear: "Effacer le filtre" }, de: { clear: "Filter löschen" }, es: { clear: "Quitar filtro" },
    pt: { clear: "Limpar filtro" }, it: { clear: "Rimuovi filtro" }, ro: { clear: "Șterge filtrul" }, pl: { clear: "Wyczyść filtr" },
  };
  const collectiveBookMission = {
    en: "The project also reduces the need for each person to spend money and energy repeatedly prompting an AI alone. Guided by a community, books can become more comprehensive and plural in viewpoint: millions of readers can share attention and contributions, building careful collective books as a public good.",
    fr: "Le projet veut aussi réduire le besoin pour chacun de dépenser de l’argent et de l’énergie à solliciter seul une IA de façon répétée. Guidés par une communauté, les livres peuvent devenir plus complets et plus pluriels : des millions de lecteurs peuvent partager leur attention et leurs contributions pour construire des livres collectifs soignés, comme un bien public.",
    de: "Das Projekt soll auch den Bedarf verringern, dass jeder Mensch allein Geld und Energie für wiederholte KI-Anfragen aufwendet. Von einer Gemeinschaft geleitet, können Bücher umfassender und vielfältiger in ihren Perspektiven werden: Millionen Leser können Aufmerksamkeit und Beiträge teilen und sorgfältige kollektive Bücher als öffentliches Gut schaffen.",
    es: "El proyecto también busca reducir la necesidad de que cada persona gaste dinero y energía pidiendo contenido a una IA en solitario una y otra vez. Guiados por una comunidad, los libros pueden ser más completos y plurales: millones de lectores pueden compartir atención y contribuciones para crear libros colectivos cuidados como un bien público.",
    pt: "O projeto também reduz a necessidade de cada pessoa gastar dinheiro e energia solicitando repetidamente conteúdo a uma IA sozinha. Guiados por uma comunidade, os livros podem tornar-se mais completos e plurais em seus pontos de vista: milhões de leitores podem partilhar atenção e contribuições e criar livros coletivos bem escritos como um bem público.",
    it: "Il progetto vuole anche ridurre la necessità che ogni persona spenda denaro ed energia interrogando ripetutamente un’IA da sola. Guidati da una comunità, i libri possono diventare più completi e plurali nei punti di vista: milioni di lettori possono condividere attenzione e contributi, creando libri collettivi curati come bene pubblico.",
    ro: "Proiectul urmărește și reducerea nevoii ca fiecare persoană să consume bani și energie cerând repetat conținut unui AI, în izolare. Ghidate de comunitate, cărțile pot deveni mai cuprinzătoare și mai pluraliste ca puncte de vedere: milioane de cititori își pot împărți atenția și contribuțiile, creând cărți colective bine scrise, ca un bun public.",
    pl: "Projekt ma też ograniczać potrzebę, by każda osoba wydawała pieniądze i energię na wielokrotne samodzielne pytanie AI. Prowadzone przez społeczność książki mogą stać się bardziej wszechstronne i pluralistyczne: miliony czytelników mogą dzielić uwagę i wkład, tworząc starannie napisane książki zbiorowe jako dobro publiczne.",
  };

  const copy = {
    en: {
      heroKicker: "About",
      heroTitle: "Books for the <em>long tail</em> of thought.",
      heroLead: "ScriptaHub brings together free books that are made to be read slowly, challenged, corrected and taken somewhere new. ScriptaHub combines YouTube’s breadth of discovery with the depth of text: complete books and concise summaries, with audio and video editions planned. Like a new kind of Wikipedia, readers can challenge, improve and extend every edition, while generative AI helps turn useful feedback into better versions. Contributions are judged openly by the value they add, without censorship that can feel arbitrary. Some books make little economic sense for one person to write: an advanced research question, a new idea or a difficult philosophy may have only hundreds or thousands of readers scattered worldwide, making conventional publication and distribution unrealistic. AI can make those books possible as collective works that a community clarifies, challenges and improves; one book can even answer another, with their relationship made visible. Niche thinkers and experts can leave a durable mark and contribute in ways that were previously impractical. That is AI’s value here, beyond the inevitable slop.",
      heroPoints: ["Long-form work for questions that do not fit a feed.", "Niche knowledge, research programmes and speculative worlds.", "A library that improves when readers leave useful traces."],
      missionKicker: "Why this exists", missionTitle: "A public workshop for valuable, unusual books.",
      mission: [
        "ScriptaHub is a platform for content created with generative AI through a research programme on generating intellectually valuable long-form work. It is built for the long tail: distinctive books with few readers, focused niche books, and science fiction that explores different corners of possibility.",
        "The point is to involve a community that can give feedback, propose valuable books and help improve the editions. Access will be free. Contributors whose accepted ideas materially improve a book may be credited in its copyright pages. Instead of asking every reader to pay for an expensive subscription and generate a book alone, the library aims to make niche books discoverable, quality-checked, corrected and strengthened by a community.",
        "ScriptaHub invests in neuro-symbolic technologies for writing and, especially, for checking the quality of generated books. As the collection grows, it will also develop more personal recommendation and value-estimation methods based on interaction history and what a reader explicitly says matters. Those technologies remain private and are not available on this site. You can help now with feedback and ideas for books worth making."
      ],
      discoverKicker: "Find a starting point", discoverTitle: "Discover", search: "Search by keyword", searchEmpty: "No books match that search yet.",
      libraryKicker: "Random books", libraryTitle: "A growing shelf of arguments and worlds.",
      keyword: "Keyword", booksTagged: (count) => `${count} ${count === 1 ? "book" : "books"} tagged`, read: "Read online", short: "Read in 10 min", inLanguage: (label) => `in ${label}`,
    },
    fr: {
      heroKicker: "À propos", heroTitle: "Des livres pour la <em>longue traîne</em> de la pensée.", heroLead: "ScriptaHub réunit des livres gratuits faits pour être lus lentement, discutés, corrigés et emmenés plus loin. ScriptaHub associe l’ampleur de découverte de YouTube à la profondeur du texte : des livres complets et des résumés concis, puis des éditions audio et vidéo à venir. Comme une nouvelle forme de Wikipédia, les lecteurs peuvent discuter, améliorer et prolonger chaque édition, tandis que l’IA générative transforme les retours utiles en meilleures versions. Les contributions sont évaluées ouvertement selon la valeur qu’elles apportent, sans censure pouvant sembler arbitraire. Certains livres n’ont guère de sens économique pour un auteur isolé : une question de recherche avancée, une idée nouvelle ou une philosophie complexe peut ne réunir que quelques centaines ou milliers de lecteurs dispersés dans le monde, rendant l’édition et la distribution classiques irréalistes. L’IA peut rendre ces livres possibles comme œuvres collectives que la communauté clarifie, conteste et améliore ; un livre peut même répondre à un autre, et leur relation devenir visible. Penseurs de niche et experts peuvent laisser une empreinte durable et contribuer de façons autrefois impraticables. C’est ici que réside la valeur de l’IA, au-delà de l’inévitable contenu médiocre.", heroPoints: ["Des textes longs pour les questions qui ne tiennent pas dans un fil.", "Savoirs de niche, programmes de recherche et mondes spéculatifs.", "Une bibliothèque qui s’améliore lorsque les lecteurs laissent des traces utiles."],
      missionKicker: "Pourquoi ce projet", missionTitle: "Un atelier public pour des livres singuliers et précieux.", mission: [
        "ScriptaHub est une plateforme de contenus créés avec l’IA générative dans le cadre d’un programme de recherche sur la production de textes longs à valeur intellectuelle. Elle vise la longue traîne : des livres singuliers à faible lectorat, des ouvrages de niche et de la science-fiction qui explore différentes possibilités.",
        "Le but est d’impliquer une communauté capable de donner des retours, de proposer des livres utiles et d’améliorer les éditions. L’accès sera gratuit. Les contributeurs dont les idées acceptées améliorent réellement un livre pourront être cités dans ses pages de copyright. Plutôt que de demander à chacun de payer un abonnement coûteux pour générer seul son livre, la bibliothèque rend des livres de niche découvrables, contrôlés, corrigés et renforcés par une communauté.",
        "ScriptaHub investit dans des technologies neuro-symboliques d’écriture et surtout de vérification de la qualité des livres générés. À mesure que la collection grandira, nous développerons aussi des recommandations plus personnelles et des méthodes d’estimation de valeur fondées sur l’historique d’interaction et sur ce que le lecteur déclare important. Ces technologies restent privées et ne sont pas disponibles ici. Vous pouvez déjà aider par vos retours et vos idées de livres qui méritent d’exister."
      ],
      discoverKicker: "Trouver un point de départ", discoverTitle: "Explorer", search: "Rechercher par mot-clé", searchEmpty: "Aucun livre ne correspond encore à cette recherche.", libraryKicker: "Livres au hasard", libraryTitle: "Une étagère grandissante d’arguments et de mondes.", keyword: "Mot-clé", booksTagged: (count) => `${count} livre${count > 1 ? "s" : ""} associé${count > 1 ? "s" : ""}`, read: "Lire en ligne", short: "Lire en 10 min", inLanguage: (label) => `en ${label}`,
    },
    de: {
      heroKicker: "Über ScriptaHub", heroTitle: "Bücher für den <em>Long Tail</em> des Denkens.", heroLead: "ScriptaHub versammelt kostenlose Bücher, die langsam gelesen, hinterfragt, korrigiert und weitergedacht werden sollen. ScriptaHub verbindet die Entdeckungsbreite von YouTube mit der Tiefe von Text: vollständige Bücher und prägnante Zusammenfassungen, später auch Audio- und Videoausgaben. Wie bei einer neuen Art Wikipedia können Leser jede Ausgabe hinterfragen, verbessern und erweitern, während generative KI hilfreiches Feedback in bessere Versionen überführt. Beiträge werden transparent nach ihrem Mehrwert beurteilt – ohne Zensur, die willkürlich wirken kann. Manche Bücher ergeben für einen einzelnen Autor wirtschaftlich kaum Sinn: Eine fortgeschrittene Forschungsfrage, eine neue Idee oder eine komplexe Philosophie findet vielleicht nur einige Hundert oder Tausend über die Welt verstreute Leser, sodass herkömmliche Veröffentlichung und Verbreitung unrealistisch sind. KI kann solche Bücher als kollektive Werke ermöglichen, die eine Gemeinschaft klärt, hinterfragt und verbessert; ein Buch kann sogar auf ein anderes antworten und diese Beziehung sichtbar machen. Nischendenker und Fachleute können bleibende Spuren hinterlassen und auf früher kaum mögliche Weise beitragen. Darin liegt hier der Wert der KI – jenseits des unvermeidlichen KI-Einheitsbreis.", heroPoints: ["Langform für Fragen, die nicht in einen Feed passen.", "Nischenwissen, Forschungsprogramme und spekulative Welten.", "Eine Bibliothek, die besser wird, wenn Leser hilfreiche Spuren hinterlassen."],
      missionKicker: "Warum es das gibt", missionTitle: "Eine öffentliche Werkstatt für wertvolle, ungewöhnliche Bücher.", mission: [
        "ScriptaHub ist eine Plattform für mit generativer KI geschaffene Inhalte aus einem Forschungsprogramm zu intellektuell wertvollen Langformtexten. Sie ist für den Long Tail gedacht: unverwechselbare Bücher mit wenigen Lesern, fokussierte Nischenbücher und Science-Fiction für unterschiedliche Möglichkeiten.",
        "Ziel ist eine Gemeinschaft, die Feedback geben, wertvolle Bücher vorschlagen und Ausgaben verbessern kann. Der Zugang bleibt kostenlos. Mitwirkende, deren angenommene Ideen ein Buch wesentlich verbessern, können auf seinen Copyright-Seiten genannt werden. Statt jeden Leser ein teures Abonnement zahlen und allein ein Buch erzeugen zu lassen, macht die Bibliothek Nischenbücher auffindbar, qualitätsgeprüft, korrigiert und durch eine Gemeinschaft stärker.",
        "ScriptaHub investiert in neurosymbolische Technologien für das Schreiben und vor allem für die Qualitätsprüfung generierter Bücher. Mit wachsender Sammlung werden auch persönlichere Empfehlungen und Verfahren zur Wertschätzung entstehen, basierend auf Interaktionsverlauf und ausdrücklich genannten Interessen. Diese Technologien sind privat und auf dieser Website nicht verfügbar. Feedback und Ideen für lohnende Bücher helfen schon jetzt."
      ],
      discoverKicker: "Einen Anfang finden", discoverTitle: "Entdecken", search: "Nach Schlagwort suchen", searchEmpty: "Noch kein Buch passt zu dieser Suche.", libraryKicker: "Zufällige Bücher", libraryTitle: "Ein wachsendes Regal aus Argumenten und Welten.", keyword: "Schlagwort", booksTagged: (count) => `${count} markierte${count === 1 ? "s Buch" : " Bücher"}`, read: "Online lesen", short: "In 10 Min. lesen", inLanguage: (label) => `auf ${label}`,
    },
    es: {
      heroKicker: "Acerca de", heroTitle: "Libros para la <em>larga cola</em> del pensamiento.", heroLead: "ScriptaHub reúne libros gratuitos hechos para leerse despacio, cuestionarse, corregirse y llevarse más lejos. ScriptaHub combina la amplitud de descubrimiento de YouTube con la profundidad del texto: libros completos y resúmenes concisos, y más adelante ediciones de audio y vídeo. Como una nueva clase de Wikipedia, los lectores pueden cuestionar, mejorar y ampliar cada edición, mientras la IA generativa convierte los comentarios útiles en versiones mejores. Las contribuciones se valoran abiertamente por lo que aportan, sin una censura que pueda parecer arbitraria. Algunos libros tienen poco sentido económico para una sola persona: una pregunta de investigación avanzada, una idea nueva o una filosofía compleja quizá solo reúna a cientos o miles de lectores dispersos por el mundo, por lo que publicarla y distribuirla de forma convencional resulta inviable. La IA puede hacer posibles esos libros como obras colectivas que una comunidad aclara, cuestiona y mejora; incluso un libro puede responder a otro y hacer visible su relación. Pensadores de nicho y especialistas pueden dejar una huella duradera y contribuir de maneras antes impracticables. Ahí está el valor de la IA, más allá del inevitable contenido basura.", heroPoints: ["Obras largas para preguntas que no caben en un feed.", "Conocimiento de nicho, programas de investigación y mundos especulativos.", "Una biblioteca que mejora cuando los lectores dejan señales útiles."],
      missionKicker: "Por qué existe", missionTitle: "Un taller público para libros valiosos y poco comunes.", mission: [
        "ScriptaHub es una plataforma de contenidos creados con IA generativa mediante un programa de investigación sobre trabajo intelectual valioso de formato largo. Está pensada para la larga cola: libros singulares con pocos lectores, obras de nicho y ciencia ficción que explora distintas posibilidades.",
        "El objetivo es implicar a una comunidad que pueda aportar comentarios, proponer libros valiosos y mejorar las ediciones. El acceso será gratuito. Las personas cuyas ideas aceptadas mejoren materialmente un libro podrán figurar en sus páginas de copyright. En lugar de pedir a cada lector que pague una suscripción costosa y genere un libro en solitario, la biblioteca busca hacer descubribles libros de nicho, revisados, corregidos y fortalecidos por una comunidad.",
        "ScriptaHub invierte en tecnologías neurosimbólicas para escribir y, sobre todo, verificar la calidad de los libros generados. A medida que crezca la colección, desarrollará recomendaciones más personales y métodos para estimar valor a partir del historial de interacción y de lo que cada lector declara importante. Estas tecnologías son privadas y no están disponibles en el sitio. Ya puedes ayudar con comentarios e ideas de libros que valga la pena crear."
      ],
      discoverKicker: "Encuentra un punto de partida", discoverTitle: "Descubre", search: "Buscar por palabra clave", searchEmpty: "Aún no hay libros que coincidan con esa búsqueda.", libraryKicker: "Libros al azar", libraryTitle: "Un estante creciente de argumentos y mundos.", keyword: "Palabra clave", booksTagged: (count) => `${count} libro${count !== 1 ? "s" : ""} etiquetado${count !== 1 ? "s" : ""}`, read: "Leer en línea", short: "Leer en 10 min", inLanguage: (label) => `en ${label}`,
    },
    pt: {
      heroKicker: "Sobre", heroTitle: "Livros para a <em>cauda longa</em> do pensamento.", heroLead: "ScriptaHub reúne livros gratuitos feitos para serem lidos devagar, questionados, corrigidos e levados adiante. A ScriptaHub combina a amplitude de descoberta do YouTube com a profundidade do texto: livros completos e resumos concisos, com edições em áudio e vídeo previstas para o futuro. Como uma nova forma de Wikipédia, os leitores podem questionar, melhorar e ampliar cada edição, enquanto a IA generativa transforma feedback útil em versões melhores. As contribuições são avaliadas abertamente pelo valor que acrescentam, sem censura que possa parecer arbitrária. Alguns livros fazem pouco sentido econômico para uma única pessoa escrever: uma questão avançada de pesquisa, uma ideia nova ou uma filosofia complexa talvez encontre apenas centenas ou milhares de leitores espalhados pelo mundo, tornando inviáveis a publicação e a distribuição convencionais. A IA pode tornar esses livros possíveis como obras coletivas que uma comunidade esclarece, questiona e melhora; um livro pode até responder a outro, deixando visível a relação entre eles. Pensadores de nicho e especialistas podem deixar uma marca duradoura e contribuir de formas antes impraticáveis. É aí que está o valor da IA, para além do inevitável conteúdo descartável.", heroPoints: ["Textos longos para perguntas que não cabem em um feed.", "Conhecimento de nicho, programas de pesquisa e mundos especulativos.", "Uma biblioteca que melhora quando leitores deixam rastros úteis."],
      missionKicker: "Por que isto existe", missionTitle: "Uma oficina pública para livros valiosos e incomuns.", mission: [
        "ScriptaHub é uma plataforma de conteúdo criado com IA generativa por meio de um programa de pesquisa sobre obras longas de valor intelectual. Ela é feita para a cauda longa: livros distintos com poucos leitores, obras de nicho e ficção científica que explora diferentes possibilidades.",
        "O objetivo é envolver uma comunidade que possa dar feedback, propor livros valiosos e melhorar as edições. O acesso será gratuito. Pessoas cujas ideias aceitas melhorem materialmente um livro poderão ser mencionadas em suas páginas de copyright. Em vez de pedir que cada leitor pague uma assinatura cara e gere sozinho um livro, a biblioteca torna livros de nicho descobríveis, avaliados, corrigidos e fortalecidos por uma comunidade.",
        "ScriptaHub investe em tecnologias neurossimbólicas para escrita e, principalmente, para verificar a qualidade dos livros gerados. Conforme a coleção crescer, desenvolverá recomendações mais pessoais e métodos de estimativa de valor baseados no histórico de interação e no que cada leitor declara importante. Essas tecnologias são privadas e não estão disponíveis no site. Você já pode ajudar com feedback e ideias de livros que valha a pena criar."
      ],
      discoverKicker: "Encontre um ponto de partida", discoverTitle: "Descubra", search: "Buscar por palavra-chave", searchEmpty: "Ainda não há livros para essa busca.", libraryKicker: "Livros aleatórios", libraryTitle: "Uma prateleira crescente de argumentos e mundos.", keyword: "Palavra-chave", booksTagged: (count) => `${count} livro${count !== 1 ? "s" : ""} marcado${count !== 1 ? "s" : ""}`, read: "Ler online", short: "Ler em 10 min", inLanguage: (label) => `em ${label}`,
    },
    it: {
      heroKicker: "Informazioni", heroTitle: "Libri per la <em>coda lunga</em> del pensiero.", heroLead: "ScriptaHub riunisce libri gratuiti fatti per essere letti lentamente, messi in discussione, corretti e portati oltre. ScriptaHub unisce l’ampiezza della scoperta di YouTube alla profondità del testo: libri completi e sintesi concise, con edizioni audio e video previste in futuro. Come una nuova forma di Wikipedia, i lettori possono mettere alla prova, migliorare ed estendere ogni edizione, mentre l’IA generativa trasforma i feedback utili in versioni migliori. I contributi vengono valutati apertamente per il valore che aggiungono, senza una censura che possa sembrare arbitraria. Alcuni libri hanno poco senso economico per un singolo autore: una domanda di ricerca avanzata, un’idea nuova o una filosofia complessa può interessare soltanto centinaia o migliaia di lettori sparsi nel mondo, rendendo irrealistiche pubblicazione e distribuzione tradizionali. L’IA può rendere possibili questi libri come opere collettive che una comunità chiarisce, mette alla prova e migliora; un libro può persino rispondere a un altro, rendendo visibile il loro legame. Pensatori di nicchia ed esperti possono lasciare un’impronta duratura e contribuire in modi prima impraticabili. È questo il valore dell’IA, oltre l’inevitabile contenuto scadente.", heroPoints: ["Opere lunghe per domande che non entrano in un feed.", "Conoscenza di nicchia, programmi di ricerca e mondi speculativi.", "Una biblioteca che migliora quando i lettori lasciano tracce utili."],
      missionKicker: "Perché esiste", missionTitle: "Un laboratorio pubblico per libri preziosi e insoliti.", mission: [
        "ScriptaHub è una piattaforma di contenuti creati con IA generativa attraverso un programma di ricerca sulla produzione di opere lunghe di valore intellettuale. È pensata per la coda lunga: libri distintivi con pochi lettori, testi di nicchia e fantascienza che esplora possibilità diverse.",
        "Lo scopo è coinvolgere una comunità capace di offrire feedback, proporre libri preziosi e migliorare le edizioni. L’accesso sarà gratuito. I contributori le cui idee accettate migliorano materialmente un libro potranno essere citati nelle sue pagine di copyright. Invece di chiedere a ogni lettore di pagare un costoso abbonamento e generare da solo il proprio libro, la biblioteca rende i libri di nicchia scopribili, controllati, corretti e rafforzati dalla comunità.",
        "ScriptaHub investe in tecnologie neuro-simboliche per la scrittura e soprattutto per verificare la qualità dei libri generati. Con la crescita della collezione svilupperà anche raccomandazioni più personali e metodi di stima del valore basati sulla cronologia delle interazioni e su ciò che il lettore dichiara importante. Queste tecnologie restano private e non sono disponibili sul sito. Puoi già aiutare con feedback e idee di libri che meritano di essere creati."
      ],
      discoverKicker: "Trova un punto di partenza", discoverTitle: "Scopri", search: "Cerca per parola chiave", searchEmpty: "Non ci sono ancora libri per questa ricerca.", libraryKicker: "Libri casuali", libraryTitle: "Uno scaffale crescente di argomenti e mondi.", keyword: "Parola chiave", booksTagged: (count) => `${count} libr${count === 1 ? "o" : "i"} associat${count === 1 ? "o" : "i"}`, read: "Leggi online", short: "Leggi in 10 min", inLanguage: (label) => `in ${label}`,
    },
    ro: {
      heroKicker: "Despre", heroTitle: "Cărți pentru <em>coada lungă</em> a gândirii.", heroLead: "ScriptaHub reunește cărți gratuite făcute pentru a fi citite lent, puse sub semnul întrebării, corectate și duse mai departe. ScriptaHub combină varietatea și ușurința descoperirii de pe YouTube cu profunzimea textului: cărți complete și rezumate concise, iar în viitor ediții audio și video. Ca un nou tip de Wikipedia, cititorii pot pune sub semnul întrebării, îmbunătăți și extinde fiecare ediție, iar IA generativă transformă feedbackul valoros în versiuni mai bune. Contribuțiile sunt evaluate deschis după valoarea adăugată, fără o cenzură ce poate părea arbitrară. Unele cărți nu au sens economic pentru un singur autor: o temă avansată de cercetare, o idee nouă sau o filosofie complexă poate avea doar sute ori mii de cititori răspândiți în întreaga lume, ceea ce face nerealiste publicarea și distribuția convenționale. AI-ul poate face posibile aceste cărți ca opere colective pe care comunitatea le clarifică, le pune la încercare și le îmbunătățește; o carte poate chiar răspunde alteia, iar legătura dintre ele poate deveni vizibilă. Gânditorii de nișă și experții își pot lăsa amprenta și pot contribui în moduri care înainte nu erau practice. Aici se află valoarea AI-ului, dincolo de inevitabilul conținut superficial.", heroPoints: ["Conținut lung pentru întrebări care nu încap într-un feed.", "Cunoaștere de nișă, programe de cercetare și lumi speculative.", "O bibliotecă ce devine mai bună când cititorii lasă urme utile."],
      missionKicker: "De ce există", missionTitle: "Un atelier public pentru cărți valoroase și neobișnuite.", mission: [
        "ScriptaHub este o platformă de conținut creat cu IA generativă printr-un program de cercetare privind generarea de conținut lung valoros intelectual. Este construită pentru coada lungă: cărți distincte cu puțini cititori, cărți de nișă și science-fiction care explorează colțuri diferite ale posibilului.",
        "Scopul este implicarea unei comunități care poate oferi feedback, propune cărți valoroase și îmbunătăți edițiile. Accesul va fi gratuit. Contribuitorii ale căror idei acceptate îmbunătățesc substanțial o carte pot fi menționați în paginile ei de copyright. În loc ca fiecare cititor să plătească un abonament scump și să își genereze singur o carte, biblioteca face cărțile de nișă ușor de găsit, verificate calitativ, corectate și întărite de comunitate.",
        "ScriptaHub investește în tehnologii neuro-simbolice pentru scriere și mai ales pentru verificarea calității cărților generate. Pe măsură ce colecția crește, va dezvolta recomandări mai personalizate și metode de estimare a valorii bazate pe istoricul interacțiunilor și pe ceea ce cititorul declară explicit că este important. Aceste tehnologii sunt private și nu sunt disponibile pe site. Ne poți ajuta deja prin feedback și idei de cărți care merită create."
      ],
      discoverKicker: "Găsește un punct de plecare", discoverTitle: "Descoperă", search: "Caută după cuvânt-cheie", searchEmpty: "Încă nu există cărți potrivite pentru această căutare.", libraryKicker: "Cărți aleatorii", libraryTitle: "Un raft în creștere de argumente și lumi.", keyword: "Cuvânt-cheie", booksTagged: (count) => `${count} ${count === 1 ? "carte etichetată" : "cărți etichetate"}`, read: "Citește online", short: "Citește în 10 min", inLanguage: (label) => `în ${label}`,
    },
    pl: {
      heroKicker: "O projekcie", heroTitle: "Książki dla <em>długiego ogona</em> myśli.", heroLead: "ScriptaHub łączy bezpłatne książki stworzone po to, by czytać je powoli, podważać, poprawiać i rozwijać dalej. ScriptaHub łączy zasięg odkrywania znany z YouTube z głębią tekstu: pełne książki i zwięzłe podsumowania, a w przyszłości także wydania audio i wideo. Jak nowy rodzaj Wikipedii, pozwala czytelnikom kwestionować, ulepszać i rozwijać każde wydanie, a generatywna AI przekształca wartościowe opinie w lepsze wersje. Wkład jest oceniany otwarcie według wartości, którą wnosi, bez cenzury mogącej sprawiać wrażenie arbitralnej. Pisanie niektórych książek przez jedną osobę nie ma ekonomicznego sensu: zaawansowane pytanie badawcze, nowa idea lub złożona filozofia może znaleźć zaledwie setki albo tysiące czytelników rozsianych po świecie, przez co tradycyjne wydanie i dystrybucja są nierealne. AI może umożliwić powstawanie takich książek jako dzieł zbiorowych, które społeczność objaśnia, podważa i ulepsza; jedna książka może nawet odpowiadać drugiej, a ich związek staje się widoczny. Niszowi myśliciele i eksperci mogą pozostawić trwały ślad i wnosić wkład w sposób wcześniej niepraktyczny. Na tym polega wartość AI — poza nieuniknioną zalewą miałkich treści.", heroPoints: ["Długa forma dla pytań, które nie mieszczą się w feedzie.", "Wiedza niszowa, programy badawcze i spekulatywne światy.", "Biblioteka, która staje się lepsza, gdy czytelnicy zostawiają użyteczne ślady."],
      missionKicker: "Dlaczego istnieje", missionTitle: "Publiczna pracownia dla wartościowych i niezwykłych książek.", mission: [
        "ScriptaHub to platforma treści tworzonych z generatywną AI w ramach programu badawczego nad wartościową intelektualnie długą formą. Jest przeznaczona dla długiego ogona: wyróżniających się książek z niewielką liczbą czytelników, książek niszowych i science fiction badającego różne możliwości.",
        "Celem jest zaangażowanie społeczności, która może dawać opinie, proponować wartościowe książki i ulepszać wydania. Dostęp będzie bezpłatny. Współtwórcy, których przyjęte pomysły istotnie poprawią książkę, mogą zostać wymienieni na jej stronach copyright. Zamiast wymagać od każdego czytelnika drogiej subskrypcji i samodzielnego generowania książki, biblioteka czyni niszowe książki odkrywalnymi, sprawdzonymi jakościowo, poprawionymi i wzmocnionymi przez społeczność.",
        "ScriptaHub inwestuje w neurosymboliczne technologie pisania, a przede wszystkim w weryfikację jakości generowanych książek. Wraz ze wzrostem kolekcji będą powstawać bardziej osobiste rekomendacje i metody szacowania wartości na podstawie historii interakcji oraz tego, co czytelnik wyraźnie deklaruje jako ważne. Technologie te pozostają prywatne i nie są dostępne na stronie. Już teraz możesz pomóc opiniami i pomysłami na książki warte stworzenia."
      ],
      discoverKicker: "Znajdź punkt wyjścia", discoverTitle: "Odkrywaj", search: "Szukaj po słowie kluczowym", searchEmpty: "Nie ma jeszcze książek pasujących do tego wyszukiwania.", libraryKicker: "Losowe książki", libraryTitle: "Rosnąca półka argumentów i światów.", keyword: "Słowo kluczowe", booksTagged: (count) => `${count} oznaczon${count === 1 ? "a książka" : "ych książek"}`, read: "Czytaj online", short: "Czytaj w 10 min", inLanguage: (label) => `po ${label}`,
    },
  };

  const supported = collection.supportedLanguages.map((item) => item.code);
  const scriptUrl = document.currentScript?.src;
  const siteRootUrl = scriptUrl ? new URL("../", scriptUrl) : new URL("./", location.href);
  const siteScaleKey = "scripta-site-scale";
  const siteThemeKey = "scripta-site-theme";
  const cloudInstruction = {
    en: "drag to rotate · Ctrl-drag to move · scroll to zoom", fr: "glisser pour tourner · Ctrl-glisser pour déplacer · défiler pour zoomer",
    de: "ziehen zum Drehen · Strg-Ziehen zum Verschieben · scrollen zum Zoomen", es: "arrastra para girar · Ctrl-arrastrar para mover · desplázate para ampliar",
    pt: "arraste para girar · Ctrl-arraste para mover · role para ampliar", it: "trascina per ruotare · Ctrl-trascina per spostare · scorri per ingrandire",
    ro: "trage pentru rotire · Ctrl-trage pentru deplasare · derulează pentru zoom", pl: "przeciągnij, aby obrócić · Ctrl-przeciągnij, aby przesunąć · przewiń, aby przybliżyć",
  };
  const cloudPreviewInstruction = {
    en: "click to enlarge", fr: "cliquez pour agrandir", de: "zum Vergrößern klicken", es: "haz clic para ampliar",
    pt: "clique para ampliar", it: "clicca per ingrandire", ro: "apasă pentru mărire", pl: "kliknij, aby powiększyć",
  };
  const cloudCloseLabel = {
    en: "Close keyword cloud", fr: "Fermer le nuage de mots-clés", de: "Schlagwortwolke schließen", es: "Cerrar nube de palabras clave",
    pt: "Fechar nuvem de palavras-chave", it: "Chiudi nuvola di parole chiave", ro: "Închide norul de cuvinte-cheie", pl: "Zamknij chmurę słów kluczowych",
  };
  const homeLoadingLabels = {
    en: "Loading the library…", fr: "Chargement de la bibliothèque…", de: "Bibliothek wird geladen…", es: "Cargando la biblioteca…",
    pt: "A carregar a biblioteca…", it: "Caricamento della biblioteca…", ro: "Se încarcă biblioteca…", pl: "Ładowanie biblioteki…",
  };
  const featuredBooks = (() => {
    const pool = [...collection.books];
    for (let index = pool.length - 1; index > 0; index -= 1) {
      const swap = Math.floor(Math.random() * (index + 1));
      [pool[index], pool[swap]] = [pool[swap], pool[index]];
    }
    return pool;
  })();
  const missionStripBooks = featuredBooks.filter((book) => Object.values(book.thumbnailUrl || {}).some(Boolean));
  const queryLanguage = () => new URLSearchParams(location.search).get("lang")?.toLowerCase().split("-")[0];
  const browserLanguage = () => (navigator.languages || [navigator.language || "en"])
    .map((item) => String(item).toLowerCase().split("-")[0]).find((item) => supported.includes(item));
  const selectedLanguage = () => {
    const requested = queryLanguage();
    const pageLanguage = document.body.dataset.bookLanguage;
    const stored = localStorage.getItem("scripta-language");
    return [requested, pageLanguage, stored, browserLanguage(), "en"].find((item) => supported.includes(item));
  };
  const savedSiteScale = () => {
    const raw = localStorage.getItem(siteScaleKey);
    if (raw === null) return 1;
    const value = Number(raw);
    return Number.isFinite(value) ? Math.max(.82, Math.min(1.24, value)) : 1;
  };
  const applySiteScale = (value, persist = false) => {
    const scale = Math.max(.82, Math.min(1.24, value));
    document.documentElement.style.setProperty("--site-scale", scale.toFixed(2));
    document.querySelectorAll("[data-site-size]").forEach((node) => { node.textContent = `${Math.round(scale * 100)}%`; });
    if (persist) try { localStorage.setItem(siteScaleKey, scale.toFixed(2)); } catch { /* Storage is optional. */ }
    requestAnimationFrame(() => document.dispatchEvent(new CustomEvent("scriptahub:scalechange", { detail: { scale } })));
  };
  const setupSiteScale = () => {
    applySiteScale(savedSiteScale());
    document.querySelectorAll("[data-site-smaller]").forEach((button) => { button.onclick = () => applySiteScale(savedSiteScale() - .06, true); });
    document.querySelectorAll("[data-site-larger]").forEach((button) => { button.onclick = () => applySiteScale(savedSiteScale() + .06, true); });
    document.querySelectorAll("[data-site-size]").forEach((button) => { button.onclick = () => applySiteScale(1, true); });
  };
  const storedTheme = () => {
    try { return localStorage.getItem(siteThemeKey) === "dark" ? "dark" : "light"; } catch { return "light"; }
  };
  const ensureThemeToggle = () => {
    document.querySelectorAll(".theme-switcher").forEach((control) => {
      control.removeAttribute("role");
      control.removeAttribute("aria-label");
      if (control.querySelector("[data-theme-toggle]")) return;
      control.innerHTML = '<button type="button" data-theme-toggle></button>';
    });
  };
  const applyTheme = (theme, persist = false) => {
    const selected = theme === "dark" ? "dark" : "light";
    document.documentElement.dataset.theme = selected;
    document.querySelectorAll("[data-theme-toggle]").forEach((button) => {
      button.textContent = selected === "dark" ? "☾" : "☼";
      button.title = selected === "dark" ? "Switch to light appearance" : "Switch to dark appearance";
      button.setAttribute("aria-label", button.title);
      button.setAttribute("aria-pressed", String(selected === "dark"));
    });
    if (persist) {
      try { localStorage.setItem(siteThemeKey, selected); } catch { /* Storage may be unavailable. */ }
    }
  };
  const setupTheme = () => {
    ensureThemeToggle();
    applyTheme(storedTheme());
    document.querySelectorAll("[data-theme-toggle]").forEach((button) => {
      button.addEventListener("click", () => applyTheme(document.documentElement.dataset.theme === "dark" ? "light" : "dark", true));
    });
  };
  const normalise = (value) => String(value).normalize("NFD").replace(/[\u0300-\u036f]/g, "").toLowerCase();
  const displayKeyword = (value) => String(value).split(" ").map((word) => word ? word[0].toLocaleUpperCase() + word.slice(1) : word).join(" ");
  const escape = (value) => String(value).replace(/[&<>'"]/g, (character) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", "'": "&#39;", '"': "&quot;" })[character]);
  const compactDescription = (value, maximum = 260) => {
    const clean = String(value || "").replace(/\s+/g, " ").trim();
    if (clean.length <= maximum) return clean;
    const clipped = clean.slice(0, maximum + 1).replace(/\s+\S*$/, "").trim();
    return `${clipped || clean.slice(0, maximum)}…`;
  };
  const isBookPage = () => document.body.dataset.bookPage === "true";
  const isAppPage = () => document.body.dataset.appPage === "true";
  const assetPath = (path) => path;
  const keywordSearchHref = (keyword, language) => {
    const params = new URLSearchParams({ lang: language, keyword: keyword.id });
    return `index.html?${params.toString()}`;
  };
  const languageName = (language) => collection.supportedLanguages.find((item) => item.code === language)?.name || language;

  function replaceText(selector, value, htmlValue = false) {
    const node = document.querySelector(selector);
    if (!node) return;
    if (htmlValue) node.innerHTML = value;
    else node.textContent = value;
  }

  function localizeGlobalHeader(language) {
    document.querySelectorAll("[data-create-link]").forEach((link) => {
      link.textContent = createLabels[language];
      link.setAttribute("aria-label", createLabels[language]);
      link.title = createLabels[language];
      const url = new URL(link.getAttribute("href"), location.href);
      url.searchParams.set("lang", language);
      link.href = url.href;
    });
    document.querySelectorAll(".site-header .header-tools").forEach((tools) => {
      const create = tools.querySelector("[data-create-link]");
      let librarian = tools.querySelector("[data-header-librarian]");
      if (!librarian) {
        librarian = document.createElement("a");
        librarian.className = "header-librarian";
        librarian.dataset.headerLibrarian = "";
        librarian.dataset.introLibrarian = "";
        create?.insertAdjacentElement("afterend", librarian);
      }
      librarian.textContent = librarianSectionLabels[language].title;
      librarian.setAttribute("aria-label", librarianSectionLabels[language].title);
      librarian.title = librarianSectionLabels[language].title;
      librarian.href = new URL(`index.html?lang=${language}#ask-librarian`, siteRootUrl).href;
    });
    const footerWords = legalFooterLabels[language];
    Object.entries(footerWords).forEach(([key, label]) => {
      document.querySelectorAll(`[data-footer-${key}]`).forEach((link) => { link.textContent = label; });
    });
    document.querySelectorAll("[data-legal-link]").forEach((link) => {
      const url = new URL(link.getAttribute("href"), location.href);
      url.searchParams.set("lang", language);
      link.href = url.href;
    });
  }

  function setupLibrarianLaunch(language) {
    const form = document.querySelector("[data-librarian-launch]");
    if (!form) return;
    if (form._speechRecognition) {
      form._speechRecognition.onend = null;
      form._speechRecognition.abort();
      form._speechRecognition = null;
    }
    const words = librarianLaunchLabels[language];
    const input = form.querySelector("[data-librarian-query]");
    const label = form.querySelector("[data-librarian-label]");
    const button = form.querySelector("[data-librarian-button]");
    const dictate = form.querySelector("[data-librarian-dictate]");
    const speechStatus = form.querySelector("[data-librarian-speech-status]");
    input.placeholder = words.label;
    label.textContent = words.label;
    button.textContent = words.button;
    dictate.textContent = "";
    dictate.setAttribute("aria-label", words.dictate);
    dictate.title = words.dictate;
    const SpeechRecognition = globalThis.SpeechRecognition || globalThis.webkitSpeechRecognition;
    const speechLanguages = { en: "en-US", fr: "fr-FR", de: "de-DE", es: "es-ES", pt: "pt-PT", it: "it-IT", ro: "ro-RO", pl: "pl-PL" };
    const resetDictationButton = () => {
      dictate.setAttribute("aria-pressed", "false");
      dictate.setAttribute("aria-label", words.dictate);
      dictate.title = words.dictate;
      speechStatus.textContent = "";
    };
    if (!SpeechRecognition) {
      dictate.disabled = true;
      dictate.title = words.unavailable;
      speechStatus.textContent = words.unavailable;
    } else {
      dictate.disabled = false;
      let recognition = null;
      dictate.onclick = () => {
        if (recognition) {
          recognition.stop();
          return;
        }
        const startingText = input.value.trim();
        recognition = new SpeechRecognition();
        form._speechRecognition = recognition;
        recognition.lang = speechLanguages[language] || language;
        recognition.continuous = true;
        recognition.interimResults = true;
        recognition.onstart = () => {
          dictate.setAttribute("aria-pressed", "true");
          dictate.setAttribute("aria-label", words.stop);
          dictate.title = words.stop;
          speechStatus.textContent = words.listening;
        };
        recognition.onresult = (event) => {
          let transcript = "";
          for (let index = 0; index < event.results.length; index += 1) transcript += event.results[index][0].transcript;
          input.value = [startingText, transcript.trim()].filter(Boolean).join(startingText ? " " : "");
          input.dispatchEvent(new Event("input", { bubbles: true }));
        };
        recognition.onerror = () => { speechStatus.textContent = words.unavailable; };
        recognition.onend = () => {
          recognition = null;
          form._speechRecognition = null;
          resetDictationButton();
        };
        recognition.start();
      };
      resetDictationButton();
    }
    form.onsubmit = (event) => {
      event.preventDefault();
      const query = input.value.trim();
      if (!query) {
        input.focus();
        return;
      }
      const params = new URLSearchParams({ lang: language });
      const request = new URLSearchParams({ request: query });
      location.href = `librarian/index.html?${params.toString()}#${request.toString()}`;
    };
  }

  function setupMissionBookTooltips(container) {
    let tooltip = document.querySelector("[data-mission-book-tooltip]");
    if (!tooltip) {
      tooltip = document.createElement("div");
      tooltip.className = "mission-book-tooltip";
      tooltip.dataset.missionBookTooltip = "";
      tooltip.setAttribute("role", "dialog");
      tooltip.hidden = true;
      tooltip.innerHTML = '<strong data-tooltip-title></strong><p data-tooltip-description></p><a data-tooltip-link></a>';
      document.body.append(tooltip);
    }
    tooltip.hidden = true;
    if (container.dataset.tooltipBound) return;
    container.dataset.tooltipBound = "true";

    let activeIcon = null;
    let hideTimer = 0;
    const cancelHide = () => {
      if (!hideTimer) return;
      clearTimeout(hideTimer);
      hideTimer = 0;
    };
    const hide = () => {
      cancelHide();
      activeIcon?.classList.remove("has-open-tooltip");
      activeIcon = null;
      tooltip.hidden = true;
    };
    const scheduleHide = () => {
      cancelHide();
      hideTimer = setTimeout(hide, 180);
    };
    const place = (icon) => {
      if (tooltip.hidden || !icon?.isConnected) return;
      const padding = 12;
      const gap = 11;
      const anchor = icon.getBoundingClientRect();
      const bounds = tooltip.getBoundingClientRect();
      let left = anchor.left + anchor.width / 2 - bounds.width / 2;
      let top = anchor.top - bounds.height - gap;
      if (top < padding) top = anchor.bottom + gap;
      tooltip.style.left = `${Math.max(padding, Math.min(left, window.innerWidth - bounds.width - padding))}px`;
      tooltip.style.top = `${Math.max(padding, Math.min(top, window.innerHeight - bounds.height - padding))}px`;
    };
    const show = (icon) => {
      if (!icon || !container.contains(icon)) return;
      cancelHide();
      activeIcon?.classList.remove("has-open-tooltip");
      activeIcon = icon;
      activeIcon.classList.add("has-open-tooltip");
      tooltip.querySelector("[data-tooltip-title]").textContent = icon.dataset.bookTitle;
      tooltip.querySelector("[data-tooltip-description]").textContent = icon.dataset.bookDescription;
      const link = tooltip.querySelector("[data-tooltip-link]");
      link.textContent = icon.dataset.bookAction;
      link.href = icon.href;
      tooltip.setAttribute("aria-label", icon.dataset.bookTitle);
      tooltip.hidden = false;
      place(icon);
    };
    container.addEventListener("pointerover", (event) => {
      const icon = event.target.closest("[data-mission-book]");
      if (!icon || icon === activeIcon) return;
      show(icon);
    });
    container.addEventListener("pointerout", (event) => {
      if (!activeIcon || activeIcon.contains(event.relatedTarget) || tooltip.contains(event.relatedTarget)) return;
      scheduleHide();
    });
    container.addEventListener("focusin", (event) => show(event.target.closest("[data-mission-book]")));
    container.addEventListener("focusout", (event) => {
      if (activeIcon?.contains(event.relatedTarget) || tooltip.contains(event.relatedTarget)) return;
      scheduleHide();
    });
    tooltip.addEventListener("pointerenter", cancelHide);
    tooltip.addEventListener("pointerleave", scheduleHide);
    tooltip.addEventListener("focusin", cancelHide);
    tooltip.addEventListener("focusout", (event) => { if (!tooltip.contains(event.relatedTarget)) scheduleHide(); });
    window.addEventListener("blur", hide);
    window.addEventListener("scroll", hide, { passive: true });
    window.addEventListener("resize", () => place(activeIcon), { passive: true });
    document.addEventListener("keydown", (event) => { if (event.key === "Escape") hide(); });
  }

  function missionBookIconMarkup(book, language, index) {
    const thumbnail = book.thumbnailUrl?.[language] || book.thumbnailUrl?.en;
    if (!thumbnail) return "";
    const title = book.title?.[language] || book.title?.en || "";
    const description = compactDescription(book.shortDescription?.[language] || book.shortDescription?.en);
    const bookHref = book.editions?.[language]?.book || book.editions?.en?.book;
    const action = cardActions[language].details;
    return `<a class="mission-book-icon" href="${escape(assetPath(bookHref))}" aria-label="${escape(`${action}: ${title}`)}" data-mission-book data-book-id="${escape(book.id)}" data-book-title="${escape(title)}" data-book-description="${escape(description)}" data-book-action="${escape(action)}" style="--book-tilt:${((index % 7) - 3) * .42}deg"><img src="${escape(assetPath(thumbnail))}" alt="" loading="lazy" decoding="async"></a>`;
  }

  function featuredBookMarkup(book, language) {
    const title = book.title?.[language] || book.title?.en || "";
    const description = book.shortDescription?.[language] || book.shortDescription?.en || "";
    const bookHref = book.editions?.[language]?.book || book.editions?.en?.book;
    const labels = cardActions[language];
    const keywords = (book.keywords?.[language] || book.keywords?.en || []).slice(0, 5);
    const status = book.publicationLabel?.[language] ? `<p class="publication-status">${escape(book.publicationLabel[language])}</p>` : "";
    return `<div class="featured-book-copy"><p class="eyebrow">${escape(featuredBookLabels[language])}</p><p class="featured-book-category">${escape(book.category)}</p>${status}<h2><a href="${escape(assetPath(bookHref))}">${escape(title)}</a></h2><div class="featured-book-keywords" aria-label="${escape(featuredBookLabels[language])}">${keywords.map((keyword) => `<span>${escape(keyword)}</span>`).join("")}</div><p class="featured-book-description">${escape(description)}</p><nav class="book-card-actions featured-book-actions"><a class="book-card-details" href="${escape(assetPath(bookHref))}">${escape(labels.details)}</a></nav></div>`;
  }

  function setupMissionBookStrip(container, language, details) {
    container._disposeMissionStrip?.();
    const pool = [...missionStripBooks];
    const pending = new Set();
    let poolIndex = 0;
    let slotCount = 0;
    let replacementSlot = 0;
    let visibleBooks = [];
    let disposed = false;

    const syncFeaturedCardHeight = () => {
      if (!details) return;
      if (globalThis.matchMedia?.("(max-width: 590px)").matches) {
        details.style.removeProperty("height");
        return;
      }
      const coverHeight = container.getBoundingClientRect().height;
      if (coverHeight <= 1) return;
      const nextHeight = `${coverHeight.toFixed(1)}px`;
      if (details.style.height !== nextHeight) details.style.height = nextHeight;
    };

    const nextBook = (excluded = new Set()) => {
      for (let attempt = 0; attempt < pool.length; attempt += 1) {
        const book = pool[poolIndex % pool.length];
        poolIndex += 1;
        if (!excluded.has(book.id)) return book;
      }
      return pool[poolIndex++ % pool.length];
    };
    const renderSlots = () => {
      const availableWidth = Math.max(220, container.clientWidth);
      const featuredCover = container.classList.contains("mission-featured-cover");
      const stacked = globalThis.matchMedia?.("(max-width: 860px)").matches;
      const cloud = document.querySelector("[data-keyword-cloud]");
      const missionCopy = document.querySelector("[data-mission-copy]");
      const availableHeight = !stacked && cloud && missionCopy
        ? cloud.getBoundingClientRect().bottom - missionCopy.getBoundingClientRect().bottom - 8
        : 100;
      // Let the covers consume the real vertical room left by the copy. This
      // is especially important at smaller site scales: fewer, legible books
      // are preferable to many tiny icons above a large empty area.
      const coverHeight = featuredCover ? availableWidth * 1.5 : Math.max(96, Math.min(190, availableHeight - 8));
      const coverWidth = coverHeight * 2 / 3;
      container.style.setProperty("--mission-book-height", `${coverHeight.toFixed(1)}px`);
      container.style.setProperty("--mission-book-width", `${coverWidth.toFixed(1)}px`);
      container.style.setProperty("--mission-strip-height", `${(coverHeight + 8).toFixed(1)}px`);
      const desiredCount = featuredCover ? 1 : Math.max(3, Math.floor((availableWidth - 24 + 9) / (coverWidth + 9)));
      if (desiredCount === slotCount && container.firstElementChild) {
        syncFeaturedCardHeight();
        return;
      }
      slotCount = desiredCount;
      document.querySelector("[data-mission-book-tooltip]")?.setAttribute("hidden", "");
      visibleBooks = visibleBooks.slice(0, slotCount);
      const excluded = new Set(visibleBooks.map((book) => book.id));
      while (visibleBooks.length < slotCount) {
        const book = nextBook(excluded);
        visibleBooks.push(book);
        excluded.add(book.id);
      }
      container.innerHTML = `<div class="mission-book-set">${visibleBooks.map((book, index) => missionBookIconMarkup(book, language, index)).join("")}</div>`;
      if (details && visibleBooks[0]) details.innerHTML = featuredBookMarkup(visibleBooks[0], language);
      syncFeaturedCardHeight();
    };
    const replaceIcon = (icon) => {
      const slotIndex = [...container.querySelectorAll("[data-mission-book]")].indexOf(icon);
      const visibleIds = new Set([...container.querySelectorAll("[data-book-id]")].map((item) => item.dataset.bookId));
      const replacement = nextBook(visibleIds);
      icon.classList.add("is-leaving");
      details?.classList.add("is-card-leaving");
      const swapTimer = setTimeout(() => {
        pending.delete(swapTimer);
        if (disposed || !icon.isConnected) return;
        const replacementMarkup = document.createElement("template");
        replacementMarkup.innerHTML = missionBookIconMarkup(replacement, language, Math.floor(Math.random() * 7));
        const fresh = replacementMarkup.content.firstElementChild;
        icon.dataset.bookId = fresh.dataset.bookId;
        icon.dataset.bookTitle = fresh.dataset.bookTitle;
        icon.dataset.bookDescription = fresh.dataset.bookDescription;
        icon.dataset.bookAction = fresh.dataset.bookAction;
        icon.href = fresh.href;
        icon.setAttribute("aria-label", fresh.getAttribute("aria-label"));
        icon.style.cssText = fresh.style.cssText;
        icon.querySelector("img").src = fresh.querySelector("img").src;
        icon.classList.remove("is-leaving");
        icon.classList.add("is-entering");
        visibleBooks[slotIndex] = replacement;
        if (details?.isConnected) {
          details.innerHTML = featuredBookMarkup(replacement, language);
          details.classList.remove("is-card-leaving");
          details.classList.add("is-card-entering");
          const cardTimer = setTimeout(() => {
            pending.delete(cardTimer);
            details.classList.remove("is-card-entering");
          }, 480);
          pending.add(cardTimer);
        }
        const arriveTimer = setTimeout(() => {
          pending.delete(arriveTimer);
          icon.classList.remove("is-entering");
        }, 420);
        pending.add(arriveTimer);
      }, 220);
      pending.add(swapTimer);
    };
    const replaceNext = () => {
      if (disposed || document.hidden) return;
      const icons = [...container.querySelectorAll("[data-mission-book]")];
      for (let attempt = 0; attempt < icons.length; attempt += 1) {
        const icon = icons[replacementSlot % icons.length];
        replacementSlot = (replacementSlot + 1) % icons.length;
        if (icon.matches(":hover") || icon.classList.contains("has-open-tooltip") || icon.classList.contains("is-leaving")) continue;
        replaceIcon(icon);
        return;
      }
    };

    renderSlots();
    const observer = globalThis.ResizeObserver ? new ResizeObserver(renderSlots) : null;
    observer?.observe(container);
    const missionLayout = container.closest(".discovery-mission");
    if (missionLayout) observer?.observe(missionLayout);
    if (details) observer?.observe(details);
    document.addEventListener("scriptahub:scalechange", renderSlots);
    const interval = setInterval(replaceNext, 6200);
    container._disposeMissionStrip = () => {
      disposed = true;
      clearInterval(interval);
      pending.forEach(clearTimeout);
      observer?.disconnect();
      document.removeEventListener("scriptahub:scalechange", renderSlots);
    };
    setupMissionBookTooltips(container);
  }

  function setLanguagePicker(language) {
    for (const select of document.querySelectorAll("[data-language-select]")) {
      select.innerHTML = collection.supportedLanguages.map(({ code, name }) => `<option value="${code}"${code === language ? " selected" : ""}>${escape(name)}</option>`).join("");
      select.onchange = () => setLanguage(select.value);
    }
  }

  function setLanguage(language) {
    localStorage.setItem("scripta-language", language);
    const url = new URL(location.href);
    url.searchParams.set("lang", language);
    history.replaceState({}, "", url);
    if (isAppPage()) {
      document.documentElement.lang = language;
      localizeGlobalHeader(language);
      setLanguagePicker(language);
      setupSearch(language);
      document.dispatchEvent(new CustomEvent("scriptahub:language", { detail: { language } }));
      return;
    }
    renderHome(language);
  }

  function bookCard(book, language) {
    const edition = book.editions[language];
    const title = book.title[language] || book.title.en;
    const description = book.shortDescription[language] || book.shortDescription.en;
    const bookUrl = assetPath(edition.book);
    const labels = cardActions[language];
    const status = book.publicationLabel?.[language] ? `<p class="publication-status">${escape(book.publicationLabel[language])}</p>` : "";
    return `<article class="book-card" data-book-url="${escape(bookUrl)}" role="link" tabindex="0" aria-label="${escape(`${labels.details}: ${title}`)}"><div class="book-card-top"><a href="${escape(bookUrl)}"><img src="${escape(assetPath(book.thumbnailUrl[language]))}" alt="${escape(title)} cover" loading="lazy"></a><div><p class="category">${escape(book.category)}</p><h3><a href="${escape(bookUrl)}">${escape(title)}</a></h3></div></div>${status}<p class="description">${escape(description)}</p><nav class="book-card-actions"><a class="book-card-details" href="${escape(bookUrl)}">${escape(labels.details)}</a></nav></article>`;
  }

  function renderKeywordSelection(keywordId, language, { updateHistory = false, scroll = false } = {}) {
    const browser = document.querySelector("[data-keyword-browser]");
    if (!browser) return;
    const keyword = keywordId ? collection.keywords[language].find((item) => item.id === keywordId) : null;
    const words = copy[language];
    const results = browser.querySelector("[data-keyword-results]");
    const clear = browser.querySelector("[data-keyword-clear]");

    if (!keyword) {
      browser.hidden = true;
      results.innerHTML = "";
      document.title = `ScriptaHub · ${words.libraryTitle}`;
      return;
    }

    const matches = collection.books.filter((book) => book.keywordIds.includes(keyword.id));
    const heading = displayKeyword(keyword.label);
    replaceText("[data-keyword-kicker]", words.keyword);
    replaceText("[data-keyword-title]", heading);
    replaceText("[data-keyword-count]", words.booksTagged(matches.length));
    clear.textContent = keywordResultLabels[language].clear;
    results.innerHTML = matches.map((book) => bookCard(book, language)).join("");
    browser.hidden = false;
    document.title = `${heading} · ScriptaHub`;

    clear.onclick = () => {
      const url = new URL(location.href);
      url.searchParams.delete("keyword");
      history.pushState({}, "", url);
      renderKeywordSelection(null, language);
    };
    if (updateHistory) {
      const url = new URL(location.href);
      url.searchParams.set("lang", language);
      url.searchParams.set("keyword", keyword.id);
      url.searchParams.delete("q");
      history.pushState({}, "", url);
    }
    if (scroll) requestAnimationFrame(() => requestAnimationFrame(() => browser.scrollIntoView({ behavior: "smooth", block: "start" })));
  }

  function setupCardNavigation() {
    if (document.documentElement.dataset.cardNavigationBound) return;
    document.documentElement.dataset.cardNavigationBound = "true";
    document.addEventListener("click", (event) => {
      const card = event.target.closest(".book-card[data-book-url]");
      if (!card || event.defaultPrevented || event.target.closest("a, button, input, select, textarea, label")) return;
      location.assign(card.dataset.bookUrl);
    });
    document.addEventListener("keydown", (event) => {
      if ((event.key !== "Enter" && event.key !== " ") || !event.target.matches(".book-card[data-book-url]")) return;
      event.preventDefault();
      location.assign(event.target.dataset.bookUrl);
    });
  }

  function setupBookHeroAlignment() {
    const hero = document.querySelector(".book-hero");
    const cover = hero?.querySelector(".cover-link");
    const details = hero?.querySelector(".book-details");
    if (!hero || !cover || !details) return;
    const sync = () => {
      if (globalThis.matchMedia?.("(max-width: 860px)").matches) {
        details.style.removeProperty("height");
        return;
      }
      details.style.height = `${cover.getBoundingClientRect().height.toFixed(1)}px`;
    };
    const observer = globalThis.ResizeObserver ? new ResizeObserver(sync) : null;
    observer?.observe(cover);
    window.addEventListener("resize", sync, { passive: true });
    document.addEventListener("scriptahub:scalechange", sync);
    sync();
  }

  function setupCoverPreview(language) {
    const trigger = document.querySelector("[data-cover-preview]");
    if (!trigger) return;
    const dialog = document.createElement("dialog");
    dialog.className = "cover-preview";
    dialog.setAttribute("aria-label", trigger.getAttribute("aria-label"));
    const close = document.createElement("button");
    close.type = "button";
    close.className = "cover-preview-close";
    close.setAttribute("aria-label", cloudCloseLabel[language]);
    close.textContent = "×";
    const artwork = trigger.querySelector("img").cloneNode();
    dialog.append(close, artwork);
    document.body.append(dialog);
    trigger.setAttribute("aria-haspopup", "dialog");
    trigger.addEventListener("click", () => {
      dialog.showModal();
      document.body.classList.add("cover-preview-open");
      close.focus();
    });
    close.addEventListener("click", () => dialog.close());
    dialog.addEventListener("click", (event) => {
      if (event.target === dialog) dialog.close();
    });
    dialog.addEventListener("close", () => {
      document.body.classList.remove("cover-preview-open");
      trigger.focus({ preventScroll: true });
    });
  }

  function renderCloud(language) {
    const cloud = document.querySelector("[data-keyword-cloud]");
    if (!cloud) return;
    // The landing-page cloud intentionally uses the exact interactive component
    // embedded in every book page.  Keep this small fallback below only for a
    // locally opened page where the component script failed to load.
    const sharedCloud = globalThis.ScriptaKeywordCloud;
    if (sharedCloud?.mount) {
      const visibleTerms = Math.min(320, collection.keywords[language].length);
      const words = collection.keywords[language].slice(0, visibleTerms).map((keyword) => ({
        ...keyword,
        href: keywordSearchHref(keyword, language),
      }));
      sharedCloud.mount(cloud, words, {
        ariaLabel: copy[language].discoverTitle,
        instruction: cloudPreviewInstruction[language],
        modalInstruction: cloudInstruction[language],
        closeLabel: cloudCloseLabel[language],
        showInstruction: false,
        onSelect: (keyword) => renderKeywordSelection(keyword.id, language, { updateHistory: true, scroll: true }),
      });
      return;
    }
    if (cloud._dispose) cloud._dispose();
    const visibleTerms = Math.min(320, collection.keywords[language].length);
    const words = collection.keywords[language].slice(0, visibleTerms).map((keyword) => ({ ...keyword, label: displayKeyword(keyword.label), href: keywordSearchHref(keyword, language) }));
    const maximum = Math.max(...words.map((item) => item.count));
    const priorInstruction = cloud.nextElementSibling;
    if (priorInstruction?.classList.contains("cloud-instruction")) priorInstruction.remove();
    cloud.innerHTML = `<canvas tabindex="0" aria-label="${escape(copy[language].discoverTitle)}"></canvas><nav class="sr-only">${words.map((keyword) => `<a href="${escape(keyword.href)}">${escape(keyword.label)}</a>`).join("")}</nav>`;
    const canvas = cloud.querySelector("canvas");
    const context = canvas.getContext("2d");
    const random = (index, salt) => {
      const value = Math.sin((index + 1) * 127.1 + salt * 311.7) * 43758.5453123;
      return value - Math.floor(value);
    };
    const nodes = words.map((keyword, index) => {
      return { keyword, x: random(index, 1) * 2 - 1, y: random(index, 2) * 2 - 1, z: random(index, 3) * 2 - 1 };
    });
    let rotationX = -.18;
    let rotationY = .45;
    let velocityX = 0;
    let velocityY = .0022;
    let zoom = 1;
    let active = false;
    let dragDistance = 0;
    let lastX = 0;
    let lastY = 0;
    let hits = [];
    let frame = 0;

    const resize = () => {
      const bounds = canvas.getBoundingClientRect();
      const density = Math.min(globalThis.devicePixelRatio || 1, 2);
      canvas.width = Math.max(1, Math.round(bounds.width * density));
      canvas.height = Math.max(1, Math.round(bounds.height * density));
      context.setTransform(density, 0, 0, density, 0, 0);
    };
    const rotate = (node) => {
      const cosY = Math.cos(rotationY), sinY = Math.sin(rotationY);
      const cosX = Math.cos(rotationX), sinX = Math.sin(rotationX);
      const x = node.x * cosY - node.z * sinY;
      const z = node.x * sinY + node.z * cosY;
      return { x, y: node.y * cosX - z * sinX, z: node.y * sinX + z * cosX };
    };
    const draw = () => {
      const bounds = canvas.getBoundingClientRect();
      const spreadX = bounds.width * .47 * zoom;
      const spreadY = bounds.height * .43 * zoom;
      const centreX = bounds.width / 2;
      const centreY = bounds.height / 2;
      context.clearRect(0, 0, bounds.width, bounds.height);
      context.save();
      context.translate(centreX, centreY);
      const projected = nodes.map((node) => ({ ...node, point: rotate(node) })).sort((left, right) => left.point.z - right.point.z);
      hits = [];
      projected.forEach((node) => {
        const depth = .44 + (node.point.z + 1) * .34;
        const x = node.point.x * spreadX;
        const y = node.point.y * spreadY;
        const importance = .75 + (node.keyword.count / maximum) * 1.55;
        const size = (8.2 + importance * 3.4) * depth;
        const hue = 128 + Math.round((node.point.z + 1) * 36) + (node.keyword.count % 4) * 13;
        context.globalAlpha = .31 + depth * .67;
        context.font = `${Math.round(size)}px Inter, ui-sans-serif, system-ui, sans-serif`;
        context.textAlign = "center";
        context.textBaseline = "middle";
        context.fillStyle = `hsl(${hue} 76% ${58 + depth * 21}%)`;
        context.shadowColor = `hsla(${hue} 90% 64% / .66)`;
        context.shadowBlur = 11 * depth;
        context.fillText(node.keyword.label, x, y);
        const measured = context.measureText(node.keyword.label).width;
        hits.push({ x: centreX + x, y: centreY + y, width: measured, height: size * 1.38, keyword: node.keyword, depth });
      });
      context.restore();
    };
    const animate = () => {
      if (!active) {
        rotationX += velocityX;
        rotationY += velocityY;
        velocityX *= .94;
        velocityY = Math.abs(velocityY) < .0022 ? .0022 : velocityY * .94;
      }
      draw();
      frame = requestAnimationFrame(animate);
    };
    const pointerPosition = (event) => ({ x: event.clientX, y: event.clientY });
    canvas.addEventListener("pointerdown", (event) => {
      active = true; dragDistance = 0;
      ({ x: lastX, y: lastY } = pointerPosition(event));
      canvas.setPointerCapture(event.pointerId);
    });
    canvas.addEventListener("pointermove", (event) => {
      if (!active) return;
      const point = pointerPosition(event);
      const dx = point.x - lastX, dy = point.y - lastY;
      dragDistance += Math.abs(dx) + Math.abs(dy);
      rotationY += dx * .008; rotationX += dy * .008;
      velocityY = dx * .0012; velocityX = dy * .0012;
      lastX = point.x; lastY = point.y;
    });
    const release = (event) => {
      active = false;
      if (canvas.hasPointerCapture(event.pointerId)) canvas.releasePointerCapture(event.pointerId);
    };
    canvas.addEventListener("pointerup", release);
    canvas.addEventListener("pointercancel", release);
    canvas.addEventListener("click", (event) => {
      if (dragDistance > 8) return;
      const bounds = canvas.getBoundingClientRect();
      const x = event.clientX - bounds.left, y = event.clientY - bounds.top;
      const hit = hits.filter((item) => Math.abs(x - item.x) <= item.width / 2 && Math.abs(y - item.y) <= item.height / 2).sort((a, b) => b.depth - a.depth)[0];
      if (hit) renderKeywordSelection(hit.keyword.id, language, { updateHistory: true, scroll: true });
    });
    canvas.addEventListener("wheel", (event) => {
      event.preventDefault();
      zoom = Math.max(.7, Math.min(1.55, zoom - Math.sign(event.deltaY) * .08));
    }, { passive: false });
    canvas.addEventListener("keydown", (event) => {
      if (event.key === "ArrowLeft") rotationY -= .14;
      else if (event.key === "ArrowRight") rotationY += .14;
      else if (event.key === "ArrowUp") rotationX -= .14;
      else if (event.key === "ArrowDown") rotationX += .14;
      else if (event.key === "+" || event.key === "=") zoom = Math.min(1.55, zoom + .08);
      else if (event.key === "-") zoom = Math.max(.7, zoom - .08);
      else return;
      event.preventDefault();
    });
    const observer = new ResizeObserver(resize);
    observer.observe(cloud);
    resize(); animate();
    cloud._dispose = () => { cancelAnimationFrame(frame); observer.disconnect(); };
  }

  function searchBooks(query, language) {
    const searchable = (value) => normalise(value || "").replace(/[_-]+/g, " ").replace(/\s+/g, " ").trim();
    const needle = searchable(query);
    if (!needle) return [];
    return collection.books.filter((book) => [...Object.values(book.title), book.sourceId, ...(book.sourceAliases || []), book.subtitle[language], book.shortDescription[language], ...book.keywords[language]].some((value) => searchable(value).includes(needle)));
  }

  function setupSearch(language) {
    const input = document.querySelector("[data-book-search]");
    const suggestions = document.querySelector("[data-search-suggestions]");
    const grid = document.querySelector("[data-book-grid]");
    const results = document.querySelector("[data-search-results]");
    if (!input || !suggestions) return;
    const root = input.dataset.searchRoot ? `${input.dataset.searchRoot.replace(/\/?$/, "/")}` : "";
    const initialQuery = new URL(location.href).searchParams.get("q") || "";
    input.placeholder = copy[language].search;
    const showResults = () => {
      if (!grid || !results) return;
      const matches = searchBooks(input.value, language);
      const active = Boolean(input.value.trim());
      grid.hidden = active;
      results.innerHTML = active ? (matches.length ? `<div class="book-grid">${matches.map((book) => bookCard(book, language)).join("")}</div>` : `<p class="search-empty">${escape(copy[language].searchEmpty)}</p>`) : "";
    };
    const showSuggestions = () => {
      const needle = normalise(input.value.trim());
      if (!needle) { suggestions.innerHTML = ""; suggestions.dataset.open = "false"; return; }
      const words = collection.keywords[language].filter((item) => normalise(item.label).includes(needle)).slice(0, 8);
      suggestions.innerHTML = words.map((item) => `<li><button type="button" data-keyword-id="${escape(item.id)}">${escape(item.label)} <small>(${item.count})</small></button></li>`).join("");
      suggestions.dataset.open = words.length ? "true" : "false";
      suggestions.querySelectorAll("button").forEach((button) => button.addEventListener("click", () => {
        const keyword = collection.keywords[language].find((item) => item.id === button.dataset.keywordId);
        if (!keyword) return;
        if (document.querySelector("[data-keyword-browser]")) renderKeywordSelection(keyword.id, language, { updateHistory: true, scroll: true });
        else location.href = `${root}${keywordSearchHref(keyword, language)}`;
      }));
    };
    const goToSearch = () => {
      const query = input.value.trim();
      if (!query) return;
      const words = [...suggestions.querySelectorAll("button")];
      if (words.length) {
        words[0].click();
        return;
      }
      const params = new URLSearchParams({ lang: language, q: query });
      location.href = `${root}index.html?${params.toString()}`;
    };
    input.oninput = () => { showSuggestions(); showResults(); };
    input.onfocus = () => { if (input.value.trim()) showSuggestions(); };
    input.onkeydown = (event) => {
      if (event.key === "Escape") suggestions.dataset.open = "false";
      if (event.key === "Enter") { event.preventDefault(); goToSearch(); }
    };
    input.onsearch = () => { showSuggestions(); showResults(); };
    if (initialQuery && !input.value) {
      input.value = initialQuery;
      showSuggestions(); showResults();
    }
    if (!input.dataset.searchBound) {
      input.dataset.searchBound = "true";
      document.addEventListener("click", (event) => { if (!event.target.closest(".search-wrap")) suggestions.dataset.open = "false"; });
    }
  }

  function splitIntroduction(value, language) {
    const text = String(value || "").replace(/\s+/g, " ").trim();
    if (!text) return [];
    if (globalThis.Intl?.Segmenter) {
      return [...new Intl.Segmenter(language, { granularity: "sentence" }).segment(text)]
        .map(({ segment }) => segment.trim())
        .filter(Boolean);
    }
    return text.match(/[^.!?。！？]+[.!?。！？]+(?:[”’»"])?|[^.!?。！？]+$/g)?.map((sentence) => sentence.trim()).filter(Boolean) || [text];
  }

  function setupIntroPresentation(language, text) {
    const source = document.querySelector("[data-hero-lead]");
    if (!source) return;
    source._disposeIntroPresentation?.();
    const sentences = splitIntroduction(text, language);
    if (sentences.length < 2) {
      source.textContent = text;
      return;
    }

    const words = introPresentationLabels[language];
    const palette = ["var(--green)", "#6746b9", "#28639f", "#a44f38", "#80438c", "#3d7768", "#8b6718", "#276f78"];
    source.innerHTML = `<section class="intro-presentation is-awaiting-choice" aria-label="${escape(words.label)}">
      <div class="intro-stage">
        <button class="intro-arrow intro-arrow-previous" type="button" data-intro-previous aria-label="${escape(words.previous)}" hidden></button>
        <article class="intro-slide" role="group" aria-roledescription="slide" aria-live="off" data-intro-slide hidden></article>
        <button class="intro-arrow intro-arrow-next" type="button" data-intro-next aria-label="${escape(words.next)}" hidden></button>
        <div class="intro-choice" data-intro-choice>
          <div><span class="eyebrow">${escape(words.label)}</span><h2 data-intro-choice-title>${escape(words.unavailable)}</h2><p data-intro-choice-note>${escape(words.unavailableNote)}</p><div class="intro-choice-actions"><button type="button" data-intro-start-voice hidden>${escape(words.read)}</button><button type="button" data-intro-start>${escape(words.start)}</button><button type="button" data-intro-librarian>${escape(librarianSectionLabels[language].title)}</button></div></div>
        </div>
      </div>
      <div class="intro-controls" data-intro-controls hidden>
        <button type="button" data-intro-previous>${escape(words.previous)}</button><span class="intro-counter" data-intro-counter aria-live="polite"></span><button type="button" data-intro-next>${escape(words.next)}</button>
        <button class="intro-icon-button" type="button" data-intro-toggle aria-label="${escape(words.pause)}" title="${escape(words.pause)}"><span aria-hidden="true">❚❚</span></button>
        <button class="intro-icon-button intro-restart" type="button" data-intro-restart aria-label="${escape(words.restart)}" title="${escape(words.restart)}"><span aria-hidden="true">↺</span></button>
        <button type="button" data-intro-read hidden>${escape(words.read)}</button><button type="button" data-intro-view-all>${escape(words.viewAll)}</button><button type="button" data-intro-librarian>${escape(librarianSectionLabels[language].title)}</button><span class="intro-status" data-intro-status></span>
      </div>
    </section>`;

    const presentation = source.querySelector(".intro-presentation");
    const choice = source.querySelector("[data-intro-choice]");
    const choiceTitle = source.querySelector("[data-intro-choice-title]");
    const choiceNote = source.querySelector("[data-intro-choice-note]");
    const startVoiceButton = source.querySelector("[data-intro-start-voice]");
    const readButton = source.querySelector("[data-intro-read]");
    const slide = source.querySelector("[data-intro-slide]");
    const controls = source.querySelector("[data-intro-controls]");
    const counter = source.querySelector("[data-intro-counter]");
    const status = source.querySelector("[data-intro-status]");
    const toggle = source.querySelector("[data-intro-toggle]");
    const arrows = [...source.querySelectorAll(".intro-arrow")];
    const speech = globalThis.speechSynthesis;
    const speechSupported = Boolean(speech && globalThis.SpeechSynthesisUtterance);
    const reducedMotion = globalThis.matchMedia?.("(prefers-reduced-motion: reduce)").matches;
    let active = 0;
    let started = false;
    let paused = Boolean(reducedMotion);
    let voiceMode = false;
    let currentVoice = null;
    let utterance = null;
    let advanceTimer = 0;
    let countdownTimer = 0;
    let nextChangeAt = 0;
    let disposed = false;
    let resumeAfterDialog = false;

    const localVoices = () => {
      if (!speechSupported) return [];
      return speech.getVoices().filter((voice) => voice.localService && voice.lang.toLowerCase().startsWith(language));
    };
    const chooseVoice = () => {
      const voices = localVoices();
      currentVoice = voices.find((voice) => voice.default) || voices[0] || null;
      return currentVoice;
    };
    const updateVoiceAvailability = () => {
      const available = Boolean(chooseVoice());
      if (disposed) return;
      choice.classList.toggle("has-local-voice", available);
      startVoiceButton.hidden = !available;
      readButton.hidden = !available;
      choiceTitle.textContent = available ? words.ready : words.unavailable;
      choiceNote.textContent = available ? words.readyNote : words.unavailableNote;
      if (!available && voiceMode) {
        voiceMode = false;
        stopSpeech();
        schedule();
      }
    };
    const clearTimers = () => {
      clearTimeout(advanceTimer);
      clearInterval(countdownTimer);
      advanceTimer = 0;
      countdownTimer = 0;
      nextChangeAt = 0;
    };
    const stopSpeech = () => {
      if (utterance && speechSupported) speech.cancel();
      utterance = null;
    };
    const durationFor = (sentence) => Math.max(4400, Math.min(9600, 2300 + sentence.split(/\s+/).length * 155));
    const updateStatus = () => {
      if (paused) { status.textContent = words.paused; return; }
      if (voiceMode) { status.textContent = utterance ? words.reading : words.preparing; return; }
      const seconds = Math.max(0, Math.ceil((nextChangeAt - Date.now()) / 1000));
      status.textContent = words.nextIn(seconds);
    };
    const schedule = () => {
      clearTimers();
      if (!started || paused || voiceMode) { updateStatus(); return; }
      const duration = durationFor(sentences[active]);
      nextChangeAt = Date.now() + duration;
      updateStatus();
      countdownTimer = setInterval(updateStatus, 250);
      advanceTimer = setTimeout(() => show(active + 1), duration);
    };
    const sentenceMarkup = (sentence) => {
      const parts = sentence.split(/(\s+)/);
      const wordCount = parts.filter((part) => /\S/.test(part)).length;
      let wordIndex = 0;
      const copy = parts.map((part) => {
        if (!/\S/.test(part)) return part;
        const delay = Math.round(wordIndex++ * Math.min(125, 3300 / Math.max(1, wordCount - 1)));
        return `<span class="intro-word" style="--intro-word-delay:${delay}ms">${escape(part)}</span>`;
      }).join("");
      const signals = Array.from({ length: 7 }, (_, index) => `<span style="--signal-x:${9 + index * 12}%;--signal-delay:${(-index * .19).toFixed(2)}s">${index % 2 ? "01<>" : "10{}"}</span>`).join("");
      return `<span class="intro-slide-copy">${copy}</span><span class="intro-signal-field" aria-hidden="true">${signals}</span>`;
    };
    const syncToggle = () => {
      const label = paused ? words.resume : words.pause;
      toggle.title = label;
      toggle.setAttribute("aria-label", label);
      toggle.querySelector("span").textContent = paused ? "▶" : "❚❚";
    };
    const speakActive = () => {
      stopSpeech();
      if (!voiceMode || paused || !chooseVoice()) { updateStatus(); return; }
      const spokenIndex = active;
      utterance = new SpeechSynthesisUtterance(sentences[active]);
      utterance.voice = currentVoice;
      utterance.lang = currentVoice.lang;
      utterance.rate = 1;
      utterance.pitch = 1;
      utterance.onend = () => {
        utterance = null;
        if (!disposed && voiceMode && !paused && spokenIndex === active) {
          status.textContent = words.nextIn(1);
          advanceTimer = setTimeout(() => { show(active + 1); speakActive(); }, 650);
        }
      };
      utterance.onerror = () => { utterance = null; if (!disposed) status.textContent = words.unavailable; };
      speech.speak(utterance);
      updateStatus();
    };
    const show = (index, restart = false) => {
      if (!started) return;
      active = (index + sentences.length) % sentences.length;
      slide.style.setProperty("--intro-card-color", palette[active % palette.length]);
      slide.setAttribute("aria-label", `${words.message} ${active + 1} / ${sentences.length}`);
      slide.innerHTML = sentenceMarkup(sentences[active]);
      counter.textContent = `${active + 1} / ${sentences.length}`;
      slide.classList.remove("is-active");
      if (restart) void slide.offsetWidth;
      requestAnimationFrame(() => slide.classList.add("is-active"));
      schedule();
    };
    const setPaused = (value) => {
      paused = value;
      if (paused) stopSpeech();
      syncToggle();
      schedule();
      if (!paused && voiceMode) speakActive();
    };
    const start = (withVoice) => {
      started = true;
      voiceMode = Boolean(withVoice && chooseVoice());
      paused = Boolean(reducedMotion && !voiceMode);
      choice.hidden = true;
      controls.hidden = false;
      slide.hidden = false;
      arrows.forEach((arrow) => { arrow.hidden = false; });
      presentation.classList.remove("is-awaiting-choice");
      syncToggle();
      show(0, true);
      if (voiceMode) speakActive();
    };
    const navigate = (offset) => {
      stopSpeech();
      show(active + offset, true);
      if (voiceMode && !paused) speakActive();
    };

    const dialog = document.createElement("div");
    dialog.className = "intro-dialog";
    dialog.hidden = true;
    dialog.innerHTML = `<button class="intro-dialog-backdrop" type="button" data-intro-dialog-close aria-label="${escape(words.close)}"></button><section class="intro-dialog-panel" role="dialog" aria-modal="true" aria-labelledby="intro-dialog-title" tabindex="-1"><header><h2 id="intro-dialog-title">${escape(words.allTitle)}</h2><button type="button" data-intro-dialog-close aria-label="${escape(words.close)}">×</button></header><div>${sentences.map((sentence) => `<p>${escape(sentence)}</p>`).join("")}</div></section>`;
    document.body.append(dialog);
    const closeDialog = () => {
      dialog.hidden = true;
      source.querySelector("[data-intro-view-all]")?.focus();
      if (resumeAfterDialog) setPaused(false);
      resumeAfterDialog = false;
    };
    const openDialog = () => {
      resumeAfterDialog = !paused;
      if (resumeAfterDialog) setPaused(true);
      dialog.hidden = false;
      dialog.querySelector(".intro-dialog-panel").focus();
    };
    const onEscape = (event) => { if (event.key === "Escape" && !dialog.hidden) closeDialog(); };
    dialog.querySelectorAll("[data-intro-dialog-close]").forEach((button) => button.addEventListener("click", closeDialog));
    document.addEventListener("keydown", onEscape);
    source.querySelector("[data-intro-start]").addEventListener("click", () => start(false));
    startVoiceButton.addEventListener("click", () => start(true));
    source.querySelectorAll("[data-intro-previous]").forEach((button) => button.addEventListener("click", () => navigate(-1)));
    source.querySelectorAll("[data-intro-next]").forEach((button) => button.addEventListener("click", () => navigate(1)));
    toggle.addEventListener("click", () => setPaused(!paused));
    source.querySelector("[data-intro-restart]").addEventListener("click", () => { setPaused(false); navigate(-active); });
    readButton.addEventListener("click", () => {
      voiceMode = true;
      paused = false;
      syncToggle();
      schedule();
      speakActive();
    });
    source.querySelector("[data-intro-view-all]").addEventListener("click", openDialog);
    if (speechSupported) speech.addEventListener?.("voiceschanged", updateVoiceAvailability);
    updateVoiceAvailability();
    source._disposeIntroPresentation = () => {
      disposed = true;
      clearTimers();
      stopSpeech();
      if (speechSupported) speech.removeEventListener?.("voiceschanged", updateVoiceAvailability);
      document.removeEventListener("keydown", onEscape);
      dialog.remove();
      delete source._disposeIntroPresentation;
    };
  }

  function setupLibrarianPopup(language) {
    const triggers = [...document.querySelectorAll("[data-intro-librarian]")];
    if (!triggers.length) return;
    const previous = document.querySelector("[data-librarian-dialog]");
    previous?._dispose?.();
    const section = librarianSectionLabels[language];
    const launch = librarianLaunchLabels[language];
    const closeLabel = introPresentationLabels[language].close;
    const dialog = document.createElement("div");
    dialog.className = "librarian-dialog";
    dialog.dataset.librarianDialog = "";
    dialog.hidden = true;
    dialog.innerHTML = `<button class="librarian-dialog-backdrop" type="button" data-librarian-close aria-label="${escape(closeLabel)}"></button><section class="librarian-dialog-panel" role="dialog" aria-modal="true" aria-labelledby="librarian-dialog-title" tabindex="-1"><header><div><p class="eyebrow">${escape(section.kicker)}</p><h2 id="librarian-dialog-title">${escape(section.title)}</h2></div><button class="librarian-dialog-close" type="button" data-librarian-close aria-label="${escape(closeLabel)}">×</button></header><p class="librarian-dialog-lead">${escape(librarianMissionPrompt[language])}</p><form class="mission-librarian librarian-dialog-form" data-librarian-launch><label class="sr-only" for="librarian-dialog-query" data-librarian-label>${escape(launch.label)}</label><textarea id="librarian-dialog-query" rows="3" data-librarian-query required></textarea><div class="mission-librarian-actions"><button class="librarian-dictate" type="button" data-librarian-dictate aria-pressed="false" aria-label="${escape(launch.dictate)}" title="${escape(launch.dictate)}"></button><button type="submit" data-librarian-button>${escape(launch.button)}</button></div><span class="librarian-speech-status" data-librarian-speech-status aria-live="polite"></span></form></section>`;
    document.body.append(dialog);
    const panel = dialog.querySelector(".librarian-dialog-panel");
    const input = dialog.querySelector("[data-librarian-query]");
    let opener = null;
    const close = () => {
      dialog.hidden = true;
      document.body.classList.remove("librarian-dialog-open");
      opener?.focus();
    };
    const open = (event) => {
      event.preventDefault();
      opener = event.currentTarget;
      dialog.hidden = false;
      document.body.classList.add("librarian-dialog-open");
      requestAnimationFrame(() => {
        panel.focus();
        input.focus();
      });
    };
    const onEscape = (event) => {
      if (event.key === "Escape" && !dialog.hidden) close();
    };
    triggers.forEach((trigger) => trigger.addEventListener("click", open));
    dialog.querySelectorAll("[data-librarian-close]").forEach((button) => button.addEventListener("click", close));
    document.addEventListener("keydown", onEscape);
    dialog._dispose = () => {
      const form = dialog.querySelector("[data-librarian-launch]");
      if (form?._speechRecognition) {
        form._speechRecognition.onend = null;
        form._speechRecognition.abort();
      }
      document.removeEventListener("keydown", onEscape);
      document.body.classList.remove("librarian-dialog-open");
      dialog.remove();
    };
    if (location.hash === "#ask-librarian") requestAnimationFrame(() => triggers[0]?.click());
  }

  function revealHomeWhenReady() {
    const loader = document.querySelector("[data-home-loading]");
    if (!loader || loader.dataset.revealStarted) return;
    loader.dataset.revealStarted = "true";
    const floor = loader.closest(".discovery-mission");
    const waitForImage = (image) => {
      if (image.complete) return typeof image.decode === "function" ? image.decode().catch(() => {}) : Promise.resolve();
      return new Promise((resolve) => {
        image.addEventListener("load", resolve, { once: true });
        image.addEventListener("error", resolve, { once: true });
      });
    };
    const assets = [...floor.querySelectorAll("img")].map(waitForImage);
    if (document.fonts?.ready) assets.push(document.fonts.ready.catch(() => {}));
    if (document.readyState !== "complete") assets.push(new Promise((resolve) => addEventListener("load", resolve, { once: true })));
    const minimumDisplay = new Promise((resolve) => setTimeout(resolve, 450));
    Promise.all([Promise.allSettled(assets), minimumDisplay])
      .then(() => new Promise((resolve) => requestAnimationFrame(() => requestAnimationFrame(resolve))))
      .then(() => {
        floor.setAttribute("aria-busy", "false");
        loader.classList.add("is-complete");
        setTimeout(() => loader.remove(), 420);
      });
  }

  function renderHome(language) {
    const words = copy[language];
    document.documentElement.lang = language;
    localizeGlobalHeader(language);
    replaceText("[data-home-loading-text]", homeLoadingLabels[language]);
    document.title = `ScriptaHub · ${words.libraryTitle}`;
    replaceText("[data-hero-kicker]", words.heroKicker);
    replaceText("[data-hero-title]", words.heroTitle, true);
    setupIntroPresentation(language, heroPresentation[language]);
    setupLibrarianPopup(language);
    setupLibrarianLaunch(language);
    renderCloud(language);
    const missionBooks = document.querySelector("[data-mission-books]");
    const featuredBook = document.querySelector("[data-featured-book]");
    if (missionBooks) setupMissionBookStrip(missionBooks, language, featuredBook);
    replaceText("[data-discover-kicker]", words.discoverKicker); replaceText("[data-discover-title]", discoveryTitles[language]); replaceText("[data-search-label]", words.search);
    replaceText("[data-library-kicker]", librarianSectionLabels[language].kicker); replaceText("[data-library-title]", librarianSectionLabels[language].title);
    replaceText("[data-library-lead]", librarianMissionPrompt[language]);
    setLanguagePicker(language); setupSearch(language);
    renderKeywordSelection(new URL(location.href).searchParams.get("keyword"), language, { scroll: Boolean(new URL(location.href).searchParams.get("keyword")) });
    revealHomeWhenReady();
  }

  function setupBookReading(language) {
    const select = document.querySelector("[data-book-reading-language]");
    const book = collection.books.find((item) => item.id === document.body.dataset.bookId);
    const reading = globalThis.ScriptaReading;
    if (!select || !book || !reading) return;
    select.value = language;
    const update = () => {
      for (const link of document.querySelectorAll("[data-reading-format]")) {
        const format = link.dataset.readingFormat;
        link.href = reading.readingUrl(book, select.value, format, language, siteRootUrl).href;
        const present = reading.available(book, select.value, format);
        link.textContent = present ? link.dataset.readingLabel : `${link.dataset.readingLabel} · ${reading.labels[language].request}`;
      }
    };
    select.addEventListener("change", update);
    update();
  }

  const language = selectedLanguage();
  setupTheme();
  setupSiteScale();
  setupCardNavigation();
  if (isBookPage()) { localizeGlobalHeader(language); setupSearch(language); setupBookHeroAlignment(); setupBookReading(language); setupCoverPreview(language); }
  else if (isAppPage()) { document.documentElement.lang = language; localizeGlobalHeader(language); setLanguagePicker(language); setupSearch(language); }
  else renderHome(language);
  if (!isBookPage() && !isAppPage()) addEventListener("popstate", () => renderKeywordSelection(new URL(location.href).searchParams.get("keyword"), selectedLanguage()));
})();
