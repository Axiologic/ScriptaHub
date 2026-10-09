import hashlib
import json
from pathlib import Path
import sys
sys.path.insert(0, str(Path.cwd()))
from tools.build_books import keyword_normalise, keyword_source_text

root = Path('.book-work/echoesfrombeyondtheveil-v1-49afb53aab7f/book')
manifest_path = root / 'manifest.json'
reader = root / 'en/short_content.html'
source = keyword_normalise(keyword_source_text(reader))
phrases = [
    'New Athens', 'Elara Venn', 'Zephyr Kane', 'Administrator Thorne', 'ARIA',
    'Cosmic Wardens', 'Global Security', 'Global Institute of Cosmology',
    'Archives of Antiquity', 'Sumerian tablets', 'Hermetic texts',
    'Gnostic gospels', 'secret societies', 'quantum research',
    'quantum entanglement', 'quantum entanglement simulation',
    'quantum fluctuations', 'anomaly', 'crystalline device', 'crystal',
    'portal', 'simulated universes', 'simulated worlds', 'quantum',
    'multiversal rebellion', 'collective awakening', 'collective resistance',
    'private doubt', 'imposed illusion', 'designed construct',
    'familiar reality', 'perfected future', 'utopia', 'perfect morning',
    'perfect surface', 'smart walls', 'holograms', 'maglevs',
    'neural assistant', 'mood-enhancing drinks', 'pills', 'advertisements',
    'surveillance', 'official control', 'routine concern',
    'unstated consequence', 'designated areas', 'mechanical voice',
    'rehearsed assurances', 'forced smiles', 'practiced smiles',
    'mirror of reality', 'fractured mirror', 'impossible dark spaces',
    'other worlds', 'timelines', 'immense beings', 'powerful beings',
    'shifting entities', 'insignificant experiment', 'research problem',
    'ritual symbol', 'hidden structure',
    'recurring signs', 'fictional mystery', 'religion and myth',
    'myth', 'Global Security officers', 'neural assistant ARIA',
    "humanity's technological success", 'technological success',
    "city's perfect surface", 'pattern in quantum fluctuations',
    'sterile room', 'hidden laboratory', 'surveillance as routine concern',
    'distortions in the sky', "utopia's facade",
    'records of secret societies', 'archive logs', 'supposed safety',
    'old texts', 'countless simulated universes',
    'destruction of their inhabitants', 'Wardens’ power',
    'cracks appear', 'collective resistance',
    'comfort of New Athens’ illusion', 'imposed illusion',
    'crystal shatters', 'apparent order', "Wardens' forms",
]
phrases = list(dict.fromkeys(phrases))
missing = [p for p in phrases if keyword_normalise(p) not in source]
if missing:
    raise SystemExit(f'Missing phrases in source ({len(missing)}): {missing}')
if len(phrases) != 90:
    raise SystemExit(f'Expected 90 reviewed phrases; got {len(phrases)}')
manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
manifest['keywordReview'] = {
    'sourceHash': hashlib.sha256(reader.read_bytes()).hexdigest(),
    'phrases': phrases,
    'basis': 'Reviewed discovery terms occurring in the four-chapter English ten-minute fiction reader.',
}
manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print('Reviewed 90 source-derived keywords')
