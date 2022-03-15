#%%
import plotly.express as px
from sklearn.manifold import TSNE
import pandas as pd
import numpy as np

import DataRetriever as dr

retriever = dr.DataRetriever()
hour = retriever.get_data("All-Subsystems-hour-Year2.pkl")

producing = retriever.get_attributes("producing_attributes.pkl")
consuming = retriever.get_attributes("consuming_attributes.pkl")
#%%
"""
LABELS:
    - Consuming as bool
    - Day of Week
    - hour of Day
"""
#%%
X = hour[consuming].copy()
X.fillna(0, inplace=True)

n_components = 3
tsne = TSNE(n_components, random_state=0)
tsne_result = tsne.fit_transform(X)
tsne_result = pd.DataFrame(tsne_result)
tsne_result
#%%
tsne_result["DoW"] = (hour["Timestamp"].dt.day_name()).reset_index(drop=True)
#%%
tsne_result["hour"] = (hour["Timestamp"].dt.hour).reset_index(drop=True)
#%%
tsne_result["Generating"] = (hour[producing[0]].astype(bool)).reset_index(drop=True)
#%%
tsne_result
#%%
for col in ["DoW", "hour", "Generating"]:
    fig = px.scatter_3d(x=tsne_result.iloc[:, 0], y=tsne_result.iloc[:, 1], color=tsne_result[col], opacity=1, z=tsne_result.iloc[:, 2])
    fig.show()
#%%
