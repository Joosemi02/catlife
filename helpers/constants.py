# CHANCE
CAT_CHANCES = {
    "ash": 1,
    "azure": 1,
    "beige": 1,
    "black": 1,
    "blue": 1,
    "brown": 1,
    "brownie": 1,
    "calico": 1,
    "carrot": 1,
    "chocolate": 1,
    "cinnamon": 1,
    "cloud": 1,
    "coal": 1,
    "cocoa": 1,
    "coffee": 1,
    "cream": 1,
    "garfield": 1,
    "gray": 1,
    "jade": 1,
    "latte": 1,
    "navy": 1,
    "obsidian": 1,
    "ocean": 1,
    "oreo": 1,
    "rust": 1,
    "sand": 1,
    "snow": 1,
    "storm": 1,
    "truffle": 1,
    "white": 1,
}

# ANIMATIONS
FRAME_SCHEME = (
    (7, 6, 6, 6, 7, 6, 6, 6),
    (5, 5, 5, 5, 5, 5, 5, 5),
    (8, 8, 8, 8, 8, 8, 8, 8),
    (4, 4, 4, 4, 4, 4, 4, 4),
    (5, 5, 5, 5, 5, 5, 5, 5),
    (8, 8, 8, 8, 8, 8, 8, 8),
    (8, 8, 8, 8, 8, 8, 8, 8),
)
BIG_RESOLUTION = 265

# COLORS
BLUE = 0x3498DB
EMBED_COLOR = 0x3498DB

# TIMEOUTS
DEFAULT_TIMEOUT = 30

if __name__ == "__main__":
    print(f"Default cat chance: {100/sum(CAT_CHANCES.values())}%")
