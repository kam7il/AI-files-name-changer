from AI_input import build_ai_input
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv('.secrets')
os.environ["OPENAI_API_KEY"] = os.getenv('open_ai_api_key')

def generate_new_filenames(filenames: list[str | list[str | None]]) -> list[str] | list[list[str]]:
    is_list = False

    # Combine file names into one string
    if not filenames:
        raise ValueError('Filenames list is empty')
    if all([isinstance(filename_lst, list) for filename_lst in filenames]):
        is_list = True
        filenames_str = "\n".join([current_name[0] for current_name in filenames])
    elif all([isinstance(filename_str, str) for filename_str in filenames]):
        filenames_str = "\n".join(filenames)
    else:
        raise ValueError('Unsupported file type in list')

    client = OpenAI()
    # Define the prompt template as a system and user message
    response = client.responses.create(
        model="gpt-4o",
        input=build_ai_input(filenames_str),
        text={
            "format": {
                "type": "text"
            }
        },
        reasoning = {},
        tools = [],
        temperature = 0,
        max_output_tokens = 1000,
        top_p = 0,
        store = False
    )

    output_text = response.output_text
    list_ready_filenames = output_text.split('\n')
    if is_list:
        for filename_lst, line in zip(filenames, list_ready_filenames):
                filename_lst[1] = line.strip()
        return filenames
    else:
        return [line.strip() for line in list_ready_filenames]
