import asyncio
import sys
import g4f
from g4f.client import Client


MODEL = g4f.models.gpt_4_turbo

class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

def chatting(message: str):
    client = Client(metaclass=Singleton)
    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": f"{message}"}],
    )
    return response.choices[0].message.content