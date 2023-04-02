from yapsy.IPlugin import IPlugin

import random

class Welcome(IPlugin):
    def get_interval(self):
        return 30

    def get_data(self):
        random_words = [
            "Welcome!",
            "¡Bienvenido!",
            "Bienvenue!",
            "Välkommen!",
            "Witaj!",
            "Willkommen!"
        ]

        random_word = random.choice(random_words)

        # Dict Format: key = widget, value = widget data
        data = {
            "welcome": {
                "title": "Latest word",
                "text": random_word,
                "moreinfo": "..."
            }
        }

        return data
