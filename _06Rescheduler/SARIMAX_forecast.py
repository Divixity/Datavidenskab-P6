import pickle
import pandas as pd
from sklearn.preprocessing import OneHotEncoder

import DataRetriever as dr

RETRIEVER = dr.DataRetriever()

with open(RETRIEVER.config_load() + '/prediction_models/sarimax_production', 'rb') as file:
    loaded_model = pickle.load(file)


def sarimax_prediction(date, pv):
    pv_copy = pd.DataFrame(pv).copy()
    pv_copy["Hour"] = pv_copy.index.hour

    ohe = OneHotEncoder(sparse=False)
    hot_np = ohe.fit_transform(pv_copy[["Hour"]])
    hot = pd.DataFrame(data=hot_np, columns=ohe.get_feature_names_out())
    del pv_copy["Hour"]

    weather_forecast = pd.read_csv("../_05Forecasting/CLEANED_GAI_2015_2016.csv")
    weather_forecast.rename(columns={'Time': 'Timestamp'}, inplace=True)

    pv_copy.reset_index(inplace=True)
    X = pv_copy.join(hot)

    ohe_condition = OneHotEncoder(sparse=False)
    hot_condition = ohe_condition.fit_transform(weather_forecast[["Condition"]])
    conditions = pd.DataFrame(data=hot_condition, columns=ohe_condition.get_feature_names_out())

    X = X.merge(conditions, left_index=True, right_index=True, how="left")
    X.set_index('Timestamp', inplace=True)
    X.rename(columns={0: "Generated Energy"}, inplace=True)

    exog_attributes = list(X.columns)
    exog_attributes.remove('Generated Energy')

    pred = loaded_model.predict(start=date, end=date + pd.Timedelta(days=2, hours=23),
                                exog=X[exog_attributes][date: date + pd.Timedelta(days=2, hours=23)])
    # sarimax_predictions = pd.DataFrame(pred.predicted_mean)
    # sarimax_predictions.rename(columns={'predicted_mean': 'Prediction'}, inplace=True)

    return pred


if __name__ == "__main__":
    print(sarimax_prediction(date=pd.Timestamp(year=2016, month=1, day=21),
                             pv=RETRIEVER.get_data(file_name='All-Subsystems-hour-Year2.pkl')[
                                    RETRIEVER.get_attributes(file_name='producing_attributes.pkl')].sum(axis=1).clip(
                                 lower=0) / 1000))
