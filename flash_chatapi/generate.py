import asyncio
import logging
import os
from itertools import cycle
from typing import Any

import aiolimiter
import openai
import openai.error
from aiohttp import ClientSession
from tqdm.asyncio import tqdm_asyncio


async def _throttled_openai_chat_completion_acreate(
    model: str,
    messages: list[dict[str, str]],
    temperature: float,
    max_tokens: int,
    top_p: float,
    limiter: aiolimiter.AsyncLimiter,
    api_keys: cycle,  # Added
) -> dict[str, Any]:
    async with limiter:
        for _ in range(3):
            try:
                openai.api_key = next(api_keys)  # Added
                return await openai.ChatCompletion.acreate(
                    model=model,
                    messages=messages,
                    temperature=temperature,
                    max_tokens=max_tokens,
                    top_p=top_p,
                )
            except openai.error.RateLimitError:
                logging.warning(
                    "OpenAI API rate limit exceeded. Sleeping for 10 seconds."
                )
                await asyncio.sleep(10)
            except asyncio.exceptions.TimeoutError:
                logging.warning("OpenAI API timeout. Sleeping for 10 seconds.")
                await asyncio.sleep(10)
            except openai.error.InvalidRequestError:
                logging.warning("OpenAI API Invalid Request: Prompt was filtered")
                return {
                    "choices": [
                        {"message": {"content": "Invalid Request: Prompt was filtered"}}
                    ]
                }
            except openai.error.APIConnectionError:
                logging.warning(
                    "OpenAI API Connection Error: Error Communicating with OpenAI"
                )
                await asyncio.sleep(10)
            except openai.error.Timeout:
                logging.warning("OpenAI APITimeout Error: OpenAI Timeout")
                await asyncio.sleep(10)
            except openai.error.APIError as e:
                logging.warning(f"OpenAI API error: {e}")
                break
        return {"choices": [{"message": {"content": "OpenAI API Error: Unknown"}}]}


async def generate_from_openai_chat_completion(
    chats: list[list[dict[str, str]]],
    model: str,
    temperature: float = 0.5,
    max_tokens: int = 100,
    top_p: float = 1,
    context_length: int = 2048,
    requests_per_minute: int = 300,
    api_keys: list[str] = None,  # Updated
) -> list[str]:
    if api_keys is None:
        if "OPENAI_API_KEY" not in os.environ:
            raise ValueError(
                "OPENAI_API_KEY environment variable must be set if no api_keys are provided."
            )
        else:
            api_keys = [os.environ["OPENAI_API_KEY"]]
    
    api_keys = cycle(api_keys)  # Added

    openai.aiosession.set(ClientSession())
    limiter = aiolimiter.AsyncLimiter(requests_per_minute)
    async_responses = [
        _throttled_openai_chat_completion_acreate(
            model=model,
            messages=chat,
            temperature=temperature,
            max_tokens=max_tokens,
            top_p=top_p,
            limiter=limiter,
            api_keys=api_keys,  # Added
        )
        for chat in chats
    ]
    responses = await tqdm_asyncio.gather(*async_responses)
    await openai.aiosession.get().close()
    return [x["choices"][0]["message"]["content"] for x in responses]
