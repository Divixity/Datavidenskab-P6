import pandas as pd
import plotly

from DataRetriever import DataRetriever
import plotly.graph_objects as go
from plotly.subplots import make_subplots

if __name__ == "__main__":
    open_data = DataRetriever()

    year1hour = open_data.get_data("All-Subsystems-hour-Year1.pkl")
    year2hour = open_data.get_data("All-Subsystems-hour-Year2.pkl")

    year1min = open_data.get_data("All-Subsystems-minute-Year1.pkl")
    year2min = open_data.get_data("All-Subsystems-minute-Year2.pkl")

    print("year 1 hour:", year1hour.shape)
    print("year 1 min:", year1min.shape)
    print("year 2 hour:", year2hour.shape)
    print("year 2 min:", year2min.shape)

    #The two extra columns in the minute versions
    for col in year2min.columns:
        if col not in year2hour.columns:
            print(col)

    #The 24 extra columns in the year2 versions
    for column in year2hour.columns:
        if column not in year1hour.columns:
            print(column)

    #Basic descriptive statistics for all columns
    y1hsummary = year1hour.describe()
    y2hsummary = year2hour.describe()

    # import plotly.express as px
    #
    # corr = year2min.corr()
    # fig = px.imshow(corr, color_continuous_scale='RdBu', color_continuous_midpoint=0)

    #fig.show()


    countnanvalues_dict = {}
    for column in year2hour.columns:
        columnnanvalue = year2hour[column].isnull().sum()
        if columnnanvalue > 0:
            countnanvalues_dict[column] = columnnanvalue
            print(column, "has ", columnnanvalue, " number of NaN values" )

    countnanvalues_df = pd.DataFrame.from_dict(countnanvalues_dict, orient='index', columns=['NaN']).sort_values(by=['NaN'], ascending=False)
    #countnanvalues_df.drop(['SHW_GlycolFlowHXCoriolisSHW', 'SHW_WaterFlowHXCoriolisSHW', 'SHW_GlycolFlowRateHXCoriolisSHW', 'SHW_WaterFlowRateHXCoriolisSHW'], axis=0, inplace=True)
    print(countnanvalues_df)

    subsystemnanvalues_df = countnanvalues_df.groupby([s.split('_')[0] for s in countnanvalues_df.index.values]).sum()
    subsystemnanvalues_df = subsystemnanvalues_df.sort_values(by=['NaN'], ascending=False)

    fig2 = make_subplots(rows=1, cols=2)
    #fig2.add_trace(go.Bar(name='Missing values in channels', x=countnanvalues_df.index, y=countnanvalues_df['NaN']), row=1, col=1)
    fig2.add_trace(go.Bar(name='Missing values per Subsystem groups', x=subsystemnanvalues_df.index, y=subsystemnanvalues_df['NaN']), row=1, col=2)
    fig2.update_yaxes(title='Number of Missing Values')
    fig2.show()