from typing import List

class Sun:
    # A balanced, high-quality cartoon sun
    # '·' is used for solid-fill placeholder logic in ui.py
    FRAME_A = [
        "      \\ | /      ",
        "    .-'---'-.    ",
        " --(··O·u·O··)-- ",
        "    '-.---.-'    ",
        "      / | \\      "
    ]
    
    FRAME_B = [
        "      \\ | /      ",
        "    .-'---'-.    ",
        " --(··-·u·O··)-- ",
        "    '-.---.-'    ",
        "      / | \\      "
    ]

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.tick = 0
        self.width = 17
        self.height = 5

    def update(self):
        self.tick += 1

    def get_art(self) -> List[str]:
        # Wink logic
        if (self.tick // 20) % 2 == 0:
            return self.FRAME_A
        return self.FRAME_B
