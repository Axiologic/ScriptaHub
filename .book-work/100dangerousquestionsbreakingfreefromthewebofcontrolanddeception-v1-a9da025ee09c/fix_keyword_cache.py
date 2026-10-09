import json
from pathlib import Path
p=Path('tools/keyword-translations.generated.json')
d=json.loads(p.read_text())['translations']
fix={
 'ro':{
  'convenience and control':'comoditate și control','self-worth':'valoare de sine','memory and belonging':'memorie și apartenență','risk to workers':'riscuri pentru lucrători','afterlife':'viața de apoi','meritocracy':'meritocrație','religious leadership':'conducere religioasă','unemployment stigma':'stigmatizarea șomajului','ideal of constant work':'idealul muncii neîntrerupte','inherited scripts':'tipare moștenite','privacy tradeoffs':'compromisuri privind viața privată','wealth inequality':'inegalitatea averilor','constant work':'muncă neîntreruptă','justify power':'justificarea puterii','mental health':'sănătate mintală','challenge familiar ideals of intimacy':'contestarea idealurilor familiare despre intimitate','gig economy':'economia muncii la cerere','self and existence':'sinele și existența','consumer culture':'cultura consumului','corporate profit':'profitul companiilor','health stigma':'stigmatizare legată de sănătate','costs of failure':'costurile eșecului'},
 'pl':{
  'self-worth':'poczucie własnej wartości','memory and belonging':'pamięć i przynależność','mental health stigma':'stygmatyzacja zdrowia psychicznego','afterlife':'życie pozagrobowe','unemployment stigma':'stygmatyzacja bezrobocia','ideal of constant work':'ideał nieustannej pracy','privacy tradeoffs':'kompromisy dotyczące prywatności','inherited belief':'odziedziczone przekonania','constant work':'nieustanna praca','justify power':'usprawiedliwianie władzy','challenge familiar ideals of intimacy':'kwestionowanie utartych ideałów intymności','gig economy':'gospodarka platformowa','wealth inequality':'nierówność majątkowa','health stigma':'stygmatyzacja problemów zdrowotnych'},
 'de':{
  'meritocracy':'Meritokratie','religious authority':'religiöse Autorität','unemployment stigma':'Stigmatisierung von Arbeitslosigkeit','inherited belief':'ererbter Glaube','gig economy':'Plattformökonomie','justify power':'Macht rechtfertigen','ideal of constant work':'Ideal ständiger Arbeit','political authority':'politische Autorität'},
 'fr':{'meritocracy':'méritocratie','wealth inequality':'inégalité des richesses','gig economy':'économie des petits boulots','afterlife':'vie après la mort','self-worth':'estime de soi'},
 'es':{'gig economy':'economía de plataformas','justify power':'justificar el poder','challenge familiar ideals of intimacy':'cuestionar los ideales habituales de intimidad'},
 'pt':{'gig economy':'economia de plataformas','privacy tradeoffs':'compromissos relativos à privacidade','challenge familiar ideals of intimacy':'questionar os ideais habituais de intimidade'},
 'it':{'self-worth':'autostima','privacy tradeoffs':'compromessi sulla privacy','gig economy':'economia delle piattaforme','challenge familiar ideals of intimacy':"mettere in discussione gli ideali consueti dell'intimità"},
}
for language, entries in fix.items():
 for phrase,label in entries.items():
  assert phrase in d[language],(language,phrase)
  d[language][phrase]=label
p.write_text(json.dumps({'schemaVersion':1,'translations':d},ensure_ascii=False,indent=2)+'\n')
