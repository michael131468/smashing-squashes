from yapsy.IPlugin import IPlugin

import random

class Buzzwords(IPlugin):
    def __init__(self):
        self.words = [
            {
                "label": "Single Node Cloud",
                "value": 0
            },
            {
                "label": "Pet Disruption",
                "value": 0
            },
            {
                "label": "Vapourware",
                "value": 0
            },
            {
                "label": "Futureware",
                "value": 0
            },
            {
                "label": "Decrypted Crypto",
                "value": 0
            },
            {
                "label": "Average Devices",
                "value": 0
            },
            {
                "label": "Internet of Beans",
                "value": 0
            },
            {
                "label": "Shell Script Ecosystem",
                "value": 0
            },
            {
                "label": "Inverse Bandwidth",
                "value": 0
            },
            {
                "label": "Legacy Rust Apps",
                "value": 0
            },
            {
                "label": "Manual Intelligence",
                "value": 0
            },
            {
                "label": "Jazz Programmer",
                "value": 0
            },
            {
                "label": "DevSysAdmin",
                "value": 0
            },
            {
                "label": "Extended Virtual",
                "value": 0
            },
            {
                "label": "Slow Agile",
                "value": 0
            },
            {
                "label": "Manual Learning",
                "value": 0
            },
        ]

    def get_interval(self):
        return 30

    def get_data(self):
        for i in range(0, len(self.words)):
            new_count = random.randint(0, 5)
            self.words[i]["value"] += new_count

        # Dict Format: key = widget, value = widget data
        data = {
            "buzzwords": {
                "title": "Buzzwords",
                "items": self.words,
                "moreinfo": "# of times said around the office"
            }
        }

        return data
