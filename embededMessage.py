import discord
from discord.ui import Button, View


class EmbededMessages:

    def __init__(self, title, description, url, color):
        self.title = title
        self.description = description
        self.url = url
        self.color = int(color.split("\n")[0], 16)
        self.audio_cog = None
        self.interaction = None
        self.button = Button(label=self.description, style=discord.ButtonStyle.blurple, emoji="▶️")

    async def button_callback(self, button_interaction):
        embed = discord.Embed(title=self.title, description=self.description, url=self.url,
                              color=self.color)
        await button_interaction.response.send_message(embed=embed)
        await self.audio_cog.play(self.url, self.interaction)

    def set_cog(self, audio_cog):
        self.audio_cog = audio_cog

    def set_interaction(self, interaction):
        self.interaction = interaction
