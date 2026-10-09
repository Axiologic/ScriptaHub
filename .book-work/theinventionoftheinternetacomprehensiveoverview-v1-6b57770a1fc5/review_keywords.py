import hashlib
import json
import sys
from pathlib import Path

sys.path.insert(0, 'tools')
from build_books import keyword_normalise, keyword_source_text, SHELF_CATEGORIES

root = Path('.book-work/theinventionoftheinternetacomprehensiveoverview-v1-6b57770a1fc5/book')
source = root / 'en/short_content.html'
path = root / 'manifest.json'
manifest = json.loads(path.read_text())
phrases = [
 'research network', 'global medium', 'life without the internet', 'institutions',
 'protocols', 'connectivity', 'conceptual vision', 'mathematical work',
 'engineering', 'public funding', 'cooperation', 'online services',
 'libraries', 'telephone booths', 'typewriters', 'scheduled television',
 'search', 'messaging', 'digital documents', 'streaming',
 'communication', 'access to knowledge', 'constant alerts', 'data collection',
 'dependence on networks', 'privacy', 'attention', 'distant collaboration',
 'rapid information sharing', 'Cold War', 'Sputnik', 'computer research',
 'J. C. R. Licklider', 'interconnected computers', 'data and programs',
 'collaboration tools', 'Paul Baran', 'distributed communications system',
 'message blocks', 'alternative routes', 'Donald Davies', 'packet switching',
 'data networks', 'packet', 'Leonard Kleinrock', 'mathematical models',
 'network traffic', 'UCLA laboratory', 'ARPANET', 'LOGIN',
 'Vint Cerf', 'Bob Kahn', 'TCP/IP', 'network of networks',
 'academic habit', 'exchanging results', 'iteration', 'shared computing',
 'hardware', 'research institutions', 'Bolt Beranek and Newman',
 'Interface Message Processors', 'packet-routing machines', 'network nodes',
 'Stanford Research Institute', 'Email', 'remote login', 'Telnet',
 'file transfer', 'resource sharing', 'Network Control Protocol',
 'local area networks', 'UNIX-based computing', 'CSNET', 'BITNET',
 'scalable', 'interoperable protocols', 'reliable packet transmission',
 'different hardware', 'National Science Foundation', 'NSFNet',
 'supercomputer centers', 'regional networks', 'academic backbone',
 'commerce', 'education', 'social platforms',
 'telemedicine', 'essential infrastructure', 'net neutrality',
]
text = keyword_normalise(keyword_source_text(source))
shelf = {keyword_normalise(label).strip() for localized in SHELF_CATEGORIES.values() for label in localized['en'].split('|')}
missing = [phrase for phrase in phrases if keyword_normalise(phrase) not in text]
collisions = [phrase for phrase in phrases if keyword_normalise(phrase).strip() in shelf]
print('count',len(phrases),'distinct',len(set(phrases)),'missing',missing,'shelf',collisions)
if len(phrases) != 90 or len(set(phrases)) != 90 or missing or collisions:
    raise SystemExit(1)
manifest['keywordReview'] = {'sourceHash': hashlib.sha256(source.read_bytes()).hexdigest(), 'phrases': phrases}
path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')
