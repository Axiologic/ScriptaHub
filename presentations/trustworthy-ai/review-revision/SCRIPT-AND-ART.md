# Trustworthy AI — replacement introduction proposal

Status: approved script and art; installed with measured English voice and all-theme QA. See QA.json.

Purpose: English narrated book introduction, 120–180 seconds; one sentence per clip, measured local Piper speech and 1.0–1.5 second real gaps. Treat Meridian as the book's fictional running example, not a deployed product. Preserve the course's engineering orientation without importing unverified current regulatory claims.

Story spine: Trustworthy AI follows Meridian from useful research assistant toward more consequential capabilities, using each change to ask what reliance the evidence actually supports; the reader learns to connect a concrete failure path, fallback and changed dependency to an engineering release decision.

## Complete spoken draft

### 1. Trustworthy AI

1. Trustworthy AI follows a fictional assistant as useful answers acquire real consequences.
2. This engineering course asks what evidence justifies relying on each new capability.
3. Its running system, Meridian, gains documents, tools, memory, and limited autonomy.
4. You learn to connect specific failure paths to controls and release decisions.

### 2. The source must be there

1. Meridian may support internal policy research through approved repositories and read-only tools.
2. A factual answer must lead back to a retrievable source passage.
3. If retrieval fails, the system should admit it cannot answer that policy question.
4. That fallback belongs to the promised behavior, alongside a human review route.

### 3. The model stays the same

1. Now change the document repository while leaving the model itself unchanged.
2. Earlier test results may no longer support the same reliance claim.
3. The book treats this as evidence decay, with affected claims requiring renewed checks.
4. Version-linked evidence makes those dependencies visible to the team deciding whether to release.

### 4. Follow the failure

1. Meridian's behavior depends on data, the model, its surrounding software, and organizational decisions.
2. A missing source may become harmful when the interface hides uncertainty.
3. Useful review therefore needs evidence and authority to stop an unsupported release.
4. The book connects these responsibilities with privacy, fairness, security, and human reliance.

### 5. Assurance is an argument

1. An assurance case links a bounded claim to evidence and remaining uncertainty.
2. It records observations that would weaken the argument or trigger reevaluation.
3. Readers can use those links to ask what would change a release decision.
4. Begin with From Model Scores to Justified Reliance, then follow Meridian's expanding responsibilities.
5. Building an Assurance Case brings those lessons together into a reviewable engineering argument.

## Source grounding and exact scope

Canonical English edition-1: `docs/books/trustworthy/ai/bk-d50cba248572411d/en/full_content.html`. HTML SHA-256 `91f9e2731650496dfa95987ec514c0bb7d62d43e767765cb7e7afdb1241d9656`; extracted text SHA-256 `3712c7a841ef010e425dcddd2b9c1b07bfbbdf04a4309adf792936f16d938fea`.

- Source-1, About This Edition, and source-3 chapter1 introduction explicitly call Meridian fictional and describe a qualitative engineering course whose running example acquires confidential data, tools, memory and limited autonomy. This gives the film its particular reading promise, not merely a general warning about AI.
- Source-4, complete1.1: justified reliance is conditional on intended use, operating envelope and evidence; Meridian's first release summarizes internal reports with supported document types, citation coverage and mandatory review. A score does not stand in for the entire system's operating evidence.
- Source-48, complete12.1: the actual example claim is internal policy research under approved repositories and read-only tools. Subclaims include factual grounding, access control, failure response and human review. The later enterprise example explicitly requires retrievable source passages and inability to answer when retrieval/model failure prevents support.
- Source-14, complete3.3: fault injection disables retrieval and tests safe degraded behavior. Depending on the task Meridian may enter clearly marked general-model mode or abstain; this film specifically selects the grounded internal-policy task, so saying it cannot answer *that policy question* does not imply a universal ban on all other output.
- Source-36, complete9.1: retrieval and source support are separate checks; a retrieved paragraph can fail to entail a generated claim. Film line2 says a factual answer must lead back to a passage, not that a citation alone proves truth. Art must not use a retrieved document as an automatic green truth stamp.
- Source-9, complete2.2: retrieval-index, corpus, prompts and tools may change while generator weights remain fixed; evidence tied to the previous configuration can become historical. Required checks follow affected claims, not a blanket demand to rerun everything.
- Source-8, complete2.1: data/model/harness/organization form the useful system decomposition; interface certainty, missing evidence and unavailable oversight can combine into a harmful path. Harness is spoken as 'surrounding software' for accessibility, retaining its meaning in provenance.
- Source-49, complete12.2: dependency changes should identify affected evidence and trigger evaluation before promotion; an assurance graph and automated invalidation are an architectural direction rather than a universal deployed guarantee. The film presents version-linked evidence as course reasoning, not a claimed existing fully automated platform.
- Source-48 and source-51, complete closing synthesis: assurance arguments contain bounded claims, evidence, residual uncertainty and defeaters; authority changes as evidence ceases to apply. The two recommended starting sections are actual source headings.

Revision reading scope: full section map and all12chapter introductions; complete About This Edition,1.1,2.1,2.2,3.3,9.1,12.1,12.2 and Closing Synthesis. Not a claim of a fresh manual word-for-word reread of all351976characters. No legal or medical advice or current-law statements are included in this adaptation.

## Source images

Inspected the full14-image inventory in a contact sheet. It contains the cover and simple process diagrams. Use the *relationships* in page15 Figure3 (data/model/harness/organization), page68 Figure9 (retrieve/generate/verify/cite-or-abstain) and page92/page95 continuous-assurance diagrams. Redraw them as the same concrete Meridian release rehearsal, rather than copying a row of generic rectangular boxes. Preserve the distinction between finding a source, checking its support, and deciding what the system may do. Other figures are outside this short film's selected example.

## Original art direction

A release rehearsal in a real collaborative workroom, with a large wall display and a reference archive. This is human-centered documentary staging of an engineering course. Use deep peacock blue, apricot-orange, warm stone, coral, and small acid-yellow indicators. Avoid the mechanical counter from Limits, Cones' clinic, Anti-Trivialization's policy screen, and Vector-Symbolic's notebook/role tokens. No floating stock AI chip, shield, checkmark or decorative connection network.

The cast is a short-haired engineer in a peacock sweater and an older reviewer in a warm coral jacket. They stand and move toward the displayed evidence, rather than sitting behind another desk. Expressive gaze and hands point to the actual missing source or stale evidence; neither is a generic presenter. A quiet background and one player heading leave room for the meaningful workroom foreground.

### Scene1 — a release rehearsal, not a score celebration

Wide view: the engineer demonstrates Meridian on a wall display to a reviewer. A clear answer has a source marker that opens into the adjacent reference archive. A small external-use exit remains closed: the current scope is internal research. New integrations are shown as actual additions to the archive/service boundary over the scene, without granting them a universal success mark. The focus is the reviewer's question about what the evidence permits. One integrated `Meridian` label identifies the fictional system; no invented logo or product claim.

Feeling: useful capability and interest, then a concrete need to inspect its limits.

### Scene2 — follow the citation until it fails

Change to a large close-up of the answer and its specific source link. A document passage can initially be opened; a support-check margin remains distinct from retrieval. During an explicit illustrated dependency fault, the source drawer cannot supply a passage. The answer changes to `Source unavailable` rather than keeping a confident enterprise-policy conclusion. A human review route remains visibly open beside the unavailable source. This stages the book's selected grounded-policy fallback; no fake policy wording, fabricated citation, benchmark percentage or empirical performance result.

Feeling: brief concern, then an intelligible bounded response. The system does something useful by preserving the failure and showing the next route.

### Scene3 — a dependency changes while the generator remains

Oblique cutaway of the same workroom display and archive. The document collection is replaced with a differently tabbed collection; the generator's central visual identity remains fixed. A previous source-support test is visibly attached to the old collection's version tab, so it no longer reaches the new one. Move to a new test slot without giving it a passing stamp. The unchanged generator plus severed evidence dependency makes evidence decay intuitive. This must not look like a collection of unrelated boxes; the archive replacement alters the one answer path established earlier.

Feeling: recognition that a small product change has a concrete evidence consequence.

### Scene4 — bring the organizational decision into view

Return to a lower, close viewpoint across the standing reviewer and engineer. The display shows the exact unavailable-source trace from scene2. The reviewer can hold promotion at the release control; the engineer can inspect the source failure. An unavailable or uninformed reviewer would leave that decision unsupported, so evidence reaches the person before the control becomes actionable. The four-layer source figure is translated into this one causal encounter: source collection, generator, software path, human authority. Do not add a four-label diagram over their faces or turn the reviewer into a rubber-stamp icon.

Feeling: thoughtful disagreement becoming a reviewable next action, not triumph.

### Scene5 — the book organizes the argument

Overhead view of a review spread on a shared reading ledge, with the actual source course open beside the existing test trace. The claim, the supporting passage/test and the unresolved issue remain connected by a few meaningful annotations. Hands from both participants revise one acceptance condition; the unresolved issue remains visible. The two source section names belong to the open reading tabs, while the spoken ending invites the course's fuller treatment of reliability, human reliance and assurance. Keep the source-book presence concrete but do not convert this into the giant notebook composition used in Vector-Symbolic; the focal action is joint review of one permission decision.

Feeling: earned clarity and a specific reason to study the course.

## Acceptance

The first30seconds must establish the fictional running case, engineering-course genre and concrete reader gain. Later examples support that introduction instead of becoming a Meridian product demo. The source outage is an illustrated test, not a reported incident. A citation is not automatic proof of source support. Changed retrieval does not automatically mean every previous result is false; it means affected claims need renewed justification. Preserve these meanings without narrating a separate disclaimer on every slide. Measure the final voice; inspect all3themes, full-size/settled capture fidelity, captions, role blocking and exact source traces before installation.
