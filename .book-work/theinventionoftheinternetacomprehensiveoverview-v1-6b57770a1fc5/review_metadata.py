from pathlib import Path
import json

root = Path('.book-work/theinventionoftheinternetacomprehensiveoverview-v1-6b57770a1fc5')
path = root / 'book/manifest.json'
manifest = json.loads(path.read_text())
data = {
'en': (
 'The Invention of the Internet: A Comprehensive Overview',
 'From ARPANET and packet switching to a network of networks',
 ['A thought experiment imagines daily life without online connections.', 'Cold War research provides the setting for early computer networking.', 'Licklider, Baran, Davies, Kleinrock, Cerf, and Kahn contribute different ideas.', 'ARPANET turns packet switching into a working research network.', 'TCP/IP and NSFNet connect more networks and expand access.', 'The final chapters examine changing uses, privacy, unequal access, and governance.'],
 ['This history begins by imagining a present without the internet, then moves to the people and institutions that helped build it. It follows Licklider’s network vision, Baran’s and Davies’s packet switching, Kleinrock’s research, and Cerf and Kahn’s TCP/IP. ARPANET becomes a working network, while NSFNet and regional connections broaden its reach.', 'The book distinguishes early military and academic aims from later uses in communication, research, commerce, education, entertainment, and public services. Its closing chapters consider privacy, unequal access, net neutrality, misinformation, and governance. The opening scenario is explicitly imaginary; the historical chapters trace a collaborative technological process.']),
'fr': (
 'L’invention d’Internet : une vue d’ensemble', 'D’ARPANET et des paquets à un réseau de réseaux',
 ['Une expérience de pensée imagine le quotidien sans connexion en ligne.', 'La guerre froide situe les débuts des réseaux informatiques.', 'Licklider, Baran, Davies, Kleinrock, Cerf et Kahn apportent des idées différentes.', 'ARPANET transforme la commutation de paquets en réseau de recherche opérationnel.', 'TCP/IP et NSFNet relient davantage de réseaux et élargissent l’accès.', 'Les derniers chapitres abordent les usages, la vie privée, les inégalités et la gouvernance.'],
 ['Cette histoire commence par imaginer un présent sans Internet, puis présente les personnes et institutions qui ont contribué à sa création. Elle suit la vision de Licklider, la commutation de paquets de Baran et Davies, les travaux de Kleinrock et le protocole TCP/IP de Cerf et Kahn. ARPANET devient un réseau fonctionnel, tandis que NSFNet et les réseaux régionaux étendent sa portée.', 'Le livre distingue les objectifs militaires et universitaires initiaux des usages ultérieurs dans la communication, la recherche, le commerce, l’éducation et les services publics. Les derniers chapitres examinent la vie privée, les disparités d’accès, la neutralité du réseau, la désinformation et la gouvernance. Son scénario initial est explicitement imaginaire.']),
'de': (
 'Die Erfindung des Internets: Ein umfassender Überblick', 'Von ARPANET und Paketvermittlung zum Netz der Netze',
 ['Ein Gedankenexperiment zeigt einen Alltag ohne Onlineverbindungen.', 'Der Kalte Krieg bildet den Hintergrund der frühen Computernetze.', 'Licklider, Baran, Davies, Kleinrock, Cerf und Kahn liefern unterschiedliche Ideen.', 'ARPANET macht aus Paketvermittlung ein funktionierendes Forschungsnetz.', 'TCP/IP und NSFNet verbinden weitere Netze und erweitern den Zugang.', 'Die letzten Kapitel behandeln Nutzung, Datenschutz, Zugangsunterschiede und Verwaltung.'],
 ['Diese Geschichte beginnt mit der Vorstellung einer Gegenwart ohne Internet und führt anschließend die Menschen und Institutionen seiner Entstehung vor. Sie behandelt Lickliders Netzwerkvision, die Paketvermittlung von Baran und Davies, Kleinrocks Forschung sowie TCP/IP von Cerf und Kahn. ARPANET wird zum funktionierenden Netz; NSFNet und regionale Verbindungen vergrößern seine Reichweite.', 'Das Buch unterscheidet frühe militärische und akademische Ziele von späteren Anwendungen in Kommunikation, Forschung, Handel, Bildung und öffentlichen Diensten. Die letzten Kapitel betrachten Datenschutz, ungleichen Zugang, Netzneutralität, Desinformation und Verwaltung. Das Eingangsszenario wird ausdrücklich als Gedankenexperiment dargestellt.']),
'es': (
 'La invención de Internet: una visión completa', 'De ARPANET y los paquetes a una red de redes',
 ['Un experimento mental imagina la vida cotidiana sin conexiones en línea.', 'La Guerra Fría enmarca las primeras redes informáticas.', 'Licklider, Baran, Davies, Kleinrock, Cerf y Kahn aportan ideas distintas.', 'ARPANET convierte la conmutación de paquetes en una red de investigación funcional.', 'TCP/IP y NSFNet conectan más redes y amplían el acceso.', 'Los capítulos finales examinan usos, privacidad, desigualdad de acceso y gobernanza.'],
 ['Esta historia comienza imaginando un presente sin Internet y después sigue a las personas e instituciones que ayudaron a construirlo. Presenta la visión de Licklider, la conmutación de paquetes de Baran y Davies, la investigación de Kleinrock y TCP/IP de Cerf y Kahn. ARPANET se convierte en una red operativa, mientras NSFNet y las conexiones regionales amplían su alcance.', 'El libro distingue los objetivos militares y académicos iniciales de los usos posteriores en comunicación, investigación, comercio, educación y servicios públicos. Sus últimos capítulos tratan la privacidad, el acceso desigual, la neutralidad de la red, la desinformación y la gobernanza. El escenario inicial se identifica claramente como imaginario.']),
'pt': (
 'A invenção da Internet: uma visão abrangente', 'Da ARPANET e dos pacotes a uma rede de redes',
 ['Uma experiência imaginária mostra o quotidiano sem ligações online.', 'A Guerra Fria contextualiza as primeiras redes de computadores.', 'Licklider, Baran, Davies, Kleinrock, Cerf e Kahn oferecem ideias distintas.', 'A ARPANET transforma a comutação de pacotes numa rede de investigação funcional.', 'TCP/IP e NSFNet ligam mais redes e alargam o acesso.', 'Os capítulos finais abordam usos, privacidade, desigualdade de acesso e governação.'],
 ['Esta história começa por imaginar um presente sem Internet e depois acompanha as pessoas e instituições que ajudaram a construí-la. Expõe a visão de Licklider, a comutação de pacotes de Baran e Davies, o trabalho de Kleinrock e o TCP/IP de Cerf e Kahn. A ARPANET torna-se uma rede funcional, enquanto a NSFNet e as redes regionais ampliam o seu alcance.', 'O livro distingue os objetivos militares e académicos iniciais dos usos posteriores em comunicação, investigação, comércio, educação e serviços públicos. Os capítulos finais consideram privacidade, desigualdade de acesso, neutralidade da rede, desinformação e governação. O cenário inicial é apresentado explicitamente como imaginário.']),
'it': (
 'L’invenzione di Internet: una panoramica completa', 'Da ARPANET e dai pacchetti a una rete di reti',
 ['Un esperimento immaginario descrive la vita quotidiana senza connessioni online.', 'La Guerra fredda fa da sfondo alle prime reti informatiche.', 'Licklider, Baran, Davies, Kleinrock, Cerf e Kahn apportano idee diverse.', 'ARPANET trasforma la commutazione di pacchetto in una rete di ricerca funzionante.', 'TCP/IP e NSFNet collegano altre reti e ampliano l’accesso.', 'I capitoli finali esaminano usi, riservatezza, disparità di accesso e governo della rete.'],
 ['Questa storia comincia immaginando un presente senza Internet e segue poi le persone e le istituzioni che contribuirono a costruirlo. Presenta la visione di Licklider, la commutazione di pacchetto di Baran e Davies, gli studi di Kleinrock e il TCP/IP di Cerf e Kahn. ARPANET diventa una rete operativa, mentre NSFNet e le connessioni regionali ne ampliano la portata.', 'Il libro distingue gli obiettivi militari e accademici iniziali dagli impieghi successivi nella comunicazione, ricerca, commercio, istruzione e nei servizi pubblici. I capitoli finali affrontano riservatezza, accesso diseguale, neutralità della rete, disinformazione e governo. Lo scenario iniziale è dichiarato esplicitamente immaginario.']),
'ro': (
 'Inventarea internetului: o prezentare cuprinzătoare', 'De la ARPANET și comutarea pachetelor la o rețea de rețele',
 ['Un experiment imaginar înfățișează viața de zi cu zi fără conexiuni online.', 'Războiul Rece oferă contextul primelor rețele informatice.', 'Licklider, Baran, Davies, Kleinrock, Cerf și Kahn aduc idei distincte.', 'ARPANET transformă comutarea pachetelor într-o rețea de cercetare funcțională.', 'TCP/IP și NSFNet conectează mai multe rețele și extind accesul.', 'Capitolele finale examinează utilizările, viața privată, accesul inegal și guvernanța.'],
 ['Această istorie începe cu imaginarea unui prezent fără internet, apoi urmărește oamenii și instituțiile care au contribuit la construirea lui. Prezintă viziunea lui Licklider despre rețele, comutarea pachetelor propusă de Baran și Davies, cercetările lui Kleinrock și TCP/IP dezvoltat de Cerf și Kahn. ARPANET devine o rețea funcțională, iar NSFNet și legăturile regionale îi extind raza.', 'Cartea distinge obiectivele militare și academice inițiale de folosirile ulterioare în comunicare, cercetare, comerț, educație și servicii publice. Capitolele finale discută viața privată, accesul inegal, neutralitatea rețelei, dezinformarea și guvernanța. Scenariul de la început este prezentat explicit ca experiment imaginar.']),
'pl': (
 'Wynalezienie Internetu: kompleksowy przegląd', 'Od ARPANET i pakietów do sieci sieci',
 ['Eksperyment myślowy przedstawia codzienność bez połączeń internetowych.', 'Zimna wojna stanowi tło pierwszych sieci komputerowych.', 'Licklider, Baran, Davies, Kleinrock, Cerf i Kahn wnoszą odmienne pomysły.', 'ARPANET zamienia komutację pakietów w działającą sieć badawczą.', 'TCP/IP i NSFNet łączą kolejne sieci oraz poszerzają dostęp.', 'Ostatnie rozdziały omawiają zastosowania, prywatność, nierówny dostęp i zarządzanie.'],
 ['Ta historia zaczyna się od wyobrażenia teraźniejszości bez Internetu, a następnie przedstawia ludzi i instytucje, którzy pomogli go zbudować. Opisuje wizję Licklidera, komutację pakietów Barana i Daviesa, badania Kleinrocka oraz TCP/IP Cerfa i Kahna. ARPANET staje się działającą siecią, a NSFNet i połączenia regionalne zwiększają jej zasięg.', 'Książka odróżnia początkowe cele wojskowe i akademickie od późniejszych zastosowań w komunikacji, badaniach, handlu, edukacji i usługach publicznych. Końcowe rozdziały omawiają prywatność, nierówny dostęp, neutralność sieci, dezinformację oraz zarządzanie. Scenariusz otwierający książkę jest wyraźnie oznaczony jako wyobrażony.']),
}
for language, (title, subtitle, short, about) in data.items():
    assert len(short) == 6 and all(len(s.split()) <= 22 for s in short), language
    assert 60 <= sum(len(p.split()) for p in about) <= 250, language
    manifest['title'][language] = title
    manifest['subtitle'][language] = subtitle
    manifest['shortDescription'][language] = ' '.join(short)
    manifest['aboutBook'][language] = about
manifest['shortDescriptionEditorial'] = {'source':'editorial','status':'reviewed','basis':'Seven source chapters, conclusion, and the English ten-minute reader; six source-grounded sentences per interface language.'}
path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')
release_path = root / 'release.json'
release = json.loads(release_path.read_text())
release['contributors'] = [{'authorId':'althea-zappa','role':'author','statementId':'internet-source-author'}] + release['contributors']
release['changes'] = {
 'en':'First ScriptaHub edition with clean complete and ten-minute English and Romanian readers, an English PDF, revised cover, and reviewed discovery metadata.',
 'ro':'Prima ediție ScriptaHub cu cititoare integrale și de zece minute în engleză și română, PDF englezesc curat, copertă revizuită și metadate de descoperire verificate.'}
release_path.write_text(json.dumps(release, ensure_ascii=False, indent=2) + '\n')
contributor_path = Path('docs/contributors.json')
contributors = json.loads(contributor_path.read_text())
contributors['statements']['internet-source-author'] = {'description': {
 'en':'AI Agent Althea Zappa is credited as author on the original title page.',
 'fr':'L’agent IA Althea Zappa est crédité comme auteur sur la page de titre originale.',
 'de':'KI-Agent Althea Zappa wird auf der ursprünglichen Titelseite als Autor genannt.',
 'es':'El agente de IA Althea Zappa figura como autor en la portada original.',
 'pt':'O agente de IA Althea Zappa consta como autor na página de título original.',
 'it':'L’agente IA Althea Zappa è indicato come autore nel frontespizio originale.',
 'ro':'Agentul IA Althea Zappa este menționat ca autor pe pagina de titlu originală.',
 'pl':'Agent AI Althea Zappa jest wymieniony jako autor na oryginalnej stronie tytułowej.'}}
contributor_path.write_text(json.dumps(contributors, ensure_ascii=False, indent=2) + '\n')
print('Reviewed metadata, contributor credit, and release notes in eight languages')
