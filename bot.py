import discord
from discord import app_commands
from discord.ext import commands
import os

# --- SETUP ---
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# --- COMMAND TREE SETUP ---
@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"✅ Logged in as {bot.user}")

# --- /warn COMMAND ---
@bot.tree.command(name="warn", description="Warn a user with an optional reason (Admin only).")
@app_commands.describe(
    user="The user to warn",
    reason="The reason for the warning (optional)"
)
async def warn(interaction: discord.Interaction, user: discord.User, reason: str = None):
    # --- Check for Admin Role ---
    if not isinstance(interaction.user, discord.Member):
        await interaction.response.send_message("This command can only be used in a server.")
        return
    
    admin_role = discord.utils.get(interaction.user.roles, name="admin")

    if not admin_role:
        # Warn the person who *tried* to use the command
        target = interaction.user
        message = f"{target.mention} has been warned.\n**Reason:** {target.name} is a stinky doodoo head."
        await interaction.response.send_message(message)
        return

    # --- Normal warning behavior for admins ---
    if reason:
        message = f"{user.mention} has been warned.\n**Reason:** {reason}"
    else:
        message = f"{user.mention} has been warned."

    await interaction.response.send_message(message)

# --- RUN BOT ---
bot.run(TOKEN)

