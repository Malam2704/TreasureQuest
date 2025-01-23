# main.py
import os
import json
import discord
from discord import app_commands
from discord.ext import commands

# If you’re storing your token as an environment variable:
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

# For demonstration, you can hardcode or store in .env:
# DISCORD_TOKEN = "your-bot-token-here"

intents = discord.Intents.default()
intents.message_content = True  # Might be needed for certain events

bot = commands.Bot(
    command_prefix="!",  # Unused if you rely solely on slash commands
    intents=intents
)

# In-memory player data (temporary). You can replace this with a file or DB later.
player_data = {}

@bot.event
async def on_ready():
    print(f"Bot is online as {bot.user}")
    try:
        synced = await bot.tree.sync()  # Sync slash commands globally
        print(f"Synced {len(synced)} commands.")
    except Exception as e:
        print(e)

# ----------------------------
# USER STORY #1: CREATE A NEW CHARACTER (/start)
# ----------------------------
# "As a player, I want to create a new character so that I can start playing the game."

@bot.tree.command(name="start", description="Begin your adventure by creating a new character.")
async def start_command(interaction: discord.Interaction):
    # Check if the user already has a character
    if interaction.user.id in player_data:
        await interaction.response.send_message(
            "You already have a character! Use /dashboard to view your stats.", 
            ephemeral=True
        )
        return

    # TODO: Ask player which class they want (Warrior, Mage, Thief, Healer).
    # For now, let's do a simple placeholder that auto-assigns "Warrior."

    # Create a basic character profile
    # (In a real flow, you'd prompt user via follow-up messages or a dropdown menu.)
    player_data[interaction.user.id] = {
        "name": interaction.user.name,
        "class": "Warrior",
        "level": 1,
        "exp": 0,
        "gold": 0,
        "health": 100,
        "mana": 30,
        "attack": 10,
        "defense": 5,
        "speed": 5
        # etc.
    }

    # Confirm creation
    await interaction.response.send_message(
        f"Character created! Welcome, **{interaction.user.name} the Warrior**.\n"
        "Use `/dashboard` to view your stats.",
        ephemeral=True
    )

# Example of a /dashboard command
@bot.tree.command(name="dashboard", description="View your character's stats.")
async def dashboard_command(interaction: discord.Interaction):
    if interaction.user.id not in player_data:
        await interaction.response.send_message(
            "You don't have a character yet! Use /start first.", ephemeral=True
        )
        return
    
    char = player_data[interaction.user.id]
    # Build a simple stats string
    stats_message = (
        f"**Name**: {char['name']}\n"
        f"**Class**: {char['class']}\n"
        f"**Level**: {char['level']}\n"
        f"**EXP**: {char['exp']}\n"
        f"**Gold**: {char['gold']}\n"
        f"**Health**: {char['health']}\n"
        f"**Mana**: {char['mana']}\n"
        f"**Attack**: {char['attack']}\n"
        f"**Defense**: {char['defense']}\n"
        f"**Speed**: {char['speed']}\n"
    )

    await interaction.response.send_message(stats_message, ephemeral=True)

# Run the bot
if __name__ == "__main__":
    bot.run(DISCORD_TOKEN)
