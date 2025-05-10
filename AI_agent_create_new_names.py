from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv('.secrets')
os.environ["OPENAI_API_KEY"] = os.getenv('open_ai_api_key')

def generate_new_filenames(filenames: list[str | list[str | None]]) -> list[str]:
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
        input=[
            {
                "role": "system",
                "content": [
                    {
                        "type": "input_text",
                        "text": "1) Usuń wszystkie spacje między słowami.\n2) Każde słowo zaczynaj wielką literą, chyba że dotyczy to spójnika lub przyimka jednoliterowego (patrz punkt 5).\n3) Zamień polskie znaki diakrytyczne (ą, ć, ę, ł, ń, ó, ś, ź, ż) na ich podstawowe odpowiedniki (a, c, e, l, n, o, s, z, z).\n4) Nie zmieniaj kolejności słów.\n5) Spójniki i przyimki jednoliterowe (np. i, z, w, o, u) oraz słowa kluczowe (np. find, grep):\n                - Dołącz do następnego słowa, zaczynając je małą literą.\n                    - Przykład:\n                        - \"Jeden i dwa lub trzy\" → \"JedenIdwaLubTrzy\"\n                        - \"kurs z excela\" → \"KursZexcela\"\n                        - \"DHCP i konfiguracja\" → \"DHCPiKonfiguracja\"\n                        - \"Polecenia find i grep\" → \"PoleceniaFindiGrep\"\n6) Słowa zapisane w całości wielkimi literami (CAPSLOCK):\n                - Zostaw bez zmian.\n                - Jeśli łączysz je z innymi słowami, użyj znaku podkreślenia \"_\".\n                    - Przykład:\n                        - \"podstawy z DNS\" → \"PodstawyZ_DNS\"\n7) Usuwaj znaki interpunkyjne, wyjątkiem jest znak \"-\"."
                    }
                ]
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "input_text",
                        "text": filenames_str
                    }
                ]
            }
        ],
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
