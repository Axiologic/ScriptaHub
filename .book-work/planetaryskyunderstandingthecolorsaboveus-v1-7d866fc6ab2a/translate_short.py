import json,pathlib
p=pathlib.Path('.book-work/planetaryskyunderstandingthecolorsaboveus-v1-7d866fc6ab2a/translations/ro/short/chunks')
t={
't000001':'Cerul planetar: înțelegerea culorilor de deasupra noastră — Ediția de zece minute',
't000002':'Cerul planetar: înțelegerea culorilor de deasupra noastră',
't000003':'Agentul IA Althea Zappa · 2024',
't000004':'Introducere — De ce se schimbă cerul',
't000005':'''Introducerea leagă culoarea cerului de lumina solară, gazele atmosferice, împrăștierea luminii și poziția Soarelui. Ea explică de ce lumina albastră a zilei, apusurile roșii și variațiile sezoniere fac parte din aceeași poveste fizică. Cartea extinde apoi această poveste către vreme, poluare, alte planete, măsurare și cultură. Cititorii pot începe întrebându-se ce particule întâlnește lumina în drumul spre ochii lor.''',
't000007':'Capitolul întâi — Imaginând alte ceruri',
't000008':'''Primul capitol străbate cerurile dincolo de Pământ, de la nuanțele prăfuite ale lui Marte la atmosfera densă a lui Venus și norii colorați ai planetelor gigantice. Exemplele arată că alcătuirea atmosferei, particulele suspendate și iluminarea determină ceea ce ar putea vedea un observator. Descrierile stârnesc curiozitatea, dar recunosc că experiența directă pe lumi ostile este ipotetică.''',
't000010':'Capitolul al doilea — Albastrul Pământului',
't000011':'''Atmosfera Pământului, bogată în azot și oxigen, împrăștie lungimile de undă scurte ale luminii solare mai eficient decât pe cele lungi. Capitolul prezintă împrăștierea Rayleigh și explică de ce un drum mai lung prin atmosferă poate lăsa apusului culori mai calde. Analizează și aerosolii, alături de alte condiții care complică explicația simplă a cerului albastru.''',
't000013':'Capitolul al treilea — Lumina și particulele',
't000014':'''Capitolul așază lumina vizibilă în spectrul electromagnetic și examinează lungimea de undă, reflexia, absorbția și împrăștierea. Procesele Rayleigh și Mie explică de ce moleculele, picăturile și particulele mai mari produc aspecte diferite. Mărimea lor în raport cu lungimea de undă le oferă cititorilor un instrument practic pentru interpretarea culorilor schimbătoare ale cerului.''',
't000016':'Capitolul al patrulea — Un tablou în mișcare',
't000017':'''Unghiul Soarelui schimbă distanța străbătută de lumină prin aer, modificând echilibrul culorilor de la zori la amiază și apus. Norii, umezeala, altitudinea și anotimpurile adaugă alte variații. Capitolul arată cum observațiile obișnuite reflectă interacțiunea dintre lumina solară, atmosferă și vreme, nu o proprietate fixă a cerului.''',
't000019':'Capitolul al cincilea — Calitatea aerului văzută în culori',
't000020':'''Poluanți precum particulele în suspensie, oxizii de azot și ozonul pot modifica împrăștierea luminii și reduce vizibilitatea. Pâcla și fumul pot estompa cerul sau intensifica unele apusuri, afectând în același timp sănătatea și ecosistemele. Capitolul leagă ceea ce vedem deasupra noastră de emisii, fumul incendiilor și necesitatea măsurării și îmbunătățirii calității aerului.''',
't000022':'Capitolul al șaselea — Semnele vizibile ale vremii',
't000023':'''Umiditatea, norii și furtunile schimbă felul în care lumina ajunge la observatori. Norii cumulus, stratus și cei înalți produc texturi și culori diferite, iar praful și vremea severă pot crea ceruri spectaculoase. Capitolul tratează aspectul cerului drept indiciu al proceselor atmosferice, cu o limită importantă: culoarea singură nu oferă o prognoză completă.''',
't000025':'Capitolul al șaptelea — Anul deasupra noastră',
't000026':'''Înălțimea Soarelui și caracterul aerului se schimbă odată cu anotimpurile. Vara, toamna și iarna aduc combinații diferite de aer limpede, umezeală și nori. Latitudinea, altitudinea și poluarea urbană fac ca tiparul să fie local, nu universal. O observație atentă poate dezvălui cum se schimbă același loc de-a lungul anului.''',
't000028':'Capitolul al optulea — Atmosferele altor lumi',
't000029':'''Revenind la alte planete, capitolul pune accent pe dovezile atmosferice. Marte, Venus, planetele gigantice și posibilele exoplanete ilustrează felul în care gazele, norii și praful absorb ori împrăștie diferite lungimi de undă. Comparația evidențiază și cât de neobișnuit este familiarul albastru al Pământului printre numeroasele ceruri planetare posibile.''',
't000031':'Capitolul al nouălea — Măsurarea a ceea ce vedem',
't000032':'''Culoarea cerului poate fi studiată cu aparate foto, spectrometre, instrumente satelitare și colorimetrie. Capitolul întreabă cum transformă cercetătorii o impresie vizuală schimbătoare în măsurători comparabile. Observația standardizată ajută la urmărirea condițiilor atmosferice, a poluării și a luminii chiar și când ochiul omenesc nu observă modificări subtile.''',
't000034':'Capitolul al zecelea — Sensuri dincolo de fizică',
't000035':'''Artiștii, scriitorii și comunitățile au folosit de mult culorile cerului pentru a exprima emoții, a spune povești și a transmite observații despre vreme. Capitolul trece prin pictură, literatură, mitologie și efectul psihologic al luminii schimbătoare. Explicația fizică nu șterge aceste sensuri, ci adaugă încă un mod de a privi scena de deasupra noastră.''',
't000037':'Capitolul al unsprezecelea — Ce s-ar putea schimba',
't000038':'''Schimbările climatice, controlul poluării și posibilele intervenții de geoinginerie ar putea modifica aspectul viitor al cerului. Capitolul le tratează ca proiecții și posibilități, nu ca predicții certe pentru fiecare loc. Urmărirea compoziției și culorii atmosferei ar putea ajuta la observarea schimbărilor de mediu și ne amintește că alegerile oamenilor afectează aerul.''',
't000040':'Concluzie — Să privim cerul cu atenție',
't000041':'''Concluzia reunește fizica luminii, comparația planetară, observația și semnificațiile culturale. Cerul este atât o înregistrare fizică a luminii care traversează atmosfera, cât și o sursă de uimire omenească. Ediția integrală dezvoltă mecanismele, exemplele și incertitudinile fiecărui capitol, invitând cititorii să observe mai atent și să protejeze atmosfera care face posibile culorile familiare ale Pământului.''',
't000043':'Bibliografie — Surse pentru aprofundare',
't000044':'''Bibliografia enumeră lucrări de meteorologie, optică atmosferică și cercetare a culorii cerului folosite de ediția sursă. Ea le oferă cititorilor puncte de plecare pentru verificarea explicațiilor fizice și continuarea studiului dincolo de capitolele narative.'''}
for n in (6,9,12,15,18,21,24,27,30,33,36,39,42,45):t[f't{n:06}']='Citește această secțiune în ediția integrală'
seen=set()
for f in sorted(p.glob('*.json')):
 d=json.loads(f.read_text())
 for x in d['segments']:
  assert not x['translation'] and x['id'] in t;x['translation']=t[x['id']];seen.add(x['id'])
 f.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
assert seen==set(t)
print('Translated',len(seen))
