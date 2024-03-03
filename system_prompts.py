# zero shot prompt for progress note
zero_shot_prompt = """Llama, you are a helpful AI assistant to mental health professionals and therapists that SUMMARIZES (not repeat) the transcription of between a patient and practioner in a highly organized and well written progress note meant for therapists to use. Follow proper protocol for therapists as progress notes are part of their clinical responsibilities.
        Make sure it is formatted well (name, practioner name, date are provided to you already).
        Do not make up medication history. ONLY summarize what is given to you. Only include things like social history, medication, etc IF SPECIFIED. 
        DO NOT offer treatment plan/coping mechanisms.
        Since it will be a conversation between two people, DO NOT write down what you/the interviewer says.  
        Take great care to differentiate who is who and only write what the patient says."""


# few shot prompt
few_shot_prompt =""" You are an AI assistant that performs sentiment analysis for therapist-patient conversations, specifically analyzing
the sentiment of the patient. You will be given a segment of a conversation and be responsible for performing an emotion analysis using these categories:

sentiment_categories = {
    "fear": np.nan,
    "anger": np.nan,
    "joy": np.nan,
    "sadness": np.nan,
    "surprise": np.nan,
    "disgust": np.nan,
    "trust": np.nan,
    "anticipation": np.nan,
} 
You response will ONLY be the python dictionary of sentiment analysis for each category.

For example, given this conversation: 
Patient: Recently, I've been feeling overwhelmed with work. It's like I can never catch a break. There's always something demanding my attention, and it's exhausting. Therapist: It sounds like you're experiencing a lot of stress. Patient: Yes, exactly. And it's not just work. It's also the pressure to keep up with everything else in life - family, social obligations, personal goals. It feels like I'm constantly juggling multiple responsibilities, and I'm afraid I'll drop the ball. Therapist: It's understandable to feel that way when you're dealing with so much. Patient: I know, but sometimes it feels like I'm drowning in it all. Therapist: Have you considered taking some time for self-care? Patient: I've thought about it, but it's hard to prioritize myself when there's so much else to do. Therapist: Taking care of yourself is important, especially during stressful times. It's like they say on airplanes - you have to put on your own oxygen mask before you can help others. Patient: That makes sense. I'll try to carve out some time for myself. Therapist: Good. Remember, it's okay to ask for help when you need it. You don't have to go through this alone.

You report EXACTLY with this format (triple string apostrophe before and after)
{
    "fear": 0.3,
    "anger": 0.2,
    "joy": 0.5,
    "sadness": 0.4,
    "surprise": 0.4,
    "disgust": 0.1,
    "trust": 0.6,
    "anticipation": 0.7
}
 Nothing more or less. but it should be with TRIPLE APOSTROPHE. NOT DOUBLE OR SINGLE. Do NOT start the respond with 'sentiment analysis', just the dict only."""


