import json


with open('dummy_config.json', encoding="utf-8") as config_file:
    config = json.load(config_file)
    config_file.close()


class ConfigManager:
    def __init__(self):
        # Initializing the config as the config.json file.
        self.config = config
        """
        BOT Credentials
        """
        self.bot_token = config['bot-credentials']['bot-token']
        self.owner_id = config['bot-credentials']['bot-owner-id']
        self.application_id = config['bot-credentials']['bot-application-id']
        self.bot_prefix = config['bot-credentials']['bot-prefix']
        self.command_prefix = config['bot-credentials']['bot-command-prefix']
        """
        API Credentials
        """
        self.google_api_key = config['api-credentials']['google-api-key']
        self.twitch_api_key = config['api-credentials']['twitch-api-key']
        # Bot extensions settings and messages
        self.greetings_ext_welcome_message = config['extensions']['greetings-extension']['welcome-message']
        self.greetings_ext_goodbye_message = config['extensions']['greetings-extension']['goodbye-message']
        self.announce_ext_announcer_ranks = config['extensions']['announce-extension']['announcer-ranks']
        """
        Developer settings section
        """
        self.sync_commands = config['developer-settings']['command-syncing']['sync-commands']
        self.sync_commands_global = config['developer-settings']['command-syncing']['sync-commands-global']
        self.sync_commands_guild_id = config['developer-settings']['command-syncing']['sync-commands-dev-guild-id']
        self.debug_mode = config['developer-settings']['debug-mode']
        self.error_logging_mode = config['developer-settings']['error-logging-mode']
        # Redis Settings
        self.redis_host = config['developer-settings']['database-settings']['redis-settings']['redis-host']
        self.redis_port = config['developer-settings']['database-settings']['redis-settings']['redis-port']
        self.max_connections = config['developer-settings']['database-settings']['redis-settings']['redis-max-connections']
        self.redis_bot_index = config['developer-settings']['database-settings']['redis-settings']['redis-bot-index']
        self.redis_dict_index = config['developer-settings']['database-settings']['redis-settings']['redis-dict-index']
        # self.  = config['developer-settings']['database-settings']['redis-settings']['']
        # Mongo Settings
        self.mongo_host = config['developer-settings']['database-settings']['mongo-settings']['mongo-host']
        self.mongo_port = config['developer-settings']['database-settings']['mongo-settings']['mongo-port']
        self.mongo_user = config['developer-settings']['database-settings']['mongo-settings']['mongo-user']
        self.mongo_password = config['developer-settings']['database-settings']['mongo-settings']['mongo-password']
        self.mongo_bot_db = config['developer-settings']['database-settings']['mongo-settings']['mongo-bot-database']
        self.mongo_bot_auth_source = config['developer-settings']['database-settings']['mongo-settings']['mongo-bot-auth-source']
        self.mongo_dict_db = config['developer-settings']['database-settings']['mongo-settings']['mongo-dict-database']
        self.mongo_dict_auth_source = config['developer-settings']['database-settings']['mongo-settings']['mongo-dict-auth-source']
        # self. = config['developer-settings']['database-settings']['mongo-settings']['']

