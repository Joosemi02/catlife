import logging
import os
from collections import namedtuple

import discord
import structlog
from discord.ext import commands
from dotenv import load_dotenv

import cogs
import helpers
import uvloop

uvloop.install()


class CatBot(commands.Bot):
    class BlueEmbed(discord.Embed):
        def __init__(self, **kwargs):
            color = kwargs.pop("color", helpers.constants.BLUE)
            super().__init__(**kwargs, color=color)

    class Embed(discord.Embed):
        def __init__(self, **kwargs):
            color = kwargs.pop("color", helpers.constants.EMBED_COLOR)
            super().__init__(**kwargs, color=color)

    def __init__(self, **kwargs):
        self.config = kwargs.pop("config", None)
        super().__init__(
            **kwargs, command_prefix=commands.when_mentioned, strip_after_prefix=True
        )
        self.activity = discord.Game("catlife!")

        # Run bot
        self.setup_logging()
        self.run(kwargs["token"], log_handler=None)

    def setup_logging(self):
        self.log: structlog.BoundLogger = structlog.get_logger()

        formatter = structlog.stdlib.ProcessorFormatter(
            processors=[
                structlog.stdlib.ProcessorFormatter.remove_processors_meta,
                structlog.dev.ConsoleRenderer()
                if self.config.DEBUG
                else structlog.processors.JSONRenderer(),
            ],
        )

        handler = logging.StreamHandler()
        handler.setFormatter(formatter)
        root_logger = logging.getLogger()
        root_logger.addHandler(handler)
        root_logger.setLevel(logging.INFO)

    async def setup_hook(self):
        for i in cogs.default:
            await self.load_extension(f"cogs.{i}")
        self.log.info("init")


if __name__ == "__main__":
    Config = namedtuple(
        "Config",
        [
            "MONGODB_URI",
            "DATABASE_NAME",
            "BOT_TOKEN",
            "SERVER_URL",
        ],
    )

    load_dotenv()

    config = Config(
        DATABASE_URI=os.getenv("MONGODB_URI"),
        DATABASE_NAME=os.environ["DATABASE_NAME"],
        BOT_TOKEN=os.environ["BOT_TOKEN"],
        SERVER_URL=os.environ["SERVER_URL"],
    )

    intents = discord.Intents.default()

    CatBot(
        token=config.BOT_TOKEN,
        case_insensitive=True,
        member_cache_flags=discord.MemberCacheFlags.none(),
        allowed_mentions=discord.AllowedMentions(everyone=False, roles=False),
        intents=intents,
        config=config,
    )
