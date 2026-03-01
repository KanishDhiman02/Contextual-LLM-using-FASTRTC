import os
import numpy as np
from fastrtc import Stream, ReplyOnPause, get_stt_model, get_tts_model, AlgoOptions, SileroVadOptions
from groq import Groq
from dotenv import load_dotenv
load_dotenv()
if not os.getenv("GORQ_API_KEY"):
    raise ValueError("unable to fetch api ley from .env")
client = Groq(api_key=os.getenv("GORQ_API_KEY"))

# trying to give model info about the project
def get_context():
    try:
        with open("project_info.txt", "r") as f:
            return f.read()
    except FileNotFoundError:
        return "project is about building a demo Fast RTC implementation and providing the llm a context about the project so that i can answer some basic project question "

# intializing 
stt = get_stt_model()
tts = get_tts_model()
project_context = get_context()

def process_audio(audio: tuple[int, np.ndarray]):
    # converting speech to text
    raw_text = stt.stt(audio)
    print(f"User: {raw_text}")
    if not raw_text or len(raw_text.strip()) < 2:
        return

    system_prompt = f"""
    You are a Technical Assistant for Kanish Dhiman.
    PROJECT CONTEXT: {project_context}
    
    INSTRUCTIONS:
    - Answer briefly (max 15 words).
    - Use the context for project questions.
    - If asked general tech questions (like histogram equalization or Lamport clocks), 
      answer accurately but briefly.
    """

    # using groq llama 3.1 8b for fast speed
    resp = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "system", "content": system_prompt},{"role": "user", "content": raw_text}],
        stream=True
    )

    # waiting for natural breaks for fuent speaking
    full_resp = ""
    print("AI : ", end="",flush=True)
    for chunk in resp:
        if chunk.choices[0].delta.content:
            content = chunk.choices[0].delta.content
            full_resp += content
            
            print(content,end="",flush=True)
            # 
            if any(p in content for p in [".", "!", "?", ":", "\n"]):
                for audio_chunk in tts.stream_tts_sync(full_resp.strip()):
                    yield audio_chunk
                full_resp = "" 
    
    print()
    
    # final check for uncomplete sentences 
    if full_resp.strip():
        for audio_chunk in tts.stream_tts_sync(full_resp.strip()):
            yield audio_chunk

# having high background noise so launching with high background noise tolerance 
stream = Stream(
    handler=ReplyOnPause(
        process_audio,
        algo_options=AlgoOptions(
            audio_chunk_duration=0.6,
            speech_threshold=0.4 
        ),
        model_options=SileroVadOptions(
            min_silence_duration_ms=800, 
            threshold=0.8                
        )
    ),
    modality="audio",
    mode="send-receive"
)

if __name__ == "__main__":
    stream.ui.launch(share=True) # for making a public access link