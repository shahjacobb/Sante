import replicate




prompt = '''
It sounds like you have had a significant journey with anxiety and panic attacks, and it's great that you are now feeling more comfortable opening up about your experiences. It's important to remember that mental health is just as important as physical health, and seeking help when needed is a sign of strength, not weakness.

It's interesting that you mentioned the physical symptoms of anxiety, such as stomach pain and hyperventilating, as these can be very uncomfortable and disruptive to daily life. It's also understandable that you felt embarrassed about your anxious ticks as a child, but it's helpful to recognize that these behaviors were likely a way of coping with your anxiety.

It's great that you have found medication to be helpful in managing your anxiety, and it's important to remember that taking medication doesn't mean you're weak or flawed. It's simply a tool to help manage a common medical condition.

I would encourage you to continue sharing your story and experiences with others, as this can help break down the stigma surrounding mental health issues and inspire others to seek help if they need it. Remember that you are not alone in your struggles, and that there is always support available for those who are willing to reach out.

Finally, it might be helpful to explore other ways to manage your anxiety, such as therapy, mindfulness practices, or relaxation techniques. These can be used in conjunction with medication to provide additional support and help you feel more confident and in control.'''


output = replicate.run(
    "replicate-internal/staging-llama-2-70b-chat-hf-mlc:a0a2781978454e825c3b81e87d6cff5928c43ad81bdc23b5cf11300d40b92916",
    input={
        "debug": True,
        "top_p": 1,
        "prompt": prompt,
        "temperature": 0.5,
        "system_prompt": """Llama, you are a helpful AI assistant to mental health professionals and therapists that SUMMARIZES (not repeat) the transcription of between a patient and practioner in a highly organized and well written progress note meant for therapists to use. Follow proper protocol for therapists as progress notes are part of their clinical responsibilities.
        Make sure it is formatted well (name, practioner name, date are provided to you already). Use Markdown to include things like headings, italics, etc. Follow Markdown heaving/style conventions.
        Do not make up medication history. ONLY summarize what is given to you. Only include things like social history, medication, etc IF SPECIFIED. 
        DO NOT offer treatment plan/coping mechanisms.
        Since it will be a conversation between two people, DO NOT write down what you/the interviewer says.  
        Take great care to differentiate who is who and only write what the patient says.""",
        "max_new_tokens": 500,
        "min_new_tokens": -1
    }
)

# The replicate-internal/staging-llama-2-70b-chat-hf-mlc model can stream output as it's running.
# The predict method returns an iterator, and you can iterate over that output.
for item in output:
    # https://replicate.com/replicate-internal/staging-llama-2-70b-chat-hf-mlc/api#output-schema
    print(item, end="")