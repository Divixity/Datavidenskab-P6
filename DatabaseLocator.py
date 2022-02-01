import configparser
import os

import main


class DatabaseLocator:
    def __init__(self):
        """
        This constructor method creates container attributes for directory paths.
        config_path is hard coded.
        database_path is loaded from the Config file.
        """
        self.__config_path = os.path.join(main.root, 'Config', 'database_path.ini')
        self.__database_path = self.__config_load()
        self.__model_path = os.path.join(main.root, 'Project', 'Models')

    def __config_load(self):
        """
        Loads database path.
        """
        config = configparser.ConfigParser()

        config.read(self.__config_path)

        return config['database']['directory']

    def get_path(self, sub_folder=None, model_path=False):
        """
        Returns the directory path to the database.
        """
        if model_path:
            path = self.__model_path

        else:
            path = self.__database_path

        if sub_folder is None:
            return path

        else:
            return os.path.join(path, sub_folder)


if __name__ == '__main__':
    test = DatabaseLocator()
    for file in os.listdir(os.path.join(test.get_path(), 'bom')):
        print(file)
