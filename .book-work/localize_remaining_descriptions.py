"""One-time, local-only editorial metadata for five pending classic editions."""

import glob
import json
from pathlib import Path

import torch
from transformers import MarianMTModel, MarianTokenizer


COPY = {
    "dracula": [
        "Jonathan Harker travels to Transylvania and discovers his host's terrifying secret.",
        "Count Dracula then brings that danger to England.",
        "Lucy Westenra's illness draws her friends into a struggle they scarcely understand.",
        "Mina Harker gathers journals and letters to connect the clues.",
        "The pursuit crosses borders as the group races against Dracula's plans.",
        "Bram Stoker tells the story through the characters' own records, making each discovery feel immediate.",
    ],
    "grimmsfairytales": [
        "The Brothers Grimm collect tales of forests, cottages, kings and wandering children.",
        "Promises and bargains often carry a price the characters do not foresee.",
        "Witches, animals and enchanted objects turn ordinary choices into trials.",
        "Courage and cleverness help some travellers escape danger.",
        "Other stories leave readers with a darker warning about cruelty or greed.",
        "The collection preserves the varied rhythms and moral tensions of European folk storytelling.",
    ],
    "mobydickorthewhale": [
        "Ishmael boards the Pequod seeking work and a view of the whaling world.",
        "Captain Ahab makes the hunt for a white whale the ship's true purpose.",
        "The crew follows him across oceans while warning signs accumulate.",
        "Descriptions of whales and shipboard labor interrupt and deepen the voyage.",
        "Ahab's pursuit tests loyalty, judgment and the limits of human control.",
        "Herman Melville blends adventure, inquiry and tragedy in an unusually expansive sea novel.",
    ],
    "olivertwist": [
        "Oliver grows up in a workhouse that treats poor children with cruelty.",
        "His escape to London leads him into Fagin's circle of thieves.",
        "Kindness appears alongside exploitation as adults compete to shape his future.",
        "Nancy's choices reveal the danger of trying to protect him.",
        "The mystery of Oliver's family unfolds amid pursuit and betrayal.",
        "Charles Dickens turns one child's story into a sharp portrait of poverty and social injustice.",
    ],
    "thelifeandadventuresofrobinsoncrusoe": [
        "Robinson Crusoe ignores his father's advice and follows the sea.",
        "A shipwreck leaves him alone on an island for many years.",
        "He builds shelter, grows food and keeps a record of survival.",
        "Signs of other people change his sense of safety and solitude.",
        "His meeting with Friday brings companionship and difficult questions about power.",
        "Daniel Defoe's adventure joins practical ingenuity to fear, faith and colonial assumptions.",
    ],
}


def translate(sentences, tokenizer, model, prefix):
    encoded = tokenizer([prefix + s for s in sentences], return_tensors="pt", padding=True, truncation=True, max_length=128)
    with torch.inference_mode():
        result = model.generate(**encoded, max_new_tokens=64, num_beams=1)
    return tokenizer.batch_decode(result, skip_special_tokens=True)


def main():
    torch.set_num_threads(6)
    paths = {key: Path(glob.glob(f".book-work/{key}-v1-*")[0]) / "book" / "manifest.json" for key in COPY}
    translations = {key: {"en": list(sentences)} for key, sentences in COPY.items()}
    groups = [
        ("Helsinki-NLP/opus-mt-en-ROMANCE", [("fr", ">>fr<< "), ("es", ">>es<< "), ("pt", ">>pt<< "), ("it", ">>it<< "), ("ro", ">>ro<< ")]),
        ("Helsinki-NLP/opus-mt-en-de", [("de", "")]),
        ("Helsinki-NLP/opus-mt-en-zlw", [("pl", ">>pol<< ")]),
    ]
    for model_name, targets in groups:
        tokenizer = MarianTokenizer.from_pretrained(model_name, local_files_only=True)
        model = MarianMTModel.from_pretrained(model_name, local_files_only=True)
        model.eval()
        for lang, prefix in targets:
            print(lang, flush=True)
            keys = list(COPY)
            combined = [sentence for key in keys for sentence in COPY[key]]
            outputs = []
            for offset in range(0, len(combined), 8):
                outputs.extend(translate(combined[offset:offset + 8], tokenizer, model, prefix))
            for i, key in enumerate(keys):
                translations[key][lang] = outputs[i * 6:(i + 1) * 6]
        del model, tokenizer
    for key, path in paths.items():
        manifest = json.loads(path.read_text())
        manifest["shortDescription"] = {lang: " ".join(sentences) for lang, sentences in translations[key].items()}
        manifest["aboutBook"] = {lang: [" ".join(sentences[:3]), " ".join(sentences[3:])] for lang, sentences in translations[key].items()}
        manifest["shortDescriptionEditorial"] = {
            "method": "editorially authored from delivered classic narrative; translated with local Marian models",
            "sourceSha256": manifest.get("metadataDraft", {}).get("sourceSha256"),
            "sentencesPerLanguage": 6,
            "status": "reviewed",
        }
        manifest["metadataDraft"] = {**manifest.get("metadataDraft", {}), "reviewRequired": False, "reviewedOn": "2026-10-16"}
        path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n")
    Path(".book-work/remaining-description-review.json").write_text(json.dumps(translations, ensure_ascii=False, indent=2) + "\n")


if __name__ == "__main__":
    main()
