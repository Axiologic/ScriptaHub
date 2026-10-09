#!/usr/bin/env python3
"""Editorial eight-language metadata for this interpretive companion to Dickens."""
import json
from pathlib import Path

p = Path(__file__).resolve().parents[1] / "book/manifest.json"
m = json.loads(p.read_text(encoding="utf-8"))
copy = {
"en": (
"Shadows and Lights: A Tale of Two Cities", "Rebirth, revolution, and sacrifice in a reading of Dickens",
"This interpretive companion follows Dickens's story across London and Paris. Manette's release introduces the theme of renewal. Lucie and Darnay connect family hope with political danger. The Revolution tests loyalty and justice. Sydney Carton's choices bring sacrifice into focus. Four chapters trace these contrasts without reproducing the novel.",
"The first chapter contrasts London and Paris as the French Revolution approaches, then follows the return of Dr. Manette from the Bastille. The second considers the effects of his imprisonment and the relationship between Lucie Manette and Charles Darnay. The book reads family bonds alongside the public forces that threaten them, making rebirth and historical change its recurring concerns.",
"Later chapters move through the Revolution's violence, Madame Defarge's demand for revenge, Darnay's danger and Sydney Carton's choice. The interpretation asks how compassion and loyalty survive political upheaval. It discusses the ending of Dickens's novel, so readers wishing to avoid spoilers should read the novel first. A short conclusion returns to justice, progress and sacrifice, followed by a bibliography."),
"ro": (
"Umbre și lumini: O poveste despre două orașe", "Renaștere, revoluție și sacrificiu într-o lectură a lui Dickens",
"Acest ghid interpretează povestea lui Dickens între Londra și Paris. Eliberarea doctorului Manette introduce tema renașterii. Lucie și Darnay leagă speranța familiei de primejdia politică. Revoluția pune la încercare loialitatea și dreptatea. Alegerile lui Sydney Carton aduc sacrificiul în prim-plan. Patru capitole urmăresc contrastele fără a reproduce romanul.",
"Primul capitol contrastează Londra și Parisul înaintea Revoluției Franceze, apoi urmărește întoarcerea doctorului Manette din Bastilia. Al doilea analizează urmările detenției sale și relația dintre Lucie Manette și Charles Darnay. Cartea citește legăturile familiei alături de forțele publice care le amenință, revenind la teme precum renașterea și schimbarea istorică.",
"Capitolele următoare trec prin violența Revoluției, dorința de răzbunare a lui Madame Defarge, primejdia lui Darnay și alegerea lui Sydney Carton. Interpretarea întreabă cum pot rezista compasiunea și loialitatea tulburărilor politice. Ea discută finalul romanului lui Dickens, astfel încât cititorii care evită dezvăluirile ar trebui să citească mai întâi romanul. O scurtă concluzie revine la dreptate, progres și sacrificiu, urmată de bibliografie."),
"fr": (
"Ombres et lumières : Un conte de deux villes", "Renaissance, révolution et sacrifice dans une lecture de Dickens",
"Ce guide interprète l'histoire de Dickens entre Londres et Paris. La libération du docteur Manette introduit la renaissance. Lucie et Darnay relient l'espoir familial au danger politique. La Révolution éprouve loyauté et justice. Les choix de Sydney Carton placent le sacrifice au centre. Quatre chapitres suivent ces contrastes sans reproduire le roman.",
"Le premier chapitre oppose Londres et Paris à l'approche de la Révolution française, puis suit le retour du docteur Manette après la Bastille. Le deuxième examine les effets de sa captivité et la relation entre Lucie Manette et Charles Darnay. Le livre lit les liens familiaux avec les forces publiques qui les menacent, revenant sans cesse à la renaissance et au changement historique.",
"Les chapitres suivants abordent la violence révolutionnaire, la vengeance de Madame Defarge, le danger qui menace Darnay et le choix de Sydney Carton. L'interprétation demande comment compassion et loyauté résistent aux bouleversements politiques. Elle évoque la fin du roman de Dickens; les lecteurs qui préfèrent éviter cette révélation peuvent lire le roman d'abord. Une brève conclusion revient sur justice, progrès et sacrifice avant la bibliographie."),
"de": (
"Schatten und Lichter: Eine Geschichte aus zwei Städten", "Wiedergeburt, Revolution und Opfer in einer Dickens-Lektüre",
"Dieser Begleittext deutet Dickens' Geschichte zwischen London und Paris. Manettes Freilassung führt das Thema Neubeginn ein. Lucie und Darnay verbinden familiäre Hoffnung mit politischer Gefahr. Die Revolution prüft Loyalität und Gerechtigkeit. Sydney Cartons Entscheidungen rücken das Opfer in den Mittelpunkt. Vier Kapitel verfolgen diese Gegensätze, ohne den Roman abzudrucken.",
"Das erste Kapitel stellt London und Paris vor der Französischen Revolution gegenüber und verfolgt Dr. Manettes Rückkehr aus der Bastille. Das zweite betrachtet die Folgen seiner Haft und die Beziehung zwischen Lucie Manette und Charles Darnay. Das Buch liest familiäre Bindungen neben den öffentlichen Kräften, die sie bedrohen, und kehrt zu Neubeginn und historischem Wandel zurück.",
"Weitere Kapitel behandeln revolutionäre Gewalt, Madame Defarges Rachedurst, Darnays Gefahr und Sydney Cartons Entscheidung. Die Deutung fragt, wie Mitgefühl und Loyalität politischen Erschütterungen standhalten. Sie bespricht das Ende von Dickens' Roman; wer dieses zunächst selbst entdecken möchte, sollte den Roman zuerst lesen. Ein kurzer Schluss führt zu Gerechtigkeit, Fortschritt und Opfer zurück, gefolgt von einer Bibliografie."),
"es": (
"Sombras y luces: Historia de dos ciudades", "Renacimiento, revolución y sacrificio en una lectura de Dickens",
"Esta guía interpreta la historia de Dickens entre Londres y París. La liberación del doctor Manette introduce el renacimiento. Lucie y Darnay unen la esperanza familiar con el peligro político. La Revolución pone a prueba lealtad y justicia. Las decisiones de Sydney Carton destacan el sacrificio. Cuatro capítulos siguen esos contrastes sin reproducir la novela.",
"El primer capítulo contrasta Londres y París antes de la Revolución francesa y sigue el regreso del doctor Manette desde la Bastilla. El segundo examina los efectos de su encierro y la relación entre Lucie Manette y Charles Darnay. El libro observa los vínculos familiares junto a las fuerzas públicas que los amenazan, y vuelve a los temas del renacimiento y el cambio histórico.",
"Los capítulos siguientes abordan la violencia revolucionaria, el deseo de venganza de Madame Defarge, el peligro de Darnay y la decisión de Sydney Carton. La interpretación pregunta cómo sobreviven compasión y lealtad a la agitación política. Explica el final de la novela de Dickens; quien desee evitar revelaciones puede leer primero la novela. Una breve conclusión vuelve a justicia, progreso y sacrificio antes de la bibliografía."),
"pt": (
"Sombras e luzes: Um conto de duas cidades", "Renascimento, revolução e sacrifício numa leitura de Dickens",
"Este guia interpreta a história de Dickens entre Londres e Paris. A libertação do doutor Manette introduz o renascimento. Lucie e Darnay ligam esperança familiar a perigo político. A Revolução testa lealdade e justiça. As escolhas de Sydney Carton destacam o sacrifício. Quatro capítulos acompanham estes contrastes sem reproduzir o romance.",
"O primeiro capítulo contrasta Londres e Paris antes da Revolução Francesa e acompanha o regresso do doutor Manette da Bastilha. O segundo examina os efeitos da sua prisão e a relação entre Lucie Manette e Charles Darnay. O livro lê os laços familiares ao lado das forças públicas que os ameaçam, regressando aos temas do renascimento e da mudança histórica.",
"Os capítulos seguintes abordam a violência revolucionária, o desejo de vingança de Madame Defarge, o perigo de Darnay e a escolha de Sydney Carton. A interpretação pergunta como compaixão e lealdade resistem à convulsão política. Discute o final do romance de Dickens; quem quiser evitar revelações pode ler primeiro o romance. Uma breve conclusão volta à justiça, ao progresso e ao sacrifício, seguida de bibliografia."),
"it": (
"Ombre e luci: Racconto di due città", "Rinascita, rivoluzione e sacrificio in una lettura di Dickens",
"Questa guida interpreta la storia di Dickens tra Londra e Parigi. La liberazione del dottor Manette introduce il tema della rinascita. Lucie e Darnay legano la speranza familiare al pericolo politico. La Rivoluzione mette alla prova lealtà e giustizia. Le scelte di Sydney Carton portano in primo piano il sacrificio. Quattro capitoli seguono tali contrasti senza riprodurre il romanzo.",
"Il primo capitolo contrappone Londra e Parigi prima della Rivoluzione francese e segue il ritorno del dottor Manette dalla Bastiglia. Il secondo esamina gli effetti della prigionia e il rapporto tra Lucie Manette e Charles Darnay. Il libro legge i legami familiari accanto alle forze pubbliche che li minacciano, tornando ai temi della rinascita e del cambiamento storico.",
"I capitoli successivi affrontano la violenza rivoluzionaria, la sete di vendetta di Madame Defarge, il pericolo per Darnay e la scelta di Sydney Carton. L'interpretazione chiede come compassione e lealtà resistano agli sconvolgimenti politici. Tratta il finale del romanzo di Dickens; chi vuole evitare anticipazioni può leggere prima il romanzo. Una breve conclusione torna su giustizia, progresso e sacrificio, seguita dalla bibliografia."),
"pl": (
"Cienie i światła: Opowieść o dwóch miastach", "Odrodzenie, rewolucja i poświęcenie w lekturze Dickensa",
"Ten przewodnik interpretuje historię Dickensa między Londynem a Paryżem. Uwolnienie doktora Manette'a wprowadza motyw odrodzenia. Lucie i Darnay łączą rodzinną nadzieję z politycznym zagrożeniem. Rewolucja wystawia na próbę lojalność i sprawiedliwość. Wybory Sydneya Cartona wysuwają na pierwszy plan poświęcenie. Cztery rozdziały śledzą te kontrasty, nie przedrukowując powieści.",
"Pierwszy rozdział zestawia Londyn i Paryż przed rewolucją francuską, a potem śledzi powrót doktora Manette'a z Bastylii. Drugi bada skutki jego uwięzienia oraz relację Lucie Manette i Charlesa Darnaya. Książka ukazuje więzi rodzinne obok sił publicznych, które im zagrażają, powracając do odrodzenia i przemian historycznych.",
"Kolejne rozdziały dotyczą przemocy rewolucyjnej, pragnienia zemsty Madame Defarge, zagrożenia Darnaya i wyboru Sydneya Cartona. Interpretacja pyta, jak współczucie i lojalność przetrwają polityczne wstrząsy. Omawia zakończenie powieści Dickensa; czytelnicy unikający zdradzenia fabuły mogą najpierw przeczytać powieść. Krótkie podsumowanie powraca do sprawiedliwości, postępu i poświęcenia, po czym następuje bibliografia."),
}
for lang, (title, subtitle, short, first, second) in copy.items():
    parts = short.split(". ")
    assert len(parts) == 6 and all(len(s.split()) <= 22 for s in parts), lang
    assert 60 <= len((first + " " + second).split()) <= 250, lang
    m["title"][lang] = title
    m["subtitle"][lang] = subtitle
    m["shortDescription"][lang] = short
    m["aboutBook"][lang] = [first, second]
m["shortDescriptionEditorial"] = {
    "method": "active-LLM authored and translated from complete chapters and ten-minute reader",
    "sourceSha256": "e967e0df05f3e967881f512952efdd34bf70a3fd23b1b0af45b2c9ea47895a0e",
    "sentencesPerLanguage": 6,
    "status": "reviewed",
}
m["metadataDraft"] = {
    "sourceSha256": "e967e0df05f3e967881f512952efdd34bf70a3fd23b1b0af45b2c9ea47895a0e",
    "reviewRequired": False,
    "basis": "Four complete interpretive chapters, substantive conclusion, bibliography, and canonical short reader",
    "reviewedOn": "2026-10-08",
}
p.write_text(json.dumps(m, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(p)
