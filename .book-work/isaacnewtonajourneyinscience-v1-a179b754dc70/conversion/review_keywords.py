"""Correct scientific terms mistranslated by the local draft translator."""
import json
from pathlib import Path

p=Path('tools/keyword-translations.generated.json')
c=json.loads(p.read_text())
langs=('fr','de','es','pt','it','ro','pl')
fix={
'early life and education':('jeunesse et formation','Kindheit und Ausbildung','primeros años y educación','infância e educação','infanzia e istruzione','copilărie și educație','dzieciństwo i edukacja'),
'white light':('lumière blanche','weißes Licht','luz blanca','luz branca','luce bianca','lumină albă','białe światło'),
'broader enlightenment confidence':('confiance plus large des Lumières','größeres Vertrauen der Aufklärung','confianza más amplia de la Ilustración','confiança mais ampla do Iluminismo','fiducia più ampia dell’Illuminismo','încrederea mai largă a Iluminismului','szersza wiara oświecenia'),
'laws of motion':('lois du mouvement','Bewegungsgesetze','leyes del movimiento','leis do movimento','leggi del moto','legile mișcării','prawa ruchu'),
'common mathematical account':('explication mathématique commune','gemeinsame mathematische Erklärung','explicación matemática común','explicação matemática comum','spiegazione matematica comune','explicație matematică unitară','wspólny opis matematyczny'),
'gottfried wilhelm leibniz':('Gottfried Wilhelm Leibniz',)*7,
'satellites and spacecraft':('satellites et engins spatiaux','Satelliten und Raumfahrzeuge','satélites y naves espaciales','satélites e naves espaciais','satelliti e veicoli spaziali','sateliți și nave spațiale','satelity i statki kosmiczne'),
'british and continental mathematicians':('mathématiciens britanniques et continentaux','britische und kontinentale Mathematiker','matemáticos británicos y continentales','matemáticos britânicos e continentais','matematici britannici e continentali','matematicieni britanici și continentali','matematycy brytyjscy i kontynentalni'),
'disturbances in uranus':('perturbations de l’orbite d’Uranus','Störungen der Uranusbahn','perturbaciones en la órbita de Urano','perturbações na órbita de Urano','perturbazioni nell’orbita di Urano','perturbațiile orbitei lui Uranus','zakłócenia orbity Urana'),
'discovery of neptune':('découverte de Neptune','Entdeckung des Neptun','descubrimiento de Neptuno','descoberta de Neptuno','scoperta di Nettuno','descoperirea lui Neptun','odkrycie Neptuna'),
'enlightenment confidence':('confiance des Lumières','Vertrauen der Aufklärung','confianza de la Ilustración','confiança do Iluminismo','fiducia dell’Illuminismo','încrederea Iluminismului','wiara oświecenia'),
'inverse-square law':('loi de l’inverse du carré','Abstandsquadratgesetz','ley del inverso del cuadrado','lei do inverso do quadrado','legge dell’inverso del quadrato','legea inversului pătratului distanței','prawo odwrotności kwadratu'),
'method of fluxions':('méthode des fluxions','Methode der Fluxionen','método de fluxiones','método das fluxões','metodo delle flussioni','metoda fluxiunilor','metoda fluksji'),
'earthly and celestial physics':('physique terrestre et céleste','irdische und himmlische Physik','física terrestre y celeste','física terrestre e celeste','fisica terrestre e celeste','fizica terestră și cea cerească','fizyka ziemska i niebieska'),
'royal society':('Royal Society','Royal Society','Royal Society','Royal Society','Royal Society','Societatea Regală','Royal Society'),
'account of motion':('explication du mouvement','Erklärung der Bewegung','explicación del movimiento','explicação do movimento','spiegazione del moto','explicația mișcării','opis ruchu'),
'refracting instruments':('instruments à réfraction','brechende Instrumente','instrumentos refractores','instrumentos refratores','strumenti a rifrazione','instrumente refractoare','przyrządy refrakcyjne'),
'law of universal gravitation':('loi de la gravitation universelle','Gesetz der universellen Gravitation','ley de la gravitación universal','lei da gravitação universal','legge di gravitazione universale','legea gravitației universale','prawo powszechnego ciążenia'),
'account of light':('explication de la lumière','Erklärung des Lichts','explicación de la luz','explicação da luz','spiegazione della luce','explicația luminii','opis światła'),
'corpuscular theory of light':('théorie corpusculaire de la lumière','Korpuskulartheorie des Lichts','teoría corpuscular de la luz','teoria corpuscular da luz','teoria corpuscolare della luce','teoria corpusculară a luminii','korpuskularna teoria światła'),
'intense concentration':('concentration intense','intensive Konzentration','concentración intensa','concentração intensa','concentrazione intensa','concentrare intensă','intensywne skupienie'),
'mathematical account':('explication mathématique','mathematische Erklärung','explicación matemática','explicação matemática','spiegazione matematica','explicație matematică','opis matematyczny'),
'reflecting telescope':('télescope à réflexion','Spiegelteleskop','telescopio reflector','telescópio refletor','telescopio riflettore','telescop reflector','teleskop zwierciadlany'),
'state of rest':('état de repos','Ruhezustand','estado de reposo','estado de repouso','stato di quiete','stare de repaus','stan spoczynku'),
'interacting bodies':('corps en interaction','wechselwirkende Körper','cuerpos en interacción','corpos em interação','corpi interagenti','corpuri aflate în interacțiune','oddziałujące ciała'),
'celestial physics':('physique céleste','Himmelsphysik','física celeste','física celeste','fisica celeste','fizică cerească','fizyka niebieska'),
'gottfried wilhelm':('Gottfried Wilhelm',)*7,
'underlying order':('ordre fondamental','zugrunde liegende Ordnung','orden subyacente','ordem subjacente','ordine sottostante','ordine fundamentală','ukryty porządek'),
}
for phrase,labels in fix.items():
    for lang,label in zip(langs,labels):
        assert phrase in c['translations'][lang],(phrase,lang)
        c['translations'][lang][phrase]=label
p.write_text(json.dumps(c,ensure_ascii=False,indent=2)+'\n')
print('corrected',len(fix),'phrases in seven languages')
