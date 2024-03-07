# Importing required discord dependencies
import discord
from discord.ext import commands

# Importing extra functions dependencies
import os
import traceback
import asyncio
import platform

# Importing bot utils
from core.ConfigManager import ConfigManager
from core.SqliteManager import SqliteManager
from core.InitializationManager import InitializationManager


# Object that contains all the config data from the config.json file
config = ConfigManager()

# Creating instance of InitializationManager
init_manager = InitializationManager()
# Initializing Redis and Mongo connections
redis_bot_conn, redis_dict_conn, mongo_bot_client, mongo_dict_client = init_manager.setup_connections()
# Initializing Logger
logger = init_manager.setup_logger()


class Bot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True
        super().__init__(command_prefix=config.command_prefix, intents=intents,
                         description="https://github.com/SrZafkiell",
                         owner_id=config.owner_id, application_id=config.application_id, debug=True)

    async def setup_hook(self):
        synced = None
        if config.sync_commands and config.sync_commands_global:
            synced = await self.tree.sync()
        elif config.sync_commands and not config.sync_commands_global:
            if config.sync_commands_guild_id:
                synced = await self.tree.sync(guild=discord.Object(id=config.sync_commands_guild_id))
        if synced:
            print(f"{config.bot_prefix} Successfully synced {len(synced)} commands.")

    async def load_extensions(self):
        try:
            # This for statement will loop on all the cogs dir searching for all the .py files
            # If it finds a .py file, it gets added to the initialExtensions list.
            for filename in os.listdir("./cogs"):
                # Conditional searching for all the files that ends with .py
                if filename.endswith(".py"):
                    # Once it finds a .py file, it gets added to the inicialExtensions list without the .py
                    # termination "[:-3]" removes the last 3 chars -> ".py"
                    await self.load_extension(f"cogs.{filename[:-3]}")
            print(f"{config.bot_prefix} Successfully loaded {len(self.extensions.items())} extensions (cogs).")
        except Exception as e:
            print(f"{config.bot_prefix} Error {e} while trying to load the extensions.")
            error = f"{e}: {traceback.format_exc()}"
            logger.log(error)

    async def on_command_error(self, ctx, error):
        await ctx.reply(error, ephemeral=True)


# Discord bot object (Usually called as 'client')
bot = Bot()


async def initialize_guild(guild, redis_bot_connection, redis_dict_connection, mongo_bot_connection, mongo_dict_connection):
    # Note: We should get to this point, but in case it happens we will know.
    if not isinstance(guild, discord.Guild):
        logger.log(f"ERROR IN: initialize_guild({guild}, {redis_bot_connection}, {redis_dict_connection}, {mongo_bot_connection}, {mongo_dict_connection})")
        logger.print_and_log(f"Something went wrong while trying to initialize the guild databases. "
                             f"We didn't receive an instance of 'discord.Guild'. "
                             f"Instead we got: {type(guild)}, and inside of it is: {guild}")
        return
    else:
        # Getting and converting the guild id into a string to use it as a key
        guild_id = str(guild.id)
        redis_bot_connection.set(guild_id, "initialized")  # Save to redis
        mongo_bot_connection["guilds"].insert_one({"guild_id": guild_id})  # Save to mongo

        # Initialize the dict databases for saving messages
        redis_dict_connection.sadd(guild_id, "initialized")
        mongo_dict_connection["messages"][guild_id].insert_one({"test": "test"})


@bot.event
async def on_guild_join(guild):
    await initialize_guild(guild)


@bot.event
async def on_guild_remove(guild):
    pass


@bot.event
async def on_ready():
    await bot.change_presence(
        activity=discord.Streaming(name="Playing on League of Network", url="https://www.twitch.tv/srzafkiell"))
    print(f"{config.bot_prefix} {bot.user.name} Is up and running with the id {bot.user.id}")
    print(f"{config.bot_prefix} Running on {len(bot.guilds)} guilds: {[guild.name for guild in bot.guilds]}")
    for guild in bot.guilds:
        await initialize_guild(guild)


@bot.hybrid_command(name="credits", with_app_command=True, description="Bot credits")
async def bot_credits(interaction: discord.Interaction):
    await interaction.response.send_message(content=f"Developed by: SrZafkiell#0001 for the LeagueOfNetwork Project",
                                            ephemeral=True)


async def main():
    async with bot:
        await bot.load_extensions()
        await bot.start(config.bot_token)


try:
    if platform.system() == 'Windows':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())
except KeyboardInterrupt:
    print(f"{config.bot_prefix} INFO: El bot ha sido terminado KeyboardInterrupt")
    logger.log(traceback.print_exc())
    # print("STARTS KeyboardInterrupt stacktrace", traceback.print_exc(), "ENDS KeyboardInterrupt stacktrace")
except RuntimeError:
    print(f"{config.bot_prefix} INFO: El bot ha sido terminado RuntimeError")
    logger.log(traceback.print_exc())
    # print("STARTS KeyboardInterrupt stacktrace", traceback.print_exc(), "ENDS KeyboardInterrupt stacktrace")
except asyncio.TimeoutError:
    print(f"{config.bot_prefix} INFO: El bot ha sido terminado asyncio RuntimeError")
    logger.log(traceback.print_exc())
    # print("STARTS asyncio.TimeoutError stacktrace", traceback.print_exc(), "ENDS asyncio.TimeoutError stacktrace")
