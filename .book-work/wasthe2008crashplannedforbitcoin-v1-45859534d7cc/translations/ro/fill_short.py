#!/usr/bin/env python3
"""Agent-authored Romanian translations for the stable short-reader chunk."""
import json
from pathlib import Path

chunk = Path(__file__).parent / "short/chunks/0001.json"
data = json.loads(chunk.read_text(encoding="utf-8"))
translations = [
    "A fost planificată prăbușirea din 2008 pentru Bitcoin? — Ediția de zece minute",
    "A fost planificată prăbușirea din 2008 pentru Bitcoin?",
    "Ediția de zece minute",
    "Cartea întreabă dacă criza financiară din 2008 doar a oferit un context favorabil pentru Bitcoin sau dacă a fost provocată deliberat pentru apariția sa. Urmărește patru fire: cercetările anterioare despre criptografie și bani digitali, colapsul bancar, evenimentele globale dinainte de 2008 și o interpretare speculativă despre orchestrarea crizei. Concluzia trasează o limită clară în jurul acestei speculații: textul afirmă că nu există dovezi concrete că prăbușirea a fost planificată pentru lansarea Bitcoin. Întrebarea rămâne, așadar, subiectul unei cercetări, nu o constatare demonstrată.",
    "Criptografia înaintea crizei",
    "Primul capitol așază Bitcoin într-o istorie tehnică mai lungă. Criptografia fusese deja folosită pentru a securiza informațiile și comunicațiile, în timp ce cercetătorii analizau sistemele distribuite și diferite forme de monedă digitală. Cartea amintește Hashcash, creat de Adam Back în 1997, și mecanismul proof-of-work ca precursori ai unor soluții asociate mai târziu cu Bitcoin. Susține că importanța tot mai mare a internetului a sporit interesul pentru sisteme sigure care nu depind de un centru unic. Acest lucru contează pentru întrebarea centrală a cărții, fiindcă tehnologia nu a apărut din nimic în 2008: componentele ei se dezvoltau înaintea crizei financiare.",
    "Capitolul se încheie cu o întrebare diferită de cea a posibilității tehnice. Chiar dacă proiectul putea fi imaginat mai devreme, a făcut climatul economic din 2008 mai probabilă lansarea și acceptarea sa publică? Cartea prezintă momentul ca întrebare pentru capitolele următoare, nu ca dovadă a vreunui plan.",
    "O criză a încrederii",
    "Capitolul al doilea descrie prăbușirea pieței imobiliare și a băncilor din Statele Unite drept o criză extinsă în economia mondială. Indică printre cauze practicile bancare riscante, reglementarea financiară slabă și bula imobiliară. În relatarea cărții, colapsul a afectat încrederea publicului în bănci și guverne, făcând mai atrăgătoare o monedă aflată în afara controlului lor direct. Apariția Bitcoin în acel moment este prezentată ca remarcabilă, iar capitolul întreabă dacă cineva ar fi putut manipula condițiile care au făcut ca lansarea sa să pară oportună.",
    "Sursa pune documentul lui Satoshi Nakamoto în legătură cu nemulțumirea față de finanțele centralizate. Nu oferă dovezi că Nakamoto sau altcineva a provocat criza. Cea mai solidă observație susținută este coincidența dintre un eșec bancar major și introducerea unui model monetar alternativ. Legătura cauzală propusă rămâne o întrebare.",
    "Evenimentele care au dus la 2008",
    "Al treilea capitol lărgește perspectiva temporală. Menționează atentatele din septembrie 2001, războaiele din Orientul Mijlociu, cheltuielile mari ale Statelor Unite, politica monetară relaxată și creșterea bulei imobiliare. Cartea leagă aceste evenimente de presiunea financiară și de condițiile care au precedat prăbușirea. Apoi întreabă dacă ele ar fi putut grăbi scăderea încrederii în banii convenționali și face mai atractivă o alternativă descentralizată.",
    "Aici argumentul trece de la o succesiune de evenimente la posibilitatea unui scop ascuns. Sursa oferă un context istoric pentru întrebare, dar nu demonstrează că evenimentele au fost coordonate pentru a pregăti Bitcoin. Diferența contează: a arăta că anumite împrejurări au precedat o invenție este mai puțin decât a demonstra că au fost aranjate pentru ea.",
    "Teoria orchestrării",
    "Capitolul al patrulea formulează propunerea cea mai speculativă. Unele teorii, spune textul, consideră criza un colaps orchestrat pentru introducerea unei noi ordini economice. În această interpretare, criptomonedele ar putea completa sau înlocui sistemele monetare tradiționale. Cartea sugerează un posibil motiv: crearea unui sistem mai transparent și mai sigur, mai puțin expus manipulării de către guverne sau bănci centrale. Întreabă și dacă anumite evenimente economice ar fi putut fi influențate pentru a oferi Bitcoin un mediu mai bun de lansare.",
    "Acestea sunt posibilități atribuite unor teorii, nu evenimente demonstrate. Cartea nu identifică un organizator și nu prezintă dovezi documentare ale unei coordonări. Capitolul dezvoltă suspiciunea și motivul propus, lăsând vizibilă lipsa dovezilor.",
    "Concluzia cărții",
    "Concluzia afirmă că nu există dovezi concrete pentru o orchestrare deliberată între 2000 și 2008. Reunește în schimb evoluțiile tehnice anterioare, criza mondială și pierderea încrederii în finanțele centralizate. Textul susține că aceste condiții au făcut modelul alternativ al Bitcoin mai relevant. Sugerează că prăbușirea a ajutat recunoașterea și adoptarea criptomonedelor, admițând totodată că aceasta nu dovedește că prăbușirea a fost provocată în acest scop.",
    "O secțiune finală întreabă cine ar putea beneficia de moneda descentralizată. Cartea indică persoanele care trăiesc cu monede naționale instabile sau sub reguli financiare restrictive, pentru care păstrarea valorii și transferul banilor în afara băncilor convenționale pot părea atrăgătoare. Astfel, discuția trece de la presupusele origini ale crizei la oamenii care ar putea câștiga dintr-o alternativă financiară. Cititorii rămân cu distincția dintre o criză documentată, o tehnologie în curs de apariție și o afirmație nedovedită despre un plan intenționat.",
    "Harta sursei",
    "Prefața și întrebarea de pornire",
    "Capitolul întâi: sisteme criptografice",
    "Capitolul al doilea: criza financiară",
    "Capitolul al treilea: evenimente dinainte de 2008",
    "Capitolul al patrulea: teoria orchestrării",
    "Concluzie și beneficiari",
    "Bibliografie",
]
assert len(translations) == len(data["segments"]), (len(translations), len(data["segments"]))
for segment, translation in zip(data["segments"], translations, strict=True):
    if segment["translation"] and segment["translation"] != translation:
        raise ValueError(f"Existing translation differs: {segment['id']}")
    segment["translation"] = translation
chunk.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(f"Filled {len(translations)} segments in {chunk}")
