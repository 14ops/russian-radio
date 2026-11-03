# Povtori FM

An endless Russian radio show for A1 beginners. Two hosts, Nika and Tyoma, tell a story that never ends, repeat key phrases for you to say out loud, answer your questions on air, drill your own words and docs, run a guessing game, and score your voice.

Everything runs in the browser. No install, no build step.

## Run it

- From a USB stick or any folder: download the repo, open the folder, double-click `Povtori FM.html`. Chrome or Edge work best.
- As a website: turn on GitHub Pages for this repo (Settings, Pages, deploy from the `main` branch, root folder). Then open `https://14ops.github.io/russian-radio/`.

Press **Слушать** to start.

## What works offline

- The radio, built-in episodes, games, word drills and reruns
- AI voices for both hosts (Supertonic 3 neural TTS, running in the browser from the `voice` folder)
- Your words, docs (txt, md, pdf, docx), questions and story ideas
- Recording yourself and the voice score (syllables, pace, pauses, pitch, clarity)

## Who writes new episodes

Pick a writer in Settings (the **Голоса** button):

- **Claude** with your own API key from console.anthropic.com. Needs internet. The key stays in your browser and goes only to api.anthropic.com.
- **Ollama** on your computer. Offline. Start it with `OLLAMA_ORIGINS="*" ollama serve` so the page is allowed to reach it.
- **Built-in episodes only.** No setup.

Full instructions: [README.txt](README.txt).

## Folder layout

| Path | What it is |
|---|---|
| `Povtori FM.html` | The app |
| `index.html` | Redirect for GitHub Pages |
| `app/` | Fonts, the Anthropic SDK browser bundle, pdf.js, mammoth |
| `voice/` | Supertonic 3 voice model and sherpa-onnx runtime, split into script chunks so they load from a plain folder |
| `LICENSES/` | Third-party licenses |

## Credits

Supertonic 3 voice model by Supertone (OpenRAIL-M). sherpa-onnx runtime (Apache 2.0), packaged by @3sln/donki-lle (MIT). Anthropic TypeScript SDK (MIT), pdf.js (Apache 2.0), mammoth (BSD 2). Fonts: Golos Text, Unbounded, JetBrains Mono (SIL OFL). See `LICENSES/`.
