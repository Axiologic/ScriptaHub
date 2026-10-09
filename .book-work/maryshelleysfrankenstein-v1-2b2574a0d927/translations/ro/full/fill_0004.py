import json
from pathlib import Path

path = Path(__file__).parent / 'chunks/0004.json'
data = json.loads(path.read_text())
translations = [
    "De aici, lucrurile merg din rău în mai rău: Justine Moritz, o tânără care lucrează pentru familia Frankenstein, este acuzată de crimă. Dovada? Asupra ei este găsit un medalion care îi aparținea lui William. Se pare că, într-o întorsătură crudă a sorții, creatura l-a pus acolo. Deși își susține nevinovăția, Justine este arestată și trimisă în judecată.",
    "Victor, chinuit de adevărul pe care îl știe, nu se poate hotărî dacă să vorbească. Pe de o parte, știe că Justine este nevinovată și că tăcerea lui poate duce la executarea ei pe nedrept. Pe de altă parte, se îngrozește de urmările dezvăluirii existenței creaturii. În timp ce se luptă cu propria conștiință, povara vinei devine tot mai grea cu fiecare zi.",
    "La proces, Justine își menține nevinovăția, dar dovezile par să fie împotriva ei. Victor stă tăcut în sala de judecată și privește cum o femeie nevinovată este condamnată pentru o faptă pe care nu a comis-o, știind că el este răspunzător de existența adevăratului ucigaș. Vina îl roade, dar nu spune nimic. Justine este condamnată la moarte, iar tăcerea lui Victor îi pecetluiește soarta.",
    "Execuția lui Justine este lovitura finală pentru starea mintală deja șubredă a lui Victor. Îl mistuie vina, rușinea și disperarea, știind că doi oameni pe care îi iubea, fratele lui și o femeie nevinovată, au murit din pricina faptelor sale. Povara responsabilității devine de nesuportat, iar el se afundă din nou într-o depresie adâncă.",
    "Acum ai crede că Victor se va hotărî în sfârșit să-și asume răspunderea pentru ființa creată. Poate că ar căuta-o, ar vorbi deschis cu ea și, știi tu, ar opri-o să mai ucidă oameni. Dar Victor alege alt drum: fuge iar de probleme. De data aceasta pleacă spre Alpii elvețieni, sperând că o drumeție frumoasă îi va limpezi gândurile. Nimic nu spune «rezolvare de probleme» mai bine decât fuga în munți, când ai lăsat liberă o creatură ucigașă pe care chiar tu ai făcut-o.",
    "Frumusețea Alpilor îi oferă lui Victor o scurtă evadare. Urcă în munți, printre vârfuri înzăpezite și aer proaspăt, și simte pentru o clipă pace. Liniștea nu durează. Într-o scenă ce ar putea fi numită «Frankenstein la drumeție extremă», Victor întâlnește creatura pe un ghețar. Vederea ei îi trezește din nou toată vina și teama, dar de data aceasta nu îl atacă. În schimb, vorbește.",
    "Este un moment hotărâtor, în care creatura își spune propria versiune. Abandonată la naștere, dezorientată și respinsă de toți cei pe care îi întâlnește, a rătăcit prin sălbăticie, învățând despre lume și devenind pe zi ce trece mai amară. Îi povestește lui Victor despre mizeria și singurătatea îndurate, despre încercările de a se împrieteni cu oamenii, întâmpinate mereu cu frică și violență. Izolarea și durerea au împins-o spre întuneric, iar pentru suferința ei îl învinuiește pe Victor.",
    "Dar, în loc să ceară răzbunare, creatura face o rugăminte. Îi spune lui Victor că își dorește doar tovărășie: pe cineva asemenea ei, care să nu o respingă și să nu se teamă. Îi cere să creeze o însoțitoare și promite că, dacă îi îndeplinește dorința, cele două ființe vor dispărea în sălbăticie și vor trăi în pace, departe de oameni.",
    "Victor, încă zguduit de moartea lui William și Justine, refuză la început. Povestea suferinței creaturii îl atinge însă. Începe să simtă o responsabilitate tulburătoare, nu numai pentru faptele ei, ci și pentru singurătatea ei. La urma urmei, chiar el a creat această ființă și apoi a abandonat-o. Poate că așa ar putea îndrepta lucrurile.",
    "Astfel, într-una dintre cele mai discutabile hotărâri ale vieții sale, și au fost destule, Victor acceptă cererea. Promite să-i creeze o însoțitoare, crezând că astfel se va sfârși, în fine, coșmarul pe care îl trăiește.",
]
assert len(data['segments']) == len(translations)
for segment, translation in zip(data['segments'], translations):
    segment['translation'] = translation
path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')
