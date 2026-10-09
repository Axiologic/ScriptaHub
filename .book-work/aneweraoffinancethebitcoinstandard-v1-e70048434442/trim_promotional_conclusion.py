from pathlib import Path
from bs4 import BeautifulSoup

work = Path(__file__).resolve().parent / 'book'
removals = {
    'en': 'The Bitcoin Standard: The Decentralized Alternative to Central Banking by Saifedean Ammous offers valuable insights into this revolutionary currency, encouraging readers to reconsider traditional notions of money and value. ',
    'ro': 'The Bitcoin Standard: The Decentralized Alternative to Central Banking, de Saifedean Ammous, oferă perspective valoroase asupra acestei monede revoluționare și îi îndeamnă pe cititori să regândească noțiunile tradiționale de bani și valoare. ',
}
for language, sentence in removals.items():
    path = work / language / 'full_content.html'
    soup = BeautifulSoup(path.read_text(), 'html.parser')
    paragraph = next(p for p in soup.find_all('p') if sentence in p.get_text())
    assert paragraph.string and sentence in paragraph.string
    paragraph.string.replace_with(paragraph.string.replace(sentence, ''))
    lead = 'As you engage with Ammous' if language == 'en' else 'Citind argumentele și analizele'
    promo = next(p for p in soup.find_all('p') if p.get_text().startswith(lead))
    promo.decompose()
    path.write_text(str(soup))
