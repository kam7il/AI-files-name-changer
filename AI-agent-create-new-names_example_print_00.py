from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
import os

load_dotenv('.secrets')
os.environ["OPENAI_API_KEY"] = os.getenv('open_ai_api_key')

def generate_new_filenames(filenames: list) -> list:
    # Define the prompt template as a system and user message
    chat_prompt = ChatPromptTemplate.from_messages([
        ("system", """
        Jesteś ekspertem od zmiany nazw plików według ściśle określonych zasad.

        Zasady zmiany nazw plików:
        1) Usuń wszystkie spacje między słowami.
        2) Każde słowo zaczynaj wielką literą, chyba że dotyczy to spójnika jednoliterowego (patrz punkt 5).
        3) Zamień polskie znaki diakrytyczne (ą, ć, ę, ł, ń, ó, ś, ź, ż) na ich podstawowe odpowiedniki (a, c, e, l, n, o, s, z, z).
        4) Nie zmieniaj kolejności słów.
        5) Spójniki i przyimki jednoliterowe (np. i, z, w, o, u):
           - Dołącz do następnego słowa, zaczynając je małą literą.
           - Przykład:
             - "Jeden i dwa lub trzy" → "JedenIdwaLubTrzy"
             - "kurs z excela" → "KursZexcela"
             - "DHCP i konfiguracja" → "DHCPiKonfiguracja"
        6) Słowa zapisane w całości wielkimi literami (CAPSLOCK):
           - Zostaw bez zmian.
           - Jeśli łączysz je z innymi słowami, użyj znaku podkreślenia "_".
           - Przykład:
             - "podstawy z DNS" → "PodstawyZ_DNS"
        7) Usuwaj znaki interpunkyjne, wyjątkiem jest znak "-".
        """),
        ("user",
         "Zmień nazwy następujących plików zgodnie z podanymi zasadami. Zwróć tylko nowe nazwy, każdą w nowej linii:\n{filenames}")
    ])

    # Initializing the model with the appropriate parameters
    llm = ChatOpenAI(
        model="gpt-4o",
        temperature=0.0  # set the temperature low for deterministic responses
    )

    # Combine file names into one string
    filenames_str = "\n".join(filenames)

    # Call the model
    messages = chat_prompt.format_messages(filenames=filenames_str)
    response = llm.invoke(messages)

    # Processing the response
    new_filenames = [name.strip() for name in response.content.strip().split('\n')]
    return new_filenames

if __name__ == '__main__':
    # Sample names to correct
    filenames_list = [
        "Nie daj się cyberzbójom! Szkolenie z cyberbezpieczeństwa dla wszystkich (v6) - edycja wieczorna",
        "Wprowadzenie do sztucznej inteligencji",
        "Zaawansowane techniki programowania",
        "Systemy operacyjne w praktyce",
        "Jak zarządzać czasem",
        "Jak korzystać z DHCP",
        "Linux - co to jest?"
    ]

    result = generate_new_filenames(filenames_list)

    # Print results
    for old, new in zip(filenames_list, result):
        print(f"{old} -> {new}")
