import logging

from discord.ext import commands

from helpers.utils import CatBot


class Cats(commands.Cog):
    def __init__(self, bot):
        self.bot: CatBot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        logging.info(f"Cog {self.qualified_name} loaded")


async def setup(bot):
    await bot.add_cog(Cats(bot))
