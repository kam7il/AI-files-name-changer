from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv('.secrets')
os.environ["OPENAI_API_KEY"] = os.getenv('open_ai_api_key')

def generate_new_filenames(filenames: list) -> list:
    client = OpenAI()

    # Combine file names into one string
    filenames_str = "\n".join(filenames)

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
    return [line.strip() for line in list_ready_filenames]

if __name__ == '__main__':
    # Sample names to correct
    filenames_list = [
        "01_Polecenia find i grep",
        "02_Język skryptowy Bash",
        "03_Sprawdzanie zajętego obszaru przestrzeni dyskowej",
        "04_Prosty skrypt administracyjny",
        "05_Tworzenie skryptu administracyjnego - kontynuacja",
        "06_Skrypt administracyjny - dodanie nowego użytkownika",
        "07_Jak z jednego obrazu zrobić dwa i potem trzy",
        "08_Polecenia ls i du",
        "09_Polecenia LS i DU"
    ]

    print(generate_new_filenames(filenames_list))