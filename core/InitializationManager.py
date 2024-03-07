import datetime
import traceback

from core.Logger import Logger
from core.ConfigManager import ConfigManager
from core.RedisManager import RedisManager
from core.MongoManager import MongoManager

config = ConfigManager()
current_date = datetime.datetime.today().strftime('%Y-%m-%d')

# Object for the Logger class
logger = Logger(f'./logs/{current_date}')


class InitializationManager:

    def __init__(self):
        self.redis_bot_conn = None
        self.redis_dict_conn = None
        self.mongo_bot_client = None
        self.mongo_dict_client = None
        self.logger = None

    def setup_connections(self):
        redis_successfully_connected = False
        mongo_successfully_connected = False

        # Redis connections
        try:
            redis_bot_manager = RedisManager(num_connections=config.max_connections, host=config.redis_host, port=config.redis_port, db=config.redis_bot_index)
            redis_dict_manager = RedisManager(num_connections=config.max_connections, host=config.redis_host, port=config.redis_port, db=config.redis_dict_index)
            self.redis_bot_conn = redis_bot_manager.get_connection()
            self.redis_dict_conn = redis_dict_manager.get_connection()
        except Exception as e:
            print(f"{config.bot_prefix} Error {e} while trying to establish connections to Redis.")
            error = f"{e}: {traceback.format_exc()}"
            logger.log(error)
            # IMPORTANT: A FALLBACK USE OF SQLITE NEEDS TO BE IMPLEMENTED

        # MongoDB connections
        try:
            # URI Scheme: mongodb://username:password@localhost:27017/database
            mongo_bot_uri = f"mongodb://{config.mongo_user}:{config.mongo_password}@{config.mongo_host}:{config.mongo_port}/{config.mongo_bot_db}?authSource={config.mongo_bot_auth_source}"
            mongo_dict_uri = f"mongodb://{config.mongo_user}:{config.mongo_password}@{config.mongo_host}:{config.mongo_port}/{config.mongo_dict_db}?authSource={config.mongo_dict_auth_source}"
            self.mongo_bot_client = MongoManager(mongo_bot_uri)
            self.mongo_dict_client = MongoManager(mongo_dict_uri)
        except Exception as e:
            print(f"{config.bot_prefix} Error {e} while trying to establish connections to Mongo.")
            error = f"{e}: {traceback.format_exc()}"
            logger.log(error)
            # ADDING TO THE IMPORTANT TAG: MONGO IS ONLY USED AS PERSISTENCE AND BACKUP FOR REDIS,
            # IT DOESN'T NEED A FALLBACK WITH SQLITE

        # Verify connections
        # Redis
        try:
            redis_bot_connection = self.redis_bot_conn.ping()
            redis_dict_connection = self.redis_dict_conn.ping()
            if redis_bot_connection and redis_dict_connection:
                redis_successfully_connected = True
        except Exception as e:
            print(f"{config.bot_prefix} Error {e} while trying to verify connection to Redis.")
            error = f"{e}: {traceback.format_exc()}"
            logger.log(error)
        # Mongo
        try:
            mongo_bot_connection = self.mongo_bot_client.ping()
            mongo_dict_connection = self.mongo_dict_client.ping()
            if mongo_bot_connection and mongo_dict_connection:
                mongo_successfully_connected = True
        except Exception as e:
            print(f"{config.bot_prefix} Error {e} while trying to verify connection to Mongo.")
            error = f"{e}: {traceback.format_exc()}"
            logger.log(error)

        # If the connections for Redis and Mongo were successful
        if redis_successfully_connected and mongo_successfully_connected:
            # Return a tuple with the connections
            return self.redis_bot_conn, self.redis_dict_conn, self.mongo_bot_client, self.mongo_dict_client
        else:
            # IMPLEMENT FALLBACK USE WITH SQLITE HERE
            pass

    def setup_logger(self):
        # Object for the Logger class
        self.logger = Logger(f'./logs/{current_date}.txt')
        return self.logger


