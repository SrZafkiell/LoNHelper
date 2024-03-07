import discord
from discord import app_commands, channel, client
from discord.ext import commands

# Importing extra function dependencies
import requests
import html
import datetime
import traceback

# Importing bot utils
from core.Logger import Logger
from core.SqliteManager import SqliteManager
from core.ConfigManager import ConfigManager
from core.InitializationManager import InitializationManager

# Object that contains all the config data from the config.json file
config = ConfigManager()

# Creating instance of InitializationManager
init_manager = InitializationManager()
# Initializing Redis and Mongo connections
redis_bot_conn, redis_dict_conn, mongo_bot_client, mongo_dict_client = init_manager.setup_connections()
# Initializing Logger
logger = init_manager.setup_logger()


url = 'https://translate.googleapis.com/language/translate/v2'
detect_scope = '/detect'
google_apikey = config.google_api_key


class Translator(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="translator", description="Main command of the 'Translator' extension.")
    @app_commands.choices(
        action_type=[app_commands.Choice(name="Add translation channel", value="add"),
                     app_commands.Choice(name="Remove translation Channel", value="remove")]
    )
    @app_commands.checks.has_permissions(administrator=True)
    async def translation_channel(self, interaction: discord.Interaction, action_type: app_commands.Choice[str]):
        channel = self.bot.get_channel(interaction.channel_id)
        guild_id = interaction.guild_id
        if action_type == "add":
            manager = SqliteManager(f'{guild_id}.db')
            manager.execute('')
            pass
        if action_type == "remove":
            pass

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{config.bot_prefix} The 'Translator' extension is ready.")

    @commands.Cog.listener()
    async def on_message(self, message):
        if not message.author.bot and message.author != self.bot.user:
            await message.channel.send(f"Author  name: {message.author} Author id: {message.author.id} Guild id: {message.guild.id}")
            params_detect = {
                'key': google_apikey,
                'q': message.content
            }
            detect_response = requests.post(url + detect_scope, params=params_detect)
            source_lang = detect_response.json()['data']['detections'][0][0]['language']
            if source_lang != "en" and source_lang != "fr":
                target = 'en'
            elif source_lang == "en":
                target = 'fr'
            elif source_lang == "fr":
                target = 'en'
            params_translate = {
                'key': google_apikey,
                'q': message.content,
                'target': target
            }
            translation_response = requests.post(url, params=params_translate)
            result = translation_response.json()['data']['translations'][0]['translatedText']
            decoded_result = html.unescape(result)
            embed = discord.Embed(color=0xf09800)
            embed.set_author(name=f"{message.author}", icon_url=f"{message.author.avatar}", url=f"{message.jump_url}")
            embed.set_thumbnail(
                url="https://leagueofnetwork.com/apps/main/public/assets/img/uploads/6a1bfa2fa7d2b427abbc30a566b9c86d.png?cache=1678712685")
            embed.add_field(name="Raw message:", value=f"{message.content}", inline=False)
            embed.add_field(name="Translated message:", value=f"{decoded_result}", inline=False)
            embed.set_footer(text=f"League of Network - Translation helper")
            await message.channel.send(embed=embed, reference=message)


# Exporting the class
async def setup(bot):
    await bot.add_cog(Translator(bot))
