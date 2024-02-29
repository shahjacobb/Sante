import streamlit as st
import whisper
from faster_whisper import WhisperModel
import replicate
import ffmpeg

# system prompts
# from prompt_strings import progress_note, treatment_plan_update

asr_model = WhisperModel('tiny', device="cpu", compute_type="int8")

# upload audio file with streamlit in the sidebar
audio_file = st.sidebar.file_uploader("Upload Audio", type=["wav", "mp3", "m4a"])

# if audio_file.name.str.endswith(('.wav', 'm4a')):


st.title("Transcribe & Summarize Patient Conversations")
patient_name = st.text_input('Enter patient name.', 'Jane Doe')
practioner_name = st.text_input('Enter practioner name.', 'Jane Smith, LCSW')
date = st.text_input('Enter date of session, DD-MM-YYYY format', '02-18-2024')
# will add this functiolaity later: note_type = st.selectbox('Transcribed Note Template', ('GIRP', 'TEST'), placeholder= 'Select the type of progress note')


# Transcribe button
transcribe_button = st.sidebar.button("Transcribe Audio")

if transcribe_button:
    if audio_file is not None:
        st.sidebar.success("Transcribing Audio")
        # TEXT IS TRANSCRIBED HERE FULLY, 
        transcription_text, info = asr_model.transcribe(audio_file.name)
        st.session_state['parsed_text'] = ''
        st.sidebar.success("Transcription Complete")
        
        for segment in transcription_text:
            # this just writes each chunk of the transcription (segment.text) right to streamlit
            # st.write(segment.text)
            print(segment.text)
            st.session_state['parsed_text'] += segment.text

st.sidebar.header("Play Original Audio File")
if audio_file is not None:
    st.sidebar.audio(audio_file)


if 'parsed_text' in st.session_state:
    output = replicate.run(
    "meta/llama-2-70b-chat",
    input={
        "prompt": f"patient name: {patient_name}, practioner_name: {practioner_name}: date: {date}" + "Conversation:\n" + st.session_state['parsed_text'],
        "system_prompt": """You are a helpful AI assistant to counscelors/therapists/psychiatrists that summarizes the transcription of the conversation in a highly organized and well written progress note. 
        Make sure it is formatted well (name, practioner name, date are provided to you already)
        Do not make up medication history. Only summarize what is given to you. Since it will be a conversation between two people, DO NOT write down what you/the interviewer says. YOU ARE NOT THE PATIENT. 
        Take great care to differentiate who is who and only write what the patient says.""",
        "debug": True,
        "top_k": 50,
        "top_p": 1,
        "temperature": 0.5,
        "max_new_tokens": 500,
        "min_new_tokens": -1
    },
    )
    joined_note_output = "".join(i for i in output)
    st.write(joined_note_output)





