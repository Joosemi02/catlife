import contextlib
import logging
import os
from logging.handlers import RotatingFileHandler

import discord

uv = False
with contextlib.suppress(ModuleNotFoundError):
    import uvloop

    uv = True

from discord.ext import commands
from dotenv import load_dotenv

import cogs
from helpers import constants
from helpers.translator import CatTranslator

if uv:
    uvloop.install()


class CatBot(commands.Bot):
    class BlueEmbed(discord.Embed):
        def __init__(self, **kwargs):
            color = kwargs.pop("color", constants.BLUE)
            super().__init__(**kwargs, color=color)

    class Embed(discord.Embed):
        def __init__(self, **kwargs):
            color = kwargs.pop("color", constants.EMBED_COLOR)
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
        await self.tree.set_translator(CatTranslator())
        self.log.info("Bot loaded")


intents = discord.Intents.default()
bot = CatBot(
    intents=intents,
    command_prefix=commands.when_mentioned,
)
bot.activity = discord.Game("catlife!")


@bot.command()
async def sync(ctx: commands.Context):
    await bot.tree.sync()
    await ctx.send("synced")


if __name__ == "__main__":
    load_dotenv()

    bot.setup_logging()
    bot.run(os.getenv("BOT_TOKEN"), log_handler=None)
