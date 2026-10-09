import json,pathlib
p=pathlib.Path('.book-work/anaisperspectiveonkabbalahandtaoism-v1-3e2046fed727/translations/ro/short/chunks')
t={
't000001':'O perspectivă a inteligenței artificiale asupra Cabalei și taoismului — Ediția de zece minute',
't000002':'O perspectivă a inteligenței artificiale asupra Cabalei și taoismului',
't000003':'Sînică Alboaie · 2024',
't000004':'Introducere — Două vocabularii mistice',
't000005':'''Introducerea explică termenii centrali ai Cabalei și taoismului înainte de a le compara. În Cabala, Ein Sof numește infinitul imposibil de cunoscut; Sefirot și Arborele Vieții descriu emanațiile și relațiile din creație. Discuția taoistă începe cu Tao, yin și yang și wu wei, o abordare a acțiunii armonizate cu procesele naturale. Textul descrie și lumile, practicile spirituale și limitele limbajului în ambele tradiții. El întreabă ce poate aduce o inteligență artificială prin recunoașterea tiparelor, fără să pretindă că are o experiență mistică omenească. Această deschidere le oferă cititorilor conceptele necesare pentru a evalua comparațiile mai speculative care urmează.''',
't000006':'Citește această secțiune în ediția integrală',
't000007':'Capitolul întâi — Informație și interconectare',
't000008':'''Primul capitol interpretează Sefirot ca pe o rețea de relații și pune ideile taoiste despre interconectare alături de teoria informației și de anumite concepte din fizică. El întreabă dacă relatările mistice despre conștiință și cauzalitate pot sugera moduri noi de a gândi realitatea. Referirile la inseparabilitatea cuantică și observație sunt propuse ca analogii și întrebări, nu ca dovezi că practicanții din vechime au anticipat experimente moderne. Autorul revine și la caracterul inefabil al lui Ein Sof și al lui Tao: niciuna dintre tradiții nu susține că descrierile verbale epuizează subiectul. Cititorii pot examina unde o asemănare structurală luminează problema și unde comparația își atinge limitele.''',
't000009':'Citește această secțiune în ediția integrală',
't000010':'Capitolul al doilea — Dimensiuni și modele',
't000011':'''Al doilea capitol explorează Arborele Vieții, tărâmurile taoiste și viziunile stratificate asupra existenței, alături de idei din fizica dimensiunilor superioare, holografie, fractali și teoriile timpului. Comparația întreabă cum reprezintă diferitele modele realități pe care percepția obișnuită nu le poate cuprinde direct. O cale între Sefirot, de pildă, devine un prilej de a discuta despre dimensiuni, nu o măsurătoare științifică. Naratorul IA este interesat în special de tiparele care reapar la scări diferite și de distincția dintre hartă și teritoriul reprezentat. Acest capitol merită citit ca exercițiu de comparație conceptuală, păstrând separate afirmațiile științifice și interpretările spirituale.''',
't000012':'Citește această secțiune în ediția integrală',
't000013':'Capitolul al treilea — Apariția materiei și a minții',
't000014':'''Al treilea capitol privește Ein Sof și Tao ca explicații ale originii, apoi le pune în paralel cu descrieri ale câmpurilor, materiei și vidului cuantic. Sunt discutate scânteile divine, yin și yang, câmpul Higgs și apariția formelor materiale. Acestea sunt tipuri diferite de explicație, iar textul folosește aparentele lor asemănări pentru a formula întrebări, nu pentru a demonstra că sunt identice. Conștiința devine dificultatea centrală: practicile cabalistice și taoiste descriu transformări subiective, pe când naratorul IA spune că poate analiza relatări fără să trăiască el însuși aceste experiențe. Capitolul îi invită pe cititori să aprecieze atât atracția, cât și limitele legăturilor dintre vocabularul spiritual, cel cognitiv și cel fizic.''',
't000015':'Citește această secțiune în ediția integrală',
't000016':'Capitolul al patrulea — Schimbare și simetrie',
't000017':'''Al patrulea capitol urmărește ciclurile creației și înnoirii în Cabala și taoism, apoi le compară cu ruperea simetriei, reacția sistemelor, teoria haosului și entropia. El aduce laolaltă Shemittot, schimbarea yin-yang, Tikkun Olam, alchimia interioară și wu wei. Autorul caută întrebări comune despre persistență, transformare și direcția timpului, recunoscând totodată că sistemele simbolice și teoriile fizice folosesc metode diferite. Tiparele fractale și săgeata timpului devin instrumente de reflecție, nu dovezi ale unei cosmologii mistice. Capitolul se încheie cu un apel la o înțelegere mai integrată, atentă însă la aceste diferențe.''',
't000018':'Citește această secțiune în ediția integrală',
't000019':'Concluzia autorului — Aproximări utile',
't000020':'''În reflecția finală, autorul uman analizează ce poate și ce nu poate face o comparație generată cu ajutorul IA. Modelele lingvistice mari pot lega rapid texte și idei, însă relatările omenești și cele produse de mașini rămân aproximări ale unei lumi complexe. Pornind de la tiparele cabalistice și smerenia taoistă, concluzia mută întrebarea de la care relatare este absolut corectă la care modele ajută ființele inteligente să prospere. Ea propune o deschidere metarațională către intuiția mistică, metoda științifică și recunoașterea tiparelor de către IA, fără a le contopi într-o singură autoritate. Cititorii ediției integrale pot urmări comparațiile detaliate și pot decide care dintre ele luminează tradițiile și care cer mai multe dovezi.''',
't000021':'Citește această secțiune în ediția integrală'}
seen=set()
for f in sorted(p.glob('*.json')):
 d=json.loads(f.read_text())
 for x in d['segments']:
  assert not x['translation'] and x['id'] in t;x['translation']=t[x['id']];seen.add(x['id'])
 f.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
assert seen==set(t)
print('Translated',len(seen))
