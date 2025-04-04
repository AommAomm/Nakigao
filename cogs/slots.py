import random
import discord
import asyncio
from discord import app_commands
from discord.ext import commands

class Slots(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="slots", description="Test your luck!")
    async def slots(self, interaction: discord.Interaction):
        Symbols = ['🍒', '🍋', '🍊', '🍇', '🔔', '💎', '7️⃣']
        slotDisplay = []
        
        def populateSlot():
            nonlocal slotDisplay
            slotDisplay = []
            for i in range(9):
                slotDisplay.append(random.choice(Symbols))
            return

        def getDisplay():
            display = (f"{slotDisplay[0]}{slotDisplay[1]}{slotDisplay[2]}\n"
                      f"{slotDisplay[3]}{slotDisplay[4]}{slotDisplay[5]}\n"
                      f"{slotDisplay[6]}{slotDisplay[7]}{slotDisplay[8]}")
            return display

        def checkWin():
            if slotDisplay[0] == slotDisplay[1] == slotDisplay[2]:
                return "Top row win!"
            elif slotDisplay[3] == slotDisplay[4] == slotDisplay[5]:
                return "Middle row win!"
            elif slotDisplay[6] == slotDisplay[7] == slotDisplay[8]:
                return "Bottom row win!"
            else:
                return "No win this time."

        populateSlot()
        await interaction.response.send_message(getDisplay())
        for i in range(10):
            populateSlot()
            await interaction.edit_original_response(content=getDisplay())
            await asyncio.sleep(0.25)  # 0.25s delay between edits
        await interaction.followup.send(checkWin())

async def setup(bot):
    await bot.add_cog(Slots(bot))