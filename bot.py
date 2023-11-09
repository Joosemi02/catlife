import os

import discord
import uvicorn
from discord.ext import commands
from dotenv import load_dotenv

from helpers.utils import CatBot

intents = discord.Intents.default()
bot = CatBot(
    intents=intents,
    command_prefix=commands.when_mentioned,
)
bot.activity = discord.Game("catlife!")


@bot.command()
@commands.is_owner()
async def sync(ctx: commands.Context):
    await bot.tree.sync()
    await ctx.send("synced")


def main(bot: CatBot):
    load_dotenv()

    bot.setup_logging()
    bot.run(os.getenv("BOT_TOKEN"), log_handler=None)


if __name__ == "__main__":
    uvicorn.main(main(bot))
