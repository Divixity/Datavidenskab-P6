import pandas
import os

import pandas as pd

if __name__ == "__main__":

    var = pd.read_csv("C:/Users/magnu/OneDrive - Aalborg Universitet/P6/Data/raw_data/All-Subsystems-hour-Year2.csv")

    var["Timestamp"] = pd.to_datetime(var["Timestamp"])

    for row in var.index:
        dt = var["Timestamp"][row]
        var.at[row, "Timestamp"] = pd.Timestamp(year=dt.year, month=dt.month, day=dt.day,
                                                   hour=dt.hour, minute=dt.minute, second=dt.second)

    var["Timestamp"] = pd.to_datetime(var["Timestamp"])

    var = var.set_index(var['Timestamp']).asfreq('h')


    var.to_pickle("C:/Users/magnu/OneDrive - Aalborg Universitet/P6/Data/All-Subsystems-hour-Year2.pkl")



    # path = "C:/Users/magnu/OneDrive - Aalborg Universitet/P6/Data/raw_data/"
    # files = os.listdir(path)
    # for file in files:
    #     data = pd.read_csv(path+file)
    #     print(data.columns)
