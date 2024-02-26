# Sante - Transcription of Conversations and Generation of Progress Notes for Mental Health Professionals

*Sante* is an AI-powered transcription and note taking assistant for licensed mental health practioners (talk therapists, psychiatrists, etc). It transcribes patient-provider/physician conversations using [OpenAI's Whisper](https://github.com/openai/whisper) and then lets the provider choose between progress notes, intake assessments, and assesment notes. Upon selection, the output of the transcription is forwarded to LLama-2-70B. This is done using [Replicate](https://replicate.com/meta/llama-2-70b-chat) (none of the inference is done locally), making this *faster than trying to do the inference locally, and no need to have 128GB VRAM and a $30,000 H100 .

Currently, it has a working MVP built with the very easy to work with [Streamlit](https://streamlit.io/cloud). 



## To Dos
* A no brainer, but authentication/user accounts. These progress notes need to have rock solid security. Everything needs to be HIPAA compliant. Recordings, transcriptions, and notes need to be secure. Thankfully, that's not hard if we migrate to ... . 
* **to a standard web application. We will build with NextJS deploy with Vercel**. This MVP is great, but having our own web app where we're fully in control of frontend, routing, API and models/dbs seems a like a no brainer. The only problem is setting up chat interfaces without tools like Gradio/Streamlit is not easy and requires a lot of additional research.
* Implement long-term memory by using ChromaDB. Currently treatment_plan_updates and assessment_notes are yet to be implemented, since we need look at previous notes. We can't do any of that if the model doesn't have any embeddings/documents to gain long-term memory.
* Microphone support. Absolute no brainer feature. We need to be able to let the user record audio and let each additional recording update each iteration of the transcription to make it all around comprehensive and more user-friendly. This also **makes recordings a lot more secure if done in a secure environment, making the need to hop onto a typical web app necessary**.


Instructions 

1. Clone this repo, and run `pip install requirements.txt`. That'll get streamlit, pytorch, whisper, ffmpeg, replicate, torchaudio, and numpy installed. 
2. Get an API token from Replicate since you'll need to utilize LLama-2-70b (or really, any LLM available there that's often used to reduce the odds of a coldstart every call)
3. Set up billing with Replicate (an entire 1 million for 10 cents, which is *nuts*).
4. Have an audio file ready. I use `ffmpeg` to convert wavs to mp3, extra mp4s from mp3s, slice/crop a part of mp3 etc.
    * If you need it, converting an mp4 to mp3 (assuming your conversation was a video) is as easy as ``ffmpeg -i inputFile.mp4 outputFile.mp3``
5. Run the service with `streamlit run app.py` (and enable 'Always rerun in the top right' to enable a debug-like mode)
6. Use the service as needed.