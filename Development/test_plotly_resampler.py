import DataRetriever as dr
import pandas as pd
import plotly.graph_objects as go
from plotly_resampler import FigureResampler

retriever = dr.DataRetriever()

year_2 = retriever.get_data("All-Subsystems-minute-Year2.pkl")

# Add timestamp converted to UTC as index to year_2
year_2["Timestamp UTC"] = pd.to_datetime(year_2["Timestamp"], utc=True, infer_datetime_format=True)
year_2.set_index("Timestamp UTC", inplace=True)

start_end_list = ["2015-02-01", "2015-03-01"]
year_2 = year_2[year_2[start_end_list]]

# Load the metadata
metadata = retriever.get_data("metadata-year2.pkl")
metadata.rename(columns={"Unnamed: 0": "Attribute"}, inplace=True)

watt_attributes = metadata[metadata["Units"] == "W"]

pv_attributes = [description.startswith("Instantaneous power produced") for description in watt_attributes["Description"]]
gen_attributes = watt_attributes[pv_attributes]
gen_attributes = gen_attributes["Attribute"].tolist()

loads_attributes = [subsystem == "Loads" for subsystem in watt_attributes["Subsystem"]]
con_attributes = watt_attributes[loads_attributes]
con_attributes = con_attributes["Attribute"].tolist()

energy_attributes = ["Timestamp"] + gen_attributes + con_attributes
energy_data = year_2[energy_attributes]

total_generated = energy_data[gen_attributes].sum().sum()
total_consumed = energy_data[con_attributes].sum().sum()

energy_data["Sum Generating"] = energy_data[gen_attributes].sum(axis=1)
energy_data["Sum Consuming"] = energy_data[con_attributes].sum(axis=1)

fig = FigureResampler(go.Figure())
fig.add_trace(go.Bar(name="Name", showlegend=True), hf_x=energy_data["Timestamp"], hf_y=energy_data["Sum Consuming"])
fig.show_dash(mode='inline')
