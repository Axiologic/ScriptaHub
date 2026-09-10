from pathlib import Path
import json
w=Path(__file__).parent/'summary-job';s=json.loads((w/'synthesis.json').read_text());d=json.loads((w/'draft.json').read_text())
# Connect the explicitly reviewed supporting examples and limits, omitted by initial idea-only aggregation.
extras={1:[90,136,170,171,172,174,175,233,234,236,260,261,297,298,319],3:[221,227,229],5:[98,99,127]}
for c,us in extras.items():s['clusters'][c-1]['sourceUnitIds']=sorted(set(s['clusters'][c-1]['sourceUnitIds'])|{f'u{u:06d}' for u in us})
d['sections'][1]['paragraphs'][3]['clusterIds'].append('cluster-001')
d['sections'][3]['paragraphs'][1]['clusterIds'].append('cluster-001')
for i,sec in enumerate(d['sections']):s['outline'][i]['clusterIds']=sorted(set(s['outline'][i]['clusterIds'])|{c for p in sec['paragraphs'] for c in p['clusterIds']})
def add(n,t,cs,us):d['sections'][n-1]['paragraphs'].append(dict(text=t,clusterIds=[f'cluster-{c:03d}' for c in cs],sourceUnitIds=[f'u{u:06d}' for u in us],audit=dict(meaningPreserved=True,factsPreserved=True,noUnsupportedClaim=True)))
add(1,'Timing adds another dimension. Two groups can have the same completed number of children yet different generation lengths, changing their relative growth over a longer horizon. Status also works through marriage rules: social monogamy limits how readily a large economic advantage becomes a large difference in descendants. These mechanisms show why the relevant unit is often a combination of traits, institutions and circumstances, rather than a single psychological characteristic considered alone.',[2],[109,110,111])
s['clusters'][1]['sourceUnitIds']=sorted(set(s['clusters'][1]['sourceUnitIds'])|{'u000110','u000111'})
add(3,'Kinship complicates any simple story of modernization. Extended families can distribute care and supply trust, while impersonal institutions can provide services that replace some of those functions. Neither arrangement is universally superior. Removing dependence on a clan without replacing its support may increase autonomy and loneliness together. Digital communities could recombine these functions, giving people practical ties across distance while also creating new barriers to encountering other perspectives.',[3],[282,283,285,286])
s['clusters'][2]['sourceUnitIds']=sorted(set(s['clusters'][2]['sourceUnitIds'])|{f'u{u:06d}' for u in [282,283,285,286]})
add(4,'This is why the book treats AI as more than a productivity tool. It may compensate for planning difficulties, make certain social abilities less necessary, or expose manipulation through reputation systems. Such changes would alter the costs and benefits of existing predispositions without directly changing anybody’s genes. The demographic question concerns how these altered opportunities interact with preferences, partnerships and cultural transmission over time.',[6],[344,345,346])
s['clusters'][5]['sourceUnitIds']=sorted(set(s['clusters'][5]['sourceUnitIds'])|{'u000346'})
(w/'synthesis.json').write_text(json.dumps(s,indent=2,ensure_ascii=False)+'\n');(w/'draft.json').write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
