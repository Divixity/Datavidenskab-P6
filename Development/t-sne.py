# import plotly.express as px
# from sklearn.manifold import TSNE
#
# import DataRetriever as dr
#
# retriever = dr.DataRetriever()
# hour = retriever.get_data("All-Subsystems-hour-Year2.pkl")
#
# X = hour.iloc[:, 1:]
# X.fillna(0, inplace=True)
#
# n_components = 3
# tsne = TSNE(n_components)
# tsne_result = tsne.fit_transform(X)
#
# fig = px.scatter_3d(x=tsne_result[:, 0], y=tsne_result[:, 1], z=tsne_result[:, 2], opacity=0.25)
# fig.show()


#%% md
# TODO: Erstat værdier 1 i 'væk' med -1, værdier 1 i 'nedenunder' med 2, og værdier 1 i 'ovenpå' med 3
#%%
import plotly.express as px

import DataRetriever as dr

retriever = dr.DataRetriever()

year_2 = retriever.get_data('All-Subsystems-minute-Year2.pkl')
metadata = retriever.get_data('metadata-year2.pkl')
metadata.rename(columns={'Unnamed: 0': 'Attribute'}, inplace=True)
#%%
parent_a_positions = metadata[metadata["Description"].str.contains('parent A is simulated as being')]
parent_b_positions = metadata[metadata["Description"].str.contains('parent B is simulated as being')]
child_a_positions = metadata[metadata["Description"].str.contains('child A is simulated as being')]
child_b_positions = metadata[metadata["Description"].str.contains('child B is simulated as being')]

positions_dict = {'ParentA': parent_a_positions['Attribute'].tolist(),
                  'ParentB': parent_b_positions['Attribute'].tolist(),
                  'ChildA': child_a_positions['Attribute'].tolist(),
                  'ChildB': child_b_positions['Attribute'].tolist()}
#%%
positions = list()
for key, value in positions_dict.items():
    for subvalue in positions_dict[key]:
        positions.append(subvalue)
#%%
position_data = year_2[positions]
position_data.index = position_data.index.floor('min')
position_data["Date"] = position_data.index.date
position_data["Time"] = position_data.index.time
position_data["Weekend"] = position_data.index.weekday > 5
#%%
position_data.rename(columns={'Load_StatusSensHeatPrntAUP': 'ParentAUp',
                              'Load_StatusSensHeatPrntADOWN': 'ParentADown',
                              'Load_StatusSensHeatPrntBUP': 'ParentBUp',
                              'Load_StatusSensHeatPrntBDOWN': 'ParentBDown',
                              'Load_StatusSensHeatChildAUP': 'ChildAUp',
                              'Load_StatusSensHeatChildADOWN': 'ChildADown',
                              'Load_StatusSensHeatChildBUP': 'ChildBUp',
                              'Load_StatusSensHeatChildBDOWN': 'ChildBDown'}, inplace=True)
#%%
position_data["ParentAUp"].replace(to_replace=1.0, value=2.0, inplace=True)
position_data["ParentBUp"].replace(to_replace=1.0, value=2.0, inplace=True)
position_data["ChildAUp"].replace(to_replace=1.0, value=2.0, inplace=True)
position_data["ChildBUp"].replace(to_replace=1.0, value=2.0, inplace=True)

position_data["ParentAPosition"] = position_data["ParentAUp"] + position_data["ParentADown"]
position_data["ParentBPosition"] = position_data["ParentBUp"] + position_data["ParentBDown"]
position_data["ChildAPosition"] = position_data["ChildAUp"] + position_data["ChildADown"]
position_data["ChildBPosition"] = position_data["ChildBUp"] + position_data["ChildBDown"]

# position_data.sort_values(by="ParentAPosition", ascending=True, inplace=True)

position_data.replace({'ParentBPosition': {0: 'Not Home', 1: 'Downstairs', 2: 'Upstairs'}}, inplace=True)

#%%
# SLET
fig = px.line(position_data[position_data["Weekend"] == False], x="Time", y="ParentBPosition", color="Date", color_discrete_sequence=['rgba(98, 111, 250, 0.01)'])
fig.update_yaxes(type="category", categoryarray=['Not Home', 'Downstairs', 'Upstairs'])

fig.show()
