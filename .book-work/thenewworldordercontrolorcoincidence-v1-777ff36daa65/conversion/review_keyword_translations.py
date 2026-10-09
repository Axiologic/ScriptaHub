#!/usr/bin/env python3
"""Repair local-model mistranslations of this essay's discovery terms."""
import json
from pathlib import Path
p=Path('tools/keyword-translations.generated.json');d=json.loads(p.read_text())
fix={
'Illuminati':{'de':'Illuminati','es':'Illuminati','pt':'Illuminati','it':'Illuminati','ro':'Illuminati','pl':'Illuminati'},
'historical Bavarian Illuminati':{'es':'Illuminati bávaros históricos','it':'Illuminati bavaresi storici','ro':'Illuminati bavarezi istorici','pl':'historyczni Illuminaci bawarscy'},
'historical Illuminati':{'es':'Illuminati históricos','it':'Illuminati storici','ro':'Illuminati istorici','pl':'historyczni Illuminaci'},
'Bavarian society':{'pl':'bawarskie stowarzyszenie'},
'Enlightenment ideals':{'fr':'idéaux des Lumières','es':'ideales de la Ilustración','pt':'ideais do Iluminismo','it':'ideali illuministi','ro':'idealuri iluministe'},
'secret-society theories':{'fr':'théories sur les sociétés secrètes','de':'Theorien über Geheimgesellschaften','es':'teorías sobre sociedades secretas','pt':'teorias sobre sociedades secretas','it':'teorie sulle società segrete','ro':'teorii despre societăți secrete','pl':'teorie o tajnych stowarzyszeniach'},
'modern claims':{'fr':'affirmations modernes','de':'moderne Behauptungen','es':'afirmaciones modernas','pt':'alegações modernas','it':'affermazioni moderne','ro':'afirmații moderne','pl':'współczesne twierdzenia'},
'conspiracy theorists':{'ro':'adepți ai teoriilor conspirației'},
'New World Order':{'fr':'Nouvel ordre mondial','ro':'Noua ordine mondială'},
'New World Order theory':{'fr':'théorie du nouvel ordre mondial','ro':'teoria noii ordini mondiale','pl':'teoria nowego porządku świata'},
'hidden power':{'fr':'pouvoir caché','it':'potere nascosto','pl':'ukryta władza'},
'central direction':{'de':'zentrale Steuerung','es':'dirección centralizada','pt':'direção centralizada','it':'direzione centralizzata','ro':'conducere centrală','pl':'centralne kierownictwo'},
'COVID-19 pandemic':{'de':'COVID-19-Pandemie','ro':'pandemia de COVID-19'},
'lockdowns':{'fr':'confinements','de':'Lockdowns','es':'confinamientos','pt':'confinamentos','it':'confinamenti','ro':'carantine','pl':'lockdowny'},
'emergency measures':{'fr':"mesures d'urgence"},
'public-health purpose':{'fr':'objectif de santé publique','de':'Zweck des Gesundheitsschutzes','es':'objetivo de salud pública','pt':'objetivo de saúde pública','it':'scopo di sanità pubblica','ro':'scop de sănătate publică','pl':'cel ochrony zdrowia publicznego'},
'health response':{'de':'Gesundheitsmaßnahme','pt':'resposta sanitária','ro':'răspuns sanitar','pl':'reakcja zdrowotna'},
'public health':{'de':'öffentliche Gesundheit'},
'viral spread':{'it':'diffusione del virus','ro':'răspândirea virusului'},
'curfews':{'pt':'recolher obrigatório','ro':'interdicții de circulație','pl':'godziny policyjne'},
'online work':{'ro':'muncă online'},
'digital contact tracing':{'es':'rastreo digital de contactos','pt':'rastreio digital de contactos','ro':'urmărirea digitală a contactelor'},
'vaccine passports':{'de':'Impfpässe','es':'pasaportes de vacunación','pt':'certificados de vacinação','ro':'pașapoarte de vaccinare','pl':'paszporty szczepionkowe'},
'vaccine-passport proposals':{'fr':'propositions de passeports vaccinaux','de':'Vorschläge für Impfpässe','es':'propuestas de pasaportes de vacunación','pt':'propostas de certificados de vacinação','it':'proposte di passaporti vaccinali','ro':'propuneri de pașapoarte de vaccinare','pl':'propozycje paszportów szczepionkowych'},
'social life':{'de':'soziales Leben'},
'physical movement':{'de':'physische Fortbewegung','ro':'deplasare fizică'},
'mass compliance':{'fr':'obéissance de masse','de':'massenhafte Befolgung','es':'obediencia masiva','pt':'obediência em massa','it':'obbedienza di massa','ro':'supunerea maselor','pl':'masowe podporządkowanie'},
'lasting control':{'pt':'controlo duradouro'},
'emergency surveillance':{'pl':'nadzór w sytuacjach nadzwyczajnych'},
'emergency controls':{'pl':'środki kontroli w sytuacjach nadzwyczajnych'},
'media messages':{'it':'messaggi dei media','pl':'przekazy medialne'},
'repeated media messages':{'it':'powtarzane messaggi dei media','pl':'powtarzane przekazy medialne'},
'news coverage':{'fr':'couverture médiatique','ro':'relacje de presă','pl':'relacje informacyjne'},
'media narratives':{'es':'narrativas mediáticas','ro':'narațiuni media'},
'news outlets':{'de':'Nachrichtenmedien','it':'testate giornalistiche','ro':'instituții de presă','pl':'redakcje informacyjne'},
'dystopian futures':{'fr':'avenirs dystopiques','de':'dystopische Zukunftsbilder','it':'futuri distopici','ro':'viitoruri distopice','pl':'dystopijne wizje przyszłości'},
'popular culture':{'de':'Popkultur'},
'concentrated power':{'fr':'pouvoir concentré','de':'konzentrierte Macht','es':'poder concentrado','pt':'poder concentrado','it':'potere concentrato','pl':'skoncentrowana władza'},
'powerful institutions':{'de':'mächtige Institutionen','pl':'potężne instytucje'},
'secret governing project':{'fr':'projet secret de gouvernement','de':'geheimes Regierungsprojekt','es':'proyecto secreto de gobierno','pt':'projeto secreto de governo','it':'progetto segreto di governo','ro':'proiect secret de guvernare','pl':'tajny projekt rządzenia'},
'pandemic-era surveillance':{'fr':'surveillance pendant la pandémie','de':'Überwachung während der Pandemie','es':'vigilancia durante la pandemia','pt':'vigilância durante a pandemia','it':'sorveglianza durante la pandemia','ro':'supraveghere în timpul pandemiei','pl':'nadzór podczas pandemii'},
'dependence on authorities':{'ro':'dependență de autorități','pl':'zależność od władz'},
'necessary health response':{'de':'notwendige Gesundheitsmaßnahme','pt':'resposta sanitária necessária','ro':'răspuns sanitar necesar'},
'fear-driven explanation':{'ro':'explicație alimentată de teamă','pl':'wyjaśnienie oparte na strachu'},
'intrusive control':{'de':'eingreifende Kontrolle','pl':'inwazyjna kontrola'},
'secret-society legends':{'fr':'légendes sur les sociétés secrètes','de':'Legenden über Geheimgesellschaften','es':'leyendas sobre sociedades secretas','pt':'lendas sobre sociedades secretas','it':'leggende sulle società segrete','ro':'legende despre societăți secrete','pl':'legendy o tajnych stowarzyszeniach'},
'organized reality':{'pl':'zorganizowana rzeczywistość'}
}
fix['repeated media messages']['it']='messaggi ripetuti dei media'
for term,langs in fix.items():
 for lang,value in langs.items():
  assert term in d['translations'][lang],(term,lang)
  d['translations'][lang][term]=value
p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
print(sum(map(len,fix.values())),'labels corrected')
