import traceback
from datetime import datetime
import time

import discord
import pytz
from discord.ext import commands
from discord import app_commands

from core.ConfigManager import ConfigManager
# Object that contains all the config data from the config.json file
config = ConfigManager()


class Announce(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{config.bot_prefix} The 'Announce' extension is ready.")

    @app_commands.command(name="announce", description="Announce something with the bot.")
    @app_commands.choices(
        announce_type=[app_commands.Choice(name="Simple text (Simple text message sent from the bot)", value="text"),
                       app_commands.Choice(name="Embed (Formats the message into an embed)", value="embed")])
    @app_commands.choices(embed_color=[app_commands.Choice(name="Yellow", value="0xf09800"),
                                       app_commands.Choice(name="Aqua", value="0x00f098"),
                                       app_commands.Choice(name="Light-Blue", value="0x00d0f0"),
                                       app_commands.Choice(name="Red", value="0xf02000")])
    @app_commands.checks.has_permissions(administrator=True)
    async def announce(self, interaction: discord.Interaction, announce_type: app_commands.Choice[str],
                       message: str = None, tags: str = None, embed_title: str = None, embed_url: str = None,
                       embed_desc: str = None, embed_color: app_commands.Choice[str] = None, embed_image_url: str = None,
                       field_title_1: str = None, field_content_1: str = None, field_alignment_1: bool = False,
                       field_title_2: str = None, field_content_2: str = None, field_alignment_2: bool = False,
                       field_title_3: str = None, field_content_3: str = None, field_alignment_3: bool = False,
                       field_title_4: str = None, field_content_4: str = None, field_alignment_4: bool = False,
                       field_title_5: str = None, field_content_5: str = None, field_alignment_5: bool = False):
        try:
            start_of_execution = time.time()
            channel = self.bot.get_channel(interaction.channel_id)
            common_role = ""
            for rank in config.announce_ext_announcer_ranks:
                for i in range(len(interaction.user.roles)):
                    if interaction.user.roles[i].name.lower() == rank.lower():
                        common_role = rank
                        break
            if not common_role:
                common_role = "Staff"
            if announce_type.value == "text":
                raw_to_tag = tags.split(" ")
                to_tag = " ".join(raw_to_tag)
                response = message.replace("\\n", "\n")
                await channel.send(response)
                await interaction.response.send_message(content="Anuncio enviado con éxito", ephemeral=True)
            elif announce_type.value == "embed":
                if embed_title or embed_url or embed_desc or embed_color:
                    if not embed_color:
                        in_use_color = "0xf09800"
                    else:
                        in_use_color = embed_color.value
                    embed = discord.Embed(title=embed_title, url=embed_url, description=embed_desc, color=int(in_use_color, 16))
                    embed.set_author(name=f"[{common_role.upper()}] {str(interaction.user)[:-5]}", url=interaction.user.avatar, icon_url=interaction.user.avatar)
                    embed.set_thumbnail(url="https://leagueofnetwork.com/apps/main/public/assets/img/uploads/6a1bfa2fa7d2b427abbc30a566b9c86d.png?cache=1678712685")
                    for i in range(1, 6):
                        field_title = locals()[f'field_title_{i}']
                        field_content = locals()[f'field_content_{i}']
                        field_alignment = locals()[f'field_alignment_{i}']
                        if field_title and field_content:
                            embed.add_field(name=field_title, value=field_content, inline=bool(field_alignment))
                    if embed_image_url:
                        embed.set_image(url=f"{embed_image_url}")
                    embed.set_footer(text=f"\n» {datetime.now(pytz.timezone('America/Bogota')).strftime('%B %d %Y - %H:%M:%S')} (GMT-5) « \nLeague of Network × Announcer")
                    await channel.send(embed=embed)
                    if tags:
                        await channel.send(f"||Tags: {tags}||")
                    await interaction.response.send_message(content=f":white_check_mark: Announcement sent.", ephemeral=True)
                else:
                    await interaction.response.send_message(content=f"No embed title, url, desc or color were given", ephemeral=True)
            end_of_execution = time.time()
            print(f"{config.bot_prefix} Announce generated, the execution took: {end_of_execution-start_of_execution}ms")
        except Exception as e:
            await interaction.response.send_message(f"Something went wrong with the announcer, please check the console log", ephemeral=True)
            print(f"Error: {print(e)}")
            traceback.print_exc()


# Exporting the class
async def setup(bot):
    await bot.add_cog(Announce(bot))
