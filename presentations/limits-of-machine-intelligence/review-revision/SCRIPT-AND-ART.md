# Limits of Machine Intelligence — replacement introduction draft

Status: script and artwork approved by root, including the explicit changed-controller sentences; installed after all-theme silent QA at156168ms.

Purpose: an English, narrated, 2–3 minute invitation to read this exploratory book. The opening names the book, its practical problem and a specific reading gain. The rest pays off that gain through one bounded verification example, a wider proof obligation and the book's own code-generation permission example.

Story spine: a ten-step check can be completely correct and still fail to authorize an eleventh step; this book asks how explicit boundaries connect mathematical limits, practical verification and the authority given to AI systems.

Expected length: 22 single-sentence clips, 262 words, with 1.25–1.4 seconds between sentences and 2 seconds at scene changes; target 145–170 seconds. Final duration must come from measured local Piper clips, not this estimate. No audible background playback.

## Spoken script

### 1. Limits of Machine Intelligence

1. Limits of Machine Intelligence asks what a machine can justify before its next action.
2. A check can cover ten steps without settling every possible future.
3. This exploratory book connects mathematical limits with the permissions we give working systems.
4. You learn to separate a useful guarantee from an unsupported extension.

### 2. Ten steps checked

1. Imagine a small controller whose counter can increase at each step.
2. Our teaching example checks every modeled path through its first ten steps.
3. No forbidden state appears within that horizon, so the bounded check succeeds.
4. An eleventh step can cross the limit that the original question excluded.
5. The book distinguishes that precise local result from a promise about unlimited operation.

### 3. A wider guarantee

1. A counterexample can refute a safety claim with one concrete execution.
2. Proving wider safety needs more than a longer collection of successful runs.
3. Now change the controller so its counter cannot increase beyond ten.
4. The book compares proofs of such limits with tests and observations during operation.

### 4. Permission follows evidence

1. Its AI example separates proposing a code change, testing it, and deploying it.
2. A model may suggest freely while execution remains inside a restricted sandbox.
3. Deployment requires its own stronger check or human authorization.
4. When required evidence is missing, the system must withhold that permission.

### 5. Read the boundary

1. The chapters revisit impossibility theorems, then examine the practical evidence engineers can obtain.
2. Outfinitism names the author's proposed discipline for declaring limits and checking their extension.
3. Its value beyond existing verification methods remains a research question.
4. Start with Practical Warrant Beyond Total Decision to follow these distinctions in detail.
5. Read this book to ask exactly which action a guarantee actually supports.

## Source and example boundaries

Source: existing canonical extraction at `../source/source.txt`, `../source/sections.json` and `../source/extraction.json`, edition-1. These existing source files are read only. No claim that this independent revision manually reread every word of the book: review covered its full section map, complete abstract, substantive bounded-verification sections and the concluding account of research status, with targeted supporting passages.

- Source-6, ABSTRACT: a deployed AI may need a certificate for its finite domain, precision, horizon and authority; practical methods obtain bounded/model-relative/trace-relative evidence. Supports opening and whole spine.
- Source-9, The Impossibility Trap and the Moving Frontier: global impossibility can coexist with a local certificate. Supports the distinction retained throughout.
- Source-20, Chapter 5 continuation: bounded model checking searches for a bad trace of length at most k; unsatisfiability means no modeled bad trace exists within k steps, not automatically unbounded safety. A concrete counterexample refutes the modeled safety property. Supports scene 2 and scene 3, sentences 1–2.
- Source-20 also explains that induction or an invariant can sometimes lift a bounded result, relative to a model. The scope must be justified, not hoped for. Supports scene 3, sentence 3.
- Source-21–23: abstraction, counterexample-guided refinement, proof-carrying code and runtime monitoring obtain different kinds of conditional evidence. Supports scene 3, sentence 4.
- Source-23: a code-generating model may propose broadly, test in a sandbox under narrower conditions and deploy only through a proof-carrying or human-approved gate. Required certificates must refer to the deployed artifact; unknown results require conservative fallback. Supports scene 4.
- Source-36, concluding research discussion: the possible contribution is a common epistemology of movable barriers; usefulness beyond established vocabulary needs formal or empirical demonstration. Supports the single research-status sentence in scene 5.

The counter is an **original, explicitly introduced toy model**, not a reported source case, experiment or deployed safety system. It instantiates the source's bounded-model-checking distinction. Definition for the production ledger: initial counter c=0; at each transition it may hold or increment; forbidden state c>10. Every path of at most ten transitions stays at c≤10; a path of eleven increments reaches c=11. Scene 3 introduces a visibly changed controller with a guard permitting increments only while c<10, not a magically strengthened certificate for the unchanged unsafe model. The latter has a simple inductive invariant c≤10. No existing rendered numerical measurement or empirical performance is implied.

Source image handling: the inspected extraction's source argument is mathematical prose rather than a relevant picture of this toy controller. Draw the authored model from its stated semantics; do not decorate it with unrelated source-cover art. Preserve source diagrams only if later source-image inspection identifies a directly relevant bounded-check figure. Production image inspection confirmed the sole extracted image is the cover, with no relevant bounded-verification diagram; it was omitted.

## Original visual identity

A precise mechanical inspection film, closer to an illustrated engineering cutaway than to a presenter beside data cards. Main foreground materials: deep aubergine `#40334e`, oxidized copper `#bd704e`, petrol blue `#226f82`, warm enamel `#ece5d8`, amber `#e5b143`, and a restrained coral danger signal `#cf5257`. The danger color appears only at a real boundary crossing. Use theme-specific ink/material variants; verify Color, Light and Dark. This palette and constructed ratchet/controller identity distinguish the film from the earlier green-platform and generic desk motifs.

The same counter assembly anchors the first three scenes, with changes of viewpoint and scale that expose different causal facts. It is never merely a repeated icon moved across a blank field. Controls visibly contact their mechanisms; a pointer moves along a calibrated arc, a stop catches a tooth, a permission latch physically remains closed. No meaningless connectors, floating cards, decorative outlines or arbitrary chart strokes.

An older maintenance engineer with short silver hair and a copper work coat appears only at the opening and closing. Hands and gaze follow the machine's relevant mechanism. The engineer is not a guide who points at every scene. Use the shared articulated rig, but author the staging and actions; avoid the reused bun-haired green-coat presenter.

One strong Red Hat Display player title per scene; Red Hat Text captions. All meaningful art text is an integrated scale, reading, part marking or instruction, with no duplicate aphorism. Reserve y≤520 for visual text and expressive hands, leaving the player’s measured caption region clear. Check caption intersection using the updated shared QA tool. Avoid arbitrary tiny ticks; show only the readable values relevant to the current sentence.

### Scene 1: an action waiting for its permission

Composition: broad three-quarter foreground cutaway of a compact controller assembly, with the engineer crouched at one side inspecting a real latch; the machine occupies most of the stage. The counter housing contains a visible scope plate reading `10 steps`. A request lever is poised, not perpetually moving. There are no standalone concept boxes.

Beat actions: the engineer approaches the latch on sentence 1; on sentence 2 the scope plate illuminates while the farther output arm remains still; sentence 3 connects the latch physically to that output; sentence 4 settles into an attentive pause. The image makes the practical distinction intuitive: possessing a check and authorizing the next action are related but separate events.

Feeling: focused curiosity, with a small unanswered mechanical tension. Do not trigger an alarm before the audience understands the machine.

### Scene 2: macro view of the checking horizon

Composition: close-up inside the counter housing, using the entire foreground for a ratchet, a large integrated numeric display and a short path with a physical horizon stop. This is not a spreadsheet of ten tiny boxes. The engineer is absent so the mechanism can be read.

Beat actions: sentence 1 introduces the initial zero and two possible changes, hold or increment; sentence 2 shows the modeled horizon ending at ten; sentence 3 settles on an intact scope seal and display `10`. On sentence 4 a newly requested transition advances to `11`, crossing a visibly marked forbidden region; a single coral flag rises. Sentence 5 keeps both the earlier scope mark and the later counterexample visible, so the audience sees that the first verdict was bounded rather than false.

Feeling: initial confidence, then precise surprise. The transition beyond ten is the dramatic turn; it is not a rapid counting effect that outpaces narration.

### Scene 3: a changed rule rather than more reassurance

Composition: side cutaway at the same scale as real machine components, exposing a newly fitted stop that catches the counter at ten. The old failing transition remains as a small physical test strip being withdrawn; the replacement guard occupies the focal position. Treat the strip as a record attached to the mechanism, not an anonymous claim rectangle.

Beat actions: sentence 1 replays just the offending eleventh transition in the test strip; sentence 2 leaves a stack of successful past checks insufficient to release the latch. Sentence 3 visibly introduces the changed guard; the drive attempts another cycle but the counter holds at ten. A minimal integrated rule `c < 10` may appear beside the actual guard only if projection readability is sufficient. Sentence 4 pulls back enough to show that inspection, modeled proof and runtime guard have distinct jobs, without adding a row of icons.

Feeling: concentration followed by earned clarity. The guard’s change is explicit, so we do not imply a proof can erase the original counterexample.

### Scene 4: from the toy model to the book's AI example

Composition: a single architectural cutaway of a software work area, viewed obliquely. A drafted patch enters an enclosed testing workspace. The deployment control is physically outside that workspace, separated by a latch with its own receiving authority. Render this as one coherent system with meaningful depth and containment, not three labelled rectangles on a line.

Beat actions: a short editable code fragment is placed in the drafting area on sentence 1; the fragment executes inside the testing enclosure on sentence 2; sentence 3 reveals the separate deployment latch; sentence 4 lets an unanswered evidence request leave that latch closed while the safe test workspace remains active. Only three integrated labels are permitted: `Propose`, `Test`, and `Deploy`, large and near their actual controls. Their appearance is paced, not simultaneous clutter.

Feeling: practical recognition and restraint. Missing evidence suspends one authority; it does not theatricalize total system failure.

### Scene 5: a specific reading invitation

Composition: return to the inspection room in a wider, calmer angle. The engineer now reads an open technical volume beside the real controller, whose scope marking and separate action latch remain visible. The book stands for this actual book; no generic library metaphor. The reader’s gaze alternates between the chapter and the physical condition the chapter helps interrogate.

Beat actions: sentence 1 reveals a source-faithful small chapter spread with mathematical limits and verification as readable section labels only if space permits; sentence 2 the engineer traces the relation between a scope marking and its guard; sentence 3 holds still for the research qualification. Sentence 4 places a finger on `Practical Warrant`, abbreviated visually while narration gives the full chapter title. Sentence 5 ends with the reader considering the action latch, not with an automatic success tick or a book purchase command.

Feeling: calm agency and a concrete question worth carrying into reading. The ending pays off the ten-step opening without claiming that the author’s philosophical framework is already validated.

## Review acceptance questions

- Does the first scene make the book and reading gain clear before introducing terminology?
- Is the authored toy-model status unambiguous in narration and provenance?
- Does scene 3 visibly change the controller before claiming a wider guarantee?
- Does each shot make the corresponding spoken causal distinction easier to understand?
- Are the exploratory status and existing-verification boundary preserved once, without repetitive disclaimers?
- Does the closing name a real starting chapter and a specific reader question?

Next steps only after root review: translate this approved direction into scene-specific art and metadata; inspect representative first/middle frames; generate English local Piper narration; retime from actual audio; run silent source, caption-overlap, all-theme and playback-control QA; publish atomically only when the replacement is complete.
