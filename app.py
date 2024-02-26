import streamlit as st
import whisper
import replicate
import ffmpeg

# system prompts
from prompt_strings import progress_note, treatment_plan_update

model = whisper.load_model("base")

# upload audio file with streamlit in the sidebar
audio_file = st.sidebar.file_uploader("Upload Audio", type=["wav", "mp3", "m4a", "mp4"])

st.title("Transcribe & Summarize Patient Conversations")
patient_name = st.text_input('Enter patient name.', 'Jane Doe')
practioner_name = st.text_input('Enter practioner name.', 'Jane Smith, LCSW')
date = st.text_input('Enter date of session, DD-MM-YYYY format', '02-18-2024')
note_type = st.selectbox('Transcribed Note Template', ('GIRP', 'placeholder= 'Select the type of progress note')

# transcription text inferenced by whisper - this is the output of whisper
transcription_text = ""
# Whatever the provider selects from st.selectbox will be used to choose the right system prompt for llama
system_prompt = ""

# Transcribe button
transcribe_button = st.sidebar.button("Transcribe Audio")

if transcribe_button:
    st.text("Model Ready For Use")
    if audio_file is not None:
        st.sidebar.success("Transcribing Audio")
        transcription = model.transcribe(audio_file.name)
        st.sidebar.success("Transcription Complete")
        # TEXT IS TRANSCRIBED HERE FULLY, 
        transcription_text = transcription['text']
    else:
        st.sidebar.error("Please upload the recording of the session with the patient")

st.sidebar.header("Play Original Audio File")
if audio_file is not None:
    st.sidebar.audio(audio_file)

joined_transcribed_text = ""
output = replicate.run(
    "meta/llama-2-70b-chat",
    input={
        "debug": False,
        "top_k": 50,
        "top_p": 1,
        "temperature": 0.5,
        "system_prompt": """You are a tool that takes the transcription of progress notes and/or intake assessments. If the text you recieve is an intake assessment, proceed with usual documentation protocol.
        Otherwise, ensure the progress note is accurately summarize in a way useful for physician/practioner records. Utilize markdown formatting""",
        "prompt": txt,
        "max_new_tokens": 500,
        "min_new_tokens": -1
    },
)


joined_transcribed_text = "".join(i for i in output)
st.write(joined_transcribed_text)