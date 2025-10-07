import discord
from discord import app_commands
from discord.ext import commands
import os

from discordtoken import DISCORD_TOKEN as TOKEN

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

warnings_log = {}

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"✅ Logged in as {bot.user}")

@bot.tree.command(name="warn", description="Warn a user with an optional reason")
@app_commands.describe(
    user="The user to warn",
    reason="The reason for the warning (optional)"
)
async def warn(interaction: discord.Interaction, user: discord.User, reason: str = None):
    if not interaction.guild:
        await interaction.response.send_message(
            "⚠ This command can only be used in a server.", ephemeral=True
        )
        return

    # Fetch the member issuing the command
    member = interaction.guild.get_member(interaction.user.id)
    if not member:
        await interaction.response.send_message(
            "⚠ Could not fetch your server member data.", ephemeral=True
        )
        return

    admin_role = discord.utils.get(member.roles, name="admin")

    if not admin_role:
        message = (
            f"{interaction.user.mention} has been warned.\n"
            f"**Reason:** {interaction.user.name} is a stinky doodoo head."
        )
        await interaction.response.send_message(message)
        return

    target_member = interaction.guild.get_member(user.id)
    if not target_member:
        await interaction.response.send_message(
            "⚠ Could not find that user in the server.", ephemeral=True
        )
        return

    if reason:
        message = f"{target_member.mention} has been warned.\n**Reason:** {reason}"
    else:
        message = f"{target_member.mention} has been warned."

    await interaction.response.send_message(message)

@bot.tree.command(name="doom", description="")
async def doom(interaction: discord.Interaction):
    await interaction.response.send_message("`I am BotVulture. I will be your doom.`")

bot.run(TOKEN)
