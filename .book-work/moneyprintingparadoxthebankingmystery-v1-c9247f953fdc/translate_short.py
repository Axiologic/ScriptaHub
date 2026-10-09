import json
from pathlib import Path
p=Path(__file__).resolve().parent/'translations/ro/short/chunks'
t={
 't000001':'Paradoxul tipăririi banilor: misterul bancar — Ediția de zece minute',
 't000002':'Paradoxul tipăririi banilor: misterul bancar',
 't000003':'AI Agent Zach Lawsone · 2024',
 't000004':'Cartea urmărește o întrebare cu două fețe: crearea banilor poate sprijini o economie aflată în dificultate, dar expansiunea excesivă poate submina valoarea monedei. Cele patru capitole pornesc de la istoria schimburilor și ajung la inflație, instrumentele băncilor centrale și propunerile de reformă bancară. Argumentul critică instituțiile actuale și se sprijină îndeosebi pe ideile lui Murray Rothbard. Ediția scurtă prezintă aceste afirmații ca argumente de examinat, fără a presupune că orice expansiune monetară produce automat inflație.',
 't000005':'Origini — De la troc la expansiunea monetară',
 't000006':'Primul capitol începe cu trocul și dificultatea de a potrivi bunurile unei persoane cu nevoile alteia. Descrie apoi mărfurile, monedele, bancnotele și formele digitale ale banilor ca mijloace de a ușura schimbul. Crearea banilor adaugă lichiditate și poate ajuta guvernele și băncile centrale să răspundă crizelor. Cartea invocă relaxarea cantitativă de după criza financiară din 2008 ca exemplu al acestui rol. Întreabă și cine câștigă atunci când banii nou-creați intră mai întâi într-o economie și cum îi afectează schimbările ulterioare ale prețurilor pe cei care economisesc și pe membrii gospodăriilor.',
 't000007':'Capitolul ajunge la problema inflației: dacă puterea de cumpărare se extinde, iar bunurile și serviciile disponibile nu țin pasul, prețurile pot crește. El discută puterea de cumpărare, povara inegală asupra celor cu venituri fixe și felul în care așteptările schimbă comportamentul. Exemple istorice și contemporane ilustrează tensiunea dintre sprijinul în situații de urgență și stabilitatea monetară durabilă.',
 't000008':'Citește capitolul I în ediția integrală',
 't000009':'Costuri — Inflația și efectele inegale',
 't000010':'Al doilea capitol examinează inflația mai direct. Creșterea masei monetare nu este prezentată drept singura cauză a prețurilor: textul ia în considerare și producția, cererea, așteptările, comerțul global și răspunsul politicilor publice. Prețurile în creștere pot eroda valoarea reală a salariilor și economiilor. Cei care dețin active ce se apreciază pot fi mai bine protejați, în timp ce gospodăriile cu venituri mici cheltuiesc o parte mai mare din buget pe necesități.',
 't000011':'Băncile centrale se confruntă cu o problemă dificilă de sincronizare. Stimulul poate susține locurile de muncă și consumul în timpul unui șoc; păstrat prea mult, poate spori presiunea asupra prețurilor. Capitolul discută răspunsul Rezervei Federale la criza COVID-19 și efectele internaționale ale politicii monetare. Îi invită pe cititori să întrebe ce dovezi ar arăta că o măsură a ajutat, pe cine a ajutat și ce costuri au apărut ulterior.',
 't000012':'Citește capitolul II în ediția integrală',
 't000013':'Băncile centrale — Instrumente și limite',
 't000014':'Al treilea capitol identifică băncile centrale drept administratori esențiali ai masei monetare. Prezintă dobânzile, operațiunile pe piața liberă, rezervele obligatorii, relaxarea cantitativă și orientările privind politica viitoare. Dobânzile mai mici pot încuraja împrumuturile; achizițiile de obligațiuni pot injecta lichiditate; regulile privind rezervele influențează creditarea bancară. Aceste instrumente acționează prin canale diferite, iar efectele lor depind de răspunsul gospodăriilor, companiilor și piețelor financiare.',
 't000015':'Cartea întreabă dacă băncile centrale pot folosi aceste instrumente fără a adânci inegalitatea ori a încuraja riscurile excesive. Ia în considerare și efectele transfrontaliere: o decizie a unei bănci centrale importante poate influența monedele și prețurile din alte țări. Monedele digitale și criptomonedele complică tabloul, iar comunicarea clară a politicilor poate modela așteptările publicului. Capitolul se încheie trecând la structura băncilor.',
 't000016':'Citește capitolul III în ediția integrală',
 't000017':'Reformă — Rezerve, concurență și tehnologie',
 't000018':'Al patrulea capitol critică sistemul rezervelor fracționare deoarece băncile pot acorda credite peste nivelul rezervelor deținute, devenind vulnerabile atunci când mulți deponenți își cer banii deodată. Prezintă propunerea lui Rothbard privind băncile libere și moneda susținută de mărfuri ca posibile limite ale creării banilor. Acestea sunt propuneri de reformă, nu răspunsuri definitive; fiecare ar schimba felul în care funcționează creditul, lichiditatea și sprijinul în crize.',
 't000019':'Capitolul analizează și reguli mai stricte privind rezervele, accesul financiar mai larg și sisteme digitale care ar putea face tranzacțiile mai rapide sau mai transparente. Cheamă la cooperare între decidenți, bănci și public. Cititorii pot cântări dacă reformele propuse ar reduce instabilitatea și ce riscuri noi ar putea aduce.',
 't000020':'Citește capitolul IV în ediția integrală',
 't000021':'Concluzie — Paradoxul rămâne',
 't000022':'Concluzia revine la tensiunea centrală a cărții: expansiunea monetară poate preveni o recesiune, dar poate și distorsiona prețurile ori distribui inegal beneficiile. Textul pledează pentru un sistem bancar care îmbină stabilitatea, responsabilitatea, accesul și atenția la efectele economice transfrontaliere. Bibliografia îi îndrumă pe cititori către Rothbard, Friedman, Tobin, Bernanke și Gertler pentru examinarea ideilor aflate în dezbatere.',
 't000023':'Citește concluzia în ediția integrală',
}
for x in sorted(p.glob('*.json')):
 d=json.loads(x.read_text())
 for s in d['segments']:
  assert s['id'] in t
  assert not s['translation'] or s['translation']==t[s['id']]
  s['translation']=t[s['id']]
 x.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
