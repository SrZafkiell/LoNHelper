import datetime
from core.ConfigManager import ConfigManager

config = ConfigManager()


class Logger:
    def __init__(self, log_file_path):
        self.log_file_path = log_file_path

    def log(self, message):
        # log_time > This variable will log the exact date and time in which the {message} got logged
        log_time = datetime.datetime.today().strftime('%d/%m/%Y-%H:%M:%S> ')
        log_message = f"{log_time}{message}"

        # Opening the log file as append to write
        with open(self.log_file_path, 'a') as log_file:
            log_file.write(log_message + '\n')

    def print_and_log(self, message):
        print(config.bot_prefix, message)
        self.log(message)
