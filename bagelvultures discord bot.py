import discord
from discord import app_commands
from discord.ext import commands
import os

# --- SETUP ---
TOKEN = "YOUR_BOT_TOKEN_HERE"

intents = discord.Intents.default()
intents.members = True  # Recommended for mod-related commands
bot = commands.Bot(command_prefix="!", intents=intents)

# --- COMMAND TREE SETUP ---
@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"✅ Logged in as {bot.user}")

# --- /warn COMMAND ---
@bot.tree.command(name="warn", description="Warn a user with an optional reason.")
@app_commands.describe(
    user="The user to warn",
    reason="The reason for the warning (optional)"
)
async def warn(interaction: discord.Interaction, user: discord.User, reason: str = None):
    if reason:
        message = f"{user.mention} has been warned.\n**Reason:** {reason}"
    else:
        message = f"{user.mention} has been warned."

    await interaction.response.send_message(message)

# --- RUN BOT ---
bot.run(TOKEN)
