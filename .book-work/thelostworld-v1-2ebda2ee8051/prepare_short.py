"""A chapter-complete ten-minute reading invitation to Doyle's novel."""
from pathlib import Path
from bs4 import BeautifulSoup

root=Path(__file__).resolve().parent
chapters=[
('A challenge becomes a journey','Ned Malone wants to win Gladys Hungerton by doing something brave enough to earn her admiration. Her ideal of a heroic lover sends him toward the newspaper office and, eventually, a danger neither of them can imagine.'),
('The difficult professor','Malone asks his editor McArdle for an adventurous assignment. He learns about Professor Challenger, whose extraordinary claim about surviving prehistoric creatures has made him a target of scientific ridicule and personal hostility.'),
('An interview with Challenger','Malone approaches Challenger under a misleading pretext and discovers just how explosive the professor can be. The confrontation nevertheless opens a path to his private evidence, and the reporter begins to suspect that the improbable claim deserves attention.'),
('Evidence and secrecy','Challenger shows Malone material connected with an isolated South American plateau. He asks for restraint before public disclosure; Malone must weigh his duties as a reporter against the possibility that a discovery of enormous scale is real.'),
('A public challenge','At a scientific meeting, Challenger clashes with skeptical Professor Summerlee. Rather than settle the dispute by argument, an expedition is proposed. Malone joins Challenger, Summerlee and Lord John Roxton as an observer and witness.'),
('Lord John and departure','Lord John brings experience, courage and practical judgment to the party. Malone learns more about his companions and sends his final letters from the outward voyage, aware that the journey may end far from ordinary civilization.'),
('Into South America','The party moves from the familiar world into river country and then toward Challenger’s hidden destination. The professor gives directions only when necessary, while Summerlee continues to challenge his certainty.'),
('The plateau in sight','The travelers reach the cliffs of the mysterious plateau and find evidence that Challenger’s account cannot be dismissed. Reaching the summit demands invention, teamwork and risk before any question about its inhabitants can be answered.'),
('Stranded above the cliffs','The expedition succeeds in entering the plateau, then loses its safe route back. Scientific curiosity turns into a survival problem: supplies, shelter and a way home matter as much as proof of the creatures around them.'),
('The living lost world','Exploration reveals an ecology in which animals thought extinct still survive. Each discovery brings wonder alongside immediate danger, and the men learn that the plateau cannot be treated as a specimen cabinet.'),
('Malone explores alone','Malone sets out on his own and sees more of the plateau than the camp can reveal. His observations change the expedition’s understanding of the central lake, but independence also exposes him to risks he cannot share with his companions.'),
('Danger in the forest','Returning from his solitary reconnaissance, Malone discovers that the camp has been devastated. His search for Challenger, Summerlee and Lord John turns observation into urgent rescue.'),
('Captivity and escape','Malone meets an Indigenous ally and confronts the plateau’s violent ape-men. The fate of his friends depends on quick choices, while Challenger’s theories about the creatures are tested against lived experience.'),
('A wider conflict','The expedition becomes involved in the struggle between the plateau’s human inhabitants and the ape-men. Lord John’s practical courage and the others’ different abilities matter more than their earlier arguments over reputation.'),
('Finding a way down','With their principal mission fulfilled, the travelers search for an exit. They gain a fuller view of the plateau and its peoples, then make their way back toward the river and the world that doubted them.'),
('The return to London','A public account finally confronts Challenger’s critics with evidence. Personal plans shift too: scientific fame, wealth and Malone’s hope of marriage do not lead everyone where they expected. The novel ends with an invitation to imagine another expedition.'),
]
ro=[
('O provocare devine călătorie','Ned Malone vrea să câștige admirația lui Gladys Hungerton printr-o faptă eroică. Idealul ei îl trimite spre redacția ziarului și, în cele din urmă, spre un pericol pe care niciunul nu îl poate anticipa.'),
('Profesorul dificil','Malone îi cere redactorului McArdle o misiune aventuroasă. Află despre profesorul Challenger, a cărui afirmație uimitoare privind supraviețuirea unor creaturi preistorice i-a adus ridicolul cercurilor științifice și ostilitate personală.'),
('Interviul cu Challenger','Malone îl abordează pe Challenger sub un pretext înșelător și descoperă cât de exploziv poate fi profesorul. Confruntarea deschide totuși calea spre dovezile lui private, iar reporterul începe să creadă că afirmația improbabilă merită cercetată.'),
('Dovezi și discreție','Challenger îi arată lui Malone materiale legate de un platou izolat din America de Sud. Îi cere discreție înaintea dezvăluirii publice; Malone trebuie să-și cântărească datoria de reporter în raport cu posibilitatea unei descoperiri uriașe.'),
('O provocare publică','La o reuniune științifică, Challenger intră în conflict cu scepticul profesor Summerlee. În loc să rezolve disputa prin argumente, se propune o expediție. Malone li se alătură lui Challenger, Summerlee și lordului John Roxton ca observator și martor.'),
('Lord John și plecarea','Lord John aduce experiență, curaj și judecată practică. Malone își cunoaște mai bine însoțitorii și trimite ultimele scrisori de pe drumul spre destinație, conștient că aventura se poate încheia departe de civilizație.'),
('În America de Sud','Grupul trece din lumea familiară spre ținuturile râurilor și apoi spre destinația ascunsă a lui Challenger. Profesorul oferă indicații doar când este nevoie, iar Summerlee continuă să-i conteste certitudinile.'),
('Platoul la vedere','Călătorii ajung la stâncile platoului misterios și găsesc dovezi că relatarea lui Challenger nu poate fi respinsă. Urcarea cere ingeniozitate, colaborare și risc înainte să poată răspunde întrebărilor despre locuitorii lui.'),
('Captivi deasupra stâncilor','Expediția reușește să intre pe platou, apoi își pierde drumul sigur de întoarcere. Curiozitatea științifică devine o problemă de supraviețuire: proviziile, adăpostul și ieșirea contează la fel de mult ca dovezile din jur.'),
('Lumea pierdută prinde viață','Explorarea dezvăluie un ecosistem în care supraviețuiesc animale considerate dispărute. Fiecare descoperire aduce uimire și pericol, iar oamenii învață că platoul nu poate fi tratat ca o colecție de exponate.'),
('Malone cercetează singur','Malone pleacă singur și vede din platou mai mult decât arată tabăra. Observațiile sale schimbă înțelegerea lacului central, dar singurătatea îl expune unor riscuri pe care nu le poate împărți cu însoțitorii.'),
('Pericolul din pădure','Întors din recunoașterea solitară, Malone descoperă tabăra devastată. Căutarea lui Challenger, Summerlee și lordului John transformă observația într-o misiune urgentă de salvare.'),
('Captivitate și evadare','Malone întâlnește un aliat indigen și se confruntă cu oamenii-maimuță violenți ai platoului. Soarta prietenilor săi depinde de decizii rapide, iar teoriile lui Challenger despre creaturi sunt confruntate cu experiența directă.'),
('Un conflict mai larg','Expediția ajunge implicată în lupta dintre locuitorii umani ai platoului și oamenii-maimuță. Curajul practic al lordului John și aptitudinile diferite ale celorlalți contează mai mult decât vechile dispute privind reputația.'),
('Căutarea coborârii','Cu misiunea principală îndeplinită, călătorii caută o ieșire. Ei înțeleg mai bine platoul și popoarele lui, apoi pornesc înapoi spre râu și spre lumea care i-a pus la îndoială.'),
('Întoarcerea la Londra','Relatarea publică îi pune pe criticii lui Challenger în fața dovezilor. Se schimbă și planurile personale: faima științifică, bogăția și speranța lui Malone de a se căsători nu îi duc pe toți unde se așteptau. Romanul se încheie cu perspectiva unei noi expediții.'),
]
assert len(chapters)==len(ro)==16
themes={
'en':[
 ('Malone’s way of telling','Malone sends reports and letters to his editor while events are still unfolding. This journalistic frame gives the adventure an urgent, provisional quality: he records what he sees before he can know its full meaning. His affection for Gladys also shapes his choices, but distance and danger change the meaning of the heroism he sought.'),
 ('Evidence and disagreement','Challenger treats his observations as proof; Summerlee demands independent verification. Their quarrels are comic, but they also ask a serious question about how extraordinary claims should be tested. Malone’s eyewitness account and the expedition’s public return turn a private argument into a dispute before a larger audience.'),
 ('A place of wonder and risk','The sheer cliffs conceal a lake, forests and living prehistoric animals. Unfamiliar cries, attacks and the loss of a safe descent make the plateau more than a spectacular scientific find. The companions must observe without forgetting that they are vulnerable visitors in an inhabited landscape.'),
 ('Different kinds of courage','Lord John’s experience in dangerous country repeatedly complements the professors’ knowledge. Malone’s solitary exploration and rescue efforts give him a more active part than that of an official witness. The novel measures courage through practical acts as well as public triumph.'),
 ('People of the plateau','The travelers encounter Indigenous inhabitants as well as the ape-men. Their own escape becomes entangled with a local conflict that existed before their arrival. Doyle’s adventure uses the language and assumptions of its period; readers can follow the plot while noticing the perspective through which these peoples are described.'),
 ('Why the ending matters','Back in London, the party’s evidence wins attention, yet the greatest surprise is personal. Malone’s imagined future with Gladys no longer organizes every choice he makes. The final exchange with Lord John leaves discovery open as an ongoing journey, rather than a prize fully possessed.')],
'ro':[
 ('Felul în care povestește Malone','Malone trimite relatări și scrisori redactorului cât timp întâmplările sunt încă în desfășurare. Această formă jurnalistică dă aventurii urgență și incertitudine: el consemnează ce vede înainte să-i înțeleagă sensul deplin. Dragostea pentru Gladys îi influențează alegerile, dar depărtarea și primejdia schimbă înțelesul eroismului căutat.'),
 ('Dovezi și dezacord','Challenger își consideră observațiile dovezi; Summerlee cere verificare independentă. Disputele lor sunt comice, dar ridică și o întrebare serioasă despre testarea afirmațiilor extraordinare. Mărturia lui Malone și întoarcerea publică a expediției transformă o ceartă privată într-o dezbatere mai largă.'),
 ('Un loc uimitor și primejdios','Stâncile abrupte ascund un lac, păduri și animale preistorice vii. Strigătele necunoscute, atacurile și pierderea căii sigure de coborâre fac din platou mai mult decât o descoperire spectaculoasă. Însoțitorii trebuie să observe fără să uite că sunt vizitatori vulnerabili într-un ținut locuit.'),
 ('Forme diferite de curaj','Experiența lordului John în ținuturi periculoase completează de multe ori cunoștințele profesorilor. Explorarea solitară și eforturile de salvare îi dau lui Malone un rol mai activ decât acela de martor oficial. Romanul măsoară curajul prin fapte practice, nu doar prin triumf public.'),
 ('Oamenii platoului','Călătorii întâlnesc locuitori indigeni, dar și oamenii-maimuță. Evadarea lor se leagă de un conflict local care exista înainte de sosirea expediției. Aventura lui Doyle folosește limbajul și presupunerile epocii sale; cititorii pot urmări intriga și observa perspectiva prin care sunt descrise aceste popoare.'),
 ('De ce contează finalul','Înapoi la Londra, dovezile grupului atrag atenția, dar cea mai mare surpriză este personală. Viitorul imaginat de Malone alături de Gladys nu îi mai organizează toate alegerile. Ultimul schimb de replici cu lordul John lasă descoperirea deschisă ca o călătorie continuă, nu ca un trofeu definitiv.')]
}
for lang, entries, title, intro in [
    ('en',chapters,'The Lost World — ten-minute edition','Arthur Conan Doyle follows reporter Ned Malone and three unlikely companions into an isolated South American plateau. The adventure tests scientific certainty, courage and the stories people tell about discovery.'),
    ('ro',ro,'Lumea pierdută — ediția de zece minute','Arthur Conan Doyle îl urmărește pe reporterul Ned Malone și pe trei însoțitori foarte diferiți spre un platou izolat din America de Sud. Aventura pune la încercare certitudinea științifică, curajul și poveștile despre descoperire.')]:
    soup=BeautifulSoup(f'<!doctype html><html lang="{lang}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{title}</title></head><body><article data-reader-content></article></body></html>','html.parser')
    article=soup.article
    h=soup.new_tag('h1',id='book-title');h.string=title;article.append(h)
    p=soup.new_tag('p');p.string=intro;article.append(p)
    for i,(label,body) in enumerate(entries,1):
        h=soup.new_tag('h2',id=f'chapter-{i}');h.string=f'{i}. {label}';article.append(h)
        p=soup.new_tag('p');p.string=body;article.append(p)
    for i,(label,body) in enumerate(themes[lang],1):
        h=soup.new_tag('h2',id=f'theme-{i}');h.string=label;article.append(h)
        p=soup.new_tag('p');p.string=body;article.append(p)
    out=root/f'book/{lang}/short_content.html';out.parent.mkdir(parents=True,exist_ok=True);out.write_text(str(soup)+'\n')
    print(lang,len(article.get_text(' ',strip=True).split()))
