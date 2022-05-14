import configparser
import os
import pandas as pd
import pickle

import main


class DataRetriever:
    """
    Class to locate, and retrieve data, as .pkl, stored in a pd.DataFrame.
    """

    def __init__(self):
        self.__config_path = os.path.join(main.root, 'Config', 'database_path.ini')
        self.__data_path = self.config_load()

    def config_load(self):
        """
        Private method to read config file for path to OneDrive.
        :return: Path.
        """
        config = configparser.ConfigParser()

        config.read(self.__config_path)

        return config['database']['directory']

    def get_data(self, file_name: str) -> pd.DataFrame:
        """
        Method for reading a Pandas pickle file, given a file name, and returning it as a pd.DataFrame.
        :param file_name: File which to open as a pd.DataFrame
        :return: pd.DataFrame of the pickle file.
        """
        path = os.path.join(self.__data_path, file_name)

        dataframe = pd.read_pickle(path)

        return dataframe

    def get_attributes(self, file_name: str):
        """
        Method for reading a normal pickle file, given a file name
        :param file_name: File which to read
        :return: Depends on the original type of Python datastructure
        """

        path = os.path.join(self.__data_path, file_name)

        file_handler = open(path, 'rb')
        file = pickle.load(file_handler)

        return file


if __name__ == "__main__":
    open_data = DataRetriever()

    df = open_data.get_data("All-Subsystems-hour-Year1.pkl")

    print(df.head(10))
