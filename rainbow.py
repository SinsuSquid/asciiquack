from typing import List

class Rainbow:
    # A multi-layered colorful arc
    # Characters represent different colors in ui.py
    ART = [
        "      .-------.      ",
        "    ./RRRRRRRRR\\.    ",
        "   /RRRRRRRRRRRRR\\   ",
        "  /MMMMMMMMMMMMMMM\\  ",
        " |MMMMMMMMMMMMMMMMM| ",
        " |YYYYYYYYYYYYYYYYY| "
    ]

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.width = 21
        self.height = 6
        self.duration = 200 # How many ticks it stays visible
        self.tick = 0

    def update(self) -> bool:
        self.tick += 1
        return self.tick < self.duration

    def get_art(self) -> List[str]:
        return self.ART
