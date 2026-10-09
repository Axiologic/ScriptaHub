import json
from pathlib import Path
root=Path(__file__).resolve().parent/'translations/ro/short/chunks'
t={
't000001':'100 de întrebări periculoase: Eliberarea din plasa controlului și înșelăciunii — Ediția de zece minute',
't000002':'100 de întrebări periculoase: Eliberarea din plasa controlului și înșelăciunii',
't000003':'Cartea este organizată în întrebări, nu ca o singură teorie care explică societatea. Fiecare răspuns prezintă mai întâi o perspectivă cunoscută, apoi întreabă ce ar putea scăpa acelei perspective. Subiectele merg de la tradiții și relații intime la muncă, religie, autoritate politică, tehnologie și identitate personală. Multe pasaje propun posibilități provocatoare; sunt invitații de a examina presupuneri, nu concluzii demonstrate. Această ediție scurtă urmărește cele zece grupuri de întrebări.',
't000004':'Societate și cultură — Ce obiceiuri urmăm?',
't000005':'Întrebările de început examinează tradițiile, democrația, celebritatea, mass-media și naționalismul. Obiceiurile pot păstra memoria și apartenența, dar pot și proteja autoritatea de critică. Alegerile promit reprezentare, însă banii și puterea instituțională pot restrânge opțiunile oamenilor. Cartea îi îndeamnă pe cititori să deosebească scopul declarat al unei practici de efectele ei și să cerceteze afirmațiile despre manipulare, nu să le accepte automat.',
't000006':'Citește capitolul unu în ediția completă',
't000007':'Iubire și relații — Ce legături alegem?',
't000008':'Întrebările despre iubirea romantică, căsătorie, iertare, respectul de sine și comunicare contestă idealurile familiare ale intimității. Căsătoria poate oferi stabilitate și grijă, dar poate reflecta și așteptări economice și sociale. Iertarea poate repara o relație, însă poate fi cerută și unei persoane care suferă un rău. Capitolul întreabă cât dintr-o legătură vine din grija reciprocă și cât din scenarii moștenite sau din teama de singurătate.',
't000009':'Citește capitolul doi în ediția completă',
't000010':'Economie și muncă — Cine beneficiază de reguli?',
't000011':'Inegalitatea averilor, economia muncii la cerere, sărăcia, profitul companiilor și idealul muncii permanente sunt toate analizate critic. Cartea întreabă dacă munca precară oferă flexibilitate sau transferă riscul asupra lucrătorilor și dacă sistemele economice răsplătesc meritul atât de constant pe cât susțin poveștile lor. Acestea sunt prezentate ca dezbateri despre instituții și stimulente, nu ca dovadă că un singur actor ascuns a proiectat fiecare rezultat.',
't000012':'Citește capitolul trei în ediția completă',
't000013':'Religie și credință — Ce face posibilă credința?',
't000014':'Întrebările privesc credința moștenită, conducerea religioasă, ideile sacre și promisiunile despre viața de apoi. Credința poate oferi sens, comunitate și îndrumare etică. Ea poate fi însă folosită și de instituții pentru a descuraja dezacordul sau a justifica puterea. Capitolul invită cititorii să examineze ambele posibilități, fără a considera că fiecare credincios este înșelat ori că fiecare autoritate religioasă merită încredere.',
't000015':'Citește capitolul patru în ediția completă',
't000016':'Sine și existență — Cât de libere sunt alegerile noastre?',
't000017':'Controlul personal, conștiința, liberul arbitru, bunătatea și căutarea sensului stau la baza acestui grup. Textul întreabă cum modelează biologia, așteptările sociale și presiunile externe deciziile care ni se par independente. Analizează și dacă acțiunile aparent generoase pot avea motive amestecate. Întrebările nu tranșează dezbaterile filosofice; îi invită pe cititori să examineze ce dovezi ar susține o afirmație despre capacitatea de a alege.',
't000018':'Citește capitolul cinci în ediția completă',
't000019':'Societate și putere — Cine definește dreptatea?',
't000020':'Următorul grup întreabă dacă legile, poliția, meritocrația și conducerea politică îi slujesc pe toți în mod egal. Așază idealurile imparțialității alături de îngrijorări privind inegalitatea de avere, statut și influență. Un sistem poate pretinde că protejează siguranța publică, distribuind totuși beneficiile inegal. Capitolul îi invită pe cititori să analizeze aceste tensiuni fără a presupune că fiecare decizie oficială este coruptă.',
't000021':'Citește capitolul șase în ediția completă',
't000022':'Relații și norme — Ce ascundem pentru a aparține?',
't000023':'Întrebările despre conformism, stigmatizarea sănătății mintale, identitatea de gen, standardele de frumusețe, prietenie și rolurile familiale arată cum recunoașterea poate veni cu condiții. Așteptările sociale pot oferi limbaj și sprijin comun, dar îi pot face și pe oameni să ascundă părți din ei înșiși. Textul întreabă cine stabilește ce este normal și ce se întâmplă cu cei care nu pot sau nu vor să respecte acel standard.',
't000024':'Citește capitolul șapte în ediția completă',
't000025':'Muncă și avere — Ce înseamnă succesul?',
't000026':'Al doilea grup economic revine la visul că munca asiduă garantează singură avansarea. Întreabă cum complică această credință privilegiul, stigmatizarea șomajului, orele lungi, cultura consumului și automatizarea. Productivitatea măsurată prin timp poate ignora rezultatele reale; averea poate extinde opțiunile fără să aducă neapărat mulțumire. Aceste întrebări încurajează o privire mai atentă asupra modului în care este măsurat succesul și asupra celor care suportă costurile eșecului.',
't000027':'Citește capitolul opt în ediția completă',
't000028':'Spiritualitate și moralitate — A cui interpretare prevalează?',
't000029':'Al nouălea grup compară viața morală în interiorul și în afara religiei, apoi întreabă de ce unele texte sunt citite literal, iar altele metaforic. Analizează și frica de moarte, suferința, practica spirituală și pretențiile unei morale universale. Întrebarea recurentă este cum alege autoritatea o interpretare și cum îi afectează această alegere pe cei cu mai puțină putere. Rămân posibile răspunsuri diferite.',
't000030':'Citește capitolul nouă în ediția completă',
't000031':'Tehnologie și media — Sunt legate comoditatea și controlul?',
't000032':'Ultimul grup întreabă ce fac dependența digitală, inteligența artificială, algoritmii, compromisurile privind viața privată și informațiile nesigure cu judecata umană. Tehnologiile conectează oamenii și lărgesc accesul la cunoaștere, însă sistemele care selectează informația pot modela și ceea ce primește atenție. Cartea se încheie îndemnând cititorii să își testeze presupunerile, în loc să se predea fricii sau liniștirii facile.',
't000033':'Citește capitolul zece în ediția completă',
}
for p in sorted(root.glob('*.json')):
 d=json.loads(p.read_text())
 for s in d['segments']:s['translation']=t[s['id']]
 p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
