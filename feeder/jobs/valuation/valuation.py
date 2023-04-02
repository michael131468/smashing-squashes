from yapsy.IPlugin import IPlugin

import random

class Valuation(IPlugin):
    def __init__(self):
        self.previous_value = 0

    def get_interval(self):
        return 5

    def get_data(self):
        previous_value = self.previous_value
        valuation_value = random.randint(0, 1000)
        self.previous_value = valuation_value

        # Dict Format: key = widget, value = widget data
        data = {
            "valuation": {
                "title": "Valuation",
                "current": valuation_value,
                "last": previous_value,
                "moreinfo": "in billions"
            }
        }

        return data
