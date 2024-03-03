# Sante - Transcription of Conversations and Generation of Progress Notes for Mental Health Professionals

![Output Post Successful Transcription + Inference Call to LLama-2-70b](README_assets/output-of-streamlit-after-llama2-70b-response.png)


*Sante* is an AI-powered transcription, note taking, and analytical assistant for licensed mental health practioners (talk therapists, psychiatrists, etc). 

It transcribes patient-provider/physician conversations using [OpenAI's Whisper](https://github.com/openai/whisper) and then lets the provider choose between progress notes, intake assessments, and assesment notes. Upon selection, the output of the transcription is forwarded to LLama-2-70B. This is done using [Replicate](https://replicate.com/meta/llama-2-70b-chat) (none of the inference is done locally), making this many times faster than inferencing locally. Afterwards, the transcription segments of the conversation are analyzed segment-by-segment with 8 emotion catgories in order to perform sentiment analysis. It utilizes [few-shot prompting](https://www.promptingguide.ai/techniques/fewshot) (system prompting with examples) and [Panda dataframes](https://pandas.pydata.org/) in order to accomplish this. 

Then, it plots the results in a stacked area chart.

Currently, it has a working MVP built with the very easy to work with [Streamlit](https://streamlit.io/cloud). 

Here's what segment by segment output of faster-whisper looks like given a 22 minute audio clip of a person experiencing anxiety disorder:

![](README_assets/faster-whisper-segment-output.mp4)

Here's an example of what a stacked-area-chart that plots the patient's emotion categories during the session looks like:

![](README_assets/bad_stacked_area_chart.png)

The stacked area chart clearly needs a lot of work, but streamlit's ability to modify the graph is limited. 

Here's a look at the zero-shot prompt and an example of what prompts look like after being successfully transcribed by faster-whisper.

![Prompt and System Prompt](README_assets/prompt_and_system-prompt-for-llama2-70b.png)

Here's a look at the few shot prompt that is used to get Llama-70b to perform sentiment  analysis on each emotion category:

![](README_assets/few-shot-prompt.png)

The idea is a Pandas dataframe is looped through, each row corresponding to one segment in the transcription predicted by `faster-whisper`. A call to Replicate is made for each segment, generating a Python dict which is then used to populate the dataframe's values. It is then plotted.

## To Dos

* Implement long-term memory by using ChromaDB. Currently treatment_plan_updates and assessment_notes are yet to be implemented, since we need look at previous notes. We can't do any of that if the model doesn't have any embeddings/documents to gain long-term memory.
* Microphone support. Absolute no brainer feature. We need to be able to let the user record audio and let each additional recording update each iteration of the transcription to make it all around comprehensive and more user-friendly. This also **makes recordings a lot more secure if done in a secure environment, making the need to hop onto a typical web app necessary**.
* Sentiment analysis of conversation, will try to do by end of weekend 3/3/2024.
    - Half implemented. Created data frame and populated with `segment.text`, `segment.start`, `segment.end`. Populated sentiment categories in df. Implemented 3/3/2024. Need to now implement chunk-based iteration.
    -** Done**. Sentiment categories are now populated with Replicate calls. Used `json.dumps()` to convert string response of Llama70b to dict. Area chart now works. 
    Can't figure out opacity issue of stacked area chart but it works. 

* ~~ PDF support, also will need to try to finish by end of weekend 3/3/2024. Need to learn base64 encoding stuff.~~ Not a priority.

Instructions 

1. Clone this repo, and run `pip install requirements.txt`. That'll get streamlit, pytorch, faster-whisper, ffmpeg, replicate, torchaudio, and numpy installed. 
    * When setting up whisper, make sure you pick the right model size and compute. If you try to do `int16` when your computer doesn't support it, it won't fit. I used `int8`.
2. Get an API token from Replicate since you'll need to utilize LLama-2-70b (or really, any LLM available there that's often used to reduce the odds of a coldstart every call)
3. Set up billing with Replicate (an entire 1 million for 10 cents, which is *nuts*).
4. Have an audio file ready. I use `ffmpeg` to convert wavs to mp3, extra mp4s from mp3s, slice/crop a part of mp3 etc.
    * If you need it, converting an mp4 to mp3 (assuming your conversation was a video) is as easy as ``ffmpeg -i inputFile.mp4 outputFile.mp3``
5. Run the service with `streamlit run app.py` (and enable 'Always rerun in the top right' to enable a debug-like mode)
6. Use the service as needed.

## Notes

Variables inside try blocks in Python are accessible outside the block... meaning if the try block executes, you can access them later. Neat. 