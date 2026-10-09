import json
from pathlib import Path

root = Path(__file__).resolve().parent / 'translations/ro/short/chunks'
translations = {
    't000001': 'O nouă eră a finanțelor: standardul Bitcoin — Ediția de zece minute',
    't000002': 'O nouă eră a finanțelor: standardul Bitcoin',
    't000003': 'Această carte abordează Bitcoin prin istoria banilor. Pornește de la troc și bunurile folosite în primele schimburi, trece prin metalele monetare și moneda fiduciară și ajunge la tranzacțiile digitale descentralizate. Argumentul central este că raritatea și independența față de emiterea guvernamentală ar putea face din Bitcoin un alt fel de bani. Secțiunile următoare sintetizează acest argument așa cum este prezentat în carte.',
    't000004': 'Metamorfoza banilor — De ce schimburile au nevoie de un mijloc comun',
    't000005': 'Trocul cere ca fiecare comerciant să își dorească exact ceea ce oferă celălalt. Pe măsură ce comunitățile cresc, această dublă coincidență a nevoilor blochează schimburile și limitează comerțul. De aceea, societățile timpurii au folosit bunuri intermediare, inclusiv scoici, mărgele și animale. Cartea urmărește trecerea către aur și argint, deoarece aceste metale sunt durabile, divizibile, portabile și relativ rare. Aurul a devenit și rezervă de valoare, și bază a creditului. Exemplele introduc criteriile cărții pentru bani: oamenii trebuie să îi recunoască, să aibă încredere în ei și să îi poată transporta, împărți și economisi.',
    't000006': 'Capitolul compară apoi sistemele susținute de metale cu monedele fiduciare emise de guverne. Susține că o ofertă monetară extinsă prin decizii politice poate eroda puterea de cumpărare. Bitcoin intră în comparație cu o ofertă maximă fixă de 21 de milioane de unități și o rețea care nu cere autorizarea fiecărei tranzacții de către o bancă. Cartea prezintă aceste trăsături drept posibile protecții împotriva inflației și dependenței de intermediari, întrebând dacă Bitcoin poate îndeplini rolul atribuit cândva aurului.',
    't000007': 'Citește capitolul I în ediția completă',
    't000008': 'Istoria neobișnuită a banilor — Moneda depinde de încredere',
    't000009': 'Privind mai atent primele forme de bani, capitolul al doilea arată că oamenii alegeau obiecte pentru schimb din motive practice și sociale. Scoicile cauri, mărgelele și animalele erau utile în anumite contexte, dar producția, transportul sau disponibilitatea lor le limitau pe măsură ce comerțul creștea. Cartea descrie și practici de ținere a evidențelor în societăți care nu foloseau monede în sensul familiar. Aceste cazuri complică ideea că banii sunt doar obiecte materiale: contabilitatea, recunoașterea comună și încrederea fac schimburile posibile.',
    't000010': 'Capitolul revine la aur și argint ca mijloace de schimb mai rafinate și întreabă ce ne învață formele mai vechi despre banii digitali. Comparația subliniază raritatea, acceptarea și încrederea într-un sistem. Propune Bitcoin ca răspuns la presupusele slăbiciuni ale banilor centralizați, însă cazurile istorice sugerează și un test: proiectarea tehnică a unei monede nu poate crea singură încrederea socială de care depinde folosirea ei.',
    't000011': 'Citește capitolul II în ediția completă',
    't000012': 'Metalele prețioase — Atracția valorii tangibile',
    't000013': 'Capitolul al treilea urmărește aurul și argintul prin rolurile lor monetare și culturale. Durabilitatea fizică și aspectul ușor de recunoscut au ajutat oamenii să le folosească perioade îndelungate și în comunități comerciale diferite. Aurul a ajuns asociat cu tranzacțiile mari, rezervele și etalonul-aur din secolul al XIX-lea. Argintul, mai abundent, a servit și schimburilor cotidiene. Cartea prezintă moneda susținută de metale ca mod de a lega creanțele monetare de un activ care nu poate fi produs pur și simplu prin decret.',
    't000014': 'Capitolul analizează și motivele pentru care oamenii revin la metale în vremuri de incertitudine. Pentru autor, această preferință exprimă dorința de a păstra valoarea și de a deține ceva tangibil când încrederea în instituții slăbește. Comparația pregătește discuția ulterioară despre Bitcoin: deși unul este fizic, iar celălalt digital, cartea susține că limitele ofertei contează pentru amândouă. Cititorii sunt invitați să judece ce proprietăți ale banilor din trecut rămân utile într-o economie digitală.',
    't000015': 'Citește capitolul III în ediția completă',
    't000016': 'Moneda fiduciară — Cine controlează oferta?',
    't000017': 'Ultimul capitol analizează monedele a căror valoare se sprijină pe încrederea publicului în instituțiile guvernamentale, nu pe dreptul la o marfă fizică. Cartea leagă îndepărtarea de sistemele susținute de aur de nevoile de finanțare ale statelor, mai ales în timp de război. Susține că extinderea ofertei monetare poate crește prețurile și slăbi economiile și că politica monetară poate afecta autonomia financiară individuală. Preocuparea ei nu privește doar materialul din care sunt făcuți banii, ci și cine le poate schimba oferta și sub ce constrângeri.',
    't000018': 'Bitcoin este prezentat ca alternativă cu o ofertă prestabilită și reguli descentralizate pentru tranzacții. Concluzia leagă acest argument de istoria anterioară a trocului, metalelor și banilor fiduciari. Îi invită pe cititori să analizeze dacă un sistem digital poate combina calitățile utile ale formelor mai vechi de bani cu accesul la schimburile globale. Cartea își leagă argumentul pentru Bitcoin de temele recurente ale proiectării monetare, rarității și încrederii.',
    't000019': 'Citește capitolul IV în ediția completă',
}
for path in sorted(root.glob('*.json')):
    data = json.loads(path.read_text())
    for segment in data['segments']:
        segment['translation'] = translations[segment['id']]
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')
