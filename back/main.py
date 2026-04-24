import asyncio
import sys

from back_vet.api.core import app

def start_app():
    from subprocess import run
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    run(["py","-m","uvicorn", "main:app","--reload"])