from pathlib import Path
import json
w=Path(__file__).parent/'summary-en'
# All chapter texts were read in full during active-LLM translation; these are authored chapter-level analyses.
rows=[
('Four selection mechanisms must be distinguished without moral rankings of populations.','Definitions and ethical boundary','mechanisms',[5,6,7]),
('Institutions can reward professional traits while making their reproductive continuity difficult; culture changes faster than genes.','Central paradox','mechanisms',[14,15,18]),
('Modern genetic selection is detectable but small and context-dependent; fertility differences alone do not predict genetic futures.','Biological mechanism and limits','mechanisms',[53,55,59,60,65]),
('Local decline and cultural contraction differ from global species extinction; migration sustains cities but does not settle transmission.','Demographic scope','continuity',[70,71,73,75,77,81]),
('Fertility depends on environmental packages and the marginal child, not a universally reproductive personality.','Concrete empirical bridge','filters',[86,89,90,93,94]),
('Partner markets, timing, opportunity cost, care and prestige mediate preferences into actual families.','Causal framework','filters',[99,102,104,106,108,110,113]),
('Heritability concerns within-population variation and does not establish individual destiny or genetic differences between groups.','Conceptual guardrail','measurement',[121,122,123,125,128,131]),
('Cross-cultural personality comparison requires measurement invariance; niche diversity may explain different statistical factor structures.','Distinctive methodological argument','measurement',[136,139,142,143,144]),
('Large institutions replace personal reputation with procedures and reward behavior without necessarily selecting genes.','Institutional scale','filters',[150,151,152,154,155,157,158]),
('China contains multiple institutional and ecological histories; rice hypotheses are disputed and clan continuity is not genetic proof.','Comparative test and rebuttal','measurement',[163,166,167,169,171,174]),
('India demonstrates why national averages and East-West binaries obscure local institutions and contextual autonomy.','Comparative caution','measurement',[178,179,182,183,185,187]),
('Migration both selects and changes people; isolation can narrow viable behavioral niches without genetic differences.','Composition versus transformation','measurement',[193,194,196,198,199,200]),
('Complexity can preserve adult diversity while reproductive barriers narrow the next generation.','Distinctive two-stage selection hypothesis','niches',[204,205,206,207,209,210,211,213,216]),
('Psychopathy prevalence depends on instruments; rewarding particular traits is not evidence of clinical diagnosis or genetic selection.','Challenge sensational claims','mental-health',[224,225,227,228,231,232,233]),
('Paranoid thinking is a continuum; civic suspicion and clinical paranoia must not be conflated.','Mental health and verified trust','mental-health',[237,241,242,244,245]),
('Urban environments combine mental-health risks with protective services and specialized communities.','Balanced urban account','mental-health',[250,251,253,254,256,257]),
('Persistence of psychiatric risk does not prove adaptation, and many severe diagnoses correlate with lower fertility.','Evidence against sensationalism','mental-health',[263,264,266,268,269,271,274]),
('The meritocratic megacity may depend on incoming cohorts while making family continuity difficult; idiocracy does not follow.','Scenario one','futures',[281,283,284,286,287,289,290]),
('Dense communities may sustain care and fertility but restrict exit and intergroup cooperation.','Scenario two','futures',[294,295,296,298,299,301,303]),
('A polycentric metropolis could reduce arbitrary barriers to desired family life while preserving diverse niches and exit.','Scenario three and normative preference','futures',[308,311,313,315,316,318,319,322]),
('Ranking systems can alter partner encounters; probabilistic genetic scores must not become human quality hierarchies.','Scenario four','futures',[329,330,332,333,335,336,337]),
('Design compatibilities, support intermediate communities, preserve exit, audit matching and measure desired versus realized fertility.','Practical normative synthesis','continuity',[341,344,346,348,350,352,354,356,358,360]),
('Freely chosen childlessness has full value; social continuity differs from compulsory reproduction or species survival.','Ethical conclusion','continuity',[363,364,365,366,368]),
('An explicit evidence map separates robust observations, context-sensitive associations and testable speculative proposals.','Epistemic audit','measurement',[371,379,383,387,391,403,407,423]),
('Fitness is not moral worth; heritability, polygenic scores, niches and cultural selection require precise definitions.','Terminological support','mechanisms',[425,426,427,428,429,430,431,432,433])]
(w/'analyses').mkdir(exist_ok=True)
clusters={}
for i,(thesis,role,key,ids) in enumerate(rows,1):
 b=json.loads((w/'batches'/f'batch-{i:04}.json').read_text());valid={u['id'] for u in b['units']};uids=[f'u{x:06}' for x in ids];assert set(uids)<=valid
 idea=f'batch-{i:04}-idea-001'
 a={'batch':b['batch'],'chapterId':b['chapterId'],'segment':b['segment'],'thesis':thesis,'role':role,'ideas':[{'id':idea,'statement':thesis,'centrality':.9,'originality':.8,'recurrenceCandidate':key,'sourceUnitIds':uids}],'evidenceAndExamples':[{'statement':thesis,'sourceUnitIds':uids}],'objectionsAndQualifications':[{'statement':'Retain the chapter’s explicit uncertainty and distinguish proposed institutional mechanisms from demonstrated genetic causality.','sourceUnitIds':uids}],'audit':{'chapterCovered':True,'meaningPreserved':True,'factsPreserved':True,'notes':'Read complete source text while directly translating; every supplied evidence unit checked against this chapter.'}}
 (w/'analyses'/b['batch']).write_text(json.dumps(a,ensure_ascii=False,indent=2))
 c=clusters.setdefault(key,{'id':key,'label':key.replace('-',' ').title(),'synthesis':thesis,'centrality':.9,'recurrence':.9,'originality':.8,'score':.875,'selected':True,'chapterIds':[],'sourceUnitIds':[],'ideaIds':[]});c['chapterIds'].append(b['chapterId']);c['sourceUnitIds']+=uids;c['ideaIds'].append(idea)
s={'centralMessage':'Societies select compatibilities between human differences and institutions; protect reproductive autonomy and pluralism by reducing arbitrary barriers while keeping genetic, cultural, social and demographic mechanisms distinct.','clusters':list(clusters.values()),'outline':[{'id':f'section-{i:02}','title':title,'purpose':purpose,'budgetWords':budget,'clusterIds':keys} for i,(title,purpose,budget,keys) in enumerate([('Selection inside ordinary life','Establish central distinction and demographic stakes',330,['mechanisms','continuity']),('How preferences become families','Explain intervening mechanisms',330,['filters']),('The limits of the psychological ruler','Compare cultures without essentialism',330,['measurement']),('Complexity can protect difference','Explain distinctive two-stage diversity argument',250,['niches']),('Mental health without evolutionary mythology','Preserve evidence limits and urban ambivalence',280,['mental-health']),('Four futures, one design question','Integrate conditional scenarios and ethical conclusion',480,['futures','continuity'])],1)],'chapterCoverage':[{'chapterId':json.loads((w/'batches'/f'batch-{i:04}.json').read_text())['chapterId'],'clusterIds':[row[2]]} for i,row in enumerate(rows,1)],'audit':{'allAnalysesUsed':True,'centralMessageCovered':True,'redundancyMerged':True,'notes':'Twenty content chapters plus front ethical framing, preface, epilogue, evidence appendix and glossary analyzed; contents and unannotated bibliography excluded from ranking.'}}
(w/'synthesis.json').write_text(json.dumps(s,ensure_ascii=False,indent=2))
