import json
from pathlib import Path

path = Path(__file__).parent / 'chunks/0009.json'
data = json.loads(path.read_text())
translations = [
    "«Revolta – Partea a II-a» (2015). Katniss se alătură unei echipe de rebeli care urmărește să-l elimine pe președintele Snow și să aducă libertatea în Panem. Pe drum, se confruntă cu trădări și sacrificii dureroase. În cele din urmă, după cucerirea Capitoliului, înțelege că președinta Coin are propriile ambiții răuvoitoare. Seria oferă nu doar o poveste captivantă despre supraviețuire și curaj, ci abordează și teme adânci despre putere, opresiune și sacrificiu.",
    "Concluzie",
    "Universul «Jocurilor foamei» oferă o reflecție profundă asupra dinamicii puterii, opresiunii și sacrificiului, arătând cum un sistem totalitar poate manipula frica și controlul pentru a supune mulțimile. Povestea lui Katniss Everdeen nu privește doar supraviețuirea fizică, ci și reziliența emoțională și morală în fața unei realități aspre, în care sacrificiile personale devin cheia schimbării. În cele din urmă, «Jocurile foamei» ne amintesc că, și în cele mai întunecate clipe ale tiraniei și disperării, speranța dăinuie, iar spiritul uman are puterea de a lupta pentru libertate și dreptate.",
    "Bibliografie",
    "Collins, Suzanne. The Hunger Games (2008).",
    "Collins, Suzanne. Catching Fire (2009).",
    "Collins, Suzanne. Mockingjay (2010).",
]
assert len(data['segments']) == len(translations)
for segment, translation in zip(data['segments'], translations):
    segment['translation'] = translation
path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')
