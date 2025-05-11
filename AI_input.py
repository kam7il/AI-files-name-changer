def build_ai_input(filenames_str: str) -> list[dict[str, str | list]]:
    return [
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
    ]
