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


# EMOJIS
FULL_HEART = "<:full_heart:1173298438599885000>"
HALF_HEART = "<:half_heart:1173298439925276792>"
EMPTY_HEART = "<:empty_heart:1173298436569845790>"
HUNGER = "<:hunger:1173304384638173295>"
BOLT = "<:bolt:1173325030118129724>"
SLEEP = "<:sleep:1173314123853987920>"

# COLORS
EMBED_COLOR = 0x3498DB

# TIMEOUTS
DEFAULT_TIMEOUT = 30

if __name__ == "__main__":
    print(f"Default cat chance: {100/sum(CAT_CHANCES.values())}%")
