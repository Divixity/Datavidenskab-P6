import plotly.express as px
from sklearn.manifold import TSNE

import DataRetriever as dr

retriever = dr.DataRetriever()
hour = retriever.get_data("All-Subsystems-hour-Year2.pkl")

X = hour.iloc[:, 1:]
X.fillna(0, inplace=True)

n_components = 3
tsne = TSNE(n_components)
tsne_result = tsne.fit_transform(X)

fig = px.scatter_3d(x=tsne_result[:, 0], y=tsne_result[:, 1], z=tsne_result[:, 2], opacity=0.25)
fig.show()
