POVTORI FM: Russian A1 radio, USB edition
==========================================

START
1. Copy the whole Povtori-FM folder onto your USB stick.
2. Open the folder and double-click "Povtori FM.html".
   Chrome or Edge work best. Firefox works too.
3. Press Слушать (Listen).

Keep the app and voice folders next to "Povtori FM.html". The page loads them from there.


WHAT RUNS OFFLINE
- The radio, built-in episodes, games, word drills and reruns
- AI voices for Nika and Tyoma (Supertonic 3, loaded from the voice folder)
- Your words, docs (txt, md, pdf, docx), questions and story notes
- Recording yourself and the voice score (pitch, pace, pauses, syllables)


WHO WRITES NEW EPISODES (Settings, the Голоса button)
Pick one:

A) Claude with your API key (needs internet)
   - Get a key at console.anthropic.com
   - Paste it in Settings, Writer, then press Test writer
   - The default model is filled in. Change it in Settings if you want.
   - The key is saved in this browser on this computer and is sent only to api.anthropic.com.
     Each segment uses a little API credit.

B) Ollama on this computer (offline)
   - Install Ollama from ollama.com
   - In a terminal: ollama pull qwen2.5:7b
   - Quit Ollama, then start it so this page is allowed to talk to it:
       Windows (PowerShell):  $env:OLLAMA_ORIGINS="*"; ollama serve
       Mac or Linux:          OLLAMA_ORIGINS="*" ollama serve
   - In Settings pick Ollama, keep http://localhost:11434, press Test writer
   - Small models make more Russian grammar mistakes than Claude.

C) Built-in episodes only (offline). No setup.


VOICES
- AI voices load from the voice folder the first time you press Listen. Give it a few seconds.
- No voice folder? With internet, the page downloads the voice once (about 145 MB).
- Settings lets you swap Nika's and Tyoma's AI voice, or switch to your computer's own voices.
- Low memory computers might fail to load the AI voice. The page then uses device voices.


RECORDING
- Voice tab, Record, say the phrase, Stop. Allow the mic when the browser asks.
- In Chrome and Edge the browser's speech recognizer also checks the words. That part needs internet.


DATA
Everything you add is stored in this browser's local storage on this computer.
Open the page in a different browser or computer and you start fresh.


CREDITS AND LICENSES (see the LICENSES folder)
- Supertonic 3 voice model by Supertone (OpenRAIL-M)
- sherpa-onnx runtime (Apache 2.0), packaged by @3sln/donki-lle (MIT)
- Anthropic TypeScript SDK (MIT), pdf.js (Apache 2.0), mammoth (BSD 2)
- Fonts: Golos Text, Unbounded, JetBrains Mono (SIL Open Font License)
