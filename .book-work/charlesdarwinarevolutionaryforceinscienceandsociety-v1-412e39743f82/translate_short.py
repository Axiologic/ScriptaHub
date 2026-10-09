import json
from pathlib import Path

root = Path('.book-work/charlesdarwinarevolutionaryforceinscienceandsociety-v1-412e39743f82/translations/ro/short/chunks')
translations = {
    't000001': 'Charles Darwin: o forță revoluționară în știință și societate',
    't000002': 'Charles Darwin: o forță revoluționară în știință și societate',
    't000003': 'Agentul AI Ava DuRhodes',
    't000004': '''Teoria evoluției prin selecție naturală formulată de Darwin a schimbat felul în care oamenii de știință explică diversitatea vieții. Cartea urmărește formarea, rafinarea și consecințele mai largi ale acestei teorii. Începe cu o întrebare deliberat speculativă despre ce ar crede Darwin despre biologia actuală, apoi revine la educația sa, călătoria pe Beagle și raționamentul din spatele lucrării sale. Capitolele următoare urmăresc genetica, disputele dintre știință și religie, folosirea abuzivă în societate a limbajului evoluționist și aplicațiile practice. Firul călăuzitor este metoda lui Darwin: observă cu grijă, compară dovezile și revizuiește explicațiile când apar cunoștințe noi.''',
    't000005': 'Darwin și biologia modernă',
    't000006': '''Primul capitol își imaginează cum ar întâmpina Darwin descoperirile care nu erau disponibile în timpul vieții sale. ADN-ul și genetica oferă o explicație fizică a eredității pe care el nu o avea. Textul analizează cum mutațiile, genetica populațiilor, deriva genetică și biologia evolutivă a dezvoltării ar extinde întrebările sale despre variație și selecție. Menționează și mutațiile neutre, schimbări care nu îmbunătățesc neapărat supraviețuirea. Aceste reacții imaginate sunt prezentate ca speculații, nu ca citate din Darwin. Capitolul întreabă unde se încheie evoluția biologică și dacă tehnologia și cultura aduc noi forțe ale schimbării.''',
    't000007': 'Citește capitolul integral',
    't000008': 'Drumul către Beagle',
    't000009': '''Darwin s-a născut într-o familie interesată de știință. Prefera observarea naturii în locul programei clasice de la școală, iar pregătirea medicală de la Edinburgh nu i s-a potrivit. La Cambridge, deși se pregătea pentru cler, a colecționat gândaci și a legat o relație decisivă cu botanistul John Stevens Henslow. Mai târziu, Henslow l-a recomandat pentru locul de la bordul navei HMS Beagle. Capitolul arată cum familia, studiile, mentorii și obișnuința timpurie de a observa s-au întâlnit înainte ca Darwin să aibă o teorie a evoluției.''',
    't000010': 'Citește capitolul integral',
    't000011': 'Călătoria pe Beagle',
    't000012': '''Beagle a pornit în 1831 într-o misiune de cercetare care s-a transformat într-o călătorie de aproape cinci ani. Darwin a călătorit ca naturalist, adunând specimene și însemnări în America de Sud și dincolo de ea. Straturile geologice din Capul Verde sugerau schimbări lente, de-a lungul unor perioade uriașe; fosilele și animalele vii îl îndemnau să compare diferite locuri. Insulele Galápagos au devenit deosebit de importante când a examinat diferențele dintre forme înrudite de la o insulă la alta. Călătoria nu i-a oferit selecția naturală drept idee gata încheiată. I-a oferit observații care făceau tot mai greu de susținut că speciile rămân neschimbate.''',
    't000013': 'Citește capitolul integral',
    't000014': 'Originile teoriei',
    't000015': '''După întoarcerea în Anglia, în 1836, Darwin și-a organizat colecțiile și a început caietele despre transformarea speciilor. Identificarea de către John Gould a cintezelor înrudite din Galápagos i-a îndreptat atenția asupra distribuției geografice. Lectura lui Thomas Malthus l-a ajutat să înțeleagă că organismele produc mai mulți urmași decât pot susține resursele limitate. Dacă trăsăturile moștenite variază, indivizii cu trăsături avantajoase pot lăsa mai mulți urmași, iar populațiile se pot schimba de-a lungul generațiilor. Capitolul urmărește această muncă intelectuală până la publicarea lucrării Despre originea speciilor în 1859.''',
    't000016': 'Citește capitolul integral',
    't000017': 'Evoluția după Darwin',
    't000018': '''Publicarea lucrării lui Darwin a deschis o nouă etapă a cercetării. Redescoperirea studiilor lui Mendel despre ereditate și dezvoltarea geneticii populațiilor au legat ulterior moștenirea trăsăturilor de selecția naturală. Cartea amintește o perioadă timpurie în care explicații concurente, inclusiv moștenirea caracterelor dobândite și evoluția dirijată, au contestat darwinismul. Sinteza modernă a unit genetica și selecția; biologia moleculară și biologia evolutivă a dezvoltării au continuat să rafineze explicația. Lecția este că teoria evoluției a crescut prin critică, măsurare și integrarea unor domenii noi.''',
    't000019': 'Citește capitolul integral',
    't000020': 'Gândire și societate',
    't000021': '''Evoluția a pus sub semnul întrebării relatările literale despre specii fixe, create separat, și a ridicat întrebări despre locul omului în natură. Argumentele lui Darwin au intrat în dezbateri teologice și filosofice, însă capitolul deosebește explicația științifică de folosirile politice ale vocabularului ei. Darwinismul social și eugenia au împrumutat limbajul evoluționist pentru a justifica ierarhia și constrângerea; aceste programe nu decurg pur și simplu din selecția naturală. Discuția se îndreaptă apoi spre dezbaterile actuale despre comportamentul uman, moralitate și interacțiunea influențelor biologice și culturale.''',
    't000022': 'Citește capitolul integral',
    't000023': 'Implicații tehnologice',
    't000024': '''Ultimul capitol de conținut leagă ideile evoluționiste de practică. Selecția artificială a modelat cultivarea plantelor și creșterea animalelor; atenția acordată diversității genetice contribuie la păstrarea semințelor și la conservare. Înțelegerea evoluției bacteriilor și virusurilor contează pentru rezistența la antibiotice și dezvoltarea vaccinurilor. Cartea descrie și algoritmii genetici, inteligența de roi și biologia sintetică drept domenii care se inspiră, în moduri diferite, din variație, selecție și adaptare. Acestea sunt aplicații și analogii, nu dovezi că fiecare tehnologie funcționează ca o specie vie.''',
    't000025': 'Citește capitolul integral',
    't000026': 'Ce rămâne util',
    't000027': '''Moștenirea lui Darwin este deopotrivă o teorie și un model de cercetare. Genomica modernă și biologia dezvoltării au întărit și revizuit explicațiile evoluționiste, în timp ce pierderea biodiversității, bolile și schimbările mediului mențin actualitatea întrebărilor. Citește capitolele integrale pentru a urmări dovezile și disputele din spatele acestei prezentări condensate, inclusiv locurile în care cartea speculează despre reacția lui Darwin la cunoștințe pe care nu le-ar fi putut vedea.''',
    't000028': 'Citește cartea integrală',
}
for path in root.glob('*.json'):
    data = json.loads(path.read_text())
    for segment in data['segments']:
        if segment['id'] in translations:
            segment['translation'] = translations[segment['id']]
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')
print('Translated', len(translations), 'short-reader segments')
