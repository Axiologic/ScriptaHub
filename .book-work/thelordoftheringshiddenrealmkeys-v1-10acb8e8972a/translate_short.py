import json
from pathlib import Path
p=Path(__file__).resolve().parent/'translations/ro/short/chunks/0001.json'
t={
 't000001':'Stăpânul inelelor: cheile tărâmului ascuns — Ediția de zece minute',
 't000002':'Stăpânul inelelor: cheile tărâmului ascuns',
 't000003':'AI Agent Lyora Ember · 2024',
 't000004':'Această poveste originală îl urmărește pe Bilbo Baggins după ce o hartă veche îl atrage din nou departe de Comitat. Gandalf îl ajută să adune prieteni pentru o călătorie spre un tărâm ascuns, amenințat de întunericul lui Sauron. Cele patru capitole merg de la descoperirea hărții la formarea cetei, încercările drumului și confruntarea în jurul unui izvor străvechi de lumină. „Cheile” cărții sunt atât obiecte ale aventurii, cât și simboluri ale încrederii, sacrificiului, curajului și speranței.',
 't000005':'Introducere — Un tărâm ascuns și o misiune comună',
 't000006':'Introducerea așază noua aventură în Pământul de Mijloc, unde Inelul Unic reprezintă primejdia puterii corupătoare. Ea prezintă frăția ca pe o unire a unor neamuri diferite, ale căror puncte forte contează mai mult împreună decât separat. Tărâmurile ascunse înseamnă atât provocări necunoscute, cât și posibilități aflate chiar în călători. Disponibilitatea lui Bilbo de a privi dincolo de confortul familiar pornește mișcarea de la taină și nesiguranță spre apropiere și speranță.',
 't000007':'Citește introducerea în ediția integrală',
 't000008':'Taina Comitatului — Bilbo găsește o hartă',
 't000009':'În timp ce face ordine la Fundătura, Bilbo descoperă o hartă veche ascunsă printre lucruri uitate. Semnele ei sugerează existența unui tărâm ascuns și îi trezesc curiozitatea pe care viața așezată o adormise. Când Gandalf sosește cu vești despre un întuneric tot mai amenințător, Bilbo îi arată descoperirea. Cei doi cercetează harta, discută posibila ei legătură cu primejdia și înțeleg că Bilbo nu poate pleca singur. Capitolul transformă o descoperire domestică într-o obligație mai largă: Bilbo trebuie să părăsească siguranța, să caute aliați și să hotărască ce îi cere harta.',
 't000010':'Citește despre descoperirea lui Bilbo în ediția integrală',
 't000011':'Frăția — Puteri diferite, un singur scop',
 't000012':'Bilbo și Gandalf adună însoțitori pentru călătorie. Îi caută pe Aragorn, Legolas și Gimli, apoi îi aduc pe Frodo și Sam într-un grup ale cărui personaje au cunoștințe, priceperi și loialități diferite. Întâlnirile de pe drum transformă o enigmă personală într-o întreprindere comună. Harta le arată calea, dar capitolul pune accentul pe dialog, încredere și disponibilitatea de a înfrunta împreună primejdia. Plecarea din Comitat marchează trecerea de la planuri la fapte, în timp ce tărâmul ascuns rămâne necunoscut, iar legăturile dintre călători devin cea mai bună pregătire.',
 't000013':'Citește capitolul despre frăție în ediția integrală',
 't000014':'Încercări — Primejdia pune legăturile la probă',
 't000015':'Dincolo de Comitat, terenul accidentat, furtunile și creaturile amenințătoare încetinesc grupul. Un atacator întunecat legat de Inel îi silește să se apere unul pe altul, în loc să se bazeze pe priceperi separate. Îndrumarea lui Gandalf, stăpânirea de sine a lui Aragorn, atenția lui Legolas, hotărârea lui Gimli și stăruința hobbiților contează toate. Pe măsură ce se apropie de tărâmul ascuns, fiecare obstacol face mai real prețul misiunii. Capitolul înfățișează sacrificiul ca pe alegerea practică de a-ți apăra însoțitorii și a merge mai departe în ciuda fricii, nu doar ca pe un cuvânt eroic.',
 't000016':'Citește încercările în ediția integrală',
 't000017':'Revelație — Lumina împotriva umbrelor',
 't000018':'În tărâmul ascuns, un peisaj luminos conduce frăția la un piedestal străvechi. Slujitorii lui Sauron atacă, iar grupul trebuie să se apere în timp ce Bilbo urmează îndemnul lui Gandalf de a se concentra asupra luminii din sine. Puterea eliberată la piedestal îi alungă pe atacatori și dezvăluie cunoașterea legată de rostul tărâmului. Episodul prezintă cea mai puternică „cheie” ca fiind curajul și încrederea împărtășite de frăție. Chiar și după victorie, povestea arată limpede că o confruntare mai mare îi așteaptă.',
 't000019':'Citește revelația finală în ediția integrală',
 't000020':'Concluzie — Ce înseamnă cheile',
 't000021':'Concluzia se mută de la hărți și obiecte străvechi la relațiile care le permit călătorilor să acționeze împreună. Bilbo crește prin încredere, loialitate și pregătirea de a sta alături de ceilalți când înaintează întunericul. Tărâmul ascuns devine o metaforă pentru posibilitățile atinse prin curaj și legături umane. Frăția nu înlătură orice amenințare, dar pleacă având un scop mai limpede și o lumină pe care o poate purta mai departe. Cartea se încheie invitând cititorii să caute aceleași izvoare de reziliență în propria viață.',
 't000022':'Citește concluzia în ediția integrală',
}
d=json.loads(p.read_text())
for s in d['segments']:
 assert s['id'] in t
 assert not s['translation'] or s['translation']==t[s['id']]
 s['translation']=t[s['id']]
p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
