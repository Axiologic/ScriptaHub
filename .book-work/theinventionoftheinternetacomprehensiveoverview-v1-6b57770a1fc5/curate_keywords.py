import json
from pathlib import Path

path = Path('tools/keyword-translations.generated.json')
cache = json.loads(path.read_text())
fix = {
 'global medium': {'fr':'média mondial','pt':'meio global','pl':'globalne medium'},
 'engineering': {'de':'Ingenieurwesen'},
 'typewriters': {'pl':'maszyny do pisania'},
 'scheduled television': {'ro':'televiziune cu program fix','pl':'telewizja o stałej ramówce','it':'televisione a orari prestabiliti'},
 'search': {'de':'Suche','es':'búsqueda','it':'ricerca','ro':'căutare','pl':'wyszukiwanie'},
 'messaging': {'ro':'mesagerie','pl':'komunikatory'},
 'constant alerts': {'pl':'ciągłe powiadomienia'},
 'distant collaboration': {'ro':'colaborare la distanță','pl':'współpraca na odległość','de':'Zusammenarbeit über Distanz'},
 'Sputnik': {'pl':'Sputnik'},
 'J. C. R. Licklider': {'pl':'J. C. R. Licklider'},
 'packet switching': {'ro':'comutarea pachetelor','pl':'komutacja pakietów'},
 'LOGIN': {'fr':'LOGIN','es':'LOGIN','pt':'LOGIN','ro':'LOGIN'},
 'Vint Cerf': {'fr':'Vint Cerf','de':'Vint Cerf','es':'Vint Cerf','pt':'Vint Cerf','it':'Vint Cerf','ro':'Vint Cerf','pl':'Vint Cerf'},
 'network of networks': {'de':'Netz der Netze'},
 'shared computing': {'ro':'utilizarea comună a calculatoarelor','pl':'współdzielone zasoby obliczeniowe'},
 'hardware': {'ro':'echipamente informatice'},
 'Bolt Beranek and Newman': {'fr':'Bolt Beranek and Newman','de':'Bolt Beranek and Newman','es':'Bolt Beranek and Newman','pt':'Bolt Beranek and Newman','it':'Bolt Beranek and Newman','ro':'Bolt Beranek and Newman','pl':'Bolt Beranek and Newman'},
 'Interface Message Processors': {'fr':'Interface Message Processors','de':'Interface Message Processors','es':'Interface Message Processors','pt':'Interface Message Processors','it':'Interface Message Processors','ro':'Interface Message Processors','pl':'Interface Message Processors'},
 'packet-routing machines': {'ro':'mașini de rutare a pachetelor','pl':'urządzenia kierujące pakietami'},
 'Stanford Research Institute': {'fr':'Stanford Research Institute','de':'Stanford Research Institute','es':'Stanford Research Institute','pt':'Stanford Research Institute','it':'Stanford Research Institute','ro':'Stanford Research Institute','pl':'Stanford Research Institute'},
 'Email': {'de':'E-Mail','pl':'poczta elektroniczna'},
 'file transfer': {'ro':'transfer de fișiere'},
 'resource sharing': {'ro':'partajarea resurselor','pl':'współdzielenie zasobów'},
 'UNIX-based computing': {'ro':'sisteme informatice bazate pe UNIX','pl':'systemy komputerowe oparte na UNIX'},
 'scalable': {'ro':'scalabil','pl':'skalowalny'},
 'interoperable protocols': {'pt':'protocolos interoperáveis','it':'protocolli interoperabili','pl':'protokoły interoperacyjne'},
 'reliable packet transmission': {'ro':'transmiterea fiabilă a pachetelor'},
 'academic backbone': {'ro':'rețea academică principală','pl':'akademicka sieć szkieletowa','de':'akademisches Kernnetz'},
 'telemedicine': {'pl':'telemedycyna'},
 'net neutrality': {'pl':'neutralność sieci'},
 'ARPANET': {'pt':'ARPANET'},
 'TCP/IP': {'pt':'TCP/IP'},
}
for phrase, labels in fix.items():
    for lang, label in labels.items():
        assert phrase in cache['translations'][lang], (phrase, lang)
        cache['translations'][lang][phrase] = label
path.write_text(json.dumps(cache, ensure_ascii=False, indent=2) + '\n')
print('Curated', sum(map(len, fix.values())), 'labels')
