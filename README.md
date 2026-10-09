# voice_changer_text_speech_converter

VoxNote AI turns recordings into transcripts and summaries, and converts text into spoken audio.

## Features

- Upload audio or record a voice message in the browser.
- Transcribe audio with Groq-hosted Whisper.
- Create short summaries, detailed summaries, or meeting notes.
- Generate speech using installed system voices, with voice and speed controls.
- Download transcripts, summaries, and WAV audio.

## Setup

Use Python 3.12. On Windows, speech uses installed system voices. Streamlit Community Cloud uses Linux speech packages listed in `packages.txt`.

```powershell
python -m venv uk
.\uk\Scripts\python.exe -m pip install -r requirements.txt
Copy-Item .env.example .env
```

Open `.env` and add your Groq API key to `GROQ_API_KEY`. You can also add a LangSmith key to `LANGSMITH_API_KEY` and set `LANGSMITH_TRACING=true` to enable tracing.

```powershell
.\uk\Scripts\python.exe -m streamlit run app.py
```

Transcription and summarization require an internet connection. Text-to-speech uses locally installed voices.

## Streamlit Community Cloud

1. Deploy the GitHub repository using branch `main` and entrypoint `app.py`. Choose Python 3.12 in advanced settings.
2. Add keys in Settings > Secrets using TOML:

```toml
GROQ_API_KEY = "your_groq_key"
LANGSMITH_API_KEY = "your_langsmith_key"
LANGSMITH_TRACING = "false"
LANGSMITH_PROJECT = "ai-voice-summarizer"
```

The LangSmith key is optional unless you want tracing. Set `LANGSMITH_TRACING = "true"` to enable it.
3. Save the secrets. Cloud installs `requirements.txt` and the Linux packages in `packages.txt`. Reboot the app from Manage app if the previous error remains.

Keep API keys at the root of the Secrets configuration rather than under a named TOML section. Root-level string secrets are available as environment variables. Do not add real keys to the repository.

## Project files

- `app.py`: Streamlit interface.
- `sumerizer.py`: Audio transcription and text summarization.
- `summarizer.py`: Compatibility import for the standard spelling.
- `speech.py`: Local speech generation.
- `.streamlit/config.toml`: App colours and typography.
- `requirements.txt`: Runtime dependencies detected by Streamlit Community Cloud.
- `packages.txt`: Linux system dependencies for speech.
- `r.txt`: Full package snapshot from the local Windows environment.

Credentials in `.env` and `.streamlit/secrets.toml`, the virtual environment, and Python caches are excluded from Git.
