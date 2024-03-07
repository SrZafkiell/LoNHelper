from pymongo import MongoClient


class MongoManager:
    def __init__(self, mongo_uri):
        self.client = MongoClient(mongo_uri)

    def get_collection(self, database_name, collection_name):
        """
        Get a collection from the specified database.
        """
        db = self.client[database_name]
        return db[collection_name]

    def close_connection(self):
        """
        Close the Mongo connection.
        """
        self.client.close()

    def ping(self):
        """
        Ping the MongoDB server to check if it is up and running.
        """
        ping_status = self.client.admin.command('ping')
        if 'ok' in ping_status:
            status = True
        else:
            status = False
        return status
