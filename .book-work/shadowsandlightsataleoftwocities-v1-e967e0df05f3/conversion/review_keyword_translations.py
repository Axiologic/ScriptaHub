#!/usr/bin/env python3
"""Repair misleading local-model labels in this book's discovery vocabulary."""
import json
from pathlib import Path

p = Path("tools/keyword-translations.generated.json")
data = json.loads(p.read_text(encoding="utf-8"))
cache = data["translations"]
fixes = {
"Reign of Terror": {"ro": "Domnia Terorii", "fr": "Terreur révolutionnaire", "es": "Reinado del Terror", "it": "Regno del Terrore"},
"Bastille": {"ro": "Bastilia"},
"family bonds": {"ro": "legături familiale", "fr": "attaches familiales", "es": "vínculos familiares", "pt": "vínculos familiares", "it": "vincoli familiari", "pl": "więzi bliskich"},
"private loyalties": {"ro": "loialități personale", "fr": "loyautés personnelles", "de": "persönliche Loyalitäten", "es": "lealtades personales", "pt": "lealdades pessoais", "it": "lealtà personali", "pl": "lojalności osobiste"},
"personal redemption": {"ro": "izbăvire personală", "de": "persönliche Erlösung", "fr": "rédemption personnelle"},
"divided past": {"ro": "trecut dezbinat", "es": "pasado dividido", "pt": "passado dividido"},
"demand for retribution": {"ro": "cerere de pedeapsă", "de": "Forderung nach Vergeltung", "es": "exigencia de castigo", "pt": "exigência de punição", "it": "richiesta di vendetta punitiva", "pl": "żądanie odwetu"},
"account of justice": {"ro": "perspectivă asupra dreptății", "de": "Darstellung der Gerechtigkeit", "fr": "réflexion sur la justice", "es": "visión de la justicia", "pt": "visão da justiça", "it": "visione della giustizia", "pl": "obraz sprawiedliwości"},
"cruelty of aristocratic power": {"ro": "cruzimea puterii aristocratice", "es": "crueldad del poder aristocrático", "pt": "crueldade do poder aristocrático", "pl": "okrucieństwo władzy arystokratycznej"},
"strain of political upheaval": {"ro": "presiunea tulburărilor politice", "es": "presión de la agitación política", "pt": "pressão da convulsão política", "it": "pressione dei rivolgimenti politici", "pl": "presja wstrząsów politycznych"},
"family in immediate danger": {"ro": "familie în primejdie imediată"},
"guided interpretation": {"pl": "interpretacja z przewodnikiem"},
"difficult return": {"ro": "întoarcere dificilă", "pl": "trudny powrót"},
"unsettled period": {"ro": "perioadă tulbure", "de": "unruhige Zeit", "es": "época turbulenta", "pt": "período conturbado", "it": "periodo turbolento", "pl": "niespokojny okres"},
"private urgency": {"ro": "urgență personală", "de": "persönliche Dringlichkeit", "fr": "urgence personnelle", "es": "urgencia personal", "pt": "urgência pessoal", "it": "urgenza personale", "pl": "osobista pilność"},
"damaged person": {"ro": "persoană rănită", "de": "verletzter Mensch", "fr": "personne meurtrie", "es": "persona herida", "pt": "pessoa ferida", "it": "persona ferita", "pl": "zraniona osoba"},
"trial": {"fr": "procès", "de": "Gerichtsprozess", "pt": "julgamento", "it": "processo giudiziario", "pl": "proces sądowy"},
"imprisonment": {"de": "Inhaftierung", "es": "encarcelamiento", "pl": "uwięzienie"},
"personal hope": {"pl": "osobista nadzieja"},
"return to France": {"ro": "întoarcere în Franța"},
"family's escape": {"ro": "fuga familiei", "pl": "ucieczka rodziny"},
"means of endurance": {"ro": "mijloc de a rezista", "de": "Mittel zum Durchhalten", "fr": "moyen de tenir bon", "es": "medio para resistir", "pt": "meio de resistir", "it": "mezzo per resistere", "pl": "sposób przetrwania"},
"revolutionary fear": {"ro": "frica din timpul revoluției", "pl": "strach czasu rewolucji"},
"banker Jarvis Lorry": {"pt": "banqueiro Jarvis Lorry"},
"Lucie Manette": {"pl": "Lucie Manette"},
"Sydney Carton": {"ro": "Sydney Carton", "fr": "Sydney Carton", "es": "Sydney Carton", "pt": "Sydney Carton", "it": "Sydney Carton"},
"Madame Defarge": {"ro": "Madame Defarge", "es": "Madame Defarge", "pt": "Madame Defarge", "it": "Madame Defarge"},
"return to life": {"ro": "întoarcere la viață"},
"recalled to life": {"ro": "readus la viață", "es": "devuelto a la vida", "pt": "trazido de volta à vida", "it": "richiamato alla vita", "pl": "przywrócony do życia"},
"renewal": {"de": "Erneuerung", "it": "rinascita"},
"trauma": {"ro": "traumă", "fr": "traumatisme psychique", "es": "trauma", "pt": "trauma", "pl": "trauma"},
"shoemaking": {"ro": "cizmărie", "fr": "cordonnerie", "es": "zapatería", "pt": "ofício de sapateiro", "it": "calzoleria", "pl": "szewstwo"},
"patient care": {"ro": "grija răbdătoare", "de": "geduldige Fürsorge", "fr": "soins attentifs", "es": "atención paciente", "pt": "cuidado paciente", "it": "cure premurose", "pl": "cierpliwa opieka"},
"recovery": {"de": "Genesung", "pl": "powrót do zdrowia"},
"political past": {"pl": "przeszłość polityczna"},
"intersecting loyalties": {"ro": "loialități întretăiate", "de": "sich überschneidende Loyalitäten", "fr": "loyautés croisées", "es": "lealtades cruzadas", "pt": "lealdades cruzadas", "it": "lealtà intrecciate", "pl": "krzyżujące się lojalności"},
"storming of the Bastille": {"ro": "asaltul Bastiliei", "fr": "prise de la Bastille", "es": "toma de la Bastilla", "pt": "tomada da Bastilha", "it": "presa della Bastiglia", "pl": "szturm Bastylii"},
"retribution": {"ro": "pedeapsă", "it": "punizione"},
"imprisonment and trial": {"ro": "întemnițare și proces", "de": "Haft und Gerichtsverfahren", "pl": "uwięzienie i proces"},
"chosen sacrifice": {"de": "bewusst gewähltes Opfer", "pl": "świadome poświęcenie"},
"guillotine": {"de": "Guillotine"},
}
for phrase, localized in fixes.items():
    for lang, label in localized.items():
        assert phrase in cache[lang], (phrase, lang)
        cache[lang][phrase] = label
p.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(sum(map(len, fixes.values())), "labels corrected")
