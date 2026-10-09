#!/usr/bin/env python3
"""Direct Romanian translation of the stable ten-minute segments."""
import json
from pathlib import Path

path = Path(__file__).resolve().parent / "short/chunks/0001.json"
translations = {
"t000001": "Umbre și lumini: O poveste despre două orașe — Ediția de zece minute",
"t000002": "Umbre și lumini: O poveste despre două orașe",
"t000003": "Ediția de zece minute",
"t000004": "Această carte propune o interpretare ghidată a romanului lui Dickens",
"t000005": "Poveste despre două orașe",
"t000006": ", urmărind patru etape, de la contrastul dintre Londra și Paris până la alegerile făcute în timpul Terorii. Accentul cade pe renașterea de după întemnițare, pe presiunea schimbărilor politice asupra loialităților personale și pe posibilitatea sacrificiului. Cartea povestește desfășurări importante și finalul romanului lui Dickens; cititorii care vor să descopere singuri finalul pot începe cu succesiunea integrală a capitolelor.",
"t000007": "Capitolul întâi: două orașe și o întoarcere la viață",
"t000008": "Primul capitol așază povestea în contextul Revoluției Franceze. El contrastează stabilitatea relativă a Londrei cu Parisul, unde inegalitatea și furia cresc. Orașele sunt mai mult decât simple locuri: condițiile lor diferite arată cum istoria publică pătrunde în viețile familiilor. Pe acest fundal, bancherul Jarvis Lorry călătorește într-o misiune legată de doctorul Manette, care a fost ținut optsprezece ani în Bastilia.",
"t000009": "Descoperirea lui Lucie Manette că tatăl ei trăiește devine imaginea centrală a reînnoirii. Expresia „readus la viață” se referă atât la eliberarea lui, cât și la întoarcerea dificilă a unui om rănit în familie și în comunitate. Capitolul păstrează în vedere și cruzimea puterii aristocratice. Contrastul dintre asuprire și speranță pregătește întrebarea de mai târziu: își pot păstra oamenii compasiunea când ordinea socială se destramă în jurul lor?",
"t000010": "Capitolul al doilea: traumă, iubire și un trecut dezbinat",
"t000011": "Al doilea capitol examinează urmările închisorii asupra doctorului Manette. Cizmăria, mai întâi un mijloc de a rezista în detenție, rămâne un semn al ușurinței cu care revin amintirile și frica. Grija răbdătoare a lui Lucie deschide o cale spre recuperare, dar capitolul nu prezintă vindecarea drept instantanee. Charles Darnay intră apoi în poveste, iar relația lui cu Lucie leagă speranța personală de un trecut politic încă viu.",
"t000012": "Legăturile familiei lui Darnay cu aristocrația franceză creează tensiune în relație. Manette își dorește fericirea fiicei, însă amintirile violenței aristocratice îi complică reacția. Capitolul folosește aceste loialități întretăiate pentru a arăta că iubirea îi poate ajuta pe oameni să se refacă fără să șteargă suferința trecută. Speranța rămâne fragilă, fiindcă evenimentele din Franța se îndreaptă spre răsturnare.",
"t000013": "Capitolul al treilea: revoluția și presiunea ei morală",
"t000014": "Al treilea capitol se întoarce către forța tot mai mare a Revoluției. Asaltul Bastiliei dă o formă publică furiei produse îndelung de inegalitate, iar relatarea arată și cum răzbunarea devine periculoasă prin ea însăși. Madame Defarge întruchipează o cerere neînduplecată de pedeapsă. Întoarcerea lui Darnay în Franța îl expune riscurilor legate de numele familiei, iar Lucie și doctorul Manette înfruntă urmările alături de el.",
"t000015": "Capitolul îl urmărește și pe Sydney Carton, a cărui dragoste pentru Lucie și nemulțumire față de sine dau conflictului larg o urgență personală. Spionii și oportuniștii profită de epoca nesigură, iar încrederea devine mai greu de păstrat. Cartea citește aceste fire împreună: un protest îndreptățit împotriva asupririi poate crea noi victime când frica și răzbunarea înving judecata.",
"t000016": "Capitolul al patrulea: ghilotina și un sacrificiu ales",
"t000017": "Ultimul capitol intră în timpul Terorii, când întemnițarea și procesul lui Darnay îi pun familia în primejdie imediată. Trecutul doctorului Manette revine cu o forță dureroasă. Cartea se concentrează asupra hotărârii lui Carton de a acționa pentru Lucie și Darnay. Planul de a-i lua locul lui Darnay transformă sentimentul unei vieți irosite într-un gest concret de loialitate.",
"t000018": "Moartea lui Carton nu este prezentată ca anulând violența Revoluției. Dimpotrivă, ea face vizibil prețul fugii unei familii și oferă narațiunii cel mai puternic exemplu de izbăvire personală. Cartea urmărește și plecarea tensionată a familiei din Paris și recunoaște că supraviețuirea poartă cu sine durere. Nedreptatea publică, curajul personal și iubirea se întâlnesc în acest final fără să devină același lucru.",
"t000019": "Perspectiva finală a cărții",
"t000020": "Concluzia substanțială revine la relatarea lui Dickens despre dreptate, schimbare socială și compasiune. Cartea invită cititorii să se gândească la felul în care violența istoriei pune la încercare valorile afirmate de oameni. Structura ei distinctă merge de la două orașe și întoarcerea unui prizonier, prin legăturile familiei și frica revoluționară, până la alegerea lui Carton. Interpretarea rezultată este o lectură a romanului lui Dickens, nu un capitol suplimentar al romanului.",
"t000021": "Citește pasajele corespunzătoare din ediția integrală",
"t000022": "Capitolul întâi: Londra, Parisul și întoarcerea doctorului Manette",
"t000023": "Capitolul al doilea: trauma și familia Manette",
"t000024": "Capitolul al treilea: presiunea Revoluției",
"t000025": "Capitolul al patrulea: alegerea lui Carton",
"t000026": "Concluzie",
"t000027": "Bibliografie",
}
chunk = json.loads(path.read_text(encoding="utf-8"))
for segment in chunk["segments"]:
    segment["translation"] = translations[segment["id"]]
path.write_text(json.dumps(chunk, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(len(translations), "short-reader segments translated")
