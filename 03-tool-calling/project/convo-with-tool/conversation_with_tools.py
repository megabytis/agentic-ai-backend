import json
import os
from dotenv import load_dotenv
from openai import OpenAI
from langchain.messages import HumanMessage
from datetime import timedelta, datetime


load_dotenv()

API = os.getenv("OPENROUTER_API_KEY")
MODEL = "openrouter/free"
URL = "https://openrouter.ai/api/v1"


# Functions
def get_current_time():
    return datetime.now().strftime("%H:%M:%S")


def get_current_date():
    return datetime.now().strftime("%Y-%m-%d")


def get_current_datetime():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


function_map = {
    "get_current_time": get_current_time,
    "get_current_date": get_current_date,
    "get_current_datetime": get_current_datetime,
}

# Function Schemas
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_current_time",
            "description": "Get current time in HH:MM:SS format",
            "parameters": {"type": "object", "properties": {}},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_current_date",
            "description": "Get current date in YYYY-MM-DD format",
            "parameters": {"type": "object", "properties": {}},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_current_datetime",
            "description": "Get current date and time in YYYY-MM-DD HH:MM:SS format",
            "parameters": {"type": "object", "properties": {}},
        },
    },
]


messages = [
    {
        "role": "system",
        "content": "You are a helpful assistant that helps in solving day to day problems/queries",
    },
]


def add_assistant_message(text):
    assistant_message = {"role": "assistant", "content": text}
    messages.append(assistant_message)


def add_user_message(text):
    user_message = {"role": "user", "content": text}
    messages.append(user_message)


def chat(message, tools=None):
    try:

        client = OpenAI(api_key=API, base_url=URL)
        completion = client.chat.completions.create(
            model=MODEL,
            messages=message,
            tools=tools,
        )
        # response = completion.choices[0].message.content
        return completion

    except ValueError as e:
        print(e)


print("👋 Welcome! I'm your chatbot. Type '/bye' to end the chat.\n")


def start_chatbot():
    while True:
        user_input = input("You: ")
        if user_input.lower() == "/bye":
            print("Goodbye!")
            break

        try:
            add_user_message(user_input)
            
            # 1st API call
            completion = chat(message=messages,tools=tools)

            if completion and hasattr(completion,"choices") and completion.choices:
                message_obj = completion.choices[0].message
                
                # checking wheather the response is calling a tool
                if (
                    hasattr(message_obj, "tool_calls")
                    and message_obj.tool_calls
                ):

                    tool_call = message_obj.tool_calls[0]

                    # Executing tool
                    args = {}
                    if tool_call.function.arguments:
                        args = json.loads(tool_call.function.arguments)
                    else:
                        args = {}
                    func_name = tool_call.function.name
                    func = function_map[func_name]
                    result = func(**args)

                    ## Sending the function result back to the AI model
                    messages.append(completion.choices[0].message)
                    messages.append(
                        {"role": "tool", "tool_call_id": tool_call.id, "content": result}
                    )

                    # Getting final response
                    response2 = chat(message=messages, tools=tools)
                    print(f"Bot: {response2.choices[0].message.content}\n")
                    add_assistant_message(response2.choices[0].message.content)

                else:
                    if message_obj.content:
                        print(f"Bot: {completion.choices[0].message.content}\n")
                        add_assistant_message(completion.choices[0].message.content)
                    else:
                        print("Bot: (No response content)\n")
            else:
                print("DEBUG: No valid response from API")
        except Exception as e:
            import traceback
            traceback.print_exc()


if __name__ == "__main__":
    start_chatbot()
