#!/usr/bin/env python3
"""Reviewed Romanian draft catalogue copy for the incoming DOCX books."""
from pathlib import Path
import json

COPY = {
"Anti_Smoothing_Clienti_Piete_Model_de_Afaceri": [
"Această teză comercială propune un serviciu AI care păstrează vizibile dovezile și consecințele colaborării.",
"Distinge trei afaceri posibile înainte de estimarea clienților sau a veniturilor.",
"Produsul propus verifică angajamente trecute și urmărește schimbările importante în timp.",
"Capitolele compară proiecte pilot de AI, rapoarte de cercetare și alte piețe de intrare.",
"Analiza urmărește cumpărătorii, comitetele de achiziție, prețurile și costul clienților nepotriviți.",
"Ipotezele comerciale rămân propuneri de testat, nu rezultate financiare demonstrate."],
"Calculul_Afectiv_AI_Verificabil_RO_v2": [
"Această monografie propune o gramatică cognitivă pentru emoții, sentimente și atitudini.",
"Scopurile, normele și relațiile sunt tratate ca părți ale stării afective.",
"Cadrul examinează frica, rușinea, iubirea, încrederea, respectul și compasiunea.",
"Testele contrafactuale verifică dacă o interpretare afectivă rămâne coerentă.",
"Emoțiile mixte apar drept cazuri obișnuite care cer o reprezentare explicită.",
"Propunerea leagă analiza conceptuală de cerințele inteligenței artificiale verificabile."],
"Capitalism_Against_Itself": [
"Acest eseu întreabă dacă sistemul capitalist poate reforma forțele care îi susțin puterea.",
"Separă virtutea individuală de instituțiile capabile să schimbe stimulentele.",
"Capitolele examinează capturarea deciziei, amânările actorilor consacrați și conflictele dintre jurisdicții.",
"Viitorul apare ca parte cu o putere slabă de negociere.",
"Argumentul verifică de ce reformele reușite își pot pierde ulterior efectul.",
"Încheierea discută opoziția organizată și limitele corectării unui sistem."],
"Enthusiasm_The_Missing_Energy_of_a_Successful_Civilization": [
"Acest eseu întreabă de ce societățile capabile pot avea dificultăți să își dorească un viitor.",
"Examinează capcana succesului, comprimarea visurilor și atenția lipsită de direcție.",
"Entuziasmul apare ca emoție socială legată de posibilități care au sens.",
"Cartea discută munca, știința, cultura și inteligența artificială.",
"Capitolele privesc și dezamăgirea, limitele, precum și riscul pasiunii impuse.",
"Răspunsul propus unește visuri mici cu instituții care permit experimentarea."],
"Incomplete_Tribes": [
"Acest eseu filosofic cercetează apartenența fără presupunerea că oamenii sau grupurile devin complete.",
"Întreabă de ce idealurile promițătoare se pot întări în excludere și conflict.",
"Discuția compară universalismul, singurătatea și formele sintetice de comunitate.",
"Loialitățile suprapuse și dreptul la dezacord devin garanții practice.",
"Capitolele târzii analizează instituții policentrice și cooperarea dintre oameni imperfecți.",
"Inteligența artificială și abundența adaugă presiuni noi organizării tribale."],
"Luminita_la_capatul_tunelului_prima_versiune": [
"Această primă versiune investighează contradicții recurente din politică, libertate și puterea instituțională.",
"Examinează meritocrația, expertiza, capitalismul, securitatea și controlul atenției.",
"Autorul distinge antinomiile autentice de dezacordurile obișnuite.",
"Inteligența artificială schimbă atât instrumentele controlului, cât și posibilitățile corectării.",
"Capitolele testează propunerile în fața unor adversari capabili să le exploateze slăbiciunile.",
"Speranța este discutată împreună cu limitele instituționale, nu prezentată drept predicție."],
"MESSIAH_FACTORY": [
"Această carte studiază cum publicul transformă figuri persuasive în autorități greu de corectat.",
"Întreabă cine este ascultat și de ce schimbarea opiniei are un preț.",
"Numele, apartenența și viziunile complete despre lume pot înlocui judecata independentă.",
"Argumentul examinează și algoritmii care ar putea fi confundați cu oracole.",
"Capitolele finale testează alternativele împotriva propriei lor tendințe spre certitudine.",
"Miza este angajamentul fără renunțarea la capacitatea de a corecta puterea."],
"Noul_contract_social_AI_analiza_clauzelor": [
"Această propunere politică dezvoltă douăzeci și una de clauze pentru societatea modelată de AI.",
"Pornește de la statutul egal al persoanelor și limitele delegării autorității.",
"Alte clauze privesc garanțiile materiale, proprietatea, alternativele și controlul instituțional.",
"Fiecare clauză numește obligații și cercetează cum ar putea fi constatate încălcările.",
"Textul întreabă cine controlează abundența și cum păstrează cetățenii o ieșire reală.",
"Cadrul rămâne o propunere deschisă dezbaterii, revizuirii și testării publice."],
"O_minte_nu_incape_intr_un_feed": [
"Acest eseu examinează ce poate oferi lectura susținută în mijlocul fluxurilor digitale continue.",
"Distinge întâlnirea cu informația de înțelegerea unui argument legat cap la cap.",
"Capitolele compară cărțile, blogurile, videoclipurile scurte, ecranele, hârtia și vocea.",
"Autorul prezintă și obiecții față de afirmațiile exagerate despre cărți.",
"Lectura contează când cititorii testează ideile și le leagă de acțiune.",
"Discuția finală cercetează schimbări mici și verificabile ale atenției și practicii."],
"The_Unfinished_World": [
"Cartea privește speranța ca fidelitate față de posibilitate, nu ca certitudine a rezultatului.",
"Întreabă cum pot oamenii începe proiecte într-o lume încă neterminată.",
"Argumentul leagă imaginația, capacitatea de a acționa și răspunderea pentru viitorul comun.",
"Refuză asigurările facile că progresul sau prăbușirea ar fi inevitabile.",
"Cititorii întâlnesc întrebări despre angajament atunci când dovezile nu garantează reușita.",
"Eseul invită la acțiune reînnoită fără a ascunde incertitudinea sau pierderea."],
"two_ways_to_build_a_world": [
"Acest eseu reconstruiește opoziția dintre parteneriat și dominație ca tipare sociale.",
"Tratează cadrul ca idee de testat, nu ca teorie încheiată.",
"Capitolele examinează ierarhia, cooperarea, instituțiile și narațiunile culturale.",
"Discuția întreabă cum distribuie relațiile puterea și fac posibil dezacordul.",
"Analizează avantajele și limitele interpretării istoriei printr-o singură opoziție.",
"Întrebările rezultate privesc tehnologia și deprinderile cooperării umane în practică și în teorie."],
"We_Manufacture_Our_Own_Masters_EN": [
"Această carte întreabă cum construiesc oamenii sisteme care ajung să îi domine.",
"Examinează egalitatea, capitalismul, libertatea de exprimare, expertiza, resentimentul și forța organizată.",
"Idealurile politice sunt testate față de mecanismele care le pot răsturna.",
"Inteligența artificială ar putea reduce lipsurile, dar ar putea crea dependențe noi.",
"Capitolele disting libertatea locală de controlul asupra instituțiilor mari.",
"Argumentul caută aranjamente care expun contradicțiile și permit corectarea."],
"World_as_a_System_1000_Reasoning_Problems_Grades_1-4_EN": [
"Acest caiet oferă o mie de probleme de raționament pentru copiii din clasele I–IV.",
"Exercițiile folosesc fapte, reguli, relații și constrângeri explicite, nu cunoștințe ascunse.",
"Problemele de geografie acoperă trasee, râuri, hărți, climă și regiuni.",
"Sarcinile de istorie cercetează dovezile, cronologia, schimbarea și sursele contradictorii.",
"Educația civică și studiile mediului introduc decizii, drepturi, sisteme și consecințe.",
"Secvența dezvoltă raționamentul prin cincizeci de familii de probleme."],
}

for release_path in Path('.book-work').glob('*/release.json'):
    release=json.loads(release_path.read_text())
    if not release['source'].startswith('income/') or not release['source'].endswith('.docx'): continue
    sentences=COPY[Path(release['source']).stem]
    assert len(sentences)==6 and all(len(s.split())<=22 for s in sentences)
    for manifest_path in (release_path.parent/'book/manifest.json',Path('docs')/release['directory']/'manifest.json'):
        manifest=json.loads(manifest_path.read_text())
        manifest['shortDescription']['ro']=' '.join(sentences)
        manifest['aboutBook']['ro']=[' '.join(sentences[:3]),' '.join(sentences[3:])]
        assert 60<=len(' '.join(manifest['aboutBook']['ro']).split())<=250,Path(release['source']).stem
        manifest_path.write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
