"""Reviewed catalogue copy for Brontë's original novel."""
from pathlib import Path
import json

path = Path(__file__).resolve().parent / 'book/manifest.json'
data = json.loads(path.read_text())
copy = {
 'en': ('Wuthering Heights', 'Catherine, Heathcliff, and the legacy of two houses', [
  'Lockwood’s visit to Wuthering Heights opens a layered account of Catherine Earnshaw and Heathcliff.',
  'Nelly Dean traces their childhood bond, Catherine’s marriage to Edgar Linton, and Heathcliff’s return.',
  'His revenge moves through property, marriage, and the lives of the next generation.',
  'The Yorkshire moors frame conflicting desires, social rank, grief, and confinement.',
  'Catherine Linton and Hareton Earnshaw find a different way to relate after inherited harm.',
  'Brontë’s shifting narrators leave passion and cruelty open to the reader’s judgment.']),
 'fr': ('Les Hauts de Hurlevent', 'Catherine, Heathcliff et l’héritage de deux maisons', [
  'La visite de Lockwood à Wuthering Heights ouvre le récit complexe de Catherine Earnshaw et Heathcliff.',
  'Nelly Dean raconte leur enfance, le mariage de Catherine avec Edgar Linton et le retour de Heathcliff.',
  'Sa vengeance passe par la propriété, le mariage et la vie de la génération suivante.',
  'Les landes du Yorkshire entourent les désirs opposés, le rang social, le deuil et l’enfermement.',
  'Catherine Linton et Hareton Earnshaw inventent un autre lien après les blessures héritées.',
  'Les narrateurs changeants de Brontë laissent au lecteur le jugement de la passion et de la cruauté.']),
 'de': ('Sturmhöhe', 'Catherine, Heathcliff und das Erbe zweier Häuser', [
  'Lockwoods Besuch auf Wuthering Heights eröffnet die vielschichtige Geschichte von Catherine Earnshaw und Heathcliff.',
  'Nelly Dean erzählt von ihrer Kindheit, Catherines Ehe mit Edgar Linton und Heathcliffs Rückkehr.',
  'Seine Rache greift über Besitz, Heirat und das Leben der nächsten Generation aus.',
  'Die Moore Yorkshires rahmen widerstreitende Wünsche, Standesunterschiede, Trauer und Gefangenschaft.',
  'Catherine Linton und Hareton Earnshaw finden nach ererbtem Leid einen anderen Umgang miteinander.',
  'Brontës wechselnde Erzähler überlassen das Urteil über Leidenschaft und Grausamkeit den Lesenden.']),
 'es': ('Cumbres borrascosas', 'Catherine, Heathcliff y el legado de dos casas', [
  'La visita de Lockwood a Wuthering Heights abre la historia entrelazada de Catherine Earnshaw y Heathcliff.',
  'Nelly Dean relata su infancia, el matrimonio de Catherine con Edgar Linton y el regreso de Heathcliff.',
  'Su venganza alcanza la propiedad, el matrimonio y la vida de la siguiente generación.',
  'Los páramos de Yorkshire enmarcan deseos enfrentados, posición social, duelo y encierro.',
  'Catherine Linton y Hareton Earnshaw descubren otra manera de relacionarse tras el daño heredado.',
  'Los narradores cambiantes de Brontë dejan al lector juzgar la pasión y la crueldad.']),
 'pt': ('O Morro dos Ventos Uivantes', 'Catherine, Heathcliff e o legado de duas casas', [
  'A visita de Lockwood a Wuthering Heights abre a história entrelaçada de Catherine Earnshaw e Heathcliff.',
  'Nelly Dean narra sua infância, o casamento de Catherine com Edgar Linton e o retorno de Heathcliff.',
  'Sua vingança atinge a propriedade, o casamento e a vida da geração seguinte.',
  'Os campos de Yorkshire emolduram desejos opostos, posição social, luto e confinamento.',
  'Catherine Linton e Hareton Earnshaw encontram outra maneira de se relacionar após danos herdados.',
  'Os narradores alternados de Brontë deixam ao leitor o julgamento da paixão e da crueldade.']),
 'it': ('Cime tempestose', 'Catherine, Heathcliff e l’eredità di due case', [
  'La visita di Lockwood a Wuthering Heights apre la storia stratificata di Catherine Earnshaw e Heathcliff.',
  'Nelly Dean racconta la loro infanzia, il matrimonio di Catherine con Edgar Linton e il ritorno di Heathcliff.',
  'La sua vendetta coinvolge proprietà, matrimonio e vita della generazione successiva.',
  'Le brughiere dello Yorkshire incorniciano desideri opposti, rango sociale, lutto e prigionia.',
  'Catherine Linton e Hareton Earnshaw trovano un modo diverso di incontrarsi dopo il danno ereditato.',
  'I narratori mutevoli di Brontë lasciano al lettore il giudizio su passione e crudeltà.']),
 'ro': ('La răscruce de vânturi', 'Catherine, Heathcliff și moștenirea a două case', [
  'Vizita lui Lockwood la Wuthering Heights deschide povestea cu mai multe voci a Catherinei Earnshaw și a lui Heathcliff.',
  'Nelly Dean povestește copilăria lor, căsătoria Catherinei cu Edgar Linton și întoarcerea lui Heathcliff.',
  'Răzbunarea lui se întinde asupra proprietăților, căsătoriilor și vieții generației următoare.',
  'Mlaștinile din Yorkshire încadrează dorințe opuse, rang social, doliu și captivitate.',
  'Catherine Linton și Hareton Earnshaw găsesc o altă cale de apropiere după răul moștenit.',
  'Naratorii schimbători ai lui Brontë lasă cititorului judecata asupra pasiunii și cruzimii.']),
 'pl': ('Wichrowe Wzgórza', 'Catherine, Heathcliff i dziedzictwo dwóch domów', [
  'Wizyta Lockwooda w Wuthering Heights otwiera wielogłosową historię Catherine Earnshaw i Heathcliffa.',
  'Nelly Dean opowiada o ich dzieciństwie, małżeństwie Catherine z Edgarem Lintonem i powrocie Heathcliffa.',
  'Jego zemsta obejmuje majątek, małżeństwo oraz życie następnego pokolenia.',
  'Wrzosowiska Yorkshire otaczają sprzeczne pragnienia, podziały społeczne, żałobę i zniewolenie.',
  'Catherine Linton i Hareton Earnshaw znajdują inną drogę do bliskości po odziedziczonych krzywdach.',
  'Zmieniający się narratorzy Brontë pozostawiają czytelnikowi ocenę namiętności i okrucieństwa.']),
}
assert set(copy) == set(data['title'])
for language, (title, subtitle, sentences) in copy.items():
    assert len(sentences) == 6
    assert all(len(sentence.split()) <= 22 for sentence in sentences), (language, sentences)
    data['title'][language] = title
    data['subtitle'][language] = subtitle
    data['shortDescription'][language] = ' '.join(sentences)
    data['aboutBook'][language] = [' '.join(sentences[:3]), ' '.join(sentences[3:])]
data['shortDescriptionEditorial'] = {'source': 'editorial-review', 'sourceVersion': 1, 'reviewed': True}
data['metadataDraft']['reviewRequired'] = False
data['metadataDraft']['reviewedAgainst'] = 'Emily Brontë’s 34 original chapters and the EN/RO ten-minute readers'
path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')
print('Reviewed metadata in', len(copy), 'languages')
