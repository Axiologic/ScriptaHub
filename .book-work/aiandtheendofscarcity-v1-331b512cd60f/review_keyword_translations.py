import json
from pathlib import Path

p = Path('tools/keyword-translations.generated.json')
d = json.loads(p.read_text())
t = d['translations']
overrides = {
 'managing variable supply': {'ro':'gestionarea ofertei variabile','pl':'zarządzanie zmienną podażą'},
 'variable supply': {'ro':'ofertă variabilă','pl':'zmienna podaż'},
 'post-scarcity society': {'ro':'societate fără penurie','fr':'société post-pénurie','de':'Gesellschaft ohne Knappheit','es':'sociedad posterior a la escasez','pt':'sociedade pós-escassez','it':'società post-scarsità','pl':'społeczeństwo bez niedoboru'},
 'post-scarcity future': {'ro':'viitor fără penurie','fr':'avenir post-pénurie','de':'Zukunft ohne Knappheit','es':'futuro posterior a la escasez','pt':'futuro pós-escassez','it':'futuro post-scarsità','pl':'przyszłość bez niedoboru'},
 'circular production': {'pl':'produkcja w obiegu zamkniętym'},
 'concentration of power': {'ro':'concentrarea puterii','fr':'concentration du pouvoir','de':'Machtkonzentration','es':'concentración del poder','pt':'concentração de poder','it':'concentrazione del potere','pl':'koncentracja władzy'},
 'public governance': {'pl':'zarządzanie sprawami publicznymi'},
 'underserved communities': {'ro':'comunități insuficient deservite','it':'comunità scarsamente servite','pl':'społeczności o ograniczonym dostępie do usług'},
 'forecast maintenance': {'ro':'planificarea întreținerii','fr':'prévoir la maintenance','de':'Wartung prognostizieren','es':'prever el mantenimiento','pt':'prever a manutenção','it':'prevedere la manutenzione','pl':'planowanie konserwacji'},
 'trained on biased data': {'ro':'antrenate pe date părtinitoare','de':'auf voreingenommenen Daten trainiert','es':'entrenados con datos sesgados','pt':'treinados com dados enviesados','it':'addestrati su dati distorti','pl':'trenowane na stronniczych danych'},
 'anticipate failures': {'ro':'anticiparea defecțiunilor','pl':'przewidywanie awarii'},
 'goods for longer life': {'ro':'bunuri cu durată de viață mai lungă','pl':'towary o dłuższej trwałości'},
 'unfair decisions': {'ro':'decizii nedrepte','pl':'niesprawiedliwe decyzje'},
 'track products': {'ro':'urmărirea produselor','fr':'suivre les produits','de':'Produkte nachverfolgen','es':'rastrear productos','pt':'rastrear produtos','it':'tracciare i prodotti','pl':'śledzenie produktów'},
 'design goods': {'ro':'proiectarea bunurilor','fr':'concevoir des biens','de':'Güter entwerfen','es':'diseñar bienes','pt':'conceber bens','it':'progettare beni','pl':'projektowanie dóbr'},
 'retraining': {'ro':'recalificare profesională'},
 'practical infrastructure': {'ro':'infrastructură funcțională','pl':'infrastruktura operacyjna'},
 'adjust production schedules': {'ro':'ajustarea programelor de producție'},
 'production schedules': {'ro':'programe de producție'},
 'ethical governance': {'pl':'etyczne zarządzanie'},
 'broad automation': {'ro':'automatizare pe scară largă','pl':'automatyzacja na szeroką skalę'},
 'human oversight': {'pl':'nadzór człowieka'},
 'disaster response': {'pl':'reagowanie na katastrofy'},
 'economic scarcity': {'pl':'niedobór gospodarczy'},
 'fossil fuels': {'pl':'paliwa kopalne'},
 'biased data': {'ro':'date părtinitoare'},
 'reduced dependence': {'ro':'dependență redusă'},
 'inclusive design': {'pl':'projektowanie włączające'},
 'storage decisions': {'pl':'decyzje o magazynowaniu energii'},
 'public oversight': {'pl':'nadzór obywatelski'},
 'unlimited power': {'pl':'nieograniczona energia'},
 'shared benefit': {'ro':'beneficiu comun','pl':'wspólna korzyść'},
 'patterns in large datasets': {'ro':'tipare în seturi mari de date'},
 'food waste': {'ro':'risipa alimentară'},
}
for phrase, labels in overrides.items():
    for lang, label in labels.items():
        assert phrase in t[lang]
        t[lang][phrase] = label
p.write_text(json.dumps(d, ensure_ascii=False, indent=2, sort_keys=True) + '\n')
