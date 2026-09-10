from pathlib import Path
import json,hashlib,re
p=Path('presentations/the-museum-of-good-reasons');r=p/'review-revision';t=(p/'source/source.txt').read_text()
scenes=[('What the lamp omits',[
'The Museum of Good Reasons makes true explanations unsettling by showing what they leave outside.',
'This philosophical novel follows Mara, hired to catalogue a museum that justifies disappearance.',
'Her first test concerns a lamp described as creating light from darkness.',
'She notices the oil that the label places outside the exhibit.',
'The director asks where her own explanation chooses to stop.',
'That exchange invites readers to examine framing without pretending complete descriptions are possible.'
]),('Whose route is shared',[
'An apparently generous umbrella becomes another test of what official language permits.',
'Mara reads two accounts of the same walk through rainy streets.',
'One describes offered companionship; the other describes repeated attempts to leave.',
'Her work includes physically retracing the route from each person’s position.',
'The novel makes perspective a material experience, not merely a contest between persuasive sentences.'
]),('Seven metres away',[
'A moved park bench has better shade and still supports sitting.',
'The official reply uses those facts to answer a widower’s complaint.',
'But his wife’s death there made its location matter.',
'Mara cannot correct the reply simply by finding a false statement.',
'The scene shows why this novel gives ordinary objects histories worth following.'
]),('A slower kind of attention',[
'Later galleries bring these tensions into family life, work, care, and public institutions.',
'They also challenge Mara’s temptation to turn affected people into evidence for her own position.',
'The prologue offers both a gradual museum route and an independent final chapter.',
'For the institutional mystery, begin with The Lamp’s Label and follow the omissions.',
'Read to notice how an explanation can remain accurate while making loss disappear.'
])]
quotes=[
'The Museum of Good Reasons had been built to prove that nothing had ever truly been taken.',
'The employment test is simple. Correct the label.',
'Its reservoir was concealed inside the pedestal. A very fine pipe descended through the marble.',
'The oil is part of the museum\'s infrastructure.',
'First rule: no label can contain the whole context.',
'The umbrella was green, with a wooden handle and two broken ribs.',
'Mara first walked Pavel\'s line. From his perspective, the deviations were small, almost natural. Then she walked Mirena\'s.',
'The first file concerned a park bench moved seven meters to make room for a statue.',
'The museum\'s reply explained that the bench was municipal property, that its new location offered better shade, and that a distance of seven meters did not affect the function of sitting.',
'Sitting was not its only function.',
'I have not asked anyone in the archive whether they want to be brought out.',
'The ordinary entrance begins with the lamp and proceeds through the museum room by room.',
'It can be read alone.'
]
evidence=[]
for q in quotes:
 a=t.index(q);start=len(t[:a].encode('utf-16-le'))//2;evidence.append({'quote':q,'start':start,'end':start+len(q.encode('utf-16-le'))//2})
source={'edition':'edition-1','sourceHtmlSha256':hashlib.sha256(Path('docs/books/the/museum/of/good/reasons/bk-0db7c8ba679b41bb/en/full_content.html').read_bytes()).hexdigest(),'sourceTextSha256':hashlib.sha256((p/'source/source.txt').read_bytes()).hexdigest(),'freshFullChaptersRead':[1,2,3,7,9,19],'otherReading':['Front matter and Two Entrances prologue','Complete actual old56-line script and full chapter/section map','Full epilogue Uninventoried Light','Final chapter conclusion from UTF16 offset230000 to242202, not the complete67k-character final chapter'],'scope':'Selected complete chapters plus explicit final/conclusion coverage, not a fresh every-word reading of the whole novel.','evidence':evidence}
(r/'source-evidence.json').write_text(json.dumps(source,indent=2,ensure_ascii=False)+'\n')
(r/'proposed-script.txt').write_text('\n\n'.join(title+'\n'+'\n'.join(lines) for title,lines in scenes)+'\n')
(r/'proposed-scenes.json').write_text(json.dumps([{'title':title,'lines':lines} for title,lines in scenes],indent=2,ensure_ascii=False)+'\n')
text='''# The Museum of Good Reasons — proposed complete revision

Status: complete 22-line draft awaiting independent script/art review **before voice or public changes**. Existing published film remains unchanged. Target measured 2–3 minutes with local Piper, real 1.45-second ordinary gaps and longer transitions; cut copy if measurement exceeds 180 seconds, never accelerate.

## Narrative spine

This philosophical novel asks how true explanations can make a person's loss disappear; Mara's work of correcting museum labels makes that problem material through ordinary objects and contested histories; following her gives readers a more patient way of examining what an account includes, excludes, and permits. The reading experience combines institutional mystery, precise objects, dry humor and ethical self-correction. No mystery's final solution is disclosed.

The hook names the novel and its reading value in the first two sentences. The lamp establishes framing, the umbrella makes perspective physically consequential, the bench demonstrates that finding factual error cannot settle every loss, and the closing restores the whole book's scope and a specific starting point. The film deliberately moves from the opening to chapter2 and then returns to a first-chapter file; it does not claim that the bench follows the umbrella in the novel's chronology.

## Complete spoken draft

'''
for i,(title,lines) in enumerate(scenes):
 text+=f'### Scene {i+1}: {title}\n\n'+'\n'.join(f'{j+1}. {line}' for j,line in enumerate(lines))+'\n\n'
text+='''## Original visual identity and staged action

Quiet ivory, deep aubergine, brass gold, rain teal and cinnabar accents. Material differences carry meaning: hard polished museum plinth, fine oil pipe, wet green cloth, worn park wood and manuscript paper. Backgrounds remain flat and scenery is restricted to what the current argument needs. One strong player heading per scene, bundled Red Hat Display/Text, caption-safe physical action above y550. No decorative frame stacks, competing slogans or repeated person-plus-three-icons staging. Pale physical floors keep dark legs in every theme.

**Cast and interpretation.** Mara remains one stable aubergine-jacketed young adult with dark bobbed hair and cream collar; source does not specify these features, so they are consistent illustrative casting, not claimed descriptions. Orven has the source's short white hair, black suit, copyist's hands and ink-stained middle finger. The umbrella is green with wooden handle and two visibly broken ribs. Pavel and Mirena are distinct illustrative adults with coats appropriate to rain; casting is invented. Bench worker/widower reenactment is explicitly conceptual staging of a file, not an additional named plot event. No late-source portrait, watch, archive code, Architect, clinical outcome or opened window appears.

### Scene1 — an exhibit with a missing dependency

Composition: medium-close museum examination, not a presenter beside symbols. Small cup-size brass lamp on a waist-high marble pedestal. Mara stands close enough that her gloved hand/pencil meets the actual label; Orven faces her across the pedestal with naturally bent arm and pointing hand, not a torso-spanning sleeve. Cup-size lamp remains proportional to actors. One short physical label reads “Self-sufficient lamp”. The flame has a quiet meaningful flicker; no glow-cloud decoration.

Lines1–2 show Mara reading, then looking from label to flame with curiosity. Line3 draws attention to the label as Orven presents the test with an open palm. Line4 temporarily uses an explicitly illustrative cutaway: a bounded portion of the pedestal's front slides aside to expose the thin descending pipe and concealed oil reservoir; pipe pulse or two droplets visibly travel toward the lamp, showing what sustains it. This is an explanatory camera/cutaway overlay, **not the installation of a transparent pipe in the source's later reform**. Line5 Orven shifts gaze along the pipe toward off-screen supply and then back to Mara, who pauses the pencil. Line6 the camera returns to the bounded exhibit; the unresolved outer extent of the pipe remains cropped by the physical scene. No claim that a reservoir contains the whole context.

Emotional arc: curiosity → small discovery → complication → thoughtful restraint. Hand movement has anticipation, contact and rest. Do not animate writing a full source quotation at caption speed.

Actual checks: lamp reservoir remains below bowl; actual pipe endpoints meet reservoir/lamp; cutaway reveals without physically supplying new fuel; Mara's palm/pencil stays within reach of label; Orven's arm has natural length; all label pixels readable in all themes.

### Scene2 — the museum's projected street route

Composition changes to an oblique/overhead floor-plan demonstration with the actual wet umbrella exhibit at the far left and three clearly joined street intersections across the floor. The source says the museum projects routes onto its floor and Mara walks each viewpoint. Here Mara is shown at a normal readable scale, with the museum floor large enough to retrace physically. There are no tiny floating heads or decorative network lines: every line is a street or one person's route.

Line1 focuses on the green umbrella and its physical condition. Line2 two short file labels “Pavel” and “Mirena” are visible on adjacent single pages beneath it; no enormous prose. Line3 changes the focus to the floor: a pale exit at each junction remains visible, while the selected shared green route follows a turn. The second reconstruction shows Mirena's attempted separation and Pavel's following path, with a short separation widening before the following path reduces it. These route traces represent the disputed accounts being examined, not a neutral documentary view of the historical walk. Prefer a sequential comparison to simultaneous duplicate casts. Line4 Mara's feet actually traverse first one path and then the other, turning torso/gaze with movement; her feet remain on the physical floor. Line5 she stops at the place where an alternative route diverges, putting the contrast into one held image. The exhibit remains peripheral rather than three illustrations fighting for focus.

If two reconstructed walkers are needed for intelligibility, use full supported bodies at sufficient scale, not head icons; clear Mara's route animation before this insert and identify it as the accounts' reconstruction. No stalking climax, fate, hidden note, later clue or revised final label is shown.

Emotional arc: light ironic curiosity → recognition of unequal freedom → held discomfort. Rain appears only over the physical umbrella or reconstruction; it is not a patterned background.

Checks: routes have three actual intersections; a genuinely diverging alternative remains possible; feet follow authored coordinates without skating; joined arms hold an umbrella handle only where it is carried; no route passes through labels/captions.

### Scene3 — an unchanged function, a changed place

Composition: wide low park strip, deliberately unlike the museum floor. A bench initially sits beside a modest physical spot in the ground; two maintenance workers move it toward a shade tree to make room for a statue, matching the first-chapter file. The bench is moved through an illustrated seven-metre span, indicated briefly by one ground-level measurement with clear endpoints. The screen is not an engineering scale model. Workers visibly grasp opposite ends, lift slightly, carry, and settle all legs onto the ground; never make a heavy bench glide by itself.

Lines1–2 end with the bench supported in the new shade, while a widower remains near the original location holding his complaint sheet. The official reply's two visible factual fields are “Better shade” and “Same seating”; avoid presenting these as film slogans. Line3 focuses on his relation to the original empty place; his hand lowers, gaze and posture soften. No corpse, ghost, invented flashback of the death or fictitious portrait. The loss is communicated by the narrated source detail and the distance between person and relocated place. Line4 cut back to Mara holding the file rather than replacing the entire park with another disconnected icon; her pencil pauses above the two factually correct fields. Line5 settle on her attention returning to the man's letter. Do not turn this into a tidy restoration or claim that a better label returns the place.

This is a conceptual reenactment of the file, not a scene in which the novel explicitly says Mara visits the park; disclose that in editorial provenance, not public narration. Maintenance worker identities, tree shape and bench construction are illustrative.

Emotional arc: practical improvement → recognition of grief → quiet unresolved attention. No sentimentality, celebratory repair or implied final judgment.

Checks: actual hand-to-bench contact throughout lift and set-down, bench feet meet surface afterward; tree shade corresponds to new position; original and new places are distinct; seven-metre notation never claims exact stage scale; complaint and true factual statements stay readable.

### Scene4 — read beyond the first label

Composition: intimate reading view, not a grand museum facade or trophy book. A supported open volume on a reader's lap enters after the bench file clears; cropped body, forearms and both hands visibly support the two lower page corners. A plain upholstered chair provides leg/arm support, distinct from the prior park bench. Mara is no longer a presenter; this is an illustrative prospective reader.

Line1 two actual part headings on page tabs point to the source's later household and time galleries, with readable selected titles “Gifts” and “Machines that create time”; these label book structure, not claimed substantive conclusions. Line2 the reader pauses turning a page, with fingers still contacting the paper; no accusing or angelic expression. Line3 turns back to the prologue's actual “Two Entrances” page. Show two lines of navigation only: “The Lamp's Label” and “Whale Within Whale”, never illustrations that disclose the final chapter. Line4 the reader selects the ordinary entrance with a physical page turn, settling on the opening chapter. Line5 the held final composition is the first lamp drawing as an illustrative page vignette and the actual chapter title; a hand rests beside a generous clear margin. Do not print an invented concluding quotation or portray an outcome from the novel.

Emotional arc: broader curiosity → self-reflection → freedom to choose → patient invitation. Source explicitly permits the independent final chapter; the film recommends the ordinary beginning for its institutional mystery. It does not equate a clinical/pharmacological episode with verified cosmology.

Checks: book rests on lap throughout; both support hands have connected forearms, natural reach and paper contact; each page/navigation text appears alone at readable size; no competing heading/caption collision; the final chapter is named without visualized revelations.

## Evidence and reserved material

Full exact source/hash/UTF16 spans in `source-evidence.json`. Fresh complete chapters read:1,2,3,7,9,19; full prologue/epilogue; complete existing film script and chapter map; final chapter conclusion read from offset230000 through242202. This is bounded source review, not a fresh end-to-end whole-book claim. One cover image exists, no interior diagrams are used; all current art is original explanatory staging.

Protected: the identity/history of the watch, father's role, bridge/inspection revelations, archive key/closed-series discoveries, Teo's accident connection, private family developments, clinical drug sequence and ambiguous ontological status, late gallery reforms, window/key resolution, fates/deaths and final ascent. The prologue publicly supplies the alternate entrance title; naming it is permitted without describing its payoff.

Reading gain is positive: the lamp exposes a chosen boundary, the umbrella makes that choice consequential for action, and the bench demonstrates that correct facts can omit a relevant function. This is not a lecture proving that all explanation or all efficiency is malicious. Later chapter scope shows that Mara's own interpretive habits are also tested.
'''
text=text.replace('complete 22-line','complete 21-line')
(r/'SCRIPT-AND-ART.md').write_text(text)
(r/'progress.json').write_text(json.dumps({'status':'Complete21-line source-grounded proposal awaiting independent review before voice','publicUnchanged':True,'newVoiceGenerated':False,'next':['Root script/art review','Only after approval, preserve current film/work then synthesize changed lines and stage original art'],'sentences':sum(len(x[1]) for x in scenes),'sourceEvidence':'source-evidence.json'},indent=2)+'\n')
print('sentences',sum(len(lines) for _,lines in scenes));print('word counts',[len(re.findall(r"[\w]+(?:[’'-][\w]+)*",l)) for _,ls in scenes for l in ls]);print('evidence',len(evidence))
