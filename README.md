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
- A mini AI that writes new story episodes and word drills (Gemma 3 270M, running in the browser from the `ai` folder)
- Your words, docs (txt, md, pdf, docx), questions and story ideas
- Recording yourself and the voice score (syllables, pace, pauses, pitch, clarity)

## Who writes new episodes

Pick a writer in Settings (the **Голоса** button):

- **Mini AI** (default). Gemma 3 270M runs in the browser through wllama (llama.cpp in WebAssembly, WebGPU when available). Offline, free, no setup. It is tiny, so expect clumsy and sometimes wrong Russian. It writes story episodes and word drills. A grammar keeps every line in the `Russian | English` format.
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
| `app/` | Fonts, the Anthropic SDK browser bundle, pdf.js, mammoth |
| `ai/` | Gemma 3 270M (Q4_K_M) and the wllama engine, split into script chunks |
| `voice/` | Supertonic 3 voice model and sherpa-onnx runtime, split into script chunks so they load from a plain folder |
| `LICENSES/` | Third-party licenses |

## Credits

Supertonic 3 voice model by Supertone (OpenRAIL-M). Gemma 3 270M by Google, under the Gemma Terms of Use. wllama (MIT). sherpa-onnx runtime (Apache 2.0), packaged by @3sln/donki-lle (MIT). Anthropic TypeScript SDK (MIT), pdf.js (Apache 2.0), mammoth (BSD 2). Fonts: Golos Text, Unbounded, JetBrains Mono (SIL OFL). See `LICENSES/`.
