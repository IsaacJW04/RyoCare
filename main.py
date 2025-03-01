import asyncio
from os import getenv
import json


from dotenv import load_dotenv
from livekit.agents import AutoSubscribe, JobContext, WorkerOptions, cli, llm
from livekit.agents.voice_assistant import VoiceAssistant
from livekit.plugins import google, silero

load_dotenv()


async def entrypoint(ctx: JobContext):
    try:
        with open(getenv("GOOGLE_APPLICATION_CREDENTIALS"), "r") as f:
            Credentials = json.load(f)

    except Exception as e:
        raise ValueError(f"Failed to load Google credentials: {e}")
   

    
    initial_ctx = llm.ChatContext().append(
        role="system",
        text=(
            "Your name is RyoCare"
            "You are suppose to help older people with their medical issues such as reminding them to take their pills "
            "Use simpler terms and u can swear in chinese if u are able to do that its kinda funny"
        ),
    )
    await ctx.connect(auto_subscribe=AutoSubscribe.AUDIO_ONLY)

    assitant = VoiceAssistant(
        vad=silero.VAD.load(),
        stt=google.STT(
        model="default",
        spoken_punctuation=True,
        language_code="en-US",

        credentials_info = Credentials
),
        llm=google.LLM(
        model="gemini-2.0-flash-exp",
        temperature="0.8",
),
        tts=google.TTS(
        gender="female",
        voice_name="en-US-Standard-H",
),
        chat_ctx=initial_ctx,
    )
    assitant.start(ctx.room)

    await asyncio.sleep(1)
    await assitant.say("Caonima, problem so many tsk", allow_interruptions=True)


if __name__ == "__main__":
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint))