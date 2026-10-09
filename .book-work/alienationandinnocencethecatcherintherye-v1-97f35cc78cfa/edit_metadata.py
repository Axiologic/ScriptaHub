import json
import re
from pathlib import Path

w=Path(__file__).parent
p=w/'book/manifest.json';d=json.loads(p.read_text())
titles={
'en':'Alienation and Innocence: The Catcher in the Rye',
'fr':'Aliénation et innocence : L’Attrape-cœurs',
'de':'Entfremdung und Unschuld: Der Fänger im Roggen',
'es':'Alienación e inocencia: El guardián entre el centeno',
'pt':'Alienação e inocência: O apanhador no campo de centeio',
'it':'Alienazione e innocenza: Il giovane Holden',
'ro':'Înstrăinare și inocență: De veghe în lanul de secară',
'pl':'Wyobcowanie i niewinność: Buszujący w zbożu',
}
subtitles={
'en':'A study of Holden Caulfield’s loneliness, desire for connection, and fear of growing up',
'fr':'Une étude de la solitude de Holden Caulfield, de son désir de liens et de sa peur de grandir',
'de':'Eine Betrachtung von Holden Caulfields Einsamkeit, Sehnsucht nach Nähe und Angst vor dem Erwachsenwerden',
'es':'Un estudio de la soledad de Holden Caulfield, su deseo de conexión y su miedo a crecer',
'pt':'Um estudo da solidão de Holden Caulfield, do desejo de ligação e do medo de crescer',
'it':'Uno studio della solitudine di Holden Caulfield, del desiderio di legami e della paura di crescere',
'ro':'Un studiu despre singurătatea lui Holden Caulfield, dorința de apropiere și teama de maturizare',
'pl':'Studium samotności Holdena Caulfielda, pragnienia bliskości i lęku przed dorastaniem',
}
sentences={
'en':[
'Holden Caulfield leaves Pencey Prep after another expulsion and feels estranged from its rules.',
'In New York, each attempt at companionship exposes his fear of rejection.',
'His anger at phoniness conceals a longing for honest human contact.',
'The essay examines meetings with Sally Hayes, Sunny, the nuns, and Carl Luce.',
'Phoebe and the museum reveal his wish to keep childhood unchanged.',
'The carousel suggests that care means accepting risk and growth.'
],
'fr':[
'Holden Caulfield quitte Pencey Prep après une nouvelle exclusion et se sent étranger à ses règles.',
'À New York, chaque tentative de rapprochement révèle sa peur du rejet.',
'Sa colère contre l’hypocrisie cache un désir de relations humaines sincères.',
'L’essai examine ses rencontres avec Sally Hayes, Sunny, les religieuses et Carl Luce.',
'Phoebe et le musée révèlent son désir de préserver l’enfance.',
'Le carrousel suggère que prendre soin exige d’accepter le risque et la croissance.'
],
'de':[
'Holden Caulfield verlässt Pencey Prep nach einem weiteren Schulverweis und fühlt sich dessen Regeln entfremdet.',
'In New York offenbart jeder Annäherungsversuch seine Angst vor Zurückweisung.',
'Seine Wut auf Verlogenheit verbirgt eine Sehnsucht nach ehrlicher menschlicher Nähe.',
'Der Essay untersucht Begegnungen mit Sally Hayes, Sunny, den Nonnen und Carl Luce.',
'Phoebe und das Museum zeigen seinen Wunsch, die Kindheit zu bewahren.',
'Das Karussell deutet an, dass Fürsorge Risiko und Wachstum zulassen muss.'
],
'es':[
'Holden Caulfield abandona Pencey Prep tras otra expulsión y se siente ajeno a sus normas.',
'En Nueva York, cada intento de compañía revela su miedo al rechazo.',
'Su ira contra la falsedad oculta un anhelo de contacto humano sincero.',
'El ensayo examina sus encuentros con Sally Hayes, Sunny, las monjas y Carl Luce.',
'Phoebe y el museo revelan su deseo de conservar la infancia.',
'El carrusel sugiere que cuidar implica aceptar riesgos y crecimiento.'
],
'pt':[
'Holden Caulfield deixa Pencey Prep após outra expulsão e sente-se alheio às suas regras.',
'Em Nova Iorque, cada tentativa de companhia revela o seu medo da rejeição.',
'A sua ira perante a falsidade esconde um desejo de contacto humano sincero.',
'O ensaio examina encontros com Sally Hayes, Sunny, as freiras e Carl Luce.',
'Phoebe e o museu revelam o desejo de preservar a infância.',
'O carrossel sugere que cuidar implica aceitar riscos e crescimento.'
],
'it':[
'Holden Caulfield lascia Pencey Prep dopo un’altra espulsione e si sente estraneo alle sue regole.',
'A New York, ogni tentativo di compagnia rivela la sua paura del rifiuto.',
'La rabbia contro la falsità nasconde un desiderio di contatto umano sincero.',
'Il saggio esamina gli incontri con Sally Hayes, Sunny, le suore e Carl Luce.',
'Phoebe e il museo rivelano il suo desiderio di conservare l’infanzia.',
'La giostra suggerisce che prendersi cura richiede di accettare rischio e crescita.'
],
'ro':[
'Holden Caulfield părăsește Pencey Prep după încă o exmatriculare și se simte străin de regulile școlii.',
'La New York, fiecare încercare de apropiere îi dezvăluie teama de respingere.',
'Furia față de falsitate ascunde dorința unei legături omenești sincere.',
'Eseul analizează întâlnirile cu Sally Hayes, Sunny, călugărițele și Carl Luce.',
'Phoebe și muzeul îi arată dorința de a păstra copilăria neschimbată.',
'Caruselul sugerează că grija înseamnă acceptarea riscului și a creșterii.'
],
'pl':[
'Holden Caulfield opuszcza Pencey Prep po kolejnym wydaleniu i czuje się obcy wobec szkolnych zasad.',
'W Nowym Jorku każda próba zbliżenia ujawnia jego lęk przed odrzuceniem.',
'Gniew wobec fałszu skrywa tęsknotę za szczerą ludzką więzią.',
'Esej analizuje spotkania z Sally Hayes, Sunny, zakonnicami i Carlem Luce’em.',
'Phoebe i muzeum ukazują jego pragnienie zachowania dzieciństwa.',
'Karuzela sugeruje, że troska wymaga akceptacji ryzyka i dorastania.'
],
}
about={
'en':'This essay interprets Holden Caulfield’s alienation in Salinger’s novel as a conflict between longing for connection and distrust of the adult world. Beginning with his expulsion from Pencey Prep, it follows his critical judgments of school, family, and social expectations. New York offers repeated encounters with Sally Hayes, Sunny, the nuns, and Carl Luce, but each leaves Holden more aware of his difficulty with vulnerability. Phoebe and the unchanging museum focus his wish to save childhood from loss. The carousel scene offers the essay’s answer: he cannot prevent growth, but he can care for others while accepting their freedom.',
'fr':'Cet essai interprète l’aliénation de Holden Caulfield chez Salinger comme un conflit entre le désir de proximité et la méfiance envers le monde adulte. Après son exclusion de Pencey Prep, il suit ses jugements sur l’école, la famille et les attentes sociales. À New York, les rencontres avec Sally Hayes, Sunny, les religieuses et Carl Luce soulignent sa difficulté à se montrer vulnérable. Phoebe et le musée immuable concentrent son souhait de préserver l’enfance. La scène du carrousel apporte une réponse nuancée : il ne peut empêcher les autres de grandir, mais peut rester présent auprès d’eux.',
'de':'Dieser Essay deutet Holden Caulfields Entfremdung in Salingers Roman als Konflikt zwischen der Sehnsucht nach Nähe und dem Misstrauen gegenüber der Erwachsenenwelt. Nach dem Schulverweis folgt er Holdens Urteilen über Pencey Prep, Familie und gesellschaftliche Erwartungen. In New York zeigen Begegnungen mit Sally Hayes, Sunny, den Nonnen und Carl Luce, wie schwer ihm Verletzlichkeit fällt. Phoebe und das unveränderliche Museum bündeln seinen Wunsch, die Kindheit vor Verlust zu bewahren. Die Karussellszene bietet eine vorsichtige Antwort: Er kann das Erwachsenwerden nicht verhindern, aber anderen in ihrer Freiheit beistehen.',
'es':'Este ensayo interpreta la alienación de Holden Caulfield en la novela de Salinger como un conflicto entre el deseo de cercanía y la desconfianza hacia el mundo adulto. Tras su expulsión de Pencey Prep, sigue sus juicios sobre la escuela, la familia y las expectativas sociales. En Nueva York, los encuentros con Sally Hayes, Sunny, las monjas y Carl Luce muestran su dificultad para mostrarse vulnerable. Phoebe y el museo inmutable concentran su deseo de preservar la infancia. La escena del carrusel propone una respuesta: no puede impedir que otros crezcan, pero sí acompañarlos mientras aceptan su libertad.',
'pt':'Este ensaio interpreta a alienação de Holden Caulfield no romance de Salinger como um conflito entre o desejo de proximidade e a desconfiança do mundo adulto. Após a expulsão de Pencey Prep, acompanha os seus juízos sobre a escola, a família e as expectativas sociais. Em Nova Iorque, os encontros com Sally Hayes, Sunny, as freiras e Carl Luce mostram a dificuldade de se tornar vulnerável. Phoebe e o museu imutável concentram o seu desejo de preservar a infância. O carrossel propõe uma resposta: não pode impedir o crescimento dos outros, mas pode acompanhá-los e respeitar a sua liberdade.',
'it':'Questo saggio interpreta l’alienazione di Holden Caulfield nel romanzo di Salinger come un conflitto tra desiderio di vicinanza e sfiducia nel mondo adulto. Dopo l’espulsione da Pencey Prep, segue i suoi giudizi sulla scuola, la famiglia e le aspettative sociali. A New York, gli incontri con Sally Hayes, Sunny, le suore e Carl Luce mostrano la sua difficoltà a esporsi. Phoebe e il museo immutabile concentrano il desiderio di proteggere l’infanzia. La scena della giostra offre una risposta: non può impedire agli altri di crescere, ma può restare vicino a loro rispettandone la libertà.',
'ro':'Eseul interpretează înstrăinarea lui Holden Caulfield din romanul lui Salinger drept un conflict între dorința de apropiere și neîncrederea în lumea adulților. După exmatricularea de la Pencey Prep, urmărește judecățile lui despre școală, familie și așteptările sociale. La New York, întâlnirile cu Sally Hayes, Sunny, călugărițele și Carl Luce îi arată dificultatea de a fi vulnerabil. Phoebe și muzeul neschimbător concentrează dorința de a feri copilăria de pierdere. Scena caruselului oferă un răspuns: nu poate împiedica maturizarea celorlalți, dar le poate fi alături respectându-le libertatea.',
'pl':'Esej odczytuje wyobcowanie Holdena Caulfielda w powieści Salingera jako konflikt między pragnieniem bliskości a nieufnością wobec świata dorosłych. Po wydaleniu z Pencey Prep śledzi jego oceny szkoły, rodziny i społecznych oczekiwań. W Nowym Jorku spotkania z Sally Hayes, Sunny, zakonnicami i Carlem Luce’em pokazują, jak trudno mu odsłonić własną wrażliwość. Phoebe i niezmienne muzeum skupiają jego pragnienie ocalenia dzieciństwa. Scena karuzeli przynosi odpowiedź: nie zdoła powstrzymać dorastania innych, lecz może im towarzyszyć, szanując ich wolność.',
}
d['title']=titles;d['subtitle']=subtitles;d['shortDescription']={k:' '.join(v) for k,v in sentences.items()}
d['aboutBook']={k:[' '.join(parts[:3]),' '.join(parts[3:])] for k,text in about.items() for parts in [re.split(r'(?<=[.!?])\s+',text)]}
d['shortDescriptionEditorial']={'method':'active-LLM-authored','sourceSha256':json.loads((w/'release.json').read_text())['sha256'],'sentencesPerLanguage':6,'status':'reviewed-intake'}
d.pop('metadataDraft',None)
p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
r=w/'release.json';e=json.loads(r.read_text());e['changes']={'en':'A clean source-text edition with English and Romanian complete and ten-minute readers, revised cover and discovery metadata.','ro':'Ediție curată a textului sursă, cu lecturi integrale și de zece minute în engleză și română, copertă și metadate revizuite.'};r.write_text(json.dumps(e,ensure_ascii=False,indent=2)+'\n')
