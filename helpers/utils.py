import logging
from logging.handlers import RotatingFileHandler

from discord import Embed, app_commands
from discord.ext import commands
from discord.interactions import Interaction

import cogs

from .constants import BLUE, EMBED_COLOR


class CatBot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, tree_cls=CatTree)

    class BlueEmbed(Embed):
        def __init__(self, **kwargs):
            color = kwargs.pop("color", BLUE)
            super().__init__(**kwargs, color=color)

    class Embed(Embed):
        def __init__(self, **kwargs):
            color = kwargs.pop("color", EMBED_COLOR)
            super().__init__(**kwargs, color=color)

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
