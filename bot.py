import os
import discord
from dotenv import load_dotenv
from discord.ext import commands
import asyncio
DEBUG = True

# Set up intents
intents = discord.Intents.default()
intents.members = True
intents.message_content = True

# Initalize 'bot' veriable, but ignores command preftix.
# Nakigao uses discord.py's slash commands, so we don't need a command prefix.
bot = commands.Bot(command_prefix="!", intents=intents)

# Load cogs from the cogs directory
async def load_cogs():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await bot.load_extension(f"cogs.{filename[:-3]}")
            print(f"Loaded cog: {filename[:-3]}")

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}")
    try:
        if (DEBUG):
            guild = discord.Object(os.getenv("DEBUG_GUILD_ID"))
            await bot.tree.sync(guild=guild)
            print("Synced commands to debug guild")
        else:
            await bot.tree.sync()
            print("Synced commands to all guilds")
    except Exception as e:
        print(f"Failed to sync commands: {e}")

# This reads embeds as message edits, will revisit (maybe)
#@bot.event
#async def on_message_edit(before, after):
#    if before.author == bot.user:
#        return
#    await before.reply("Don't edit your messages, coward!")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if "alot" in message.content.lower():
        await message.reply("a lot*")

async def main():
    load_dotenv()
    await load_cogs()
    await bot.start(os.getenv("DISCORD_TOKEN"))

if __name__ == "__main__":
    asyncio.run(main())