#!/usr/bin/env python3
"""Optional local NLP worker; catalogue I/O and command dispatch live in Node.js."""

from __future__ import annotations

import contextlib
from collections import Counter
import importlib.metadata
import json
import os
from pathlib import Path
import re
import sys
import unicodedata

if sys.version_info < (3, 10):
    raise SystemExit("Local keyword processing requires Python 3.10 or newer. See dependencies.md.")

VOCABULARY = json.loads((Path(__file__).resolve().parent / "vocabulary.json").read_text(encoding="utf-8"))
ENGLISH_STOP_WORDS = frozenset(VOCABULARY["stopWords"])
KEYWORD_NOISE_WORDS = frozenset(VOCABULARY["noiseWords"])
LANGUAGES = ("en", "fr", "de", "es", "pt", "it", "ro", "pl")


def prerequisites(translation=False, require_models=False):
    if sys.version_info < (3, 10):
        raise RuntimeError("Local keyword processing requires Python 3.10 or newer. See dependencies.md.")
    try:
        import nltk
        verify_package("nltk", (3, 10), (4, 0))
        nltk.data.find("tokenizers/punkt_tab/english/")
        nltk.data.find("taggers/averaged_perceptron_tagger_eng/")
        if translation:
            import torch
            import sentencepiece
            from transformers import MarianMTModel, MarianTokenizer
            verify_package("torch", (2, 0))
            verify_package("sentencepiece", (0, 2), (1, 0))
            verify_package("transformers", (4, 50), (5, 0))
            if require_models:
                for model_name in (
                    "Helsinki-NLP/opus-mt-en-ROMANCE",
                    "Helsinki-NLP/opus-mt-en-de",
                    "Helsinki-NLP/opus-mt-en-zlw",
                ):
                    tokenizer = MarianTokenizer.from_pretrained(model_name, local_files_only=True)
                    model = MarianMTModel.from_pretrained(model_name, local_files_only=True)
                    del tokenizer, model
    except (ImportError, LookupError, OSError) as error:
        raise RuntimeError(
            "Local keyword processing needs the optional packages in tools/requirements-keywords.txt "
            "and NLTK punkt_tab/averaged_perceptron_tagger_eng data, plus cached Marian models for imports. "
            "Install them in a project virtual environment as described in dependencies.md. "
            "Nothing is downloaded or installed by this command."
        ) from error


def verify_package(name, minimum, maximum=None):
    installed = importlib.metadata.version(name)
    match = re.fullmatch(r"(\d+)\.(\d+)(?:\.\d+)*(?:\.post\d+)?(?:\+[a-zA-Z0-9._-]+)?", installed)
    version = tuple(map(int, match.groups())) if match else ()
    if version < minimum or (maximum and version >= maximum):
        raise RuntimeError(
            f"Incompatible {name} version {installed}. Use tools/requirements-keywords.txt; see dependencies.md."
        )

def keyword_normalise(value: str) -> str:
    value = unicodedata.normalize("NFKD", value.casefold()).encode("ascii", "ignore").decode("ascii")
    return " " + re.sub(r"\s+", " ", re.sub(r"[^a-z0-9]+", " ", value)).strip() + " "

def _keyword_label(tokens: list[str]) -> str:
    acronyms = {"ai", "agi", "api", "cpu", "gpu", "llm", "ml", "nlp", "rag", "rl", "ui", "ux"}
    words = []
    for token in tokens:
        if token.lower() in acronyms:
            words.append(token.upper())
        else:
            words.append(token.lower())
    return " ".join(words)

def extract_keyword_candidates(
    title: str, description: str, source_text: str, limit: int = 140,
) -> list[str]:
    """Rank noun phrases found verbatim in a book's short edition.

    Only grammar, stop words, and document structure live in code. Subject
    vocabulary comes from the edition itself. Headings are weighted by
    keyword_source_text; the synopsis receives a smaller additional weight.
    """
    try:
        import nltk
    except ImportError as error:
        raise RuntimeError(
            "Keyword extraction needs NLTK; install tools/requirements-keywords.txt"
        ) from error

    weighted = ((description + " ") * 4) + source_text
    title_key = keyword_normalise(title).strip()
    title_terms = {
        token for token in title_key.split()
        if token not in ENGLISH_STOP_WORDS and len(token) > 2
    }
    counts: Counter[str] = Counter()
    surfaces: dict[str, Counter[str]] = {}
    connectors = {"and", "of", "for", "in", "on", "with", "without", "between", "under", "after", "before", "through"}
    sentences = [sentence for sentence in nltk.sent_tokenize(weighted) if sentence.strip()]
    tagged_sentences = nltk.pos_tag_sents([nltk.word_tokenize(sentence) for sentence in sentences])

    def content_token(token: str, tag: str) -> bool:
        lower = keyword_normalise(token).strip()
        return (
            bool(lower)
            and lower not in ENGLISH_STOP_WORDS
            and lower not in KEYWORD_NOISE_WORDS
            and not lower.startswith(("scriptahub", "axiologic", "achilles"))
            and (
                tag.startswith("NN")
                or tag.startswith("JJ")
                or tag in {"VBG", "VBN", "FW"}
                or (token.isupper() and 2 <= len(token) <= 8)
            )
        )

    for tagged in tagged_sentences:
        for start, (token, tag) in enumerate(tagged):
            if not content_token(token, tag):
                continue
            chunk: list[str] = []
            noun_count = 0
            content_count = 0
            for end in range(start, min(len(tagged), start + 7)):
                current, current_tag = tagged[end]
                lower = keyword_normalise(current).strip()
                if content_token(current, current_tag):
                    chunk.append(current)
                    content_count += 1
                    if current_tag.startswith("NN") or (current.isupper() and len(current) >= 2):
                        noun_count += 1
                elif (
                    lower in connectors
                    and chunk
                    and end + 1 < len(tagged)
                    and content_token(*tagged[end + 1])
                ):
                    chunk.append(lower)
                else:
                    break
                if len(chunk) > 5:
                    break
                if content_count < 2 or noun_count < 1:
                    continue
                gerund_noun = current_tag == "VBG" and len(chunk) >= 2 and chunk[-2].casefold() not in connectors
                if not (
                    current_tag.startswith("NN")
                    or current_tag == "FW"
                    or gerund_noun
                    or (current.isupper() and len(current) >= 2)
                ):
                    continue
                label = _keyword_label(chunk)
                key = keyword_normalise(label).strip()
                if key == title_key or len(label) < 5 or len(label) > 68:
                    continue
                key_terms = {
                    item for item in key.split()
                    if item not in ENGLISH_STOP_WORDS and len(item) > 2
                }
                if key_terms and key_terms <= title_terms:
                    continue
                counts[key] += 1
                surfaces.setdefault(key, Counter())[label] += 1

    scored = []
    synopsis_key = keyword_normalise(description)
    for key, frequency in counts.items():
        tokens = key.split()
        length = len(tokens)
        phrase = surfaces[key].most_common(1)[0][0]
        synopsis_boost = 18 if keyword_normalise(phrase) in synopsis_key else 0
        acronym_boost = 5 if any(part.casefold() in {"ai", "agi", "api", "cpu", "gpu", "llm", "ml", "nlp", "rag", "rl"} for part in phrase.split()) else 0
        length_boost = {2: 13, 3: 18, 4: 16, 5: 10}.get(min(length, 5), 4)
        repetition = min(frequency, 12) * (3.4 + length * .62)
        specificity = sum(min(len(token), 13) for token in tokens) / max(length, 1)
        score = repetition + length_boost + synopsis_boost + acronym_boost + specificity
        scored.append((score, frequency, length, key, phrase))

    selected: list[str] = []
    selected_token_sets: list[set[str]] = []
    prefix_counts: Counter[tuple[str, ...]] = Counter()
    for _, _, _, key, phrase in sorted(scored, key=lambda row: (-row[0], -row[1], -row[2], row[3])):
        token_set = set(key.split())
        if any(len(token_set & prior) / max(len(token_set | prior), 1) > .72 for prior in selected_token_sets):
            continue
        prefix = tuple(key.split()[:2])
        if prefix_counts[prefix] >= 2:
            continue
        selected.append(phrase)
        selected_token_sets.append(token_set)
        prefix_counts[prefix] += 1
        if len(selected) >= limit:
            break

    if len(selected) < min(90, limit):
        present = {keyword_normalise(item).strip() for item in selected}
        for _, _, _, key, phrase in sorted(scored, key=lambda row: (-row[0], -row[1], -row[2], row[3])):
            if key in present:
                continue
            selected.append(phrase)
            present.add(key)
            if len(selected) >= limit:
                break
    return selected


def translate_phrases(phrases, cached):
    import torch
    from transformers import MarianMTModel, MarianTokenizer

    translations = {"en": {phrase: phrase for phrase in phrases}}
    for language, values in cached.get("translations", {}).items():
        if language in LANGUAGES and language != "en" and isinstance(values, dict):
            translations[language] = {str(key): str(value) for key, value in values.items()}
    for language in LANGUAGES:
        translations.setdefault(language, {})
    model_groups = (
        ("Helsinki-NLP/opus-mt-en-ROMANCE", (("fr", ">>fr<< "), ("es", ">>es<< "), ("pt", ">>pt<< "), ("it", ">>it<< "), ("ro", ">>ro<< "))),
        ("Helsinki-NLP/opus-mt-en-de", (("de", ""),)),
        ("Helsinki-NLP/opus-mt-en-zlw", (("pl", ">>pol<< "),)),
    )
    torch.set_num_threads(max(1, min(8, os.cpu_count() or 1)))
    ordered_phrases = sorted(phrases, key=lambda value: (value.casefold(), value))
    for model_name, targets in model_groups:
        pending_targets = [
            (language, prefix, [phrase for phrase in ordered_phrases if phrase not in translations[language]])
            for language, prefix in targets
        ]
        pending_targets = [target for target in pending_targets if target[2]]
        if not pending_targets:
            continue
        print(f"Loading local keyword translator {model_name}...", file=sys.stderr, flush=True)
        try:
            tokenizer = MarianTokenizer.from_pretrained(model_name, local_files_only=True)
            model = MarianMTModel.from_pretrained(model_name, local_files_only=True)
        except OSError as error:
            raise RuntimeError(
                f"Keyword model {model_name} is not available locally. Prepare the optional models "
                "as described in dependencies.md. No download was attempted."
            ) from error
        model.eval()
        for language, prefix, pending in pending_targets:
            print(f"Translating {len(pending)} extracted phrases to {language}...", file=sys.stderr, flush=True)
            for offset in range(0, len(pending), 128):
                batch_phrases = pending[offset:offset + 128]
                encoded = tokenizer(
                    [prefix + phrase for phrase in batch_phrases], return_tensors="pt",
                    padding=True, truncation=True, max_length=64,
                )
                with torch.inference_mode():
                    generated = model.generate(**encoded, max_new_tokens=48, num_beams=1)
                outputs = tokenizer.batch_decode(generated, skip_special_tokens=True)
                for phrase, output in zip(batch_phrases, outputs, strict=True):
                    output = re.sub(r"\s+", " ", output).strip(" \t\r\n•–—;,")
                    if not output:
                        raise ValueError(f"Empty {language} translation for {phrase!r}")
                    translations[language][phrase] = output
        del model, tokenizer
    return translations


def main():
    try:
        if sys.version_info < (3, 10):
            raise RuntimeError("Local keyword processing requires Python 3.10 or newer. See dependencies.md.")
        payload = json.load(sys.stdin)
        operation = payload.get("operation")
        if operation not in {"check", "extract", "translate"}:
            raise ValueError("Expected keyword worker operation check, extract, or translate.")
        prerequisites(operation == "translate" or payload.get("translation", False), payload.get("requireModels", False))
        with contextlib.redirect_stdout(sys.stderr):
            if operation == "check":
                result = {"ready": True}
            elif operation == "extract":
                result = [extract_keyword_candidates(
                    record["title"], record["description"], record["sourceText"], record.get("limit", 140),
                ) for record in payload["records"]]
            else:
                result = translate_phrases(set(payload["phrases"]), payload.get("cache", {}))
        print(json.dumps(result, ensure_ascii=False))
        return 0
    except Exception as error:
        print(f"Unable to process local keywords: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
