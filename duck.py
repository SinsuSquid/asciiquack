from typing import List

class Duck:
    # Right-facing duck
    ART_RIGHT = [
        "      __",
        "    <(o )___",
        "     ( ._> /",
        "      `---'"
    ]
    
    # Left-facing duck
    ART_LEFT = [
        "      __",
        "   ___( o)>",
        "   \\ <_. )",
        "    `---'"
    ]

    def __init__(self, x: int, y: int):
        self.x = float(x)
        self.y = float(y)
        self.vx = 0.5
        self.vy = 0.2
        self.width = 12
        self.height = 4
        self.facing_right = True

    def update(self, bounds_width: int, bounds_height: int):
        self.x += self.vx
        self.y += self.vy

        # Bounce X
        if self.x <= 0:
            self.x = 0
            self.vx *= -1
            self.facing_right = True
        elif self.x + self.width >= bounds_width:
            self.x = bounds_width - self.width
            self.vx *= -1
            self.facing_right = False

        # Bounce Y
        if self.y <= 0:
            self.y = 0
            self.vy *= -1
        elif self.y + self.height >= bounds_height:
            self.y = bounds_height - self.height
            self.vy *= -1

    def get_art(self) -> List[str]:
        return self.ART_RIGHT if self.facing_right else self.ART_LEFT
