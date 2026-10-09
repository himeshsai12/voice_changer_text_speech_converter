import streamlit as st

from sumerizer import transcribe_audio, summarize_text
from speech import text_to_speech


st.set_page_config(
    page_title="VoxNote AI",
    page_icon=":material/graphic_eq:",
    layout="centered",
    initial_sidebar_state="expanded"
)


if "transcript" not in st.session_state:
    st.session_state.transcript = ""

if "summary" not in st.session_state:
    st.session_state.summary = ""

if "speech_audio" not in st.session_state:
    st.session_state.speech_audio = None


with st.container(border=True):
    st.title(":violet[VoxNote AI]", icon=":material/graphic_eq:", anchor=False)
    st.markdown("**Turn conversations into clear notes.**")
    st.caption(
        "Record an idea, capture a conversation, or give your words a voice."
    )
    with st.container(horizontal=True):
        st.badge("Audio to text", icon=":material/mic:", color="blue")
        st.badge("Clear summaries", icon=":material/auto_awesome:", color="violet")
        st.badge("Text to voice", icon=":material/volume_up:", color="green")


with st.sidebar:
    st.header("Make it yours", icon=":material/tune:")
    st.caption("Choose how your notes read and sound.")

    summary_style = st.selectbox(
        "Summary length",
        ["Short", "Detailed", "Meeting Notes"],
        index=1
    )

    voice_gender = st.segmented_control(
        "Narrator voice",
        ["Female", "Male"],
        default="Female",
        required=True,
        key="narrator_voice",
        width="stretch"
    )

    speech_rate = st.slider(
        "Speaking speed",
        min_value=120,
        max_value=220,
        value=165,
        step=5
    )

    st.caption(
        "Audio transcription and summaries use your Groq API key. "
        "Text-to-speech uses the voices installed on your computer."
    )


audio_tab, text_tab, about_tab = st.tabs([
    ":material/mic: Audio summarizer",
    ":material/volume_up: Text to voice",
    ":material/info: How it works"
])


with audio_tab:
    st.header("Start with your audio", anchor=False)

    st.write(
        "Upload a recording or record a message with your microphone."
    )

    upload_col, record_col = st.columns(2)

    with upload_col.container(border=True):
        st.subheader("Upload audio", icon=":material/upload_file:")
        st.caption("Bring a recording you already have.")

        uploaded_audio = st.file_uploader(
            "Choose an audio file",
            type=[
                "wav", "mp3", "m4a", "mp4",
                "mpeg", "mpga", "webm", "ogg"
            ],
            key="audio_upload"
        )

    with record_col.container(border=True):
        st.subheader("Record your voice", icon=":material/mic:")
        st.caption("Capture a thought or a conversation.")

        recorded_audio = st.audio_input(
            "Record a voice message",
            key="microphone_recording"
        )

    selected_audio = recorded_audio or uploaded_audio

    if selected_audio:
        st.success("Audio is ready for processing.")
        st.audio(selected_audio)

    if st.button(
        "Transcribe and summarize",
        type="primary",
        icon=":material/auto_awesome:",
        width="stretch",
        disabled=selected_audio is None
    ):
        try:
            audio_bytes = selected_audio.getvalue()

            if not audio_bytes:
                st.error("The selected audio file is empty.")
                st.stop()

            if len(audio_bytes) > 25 * 1024 * 1024:
                st.error(
                    "Please use an audio file smaller than 25 MB."
                )
                st.stop()

            filename = getattr(
                selected_audio,
                "name",
                "recording.wav"
            )

            mime_type = getattr(
                selected_audio,
                "type",
                None
            ) or "audio/wav"

            with st.spinner(
                "Whisper is transcribing your audio..."
            ):
                transcript = transcribe_audio(
                    audio_bytes,
                    filename,
                    mime_type
                )

            st.session_state.transcript = transcript
            st.session_state.summary = ""
            st.session_state.speech_audio = None

            with st.spinner(
                "Groq is creating your summary..."
            ):
                summary = summarize_text(
                    transcript,
                    summary_style
                )

            st.session_state.summary = summary

            st.success(
                "Your transcript and summary are ready!"
            )

        except Exception as error:
            st.error(f"Processing failed: {error}")

    if st.session_state.transcript:
        st.divider()

        st.header("Your transcript", icon=":material/article:", anchor=False)

        edited_transcript = st.text_area(
            "Review or edit the recognized text",
            value=st.session_state.transcript,
            height=220,
            key="edited_transcript"
        )

        st.download_button(
            "Download transcript",
            data=edited_transcript,
            file_name="transcript.txt",
            mime="text/plain",
            width="stretch"
        )

        if st.button(
            "Summarize edited transcript",
            width="stretch"
        ):
            try:
                with st.spinner(
                    "Creating a new summary..."
                ):
                    st.session_state.summary = summarize_text(
                        edited_transcript,
                        summary_style
                    )

                    st.session_state.speech_audio = None

                st.success("Updated summary created!")

            except Exception as error:
                st.error(
                    f"Summarization failed: {error}"
                )

    if st.session_state.summary:
        st.divider()

        st.header("Your summary", icon=":material/auto_awesome:", anchor=False)

        with st.container(border=True):
            st.markdown(st.session_state.summary)

        st.download_button(
            "Download summary",
            data=st.session_state.summary,
            file_name="ai_summary.txt",
            mime="text/plain",
            width="stretch"
        )

        if st.button(
            "Generate spoken summary",
            width="stretch"
        ):
            try:
                with st.spinner(
                    "Generating your AI voice..."
                ):
                    st.session_state.speech_audio = text_to_speech(
                        st.session_state.summary,
                        voice_gender,
                        speech_rate
                    )

                st.success("Speech audio is ready!")

            except Exception as error:
                st.error(
                    f"Text-to-speech failed: {error}"
                )

        if st.session_state.speech_audio:
            st.audio(
                st.session_state.speech_audio,
                format="audio/wav"
            )

            st.download_button(
                "Download spoken summary",
                data=st.session_state.speech_audio,
                file_name="spoken_summary.wav",
                mime="audio/wav",
                width="stretch"
            )


with text_tab:
    st.header("Give your words a voice", anchor=False)

    text_for_speech = st.text_area(
        "Enter the text you want the application to speak",
        height=220,
        placeholder=(
            "Enter a meeting summary, study notes, "
            "or any text here..."
        ),
        key="standalone_text"
    )

    text_voice = st.segmented_control(
        "Choose voice",
        ["Female", "Male"],
        default="Female",
        required=True,
        key="text_voice",
        width="stretch"
    )

    text_rate = st.slider(
        "Choose speaking speed",
        120,
        220,
        165,
        5,
        key="text_rate"
    )

    if st.button(
        "Convert text to voice",
        type="primary",
        icon=":material/volume_up:",
        width="stretch"
    ):
        if not text_for_speech.strip():
            st.warning("Please enter some text first.")
        else:
            try:
                with st.spinner(
                    "Generating spoken audio..."
                ):
                    audio = text_to_speech(
                        text_for_speech,
                        text_voice,
                        text_rate
                    )

                st.success(
                    "Speech generated successfully."
                )

                st.audio(audio, format="audio/wav")

                st.download_button(
                    "Download speech",
                    data=audio,
                    file_name="text_to_speech.wav",
                    mime="audio/wav",
                    width="stretch"
                )

            except Exception as error:
                st.error(
                    f"Speech generation failed: {error}"
                )


with about_tab:
    st.markdown("## How this project works")

    st.markdown("""
    **1. Audio input:** The user uploads a recording or records
    a voice message.

    **2. Speech recognition:** Whisper converts the audio
    into a text transcript.

    **3. Language processing:** LangChain prepares the prompt
    and connects it to the Groq-hosted language model.

    **4. Summarization:** The model extracts the important
    information and presents it in readable language.

    **5. Speech generation:** The local text-to-speech engine
    reads the summary aloud.

    **6. Downloads:** The user can save the transcript,
    summary, and generated audio.
    """)

    st.info(
        "Avoid uploading confidential meetings, passwords, "
        "personal records, or sensitive company audio unless "
        "you have authorization to process them."
    )


st.divider()

st.caption("VoxNote AI · Voice notes made simple.")