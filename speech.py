"""Generate WAV audio using the voices installed on this computer."""

import os
import tempfile
import threading
from pathlib import Path

import pyttsx3

_speech_lock = threading.Lock()


def text_to_speech(text, voice_gender="Female", speech_rate=165):
    """Return spoken text as WAV bytes for Streamlit playback and download."""
    if not isinstance(text, str) or not text.strip():
        raise ValueError("Please enter some text to speak.")
    rate = int(speech_rate)
    if rate <= 0:
        raise ValueError("Speaking speed must be greater than zero.")

    with _speech_lock:
        com = None
        engine = None
        try:
            if os.name == "nt":
                import pythoncom

                com = pythoncom
                com.CoInitialize()

            engine = pyttsx3.init()
            voices = engine.getProperty("voices")
            if not voices:
                raise RuntimeError("No speech voices are installed on this computer.")
            requested_gender = str(voice_gender).casefold()
            voice = next(
                (v for v in voices
                 if str(getattr(v, "gender", "")).casefold() == requested_gender),
                voices[0],
            )
            engine.setProperty("voice", voice.id)
            engine.setProperty("rate", rate)

            with tempfile.TemporaryDirectory(prefix="voxnote-speech-") as directory:
                audio_path = Path(directory) / "speech.wav"
                engine.save_to_file(text.strip(), str(audio_path))
                engine.runAndWait()
                audio = audio_path.read_bytes()
                if len(audio) <= 44:
                    raise RuntimeError("The speech engine did not generate audio.")
                return audio
        finally:
            if engine is not None:
                engine.stop()
                engine = None
            if com is not None:
                com.CoUninitialize()
