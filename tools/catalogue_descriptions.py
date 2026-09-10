#!/usr/bin/env python3
"""Install independently reviewed, LLM-authored catalogue descriptions. Never extract prose."""
import argparse
import hashlib
import json
from pathlib import Path
import sys

from build_books import LANGUAGES, editorial_description_problems

ROOT = Path(__file__).resolve().parents[1]
DEFAULT = ROOT / '.book-work/catalogue-descriptions-20260910'

def load(path):
    return json.loads(path.read_text(encoding='utf-8'))

def collect(workspace, require_review=False):
    inventory = {row['id']: row for row in load(workspace / 'inventory.json')}
    records, problems = {}, []
    for index in (1, 2, 3):
        path = workspace / f'descriptions-{index}.json'
        if not path.exists():
            problems.append(f'Missing {path.name}')
            continue
        rows = load(path)
        expected = {row['id'] for row in load(workspace / f'batch-{index}.json')}
        if {row['id'] for row in rows} != expected:
            problems.append(f'Batch {index} is incomplete or has foreign IDs')
        if require_review:
            review_path = workspace / f'review-{index}.json'
            if not review_path.exists():
                problems.append(f'Batch {index} has no independent review')
            else:
                review = load(review_path)
                digest = hashlib.sha256(path.read_bytes()).hexdigest()
                if not review.get('passed') or review.get('draftSha256') != digest or set(review.get('bookIds', [])) != expected:
                    problems.append(f'Batch {index} review is failed, incomplete or stale')
        for row in rows:
            identifier = row['id']
            if identifier in records:
                problems.append(f'Duplicate book: {identifier}')
            records[identifier] = row
            problems.extend(editorial_description_problems({**row, 'shortDescriptionEditorial': {'version': 1}}))
            if not row.get('evidence', {}).get('themes') or not row.get('evidence', {}).get('source'):
                problems.append(f'{identifier}: missing source evidence')
    if set(records) != set(inventory):
        problems.append(f'Coverage: {len(records)}/{len(inventory)} books')
    for language in LANGUAGES:
        seen = {}
        for identifier, row in records.items():
            text = row['shortDescription'].get(language, '')
            if text and text.casefold() in seen:
                problems.append(f'{identifier}/{seen[text.casefold()]}: duplicated {language} description')
            seen[text.casefold()] = identifier
    return inventory, records, problems

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=['check', 'install'])
    parser.add_argument('--workspace', type=Path, default=DEFAULT)
    args = parser.parse_args()
    inventory, records, problems = collect(args.workspace, require_review=args.command == 'install')
    if problems:
        print('\n'.join(problems), file=sys.stderr)
        return 1
    if args.command == 'install':
        report = {'date': '2026-09-10', 'bookCount': len(records), 'languageCount': len(LANGUAGES), 'sentencesPerDescription': 6,
                  'reviews': [load(args.workspace / f'review-{index}.json') for index in (1, 2, 3)], 'books': []}
        for identifier, row in records.items():
            path = ROOT / inventory[identifier]['manifest']
            manifest = load(path)
            manifest['shortDescription'] = row['shortDescription']
            manifest['shortDescriptionEditorial'] = {'version': 1, 'reviewedOn': '2026-09-10', 'sentences': 6, 'basis': 'aboutBook and cited reader context'}
            path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
            report['books'].append({'id': identifier, 'title': inventory[identifier]['title']['en'], 'evidence': row['evidence'],
                'descriptionSha256': hashlib.sha256(json.dumps(row['shortDescription'], ensure_ascii=False, sort_keys=True).encode()).hexdigest()})
        (ROOT / 'tasks/catalogue-descriptions-review.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        print(f'Installed {len(records)} books × {len(LANGUAGES)} reviewed descriptions. Run build_books.py refresh.')
    else:
        print(f'{len(records)} books × {len(LANGUAGES)} descriptions pass structural and duplicate checks.')
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
