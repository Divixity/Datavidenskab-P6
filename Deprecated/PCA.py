import pandas as pd
import plotly.graph_objects as go

import DataRetriever as dr

from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.decomposition import PCA
from sklearn.metrics import mean_squared_error, make_scorer
from sklearn.preprocessing import StandardScaler


def PCA_function(X, number_of_PC, Skreeplot=True, reduced_dim_plot=True):
    pca = PCA(n_components=number_of_PC)
    pca.fit(X)
    pca_explained_var_ratio = pca.explained_variance_ratio_

    if Skreeplot == True:
        fig1 = go.Figure([go.Bar(y=pca_explained_var_ratio)])
        fig1.update_xaxes(title='Principal Component number')
        fig1.update_yaxes(title='Explained Variance Ratio')
        fig1.show()

    print('Componenets are', pca.components_)

    print(pca.components_[0])

    print('Singular values are', pca.singular_values_)

    if reduced_dim_plot == True:

        X_reduced = pca.transform(X)
        X_reduced_df = pd.DataFrame(X_reduced)
        print(X_reduced_df)
        print(X_reduced_df.columns)
        fig2 = go.Figure([go.Scatter3d(
            x=X_reduced_df[0],
            y=X_reduced_df[1],
            z=X_reduced_df[2],
            mode='markers',
            marker=dict(
                size=4,
                opacity=0.3
            )
        ),
        ])

        fig2.update_layout(scene=dict(
            xaxis = dict(title = 'PC1'),
            yaxis = dict(title = 'PC2'),
            zaxis = dict(title = 'PC3'),
        ))

        fig2.show()

if __name__ == '__main__':
    retriever = dr.DataRetriever()
    year_two = retriever.get_data("All-Subsystems-minute-Year2.pkl")
    year_two = year_two.dropna().reset_index(drop=True)
    year_two = year_two.drop(['Timestamp', 'TimeStamp_Count', 'DayOfWeek'], axis=1)

    scale = StandardScaler()
    year_two_scaled = scale.fit_transform(year_two)

    PCA_function(year_two_scaled, number_of_PC=0.9, Skreeplot=False, reduced_dim_plot=False)
