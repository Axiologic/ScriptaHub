# UI task queue

- [x] Refine the book reminder beneath “Improve this presentation” in the shared
  component: justify the description, show at most two lines followed by an
  explicit clickable ellipsis when truncated, and show the full description in
  a tooltip. Clicking the ellipsis expands the description in place; support
  keyboard activation and expose the expanded state to assistive technology.
  Reduce spacing between the section title and the book reminder. Make “What
  would make this book introduction clearer or more compelling?” bolder and
  more distinct, white on dark themes (with readable contrast on light themes).
  Completed 2026-09-10 in the shared book-view/workflow component. Verified
  60 standalone/embedded cases across five themes, 320/390/1440px, short/long
  descriptions and Enter activation, plus 16 cases across eight languages at
  150% text size with Space activation. Full text and focus are preserved;
  mobile descriptions use the full reminder width below the cover. Evidence:
  `tests/artifacts/reminder-ui/`; browser checks run silently.

- [x] Start a book presentation automatically after the visitor clicks Animation,
  without requiring a second Play click. Preserve narration, allow closing/pausing,
  and keep direct/background loads from starting unexpectedly. If the browser
  denies audible autoplay, retain a usable Play control. Verify silently.
  Requested and completed 2026-09-10. Verified silently by
  `tests/animation-start.browser.mjs`: trusted click, one-use intent, direct/reload
  and synthetic/copy/expired loads, blocked-audio Play fallback, cancellation
  when hidden before readiness, and Back to book during loading. Player muted
  before loading; blocked unlock and visibility transition explicitly simulated.

- [x] Fix SHF scene-transition controls and investigate the accompanying brief
  pause reported by the user. Advancing to another scene during playback must
  not reveal the viewer controls or restart their visibility timer. Reveal
  controls through deliberate pointer interaction with their area or a touch
  gesture on mobile; preserve keyboard focus access. Investigate unintended
  transition stalls separately from authored narration pauses; retain the
  intended pauses between sentences. Apply any shared runtime fix to both the
  skill player and the site's installed player, and rebuild affected standalone
  exports when necessary. Verify automatic and manual scene changes, desktop
  pointer interaction, mobile touch, fullscreen, and keyboard navigation with
  muted playback. Requested 2026-09-10; implemented in shared site/skill runtimes and 137 current standalone exports. Muted browser regression checks cover slow next-scene preparation, automatic transitions, manual seek, desktop/mobile-sized pointer and touch events, keyboard focus and fullscreen. Physical-device testing is not claimed.

- [x] Dismiss SHF controls immediately on a pointer press outside the player;
  hide after 3.5 seconds with the pointer outside the control rail, even when
  a previously clicked button retains focus. Verified silently at desktop/mobile
  sizes, including keyboard access and fullscreen; shared site/skill runtime
  and current standalone exports updated.
