import pandas as pd 
import numpy as np
import streamlit as st
import base64
from faster_whisper import WhisperModel
import replicate
import ffmpeg
import logging


# logging.basicConfig(level = logging.DEBUG)
# logger = logging.getLogger(__name__)


st.title("Transcribe & Summarize Patient Conversations")
patient_name = st.text_input('Enter patient name.', 'Jane Doe')
practioner_name = st.text_input('Enter practioner name.', 'Jane Smith, LCSW')
date = st.text_input('Enter date of session, DD-MM-YYYY format', '02-18-2024')
model = "small"
asr_model = WhisperModel('small', device="cpu", compute_type="int8")

sentiment_categories = {
    "fear": np.nan,
    "anger": np.nan,
    "joy": np.nan,
    "sadness": np.nan,
    "surprise": np.nan,
    "disgust": np.nan,
    "trust": np.nan,
    "anticipation": np.nan,
    # Add more sentiment categories as needed
}

transcribed_df = pd.DataFrame(columns = ['Start (seconds)', 'End (seconds)', 'Text'])



audio_file = st.sidebar.file_uploader("Upload Audio", type=["wav", "mp3", "m4a"])
# Transcribe button
transcribe_button = st.sidebar.button("Transcribe Audio")
if transcribe_button:
        if audio_file is not None:
            st.sidebar.success("Transcribing Audio")
            # TEXT IS TRANSCRIBED HERE FULLY, 
            
            transcription_text, info = asr_model.transcribe(audio_file.name)
            st.session_state['parsed_text'] = ''
            
            for i, v in enumerate(transcription_text):
                # this just writes each chunk of the transcription (segment.text) right to streamlit
                # st.write(segment.text)
                st.session_state['parsed_text'] += v.text
                print(v.text)
                transcribed_df.loc[i] = [v.start, v.end, v.text]
            for k, vals in sentiment_categories.items():
                transcribed_df[k] = vals
            st.sidebar.success("Transcription Complete")
            st.dataframe(transcribed_df)
            st.write(transcribed_df.dtypes)
        
        
                 
# st.sidebar.header("Play Original Audio File")
# if audio_file is not None:
#     st.sidebar.audio(audio_file)

# if 'parsed_text' in st.session_state:
#     output = replicate.run(
#     "meta/llama-2-70b-chat",
#     input={
#         "prompt": f"patient name: {patient_name}, practioner_name: {practioner_name}: date: {date}" + "Conversation:\n" + st.session_state['parsed_text'],
#         "system_prompt": """Llama, you are a helpful AI assistant to mental health professionals and therapists that SUMMARIZES (not repeat) the transcription of between a patient and practioner in a highly organized and well written progress note meant for therapists to use. Follow proper protocol for therapists as progress notes are part of their clinical responsibilities.
#         Make sure it is formatted well (name, practioner name, date are provided to you already).
#         Do not make up medication history. ONLY summarize what is given to you. Only include things like social history, medication, etc IF SPECIFIED. 
#         DO NOT offer treatment plan/coping mechanisms.
#         Since it will be a conversation between two people, DO NOT write down what you/the interviewer says.  
#         Take great care to differentiate who is who and only write what the patient says.""",
#         "debug": True,
#         "top_k": 50,
#         "top_p": 1,
#         "temperature": 0.5,
#         "max_new_tokens": 500,
#         "min_new_tokens": -1
#     },
#     )
#     joined_note_output = "".join(i for i in output)
#     st.write(joined_note_output)
