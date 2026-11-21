# Change log

The app shows the same log under **What's new** at the bottom of the page.

## v2.2.1 (2026-11-21)

- **Mini AI dictionary check.** Every line the mini AI writes goes through `data/dict.js` before it goes on air. It drops lines with a made-up word, a verb that does not fit its subject (*ты покупаете*, *мама сказало*), an adjective that does not fit its noun, the wrong case after a preposition (*у Машу*), в or на with the wrong place (*на магазине*), a noun the English gets wrong (*котлеты* as "chicken skewers"), dark words, and near copies. It passes 455 of the 456 course lines. The one it rejects is a teaching line where Tyoma quotes a woman.
- **Stress marks on mini AI lines.** The dictionary adds stress marks and ё where every reading agrees, so *идет* becomes *идёт* and *магазин* becomes *магази́н*. On the course lines, 1317 of 1318 marks match the hand-checked ones.
- **Bigger models write better stories.** The chat prompt now has the rules as a system message, a course lesson as the example (lesson 10 for A1, lesson 22 for A2), hosts that take turns, Nika speaking as a woman and Tyoma as a man, and a light everyday story. Your story idea becomes the plot, and it leaves the list once an episode uses it, or after 2 tries.
- **Bigger models run faster after the first episode.** Every prompt starts with the same rules and example, so the engine keeps that part cached and reads only the new request. With Qwen2.5 1.5B Instruct (q4_k_m) on a test computer without a graphics chip, one CPU thread: the first episode read 599 prompt tokens and took 7 minutes, the next episode read 87 new tokens (523 from cache) and took 2.5 minutes. A drill word takes about a minute.
- **Debug log.** Each mini AI prompt logs its speed (tokens read, tokens from cache, tokens per second) and what the check dropped.
- **Dictionary.** Names (Маша, Борис, Ника, Тёма and 20 more) have gender and the right case labels, so tapping *Ма́ши* says genitive. Pronoun forms such as *него́*, *ней*, *нему́*, *кого́*, *на́ш* and *ва́ш* were missing and are in now.
- The built-in Gemma 3 270M goes through the same check and gets one more try for a drill word when nothing passed.

## v2.2.0 (2026-11-17)

- **Course.** 30 hand-written lessons from A1 to A2 in `data/course.js`: greetings to all six cases, the past and the future, told through Masha, Anton, Boris and Sharik. 505 lines, 281 words, 90 quiz questions. Every stress mark comes from, or was checked against, the OpenRussian dictionary by `tools/build_course.py`. The radio plays the next lesson every other segment, each followed by its 3-question quiz. The Story tab lists all 30 with Play and MP3 buttons and your quiz score. A finished lesson adds its words to your list, first due the next day. The AI writers see which lessons you finished and recycle their words.
- **Word review round.** A 2-minute round in the Words tab, up to 20 due words. New words come as "hear it, pick the meaning" cards with 4 options; words from stage 2 on can also come as "type the Russian" cards with the on-screen keyboard. One wrong letter in a word of 5 or more letters still counts. A miss comes back once at the end of the round. Only a right answer moves a word to its next gap: hearing a word on air no longer counts as a review.
- **Tap a word.** Tap any Russian word in the transcript or on air: meaning, stress, part of speech, gender or aspect, and which form it is ("ры́бу is the accusative singular of ры́ба"). One tap adds it to your words. The dictionary is `data/dict.js`, 12,206 words with their forms from OpenRussian (CC BY-SA 4.0), loaded on the first tap. New words you type get their meaning and stress filled in from it, offline.
- **USB helpers.** `Start Povtori FM.cmd` opens the radio in Chrome or Edge. `Update Povtori FM.cmd` downloads `files.json`, compares sizes and SHA-256 fingerprints, and downloads only changed or missing files, checking each one before it goes in place. It repairs a copy with missing or damaged files too.
- Progress counts review answers, and 5 review answers make a day count toward the streak.

## v2.1.1 (2026-11-09)

- Word review: a review day runs from 04:00 to 04:00. A late-night session that crosses midnight no longer counts a word twice.
- Debug log: the AI voices line reports where the voices load from after the voice folder check, so it no longer says "from the internet" when the folder is there.
- The update notice no longer names a fixed number of new features, and it no longer blocks clicks on buttons under it.

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
