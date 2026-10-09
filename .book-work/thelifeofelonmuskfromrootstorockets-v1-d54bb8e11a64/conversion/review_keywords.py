import json
from pathlib import Path
p=Path('tools/keyword-translations.generated.json');c=json.loads(p.read_text())
langs=('fr','de','es','pt','it','ro','pl')
fix={
'spacex and reusable rockets':('SpaceX et fusées réutilisables','SpaceX und wiederverwendbare Raketen','SpaceX y cohetes reutilizables','SpaceX e foguetes reutilizáveis','SpaceX e razzi riutilizzabili','SpaceX și rachete reutilizabile','SpaceX i rakiety wielokrotnego użytku'),
'artificial-intelligence risks':('risques liés à l’intelligence artificielle','Risiken künstlicher Intelligenz','riesgos de la inteligencia artificial','riscos da inteligência artificial','rischi dell’intelligenza artificiale','riscurile inteligenței artificiale','zagrożenia związane ze sztuczną inteligencją'),
'driver-assistance software':('logiciel d’aide à la conduite','Fahrerassistenzsoftware','software de asistencia al conductor','software de assistência ao condutor','software di assistenza alla guida','software de asistență a șoferului','oprogramowanie wspomagające kierowcę'),
'self-sustaining settlement':('colonie autosuffisante','sich selbst erhaltende Siedlung','asentamiento autosuficiente','colónia autossustentável','insediamento autosufficiente','așezare autosuficientă','samowystarczalna osada'),
'self-sustaining settlement on Mars':('colonie autosuffisante sur Mars','sich selbst erhaltende Siedlung auf dem Mars','asentamiento autosuficiente en Marte','colónia autossustentável em Marte','insediamento autosufficiente su Marte','așezare autosuficientă pe Marte','samowystarczalna osada na Marsie'),
'larger starship program':('programme Starship de plus grande envergure','größeres Starship-Programm','programa Starship de mayor alcance','programa Starship de maior dimensão','programma Starship più ampio','programul Starship mai amplu','szerszy program Starship'),
'paypal transfer service':('service de transfert PayPal','PayPal-Überweisungsdienst','servicio de transferencias PayPal','serviço de transferências PayPal','servizio di trasferimento PayPal','serviciul de transfer PayPal','usługa przelewów PayPal'),
'determination and technological risk':('détermination et risque technologique','Entschlossenheit und technologisches Risiko','determinación y riesgo tecnológico','determinação e risco tecnológico','determinazione e rischio tecnologico','hotărâre și risc tehnologic','determinacja i ryzyko technologiczne'),
'greenhouse on mars':('serre sur Mars','Gewächshaus auf dem Mars','invernadero en Marte','estufa em Marte','serra su Marte','seră pe Marte','szklarnia na Marsie'),
'spacex and tesla':('SpaceX et Tesla','SpaceX und Tesla','SpaceX y Tesla','SpaceX e Tesla','SpaceX e Tesla','SpaceX și Tesla','SpaceX i Tesla'),
'access in underserved areas':('accès dans les zones mal desservies','Zugang in unterversorgten Gebieten','acceso en zonas desatendidas','acesso em áreas mal servidas','accesso in zone poco servite','acces în zone insuficient deservite','dostęp w słabo obsługiwanych regionach'),
'james bond film':('film de James Bond','James-Bond-Film','película de James Bond','filme de James Bond','film di James Bond','film James Bond','film o Jamesie Bondzie'),
'long-range goal':('objectif à long terme','langfristiges Ziel','objetivo a largo plazo','objetivo a longo prazo','obiettivo a lungo termine','obiectiv pe termen lung','cel długoterminowy'),
'underserved areas':('zones mal desservies','unterversorgte Gebiete','zonas desatendidas','áreas mal servidas','zone poco servite','zone insuficient deservite','słabo obsługiwane regiony'),
'small greenhouse':('petite serre','kleines Gewächshaus','invernadero pequeño','pequena estufa','piccola serra','seră mică','mała szklarnia'),
'spacecraft development':('développement de vaisseaux spatiaux','Entwicklung von Raumfahrzeugen','desarrollo de naves espaciales','desenvolvimento de naves espaciais','sviluppo di veicoli spaziali','dezvoltarea navelor spațiale','rozwój statków kosmicznych'),
'established manufacturers':('constructeurs établis','etablierte Hersteller','fabricantes establecidos','fabricantes estabelecidos','produttori affermati','producători consacrați','uznani producenci'),
'low-resistance tubes':('tubes à faible résistance de l’air','Röhren mit geringem Luftwiderstand','tubos de baja resistencia del aire','tubos de baixa resistência do ar','tubi a bassa resistenza dell’aria','tuburi cu rezistență redusă a aerului','tuby o małym oporze powietrza'),
'home energy storage':('stockage d’énergie domestique','Energiespeicherung zu Hause','almacenamiento doméstico de energía','armazenamento doméstico de energia','accumulo domestico di energia','stocarea energiei în locuințe','magazynowanie energii w domu'),
'major shareholder':('actionnaire principal','Hauptaktionär','accionista principal','acionista principal','azionista principale','acționar principal','główny akcjonariusz'),
}
for phrase,labels in fix.items():
 for lang,label in zip(langs,labels):
  assert phrase in c['translations'][lang],(phrase,lang)
  c['translations'][lang][phrase]=label
p.write_text(json.dumps(c,ensure_ascii=False,indent=2)+'\n')
print('corrected',len(fix),'phrases')
