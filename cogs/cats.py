import logging

from discord import Interaction, app_commands
from discord.ext import commands

from helpers.utils import CatBot, generate_cat, merge_cat_images


class Cats(commands.Cog):
    def __init__(self, bot):
        self.bot: CatBot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        logging.info(f"Cog {self.qualified_name} loaded")

    @app_commands.command()
    async def start(self, i: Interaction):
        embed = self.bot.Embed(title="Pick your starter cat")
        cats = []
        while len(cats) < 3:
            cat = generate_cat()
            if cat not in cats:
                cats.append(cat)
                embed.add_field(**cat.embed_field_args)
        embed.set_image(url="attachment://attachment.gif")
        await i.followup.send(embed=embed, file=merge_cat_images(cats))


async def setup(bot):
    await bot.add_cog(Cats(bot))
