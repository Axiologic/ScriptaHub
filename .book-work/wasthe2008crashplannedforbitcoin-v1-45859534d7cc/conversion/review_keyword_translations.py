#!/usr/bin/env python3
"""Correct misleading local-model discovery labels for this reader."""
import json
from pathlib import Path

p = Path("tools/keyword-translations.generated.json")
data = json.loads(p.read_text(encoding="utf-8"))
translations = data["translations"]
fixes = {
    "banking collapse": {"pl": "załamanie banków"},
    "deliberate orchestration": {"pl": "celowa koordynacja"},
    "distributed systems": {"pl": "systemy rozproszone"},
    "digital currency": {"ro": "monedă digitală"},
    "proof-of-work": {"fr": "preuve de travail", "de": "Proof of Work", "es": "prueba de trabajo", "it": "prova di lavoro"},
    "Hashcash": {"ro": "Hashcash", "pt": "Hashcash", "it": "Hashcash"},
    "monetary design": {"ro": "model monetar", "de": "monetäres Konzept", "pt": "conceção monetária"},
    "white paper": {"ro": "document de prezentare tehnică", "de": "Whitepaper", "es": "libro blanco", "pt": "livro branco", "it": "documento tecnico"},
    "housing market": {"de": "Immobilienmarkt"},
    "financial regulation": {"ro": "reglementare financiară", "de": "Finanzregulierung", "es": "regulación financiera", "pt": "regulação financeira", "it": "regolamentazione finanziaria", "pl": "regulacja finansowa"},
    "housing bubble": {"ro": "bulă imobiliară", "de": "Immobilienblase", "fr": "bulle immobilière", "es": "burbuja inmobiliaria", "pt": "bolha imobiliária", "it": "bolla immobiliare"},
    "centralized finance": {"ro": "finanțe centralizate", "de": "zentralisiertes Finanzwesen", "fr": "finance centralisée", "es": "finanzas centralizadas", "pl": "scentralizowane finanse"},
    "public launch": {"de": "öffentliche Einführung", "pl": "publiczne wprowadzenie"},
    "launch and acceptance": {"de": "Einführung und Akzeptanz", "pl": "wprowadzenie i akceptacja"},
    "weak financial regulation": {"de": "schwache Finanzregulierung"},
    "banking failure": {"ro": "faliment bancar", "de": "Bankenzusammenbruch", "es": "quiebra bancaria", "pl": "upadłość bankowa"},
    "alternative monetary design": {"ro": "model monetar alternativ", "de": "alternatives monetäres Konzept", "pt": "modelo monetário alternativo", "pl": "alternatywny model monetarny"},
    "attacks of September 2001": {"es": "atentados de septiembre de 2001"},
    "loose monetary policy": {"ro": "politică monetară permisivă", "de": "expansive Geldpolitik", "fr": "politique monétaire accommodante", "es": "política monetaria expansiva", "pt": "política monetária expansionista", "it": "politica monetaria espansiva", "pl": "łagodna polityka pieniężna"},
    "financial strain": {"pl": "napięcia finansowe", "pt": "pressão financeira"},
    "historical setting": {"ro": "context istoric", "es": "contexto histórico", "pl": "kontekst historyczny"},
    "orchestration theory": {"ro": "teoria orchestrării", "pl": "teoria celowej koordynacji"},
    "orchestrated collapse": {"pl": "skoordynowane załamanie"},
    "cryptocurrencies": {"ro": "criptomonede", "pl": "kryptowaluty"},
    "documentary evidence": {"de": "dokumentarische Belege", "pl": "dowody dokumentalne"},
    "evidentiary gap": {"ro": "lipsă de dovezi", "pl": "luka dowodowa", "pt": "lacuna probatória"},
    "national currencies": {"ro": "monede naționale"},
    "storing value": {"ro": "păstrarea valorii", "de": "Wertspeicherung", "fr": "conservation de la valeur", "es": "conservación del valor", "pt": "reserva de valor", "it": "conservazione del valore", "pl": "przechowywanie wartości"},
    "intentional design": {"ro": "proiectare intenționată", "de": "bewusster Entwurf", "pt": "conceção intencională", "pl": "celowy projekt"},
    "cryptographic systems": {"pl": "systemy kryptograficzne", "es": "sistemas criptográficos", "pt": "sistemas criptográficos"},
    "single center": {"de": "einzige Zentrale", "it": "centro unico"},
    "global events": {"de": "globale Ereignisse"},
    "established finding": {"ro": "constatare demonstrată", "de": "gesicherte Erkenntnis", "fr": "constat établi", "es": "conclusión demostrada", "pt": "conclusão demonstrada", "it": "risultato accertato", "pl": "potwierdzony wniosek"},
    "speculative account": {"ro": "interpretare speculativă", "de": "spekulative Darstellung", "fr": "interprétation spéculative", "es": "interpretación especulativa", "pt": "interpretação especulativa", "it": "interpretazione speculativa", "pl": "spekulacyjna interpretacja"},
    "decentralized currency": {"ro": "monedă descentralizată"},
    "adoption of cryptocurrency": {"pl": "przyjęcie kryptowaluty", "pt": "adoção de criptomoedas"},
    "speculative proposal": {"de": "spekulative These", "pl": "spekulacyjna teza"},
    "growth of a housing bubble": {"ro": "creșterea unei bule imobiliare", "de": "Wachstum einer Immobilienblase", "fr": "croissance d'une bulle immobilière", "es": "crecimiento de una burbuja inmobiliaria", "pt": "crescimento de uma bolha imobiliária", "it": "crescita di una bolla immobiliare"},
    "technical history": {"ro": "istorie tehnică"},
    "major banking failure": {"ro": "prăbușire bancară majoră", "de": "schwerer Bankenzusammenbruch", "es": "gran quiebra bancaria", "it": "grave crisi bancaria", "pl": "poważna zapaść bankowa"},
    "decentralized alternative": {"es": "alternativa descentralizada"},
}
for phrase, languages in fixes.items():
    for language, value in languages.items():
        assert phrase in translations[language], (phrase, language)
        translations[language][phrase] = value
p.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(sum(len(v) for v in fixes.values()), "keyword labels reviewed")
