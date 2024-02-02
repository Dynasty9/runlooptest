import runloop
from openai import OpenAI
_SYSTEM_MSG = {"role": "system",
               "content": "You are a kind, helpful travel who makes travel suggestions based on a users' prefered weather. " +
               "If you don't know the users' prefered weather, you should probably ask for it!" }


openAIClient = OpenAI()

@runloop.loop
def travel_agent(metadata: dict[str, str], greeting: list[str]) -> tuple[list[str], dict[str, str]]:
    completion = openAIClient.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[_SYSTEM_MSG] + session.history + { "role": "user", "content": message },
    )
    
    # Update our session history & respond to our client with new messages
    return [completion.choices[0].message.content], metadata
