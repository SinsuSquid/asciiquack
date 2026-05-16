from typing import List

class Sun:
    # Winking smiling sun frames
    FRAME_A = [
        "   \\  |  /   ",
        "  -- O u O -- ",
        "   /  |  \\   "
    ]
    
    FRAME_B = [
        "   \\  |  /   ",
        "  -- O u - -- ",
        "   /  |  \\   "
    ]

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.tick = 0
        self.width = 13
        self.height = 3

    def update(self):
        self.tick += 1

    def get_art(self) -> List[str]:
        # Wink every 40 ticks
        if (self.tick // 20) % 2 == 0:
            return self.FRAME_A
        return self.FRAME_B
