# voice_changer_text_speech_converter

VoxNote AI turns recordings into transcripts and summaries, and converts text into spoken audio.

## Features

- Upload audio or record a voice message in the browser.
- Transcribe audio with Groq-hosted Whisper.
- Create short summaries, detailed summaries, or meeting notes.
- Generate speech using installed Windows voices, with voice and speed controls.
- Download transcripts, summaries, and WAV audio.

## Setup

This dependency snapshot is for Windows with Python 3.12. Local speech uses the voices installed on Windows.

```powershell
python -m venv uk
.\uk\Scripts\python.exe -m pip install -r r.txt
Copy-Item .env.example .env
```

Open `.env` and add your Groq API key to `GROQ_API_KEY`. You can also add a LangSmith key to `LANGSMITH_API_KEY` and set `LANGSMITH_TRACING=true` to enable tracing.

```powershell
.\uk\Scripts\python.exe -m streamlit run app.py
```

Transcription and summarization require an internet connection. Text-to-speech uses locally installed voices.

## Project files

- `app.py`: Streamlit interface.
- `sumerizer.py`: Audio transcription and text summarization.
- `summarizer.py`: Compatibility import for the standard spelling.
- `speech.py`: Local speech generation.
- `.streamlit/config.toml`: App colours and typography.
- `r.txt`: Installed package versions.

Credentials in `.env` and `.streamlit/secrets.toml`, the virtual environment, and Python caches are excluded from Git.
