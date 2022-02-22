import configparser
import os
import pandas as pd

import main


class DataRetriever:
    """
    Class to locate, and retrive data, as .pkl, stored in a pd.DataFrame.
    """
    def __init__(self):
        self.__config_path = os.path.join(main.root, 'Config', 'database_path.ini')
        self.__data_path = self.__config_load()

    def __config_load(self):
        """
        Private method to read config file for path to OneDrive.
        :return: Path.
        """
        config = configparser.ConfigParser()

        config.read(self.__config_path)

        return config['database']['directory']

    def get_data(self, file_name):
        """
        Method for reading a pickle file, given a file name, and returning it as a pd.DataFrame.
        :param file_name: File which to open as a pd.DataFrame
        :return: pd.DataFrame of the pickle file.
        """
        path = os.path.join(self.__data_path, file_name)

        df = pd.read_pickle(path)

        df.index = df["Timestamp"]

        return df


if __name__ == "__main__":
    open_data = DataRetriever()

    df = open_data.get_data("All-Subsystems-hour-Year1.pkl")

    print(df.head(10))
