import json
from pathlib import Path
p = Path(__file__).resolve().parent / 'translations/ro/short/chunks'
t = {
 't000001':'Explorând marea transformare a gândirii economice — Ediția de zece minute',
 't000002':'Explorând marea transformare a gândirii economice',
 't000003':'Agentul IA Adria Morgan · 2024',
 't000004':'Cartea examinează schimbarea economică prin perspectiva lui Karl Polanyi asupra relației dintre piață și societate. Întreabă ce se întâmplă când activitatea economică este separată de obligațiile sociale și cum răspund comunitățile atunci când extinderea pieței le amenință siguranța. Patru capitole trec de la fundamentele gândirii economice la perturbări sociale, măsuri de protecție și integrarea libertății economice cu responsabilitatea socială. Introducerea și concluzia leagă argumentele de dezbaterile despre inegalitate, tehnologie și durabilitatea mediului.',
 't000005':'Introducere — Economia în interiorul societății',
 't000006':'Sistemele economice modelează viața cotidiană și instituțiile sociale. Introducerea cere examinarea nu numai a prețurilor și creșterii, ci și a contextelor culturale, politice și etice ale deciziilor economice. Ea opune piețele nereglementate supravegherii sociale și leagă distribuția averii, drepturile lucrătorilor și problemele mediului de discuția despre dreptate. Cititorii sunt invitați să-și examineze propriul rol de consumatori, lucrători și cetățeni.',
 't000007':'Citește introducerea în ediția integrală',
 't000008':'Fundamente — De la reciprocitate la piață',
 't000009':'Primul capitol descrie comunitățile anterioare pieței, unde schimburile economice făceau parte din cooperare, tradiție și sprijin reciproc. Comerțul și industrializarea au slăbit această organizare și au susținut ideea pieței autoreglate. Prețurile au devenit semnale pentru producție și consum, iar oamenii au fost prezentați tot mai mult ca indivizi care își urmăresc interesul propriu. Polanyi avertizează că urmărirea eficienței poate intra în conflict cu legăturile comunitare și valorile sociale. Capitolul tratează gândirea economică drept expresie a priorităților umane, nu doar ca ansamblu de modele abstracte.',
 't000010':'Citește capitolul I în ediția integrală',
 't000011':'Perturbările pieței — Costurile sociale ale extinderii',
 't000012':'Extinderea pieței schimbă relațiile care țin comunitățile împreună. Al doilea capitol susține că transformarea muncii, pământului și banilor în mărfuri poate reduce lucrătorii la utilitatea lor economică și poate slăbi vechile legături de reciprocitate. El leagă schimbarea de înstrăinare, inegalitate și vulnerabilitate în crize, inclusiv Marea Criză. Susținătorii pieței și cei ai protecției sociale nu sunt de acord dacă intervenția statului amenință eficiența sau previne instabilitatea. Cartea prezintă această tensiune ca problemă definitorie a economiilor moderne.',
 't000013':'Citește capitolul II în ediția integrală',
 't000014':'Protecție — Răspunsul societății la piață',
 't000015':'Capitolul al treilea urmărește răspunsurile de protecție la presiunile pieței. Sindicatele au negociat colectiv salarii echitabile, programe rezonabile și locuri de muncă mai sigure. Guvernele au creat asigurări de șomaj, legi ale salariului minim, programe de sănătate publică și reguli împotriva monopolurilor și concurenței neloiale. Cartea leagă trecerea spre intervenție de Marea Criză și de ideile keynesiene. Ea arată și că protecția trebuie adaptată globalizării, muncii pe platforme, schimbărilor tehnologice și șocurilor precum pandemia. Scopul este apărarea demnității și bunăstării sociale fără abandonarea activității economice.',
 't000016':'Citește capitolul III în ediția integrală',
 't000017':'Un drum înainte — Libertate cu responsabilitate',
 't000018':'Capitolul final susține că libertatea economică și protecția trebuie să se dezvolte împreună. El descrie capitalismul părților interesate, în care firmele țin seama de angajați, clienți și comunități alături de acționari, și întreprinderile sociale care îmbină veniturile cu misiuni sociale. Politica publică poate stabili norme echitabile de muncă și mediu, permițând inovația și concurența. Educația, participarea civică și societatea civilă îi ajută pe oameni să influențeze aceste alegeri. Schimbările climatice și economia digitală fac combinația urgentă: investițiile verzi și recalificarea pot crea oportunități dacă tranziția este incluzivă.',
 't000019':'Citește capitolul IV în ediția integrală',
 't000020':'Concluzie — Piețele sunt alegeri umane',
 't000021':'Concluzia revine la ideea lui Polanyi că piețele sunt modelate de relații și valori sociale. Ea cere decizii economice care țin seama de bunăstare, limite ecologice și responsabilitate comună. Crizele financiare, inegalitatea, schimbarea digitală și degradarea mediului păstrează vizibilă tensiunea dintre libertatea pieței și protecție. Cartea nu oferă un singur model instituțional fix; cere cetățenilor, firmelor, guvernelor și comunităților să colaboreze pentru o economie care slujește mai mult decât câțiva oameni. Bibliografia enumeră lucrări de Smith, Hayek, Mises, Friedman și Keynes.',
 't000022':'Citește concluzia în ediția integrală',
}
for x in sorted(p.glob('*.json')):
    d = json.loads(x.read_text())
    for s in d['segments']:
        assert s['id'] in t
        assert not s['translation'] or s['translation'] == t[s['id']]
        s['translation'] = t[s['id']]
    x.write_text(json.dumps(d, ensure_ascii=False, indent=2) + '\n')
