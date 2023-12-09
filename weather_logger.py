"""
This module contains the WeatherLogger class,
which returns a formatted logger for logging data in this application.
"""

import logging

class WeatherLogger:
    """ Represents a formatted logging object. """
    def __init__(self):
        """ Initializes an instance of the WeatherLogger class. """
        self.logger = logging.getLogger('log')
        self.logger.setLevel(logging.DEBUG)

        # File handler for low-level logs
        file_handler = logging.FileHandler('weather_processor.log')
        file_handler.setLevel(logging.DEBUG)

        # Console handler is given higher log level
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.ERROR)

        # Adding formatting
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        console_handler.setFormatter(formatter)
        file_handler.setFormatter(formatter)

        # add the handlers to logger
        self.logger.addHandler(console_handler)
        self.logger.addHandler(file_handler)

    def get_logger(self):
        """ Returns the formatted logger. """
        return self.logger