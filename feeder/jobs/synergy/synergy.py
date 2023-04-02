from yapsy.IPlugin import IPlugin

import random

class Synergy(IPlugin):
    def get_interval(self):
        return 10

    def get_data(self):
        synergy_value = random.randint(0, 100)
        # Dict Format: key = widget, value = widget data
        data = {
            "synergy": {
                "title": "Synergy",
                "value": synergy_value,
                "moreinfo": "..."
            }
        }

        return data
