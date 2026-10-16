"""Human review of Romanian metadata after local draft translation."""

import glob
import json
from pathlib import Path

RO = {
    "dracula": [
        "Jonathan Harker călătorește în Transilvania și descoperă secretul înfricoșător al gazdei sale.",
        "Contele Dracula duce apoi primejdia în Anglia.",
        "Boala lui Lucy Westenra îi atrage prietenii într-o luptă pe care abia încep să o înțeleagă.",
        "Mina Harker adună jurnale și scrisori pentru a lega indiciile.",
        "Urmărirea trece granițele, iar grupul încearcă să zădărnicească planurile contelui.",
        "Bram Stoker spune povestea prin însemnările personajelor, astfel încât fiecare descoperire pare imediată.",
    ],
    "grimmsfairytales": [
        "Frații Grimm adună povești despre păduri, căsuțe, regi și copii rătăciți.",
        "Promisiunile și înțelegerile au adesea un preț pe care personajele nu îl prevăd.",
        "Vrăjitoarele, animalele și obiectele fermecate transformă alegerile obișnuite în încercări.",
        "Curajul și istețimea îi ajută pe unii călători să scape de primejdie.",
        "Alte povești lasă un avertisment mai întunecat despre cruzime sau lăcomie.",
        "Culegerea păstrează ritmurile variate și tensiunile morale ale basmelor populare europene.",
    ],
    "mobydickorthewhale": [
        "Ishmael se îmbarcă pe Pequod pentru a munci și a cunoaște lumea vânătorilor de balene.",
        "Căpitanul Ahab face din urmărirea balenei albe adevăratul scop al vasului.",
        "Echipajul îl urmează peste oceane, în timp ce semnele de avertizare se înmulțesc.",
        "Descrierile balenelor și ale muncii la bord întrerup și adâncesc povestea călătoriei.",
        "Obsesia lui Ahab pune la încercare loialitatea, judecata și limitele controlului omenesc.",
        "Herman Melville îmbină aventura, cercetarea și tragedia într-un amplu roman al mării.",
    ],
    "olivertwist": [
        "Oliver crește într-un azil de săraci unde copiii sunt tratați cu cruzime.",
        "Fuga lui la Londra îl aduce în cercul de hoți al lui Fagin.",
        "Bunătatea coexistă cu exploatarea, în timp ce adulții încearcă să îi decidă viitorul.",
        "Alegerile lui Nancy arată cât de primejdios este să încerci să îl protejezi.",
        "Misterul familiei lui Oliver se dezvăluie printre urmăriri și trădări.",
        "Charles Dickens transformă povestea unui copil într-un portret incisiv al sărăciei și nedreptății sociale.",
    ],
    "thelifeandadventuresofrobinsoncrusoe": [
        "Robinson Crusoe ignoră sfatul tatălui și pleacă pe mare.",
        "Un naufragiu îl lasă singur pe o insulă timp de mulți ani.",
        "Își construiește un adăpost, cultivă hrană și ține un jurnal al supraviețuirii.",
        "Urmele altor oameni îi schimbă sentimentul de siguranță și singurătate.",
        "Întâlnirea cu Vineri aduce tovărășie și întrebări dificile despre putere.",
        "Aventura lui Daniel Defoe îmbină ingeniozitatea practică, teama, credința și presupunerile coloniale.",
    ],
}

for key, sentences in RO.items():
    path = Path(glob.glob(f".book-work/{key}-v1-*")[0]) / "book" / "manifest.json"
    data = json.loads(path.read_text())
    data["shortDescription"]["ro"] = " ".join(sentences)
    data["aboutBook"]["ro"] = [" ".join(sentences[:3]), " ".join(sentences[3:])]
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n")
