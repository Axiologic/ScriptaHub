import json
from pathlib import Path

root = Path(__file__).parent / 'translations/ro/full/chunks/0008.json'
data = json.loads(root.read_text(encoding='utf-8'))
translations = {
    't000018': 'Concluzie',
    't000019': 'În concluzie, Hobbitul: Sau până acolo și înapoi de J.R.R. Tolkien este mai mult decât o poveste de aventură; este o explorare profundă a creșterii, curajului și transformării interioare. Bilbo Baggins, un hobbit obișnuit, pornește într-o călătorie neașteptată care îi pune la încercare limitele vitejiei și îi schimbă complet felul de a privi lumea. Din viața confortabilă a Comitatului, Bilbo se aventurează în necunoscut, înfruntând creaturi primejdioase, ținuturi ostile și, mai ales, propriile temeri. Astfel, povestea lui Tolkien nu este doar o epopee fantastică, ci și o lecție despre creștere personală, descoperire de sine și curajul de a ieși din zona de confort pentru a deveni mai puternic și mai autentic. Lumea Pământului de Mijloc, plină de magie, pericol și uimire, a captivat generații de cititori. Hobbitul este mai mult decât un preludiu la Stăpânul inelelor; stă pe propriile picioare ca o poveste frumos construită despre prietenie, loialitate și lupta dintre bine și rău.',
    't000020': 'Bibliografie',
}
for item in data['segments']:
    item['translation'] = translations.get(item['id'], item['source'])
root.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
