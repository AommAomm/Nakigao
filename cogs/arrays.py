import discord
from discord import app_commands
from discord.ext import commands

class Arrays(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="sort", description="Sorts a list of numbers")
    async def sort(self, interaction: discord.Interaction, numbers: str):
        try:
            num_list = list(map(int, numbers.split()))
            sorted_list = sorted(num_list)
            await interaction.response.send_message(f"Sorted numbers: {sorted_list}")
        except ValueError:
            await interaction.response.send_message("Please provide a space-separated list of numbers.")

    @app_commands.command(name="reverse", description="Reverses a string")
    async def reverse(self, interaction: discord.Interaction, text: str):
        reversed_text = text[::-1]
        await interaction.response.send_message(f"Reversed string: {reversed_text}")

async def setup(bot):
    await bot.add_cog(Arrays(bot))