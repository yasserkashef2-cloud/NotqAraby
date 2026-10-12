# QA summary

Run on 2026-10-12 with headless Chromium (Playwright), served from a local web server and also opened from `file://`.

## Tested and passing

- cover renders
- routes in data = pages built
- no horizontal overflow (desktop 1280 + phone 390, all 41 pages)
- all in-page links resolve to a page
- all "jump to source" buttons point at an existing element
- no broken images on any page
- self-hosted fonts load (title, Amiri, Plex Arabic, Noto Serif)
- listening titles dark blue (title + exercise headings)
- reading/recitation titles dark red (title + exercise headings)
- flip card flips
- star marks card learned
- progress label updates after finishing an item
- answer persists after reload
- completion persists after reload
- star persists after reload
- download of answers works and contains the answer + question text
- drawer opens
- Esc closes the drawer
- text-size button enlarges text
- reading mode toggles
- theme toggle changes the background
- jump button scrolls to and highlights its target
- paragraph navigator shown on the statement page
- paragraph navigator advances
- no iframe before pressing load (nothing leaves the browser)
- load button creates a youtube-nocookie iframe
- glossary popover appears on hover
- target-sound highlighter marks letters and clears them
- source-error flag shows note and proposed fix
- cloze gives feedback with source line
- self-assessment choice persists
- map summary counts rated rows
- vocabulary filter narrows the list
- site search returns results
- Bilal video has seek buttons for the two stated times
- speed button sets playbackRate 0.75
- print stylesheet produces a PDF
- no console errors / page errors during the whole run (http)
- no failed or 4xx/5xx requests (http; aborted media preloads on navigation ignored)
- opens from file:// and renders an item page
- file:// run: no script errors (localStorage may be restricted; guarded)
- Source fidelity (verify.py): every non-empty line of the Word file appears on a page, except the 105 withheld lines; all 63 media files and the answers/jump targets (102) resolve.

## Found and fixed during QA

- Glossary highlighter missed prefixed words and re-scanned modified markup (fixed: clitic prefixes, re-split after each wrap).
- Cover SVG had an invalid height attribute (console error) — removed.
- Mixed Arabic/English small print rendered with scrambled bidi — split into separate spans.
- Lazy-loaded images were reported broken by the first QA script — check now loads each image explicitly.

## Not tested / cannot be verified here

- YouTube playback (the sandbox has no external network; only iframe creation is tested). From file:// YouTube may show error 153.
- Audio/video playback and the seek-to-2:00 button: the test Chromium cannot decode H.264/AAC; the buttons exist and playbackRate is tested.
- I cannot listen to or watch the media; mapping to exercises was done from file names, first frames and position in the lessons.
- Browsers other than Chromium (Safari, Firefox), real phones/tablets, and screen readers (only ARIA/keyboard structure was checked).
- The original Sakkal Majalla font (replaced by Amiri); print output was checked only as a generated PDF, not on paper.
- Educational glosses, questions and cultural prompts have not been reviewed by an Arabic teacher.