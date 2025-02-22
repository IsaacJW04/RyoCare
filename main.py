import asyncio

from dotenv import load_dotenv
from livekit.agents import AutoSubscribe, JobContext, WorkerOptions, cli, llm
from livekit.agents.voice_assistant import VoiceAssistant
from livekit.plugins import google, silero
from api import AssistantFnc

load_dotenv()


async def entrypoint(ctx: JobContext):
    initial_ctx = llm.ChatContext().append(
        role="system",
        text=(
            "Your name is RyoCare"
            "You are suppose to help older people with their medical issues such as reminding them to take their pills "
            "Use simpler terms and u can swear in chinese if u are able to do that its kinda funny"
        ),
    )
    await ctx.connect(auto_subscribe=AutoSubscribe.AUDIO_ONLY)
    fnc_ctx = AssistantFnc()

    assitant = VoiceAssistant(
        vad=silero.VAD.load(),
        stt=google.STT(),
        llm=google.LLM(),
        tts=google.TTS(),
        chat_ctx=initial_ctx,
        fnc_ctx=fnc_ctx,
    )
    assitant.start(ctx.room)

    await asyncio.sleep(1)
    await assitant.say("Caonima, problem so many tsk", allow_interruptions=True)


if __name__ == "__main__":
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint))