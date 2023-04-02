from yapsy.IPlugin import IPlugin

import random

class Convergence(IPlugin):
    def __init__(self):
        self.points = []
        for x in range(0, 9):
            y = random.randint(0, 50)
            self.points.append({"x": x, "y": y})

    def get_interval(self):
        return 2

    def get_data(self):
        del self.points[0]
        self.points.append({"x": self.points[-1]["x"] + 1, "y": random.randint(0, 50)})

        # Dict Format: key = widget, value = widget data
        data = {
            "convergence": {
                "title": "Convergence",
                "points": self.points,
                "moreinfo": "..."
            }
        }

        return data
