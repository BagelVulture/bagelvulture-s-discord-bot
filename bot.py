@bot.tree.command(name="warn", description="Warn a user with an optional reason")
@app_commands.describe(
    user="The user to warn",
    reason="The reason for the warning (optional)"
)
async def warn(interaction: discord.Interaction, user: discord.User, reason: str = None):
    if not interaction.guild:
        await interaction.response.send_message(
            "This command can only be used in a server.", ephemeral=True
        )
        return

    # Get Member object to access roles
    member = interaction.guild.get_member(interaction.user.id)
    if not member:
        await interaction.response.send_message(
            "Could not fetch your server member data.", ephemeral=True
        )
        return

    # Check admin role
    admin_role = discord.utils.get(member.roles, name="admin")  # check exact role name

    if not admin_role:
        # Non-admin warning
        message = (
            f"{interaction.user.mention} has been warned.\n"
            f"**Reason:** {interaction.user.name} is a stinky doodoo head."
        )
        await interaction.response.send_message(message)
        return

    # Admin warning
    target_member = interaction.guild.get_member(user.id)
    if not target_member:
        await interaction.response.send_message(
            "Could not find that user in the server.", ephemeral=True
        )
        return

    message = f"{target_member.mention} has been warned."
    if reason:
        message += f"\n**Reason:** {reason}"

    await interaction.response.send_message(message)
