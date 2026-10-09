import json
from pathlib import Path

p=Path('tools/keyword-translations.generated.json');c=json.loads(p.read_text())
fixes={
'Alyosha':{'es':'Aliosha','pt':'Aliócha','ro':'Alyosha'},
'Grushenka':{'es':'Grushenka','pt':'Grushenka','it':'Grushenka','ro':'Grushenka'},
'Karamazov family':{'pl':'rodzina Karamazowów'},
'Fyodor’s murder':{'ro':'uciderea lui Fyodor','pl':'zabójstwo Fiodora'},
'shared guilt':{'pl':'wspólna wina','ro':'vină împărțită'},
'reason':{'de':'Vernunft','ro':'rațiune','pl':'rozum'},
'desire and restraint':{'fr':'désir et retenue','de':'Begehren und Selbstbeherrschung','es':'deseo y contención','pt':'desejo e contenção','it':'desiderio e autocontrollo','ro':'dorință și cumpătare','pl':'pragnienie i powściągliwość'},
'moral limit':{'pl':'granica moralna'},
'religious certainty':{'fr':'certitude religieuse','es':'certeza religiosa'},
'spiritual care':{'fr':'sollicitude spirituelle','de':'spirituelle Fürsorge','ro':'grijă spirituală'},
'inherited wrongdoing':{'fr':'faute héritée','es':'culpa heredada','it':'colpa ereditata','ro':'rău moștenit','pl':'odziedziczona wina'},
'moral damage':{'de':'moralischer Schaden','pl':'szkoda moralna'},
'Grushenka’s affection':{'de':'Grushenkas Zuneigung','pt':'afeto de Grushenka','it':'affetto di Grushenka','ro':'afecțiunea Grushenkăi','pl':'uczucie Gruszeńki'},
'false accusation':{'ro':'acuzație falsă','pl':'fałszywe oskarżenie'},
'philosophical doubt':{'it':'dubbio filosofico','ro':'îndoială filosofică','pl':'wątpliwości filozoficzne'},
'detachment':{'de':'Distanzierung','es':'distanciamiento','pt':'distanciamento','pl':'dystans emocjonalny'},
'family’s collapse':{'de':'Zerfall der Familie','es':'desmoronamiento de la familia','pt':'desagregação da família','it':'disgregazione della famiglia','ro':'destrămarea familiei'},
'Grand Inquisitor':{'de':'Großinquisitor','it':'Grande Inquisitore','ro':'Marele Inchizitor'},
'pain of children':{'fr':'souffrance des enfants','de':'Leid der Kinder','pt':'sofrimento das crianças','it':'sofferenza dei bambini','ro':'suferința copiilor'},
'future harmony':{'pl':'przyszła harmonia'},
'Spanish Inquisition':{'ro':'Inchiziția spaniolă','pl':'Inkwizycja hiszpańska'},
'security and certainty':{'fr':'sécurité et certitude','de':'Sicherheit und Gewissheit','es':'seguridad y certeza','pt':'segurança e certeza'},
'good or evil':{'pl':'dobro lub zło'},
'guilt':{'de':'Schuld','it':'colpa','ro':'vină','pl':'wina'},
'connection':{'fr':'lien humain','es':'vínculo humano','pt':'ligação humana','it':'legame umano','ro':'legătură umană','pl':'więź międzyludzka'},
'survival guide':{'de':'Überlebensleitfaden','pl':'przewodnik przetrwania'},
'patient care':{'fr':'attention patiente','es':'cuidado paciente','it':'cura paziente','pl':'cierpliwa troska'},
'self-protection':{'pl':'samoobrona'},
'repair after harm':{'fr':'réparer le tort causé','de':'Wiedergutmachung nach Schaden','es':'reparar el daño causado','pt':'reparar o dano causado','it':'riparare il danno causato','ro':'repararea răului făcut','pl':'naprawienie wyrządzonej szkody'},
'temptation':{'ro':'ispită'},
'father’s example':{'fr':'exemple du père','de':'Vorbild des Vaters','es':'ejemplo del padre','pt':'exemplo do pai','it':'esempio del padre'},
'novel’s central events':{'fr':'événements centraux du roman','de':'zentrale Ereignisse des Romans','es':'acontecimientos centrales de la novela','pt':'acontecimentos centrais do romance','it':'eventi centrali del romanzo','ro':'evenimentele centrale ale romanului'},
'search for redemption':{'fr':'quête de rédemption','pl':'poszukiwanie odkupienia','ro':'căutarea izbăvirii'},
'competing responses to suffering':{'fr':'réponses différentes à la souffrance','de':'unterschiedliche Antworten auf Leid','es':'distintas respuestas al sufrimiento','pt':'respostas diferentes ao sofrimento','it':'risposte diverse alla sofferenza','ro':'răspunsuri diferite la suferință','pl':'różne reakcje na cierpienie'},
'person who performs an act':{'fr':'auteur matériel de l’acte','de':'unmittelbarer Täter','es':'autor material del acto','pt':'autor material do ato','it':'autore materiale dell’atto','ro':'autorul faptei','pl':'bezpośredni sprawca czynu'},
'wish to question every moral limit':{'fr':'désir de remettre en question toute limite morale','de':'Wunsch, jede moralische Grenze zu hinterfragen','es':'deseo de cuestionar todo límite moral','pt':'desejo de questionar todos os limites morais','it':'desiderio di mettere in discussione ogni limite morale','ro':'dorința de a contesta orice limită morală','pl':'pragnienie kwestionowania każdej granicy moralnej'},
'intellect':{'fr':'intellect','it':'intelletto','pl':'intelekt'},
'earlier choices':{'fr':'choix antérieurs','de':'frühere Entscheidungen','es':'decisiones anteriores','pt':'escolhas anteriores','it':'scelte precedenti','ro':'alegeri anterioare','pl':'wcześniejsze wybory'},
'hope and connection':{'fr':'espoir et liens humains','de':'Hoffnung und Verbundenheit','es':'esperanza y vínculos humanos','pt':'esperança e laços humanos','it':'speranza e legami umani','ro':'speranță și legături umane','pl':'nadzieja i więzi'},
'seek forgiveness':{'fr':'chercher le pardon','de':'Vergebung suchen','es':'buscar el perdón','pt':'procurar perdão','it':'cercare il perdono','ro':'a căuta iertarea','pl':'szukać przebaczenia'},
'three ways through chaos':{'de':'drei Wege durch das Chaos','ro':'trei căi prin haos'},
}
for phrase,labels in fixes.items():
    for lang,label in labels.items():
        assert phrase in c['translations'][lang],(phrase,lang)
        c['translations'][lang][phrase]=label
p.write_text(json.dumps(c,ensure_ascii=False,indent=2)+'\n')
print(sum(map(len,fixes.values())),'labels corrected')
