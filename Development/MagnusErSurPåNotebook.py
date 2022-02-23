import DataRetriever as dr
import pandas as pd
import plotly.express as px

if __name__ == "__main__":

    # Load data and metadata
    retriever = dr.DataRetriever()
    year_2 = retriever.get_data("All-Subsystems-minute-Year2.pkl")
    metadata = retriever.get_data("metadata-year2.pkl")
    metadata.rename(columns={"Unnamed: 0": "Attribute"}, inplace=True)

    watt_attributes = metadata[metadata["Units"] == "W"]

    # Define generating attributes as attributes in W that have description "Instantaneous power produced"
    powerproduced_attributes = [description.startswith("Instantaneous power produced") for description in watt_attributes["Description"]]
    gen_attributes = watt_attributes[powerproduced_attributes]
    gen_attributes = gen_attributes["Attribute"].tolist()

    # Define consuming attributes as attribute not having description 'Instantaneous power produced" and are in W.
    not_powerproduced = [not attribute for attribute in powerproduced_attributes]
    con_attributes = watt_attributes[not_powerproduced]
    con_attributes = year_2[con_attributes["Attribute"].tolist()]

    # Need to further sort in the consuming attributes as some are duplicates and measure the same thing
    correlations_df = con_attributes.corr().abs()

    correlation_pairs = dict()
    for rowIndex, row in correlations_df.iterrows(): #RowIndex is the row name, row is a pd.Series of (column name : entry value)
        for columnIndex, value in row.items(): #columnIndex is column name, value is the entry value
            if value > 0.95: #If correlation is larger than threshold and row name and column name is not the same
                if rowIndex != columnIndex:
                    correlation_pairs.setdefault(rowIndex, []) #Insert row name as key if it does not already exist. Make the value pairs an empty list.
                    correlation_pairs[rowIndex].append(columnIndex) #Append the column name as value to the key.

    # for i in correlation_pairs:
    #     print(i, correlation_pairs[i])

    #Hvis
    correlation_pairs_cleaned = correlation_pairs.copy()
    for value in correlation_pairs_cleaned.values():
        for key in correlation_pairs_cleaned.keys():
            if value == key:
                correlation_pairs_cleaned.pop(key)

    # print('Ny dict starter her')
    # for i in correlation_pairs_cleaned:
    #     print(i, correlation_pairs_cleaned[i])

    columnstodrop = list(correlation_pairs_cleaned.values())
    for column in con_attributes.columns:
        if [column] in columnstodrop:
            con_attributes = con_attributes.drop([column], axis = 1)

