import json
from pathlib import Path

path = Path(__file__).parent / 'chunks/0012.json'
data = json.loads(path.read_text())
translations = [
    "Deși apar noi vedete, Kylian Mbappé, Erling Haaland și alții, rivalitatea Messi–Ronaldo va rămâne un capitol de aur al istoriei fotbalului, despre care generațiile viitoare vor vorbi cu respect. Moștenirea lor va dăinui mult după retragere. Numele le vor intra în legenda fotbalului, iar recordurile stabilite vor fi repere pentru noul val de talent. Dar dincolo de trofee, goluri și recorduri, cel mai mare dar făcut fotbalului ar putea fi inspirația oferită milioanelor de oameni din întreaga lume. Au arătat că măreția nu ține numai de talent, ci și de muncă, hotărâre, modestie și disponibilitatea de a împinge limitele posibilului.",
    "În cele din urmă, fie că îl consideri pe Messi cel mai mare, fie că îi acorzi acest titlu lui Ronaldo, amândoi au lăsat o urmă de neșters asupra sportului, iar influența lor se va simți generații la rând. Sunt titanii fotbalului din vremea noastră și am avut norocul să le urmărim drumul extraordinar. Dezbaterea despre cine este mai bun s-ar putea să nu se încheie niciodată, dar un lucru e sigur: Messi și Ronaldo vor rămâne în istorie drept doi dintre cei mai mari jucători care au încântat vreodată lumea fotbalului.",
    "Bibliografie",
    "«Messi: The Inside Story of the Boy Who Became a Legend», de Luca Caioli – publicată în 2012.",
    "«Ronaldo: The Obsession for Perfection», de Leonardo Faccio – publicată în 2015.",
    "«Messi: The Biography», de Guillem Balagué – publicată în 2013.",
    "«Cristiano Ronaldo: The World’s Greatest», de Luca Caioli – publicată în 2016.",
]
assert len(data['segments']) == len(translations)
for segment, translation in zip(data['segments'], translations):
    segment['translation'] = translation
path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')
