# Paused at the editor's request

Production was stopped on 2026-09-11. Resume only after an explicit user request.
All owned audio workers, coordinator, agents, QA browser and local QA server were stopped. `production-paused.json` prevents an accidental coordinator restart.

Resume from current per-book artifacts and verified clip hashes; never regenerate all cached audio.

- Latest user preference: diversify voices beyond Ryan/Aiden, including other suitable local voices. Local voice audit/casting work by production_2 was interrupted; inspect partial changes before continuing. `migrate-short-film-qwen.mjs` previously overwrote casting with Ryan/Aiden, so explicit override support needs verification.
- Critical: Between Faith and Evidence `how-line-1` has a malformed preamble. Bad audio/cache evidence is archived. A cache-only retake was interrupted; Qwen seeds are explicit and deterministic, so use a genuinely different per-clip seed/take before retrying. Preserve seven good clips.
- Interrupted voice projects: consult production-audio-queue-state.json. Last live jobs were Between Faith and Evidence, Borrowed Credibility and Cones of Meaning. Concordia, Coherence Pressure and Can't See the Forest for the Trees finished their voice batches; verify receipts before resuming.
- Bias in AI v4 was republished at 66.865 seconds after caption/contrast repairs; current expanded QA passed 23 checks/48 frames and independent review passed.
- Beyond the Last Stone: latest independent repair art hash was 6850279fc17a8a6f939171d3b5e71624427a4273f44697757275b20114248da1, but further caption review was in progress. Inspect actual current files/review, not old screenshots. Not yet published in this batch.
- AI Adoption Beyond the Slop: production_1 was repairing actual spoken-midpoint silhouette/caption overlaps. Inspect partially completed current art and review before republishing.
- Coherence Pressure: private narrated build 63.929 seconds; expanded QA found scene 2 sentence 2 Question / Still uncertain cards in caption band. Repair before publication.
- Can't See the Forest for the Trees: private narrated build 79.538 seconds; ASR mostly matched with minor differences; final narrated visual QA/publication still pending.
- Expanded `qa-film.mjs` now captures every spoken sentence midpoint plus scene edges (48 frames for four scenes/eight sentences), and writes explicit failed reports. Old three-sample scene QA could miss caption overlaps. Track the remaining published-film audit in `published-film-caption-review.json`; A Balance of Iron and Salt and Bias in AI passed the expanded actual-image review.
- Recent author/review work: Hunger, Investing, Judgment Engines, Life Without an Audience independently reviewed; inspect canonical hashes and states. Preserve all source scripts.
- Atomic SHF publication and retry/error display prevent status reads of partially written archives from killing unrelated audio jobs. Concurrent-reader regression test passed.
- Skill quality-gate lessons changed through the ScriptaSkillSet symlink and belong to that separate repository.

At resume, clear the pause marker deliberately, start only one coordinator (3 workers, CPU groups1–5/6–10/11–15, CPU0 reserved), and re-create a muted owned QA browser with all AGENTS.md network flags. Verify current state before launching anything.
