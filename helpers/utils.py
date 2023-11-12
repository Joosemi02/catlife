import logging
import random
from datetime import datetime
from logging.handlers import RotatingFileHandler
from typing import Self

from discord import Embed, User, app_commands
from discord.ext import commands
from discord.interactions import Interaction

import cogs

from .constants import BOLT, CAT_CHANCES, EMBED_COLOR, HUNGER
from .db import CATS


class Cat:
    def __init__(
        self, variant, born, health, energy, hunger, owner=None, name=None, id=None
    ):
        self.name: str = name or variant
        self.born: datetime = born
        self.age: str = format_timedelta(born)
        self.health: int = health
        self.energy: int = energy
        self.hunger: int = hunger
        self.variant: str = variant
        self.owner: User | None = owner
        self.id: int | None = id

    def __str__(self) -> str:
        pass

    def __eq__(self, cat: object) -> bool:
        return isinstance(cat, Cat) and self.id == cat.id

    async def add_id(self):
        lowest = CATS.find_one(sort=[("_id", 1)])
        return lowest["_id"] + 1 or 1

    async def set_owner(self, user: User):
        self.owner = user
        await CATS.update_one()

    @classmethod
    async def from_id(cls, id: int) -> Self:
        return cls(**await CATS.find_one({"_id": id}))

    @property
    def embed_field_args(self):
        return {
            "name": f"{self.name}",
            "value": get_stats_string(),
        }


# CATS
def get_random_stats(variant: str):
    points = random.randint(60, 200)
    if variant == "catvariant":
        points = min(points * 1.2, 200)  # 20% boost
    energy = points / 2
    hunger = points / 2
    return {
        "born": datetime.now(),
        "health": 10,
        "energy": int(energy),
        "hunger": int(hunger),
    }


async def generate_cat() -> Cat:
    population = list(CAT_CHANCES.keys())
    weights = list(CAT_CHANCES.values())
    cat = random.choices(population, weights)[0]
    stats = get_random_stats(cat)
    return Cat(variant=cat, **stats)


# FORMAT
def get_stats_string(cat: Cat):
    return f"{cat.energy} {BOLT}\n{cat.hunger} {HUNGER}"


def singularize(amount, unit):
    """singularizer(?) - returns a string containing the amount
    and type of something. The type/unit of item will be pluralized
    if the amount is greater than one."""
    return f"{amount} {amount == 1 and f'{unit}' or f'{unit}s'}"


def format_timedelta(seconds: int) -> str:
    """Converts a timedelta's total_seconds() to a humanized string."""
    mins, secs = divmod(seconds, 60)
    hrs, mins = divmod(mins, 60)
    dys, hrs = divmod(hrs, 24)
    timedict = {"day": dys, "hour": hrs, "minute": mins, "second": secs}
    cleaned = {k: v for k, v in timedict.items() if v != 0}
    return " ".join(singularize(v, k) for k, v in cleaned.items())


# CLASSES
class CatBot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, tree_cls=CatTree)

    class Embed(Embed):
        def __new__(cls, **kwargs):
            color = kwargs.pop("color", EMBED_COLOR)
            return super().__new__(**kwargs, color=color)

    def setup_logging(self):
        logging_format = logging.Formatter(
            "{asctime} {levelname:<8}: {message}",
            "%d-%m-%Y %H:%M:%S",
            "{",
        )
        self.log = logger = logging.getLogger()
        logger.setLevel(logging.INFO)

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(logging_format)
        console_handler.setLevel(logging.INFO)
        logger.addHandler(console_handler)

        file_handler = RotatingFileHandler(
            filename="discord.log",
            encoding="utf-8",
            maxBytes=5 * 1024 * 1024,  # 5 Mb
            backupCount=3,
        )
        file_handler.setFormatter(logging_format)
        file_handler.setLevel(logging.WARN)
        logger.addHandler(file_handler)

    async def setup_hook(self):
        for i in cogs.default:
            await self.load_extension(f"cogs.{i}")
        self.log.info("Bot loaded")


class CatTree(app_commands.CommandTree):
    async def interaction_check(self, i: Interaction):
        await i.response.defer()
        return True
