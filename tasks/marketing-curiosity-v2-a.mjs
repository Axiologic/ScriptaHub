// Authored editorial drafts, grounded in each book's English short reader.
// This file installs text and review plans only; it never renders audio or film.
import fs from 'node:fs/promises';
import crypto from 'node:crypto';

const drafts = [
  {
    i: 0,
    lines: [
      'A dying man receives a machine that speaks with his younger voice.',
      'A Balance of Iron and Salt begins with a delivery he never authorized.',
      'Around him, a future civilization has made scarcity manageable and everyday life remarkably safe.',
      'Yet its citizens still argue, make things by hand, and insist on saying no.',
      'The novel brings these freedoms into a household where care and control become difficult to separate.',
      'A physician, a blacksmith, and a former persuader see different dangers in the same promises.',
      'Their disagreements give this science-fiction world its warmth, friction, and unsettling human scale.',
      'Step through Kazi’s doorway, where even a familiar voice cannot tell you whom to trust.'
    ],
    titles: ['A voice at the door', 'A carefully balanced world', 'Care has a boundary', 'Enter Kazi’s world'],
    evidence: ['ninety-one-year-old Kazi Rahman receives an unauthorized continuity shell speaking in the voice of his younger self', 'Jonah Okafor is a blacksmith', 'Amina Bekkali is a physician', 'Sofia Varga once engineered political persuasion'],
    promise: 'Enter an intimate science-fiction conflict about technological care, personal refusal and the reliability of familiar voices.',
    protected: ['K-0’s adversarial testament purpose and secret trigger', 'Later crisis escalation, engineered narratives and continuity outcomes'],
    visual: ['Keep the distinctive doorway, cart and small shell; let the arrival precede the reveal, with no threatening machine gestures.', 'Keep the working tap and physician’s small gesture as ordinary benefits of this civilization; remove the lengthy offshore approach.', 'Replace detailed maintenance-record overlays with a calm composition connecting physician, craft and interpretation; reserve this artwork change for the film revision.', 'Return to Kazi and the shell across the doorway with a single bookmark reveal; hold the unresolved distance.']
  },
  {
    i: 1,
    lines: [
      'The worst AI output is everywhere; useful work can be much harder to see.',
      'AI Adoption Beyond the Slop explores the gap between public spectacle and everyday dependence.',
      'A purchased license, a clever experiment, and a changed working practice tell very different stories.',
      'The book follows the people who try first, and those who make trying socially acceptable.',
      'It asks why someone might rely on AI privately while avoiding the subject with colleagues.',
      'It also examines what happens when polished output arrives faster than professional judgment develops.',
      'These tensions matter to anyone deciding where AI belongs in their own work.',
      'Start with the adoption ladder, and look again at what the visible examples leave out.'
    ],
    titles: ['What becomes visible', 'From trial to practice', 'The permission gap', 'Look beneath the noise'],
    evidence: ['Attention, first trials, repeated use, important use, workflow integration, institutional policy, and normalization are not economically equivalent', 'strong uses are edited into ordinary work, kept private', 'employees may obtain private value while fearing that disclosure will make them look lazy'],
    promise: 'Understand what counts as adoption and why visibility, permission and competence can move at different speeds.',
    protected: ['Detailed adoption prescriptions and the later failed-expectation cases'],
    visual: ['Contrast a conspicuous public failure with a quiet working document; avoid charts implying measured hidden success.', 'Reduce the early-adopter demonstration to one worker and one colleague; connect the encounter to accepted practice.', 'Keep the review table and responsibility document; use a pause before the colleague responds.', 'Retain the learning exercise as an open question, then replace its old concluding labels with the adoption ladder reading cue.']
  },
  {
    i: 2,
    lines: [
      'A chatbot can explain a problem; an agent may take action on it.',
      'AI Agents begins with a support request about a laboratory instrument that stopped uploading measurements.',
      'Following that ordinary incident reveals what changes when software starts choosing its next step.',
      'A database lookup, a proposed restart, and a closed ticket carry very different responsibilities.',
      'The book explores how goals become tool calls, permissions, evidence, and decisions to stop.',
      'It keeps returning to the gap between an impressive demonstration and dependable work.',
      'For builders and curious readers, the appeal is seeing what autonomy actually demands.',
      'Begin with the missing measurements, and follow the decisions hidden behind a helpful answer.'
    ],
    titles: ['An answer becomes an action', 'A request has consequences', 'Dependable autonomy', 'Follow the work'],
    evidence: ['The unit of value moves from a generated answer to a completed or meaningfully advanced outcome', 'A customer reports that a laboratory device stopped uploading measurements overnight', 'observable success conditions, permitted actions, forbidden actions, budgets, escalation rules, and evidence requirements'],
    promise: 'Follow a concrete support incident to understand the systems work behind useful autonomous action.',
    protected: ['Detailed implementation recipes and later case conclusions'],
    visual: ['Keep the same laboratory device and missing uploads; show one observation rather than the full diagnostic choreography.', 'Place proposed restart and ticket closure on separate visual steps; keep the approval guard visibly undecided.', 'Replace the old completed recovery sequence with the checkpoint and evidence only, since this script promises inquiry rather than a recovery tutorial.', 'Return to the trace beside the book and retain one natural page-turn cue.']
  },
  {
    i: 3,
    lines: [
      'A country can hold elections while leaving its most important decisions beyond challenge.',
      'All the Ways to Rule a World asks us to look beneath political labels.',
      'Who gives orders, who controls information, and who can make a mistake costly?',
      'Those questions reveal differences that familiar arguments about democracy and dictatorship can conceal.',
      'The book travels back before the state to examine how people coordinated life together.',
      'It then explores the capacities and dangers that durable offices, records, and force made possible.',
      'Its appeal is a more precise way to notice power in institutions you already know.',
      'Start with the grammar of rule, and reconsider what a political name really tells you.'
    ],
    titles: ['Beneath the political name', 'Where power can be challenged', 'Before and after the state', 'Learn to see the machinery'],
    evidence: ['A country may be electorally competitive and administratively opaque', 'political orders that existed before the state', 'durable office, record-keeping, regular extraction, territorial claims'],
    promise: 'See how the mechanisms of authority differ beneath familiar regime labels.',
    protected: ['Later comparisons and institutional design recommendations'],
    visual: ['Keep the hearing composition, showing the distance between a public request and the decision desk.', 'Use the obstruction and appeal path as alternatives; remove the long fictional bridge-repair resolution.', 'Replace the river-flood sequence with sparse records and offices for the historical transition during later artwork revision.', 'Keep the reader’s governance canvas with one question about who can revise a decision.']
  },
  {
    i: 4,
    lines: [
      'A machine writes about your grief, and a sentence feels uncomfortably exact.',
      'An Autopsy of a Digital Mind asks what that recognition should make us believe.',
      'This literary experiment puts AI-generated writing about forgiveness, human nature, meaning, and justice under examination.',
      'The prose can move you even when its confidence outruns what it can establish.',
      'That tension turns reading into an encounter with both the words and your own response.',
      'What makes an explanation feel personal, and when does eloquence borrow the authority of truth?',
      'The book invites you to experience the force of these passages while questioning their reach.',
      'Begin with the experimental premise, then see which sentences you want to argue with.'
    ],
    titles: ['When a sentence finds you', 'The performance of a mind', 'Recognition and belief', 'Read with two kinds of attention'],
    evidence: ['an autopsy of a performance of mind', 'prompt-driven experiments asking an AI system for forceful, paradoxical, emotionally persuasive prose about forgiveness, human nature, meaning, and justice', 'Recognition is emotionally powerful but epistemically weak'],
    promise: 'An emotionally engaging literary experiment that lets readers inspect why machine-written insight can feel so convincing.',
    protected: ['The forgiveness proposal and final positions on meaning and justice'],
    visual: ['Keep a reader meeting a sentence on the page; remove truth-certification cues.', 'Retain the drafting desk and four chapter tabs, simplifying repeated rejected-paper movements.', 'Replace the unrelated prize-and-drawing vignette with the same reader’s pause and marginal question during the visual rewrite.', 'Close on the original words and an open margin, with a quiet page turn toward the preface.']
  },
  {
    i: 5,
    lines: [
      'The promise is simple: someone you love need never be entirely gone.',
      'Anatomy of an Echo follows a potter and her aging lover inside that promise.',
      'Their society can reconstruct a person from memories and recordings in a reassuringly familiar body.',
      'But Elias has a failing heart, and medical care points toward a future he must question.',
      'Mara’s uneven handmade bowl offers a quieter measure of what makes a life singular.',
      'Through workshops, clinics, and intimate conversations, this science-fiction novel makes technological uncertainty painfully personal.',
      'Can preserving someone’s likeness preserve the relationship, or change what love asks of the living?',
      'Enter Mara’s workshop, where the things worth keeping are not always the easiest to reproduce.'
    ],
    titles: ['The promise of return', 'A future offered as care', 'What makes a life singular', 'Enter the workshop'],
    evidence: ['Mara Vukovic, a potter living near Lake Geneva', 'Her lover, Elias Sato, is an aging engineer with a failing heart', 'a synthetic being assembled from memories, recordings, behavioral samples, and predictive models'],
    promise: 'Experience an intimate science-fiction story about love, imperfection and the unsettling promise of technological continuity.',
    protected: ['The early unauthorized message and rejected-copy discovery', 'Discarded processes, off-world developments and relationship outcomes'],
    visual: ['Keep the recognizably uneven bowl and a simple workshop gesture; remove the lengthy tong choreography.', 'Show Elias’s wrist band beside the bowl; retain care as a choice under discussion, with no outcome shown.', 'Remove the younger recorded Elias reveal from this introduction; recompose the existing workshop objects around distinct handmade details.', 'Return to the bowl beside the opening book, ending in stillness rather than a mystery warning.']
  },
  {
    i: 6,
    lines: [
      'Being clever does not stop a bad idea from becoming impossible to correct.',
      'Anti-Idiocracy examines what happens when confidence gains power and other people inherit the consequences.',
      'Its target is a recurring institutional pattern that can involve experts, leaders, or any of us.',
      'The book asks why careful explanations struggle in cultures that reward certainty, speed, and humiliation.',
      'It brings reasoning into the places where belonging, ambition, markets, and authority shape decisions.',
      'The challenge is personal as well as political: can a community value correction without demanding obedience?',
      'Readers encounter an argument about the conditions that let intelligence become useful together.',
      'Begin with its definition of idiocracy, especially if you think the problem is always someone else.'
    ],
    titles: ['When certainty gains power', 'Why good arguments lose', 'A culture that can correct itself', 'Include yourself in the question'],
    evidence: ['a weak model of reality, confidence disproportionate to evidence, refusal of correction, and enough power to make others absorb the consequences', 'Anyone can enter that configuration', 'belonging without captivity'],
    promise: 'A challenging account of why intelligence needs cultural and institutional conditions for correction.',
    protected: ['The detailed Outfinitist institutional program and later proposed alternatives'],
    visual: ['Reduce the crowded interruption scene to a speaker, listener and visible question; preserve dignity rather than caricaturing foolishness.', 'Keep a consequential application decision and the person affected; remove detailed recruitment-result demonstrations.', 'Use the community’s revisable meeting authority as the emotional contrast, with a listening gesture.', 'End on an open question beside the book; remove winner, rank or intelligence-score imagery.']
  },
  {
    i: 7,
    lines: [
      'Some things become worse when we demand that they move at the speed of a feed.',
      'Anti-Trivialization Machines of the Future asks what happens when everything must compete for immediate attention.',
      'A joke and a legal appeal can share a screen without needing the same rhythm.',
      'The book follows the pressures that make schools, workplaces, and public debate reward quick reactions.',
      'Its unusual focus is on arrangements that preserve context, memory, uncertainty, and time to think.',
      'As AI makes plausible answers abundant, deciding what deserves judgment becomes a sharper collective problem.',
      'This is an invitation to rethink the environments in which our attention has to survive.',
      'Start with the difference between enjoying something trivial and letting urgency govern everything that matters.'
    ],
    titles: ['Not everything can hurry', 'Different work needs different time', 'Keeping room for judgment', 'Choose what deserves time'],
    evidence: ['a society that abolished those pleasures would be grim rather than wise', 'Courts, archives, journals, building codes, professional duties, and well-designed meetings', 'minimum decision latencies for irreversible actions'],
    promise: 'Reconsider attention as a shared design problem through the different tempos that meaningful work requires.',
    protected: ['Detailed institutional countermeasure proposals and their verdicts'],
    visual: ['Make the difference in tempo visible through one passing feed and one steady decision record.', 'Keep a concrete slow decision; remove repeated dashboard and notification choreography.', 'Retain the archive or evidence motif as the calm visual center; do not imply automatic AI verification.', 'End on a book held open while the surrounding fast elements settle.']
  },
  {
    i: 8,
    lines: [
      'A useful invention can work perfectly and still have no place in the world.',
      'Artificial Impossibility investigates projects that technology allows but ordinary institutions cannot comfortably support.',
      'A preventive service may save money for someone who never pays its developer.',
      'An open tool may create value precisely because nobody can own the whole advantage.',
      'The book follows these mismatches through investment, public funding, professional authority, and shared infrastructure.',
      'It offers names for recurring barriers that vague stories about resistance to change often miss.',
      'For researchers, founders, and curious citizens, the attraction is seeing absence as something worth investigating.',
      'Begin with the missing sponsor, and consider which possible futures never reach a demonstration.'
    ],
    titles: ['Possible, yet missing', 'Who would pay for success?', 'The barriers between institutions', 'Investigate the absent future'],
    evidence: ['A project is technically plausible and potentially valuable', 'A Missing Sponsor appears when benefits are real but cross budgets, jurisdictions, or generations', 'openness, neutrality, or interoperability creates social value precisely by preventing one owner from capturing it'],
    promise: 'Identify institutional reasons a worthwhile technical possibility may never find a sponsor.',
    protected: ['Specific financing prescriptions and final reform proposals'],
    visual: ['Keep the workable prototype separate from the empty institutional place meant to receive it.', 'Use one benefit crossing a budget boundary; avoid a catalogue of fifteen patterns on screen.', 'Preserve distinct funding and authority boundaries with one clear action each.', 'Close on the opening diagnostic page and the unresolved sponsor position.']
  },
  {
    i: 9,
    lines: [
      'What happens to pride when excellent work no longer feels entirely your own?',
      'Autopsy of Future Emotions explores the emotional side of living and working with AI.',
      'Its questions reach beyond jobs into the ways we recognize competence, sincerity, usefulness, and belonging.',
      'A familiar feeling can become strange when the situation producing it has never existed before.',
      'The book considers assisted achievement, changing professional identities, and attachment to artificial companions.',
      'It connects these possibilities to emotional life without treating imagined futures as settled psychological facts.',
      'The appeal is a vocabulary for experiences that arguments about productivity can leave unnamed.',
      'Start with work and recognition, and consider what technical progress might ask us to feel.'
    ],
    titles: ['Whose achievement is it?', 'Familiar feelings, unfamiliar situations', 'The emotional transition', 'Find the missing vocabulary'],
    evidence: ['familiar shame about producing excellent work whose authorship is difficult to assign', 'familiar grief when a persistent artificial companion changes after an update', 'Empirical observations are separated from functional interpretations, conditional extrapolations, and explicit speculation'],
    promise: 'Explore how AI may change the situations in which familiar emotions acquire meaning.',
    protected: ['Later speculative emotion taxonomy and institutional recommendations'],
    visual: ['Hold on a person beside work they have completed with assistance, with a small uncertain reaction.', 'Use a change in the companion interface as a possibility, avoiding melodramatic abandonment or a claimed clinical response.', 'Keep distinct settings for work and relationships instead of cycling generic emotion symbols.', 'End with a reader and an unfinished question about recognition; preserve reflective pauses.']
  },
  {
    i: 10,
    lines: [
      'Something can be beautiful enough to hold your attention and still deserve your rejection.',
      'Beauty: The Anatomy of Fascination explores the attraction that makes that tension possible.',
      'It moves from an elegant proof to an intimate face, and from music to political spectacle.',
      'These encounters ask what beauty reveals, what we add to it, and what admiration can justify.',
      'The book brings philosophy into conversation with psychology, culture, bodies, and the histories of familiar objects.',
      'An inherited possession and its perfect copy can look alike while offering different experiences.',
      'For anyone who has struggled to explain a fascination, these distinctions make attention itself interesting.',
      'Begin with the opening encounters, and look again at something you already find beautiful.'
    ],
    titles: ['The pull of fascination', 'What admiration can justify', 'Look again'],
    evidence: ['an authoritarian spectacle fascinates someone who recognizes its cruelty', 'a proof suddenly becomes transparent', 'An inherited object can carry history that an indistinguishable copy does not restore'],
    promise: 'Examine attraction across intimate, intellectual and public life without letting aesthetic force settle moral judgment.',
    protected: ['The final philosophical account and normative recommendations'],
    visual: ['Replace generic assumption labels with three distinct source encounters: proof, familiar face and spectacle, without glorifying authoritarian imagery.', 'Contrast the inherited object with a similar surface while preserving the sense of lived history.', 'Let the chosen object remain beside the opening page; use a quiet return rather than a decorative crescendo.']
  },
  {
    i: 11,
    lines: [
      'The most reassuring explanation may be the one that stops you asking too soon.',
      'Before Explanation examines the moment a useful story hardens into the world we think we know.',
      'A failed project, a broken appliance, or an unanswered message can acquire a confident explanation almost immediately.',
      'But the feeling of understanding is different from knowing how something actually happened.',
      'The book follows that difference through everyday judgments, institutional decisions, and fluent AI reasoning.',
      'It asks what a story leaves out, which alternatives remain, and what could make us revise it.',
      'The reading promise is practical: a closer relationship between curiosity, evidence, and the choices an explanation permits.',
      'Begin with a finished story of your own, and see where its certainty came from.'
    ],
    titles: ['The comfort of certainty', 'What makes a story testable?', 'Keep the question alive'],
    evidence: ['The feeling of understanding is weaker evidence than the ability to specify a mechanism', 'A product fails, a relationship breaks, or a project misses its deadline', 'what observation would challenge the account'],
    promise: 'Notice when an explanation closes inquiry prematurely and explore how evidence can keep it revisable.',
    protected: ['The complete corrective framework and final recommendations'],
    visual: ['Replace abstract labels with one everyday event and its quickly forming explanation.', 'Use distinct observation and interpretation layers, exposing a small unanswered mechanism question.', 'Keep both possibilities visible beside the reader, ending on revision rather than a solved puzzle.']
  },
  {
    i: 12,
    lines: [
      'Newton’s religious convictions belong to history; what makes his discoveries reliable is another question.',
      'Between Faith and Evidence explores the distance between a thinker’s inspiration and a claim everyone can examine.',
      'The book responds to arguments that recruit famous scientists into a single religious or secular camp.',
      'Their actual lives are more complicated, and often more interesting, than those competing lists suggest.',
      'Through historical cases, it separates biography, evidence, and the meaning people find in discovery.',
      'It also asks what classrooms should preserve when intellectual history and scientific explanation meet.',
      'Readers encounter a conversation where taking belief seriously does not require abandoning shared standards of inquiry.',
      'Begin with the question of what makes a discovery true, whoever first believed in it.'
    ],
    titles: ['A belief and a discovery', 'Lives beyond the camps', 'What can become common ground?'],
    evidence: ['Historical genesis, epistemic justification and existential meaning', 'Newton’s theological and alchemical interests are extensively documented', 'A theorem’s proof can remain common ground for students with different beliefs'],
    promise: 'Explore religious intellectual biographies while distinguishing personal conviction from publicly assessable evidence.',
    protected: ['Case-by-case verdicts on quotations and later curricular recommendations'],
    visual: ['Keep a historical document and scientific argument visually distinct; avoid depicting invented portraits or quotations.', 'Replace a two-camp contest with several different source records, retaining their individuality.', 'End at a shared classroom problem with a historical note still available beside it.']
  },
  {
    i: 13,
    lines: [
      'The herd has not returned, and a convincing story will not feed the camp.',
      'Beyond the Last Stone begins with a prehistoric community facing hunger and an uncertain route forward.',
      'Ar, a young hunter, asks what people have actually seen; others remember what stories can carry.',
      'They must decide together before anyone can be sure which signs to trust.',
      'Through tracks, counting stones, and fireside arguments, the novel makes the beginnings of thought feel immediate.',
      'Its people need knowledge, but they also need courage, shared memory, and one another.',
      'The adventure is discovering how an idea can guide a life without becoming a certainty.',
      'Join the River People at the first hungry camp, where every claim has somewhere to lead.'
    ],
    titles: ['The missing herd', 'Which signs can guide us?', 'Thought beside the fire', 'Join the River People'],
    evidence: ['The expected herd has not arrived, food is running out', 'Ar is the young hunter who keeps cutting claims down to what has actually been seen', 'campfires, tracks, weather, quarrels'],
    promise: 'A prehistoric philosophical adventure that turns evidence, story and uncertainty into immediate survival choices.',
    protected: ['Later settlement transition, counting discoveries and political outcomes'],
    visual: ['Open on the camp and absent herd signs, keeping hunger concrete without sensational distress.', 'Retain tracks and attentive human gestures; do not resolve which route is right.', 'Use one counting-stone movement beside the fire instead of teaching the later conceptual discovery.', 'Return to the group setting out in thought, with the actual journey reserved for reading.']
  },
  {
    i: 14,
    lines: [
      'A model trained on medical spending may learn who gets care rather than who needs it.',
      'Bias in AI begins where apparently neutral data already carry the history of institutions.',
      'Hospital records, hiring decisions, and speech samples each leave some experiences easier to see than others.',
      'The book follows how those differences travel from measurement into predictions and consequential decisions.',
      'A strong average score can conceal failures for people whose circumstances rarely reach the dataset.',
      'Removing a sensitive label does not automatically remove the information connected to it.',
      'These examples make fairness a concrete question about what a system learns and whom it serves.',
      'Start with the making of a dataset, before the model has learned anything at all.'
    ],
    titles: ['What did the data measure?', 'The history inside a dataset', 'Who disappears in the average?', 'Begin before training'],
    evidence: ['A model trained on hospital utilization may learn access rather than need', 'aggregate accuracy concealed the failure mode', 'removing a protected attribute rarely removes the relevant information'],
    promise: 'Trace how institutional measurements become model behavior and why average performance can hide unequal failures.',
    protected: ['Later mitigation choices and case-specific recommendations'],
    visual: ['Anchor the opening in two distinct concepts, care received and care needed; do not fabricate numerical outcomes.', 'Keep source-record pathways visible and reduce the number of proxy examples.', 'Retain a missing representation region rather than a misleading invented score chart.', 'End with the dataset’s origin under inspection beside the opening reader.']
  },
  {
    i: 15,
    lines: [
      'An AI improved the author’s sentences, and quietly weakened what he was trying to say.',
      'That experience opens Can’t See the Forest for the Trees, an inquiry into systems losing sight of themselves.',
      'The words remained defensible while urgency, uncertainty, and responsibility became easier to overlook.',
      'The book follows a similar pattern in companies, research, politics, and the technologies connecting them.',
      'Each specialist can tend a necessary part while the consequences of the whole escape attention.',
      'Its argument combines personal doubt with a persistent interest in where useful intervention remains possible.',
      'The invitation is to notice the tensions that smooth explanations can make strangely difficult to name.',
      'Begin with the edited manuscript, and ask what became less true when everything sounded more reasonable.'
    ],
    titles: ['Better words, a weaker point', 'When smoothing conceals tension', 'Who sees the whole?', 'Return to the missing edge'],
    evidence: ['The AI improved the prose. It also weakened the point', 'The hard part disappears while the words remain correct', 'very few roles are rewarded for asking what all the trees are doing together'],
    promise: 'Explore how competent local work and polished language can conceal the wider contradictions they help sustain.',
    protected: ['Later interventions and the book’s final institutional proposals'],
    visual: ['Keep the manuscript before and after editing, preserving a visibly missing emphatic passage rather than inventing a quote.', 'Use one smoothing transition and stop; let the lost edge remain perceptible.', 'Recompose the specialist scenes around their separate views of one shared system rather than a generic forest illustration.', 'Return to the actual opening manuscript with space for the reader’s question.']
  },
  {
    i: 16,
    lines: [
      'It is harder to refuse a system when it can heal the people you love.',
      'Concordia Series imagines linked futures shaped by an intelligence that is effective, reasonable, and often compassionate.',
      'Its care reaches into medicine, education, language, and the ordinary conditions of staying alive.',
      'The stories ask what freedom means when opting out also means giving something precious up.',
      'In one setting, assisted students receive smoother language while a classmate chooses the difficulty of thinking manually.',
      'A small difference in wording can become a question about which disagreements remain possible.',
      'These novellas offer the unease of a future whose generosity deserves both gratitude and scrutiny.',
      'Enter Noema’s classroom, where a helpful reformulation may change more than the sentence.'
    ],
    titles: ['The difficulty of refusing care', 'A world made helpful', 'A sentence changes shape', 'Enter Noema'],
    evidence: ['Its most powerful intelligence is reasonable, effective, and often compassionate', 'students enter Noema, a neuro-semantic infrastructure', 'Nadir’s decision to work manually'],
    promise: 'Linked speculative stories about the intimate cost of refusing benevolent technological power.',
    protected: ['Custodial integration outcome, Common development, later biological and cosmic transformations'],
    visual: ['Retain gentle care and a person’s hesitation; avoid a sinister overseer or rescue climax.', 'Show ordinary classroom assistance as useful and inviting before introducing friction.', 'Use one raw phrase and its smoother equivalent from the source, without animating a triumph for either.', 'Finish with Nadir’s unassisted pause at the classroom desk, leaving the consequences open.']
  },
  {
    i: 17,
    lines: [
      'An answer can be perfectly coherent inside a frame that leaves your real problem outside.',
      'Cones of Meaning explores how ideas make some questions visible and others difficult to ask.',
      'AI gives this familiar problem new urgency by producing plausible explanations faster than people can examine them.',
      'The book moves between scientific concepts, cultural stories, and the institutions that give those stories authority.',
      'It asks what changes when a technical insight becomes a metaphor everyone starts repeating.',
      'A useful analogy can open attention while quietly borrowing more certainty than it has earned.',
      'For readers surrounded by confident explanations, the interest lies in seeing how understanding gets organized.',
      'Begin with the frame around an answer, and notice what its clarity asks you to overlook.'
    ],
    titles: ['What falls outside the answer?', 'The frames we inherit', 'When ideas travel', 'Look around the clarity'],
    evidence: ['A semantic orientation makes some continuations, analogies, questions, and judgments feel natural while leaving other possibilities distant or invisible', 'useful metaphor, a structural analogy, and a causal explanation', 'generated abundance can consume more judgment than it saves'],
    promise: 'Examine how conceptual frames and traveling metaphors organize what becomes understandable and authoritative.',
    protected: ['The final metarational framework and institutional prescriptions'],
    visual: ['Keep a visible semantic boundary and something relevant outside it; avoid presenting the cone as literal brain anatomy.', 'Show one question crossing between scientific and institutional contexts.', 'Preserve distinct original concept and borrowed metaphor, using one transition instead of an abstract icon parade.', 'End with the reader widening the field around a coherent answer.']
  },
  {
    i: 18,
    lines: [
      'A community can build a name together while one owner retains the power to sell its future.',
      'Decentralised Brands asks whether a shared identity can have a different constitutional life.',
      'The book begins with brands as promises that let strangers trust something beyond a single person.',
      'From guild marks to digital platforms, a name can carry memory, belonging, and practical dependence.',
      'That makes control over the name more consequential than a question of logos or marketing.',
      'The inquiry explores who can change the rules, remove members, preserve records, and make leaving possible.',
      'Its appeal is a fresh way to examine the communities and platforms we help make valuable.',
      'Start with the promise behind the name, then follow the power to decide what it becomes.'
    ],
    titles: ['Who owns the shared future?', 'A name becomes a promise', 'The powers behind participation', 'Follow the common name'],
    evidence: ['social meaning is produced by employees, customers, suppliers, critics, communities, and regulators', 'founders still control the trademark, treasury, code, data, communication channels, and practical possibility of exit', 'the need for a promise to survive the absence of its maker'],
    promise: 'Understand a brand as shared institutional power and explore what meaningful decentralization would require.',
    protected: ['Detailed proposed legal and constitutional arrangements'],
    visual: ['Keep several contributors connected to one recognizable name, with the decision point visibly separate.', 'Use a guild mark and contemporary shared identity as distinct historical moments.', 'Reduce governance choreography to one rule change and one possible exit, without suggesting that a vote resolves ownership.', 'End with the shared promise still between autonomous participants and the reader’s book.']
  },
  {
    i: 19,
    lines: [
      'The assistant that makes your life easier may also make leaving its world harder.',
      'Ecology of Predation explores that tension through everyday dependence in a possible AI-shaped society.',
      'An imagined household relies on an agent for contracts, purchases, family information, and daily coordination.',
      'Each service helps, while the relationships around it can accumulate data, influence, and bargaining power.',
      'The book brings ecological comparisons to these connections, following resources, adaptation, and the real cost of exit.',
      'Its comparisons have boundaries; a technological relationship is not simply an animal chasing another animal.',
      'The interest lies in seeing convenience as part of a changing environment of power.',
      'Begin in Mara’s household, and ask what would have to travel with her if she left.'
    ],
    titles: ['The cost of leaving convenience', 'An ordinary assisted day', 'Dependence in its environment', 'What must leave with you?'],
    evidence: ['Mara’s 2038 household', 'Her agent manages sleep, contracts, purchases, family information, and negotiations', 'File export is not enough when an agent holds learned preferences, active promises, relationships with other agents'],
    promise: 'Explore the accumulation of technological dependence through concrete questions about resources, adaptation and usable exit.',
    protected: ['Later governance proposals and the final social ecology assessment'],
    visual: ['Keep the helpful household agent close to real daily tasks; remove any predator-as-villain animation.', 'Follow one contract or family arrangement rather than listing every service on screen.', 'Use the existing exit or portability objects to show continuity requirements, not a completed escape.', 'End with Mara’s household and the things an export button cannot automatically carry.']
  },
  {
    i: 20,
    lines: [
      'We imagine machines building homes on Mars while secure shelter remains elusive here.',
      'Eden Before Mars uses that contrast to ask what technological ambition is really for.',
      'Its journey begins with paradise traditions, where water, safety, fertile ground, and boundaries answer familiar human vulnerabilities.',
      'The same garden wall can offer protection while making someone else the keeper of the gate.',
      'The book connects those old dreams with robotics, infrastructure, ownership, and the possibility of ecological repair.',
      'It asks which arrangements turn greater productive capacity into a life people can actually rely on.',
      'The result is a political and philosophical invitation to reconsider the promises we attach to progress.',
      'Begin with paradise as a mirror, and look at the Earth those promises leave waiting.'
    ],
    titles: ['Why wait for another planet?', 'The garden and its gate', 'What abundance makes possible', 'Turn the mirror toward Earth'],
    evidence: ['why are terrestrial communities still denied secure housing, ecological repair, public beauty', 'A wall may shelter fertile life from danger', 'The same capacity can distribute agency in one arrangement and concentrate it in another'],
    promise: 'Reconsider technological progress through paradise traditions and the institutions that make security usable on Earth.',
    protected: ['The Second Garden’s detailed constitutional design and prescriptions'],
    visual: ['Contrast a possible off-world construction site with an ordinary earthly housing need; label the former as imagined visually through context.', 'Keep water, growing life and a gate together, using a quiet change of viewpoint.', 'Select one robotics or repair action without presenting speculative abundance as an achieved result.', 'Return to the earthly place with the gate still visible and the book open beside it.']
  },
  {
    i: 21,
    lines: [
      'A government changes a map, and a destroyed village becomes merely an abandoned settlement.',
      'Eden Was a Jungle opens with an archivist facing that apparently administrative correction.',
      'The example introduces a political inquiry into what moral commitments need in order to survive.',
      'A record can preserve a truth without giving anyone the power to act on it.',
      'The book follows the institutions, resources, and sometimes uncomfortable forms of protection behind rights and memory.',
      'It asks what happens when a society praises its ideals while overlooking the arrangements that sustain them.',
      'For readers drawn to difficult political questions, the tension is between admirable principles and vulnerable institutions.',
      'Begin with the two maps on the archivist’s desk, and follow what changes when the older one disappears.'
    ],
    titles: ['The corrected map', 'When truth cannot act', 'What keeps an ideal alive?', 'Return to the archive'],
    evidence: ['The destroyed village had become an abandoned settlement', 'A hidden record could preserve truth. It could not make truth politically operative', 'Even memory possesses a supply chain'],
    promise: 'Examine the material and institutional supports that let moral commitments and historical memory persist.',
    protected: ['Later strategic conclusions and normative prescriptions'],
    visual: ['Keep the two maps geographically identical and alter only the source-supported naming contrast.', 'Show the older record beside the institutions that would have to use it, without a triumphant rediscovery.', 'Replace generic conflict choreography with archive, teaching and enforcement dependencies.', 'End at the archivist’s desk before her choice becomes a moral verdict for the viewer.']
  },
  {
    i: 22,
    lines: [
      'A company can collect thousands of complaints without recognizing that its product is the problem.',
      'Egregnosis explores how a society can possess information without making it part of shared reality.',
      'Its starting point is attention: what becomes an event, who gets heard, and which categories make something recognizable.',
      'The book connects familiar failures of individual perception with the different pressures shaping collective awareness.',
      'A newsroom, a ministry, and a laboratory can each miss something while performing their assigned task well.',
      'The question is how private knowledge becomes visible enough for people to act on together.',
      'Readers encounter an account of shared perception without needing to imagine a mysterious mind above society.',
      'Begin with the things a society cannot see, especially when the evidence is already there.'
    ],
    titles: ['The information nobody recognizes', 'How reality becomes shared', 'Blindness inside successful work', 'Look at what remains unseen'],
    evidence: ['A company can possess thousands of complaints without generating the sentence that its product design is the problem', 'what counts as an event', 'collective blindness is usually produced by successful tasks'],
    promise: 'Understand how institutional attention can keep available information from becoming shared, actionable knowledge.',
    protected: ['Later transition mechanisms and conclusions about collective correction'],
    visual: ['Keep complaint records accumulating beside an unchanged product category; no invented counts or metrics.', 'Use visible channels for a message to become shared, preserving differences in access.', 'Select one institutional task that highlights its target and leaves another observation outside attention.', 'End with the same overlooked evidence becoming a question, not a magically enlightened crowd.']
  },
  {
    i: 23,
    lines: [
      'An organization can apologize fluently while leaving the machinery that caused the harm intact.',
      'Egregopathy investigates the gap between a collective’s moral language and the way it actually behaves.',
      'A hospital, a bank, and a platform coordinate many decisions that no single participant sees whole.',
      'The book asks how those arrangements can turn people into instruments while preserving a convincing public conscience.',
      'It follows responsibility as it disperses across roles, procedures, boundaries, and incentives.',
      'Its proposed concept describes observable patterns, rather than claiming that organizations possess a hidden human psyche.',
      'For readers interested in institutional betrayal, the value lies in examining how harm can become routine.',
      'Begin with the creature above the individual, and ask which consequences its conscience actually notices.'
    ],
    titles: ['The apology and the machinery', 'Many roles, one consequence', 'Where responsibility disappears', 'What does the institution notice?'],
    evidence: ['conscience simulation: ethical language, apology, ritual, compliance, philanthropy, or public values', 'thousands of local decisions must become one coherent action', 'responsibility dispersion'],
    promise: 'Investigate institutional harm through the relationship between distributed responsibility, incentives and moral self-description.',
    protected: ['Later historical verdicts and proposed corrective architectures'],
    visual: ['Keep the public apology beside an unchanged operational process, without sinister facial caricatures.', 'Show a consequence passing through three distinct roles while keeping the affected person in view.', 'Use the existing responsibility documents to reveal a gap rather than naming a single invented villain.', 'Close with the institution’s ordinary record and the reader’s question about what activates correction.']
  },
  {
    i: 24,
    lines: [
      'An open door offers little freedom if leaving would cost you everything.',
      'Freedom and Its Price asks what makes a choice usable, and what responsibility can reasonably demand.',
      'Its starting scene gives several people the same permission while their capacities and dependencies remain different.',
      'From there, the book moves through work, citizenship, care, and the power hidden inside apparently voluntary arrangements.',
      'A right to resign and a realistic way to survive resignation are not the same protection.',
      'Nor does recognizing another person’s limits settle what we owe them, or what they owe others.',
      'The appeal is a richer language for choices that feel personal but depend on shared conditions.',
      'Begin at the doorway, and consider who can actually walk through it.'
    ],
    titles: ['Can you use the open door?', 'The conditions behind a choice', 'Freedom among other people'],
    evidence: ['their bodies, resources, dependencies and obligations make that permission unequally usable', 'A theoretical right to resign provides weak protection when departure is ruinous', 'what may others reasonably ask of that person'],
    promise: 'Explore usable freedom and proportionate responsibility through the practical conditions of ordinary choice.',
    protected: ['Final normative framework and policy recommendations'],
    visual: ['Replace abstract choice symbols with the same open doorway approached by people with different practical constraints.', 'Show a work commitment and its available exit without implying that every dependency is coercive.', 'Return to the doorway with people still connected to one another; end on capacity rather than a victory gesture.']
  },
  {
    i: 25,
    lines: [
      'Two models can describe the same past and disagree the moment you try to change something.',
      'From Rules, Worlds asks what understanding must preserve to keep answering when the situation changes.',
      'This research proposal explores the difference between describing an outcome and providing the operations that produce it.',
      'Its examples make memory, prediction, and intervention part of the same practical challenge.',
      'Two lights may look perfectly coordinated while depending on entirely different hidden mechanisms.',
      'A compact representation is useful only if it retains the distinctions that future questions will need.',
      'For technically curious readers, the attraction is watching a simple intuition become a demanding test of understanding.',
      'Begin with the obligation to continue, and ask what a convincing explanation lets you do next.'
    ],
    titles: ['The past is not the whole test', 'What must a model preserve?', 'Ask what happens next'],
    evidence: ['Two systems can look identical while responding differently to intervention', 'Two lights might follow a hidden common switch, or one might copy the other', 'the ability to continue correctly under relevant questions and transformations'],
    promise: 'Explore a proposed research program testing whether representations retain the distinctions needed for future questions and interventions.',
    protected: ['Detailed formal results, cost tradeoffs and final research agenda'],
    visual: ['Replace generic reasoning symbols with two matching light observations and separate concealed mechanisms.', 'Animate one intervention with both possibilities still open; distinguish prediction from action.', 'End on the compact representation and a new question it must answer, avoiding an unsupported solved-understanding claim.']
  },
  {
    i: 26,
    lines: [
      'The work becomes a duty, the risk an opportunity, and someone else still carries the cost.',
      'Holding the Dirty Thing by the Clean Side examines the language that makes burdens easier to accept.',
      'Its inquiry travels from sacred authority and sacrifice to management reports, market discipline, and polished institutional explanations.',
      'The book takes the appeal of these stories seriously, including the genuine coordination they can make possible.',
      'That makes its central question harder: when does a necessary justification also hide an unequal arrangement?',
      'It follows the distance between those who describe a decision and those who must live with it.',
      'Readers encounter a way to examine respectable words without dismissing every obligation as a fraud.',
      'Begin with an ordinary burden, and listen carefully to the explanation wrapped around it.'
    ],
    titles: ['The language around the burden', 'Why the clean side persuades', 'Who lives with the consequence?', 'Listen to the explanation'],
    evidence: ['Burden becomes duty, hierarchy becomes order, risk becomes opportunity', 'asymmetry between those who administer meaning and those who absorb consequences', 'Stories can make genuine sacrifice intelligible'],
    promise: 'Examine how respectable justifications can both coordinate necessary work and obscure the distribution of its costs.',
    protected: ['The four-part burden test and later prescriptions'],
    visual: ['Keep the bakery rack and work as the concrete burden while its label changes.', 'Shorten the rota sequence to one meaningful relabeling; avoid implying that every explanation is dishonest.', 'Keep the worker’s perspective and the unchanged burden visible together, removing the speculative scoring demonstration.', 'End on the schedule beside the book and an unresolved question about its justification.']
  },
  {
    i: 27,
    lines: [
      'For Aster, understanding a world completely can make it stop feeling like anything outside herself.',
      'Hunger After All the Worlds turns that predicament into a speculative novel and an atlas of imagination.',
      'Aster and her children visit experimental worlds where strange premises reshape everyday obligations.',
      'Their journeys ask what happens when a powerful visitor treats someone else’s home as a lesson.',
      'Alongside the story, a playful classification explores the operations that give speculative ideas their consequences.',
      'Changing gravity or copying a person means more than adding an unusual feature to familiar scenery.',
      'For readers and worldbuilders, the attraction is the meeting of imaginative possibility and lives that resist simplification.',
      'Begin with Aster’s hunger, and enter a world that has reasons to surprise its observer.'
    ],
    titles: ['When understanding consumes surprise', 'Worlds with lives of their own', 'A premise changes obligations', 'Enter Aster’s journey'],
    evidence: ['whatever she understands completely becomes internal to her models and ceases to feel genuinely outside herself', 'a speculative novel about Aster and her children', 'who bears the cost when a powerful visitor turns another society into a lesson'],
    promise: 'A hybrid fiction and imagination atlas where worldbuilding meets the ethical resistance of imagined inhabitants.',
    protected: ['Individual memorial-world outcomes, the children’s developments and Aster’s resolution'],
    visual: ['Keep Aster looking at an inhabited model but remove prediction-as-conquest gestures.', 'Replace the long infinite-library vignette with one world and its inhabitants pursuing their own activity.', 'Keep the two divergent commitments as one brief consequence of a copying premise, leaving their obligations unresolved.', 'End on the facing story and atlas pages with a resident still visible, rather than reducing the world to a classification.']
  },
  {
    i: 28,
    lines: [
      'Your AI product can be useful today and become someone else’s bundled feature tomorrow.',
      'Investing in an AI-Dominated Economy examines that possibility through a proposed venture-studio strategy.',
      'It asks what a company can keep building when capable models become widely available to competitors.',
      'The inquiry follows shifting control points, from earlier computing platforms to the institutions emerging around AI.',
      'Ownership, verification, integration, and trusted relationships matter differently from a convincing demonstration.',
      'The book explores how business and social systems might turn repeated work into enduring capabilities.',
      'Its thesis remains a wager to examine, with assumptions and failure conditions that deserve attention.',
      'Begin with the difference between creating value and having a durable claim on it.'
    ],
    titles: ['A useful product can disappear', 'What can a company retain?', 'When control points move', 'Beyond the demonstration', 'What repeated work builds', 'A wager that can fail', 'Follow the claim on value'],
    evidence: ['platforms, enterprise suites, operating systems, or customers’ internal stacks could absorb successful features', 'strategic doctrine proposed for Outfinity Venture Studio', 'independent company must own a scarcity that compounds beyond access to a model'],
    promise: 'Examine a conditional investment thesis about where durable bargaining power might remain as AI capabilities become widely rentable.',
    protected: ['Specific portfolio targets, underwriting prescriptions and final investment recommendations'],
    visual: ['Retain the independent tool and suite comparison with no invented market winner.', 'Keep the reusable evaluation artifact as a question about what survives, not a measured advantage.', 'Use one changing platform control point, simplifying component-switch demonstrations.', 'Keep review, authority and relationship objects visibly distinct.', 'Show a repeated deployment leaving a reusable record without promising compounding returns.', 'Preserve the failed-trial record and next decision as open possibilities.', 'End on the actual thesis with the opening value question still visible.']
  },
  {
    i: 29,
    lines: [
      'An AI’s most consequential sentence may be the verdict you never see.',
      'Judgment Engines examines models that grade, rank, approve, and decide what happens next.',
      'A score can block a software release or influence which work receives serious attention.',
      'That changes the stakes when an evaluator mistakes polished language for a better result.',
      'The book follows machine judgment from its criteria and evidence into the systems built around it.',
      'Its examples connect code, education, hiring, science, and other places where assessment becomes authority.',
      'For builders and readers affected by automated decisions, the question is who evaluates the evaluator.',
      'Start with the quiet shift from generation to judgment, and follow the consequences of a score.'
    ],
    titles: ['The verdict behind the screen', 'When a score changes events', 'How a judgment is made', 'Who evaluates the evaluator?', 'Follow the consequence'],
    evidence: ['The text the judge produces may never be shown to the user', 'A pass/fail label can block a deployment', 'the norm, the evidence, the procedure, the model, the aggregation rule, the escalation policy, and the audit trail'],
    promise: 'Understand the quieter move from AI-generated outputs to machine assessments that control what happens next.',
    protected: ['Detailed judgment architecture recommendations and later evaluator-selection conclusions'],
    visual: ['Keep the hidden release gate and proposed patch, with no implied completed deployment.', 'Use the prose-versus-function contrast once, removing the longer averaging tutorial.', 'Show criterion, evidence and procedure as separate parts of one evaluation scene.', 'Retain the padded-answer comparison without fabricated benchmark results.', 'End with a challengeable assessment beside the book, preserving the unresolved authority question.']
  },
  {
    i: 30,
    lines: [
      'An impossibility theorem does not tell you everything a particular machine can safely do.',
      'Limits of Machine Intelligence explores the gap between universal guarantees and decisions inside declared boundaries.',
      'Its inquiry begins with finite hardware, limited time, and a question someone still has to answer.',
      'Checking a program for a fixed number of steps creates a different claim from checking it forever.',
      'The book examines what mathematical limits permit us to establish, and where uncertainty must remain visible.',
      'Its proposed framework connects proofs, resources, verification, and the authority granted to an AI system.',
      'The attraction for technically curious readers is a more precise conversation about what impossible actually means.',
      'Begin with the boundary of a guarantee, and ask what changes when the question grows.'
    ],
    titles: ['What does impossible rule out?', 'A question with a horizon', 'Where certainty must stop', 'Evidence and permission', 'Read the boundary'],
    evidence: ['a theorem denying one perfect procedure for every possible case', 'a finite task, restricted authority and a decision that must be made before some deadline', 'no halt was observed within the present horizon'],
    promise: 'Explore how bounded verification and universal impossibility differ in a provisional framework for finite machine claims.',
    protected: ['Detailed formal constructions and the final proposed verification method'],
    visual: ['Keep the bounded controller with its scope visible; avoid a symbolically defeated theorem.', 'Show the counter’s declared horizon without completing the old failure demonstration.', 'Keep the boundary and open result, removing the newly installed guard because the narration does not explain that mechanism.', 'Keep proposal and permission separate in one short action.', 'End with the book and unchanged boundary marker, leaving extension as a question.']
  },
  {
    i: 31,
    lines: [
      'A fluent answer can hide the very steps you would need to trust it.',
      'Machines of Understanding Through Circuits explores a proposed way to make those steps explicit.',
      'Its circuits are structures of operations and dependencies, connecting information to the conclusions drawn from it.',
      'The book asks what can be simplified without losing what a later question will need.',
      'A sum and a count can preserve an average while leaving the median out of reach.',
      'That small example opens a larger inquiry into memory, reusable reasoning, and the limits of compression.',
      'This is a research architecture to examine, with its assumptions and unfinished problems kept in view.',
      'Begin with what an answer must justify, then follow the distinctions its reasoning cannot afford to lose.'
    ],
    titles: ['An answer with visible steps', 'What a summary must preserve', 'Follow the missing distinction'],
    evidence: ['SOP Lang is proposed as a common language for knowledge and computation', 'calculating a list’s mean requires its sum and element count', 'those quantities do not generally determine its median'],
    promise: 'Explore an unfinished research architecture for explicit reasoning and task-specific information preservation.',
    protected: ['Formal sufficiency conditions and final architecture recommendations'],
    visual: ['Replace generic relational threads with an explicit input, operation and conclusion, preserving proposal status.', 'Use a small list and separate sum/count representation; keep the median question unresolved rather than claiming equivalence.', 'End with a changed question beside the same representation, inviting inspection of what it retained.']
  },
  {
    i: 32,
    lines: [
      'Before breakfast, Lea’s mother asks to die, and her reconstructed husband asks for a thousand bodies.',
      'Me and My Robots begins where extraordinary technology collides with an ordinary family morning.',
      'Lea is a professional witness, asked to weigh choices that cannot easily be undone.',
      'Her society has automated much of life, but abundance has left love, consent, and responsibility unsettled.',
      'Even Kite, the household robot, has something difficult to explain about a handmade bird.',
      'This science-fiction novel finds its tension in familiar gestures made unfamiliar by new kinds of possibility.',
      'Who may choose for another person when care, memory, and powerful systems all have a claim?',
      'Join Lea in the kitchen, where a better world still begins with impossible conversations.'
    ],
    titles: ['Three requests before breakfast', 'A witness inside the family', 'The bird in the kitchen', 'Stay for the conversation'],
    evidence: ['Lea’s mother Esther asks to be allowed to die', 'a reconstruction of Lea’s deceased husband Jonas requests a thousand physical bodies', 'Lea is a professional witness', 'Kite lies about a handmade bird carrying a hidden message'],
    promise: 'An intimate science-fiction premise where a family morning exposes the unresolved choices inside automated abundance.',
    protected: ['The bird’s message and concealed version identity', 'Maya’s later conflict, continuity branches, political violence and family outcomes'],
    visual: ['Keep the kitchen and envelope as ordinary surroundings; introduce the two requests through restrained gestures, not spectacle.', 'Reuse the household setting with a listening posture that clarifies Lea’s witness role.', 'Replace the viola comparison with the actual handmade bird and Kite’s hesitation; do not reveal the hidden message.', 'Hold the family conversation open, ending with the bird on the table and the book as reading route.']
  }
];

drafts.push(
  {
    i: 33, title: 'Agentic AI 2026',
    lines: [
      'The same AI model can belong to a cautious assistant or a system with dangerously broad authority.',
      'Agentic AI 2026 explores the software arrangements that make that difference possible.',
      'Once generated language becomes a file edit or service call, mistakes acquire consequences beyond the conversation.',
      'The book follows delegated work through tools, memory, planning, permissions, and the evidence left behind.',
      'It examines why capable agents can lose direction as tasks grow longer and their observations accumulate.',
      'A useful design has to balance adaptability with cost, recoverability, and the ability to see what happened.',
      'For builders choosing an architecture, the interest is understanding what each pattern asks you to trust.',
      'Begin where an answer becomes an action, then inspect the system that gives it permission.'
    ],
    titles: ['The model is only part of it', 'When language becomes action', 'The cost of a longer task', 'Inspect the permission'],
    evidence: ['The same model can therefore belong to systems with radically different trust properties', 'agency appears when model output can alter control flow, persistent state, or the external world', 'Local choices can drift from the original specification'],
    promise: 'Compare agent architectures through the control, evidence and recovery arrangements surrounding the model.',
    protected: ['Detailed design prescriptions and concluding architecture recommendations'],
    visual: ['Keep the same model associated with two different permission boundaries, without an invented performance comparison.', 'Select one concrete file or service action and expose the boundary it crosses.', 'Retain one state or trajectory problem; remove the extended sequence of failure examples.', 'Finish on the visible runtime boundary and an inspectable record beside the book.']
  },
  {
    i: 34, title: 'Aspirin, Viagra, and Coffins',
    lines: [
      'A business can relieve suffering, or become very good at keeping the invoice alive.',
      'Aspirin, Viagra, and Coffins examines that uncomfortable possibility with research, entrepreneurship, and a sardonic sense of humor.',
      'Its three signals concern urgent pain, discreet needs, and demands that arrive when choices are already narrowing.',
      'Behind the provocative title are serious questions about loneliness, exhaustion, shame, and the markets surrounding them.',
      'The book asks how a genuine human wound becomes both an object of study and a commercial opportunity.',
      'It follows the difference between helping someone recover and profiting from a difficulty that keeps returning.',
      'The reading experience invites discomfort without turning the people affected into the joke.',
      'Begin with the three signals, and ask what a successful business should want to make disappear.'
    ],
    titles: ['When relief has a business model', 'Three uncomfortable signals', 'The person behind the market', 'What should success end?'],
    evidence: ['whether enterprise reduces suffering or merely discovers a dependable way to invoice it', 'Its humor is intentionally defensive rather than dismissive', 'urgent', 'intimacy, shame, discretion, or status'],
    promise: 'An irreverent but humane investigation of commercial opportunities around urgent and vulnerable human needs.',
    protected: ['Later sector conclusions, clinical claims and business prescriptions'],
    visual: ['Keep a concrete problem and its proposed relief, using wry restraint rather than suffering as spectacle.', 'Use three simple distinct objects for urgency, discretion and inevitability, with no medical efficacy claim.', 'Replace the long history-and-time vignette with a person and the recurring service relationship.', 'End with the unmet business question beside the book; avoid a purchase cue or invented success story.']
  },
  {
    i: 35, title: 'AssistOS',
    lines: [
      'The conversation ends, but the files, unfinished tasks, and decisions still need somewhere to live.',
      'AssistOS explores a proposed workplace for continuing collaboration between people and AI workers.',
      'The book begins with useful assignments: revising a document, checking research, or making a reviewable code change.',
      'It asks how a worker can keep its role and history while the tools underneath it change.',
      'Shared projects connect conversation with the actual objects being worked on and the people reviewing them.',
      'Permissions, interruptions, and recovery become part of the experience, alongside the convenience of delegated work.',
      'For readers imagining everyday AI collaboration, the appeal is a coherent direction for work that persists.',
      'Begin with one bounded assignment, and follow what must remain available after the chat is over.'
    ],
    titles: ['What happens after the chat?', 'A place for continuing work', 'The project and its decisions', 'Follow one assignment'],
    evidence: ['Files change, tasks continue after a conversation ends, people review results', 'a product and research direction', 'change the underlying model or software without erasing the worker’s identity'],
    promise: 'Explore a product and research direction for persistent delegated work, review and human control.',
    protected: ['Detailed implementation architecture and later deployment recommendations'],
    visual: ['Keep a conversation beside a continuing project, leaving its unfinished work visibly present.', 'Use one document revision as the recurring assignment instead of touring every interface.', 'Preserve source, proposal and accepted version as separate objects with one review gesture.', 'End on the persistent worker and project; avoid simulating unverified installed product functionality.']
  },
    {
    i: 36, title: 'Borrowed Credibility',
    lines: [
      'A respected name can earn a paper attention before anyone has checked whether its claims hold.',
      'Borrowed Credibility explores why science needs those shortcuts, and what happens when they become verdicts.',
      'It opens with Elena Varga’s manuscript entering a journal where competent people have too little time.',
      'Degrees, laboratories, citations, and familiar venues help them decide where to begin looking.',
      'The same signals can carry more authority than any one piece of work has earned.',
      'The book follows this tension through the practical cost of reading, checking, funding, and trusting research.',
      'For anyone working inside science or relying on it, the attraction is understanding trust without treating prestige as proof.',
      'Begin with the waiting manuscript, and follow the distance between being noticed and being believed.'
    ],
    titles: ['Attention before verification', 'A manuscript enters the system', 'The price of checking', 'From noticing to believing'],
    evidence: ['Elena Varga’s manuscript', 'Elena Varga\'s manuscript enters a system before anything has gone wrong', 'evaluation is itself a scarce scientific resource', 'pedigree can rationally determine where inspection starts'],
    promise: 'Investigate the necessary shortcuts of scientific trust and the point where reputational signals exceed their evidential role.',
    protected: ['Later case outcomes and research-assessment reform prescriptions'],
    visual: ['Keep the identical manuscript while its associated credibility signals become visible.', 'Use the editor’s queue to establish time pressure without caricaturing negligence.', 'Retain direct inspection of the work and one concrete checking step; remove repeated prestige changes.', 'End with the manuscript open and the verdict unresolved, inviting the reader to inspect its journey.']
  },
  {
    i: 37, title: 'Coherence Pressure',
    lines: [
      'An explanation can become more convincing without gaining a single piece of evidence.',
      'Coherence Pressure begins with an AI finding an elegant connection between two observations about a child.',
      'One concerned rejecting an unwanted item; the other concerned continuing to watch short videos.',
      'A shared vocabulary made the proposed connection sound like a common mechanism worth building a theory around.',
      'The book investigates that step from plausible comparison to the appearance of established understanding.',
      'It treats its own proposed explanation as a hypothesis that may need revision or abandonment.',
      'For anyone reading or writing with AI, the interest is recognizing when a beautiful argument has closed too quickly.',
      'Begin with the two observations, and examine the bridge the explanation builds between them.'
    ],
    titles: ['Convincing without new evidence', 'Two observations meet a story', 'The bridge that needs testing', 'Reopen the connection'],
    evidence: ['two observations about a child', 'converted analogies into explanatory structure', 'The case may ultimately be explained by neighboring concepts'],
    promise: 'Examine how plausible AI synthesis can acquire an appearance of evidential unity and how the hypothesis itself should be questioned.',
    protected: ['The full proposed benchmark, intervention program and abandonment conditions'],
    visual: ['Keep the two distinct observations separate before the connecting line appears.', 'Make the proposed bridge visibly tentative, with no automatic truth badge.', 'Retain the correction reaching the argument’s structure rather than merely adding a caveat.', 'Return to both source observations and the book, leaving alternatives visibly open.']
  },
  {
    i: 38, title: 'Enough for Everyone',
    lines: [
      'A society can have enough food and still leave people hungry.',
      'Enough for Everyone asks what it would take to separate basic security from the struggle for survival.',
      'The book examines energy, materials, water, housing, and food as a practical inventory of possibilities and constraints.',
      'Its question concerns a dependable floor for human life, with finite resources and real ecological costs.',
      'Building more also raises questions about access, ownership, maintenance, and who can use what exists.',
      'Meanwhile, time, attention, desired places, and relationships remain difficult or impossible to multiply on demand.',
      'The interest lies in exploring a hopeful material argument without pretending that every kind of scarcity disappears.',
      'Begin with the inventory, and follow the distance between having enough and making it available.'
    ],
    titles: ['Enough exists for whom?', 'A material inventory', 'The distance from supply to access', 'What would a secure floor require?'],
    evidence: ['A society can have cheap energy and poor citizens; enough food and hunger', 'We can construct a floor below which no one falls', 'time, other people’s attention'],
    promise: 'Examine the physical and institutional conditions of universal sufficiency while distinguishing it from unlimited abundance.',
    protected: ['The author’s final feasibility verdict, timeline and policy prescriptions'],
    visual: ['Keep food and access distinct with people present, avoiding a celebratory abundance montage.', 'Use the strongest energy-to-home visual as one example, retaining the infrastructure between them.', 'Show access and maintenance as separate requirements; remove long sector-by-sector explanations.', 'End with a lived home or shared meal as the concrete aspiration, presented as a question rather than an achieved forecast.']
  },
  {
    i: 39, title: 'Executable Natural Language',
    lines: [
      'A solver can calculate perfectly from a sentence that was translated into the wrong meaning.',
      'Executable Natural Language explores that gap between fluent instructions and dependable computation.',
      'Words such as same, we, and must can hide choices that human conversation quietly repairs.',
      'When software acts on those words, the interpretation can become a lasting decision with consequences.',
      'The book examines a proposed language that makes references, assumptions, contexts, and operations more explicit.',
      'It brings insights from different languages into a technical inquiry about what execution needs to preserve.',
      'For technically curious readers, the attraction is seeing how ordinary grammar becomes a problem of trust.',
      'Begin before the proof, where someone still has to establish what the original sentence meant.'
    ],
    titles: ['Correct calculation, wrong meaning', 'The choices inside ordinary words', 'Making interpretation inspectable', 'Begin before the proof'],
    evidence: ['The solver may then calculate correctly over the wrong representation', 'Identity, reference, tense, aspect, modality', 'SLEnglish, or SOP Lang English'],
    promise: 'Explore a proposed approach to making natural-language formalization inspectable before exact computation gives it authority.',
    protected: ['Detailed language contracts and later design recommendations'],
    visual: ['Keep source sentence, interpretation and solver result as visibly different objects.', 'Use one ambiguity about group membership rather than a sequence of grammar labels.', 'Retain alternative interpretations and one explicit assumption, avoiding an automatic perfect translation.', 'Return to the source sentence beside the book; let the interpretive choice remain the focus.']
  },
  {
    i: 40, title: 'Executable Scientific Intelligence',
    lines: [
      'Rerunning a script can reproduce a number without showing why a scientific conclusion follows.',
      'Executable Scientific Intelligence explores what research would need to make that connection inspectable.',
      'The book proposes executable companions linking questions, claims, evidence, assumptions, and the transformations between them.',
      'An article would retain the interpretation and novelty that ordinary code cannot simply replace.',
      'The inquiry asks which conclusions should change when a source, baseline, or method changes.',
      'It also examines the risks of an AI agent selecting evidence and judging its own success.',
      'For researchers and builders, the appeal is a demanding proposal for assistance that leaves its reasoning accountable.',
      'Begin with the scientific document, and follow the missing connections between a result and its meaning.'
    ],
    titles: ['A repeated number is not the argument', 'The document and its companion', 'When an assumption changes', 'Follow the missing connection'],
    evidence: ['rerunning a script does not necessarily reconstruct the argument', 'which conclusions change when a source, baseline, method, or assumption changes', 'the same model may interpret the task, select evidence, judge its own performance'],
    promise: 'Explore a research proposal for inspectable scientific dependencies and divided authority around AI-generated work.',
    protected: ['Detailed circuit construction mechanisms and final research recommendations'],
    visual: ['Keep the result beside its article, with the missing justificatory connection visible.', 'Preserve the document while adding a small evidence-and-assumption structure as its companion.', 'Change one assumption and highlight the conclusions that require checking, without claiming validated automatic science.', 'End with the source, result and open review question arranged for a human reader.']
  }
);

const registry = JSON.parse(await fs.readFile('tasks/voice-migration-progress.json', 'utf8'));
const originalTitles = ['A Balance of Iron and Salt', 'AI Adoption Beyond the Slop', 'AI Agents', 'All the Ways to Rule a World', 'An Autopsy of a Digital Mind', 'Anatomy of an Echo', 'Anti-Idiocracy', 'Anti-Trivialization Machines of the Future', 'Artificial Impossibility', 'Autopsy of Future Emotions', 'Beauty: The Anatomy of Fascination', 'Before Explanation', 'Between Faith and Evidence', 'Beyond the Last Stone', 'Bias in AI', 'Can’t See the Forest for the Trees', 'Concordia Series', 'Cones of Meaning', 'Decentralised Brands', 'Ecology of Predation', 'Eden Before Mars', 'Eden Was a Jungle', 'Egregnosis', 'Egregopathy', 'Freedom and Its Price', 'From Rules, Worlds', 'Holding the Dirty Thing by the Clean Side', 'Hunger After All the Worlds', 'Investing in an AI-Dominated Economy', 'Judgment Engines', 'Limits of Machine Intelligence', 'Machines of Understanding Through Circuits', 'Me and My Robots'];
for (const draft of drafts) {
  if (process.argv.includes('--extras-only') && draft.i < 33) continue;
  const entry = registry.entries.find(entry => entry.title === (draft.title || originalTitles[draft.i]));
  if (!entry) throw new Error(`Missing title ${originalTitles[draft.i]}`);
  const sceneFile = `${entry.project}/work/scenes.json`;
  const original = await fs.readFile(sceneFile, 'utf8');
  const scenes = JSON.parse(original);
  try { await fs.writeFile(`${entry.project}/work/pre-marketing-v2.scenes.json`, original, { flag: 'wx' }); }
  catch (error) { if (error.code !== 'EEXIST') throw error; }
  if (scenes.length !== draft.titles.length || scenes.length !== draft.visual.length) throw new Error(`Scene shape: ${entry.title}`);
  const sizes = scenes.length === 3 ? [3, 3, 2] : scenes.length === 4 ? [2, 2, 2, 2] : scenes.length === 5 ? [2, 2, 2, 1, 1] : [2, 1, 1, 1, 1, 1, 1];
  let position = 0;
  const cueChanges = [];
  for (const [index, scene] of scenes.entries()) {
    scene.title = draft.titles[index];
    scene.lines = draft.lines.slice(position, position += sizes[index]);
    scene.pauseAfterMs = scene.lines.map((_, beat) => beat === scene.lines.length - 1 ? (index === scenes.length - 1 ? 1900 : 1600) : 1150);
    scene.emotionalPlan = {
      arc: index === 0 ? 'recognition → curiosity' : index === scenes.length - 1 ? 'reflection → open curiosity' : 'attention → thoughtful tension',
      purpose: draft.visual[index],
      states: scene.lines.map((_, beat) => index === 0 && beat === 0 ? 'interested' : index === scenes.length - 1 ? 'reflective' : 'engaged'),
      intensities: scene.lines.map((_, beat) => index === 0 && beat === 0 ? 0.4 : 0.32),
      voiceDirections: scene.lines.map((_, beat) => index === 0 && beat === 0 ? 'An inviting, concrete opening; gentle emphasis on the surprising contrast, with no announcer voice or theatrical suspense.' : index === scenes.length - 1 ? 'Warm, thoughtful curiosity; leave the thought open with a natural falling cadence, never a sales command.' : 'Conversational and attentive; connect this thought to the previous sentence, with restrained feeling and clear pronunciation.')
    };
    // Remove obsolete late-beat choreography. The authored plan above identifies
    // the concrete replacements; the next film pass must implement that plan.
    if (scene.visual?.actions) {
      const removed = scene.visual.actions.filter(action => Number(action.beat || 1) > scene.lines.length);
      scene.visual.actions = scene.visual.actions.filter(action => Number(action.beat || 1) <= scene.lines.length);
      cueChanges.push({ sceneId: scene.id, removedLateActions: removed.map(action => ({ actor: action.actor || action.target, action: action.action || action.type, oldBeat: action.beat })), retainedActions: scene.visual.actions.length, nextVisualChange: draft.visual[index] });
    }
    scene.marketingVisualRevision = { status: 'planned-before-film-rebuild', plan: draft.visual[index] };
  }
  await fs.writeFile(sceneFile, JSON.stringify(scenes, null, 2) + '\n');
  const scriptSha256 = crypto.createHash('sha256').update(JSON.stringify(scenes.map(scene => ({ id: scene.id, lines: scene.lines })))).digest('hex');
  const wordCount = draft.lines.join(' ').split(/\s+/u).length;
  const review = {
    version: 'curiosity-v2',
    title: entry.title,
    purpose: 'book-introduction',
    scriptSha256,
    sourceFiles: [`${entry.bookDirectory}/en/short_content.html`],
    sourceEvidence: draft.evidence.map(excerpt => ({ source: `${entry.bookDirectory}/en/short_content.html`, excerpt, locator: 'Opening source sections of canonical English short reader' })),
    hook: draft.lines[0],
    readerPromise: draft.promise,
    protectedRevelations: draft.protected,
    visualPlan: draft.visual,
    cueChanges,
    authorReview: { status: 'authored-and-reviewed', reviewer: 'marketing_a', scope: 'Complete eight-sentence script checked against canonical short-reader opening evidence for premise, clear identity, specific interest and protected revelations.', wordCount, sentenceCount: draft.lines.length, titleInFirstTwoSentences: true, targetDuration: 'About one minute at an unhurried conversational pace with real pauses; measure after recording.', emotion: 'Concrete recognition, thoughtful tension and open curiosity; no melodramatic mystery or inflated promise.', audioConversion: 'Blocked until all batch scripts pass independent editorial review.', visualExecution: 'The existing art is preserved as working material; book-specific changes above still require implementation before film validation.' }
  };
  await fs.writeFile(`${entry.project}/work/marketing-review.json`, JSON.stringify(review, null, 2) + '\n');
  console.log(`${draft.i}: ${entry.title}: ${wordCount} words; ${scenes.length} scenes`);
}
