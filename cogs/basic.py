import discord
from discord import app_commands
from discord.ext import commands

class Basic(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="ping", description="Pong!")
    async def ping(self, interaction: discord.Interaction):
        await interaction.response.send_message("Pong!")

    @app_commands.command(name="nya", description="Nyaa!!")
    async def nya(self, interaction: discord.Interaction):
        await interaction.response.send_message("https://preview.redd.it/how-would-happy-chaos-and-neco-arc-interact-v0-wxhndj4ttqib1.jpg?width=957&format=pjpg&auto=webp&s=1d3123f16c307b4e36683c45799841fb5216ccdb")

async def setup(bot):
    await bot.add_cog(Basic(bot))