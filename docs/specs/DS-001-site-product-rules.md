# DS-001 — Site product rules

Status: active  
Scope: ScriptaHub catalogue, discovery, book pages, readers, workflows, legal pages, and shared presentation  
Audience: maintainers and agents. This is an internal engineering specification, not public product copy.

## 1. Product promise and public language

ScriptaHub is a free library for readers, researchers, and creators who need more depth than short social posts or superficial articles provide. It supports niche knowledge, difficult ideas, research programmes, and speculative worlds through complete books and concise reading editions. Readers can propose, question, correct, and extend editions; useful accepted contributions may be credited.

Public copy explains what a visitor can accomplish, what action will occur, and what information is handled. It must not advertise incidental delivery architecture. Do not describe the site, forms, catalogue, or workflows to visitors as static, prebuilt, generated, backend-free, or temporary because of an implementation limitation. The implementation may evolve without changing the product promise.

## 2. Source of truth and generated output

Each book manifest under `docs/books/<normalised-English-title-words>/<bk-random-id>/manifest.json` is the source record. `docs/collection.json` and `docs/collection.js` are aggregate indexes rebuilt from manifests. `tools/build_books.py` owns route migration, manifest aggregation, edition links, book-page rendering, cover derivatives, discovery metadata, and validation.

Generated files are replaced from their sources. Do not patch generated book pages or aggregate catalogue files to make a durable change; change the generator or manifest and rebuild. A catalogue refresh may run periodically. That cadence is an operational detail and must not appear in visitor-facing copy.

## 3. Page topology

The site has these product surfaces:

- `docs/index.html`: the library entrance, introduction, keyword cloud, featured book, and dynamic keyword results.
- Localised `book.html` files: one book’s title, description, discovery cloud, reading actions, feedback action, edition history, and an About Book presentation.
- Canonical reader HTML: full and ten-minute reading modes, language selection, theme, text controls, and Read Aloud where supported.
- `docs/librarian/`: question-specific recommendations and a separate recommendation-feedback page.
- `docs/create/`, `docs/feedback/`, `docs/editions/`, and `docs/translate/`: proposal, edition-feedback, publication-history, and translation-request workflows.
- `docs/legal/`: terms, privacy, cookies and local storage, legal notice, and AI transparency.
- `docs/status.html`: an unlinked, `noindex` internal maintenance view for animation-voice migration. It reads generated progress data, shows each book’s current narration state and links back to its book and animation pages. It never appears in headers, footers, sitemaps or public discovery.

The shared header places a Home link with a house icon immediately before Create, keeping Create before discovery actions. Home and the ScriptaHub.com wordmark return to the first page with the selected interface language. A simplified full-body icon derived from the shared librarian mascot, including its book and feet, precedes the wordmark and also serves as the SVG favicon, with PNG and multi-size ICO derivatives. The reader retains its book Back action and adds a separate Home action. The shared footer keeps the normal legal destinations visible. Selected interface language is carried by `?lang=` on navigation URLs.

## 4. Catalogue routes

Book routes contain one lower-case, punctuation-normalised folder per English title word, in title order, followed by a freshly random `bk-` identifier. Taxonomy, language, author, and arbitrary category folders never enter a book route.

The English title is established before preparing a new book, including when the original manuscript and its filename are Romanian or another language. The source filename remains provenance and a matching alias; it does not determine the public route. For example, `Responsabilitatea.docx` with English title `Responsibility` belongs under `docs/books/responsibility/bk-<random>/`. Private `tasks/` and `.book-work/` names may follow the source filename. Releases of an existing book retain its identity and route; do not create another book because a source or translated filename differs. The project skill `.agents/skills/scriptahub-book/SKILL.md` documents the operational structure and generation procedure.

Every book manifest has localised title, subtitle, short description, cover metadata, and exactly 100 distinct discovery keywords for each of `en`, `fr`, `de`, `es`, `pt`, `it`, `ro`, and `pl`. Every language has a `book.html` landing page. Newly received books become searchable immediately with `publicationStatus: preparing`; their initial pages may have 10–100 real discovery keywords while editorial work continues. Completed releases require exactly 100. This catalogue and interface coverage is separate from translating book readers: new books and new releases receive English and Romanian complete and ten-minute HTML editions automatically. French, German, Spanish, Portuguese, Italian and Polish readers are translated only in response to an explicit request for that book and language. Missing readers are valid until requested and completed; existing translated editions are preserved.

## 5. Keyword discovery

Keywords are catalogue data. They are specific fields, methods, problems, genres, and concepts that a reader could plausibly seek. A keyword has a stable language-independent identifier and a localised label. Slugs may remain in aggregate data for compatibility, but they do not define public routes.

There is no per-keyword HTML generation and no `docs/keywords/` directory. Creating one page for every translated term multiplies files without adding a distinct product surface and is forbidden.

The stable keyword URL contract is:

```text
index.html?lang=<supported-language>&keyword=<stable-keyword-id>
```

On the home page, choosing a cloud term updates browser history, resolves the keyword identifier in the selected language, filters `collection.books` by exact membership in `book.keywordIds`, and renders the matching book cards in the page. Changing language preserves the identifier and changes the localised label. Back and Forward restore the selected filter. A book-page cloud links to the same home-page URL contract. Fullscreen discovery opens `librarian/index.html?lang=<code>#request=<localised-keyword>` and immediately shows matching recommendations, whether opened from the homepage or a book. Both pointer selection and accessible keyword links use this route; embedded catalogue links retain the stable keyword URL contract.

The non-visual cloud navigation contains the same destinations so keyboard and assistive-technology users receive real links. Missing or unknown keyword identifiers produce the ordinary unfiltered home page.

## 6. AI Librarian

The AI Librarian accepts a question in the visitor’s own words and returns at most ten catalogue recommendations. Ranking currently runs in the browser over every localised title, source aliases, the selected-language subtitle, description, category, and discovery keywords. This lets a visitor find the same book by its English route title, translated display title, or delivered source name regardless of interface language. Title, alias, and keyword signals carry more weight than general description text, and character-level matching tolerates modest spelling or word-form differences.

The result page opens directly with recommendations for the submitted question. It does not repeat the question form above the results. A restrained “Help improve these recommendations” action follows the list and opens the separate feedback page with the original question available as context.

Visitor-facing text describes personalised recommendations and how to ask a useful question. It does not expose ranking names, weights, indexes, or other implementation details. Legal and privacy text may describe the categories of information compared and whether a question leaves the device, without naming the ranking algorithm.

## 7. Cards and actions

Catalogue, keyword-filter, and Librarian result cards use the book thumbnail and one clear `View Book` action. `Read in 10 min` and `Read Online` appear only on the book page. Book pages keep `Suggest An Edit` as the visually primary editorial action and capitalise `Read Aloud` consistently.

All book descriptions are authored editorial metadata in `manifest.shortDescription`, with six short sentences per supported language (at most 22 words per sentence). They state the book's specific subject or fictional premise, scope and central message in natural language. Nonfiction descriptions may state the book's thesis, while clearly qualifying proposals and speculative claims; fiction descriptions withhold endings and twists. Do not extract the opening paragraph, a table of contents, numbered headings, generic shelf copy or a resolution. Localisations preserve the same meaning rather than copying unrelated reader fragments. Reviewed descriptions carry `shortDescriptionEditorial` provenance and are protected from legacy enrichment and recovery commands. The catalogue check validates sentence count and length; `tools/catalogue_descriptions.py` validates coverage, duplicates and independent review before installing a complete revision.

`docs/assets/book-view.js` is the shared book-view component for the featured card, catalogue/search cards, Librarian results, book-page description and workflow context cards. Its localised model and rendering helpers own the title, description, cover and standard action structure. The full page retains generated, readable HTML as a fallback, then hydrates its copy from this component. A single observer mounts inserted presentations, suspends them behind loading gates and disposes removed instances. Do not add separate card-specific description rendering or initialisation paths. `refresh` fingerprints shared assets in page URLs, preventing cached code from disagreeing with newly generated markup.

The independent `textShow` component (`docs/assets/text-show.js` and `text-show.css`) owns sentence segmentation, progressive word rendering, playback timing, visibility suspension and completion. The homepage welcome uses a separate narrated SHF film launched by the librarian mascot; `textShow` remains the shared engine for book descriptions. Every short-description card (featured, book-page description, catalogue/search, keyword results and AI Librarian results) uses a silent `textShow` without playback controls, voice actions or a full-message dialog. Its first sentence stays visible while waiting; playback starts when its description becomes visible, pauses outside the viewport or in a hidden tab, and leaves the final sentence visible in result cards. On the book page, `loop: true` repeats all six sentences continuously while visible. The featured card uses `loop: false`, completes once, then yields to the next book. Looping is a component option, not a separate player implementation. Assistive technology receives the complete description once. Reduced-motion mode shows the complete card description without animation.

The featured book can rotate only after its own `textShow` completes, including the final sentence's word animation and reading hold. Loading and hidden time do not count toward presentation time. Hover or keyboard focus on the featured card/cover delays replacement. Changing interface language or replacing results disposes old presentations before mounting new instances. Reserve enough space for the longest sentence to prevent per-sentence layout jumps.

Cover derivatives trim empty export margins, then fit the complete artwork into the portrait canvas using the source corner colour for any added space. Never crop remaining artwork to force the aspect ratio: typographic titles, subtitles and authors must remain visible. `cover.png` stays unchanged; `cover.webp` is 640 × 960 and catalogue `thumbnail.webp` is 320 × 480.

Clicking the cover on a book page opens an in-page modal preview, with a visible, localised close control. Escape and a backdrop click also close it, restore focus to the cover and preserve the book page and scroll position. Never navigate the visitor to a bare image without a return action.

Every book page includes an `About Book` section (`Despre carte` in Romanian, with equivalents in all eight interface languages). This heading is independent of the `Read Online` action, which continues to open the full reader. The section contains an inviting, book-specific presentation grounded in the canonical English reader: its central question or story premise, what readers will encounter, and the reason to explore it. Keep it within one page of prose and a few minutes of reading: 2–4 paragraphs, 60–250 words in each language. Paragraphs use the full available section width within the shared gutters, without an additional line-length cap, and use justified alignment with natural wrapping. Avoid generic library slogans, copied publication notices, plot resolutions, or claims that a speculative proposal is established fact.

Store the presentation as an `aboutBook` map of language codes to plain-text paragraph arrays in each book manifest. Author and localise this metadata separately from the short description and from full or ten-minute reader editions. The page generator must render those paragraphs directly, escape them as text, and never substitute a generic introduction. A new book needs this copy in all eight languages before publishing its landing pages; `refresh` rebuilds the aggregate and pages from manifests, and `check` validates the presentation's length, completeness, heading, and agreement with its source.

On narrow screens, a result card begins with a two-cell action row: cover on the left and actions on the right; descriptive text follows below that row. Discovery keyword chips are hidden on mobile. The featured information panel and the desktop book-page information panel have exactly the cover's height. The shared book-view component supplies one cover-height measurement to their common styles. Keep the text and actions together in a vertically centred group, with equal padding above and below actions; never push the buttons away with an automatic margin or stretch the panel to a taller enclosing row. At book-page widths up to 1100px, put the description beneath the cover/action row so long titles remain readable; the action panel still matches the cover's height. The home feature stacks its cover and information panel below 861px. Descriptions are never line-clamped. If accessibility settings enlarge content beyond the matched height, preserve access through panel scrolling and safe alignment rather than clipping it.

Every labelled primary action uses the shared action font size, icon box, and icon-to-label gap. Icons reinforce action meaning but never replace an accessible label, except the Dictate control, whose visible icon has an accessible name and tooltip. Read-mode actions keep vertically centred labels.

## 8. Keyword cloud interaction

The embedded and fullscreen clouds share one component and one collision model. Keyword size combines catalogue popularity with projected 3D depth. Collision testing uses the rendered text bounds after scale, perspective, and rotation; a smaller rear term yields to a larger visible term, while ties are resolved deterministically enough to avoid flicker.

Background keyword clouds on the home page and book pages sit beneath a non-interactive frosted-glass layer: a neutral tint at approximately 50% opacity, a subtle 0.8px blur and restrained saturation. Light and dark themes use their respective floor colours. Apply the layer only to background clouds, above the canvas and below foreground book content; pointer and keyboard interactions must still reach the canvas. Fullscreen discovery stays clear for deliberate exploration.

Dragging rotates the cloud. Ctrl-drag pans the camera. Wheel and pinch zoom toward the pointer or touch focus rather than toward a fixed centre. Embedded clouds accept these interactions where the background remains exposed. Fullscreen close restores the embedded cloud’s suspension, dimensions, and centred usable frame. Embedded mode does not display interaction instructions over the visual.

## 9. Visual system

The page reads as a compact tower of clear horizontal floors. Section boundaries come primarily from background and contrast changes, with restrained borders and small corner radii. Light Green, Light Orange, Light Linen and Dark keep the same dimensions, hierarchy, spacing, and interactions; only their colour tokens change.

Light theme uses a calm neutral grey for the header, footer context, fields, and keyword-cloud floor, white for primary reading surfaces, and WhatsApp-inspired green for primary actions and selected states. Dark theme mirrors the hierarchy with true black primary surfaces, one calm dark grey for secondary floors and controls, muted cloud colours, and restrained green accents. Avoid adjacent near-identical greys that create visual noise.

Light Orange is an additional opt-in site appearance: saturated orange `#ff7900` replaces the green brand band and translucent homepage strips, with dark burnt-orange primary actions, warm keyword colours, a matching full-body mascot/logo, and the same recessed grey secondary choices. The appearance control cycles Light Green → Light Orange → Light Linen → Dark, persists across pages, and applies before catalogue loading. Readers preserve the orange accent in paper mode. Existing Light Green and Dark remain available. The film player retains its independent Color, Light and Dark themes. Light Linen replaces the previous blue palette with warm ivory (`#f4f1ee`), greige bands (`#d9cec5`) and muted burgundy actions (`#684653`). Only colours change; all geometry, shapes and interactions remain shared. The legacy `nord` storage key now resolves to Linen, preserving existing selections without retaining a fifth theme. Orange uses the Orange brand’s [documented logo colour](https://boosted.orange.com/docs/5.3/about/brand/), `#ff7900`, for its primary accent. Every appearance persists in `scripta-site-theme`; the last light variant also survives a reader round-trip through Night.

The whole site tower narrows on wide screens: header background, grey/cloud
floor, reading surfaces and footer share the same centred outer bounds. Preserve
ordinary desktop dimensions; add outer space smoothly above 1440 CSS pixels.
Use shared `--wide-screen-inset: max(0px, min(220px, 30vw - 432px))` and set the
shell width to the smaller of `80% - 2 * --wide-screen-inset` and
`--content-max + 2 * --tower-gutter`. The content maximum is 1760px; the ordinary
inner gutter is `clamp(24px, 4.5vw, 68px)`, or 20px on small screens.
This moves the extra wide-screen spacing outside the tower, preserving the
already approved central content width and a modest inset for the two homepage
strips within the cloud floor. Never leave header/footer backgrounds at their old
wide bounds or apply the wide-screen reduction a second time inside the shell.
Implement these tokens once in shared CSS for home, book, librarian, legal and
workflow pages. The reader retains its own bounded reading measure. Desktop and mobile preserve a clear alignment line between headings, text, inputs, covers, and actions. The header remains compact on mobile: the wordmark has its own line and the controls form one line below it, with text labels removed from Create and Ask AI Librarian where space requires. The footer remains at the bottom of short pages without leaving a strip beneath it.

## 10. Home-page loading state

The homepage librarian and its choices render before the catalogue is available. Confine the loading indicator and busy state to the featured-book strip while its content and cover initialise. Visitors can write a librarian question immediately; their text survives catalogue initialisation. Match the loader to its foreground strip and remove it promptly, without artificial delays.

## 11. Reader editions

Reader editions are canonical HTML. Repairs and translations use the chunk workflow in the `book-reader-translations` skill. PDFs remain English source editions and are not translated. The reader keeps language selection usable and uses the same single-state light/dark toggle as the main site. Compact mobile reader headers and footers must not overlap content or wrap into chaotic control rows.

The language selected in the header is the preferred reading language. Book pages have no additional reading-language selector. Full and ten-minute actions open that language's exact format when available, otherwise the same format in English, preserving `lang` in navigation. The reader header uses the same language preference and English fallback. Never substitute a short edition for a complete book or a complete book for a short edition. If neither the selected nor English format exists, its reading action is unavailable rather than linking to a nonexistent file.

When a selected-language format is missing, show the localised “This reading edition is not yet available in …” sentence as a link to `translate/index.html`, preserving book, target, format and interface language. This notice is the request entry point; reading buttons and language options must not append “Request translation” or its equivalents. Changing language or clicking an ordinary reading action never opens the request form. Current book-page and reader PDF downloads always use the English source PDF, independently of interface or HTML reading language. Preserve archived edition downloads.

Read Aloud reports useful ScriptaHub context when speech output cannot start, rather than exposing device capability diagnostics or redirecting the visitor into the text presentation.

## 12. Proposals, feedback, and editions

Feedback, edition-history and translation-request pages keep a localised `Back to book` action at the top left, before the page heading, preserving the interface language. Their headings are compact, use the available width and stay on one line; exceptionally long headings truncate visually while retaining their full accessible text and title. The book context repeats the complete title. Heading, lead and content share the same page gutters; these utility pages do not use oversized promotional headlines.

Create and feedback forms open a structured email addressed to `create@scriptahub.com`. Public copy states this direct outcome. Because an email link cannot attach selected local files, the interface must clearly tell visitors to attach those files in their email application. This functional disclosure remains until the transport changes; do not explain it as a missing backend.

Translation requests use the same mailbox. The form shows the book, requested language and complete/ten-minute HTML format, with optional name, reply email and message. The visitor opens, reviews and sends the email. No email is sent by selecting a language or opening the form. If a selected translation is already available, offer its reader instead of an unnecessary request.

The Create form groups name and reply email, promotional website and one proposed title, plus a compact attachment area as a third visual column where space permits. Attached filenames appear as bounded pills with a shortened stem and visible extension. Instructions for the book receive the main writing area. The contribution agreement is a separate shared final step at `agreement/index.html`, after the form’s Next action and before opening email.

Every book root owns `editions.json`. Existing records and downloads are preserved. Replacing a current PDF means archiving it under `edition-files/<edition-id>/<language>.pdf`, pointing the old record to the archive, and appending a new dated edition with a localised change log.

Each edition also owns a `covers` map to preserved artwork under `edition-files/<edition-id>/covers/`. Edition-history cards show that edition's cover alongside its date, change log and downloads. Snapshot known current artwork when establishing this history; never invent an old cover by substituting a newer one. Inspect the cover from every new source delivery and update all active cover and thumbnail derivatives when publishing it. Pending editions may show their new cover while the previous published edition remains current. Published cover snapshots must never be overwritten.

History uses a compact cover column and an adjacent text column, including on narrow screens. Align status or date, edition title, change log and downloads beside the image, without an empty metadata column. Dates use the locale's month/day/year ordering without a `Published` prefix. If no historical cover is known, let the text use the full row.

For a book with a published edition, show a pending release's preparation status only in edition history. Do not put a new-edition notice on its book page or catalogue cards. A completely new book with no published edition still carries its brief `In preparation` label until it is ready.

Book-maintenance work begins by scanning `tasks/` for PDF, DOC and DOCX sources. Normalised filenames identify books; trailing `_v2`, `_v3`, etc. identify source versions and are excluded from title matching. An unsuffixed first source is version 1. Matching sources create releases under the existing book ID and route; genuinely new titles receive a new route and random ID. Source hashes prevent repeat ingestion. Stage and validate both EN/RO reader formats and refreshed descriptions, presentations, keywords and covers before installation. Archive previous readers and their local assets together with downloads, and associate older translations with their historical edition. The detailed procedure is in `DS-002-book-releases.md`. Completed DOCX deliveries are removed from `tasks/` after validated conversion and PDF installation, with an identical source retained in the edition archive; unfinished deliveries remain queued.

On intake, expose the book landing pages and a pending edition-history record immediately, even while the book is being prepared. Mark them clearly as `In preparation` in the selected interface language. A pending edition has `status: preparing` and `startedAt`; it has no publication date and does not replace a previous current edition. Search includes titles in all languages, source IDs and filename aliases, with spaces, underscores and hyphens treated consistently. The ongoing work is recorded in `tasks/RELEASE-PROGRESS.md` and `tasks/release-progress.json`, including source hashes, stable IDs, workspaces, completed chunks and remaining checks. Update that ledger throughout work and resume from it after interruptions.

## 13. Privacy, legal, and AI communication

Legal pages remain easy to reach and distinguish confirmed behavior from placeholders that require operator or counsel input. Privacy copy states what hosting, local preferences, dictation providers, email providers, and reader analytics may process. AI transparency explains that books can be AI-assisted, that recommendations are relative catalogue matches, and that editorial responsibility and correction routes matter.

No public legal or product text should freeze the service into its current delivery method. Claims about data handling must remain precise even if the transport changes; update privacy and AI pages alongside any architecture change that changes those claims.

## 14. Validation and change control

After a catalogue, generator, route, or shared interaction change, run:

```text
python3 tools/build_books.py check
python3 tools/audit_internal_links.py --check
```

Also syntax-check changed JavaScript and Python, run `git diff --check`, and verify these invariants:

- `docs/keywords/` does not exist.
- No source or generated book page links to `/keywords/<language>/<slug>/`.
- Keyword URLs use a stable identifier and preserve `lang`.
- All eight supported languages resolve the same identifier to a localised label.
- Catalogue cards expose one `View Book` action; reading actions stay on book pages.
- The AI Librarian returns no more than ten results and feedback follows the result list.
- Public copy does not describe the site or workflows as static, prebuilt, generated, temporary because of architecture, or backend-free.

A deliberate change to one of these decisions updates this specification, its implementation, generator checks where practical, and any affected public privacy or legal statement in the same change.

## 15. Narrated SHF book presentations

A book may offer a source-grounded SHF animation on a dedicated page under
`docs/books/<book-route>/Animation/index.html`, beside its language folders. Its book-page action list shows
`Animation` when an animation is registered in the source manifest. The optional
`animation` record contains paths relative to the book root (`page`, `shf`),
`language`, `edition`, `durationMs`, and `status`. Both paths must belong to this
book’s `Animation/` directory.
The aggregate copies this record with paths resolved relative to `docs/`.
Catalogue cards retain their single View Book action. Animations appear only
on their own presentation page, reached from the book’s Animation action; do
not add them to the home-page body. There is no `featured` field.

Requested presentations default to English script, screen text, transcript,
and narration; they are independent of the eight interface languages. Do not
create additional presentation translations automatically. Keep `?lang=` in
navigation; the film remains English when interface language changes.
Default book introductions to one to two minutes, with a two-minute maximum, adapting the
accepted source edition with provenance retained in metadata and QA. Open with
a concrete, source-grounded hook and identify the book within the first two
sentences. Convey its premise, human stakes, distinctive approach and an inviting
open question in roughly 85–150 words. Marketing copy should earn curiosity
without revealing fictional outcomes or promising unsupported benefits. Preserve
natural pauses and shorten content rather than accelerating speech. The current
migration includes all books, including films previously longer than five minutes.

During the short-film migration, rewrite and independently review the entire
script batch before voice conversion begins. Store a review tied to each script
hash; changing the wording invalidates approval and the affected recordings.
The unlinked status page shows exact proposed narration, source-specific visual
plans, editorial review state and remaining production work. Distinguish existing
voice recordings and published duration from the proposed voice and duration
target. Planned visuals are not completed films, and synthesis does not establish
listening approval.

The status dashboard tracks Text, Animation and Voice as separate tasks for
every book, with active work first and exact narration under “Spoken script and
film plan”. Refresh data automatically every 60 seconds and on returning to the
tab; preserve expanded scripts and the search query. Stage transitions and
failures must update the durable per-project progress record and regenerate
the dashboard data. Never equate an authored visual plan with a finished film.

Standardize SHF delivery, typography, single-sentence captions and pacing, while giving each book its own source-grounded visual identity and composition. Science-fiction introductions establish the premise, questions and reader fit without revealing later twists or resolutions. Use source-appropriate nonhuman forms when the story has no human characters; do not copy the AssistOS cast or visual staging.

Narration is included by default. If no audio engine is configured, report the
absence, create project configuration/templates, and prepare a small local
neural English voice (initially Piper en_US-ljspeech-medium), without requesting
confirmation already provided by the workspace. Private dependency/model
installation is authorized for this fallback. Preserve selected cloud providers;
never switch silently after a provider failure. Keep private runtime, model,
credentials and cached takes outside public assets and ignored by Git.

Every SHF embed derives transport, progress/volume, focus, selected controls and drawer colours from the current site theme through shared CSS tokens. This includes book pages, the librarian dialog and fullscreen; do not hardcode a green accent per film. The artwork palette remains independently selectable.

The public player uses the supplied SHF runtime, actual measured narration,
chapter navigation, captions, playback speed, mute, seeking and fullscreen.
Retain voice provenance in metadata and QA. A trusted, unmodified same-tab click
on a book's Animation action starts its narrated film after loading, without a
second Play click. Carry this intent with a single-use session token matching
the destination and a short expiry, then remove its URL fragment immediately.
Direct links, copied URLs, reloads, modified/new-tab clicks and background loads
remain paused. Hiding the page, pausing or leaving cancels a pending start; becoming
visible again does not resume it. If audible autoplay is denied or its audio
unlock stays suspended, return to a usable Play control rather than running a
silent film or reporting a false page-loading failure. Keep narration and the
interface language unchanged. The presentation page includes a contextual improvement form below its player.
Do not append production notes, downloads, chapter lists or transcripts.
Keep chapter navigation and the full transcript inside the player. Single-film
standalone exports show only the player. Place three accessible Color, Light and
Dark theme choices directly in the bottom transport bar, rather than requiring
the settings drawer. Keep the SHF and a generated entry page in the book’s Animation folder; optional
self-contained HTML exports live outside public book folders.
Measure final duration from audio,
retain source edition/hash, editable direction, receipts and truthful QA in
`presentations/<presentation-id>/`. A later book release must not silently
relabel an older animation as an adaptation of the new edition.

On small screens, the animation page uses the available viewport width with the shared gutters. The SHF player reserves a separate caption/transport area below the artwork; narrow embeds wrap controls into two rows. Captions must not obscure the explanatory illustration.

Presentation narratives use source-grounded why, how and what, integrated into
an explanation of the document’s distinctive ideas. Preserve technical definitions
and relationships, and omit generic motivational text or unsupported novelty.
The first one or two sentences introduce a source-supported distinctive insight;
the opening establishes why the document deserves attention within 20–30 seconds
and the explanation subsequently pays off that promise.
Every narration clip contains exactly one sentence; captions display that whole
sentence alone for its measured interval. Edited text invalidates its old voice
receipt. Keep browser automation muted before scheduling audio and stop owned
players during cleanup; audible listening starts through the visitor’s action.

SHF presentations are illustrated theatre: the script includes an emotional plan
and varies curiosity, tension, discovery, reflection and earned relief as supported
by the source. Human characters retain identity while changing expressions,
gaze, posture and articulated gestures tied to individual sentences. Deliberate
stillness contrasts with more expressive passages; avoid a uniformly flat delivery
or unrelated looping motion. Reduced motion preserves explanatory and facial
states while suppressing nonessential gesture movement.

Animation entry pages contain only the book identifier and shared asset references.
`tools/build_books.py refresh` generates them for every registered animation from
one template. `docs/assets/animation.js` owns the shared page shell and interaction;
provenance stays in film metadata and QA, with no hardcoded book names or edition
numbers. `docs/assets/shf/` owns the single runtime, and `tools/shf/` owns reusable
stage authoring. Reject extra runtime or copied UI files in a book’s Animation
folder during catalogue validation.

All three film themes use a flat background with no decorative frame, nested
panel, outline or arbitrary line. Keep only meaningful foreground elements and
necessary relationships. Show one short scene title in the player header, without
an SVG duplicate, large subtitle, chapter banner, folio or competing page heading.
Validate separation among text, moving actors, props, captions and controls in
Color, Light and Dark; passing one theme is insufficient.

SHF narration favors 8–16-word sentences, one idea at a time; review and simplify
sentences exceeding 20 words without losing technical meaning. Source diagrams
and photos are optional explanatory material: inspect them, adapt useful ones
to the film's visual style without altering evidence, and omit unsuitable ones.
Record those decisions in the authoring workspace. The movie page shows neither
source/production boilerplate nor an external duration/language badge; playback
time belongs in the player. Reusable lessons from SHF reviews are incorporated
into the creation skill during the same authorized task.

Book-page animations default to a reading invitation. They establish the book’s
reason to exist, distinctive messages, actual contents and reader gains, with
a few substantive content samples. They distinguish speaking about the book,
entering its subject and explaining the reading value. A technical book must not
automatically become a product demo or tutorial. The final invitation identifies
a concrete reason to read and a useful source section to begin with. This purpose
is reviewed before voice production and takes precedence over a genre template.


## 16. Librarian entrance and site presentation

The homepage has two aligned strips over the shared word-cloud discovery area:
the librarian first and the featured book second. Give them the same full width,
left illustration column, content alignment, rounded corners and spacing. Use
a 70% light/dark veil over the word cloud. Light-theme foreground strips use
the header band’s green (`#00a884`) at 85% opacity (15% transparency),
with a light 0.8px backdrop blur so discovery keywords remain subtly visible.
Apply transparency only to the background, preserving opaque text, covers,
mascot and controls. Dark green text stays legible against the softened green. Light-theme buttons across navigation, book actions,
librarian, workflows and the reader use a darker green (`#075e54`, hover
`#064b43`) with white text, with deliberate exceptions: Create, scale and theme
controls in the header use the bright background green; Home, View Book and
the two homepage librarian choices use quiet grey (`#e3e8e7`, hover `#d7dfdd`),
dark labels and a restrained inset shadow, like recesses in the surface. Share
the inset colour and shadow tokens; avoid raised shadows or glossy effects.
Preserve the existing Dark-theme colours. Keep actual
content fully opaque. Avoid floating 3D objects and cast shadows. On desktop,
the featured cover defines the adjacent copy bounds: From the shelf starts at
its top edge and View Book ends at its bottom edge, without extra outer margins
or action padding. Both entrance strips share the resulting height.

The entrance contains the shared academic robot and two primary choices in this
order: **Ask AI Librarian**, then **Why ScriptaHub.com?**, localised with the
interface. There is no hero title or introductory paragraph. The header retains
Create, appearance, scale and language controls, without a duplicate Librarian
action on the homepage.

The mascot uses understated spectacles, a book, forest-green tailoring, ivory
and brass. Keep it approximately the height of the two choices. At ordinary
desktop sizes the unfiltered initial page should fit vertically without clipping
content or disabling document scrolling. Expanded input, filters, narrow screens
and enlarged text may require scrolling.

The mascot’s one editable vector source is `docs/assets/librarian-mascot.js`.
The homepage and film consume this identity. Shared UI and styles live in
`home-librarian.js` and `home-librarian.css`. Respect reduced motion.

Ask AI Librarian replaces the two choices with a labelled input in the same
area, beside the mascot, without moving the strip. A top-right close control
and Escape restore the two choices and focus. Place close, dictation and submit in one evenly spaced right-hand column,
with equal 32px circular controls and centred SVG icons. Keep the input beside
the column, with no text under the controls. Use the shared browser dictation
module before catalogue loading; start the microphone only on a Dictate click,
append recognized text, and stop on close, submission or a language change.
Expose listening/error status and disable dictation with a clear accessible
reason when unsupported. Preserve entered text across interface-language changes.
The mascot and its controls initialise before the catalogue script. Confine
the initial loader and busy state to the featured-book strip; visitors can
start writing while the catalogue downloads. Submission uses the existing recommendation route, with the interface language
and question fragment preserved. Links ending in `#ask-librarian` reveal it.

Why ScriptaHub.com? opens a viewport-filling, closable native dialog with the
shared SHF player. Start narration only following that visitor action. Escape
and the close control stop playback and restore focus; closing during loading
cancels the pending start. The site tour lives in
`docs/assets/films/library-introduction.shf`; book films stay book-local.

The English site tour first explains the library's reason to exist: complex
subjects benefit from the depth of books, but a small audience may not justify
conventional human authorship economically. AI makes more niche books feasible.
Experts contribute questions, structure and corrections; AI develops books and
new editions using that guidance, with readers contributing further scrutiny.

A well-scoped, well-written book lets many readers reuse the human thinking that
shaped it, including questions they might not have known to ask. For deep study,
this can outperform repeatedly starting an agent conversation and reduce repeated
AI computation, energy and cost. These are conditional benefits, not measured
savings or a claim that every book beats every conversation. Science fiction and
other literary forms also benefit: small audiences can sustain valuable cultural
diversity even when mainstream distribution would overlook them.

Lead discovery through **Ask AI Librarian**, then explain short/full reading
editions, language availability and contribution actions. Do not narrate temporary
email transport in the film; retain accurate instructions in the actual forms.
Do not imply that planned account-based contributions already exist. The film
balances this purpose with a concise visitor orientation. Use collections for
the library, volumes for books, and varied causal diagrams, interface close-ups,
comparisons and mascot scenes. Reusable thinking is represented by a book serving
many readers, not a fabricated numeric savings chart.

All SHF presentations use short single-sentence narration with deliberate real
pauses, normally 1.0–1.5 seconds between sentences and longer scene transitions.
Do not accelerate speech to fit a duration brief. The shared player shows one
confident scene heading: large Red Hat Display Bold, natural sentence case,
slightly tight spacing and high contrast, in a dedicated area clear of artwork
and captions. Short labels use Red Hat Display SemiBold; narration captions use
Red Hat Text Regular. Bundle the original OFL fonts in the shared player so
rendering is consistent and requires no external font service. Shared book illustrations use
coherent covers, spines and page blocks. Reusable authoring, narration and
publication code lives in `tools/shf/` and the creation skill.


## Book animation proposals and derived books

Every book page exposes Animation, including books without a film. Ready films
open their book-local Animation page; missing films open the shared animation
proposal workflow with the source book and interface language retained. A shared
form below each book player accepts suggestions for improving its narrative or
visuals. These forms prepare an email for the visitor to review and send, using
the same contribution terms as existing editorial suggestions; they do not claim
automatic delivery. No film payload or reusable UI is copied into missing-film
book folders.

Every book also exposes Fork, a source-aware Create workflow for a derived book.
The visitor describes what to retain and change, the new audience and purpose,
and may select additional documents. The proposal preserves source book ID,
title, directory and available source edition. Selected files must be attached
by the visitor in the mail client, as in Create. Shared workflows support all
eight interface languages and retain ?lang=.

New book introductions normally last 5–10 minutes. Their opening identifies the
book, why it merits reading and its central message/direction before examples.
The spoken narrative develops why, how and what coherently; hidden editorial
labels are not evidence that viewers can follow it. Every book receives a unique
visual direction with verified bundled display typography and readable headings.


The appearance cycle now includes Light Green, Light Orange, Light Linen,
Dark Green and Dark Orange. Dark Orange inherits the dark layout and uses
#ff7900 accents with dark ink on orange buttons. Both dark themes use a black
outer surround beside the charcoal keyword-cloud area. Dark Orange uses black for the outer top band behind the main site shell,
matching the outer surround. Its footer remains #ff7900 with dark text;
its panels use neutral charcoal, not brown. The last selection stays
in local storage; reader Night mode preserves the selected dark variant as well
as the last light variant. Player controls and discovery graphics follow the
site palette; the film artwork retains its own theme choices.

Scene visuals must make the particular narrated relationship intuitive, using
source-specific action and consequence. Repeating generic asset arrangements
with changed labels or colours does not constitute a distinct visual direction.

The saved theme is applied synchronously in each page's head before stylesheet
paint, including generated book and animation pages. The reader also initializes
its app palette immediately when its shell is parsed. New themes must be added
to this early bootstrap, not only the interactive selector. Fingerprint reader
CSS/JS alongside other shared assets. Verify navigation and refresh with external
application scripts blocked so a light-green flash cannot be masked by fast JS.


Dark Orange is the default when no valid saved theme exists, including the
synchronous head bootstrap and reader. Preserve an explicit saved preference.
Its logo/navigation bar is near-black (#080808), with the orange band behind it.
The additional short book-introduction batch targets 2–3 measured minutes,
concentrating on the book's message, questions and reason to read; preserve
original visual identity and source-grounded curiosity without fictional spoilers.


On book pages, Animation is the first reading action, before Read in 10 minutes.
Fork, Suggest and Editions form an equally sized vertical right-hand rail
on desktop. At narrow widths this group moves below the book content and wraps
into a vertical stack on small phones. The reading action group stays separate.


All book-related workflows (feedback, editions, translations, Fork and animation
proposals) share the compact `data-book-workflow` heading style. Use a small
single-line heading, restrained lead and tight vertical spacing; never inherit
a large marketing hero when adding a new contextual form. Keep the source-book
reference compact so the form starts high on the page.

The desktop contribution rail lives inside the shared book-details surface,
without its own panel or separating background gap. Its buttons are equal
34px-high single-line controls; the English feedback label is “Suggest”.

Align the desktop contribution rail with the top of the book copy and its first
text line, never vertically centre it beside the description.

Presentation hosts use a visible X alone, without text, fill or border, directly
above the player at its right edge. Retain a localised accessible name and a
44px hit target. Home closes its dialog and stops playback; book presentation
pages return to the source book and pause playback.

All catalogue books should have an English narrated book-introduction animation.
Complete missing films as concise 2–3 minute invitations, while preserving
existing longer presentations. Use richer, varied foreground colours and a
slightly brighter emotional tone where the source supports it; serious subjects
retain their gravity. The site default remains Dark Orange (Orange Black),
including the pre-render bootstrap; preserve an explicitly saved theme choice.

On mobile, compact header actions may hide their visible labels, but Create
retains its plus and Ask AI Librarian its distinct symbol. Size these icons
independently of the collapsed parent font, centre them, retain localised
accessible names, and verify visibility across every site theme.

Desktop book pages include a small, muted grey availability note below the
reading/download actions: animation availability, actual full-reader languages
(compact codes with full names on hover), and published edition count. Derive it
from manifest reader files and edition history; interface metadata is not a
translation, and in-preparation releases are not published editions. Hide the
entire note at mobile/tablet book-layout widths.

The book animation wrapper explicitly fills the available width up to 1100px;
centred flex layout must not shrink it to the icon-only close link. Integration
QA must measure the loaded player stage on desktop and mobile, not only the X.

Site typography uses a 19.84px root base: the new 100% equals the former 124%.
Header size controls run from 100% to 150% in 5-point steps, with 100% as reset
and default. Store this rebased preference separately from the old scale and
apply it before first paint. Reader text shares the 24% baseline increase with
its own 100–150% text control; PDF fit/zoom remains a document-viewing control.

At increased text sizes, allow header controls to wrap and book panels to grow
to their content. Mobile reading actions may wrap their labels with sufficient
height; never clip enlarged text or let it overlap titles.

All contribution workflows (Create, Fork, Suggest, animation suggestions and
translation requests) collect details first and use a localised Next action.
Navigate to the shared agreement page with an opaque draft ID and interface
language; never put names, email addresses or contribution text in the URL.
Keep the draft in tab-scoped session storage, expire it after 24 hours, and
restore fields and selected attachment names when returning to edit. File bytes
are not stored: the visitor attaches the documents in the mail application.
The first agreement clause is an explicit declaration on the contributor’s own
responsibility that they hold the necessary intellectual-property rights or
authorisation to submit and grant the stated permissions. Never preselect consent.
Only the agreement’s final action opens the structured email; it does not send
mail automatically. Preserve the common submission boundary for a future
endpoint integration without claiming that endpoint exists now.

SHF animations start in Colorful (`color`) on both book pages and the homepage
introduction, independently of the site theme. Changing the site theme must not
change the film artwork theme. Visitors may still choose another artwork theme
using the player controls; reopening the homepage introduction starts in Colorful.

Animation suggestion forms show a compact book reminder before the introductory
question: linked cover, title, localised category and short description, using
the shared book-view component. This also applies beneath an existing player.
The reminder shows the actual description as justified prose, initially limited
to two lines. When it overflows, show a visible ellipsis button that expands the
complete text in place, supports keyboard activation and exposes `aria-expanded`
and `aria-controls`; preserve the text and show it in the native hover tooltip.
Do not animate individual sentences in this opt-in compact reminder. Short
fitting descriptions need no disclosure. Keep title-to-reminder spacing tight,
and make the introductory question bold, white in both dark site themes and
high-contrast in light themes. Keep the shared component responsive to width,
font-size and language changes without duplicating per-book markup.

SHF subtitles use centred, balanced wrapping in a narrower reading measure,
preferably two even lines when a long sentence fits. Use semibold (600) black text with a white outline in Colorful/Light and regular
(400) white text with a
black outline in Dark, following the player theme independently of the site.
Do not restore the grey panel. Player settings offer remembered subtitle size
(75–150%) instead of Speed; omit the Reduced motion checkbox while preserving
the system motion preference. On narrow screens allow additional lines rather
than clipping captions or hiding words.


Every book exposes a one-word Contributors action alongside Fork, Suggest and
Editions, using the shared `/contributors/index.html?book=<directory>&lang=<code>`
workflow. Keep its heading compact and show only the book title above the provenance, without a cover.
Use a full-width semantic table per edition: linked author name in the first
column, contribution text in the second. Provide clear row and column rules,
allow any number of contributors, and avoid an artificial text-width limit.
Do not render the URL as a separate field.
Contributions belong to explicit edition IDs in `editions.json`, preserving
historical credits when later editions add ideas, feedback or other work.
The initial editions of the current104 books credit Axiologic Research SRL
(`https://www.axiologic.net`) for creating and contributing the initial book
within the SCRIPTA use case of Achilles (`https://www.achilles-project.eu/`).
This is editor-provided attribution. Store shared identities and initial text in
`docs/contributors.json`; edition entries reference `authorId` and `statementId`.
Future entries may instead supply an `author` object with name/url and a localized
`description` (plain text or text/link segments), plus a role. Do not automatically
attribute future contributors or releases. The catalogue and local-file mirror
include resolved edition credits, so this page does not depend on a fetch.

Book animation pages expose the standard localized “Back to book” button above
the player, alongside the unobtrusive close icon. Both return to the same book
and pause playback. Contributors tables use compact uppercase column headings,
comfortable cell spacing, subtle alternating row surfaces and a rounded outer
border. Keep contribution prose naturally wrapped across the available width.
Integrate each edition caption into a restrained accent-edged table heading.
Use distinct header and author-column surfaces, strong linked author names and
continuous table borders; inherit the active theme and retain a real two-column
table on mobile without unnecessary desktop line breaks.

The entire homepage featured-book strip opens the current book, including its
cover, description, category, keywords and padding. Use a native link with the
same localized destination as View Book so modifier clicks work. Keep existing
keyboard-accessible title/action links. Update the whole-card destination on
every book rotation and language change, and pause rotation while the strip is
hovered or contains keyboard focus.

The featured strip exposes a small carousel chevron beyond its right-hand
background surface, in the surrounding gutter. Its localized accessible label
is `Next Book`. The control must not change the content grid: the `View Book`
action stays aligned with the librarian controls above. It advances the
cover, copy and whole-card destination together without navigating, while its
restrained circular treatment keeps it distinct from `View Book`.


### Scene transitions and transport visibility

Automatic scene advance is a continuation of playback, not a new user Play
action: preserve hidden controls and their interaction timer, and emit
`shf-play` only for an actual playback start. Reveal transport for pointer
interaction within its own area, a touch gesture, or keyboard focus/navigation.
Do not reveal it for mouse movement elsewhere over the artwork. Preserve the
mobile transport rail dimensions while hiding its controls, avoiding layout jumps.
Prepare only the next scene's audio ahead of the boundary, retaining bounded
decoded caching and authored sentence pauses. An automatic transition must not
add the initial playback scheduling delay. Verify muted playback with deliberately
slow preparation, plus desktop/mobile hover, touch and keyboard interactions.

A pointer press outside the player immediately dismisses transport during playback.
Pointer movement outside its control rail clears hover and pointer-era button
focus as reasons to keep it open; it hides after 3.5 seconds without interaction.
Keyboard navigation still reveals controls. Attach outside-pointer listeners only
while connected and remove them on disconnect.
