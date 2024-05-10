import random
from typing import List, Optional

from openai import OpenAI


def gpt35_turbo(
    history: List[List[Optional[str]]],
    temperature: float = 1,
    top_p: float = 0.9,
    max_output_tokens: int = 2048,
):
    client = OpenAI()
    messages = []
    for human, ai in history:
        if human:
            messages.append({"role": "user", "content": human})
        if ai:
            messages.append({"role": "assistant", "content": ai})

    stream = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        stream=True,
        temperature=temperature,
        top_p=top_p,
        max_tokens=max_output_tokens,
    )
    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            yield chunk.choices[0].delta.content


def gpt4_turbo(
    history: List[List[Optional[str]]],
    temperature: float = 1,
    top_p: float = 0.9,
    max_output_tokens: int = 2048,
):
    client = OpenAI()
    messages = []
    for human, ai in history:
        if human:
            messages.append({"role": "user", "content": human})
        if ai:
            messages.append({"role": "assistant", "content": ai})

    stream = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=messages,
        stream=True,
        temperature=temperature,
        top_p=top_p,
        max_tokens=max_output_tokens,
    )
    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            yield chunk.choices[0].delta.content


def get_all_models():
    return [
        {
            "name": "gpt-3.5-turbo",
            "model": gpt35_turbo,
        },
        {
            "name": "gpt-4-turbo",
            "model": gpt4_turbo,
        },
    ]


def get_random_models(number: int = 2):
    return random.sample(get_all_models(), number)
