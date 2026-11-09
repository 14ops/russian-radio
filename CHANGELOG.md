# Change log

The app shows the same log under **What's new** at the bottom of the page.

## v2.1.0 (2026-11-09)

- **Debug log** at the bottom of the page. It records every warning and error, uncaught errors, and what the app did: start-up, the writer starting and finishing, the mini AI loading (model, WebGPU or CPU, chat or plain), AI voices, each segment on air, quizzes, MP3 saves and settings changes. *Copy log* and *Save as .txt* add a header with the version, browser and setup. The previous visit stays in the log, so a crash before a reload still shows up. API keys are scrubbed from every line.

## v2.0.0 (2026-11-09)

- **Smart word review.** Each word on your list comes back after 1, 3, 7 and 16 days, then 35 and 60. The hosts put due words into new stories and drills. The Words tab shows what is due, and a word counts as known once it passes the 7-day review. A quiz or dictation miss brings a word back sooner.
- **Story quiz.** After each story episode the hosts run 3 tap-to-answer questions in the Game tab. Every right answer adds a point to your game score. Claude writes the questions about what happened. Offline and with the mini AI, the app builds them from the episode's own lines.
- **Save episodes as MP3.** Story tab, *Take it with you*, or the *Save MP3* button on any segment in the transcript. The AI voices render the episode with the chime and the pauses where you repeat, then the app encodes it at 64 kbps mono: about 5 MB per 10 minutes.
- **Earbud, keyboard and lock-screen controls.** Play and pause, next skips the segment, previous replays the last line slowly. The lock screen shows the line on air.
- **Dictation.** New Dictation tab: hear a line from the show, type it, and see every wrong, missing or extra letter. On-screen Russian keyboard included. Е and Ё count as the same letter, and punctuation does not count.
- **Bigger mini AI models use their chat format.** Instruct models such as Qwen2.5 1.5B Instruct get prompts through the chat template inside the model file, plus the story so far and your story ideas. Settings has a *Prompt style* switch: Auto, chat or plain.
- **Progress page.** Minutes listened per day for the last 14 days, day streak, words known, total hours, quiz and dictation scores.
- **A2 mode.** The A1 / A2 switch at the top. A2 brings past tense, the future with бу́ду and all six cases, two new studio tapes, and A2 examples for the mini AI.
- A version number and this change log.

## v1.3.0 (2026-11-05)

- The mini AI runs a bigger GGUF model file you pick, for example Qwen2.5 1.5B Instruct.

## v1.2.0 (2026-11-03)

- Mini AI writer: Gemma 3 270M writes new story episodes and word drills in the browser, offline.

## v1.1.0 (2026-11-03)

- The Claude API key stays in memory unless you tick Remember.
- A Content Security Policy keeps the page from sending data anywhere except Claude and Ollama.

## v1.0.0 (2026-11-03)

- First release: endless A1 Russian radio with two hosts, repeat pauses, your words and docs, an inbox for questions, a guessing game, voice scoring, AI voices and lo-fi music. Runs offline from a folder or a USB stick.
