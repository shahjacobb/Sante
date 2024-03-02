import streamlit as st
from st_audiorec import st_audiorec
import base64
from fpdf import FPDF
from faster_whisper import WhisperModel
import replicate
import ffmpeg

asr_model = WhisperModel('tiny', device="cpu", compute_type="int8")


st.title("Transcribe & Summarize Patient Conversations")
patient_name = st.text_input('Enter patient name.', 'Jane Doe')
practioner_name = st.text_input('Enter practioner name.', 'Jane Smith, LCSW')
date = st.text_input('Enter date of session, DD-MM-YYYY format', '02-18-2024')

if patient_name and practioner_name and date:
    # upload audio file with streamlit in the sidebar
    audio_file = st.sidebar.file_uploader("Upload Audio", type=["wav", "mp3", "m4a"])
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

# to create a download link, will be triggered when button is clicked
def create_download_link(val, filename):
        b64 = base64.b64encode(val)  
        return f'<a href="data:application/octet-stream;base64,{b64.decode()}" download="{filename}.pdf">Download file</a>'

if 'parsed_text' in st.session_state:
    output = replicate.run(
    "meta/llama-2-70b-chat",
    input={
        "prompt": f"patient name: {patient_name}, practioner_name: {practioner_name}: date: {date}" + "Conversation:\n" + st.session_state['parsed_text'],
        "system_prompt": """Llama, you are a helpful AI assistant to mental health professionals and therapists that SUMMARIZES (not repeat) the transcription of between a patient and practioner in a highly organized and well written progress note meant for therapists to use. Follow proper protocol for therapists as progress notes are part of their clinical responsibilities.
        Make sure it is formatted well (name, practioner name, date are provided to you already).
        Do not make up medication history. ONLY summarize what is given to you. Only include things like social history, medication, etc IF SPECIFIED. 
        DO NOT offer treatment plan/coping mechanisms.
        Since it will be a conversation between two people, DO NOT write down what you/the interviewer says.  
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
    # will add functionality later - export_btn = st.button('Export Progress Note as PDF')
    # this is how streamlit handles event listeners, just check if true

# streamlit's magic automatically writes triple strings ... so 
pdf_functionality =  ''' if export_btn:
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font('Inter', 12)
        pdf.cell(200, 10, joined_note_output, ln = True)
        pdf.output('F', f'{patient_name}-Progress-Note-{date}.pdf')
        html = create_download_link(f'{patient_name}-Progress-Note-{date}.pdf')
        st.markdown(html, unsafe_allow_html=True

'''

