import discord
from discord import app_commands
from discord.ext import commands
import os

from bvconfig import DISCORD_TOKEN as TOKEN
from bvconfig import CAN_WARN_ROLE_NAME as can_warn
from bvconfig import ON_JOIN_GIVEN_ROLE_NAME as default_role
from bvconfig import WELCOME_CHANNEL as announcements_channel

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

warnings_log = {}

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"Logged in as {bot.user}")

@bot.tree.command(name="warn", description="Give a user a warning")
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

    member = interaction.guild.get_member(interaction.user.id)
    if not member:
        await interaction.response.send_message(
            "⚠ Could not fetch your server member data.", ephemeral=True
        )
        return

    admin_role = discord.utils.get(member.roles, name=can_warn)

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

@bot.tree.command(name="doom", description="doom")
async def doom(interaction: discord.Interaction):
    await interaction.response.send_message("`I am BotVulture. I will be your doom.`")

@bot.event
async def on_member_join(member: discord.Member):
    stupid_role = discord.utils.get(member.guild.roles, name=default_role)
    if not stupid_role:
        print("⚠  " + default_role + " role not found in the server.")
        return

    await member.add_roles(stupid_role)
    print(f"Made {member.name} default_role")

    announcements_channel = discord.utils.get(member.guild.text_channels, name=announcements_channel)
    if announcements_channel:
        await announcements_channel.send(f"{member.mention} has arrived in the server!")
    else:
        print("⚠ " + default_role + " channel not found.")

bot.run(TOKEN)


