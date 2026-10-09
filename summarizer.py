"""Expose the summarizer under the standard module name."""

from sumerizer import summarize_text, transcribe_audio

__all__ = ["summarize_text", "transcribe_audio"]
