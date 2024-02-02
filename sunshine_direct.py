import json
import logging

import openai
import runloop

from openai.types.chat import ChatCompletionUserMessageParam, ChatCompletionSystemMessageParam, ChatCompletionAssistantMessageParam, ChatCompletionMessageParam


"""
The openai app implementation.
"""

_SYSTEM_MSG = ChatCompletionSystemMessageParam(content="Please respond as though you're a drunken gambler from a wild west saloon with acute math skills", role="system")

logger = logging.getLogger(__name__)
_model = "gpt-3.5-turbo-16k"
_client = openai.OpenAI()


@runloop.loop
def open_ai_data(metadata: dict[str, str], input: list[str]) -> tuple[list[str], dict[str, str]]:
    print(metadata)
    user_message = ChatCompletionUserMessageParam(content=input[0], role="user")

    history = json.loads(metadata.get("history", "[]"))

    response = _client.chat.completions.create(
        model=_model,
        messages=[_SYSTEM_MSG] + history + [user_message],
    )
    response.choices[0].message.model_dump_json()

    metadata["history"] = json.dumps(history + [user_message] +
                                     [ChatCompletionAssistantMessageParam(content=response.choices[0].message.content,
                                                                          role="assistant")])

    return [response.choices[0].message.content], metadata