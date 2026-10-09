import json
from pathlib import Path

path=Path('tools/keyword-translations.generated.json')
data=json.loads(path.read_text())
langs=('ro','fr','de','es','pt','it','pl')
fix={
 'Rodion Raskolnikov':('Rodion Raskolnikov',)*7,
 'Alyona Ivanovna':('Alyona Ivanovna',)*7,
 'Lizaveta':('Lizaveta',)*7,
 'Sonia Semyonovna Marmeladov':('Sonia Semyonovna Marmeladov',)*7,
 'Razumikhin':('Razumikhin',)*7,
 'Porfiry Petrovich':('Porfiry Petrovich',)*7,
 'St. Petersburg':('Sankt Petersburg','Saint-Pétersbourg','Sankt Petersburg','San Petersburgo','São Petersburgo','San Pietroburgo','Petersburg'),
 'pawnbroker':('cămătăreasă','prêteuse sur gages','Pfandleiherin','prestamista','agiota','usuraia','lichwiarka'),
 'severe poverty':('sărăcie cruntă','grande pauvreté','schwere Armut','pobreza extrema','pobreza extrema','grave povertà','skrajna bieda'),
 'desperate customers':('clienți disperați','clients désespérés','verzweifelte Kunden','clientes desesperados','clientes desesperados','clienti disperati','zdesperowani klienci'),
 'extraordinary men':('oameni extraordinari','hommes extraordinaires','außergewöhnliche Menschen','hombres extraordinarios','homens extraordinários','uomini straordinari','ludzie niezwykli'),
 'moral law':('lege morală','loi morale','Moralgesetz','ley moral','lei moral','legge morale','prawo moralne'),
 'greater good':('bine superior','bien supérieur','höheres Wohl','bien superior','bem maior','bene superiore','wyższe dobro'),
 'murder':('omor','meurtre','Mord','asesinato','assassinato','omicidio','morderstwo'),
 'confession':('mărturisire','aveu','Geständnis','confesión','confissão','confessione','wyznanie winy'),
 'central question':('întrebare centrală','question centrale','zentrale Frage','pregunta central','questão central','questione centrale','pytanie centralne'),
 'changing condition of Raskolnikov’s mind':('schimbările din mintea lui Raskolnikov','évolution de l’esprit de Raskolnikov','Wandel in Raskolnikows Denken','cambios en la mente de Raskólnikov','mudanças na mente de Raskólnikov','mutamenti nella mente di Raskolnikov','zmiany w umyśle Raskolnikowa'),
 'burden of conscience':('povara conștiinței','poids de la conscience','Last des Gewissens','peso de la conciencia','peso da consciência','peso della coscienza','ciężar sumienia'),
 'higher purpose':('scop superior','but supérieur','höherer Zweck','propósito superior','propósito maior','scopo superiore','wyższy cel'),
 'proposed murder':('omor plănuit','meurtre envisagé','geplanter Mord','asesinato planeado','assassinato planejado','omicidio progettato','planowane morderstwo'),
 'dread':('groază','effroi','Grauen','temor','pavor','terrore','groza'),
 'axe':('topor','hache','Axt','hacha','machado','ascia','siekiera'),
 'Alyona’s building':('clădirea Alionei','immeuble d’Alyona','Aljonas Wohnhaus','edificio de Alyona','prédio de Alyona','palazzo di Alyona','kamienica Alony'),
 'innocent sister':('soră nevinovată','sœur innocente','unschuldige Schwester','hermana inocente','irmã inocente','sorella innocente','niewinna siostra'),
 'second murder':('al doilea omor','second meurtre','zweiter Mord','segundo asesinato','segundo assassinato','secondo omicidio','drugie morderstwo'),
 'coins and trinkets':('monede și mărunțișuri','pièces et bibelots','Münzen und Schmuckstücke','monedas y baratijas','moedas e bugigangas','monete e cianfrusaglie','monety i drobiazgi'),
 'stolen items':('lucruri furate','objets volés','gestohlene Gegenstände','objetos robados','objetos roubados','oggetti rubati','skradzione przedmioty'),
 'moral descent':('decădere morală','chute morale','moralischer Abstieg','caída moral','queda moral','discesa morale','upadek moralny'),
 'fear, confusion':('frică și confuzie','peur et confusion','Angst und Verwirrung','miedo y confusión','medo e confusão','paura e confusione','strach i zamęt'),
 'crime':('crimă','crime','Verbrechen','crimen','crime','delitto','zbrodnia'),
 'blood':('sânge','sang','Blut','sangre','sangue','sangue','krew'),
 'fears discovery':('se teme că va fi descoperit','craint d’être découvert','fürchtet die Entdeckung','teme ser descubierto','tem ser descoberto','teme di essere scoperto','boi się odkrycia'),
 'ordinary streets':('străzi obișnuite','rues ordinaires','gewöhnliche Straßen','calles corrientes','ruas comuns','strade ordinarie','zwykłe ulice'),
 'oppressive summer heat':('căldură apăsătoare de vară','chaleur estivale accablante','drückende Sommerhitze','calor sofocante del verano','calor sufocante do verão','caldo estivo opprimente','duszny letni upał'),
 'philosophical certainty':('certitudine filosofică','certitude philosophique','philosophische Gewissheit','certeza filosófica','certeza filosófica','certezza filosofica','pewność filozoficzna'),
 'psychological story':('poveste psihologică','récit psychologique','psychologische Erzählung','relato psicológico','narrativa psicológica','racconto psicologico','opowieść psychologiczna'),
 'suffocation':('sufocare','étouffement','Erstickung','asfixia','sufocamento','soffocamento','duszenie'),
 'accept punishment':('acceptarea pedepsei','accepter la peine','Strafe annehmen','aceptar el castigo','aceitar a punição','accettare la pena','przyjęcie kary'),
 'investigator':('anchetator','enquêteur','Ermittler','investigador','investigador','investigatore','śledczy'),
 'atonement':('ispășire','expiation','Sühne','expiación','expiação','espiazione','pokuta'),
 'redemption':('izbăvire','rédemption','Erlösung','redención','redenção','redenzione','odkupienie'),
 'detached reasoning':('raționament detașat','raisonnement détaché','distanziertes Denken','razonamiento distante','raciocínio distanciado','ragionamento distaccato','zdystansowane rozumowanie'),
 'theory promised freedom':('teoria promitea libertate','la théorie promettait la liberté','die Theorie versprach Freiheit','la teoría prometía libertad','a teoria prometia liberdade','la teoria prometteva libertà','teoria obiecywała wolność'),
 'bound him to guilt':('l-a legat de vinovăție','l’a enchaîné à la culpabilité','band ihn an die Schuld','lo ató a la culpa','prendeu-o à culpa','lo legò alla colpa','przywiązała go do winy'),
 'Sonia’s compassion':('mila Soniei','la compassion de Sonia','Sonias Mitgefühl','la compasión de Sonia','a compaixão de Sonia','la compassione di Sonia','współczucie Soni'),
 'outward events':('întâmplări exterioare','événements extérieurs','äußere Ereignisse','acontecimientos externos','acontecimentos externos','eventi esterni','wydarzenia zewnętrzne'),
 'murder, guilt':('omor și vinovăție','meurtre et culpabilité','Mord und Schuld','asesinato y culpa','assassinato e culpa','omicidio e colpa','morderstwo i wina'),
 'poverty and oppressive heat':('sărăcie și căldură apăsătoare','pauvreté et chaleur oppressante','Armut und drückende Hitze','pobreza y calor agobiante','pobreza e calor opressivo','povertà e caldo opprimente','bieda i duszny upał'),
 'low offer':('ofertă derizorie','offre dérisoire','niedriges Angebot','oferta irrisoria','oferta irrisória','offerta irrisoria','niska oferta'),
 'Sonia’s room':('camera Soniei','la chambre de Sonia','Sonias Zimmer','la habitación de Sonia','o quarto de Sonia','la stanza di Sonia','pokój Soni'),
}
for phrase,labels in fix.items():
 assert len(labels)==7,(phrase,len(labels))
 for lang,label in zip(langs,labels):data['translations'][lang][phrase]=label
path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
print('Corrected',len(fix),'phrases across 7 languages')
