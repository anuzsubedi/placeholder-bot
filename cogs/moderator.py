import discord
from discord.ext import commands
from discord import app_commands
import yaml

# Load the configuration from the YAML file
with open("config.yaml", "r") as file:
    config = yaml.safe_load(file)


class Moderator(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def check_mod(self, ctx):
        try:
            mod_roles = config["configuration"]["mod-roles"]
            for role in ctx.user.roles:
                if role.name in mod_roles:  # Use role.name to compare the role's name
                    return True
            return False

        except Exception as e:
            print(f"\n++++++++++++\n")
            print(e)

    @commands.Cog.listener()
    async def on_ready(self):
        print("Moderator Cog is ready")

    @app_commands.command(
        name="checkmod", description="A command to check moderator permissions."
    )
    async def checkmod(self, ctx: discord.Interaction):
        try:
            mod_roles = config["configuration"]["mod-roles"]
            if ctx.user.guild_permissions.administrator:
                await ctx.response.send_message(
                    "You are eligible to use moderator commands.\nYou are an administrator.",
                    ephemeral=True,
                )
            elif self.check_mod(ctx):
                await ctx.response.send_message(
                    "You are eligible to use moderator commands.\nYou are a moderator.",
                    ephemeral=True,
                )
            else:
                await ctx.response.send_message(
                    "You are not allowed to use moderator commands.", ephemeral=True
                )
        except Exception as e:
            print(f"\n++++++++++++\n")
            print(e)

    @app_commands.command(
        name="announce", description="Send an announcement to the announcement channel."
    )
    async def announce(self, ctx: discord.Interaction, message: str):
        try:
            message = message.replace("\\n", "\n")
            if ctx.user.guild_permissions.administrator or self.check_mod(ctx):
                announcement_channel = self.bot.get_channel(
                    config["configuration"]["announcement-channel"]
                )
                await announcement_channel.send(message)
                await ctx.response.send_message(
                    f"Announcement sent to {announcement_channel.mention}.",
                    ephemeral=True,
                )
            else:
                await ctx.response.send_message(
                    "You are not allowed to use this command.", ephemeral=True
                )
        except Exception as e:
            print(f"\n++++++++++++\n")
            print(e)

    @app_commands.command(
        name="embedannounce", description="Send an announcement as an embed."
    )
    async def embedannounce(
        self, ctx: discord.Interaction, title: str, description: str
    ):
        try:
            if ctx.user.guild_permissions.administrator or self.check_mod(ctx):
                announcement_channel = self.bot.get_channel(
                    config["configuration"]["announcement-channel"]
                )
                embed = discord.Embed(
                    title=title,
                    description=description.replace("\\n", "\n"),
                    color=discord.Color.green(),
                )
                await announcement_channel.send(embed=embed)
                await ctx.response.send_message(
                    f"Announcement sent to {announcement_channel.mention}.",
                    ephemeral=True,
                )
            else:
                await ctx.response.send_message(
                    "You are not allowed to use this command.", ephemeral=True
                )
        except Exception as e:
            print(f"\n++++++++++++\n")
            print(e)


# Add the cog to the bot
async def setup(bot):
    await bot.add_cog(Moderator(bot))
