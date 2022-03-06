import DataRetriever as dr
import pandas as pd
import plotly.express as px

if __name__ == "__main__":

    retriever = dr.DataRetriever()

    year_2 = retriever.get_data("All-Subsystems-minute-Year2.pkl")

    # Add timestamp converted to UTC as index to year_2
    # year_2["Timestamp UTC"] = pd.to_datetime(year_2["Timestamp"], utc=True, infer_datetime_format=True)
    # year_2.set_index("Timestamp UTC", inplace=True)

    # Load the metadata
    metadata = retriever.get_data("metadata-year2.pkl")
    metadata.rename(columns={"Unnamed: 0": "Attribute"}, inplace=True)

    year_2[["PV_Watts3PhTotalW3PhT1", "PV_Watts3PhTotalW3PhT2", "PV_PVSystem1ACPowerOSPACPV1OS", "PV_PVSystem2ACPowerOSPACPV2OS",
            "Elec_PowerPV1of2", "Elec_PowerPV2of2"]].clip(lower=0) #Minimum value of these columns must be 0, else set to 0.

    watt_attributes = metadata[metadata["Units"] == "W"]

    #Kitchen
    kitchen_attributes = watt_attributes[watt_attributes['Measurement_Location'] == 'Kitchen']
    kitchen_attributes = year_2[kitchen_attributes["Attribute"].tolist()]
    kitchen_attributes = list(kitchen_attributes.columns) + ["Timestamp"]
    kitchen_data = year_2[kitchen_attributes]

    fig = px.histogram(data_frame=kitchen_data[0:20000],
                 x="Timestamp",
                 y=["Elec_PowerRefrigerator", "Elec_PowerHeatLoadforRefrigerator", "Load_RefrigeratorPowerWithStandby"],
                       barmode='group')
    fig.show()

    fig2 = px.histogram(data_frame=kitchen_data[0:20000],
                        x = "Timestamp",
                        y = ["Elec_PowerPlugsInstKitD", "Elec_PowerPlugsInstKitA", "Load_KPlugLoadsPowerUsage"],
                        barmode="group")
    fig2.show()
