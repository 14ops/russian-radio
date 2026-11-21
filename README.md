# Povtori FM

**v2.2.1** · [Change log](CHANGELOG.md)

An endless Russian radio show for A1 and A2 learners. Two hosts, Nika and Tyoma, tell a story that never ends, repeat key phrases for you to say out loud, answer your questions on air, drill your own words and docs, run a guessing game, and score your voice.

Everything runs in the browser. No install, no build step.

## Run it

- From a USB stick or any folder: download the repo, open the folder, double-click `Povtori FM.html`. Chrome or Edge work best.
- As a website: turn on GitHub Pages for this repo (Settings, Pages, deploy from the `main` branch, root folder). Then open `https://14ops.github.io/russian-radio/`.

Press **Слушать** to start.

## New in v2.2.1

- **Dictionary check for the mini AI**: every AI line goes through `data/dict.js` before it airs. Made-up words, broken endings (*ты покупаете*), wrong cases (*у Машу*) and wrong English meanings stay off air. It passes 455 of the 456 course lines.
- **Stress marks on AI lines**, from the same dictionary: 1317 of 1318 match the course.
- **Bigger models write better and run faster**: a course lesson as the example, your story idea as the plot, and a cached prompt start. With Qwen2.5 1.5B the second episode took 144 s instead of 407 s.

## New in v2.2.0

- **Course**: 30 hand-written lessons from A1 to A2 with checked stress marks and a quiz each. The radio plays the next one every other segment.
- **Word review round**: 2 minutes, hear a word and pick its meaning, or type the Russian. Only right answers move a word up.
- **Tap a word**: meaning, stress and form of any Russian word in the transcript, offline.
- **USB helpers**: `Start Povtori FM.cmd` and `Update Povtori FM.cmd`.

## New in v2.0.0

- **Word review**: each word you add comes back after 1, 3, 7 and 16 days. The hosts put due words into new stories and drills.
- **Story quiz**: 3 tap-to-answer questions after each story. Right answers add game points.
- **Save as MP3**: any story, drill, doc lesson or answer, voiced by the AI voices with the repeat pauses. About 5 MB per 10 minutes.
- **Media keys**: earbuds, keyboard media keys and the lock screen. Next skips the segment, previous replays the last line slowly.
- **Dictation**: hear a line, type it, see every wrong letter. On-screen Russian keyboard.
- **Progress**: minutes per day, day streak, words known, quiz and dictation scores.
- **A2 mode**: past tense, the future with бу́ду and all six cases.
- **Chat format for bigger models**: instruct GGUF models get prompts through their own chat template.

Full details in [CHANGELOG.md](CHANGELOG.md).

## Start and update on Windows

- **Start Povtori FM.cmd** opens the radio in Chrome or Edge.
- **Update Povtori FM.cmd** downloads only the files that changed or are missing, and checks each one against `files.json` before it goes in place. An update is usually a few MB. It also repairs a copy with missing or damaged files.
- If Windows says "Windows protected your PC", click **More info**, then **Run anyway**.

No helpers yet? Download the zip once and unzip it over the old folder. Your words, story and progress live in the browser, so they stay. In CMD (not PowerShell), with the stick as `E:`:

```
cd /d E:\ && curl.exe -fL -o radio.zip https://github.com/14ops/russian-radio/archive/refs/heads/main.zip && tar -xf radio.zip && del radio.zip
```

## Something broke?

Open **Debug log** at the bottom of the page. It lists every warning and error, plus what the app did, and it keeps the previous visit. Press **Save as .txt** or **Copy log** and send that along. API keys never show up in it.

## What works offline

- The radio, built-in episodes, games, word drills and reruns
- AI voices for both hosts (Supertonic 3 neural TTS, running in the browser from the `voice` folder)
- A mini AI that writes new story episodes and word drills (Gemma 3 270M, running in the browser from the `ai` folder)
- Your words, docs (txt, md, pdf, docx), questions and story ideas
- Recording yourself and the voice score (syllables, pace, pauses, pitch, clarity)
- Word review, the story quiz, dictation, progress and MP3 export

## Who writes new episodes

Pick a writer in Settings (the **Голоса** button):

- **Mini AI** (default). Gemma 3 270M runs in the browser through wllama (llama.cpp in WebAssembly, WebGPU when available). Offline, free, no setup. It is tiny, so expect clumsy and sometimes wrong Russian. It writes story episodes and word drills. A grammar keeps every line in the `Russian | English` format, and a dictionary check drops lines with made-up words, broken endings or a wrong English meaning before they go on air. Lines that pass get stress marks from the dictionary.
  - **Bigger model:** download a GGUF under 2 GB on your computer, for example [Qwen2.5 1.5B Instruct](https://huggingface.co/Qwen/Qwen2.5-1.5B-Instruct-GGUF) (`q4_k_m`, about 1.1 GB) or [Gemma 3 1B IT](https://huggingface.co/ggml-org/gemma-3-1b-it-GGUF) (`Q4_K_M`, about 0.8 GB). In Settings pick **Use a bigger model file**. The browser keeps it, and **Back to built-in** undoes it. Instruct models get prompts in their own chat format (Settings, **Prompt style**). Speed with Qwen2.5 1.5B on a test computer without a graphics chip: 7 minutes for the first episode, about 2.5 minutes for each one after it, because the engine keeps the start of the prompt cached. Built-in episodes play while it writes. The debug log shows the speed on your computer.
- **Claude** with your own API key from console.anthropic.com. Needs internet. See [Your API key](#your-api-key).
- **Ollama** on your computer. Offline. Start it with `OLLAMA_ORIGINS="*" ollama serve` so the page is allowed to reach it.
- **Built-in episodes only.** No setup.

Full instructions: [README.txt](README.txt).

## Your API key

- The key never goes in this repo. You type it into the app on your own device.
- The app sends it only to `api.anthropic.com`. A Content Security Policy in `Povtori FM.html` blocks connections to any other address.
- By default the key lives in memory and disappears when you close the tab. Tick **Remember the key on this computer** to keep it in browser storage. **Forget key** wipes it.
- A remembered key sits in browser storage that other pages on the same origin share: every `14ops.github.io` site, or every HTML file Chrome opens from disk. Leave Remember off on shared computers.
- Use a separate key with a spend limit for this app.

## Folder layout

| Path | What it is |
|---|---|
| `Povtori FM.html` | The app |
| `index.html` | Redirect for GitHub Pages |
| `app/` | Fonts, the Anthropic SDK browser bundle, pdf.js, mammoth, lamejs (MP3 encoder) |
| `ai/` | Gemma 3 270M (Q4_K_M) and the wllama engine, split into script chunks |
| `voice/` | Supertonic 3 voice model and sherpa-onnx runtime, split into script chunks so they load from a plain folder |
| `data/` | The course (`course.js`) and the tap-a-word dictionary (`dict.js`) |
| `Start Povtori FM.cmd`, `Update Povtori FM.cmd` | Windows helpers: open the radio, update it |
| `files.json` | Every shipped file with its size and SHA-256, for the updater |
| `tools/` | Builders for the course, the dictionary and `files.json` (not needed to run the app) |
| `LICENSES/` | Third-party licenses |
| `CHANGELOG.md` | Every version and what changed |

## Credits

Supertonic 3 voice model by Supertone (OpenRAIL-M). Gemma 3 270M by Google, under the Gemma Terms of Use. wllama (MIT). sherpa-onnx runtime (Apache 2.0), packaged by @3sln/donki-lle (MIT). Anthropic TypeScript SDK (MIT), pdf.js (Apache 2.0), mammoth (BSD 2), lamejs, a JavaScript port of [LAME](https://lame.sourceforge.net) (LGPL 3.0, used unmodified as `app/lame.min.js`). Dictionary and stress data: [OpenRussian](https://en.openrussian.org) (CC BY-SA 4.0), in `data/dict.js` and behind the stress marks in `data/course.js`. Fonts: Golos Text, Unbounded, JetBrains Mono (SIL OFL). See `LICENSES/`.
