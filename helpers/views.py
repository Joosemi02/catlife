from discord import Interaction
from discord.ui import View, button


class StarterCatView(View):
    def __init__(self, *, timeout: float | None = 180):
        super().__init__(timeout=timeout)

    @button
    async def one(self, i: Interaction, _):
        pass

    @button
    async def two(self, i: Interaction, _):
        pass

    @button
    async def three(self, i: Interaction, _):
        pass

    async def choose_cat(self):
        pass
