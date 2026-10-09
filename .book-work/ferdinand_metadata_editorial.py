#!/usr/bin/env python3
"""Editorial metadata for the two distinct Count Fathom intake records."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BOOK = ROOT / "docs/books/the/adventures/of/ferdinand/count/fathom/part"
WORK = ROOT / ".book-work"

# Each entry: localized title, subtitle, six-sentence discovery description,
# two source-grounded About Book paragraphs. Neither volume reveals the ending.
COPY = {
"i": {
"en": (
"The Adventures of Ferdinand Count Fathom: Part I", "A cunning adventurer crosses military camps and European society",
"Ferdinand Fathom grows up amid war and learns to exploit patronage. His education sharpens a talent for deception. Partnerships and intrigues take him to Vienna. Paris tests his skill at winning favor. Later journeys carry him toward English society. Smollett's satire asks readers to judge appearances against conduct.",
"Tobias Smollett introduces Ferdinand Fathom through his childhood, military surroundings and education. The young adventurer gains a patron, studies the uses of charm and enters schemes with an associate. Vienna brings new opportunities and hazards as he turns social access into advantage. The novel follows his movements through a world where rank, wealth and reputation can be manipulated.",
"The first part continues through Paris, travel and encounters in England. Fathom's successes draw attention, but reversals expose the uncertainty beneath his cultivated persona. Smollett's comic, often biting narration makes the rogue's resourcefulness engaging without presenting deceit as virtue. This volume contains the original narrative through chapter thirty-eight; its accompanying historical material situates the eighteenth-century satire."),
"ro": (
"Aventurile lui Ferdinand, conte de Fathom: Partea I", "Un aventurier viclean traversează tabere militare și societatea europeană",
"Ferdinand Fathom crește în vreme de război și învață să folosească protecția celor puternici. Educația îi ascute talentul pentru înșelăciune. Parteneriatele și intrigile îl duc la Viena. Parisul îi pune la încercare farmecul social. Călătoriile îl apropie apoi de societatea engleză. Satira lui Smollett compară aparențele cu faptele.",
"Tobias Smollett îl prezintă pe Ferdinand Fathom prin copilărie, mediul militar și educație. Tânărul aventurier câștigă un protector, învață folosirea farmecului și începe planuri alături de o asociată. Viena îi oferă ocazii și pericole noi, pe măsură ce transformă accesul social în avantaj. Romanul îl urmărește într-o lume unde rangul, averea și reputația pot fi manipulate.",
"Prima parte continuă prin Paris, călătorii și întâlniri în Anglia. Reușitele lui Fathom atrag atenția, dar răsturnările de situație arată nesiguranța din spatele imaginii sale atent construite. Narațiunea comică, adesea aspră, îi face ingeniozitatea interesantă fără a prezenta înșelăciunea drept virtute. Volumul cuprinde povestea originală până la capitolul treizeci și opt și material despre contextul satirei din secolul al XVIII-lea."),
"fr": (
"Les Aventures de Ferdinand, comte Fathom : première partie", "Un aventurier rusé traverse les camps militaires et la société européenne",
"Ferdinand Fathom grandit dans la guerre et apprend à exploiter la protection des puissants. Son éducation aiguise son goût de la tromperie. Des alliances et des intrigues le conduisent à Vienne. Paris éprouve son art de gagner des faveurs. Ses voyages le mènent ensuite vers la société anglaise. La satire de Smollett confronte apparences et conduite.",
"Tobias Smollett présente Ferdinand Fathom à travers son enfance, son milieu militaire et son éducation. Le jeune aventurier obtient un protecteur, apprend à se servir de son charme et monte des projets avec une complice. Vienne lui offre de nouvelles occasions et de nouveaux dangers. Le roman le suit dans un monde où rang, fortune et réputation peuvent servir à tromper.",
"Cette première partie passe par Paris, les voyages et des rencontres en Angleterre. Les succès de Fathom attirent l'attention, tandis que ses revers révèlent la fragilité de l'image qu'il cultive. Le récit comique, parfois mordant, rend son ingéniosité captivante sans faire de la fraude une vertu. Ce volume contient le récit original jusqu'au chapitre trente-huit et un éclairage sur la satire du XVIIIe siècle."),
"de": (
"Die Abenteuer des Ferdinand Graf Fathom: Teil I", "Ein listiger Abenteurer durchquert Feldlager und europäische Gesellschaft",
"Ferdinand Fathom wächst im Krieg auf und lernt, mächtige Gönner auszunutzen. Seine Erziehung schärft sein Talent zur Täuschung. Bündnisse und Intrigen führen ihn nach Wien. Paris prüft seine Kunst, sich beliebt zu machen. Später gelangt er in die englische Gesellschaft. Smolletts Satire stellt Schein und Verhalten gegenüber.",
"Tobias Smollett führt Ferdinand Fathom über Kindheit, militärisches Umfeld und Erziehung ein. Der junge Abenteurer gewinnt einen Gönner, setzt seinen Charme ein und schmiedet mit einer Komplizin Pläne. Wien bietet neue Chancen und Gefahren, während er gesellschaftliche Zugänge für sich nutzt. Der Roman begleitet ihn durch eine Welt, in der Rang, Vermögen und Ruf manipulierbar sind.",
"Der erste Teil führt über Paris, Reisen und Begegnungen in England. Fathoms Erfolge machen ihn bekannt, doch Rückschläge zeigen die Unsicherheit hinter seiner sorgsam gepflegten Erscheinung. Smolletts komische, oft scharfe Erzählweise macht seinen Einfallsreichtum reizvoll, ohne Betrug zur Tugend zu erklären. Dieser Band enthält die ursprüngliche Handlung bis Kapitel achtunddreißig sowie Material zum historischen Kontext der Satire des achtzehnten Jahrhunderts."),
"es": (
"Las aventuras de Ferdinand, conde Fathom: Parte I", "Un aventurero astuto recorre campamentos militares y la sociedad europea",
"Ferdinand Fathom crece entre guerras y aprende a explotar el patronazgo. Su educación afina su talento para el engaño. Las alianzas y las intrigas lo llevan a Viena. París pone a prueba su habilidad social. Más tarde viaja hacia la sociedad inglesa. La sátira de Smollett contrapone las apariencias y los actos.",
"Tobias Smollett presenta a Ferdinand Fathom mediante su infancia, el entorno militar y su educación. El joven aventurero consigue un protector, aprende a usar su encanto y urde planes con una cómplice. Viena le ofrece nuevas oportunidades y peligros mientras convierte el acceso social en ventaja. La novela lo sigue por un mundo donde el rango, la riqueza y la reputación pueden manipularse.",
"La primera parte continúa por París, los viajes y los encuentros en Inglaterra. Los éxitos de Fathom atraen atención, pero los reveses muestran la inseguridad detrás de su imagen cuidadosamente cultivada. La narración cómica, a menudo mordaz, hace interesante su ingenio sin presentar el engaño como virtud. Este volumen contiene la historia original hasta el capítulo treinta y ocho y material sobre la sátira del siglo XVIII."),
"pt": (
"As aventuras de Ferdinand, conde Fathom: Parte I", "Um aventureiro astuto atravessa acampamentos militares e a sociedade europeia",
"Ferdinand Fathom cresce em tempo de guerra e aprende a explorar o patrocínio. A educação aguça o seu talento para o engano. Parcerias e intrigas levam-no a Viena. Paris põe à prova a sua habilidade social. As viagens aproximam-no depois da sociedade inglesa. A sátira de Smollett contrapõe aparências e conduta.",
"Tobias Smollett apresenta Ferdinand Fathom através da infância, do ambiente militar e da educação. O jovem aventureiro ganha um protetor, aprende a usar o seu encanto e planeia golpes com uma cúmplice. Viena oferece oportunidades e perigos novos enquanto ele transforma o acesso social em vantagem. O romance acompanha-o num mundo onde posição, fortuna e reputação podem ser manipuladas.",
"A primeira parte passa por Paris, viagens e encontros em Inglaterra. Os êxitos de Fathom atraem atenção, mas os reveses mostram a fragilidade da imagem que cultiva. A narração cómica, por vezes mordaz, torna o seu engenho interessante sem apresentar o engano como virtude. Este volume contém a narrativa original até ao capítulo trinta e oito e material sobre a sátira do século XVIII."),
"it": (
"Le avventure di Ferdinand, conte Fathom: Parte I", "Un avventuriero astuto attraversa accampamenti militari e società europea",
"Ferdinand Fathom cresce durante la guerra e impara a sfruttare i protettori. L'educazione affina il suo talento per l'inganno. Alleanze e intrighi lo portano a Vienna. Parigi mette alla prova le sue abilità sociali. I viaggi lo conducono poi nella società inglese. La satira di Smollett confronta apparenze e comportamenti.",
"Tobias Smollett presenta Ferdinand Fathom attraverso infanzia, ambiente militare ed educazione. Il giovane avventuriero ottiene un protettore, impara a usare il fascino e prepara stratagemmi con una complice. Vienna offre nuove occasioni e pericoli mentre egli trasforma l'accesso sociale in vantaggio. Il romanzo lo segue in un mondo dove rango, ricchezza e reputazione si prestano alla manipolazione.",
"La prima parte prosegue attraverso Parigi, i viaggi e gli incontri in Inghilterra. I successi di Fathom attirano attenzione, ma le sconfitte rivelano l'incertezza dietro l'immagine che coltiva. La narrazione comica, spesso pungente, rende interessante la sua ingegnosità senza elevare l'inganno a virtù. Il volume contiene la storia originale fino al capitolo trentotto e materiale sul contesto della satira settecentesca."),
"pl": (
"Przygody Ferdynanda, hrabiego Fathoma: Część I", "Przebiegły awanturnik w obozach wojskowych i europejskich salonach",
"Ferdynand Fathom dorasta podczas wojny i uczy się wykorzystywać wpływowych protektorów. Edukacja rozwija jego talent do oszustwa. Sojusze i intrygi prowadzą go do Wiednia. Paryż sprawdza jego umiejętności towarzyskie. Późniejsze podróże zbliżają go do angielskiego społeczeństwa. Satyra Smolletta zestawia pozory z czynami.",
"Tobias Smollett przedstawia Ferdynanda Fathoma poprzez dzieciństwo, środowisko wojskowe i edukację. Młody awanturnik zyskuje protektora, poznaje siłę uroku i knuje plany ze wspólniczką. Wiedeń przynosi mu nowe okazje i zagrożenia, gdy zamienia kontakty towarzyskie w korzyść. Powieść prowadzi go przez świat, w którym pozycję, majątek i reputację można wykorzystać do oszustwa.",
"Pierwsza część obejmuje Paryż, podróże i spotkania w Anglii. Sukcesy Fathoma przyciągają uwagę, lecz niepowodzenia odsłaniają niepewność ukrytą za starannie budowanym wizerunkiem. Komizm i ostra satyra Smolletta czynią pomysłowość bohatera ciekawą, nie przedstawiając oszustwa jako cnoty. Tom zawiera oryginalną narrację do rozdziału trzydziestego ósmego oraz materiał o osiemnastowiecznym kontekście utworu."),
},
"ii": {
"en": (
"The Adventures of Ferdinand Count Fathom: Part II", "Fathom's reversals test friendship, reputation, and his latest disguises",
"The second volume resumes Fathom's adventures amid debt and confinement. New roles let him rebuild his standing. His schemes reach into medicine and marriage. Renaldo and Monimia face consequences of his deception. Smollett shifts between comic exposure and serious distress. The closing chapters bring the intertwined stories toward a reckoning.",
"Part II opens as Ferdinand Fathom encounters a new social world under the pressure of debt. He adapts his performance to changing circumstances, including a turn toward medical practice. The plot moves among prisons, households and London society, where claims of gentility compete with material need. His friendship with Renaldo becomes a central measure of the harm his schemes can cause.",
"Monimia's situation and Renaldo's trials give this half of the novel a more serious emotional weight. Smollett still uses comic portraits and sharp observations of reputation, profession and class, but the separate narrative lines begin to converge. Readers can follow how deception alters trust without learning the final resolution here. This volume contains chapters thirty-nine through sixty-seven and contextual material on the novel's eighteenth-century setting."),
"ro": (
"Aventurile lui Ferdinand, conte de Fathom: Partea a II-a", "Răsturnările de situație pun la încercare prietenia, reputația și noile măști ale lui Fathom",
"Al doilea volum reia aventurile lui Fathom în condiții de datorie și detenție. Roluri noi îi permit să-și refacă poziția. Planurile lui ajung în medicină și căsătorie. Renaldo și Monimia suportă urmările înșelăciunilor sale. Smollett alternează comicul cu suferința gravă. Capitolele finale apropie firele poveștii de o confruntare.",
"Partea a doua începe când Ferdinand Fathom întâlnește o lume socială nouă sub presiunea datoriilor. Își adaptează aparențele împrejurărilor schimbătoare, inclusiv printr-o incursiune în practica medicală. Acțiunea trece prin închisoare, case particulare și societatea londoneză, unde pretențiile de noblețe întâlnesc nevoia materială. Prietenia cu Renaldo devine o măsură a răului produs de planurile sale.",
"Situația Monimiei și încercările lui Renaldo dau acestei jumătăți a romanului o greutate emoțională mai mare. Smollett păstrează portretele comice și observațiile despre reputație, profesie și clasă socială, dar firele narative încep să se întâlnească. Cititorul poate urmări efectul înșelăciunii asupra încrederii fără a afla aici deznodământul. Volumul cuprinde capitolele treizeci și nouă până la șaizeci și șapte și material despre contextul secolului al XVIII-lea."),
"fr": (
"Les Aventures de Ferdinand, comte Fathom : deuxième partie", "Les revers éprouvent l'amitié, la réputation et les nouveaux rôles de Fathom",
"Le second volume reprend les aventures de Fathom entre dettes et captivité. De nouveaux rôles lui permettent de refaire sa position. Ses intrigues touchent la médecine et le mariage. Renaldo et Monimia subissent les conséquences de ses tromperies. Smollett alterne satire comique et détresse. Les derniers chapitres rapprochent les histoires entrelacées d'un dénouement.",
"La deuxième partie commence lorsque Ferdinand Fathom découvre un nouveau milieu sous la pression des dettes. Il adapte son personnage aux circonstances, notamment en se tournant vers la médecine. L'intrigue passe par la prison, des maisons privées et la société londonienne, où les prétentions de rang rencontrent le besoin matériel. Son amitié avec Renaldo mesure de plus en plus les dégâts causés par ses manœuvres.",
"La situation de Monimia et les épreuves de Renaldo donnent à cette moitié du roman un poids affectif plus grave. Smollett conserve ses portraits comiques et ses observations sur réputation, métier et classe, tandis que les fils du récit convergent. Le lecteur peut suivre les effets de la tromperie sur la confiance sans connaître ici la résolution. Ce volume réunit les chapitres trente-neuf à soixante-sept et des repères sur le XVIIIe siècle."),
"de": (
"Die Abenteuer des Ferdinand Graf Fathom: Teil II", "Rückschläge prüfen Freundschaft, Ruf und Fathoms neue Rollen",
"Der zweite Band setzt Fathoms Abenteuer zwischen Schulden und Gefangenschaft fort. Neue Rollen helfen ihm, wieder Ansehen zu gewinnen. Seine Pläne reichen in Medizin und Ehe. Renaldo und Monimia tragen Folgen seiner Täuschungen. Smollett wechselt zwischen Komik und ernstem Leid. Die letzten Kapitel führen die Handlungsstränge auf eine Entscheidung zu.",
"Teil II beginnt, als Ferdinand Fathom unter dem Druck seiner Schulden eine neue soziale Welt kennenlernt. Er passt seine Rolle veränderten Umständen an und versucht sich auch in der Heilkunde. Die Handlung führt durch Gefängnis, Häuser und Londoner Gesellschaft, wo Standesansprüche auf materielle Not treffen. Seine Freundschaft mit Renaldo zeigt, welchen Schaden seine Pläne anrichten können.",
"Monimias Lage und Renaldos Prüfungen verleihen dieser Romanhälfte größeres emotionales Gewicht. Smollett behält komische Figuren und scharfe Beobachtungen zu Ruf, Beruf und Klasse bei, während die Handlungsfäden zusammenlaufen. Leser können verfolgen, wie Täuschung Vertrauen verändert, ohne hier die Auflösung zu erfahren. Dieser Band umfasst Kapitel neununddreißig bis siebenundsechzig und historisches Material zum achtzehnten Jahrhundert."),
"es": (
"Las aventuras de Ferdinand, conde Fathom: Parte II", "Los reveses ponen a prueba la amistad, la reputación y los nuevos papeles de Fathom",
"El segundo volumen continúa las aventuras de Fathom entre deudas y encierro. Nuevos papeles le permiten recuperar posición. Sus planes alcanzan la medicina y el matrimonio. Renaldo y Monimia sufren las consecuencias de sus engaños. Smollett alterna exposición cómica y dolor. Los capítulos finales acercan los hilos de la historia a una resolución.",
"La segunda parte comienza cuando Ferdinand Fathom conoce otro mundo social bajo la presión de las deudas. Adapta su personaje a circunstancias cambiantes, incluso mediante una incursión en la práctica médica. La trama pasa por la cárcel, los hogares y la sociedad londinense, donde las pretensiones de rango chocan con las necesidades materiales. Su amistad con Renaldo mide el daño que sus planes pueden causar.",
"La situación de Monimia y las pruebas de Renaldo dan a esta mitad de la novela mayor peso emocional. Smollett conserva retratos cómicos y observaciones sobre reputación, profesión y clase, mientras convergen las líneas narrativas. El lector puede seguir cómo el engaño altera la confianza sin descubrir aquí el desenlace. El volumen reúne los capítulos treinta y nueve a sesenta y siete y material sobre el siglo XVIII."),
"pt": (
"As aventuras de Ferdinand, conde Fathom: Parte II", "Os reveses põem à prova a amizade, a reputação e os novos papéis de Fathom",
"O segundo volume retoma as aventuras de Fathom entre dívidas e prisão. Novos papéis permitem-lhe recuperar posição. Os seus planos chegam à medicina e ao casamento. Renaldo e Monimia sofrem consequências dos seus enganos. Smollett alterna comicidade e sofrimento sério. Os últimos capítulos aproximam as histórias entrelaçadas de uma resolução.",
"A segunda parte começa quando Ferdinand Fathom conhece um novo meio social sob a pressão das dívidas. Adapta a personagem às circunstâncias, incluindo uma passagem pela prática médica. A ação percorre prisão, casas particulares e sociedade londrina, onde pretensões de posição esbarram na necessidade material. A amizade com Renaldo mostra o dano que os seus planos podem causar.",
"A situação de Monimia e as provações de Renaldo dão maior peso emocional a esta metade do romance. Smollett mantém retratos cómicos e observações sobre reputação, profissão e classe, enquanto os fios narrativos convergem. O leitor pode seguir os efeitos do engano sobre a confiança sem descobrir aqui o desfecho. Este volume contém os capítulos trinta e nove a sessenta e sete e material sobre o século XVIII."),
"it": (
"Le avventure di Ferdinand, conte Fathom: Parte II", "Le avversità mettono alla prova amicizia, reputazione e nuovi ruoli di Fathom",
"Il secondo volume riprende le avventure di Fathom tra debiti e prigionia. Nuovi ruoli gli permettono di ricostruire la propria posizione. I suoi intrighi coinvolgono medicina e matrimonio. Renaldo e Monimia subiscono le conseguenze degli inganni. Smollett alterna comicità e sofferenza. I capitoli finali avvicinano le storie intrecciate a una resa dei conti.",
"La seconda parte comincia quando Ferdinand Fathom incontra un nuovo ambiente sociale sotto il peso dei debiti. Adatta il suo personaggio alle circostanze, anche dedicandosi alla pratica medica. La trama attraversa prigione, case private e società londinese, dove le pretese di rango incontrano il bisogno materiale. L'amicizia con Renaldo diventa una misura del danno che i suoi piani possono causare.",
"La situazione di Monimia e le prove di Renaldo danno a questa metà del romanzo un peso emotivo più serio. Smollett conserva i ritratti comici e le osservazioni su reputazione, professione e classe, mentre le linee narrative convergono. Il lettore può seguire gli effetti dell'inganno sulla fiducia senza conoscere qui la conclusione. Il volume comprende i capitoli dal trentanove al sessantasette e materiale sul Settecento."),
"pl": (
"Przygody Ferdynanda, hrabiego Fathoma: Część II", "Przeciwności wystawiają na próbę przyjaźń, reputację i nowe role Fathoma",
"Drugi tom kontynuuje przygody Fathoma wśród długów i uwięzienia. Nowe role pozwalają mu odbudować pozycję. Jego intrygi sięgają medycyny i małżeństwa. Renaldo i Monimia ponoszą skutki jego oszustw. Smollett łączy komizm z poważnym cierpieniem. Ostatnie rozdziały zbliżają splecione historie do rozstrzygnięcia.",
"Druga część zaczyna się, gdy Ferdinand Fathom poznaje nowe środowisko pod presją długów. Dostosowuje swoją rolę do zmiennych okoliczności, także próbując sił w praktyce medycznej. Akcja prowadzi przez więzienie, domy i londyńskie towarzystwo, gdzie ambicje stanowe zderzają się z materialną potrzebą. Przyjaźń z Renaldem pokazuje rozmiar szkód powodowanych przez jego intrygi.",
"Położenie Monimii i próby Renalda nadają tej połowie powieści większy ciężar emocjonalny. Smollett zachowuje komiczne portrety oraz ostre uwagi o reputacji, zawodzie i klasie, gdy wątki narracyjne zaczynają się łączyć. Czytelnik może śledzić, jak oszustwo niszczy zaufanie, bez poznawania tutaj zakończenia. Tom obejmuje rozdziały od trzydziestego dziewiątego do sześćdziesiątego siódmego oraz materiały o XVIII wieku."),
},
}

PATHS = {
    "i": (BOOK / "i/bk-3d089c4dadb048d3/manifest.json", WORK / "theadventuresofferdinandcountfathomparti-v1-5cee39d4616a/book/manifest.json"),
    "ii": (BOOK / "ii/bk-3bbca23e054f437d/manifest.json", WORK / "theadventuresofferdinandcountfathompartii-v1-c65915d6f417/book/manifest.json"),
}

for part, paths in PATHS.items():
    for path in paths:
        m = json.loads(path.read_text(encoding="utf-8"))
        for language, (title, subtitle, description, first, second) in COPY[part].items():
            sentences = [sentence for sentence in description.split(". ") if sentence]
            if len(sentences) != 6 or any(len(sentence.split()) > 22 for sentence in sentences):
                raise ValueError(f"{part} {language}: invalid six-sentence description")
            if not 60 <= len((first + " " + second).split()) <= 250:
                raise ValueError(f"{part} {language}: invalid About Book length")
            m["title"][language] = title
            m["subtitle"][language] = subtitle
            m["shortDescription"][language] = description
            m["aboutBook"][language] = [first, second]
        source_hash = m["metadataDraft"]["sourceSha256"]
        m["metadataDraft"] = {
            "sourceSha256": source_hash,
            "reviewRequired": False,
            "reviewedOn": "2026-10-08",
            "basis": f"Delivered Part {part.upper()} PDF contents, original narrative chapter map and representative passages; no ending revealed",
        }
        m["shortDescriptionEditorial"] = {
            "method": "active-LLM authored and translated from delivered chapter map and representative narrative passages",
            "sourceSha256": source_hash,
            "sentencesPerLanguage": 6,
            "status": "reviewed",
        }
        path.write_text(json.dumps(m, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(path)
