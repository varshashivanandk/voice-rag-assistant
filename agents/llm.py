# Small wrapper around the Groq API (the LLM / foundation model).

import os

from config import GROQ_MODEL


class LLMError(Exception):
    pass


def is_available():
    return bool(os.environ.get("GROQ_API_KEY"))


def chat(system_prompt, user_prompt, max_tokens=600):
    """Send one request to the LLM and return its text reply."""
    if not is_available():
        raise LLMError("GROQ_API_KEY is not set. Add it to the .env file.")
    try:
        from groq import Groq
        client = Groq(api_key=os.environ["GROQ_API_KEY"])
        reply = client.chat.completions.create(
            model=GROQ_MODEL,
            messages=[{"role": "system", "content": system_prompt},
                      {"role": "user", "content": user_prompt}],
            temperature=0,          # same question -> same answer, fewer made-up details
            max_tokens=max_tokens,
        )
        return reply.choices[0].message.content.strip()
    except Exception as error:
        raise LLMError(f"LLM request failed: {error}") from error
