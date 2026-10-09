import json
from pathlib import Path

root = Path(__file__).parent / 'translations/ro/short/chunks'
translations = {
    't000001': 'În necunoscut: Călătoria lui Bilbo în Hobbitul — ediția de zece minute',
    't000002': 'În necunoscut: Călătoria lui Bilbo în Hobbitul',
    't000003': 'Această carte îl urmărește pe Bilbo Baggins ca ghid pentru cititori prin curajul, creșterea și atracția dintre confort și aventură în Hobbitul de J.R.R. Tolkien. Trece de la plecarea șovăitoare a lui Bilbo prin întâlnirile cu troli, goblini și Smaug până la alegerile sale de aproape de finalul călătoriei. Autoarea acordă atenție umorului și ezitărilor lui Bilbo, la fel ca vitejiei sale. Capitolele discută momente importante ale romanului, inclusiv conflictul de mai târziu, fiind potrivite pentru cineva care acceptă detalii din poveste.',
    't000004': 'Un călător nehotărât',
    't000005': 'Introducerea începe cu viața așezată a lui Bilbo în Comitat. Gandalf și piticii tulbură o lume ordonată în jurul meselor cunoscute, al rutinei și al siguranței. Bilbo nu devine dintr-odată un aventurier neînfricat; perspectiva de a pleca de acasă îl neliniștește. Cartea tratează această ezitare ca pe o parte a farmecului său. Călătoria imaginată de Tolkien întreabă dacă dezvoltarea cere părăsirea confortului și dacă omul poate descoperi capacități pe care acasă nu avusese nevoie să le folosească.',
    't000006': 'Citește integral secțiunea 1',
    't000007': 'Primul pas dincolo de casă',
    't000008': 'Primul capitol urmărește adunarea neașteptată de la ușa lui Bilbo și presiunea de a se alătura cetei lui Thorin. Piticii așteaptă un hoț; Bilbo nu are prea multe dovezi că ar putea fi unul. Plecarea lui este, așadar, o alegere făcută în incertitudine, nu simpla dezvăluire a unui erou. Autoarea subliniază nepotrivirea comică dintre obiceiurile domestice ale lui Bilbo și drumul sălbatic din fața sa. Nepotrivirea dă energie începutului poveștii și face ca fiecare act de curaj de mai târziu să pară câștigat.',
    't000009': 'Citește integral secțiunea 2',
    't000010': 'Troli, goblini și o minte mai ageră',
    't000011': 'Al doilea capitol îl urmărește pe Bilbo într-o lume în care mărimea și puterea nu rezolvă fiecare problemă. Trolii și goblinii arată cât de vulnerabilă poate fi ceata, iar ghicitorile lui Gollum fac decisivă gândirea sub presiune. Bilbo este speriat și greșește, însă învață să observe, să improvizeze și să acționeze când ajutorul nu este aproape. Autoarea citește aceste scene ca pe o schimbare a relației lui Bilbo cu pericolul. Nu încetează să se teamă; începe să găsească și alt răspuns decât retragerea.',
    't000012': 'Citește integral secțiunea 3',
    't000013': 'În fața lui Smaug',
    't000014': 'Al treilea capitol se concentrează asupra întâlnirii lui Bilbo cu dragonul. Intrarea în vizuina lui Smaug cere să nu fie văzut, dar conversația cere și cuvinte alese atent. Bilbo trebuie să strângă informații fără să dezvăluie prea mult. Capitolul explorează curajul și riscul acestui schimb: vorbele istețe pot deschide o cale, dar pot și provoca un dușman puternic. Cartea arată cum crește încrederea lui Bilbo în această întâlnire și cum faptele lui au urmări dincolo de el și de pitici.',
    't000015': 'Citește integral secțiunea 4',
    't000016': 'Înțelepciune în mijlocul conflictului',
    't000017': 'Al patrulea capitol privește ce face Bilbo după dragon. Revendicările concurente asupra comorii amenință să transforme o misiune împlinită într-un nou dezastru. Alegerile lui Bilbo arată un alt fel de curaj: încearcă să împiedice violența chiar când prietenilor săi s-ar putea să nu le placă metoda. Autoarea pune față în față loialitatea față de tovarăși și răspunderea față de oamenii din afara grupului. Puterea lui Bilbo nu se mai măsoară doar prin cât de departe poate merge sau ce pericol poate supraviețui, ci prin judecata pe care o aduce într-o situație tensionată.',
    't000018': 'Citește integral secțiunea 5',
    't000019': 'Întoarcerea unui om schimbat',
    't000020': 'Concluzia vede călătoria lui Bilbo ca pe mai mult decât un drum din Comitat până la un munte și înapoi. Curajul lui crește odată cu înțelegerea propriilor limite, a prieteniei și a prețului lăcomiei. Căminul cunoscut rămâne important, dar Bilbo se întoarce cu un simț mai larg al lucrurilor pe care le cuprinde lumea și al faptelor pe care le poate face. Cartea îi invită pe cititori să observe cum folosește Tolkien un personaj mic și nehotărât pentru a face personale întrebările mari despre schimbare.',
    't000021': 'Citește integral secțiunea 6',
}
seen = set()
for path in sorted(root.glob('*.json')):
    data = json.loads(path.read_text(encoding='utf-8'))
    for item in data['segments']:
        item['translation'] = translations[item['id']]
        seen.add(item['id'])
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
assert seen == set(translations)
