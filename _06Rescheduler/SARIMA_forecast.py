import pandas as pd
from statsmodels.tsa.statespace.sarimax import SARIMAX

import DataRetriever as dr

RETRIEVER = dr.DataRetriever()


def sarima_prediction(date, data):
    best_params = (4, 1, 2, 0, 1, 1, 168)

    model = SARIMAX(endog=data,
                    trend='n',
                    order=best_params[: 3],
                    seasonal_order=best_params[3:]) \
        .fit(low_memory=True, disp=False, full_output=False)

    predictions = pd.DataFrame(model.predict(start=date, end=date + pd.Timedelta(days=2, hours=23)))

    return predictions


if __name__ == "__main__":
    print(sarima_prediction(date=pd.Timestamp(year=2016, month=1, day=21),
                            data=RETRIEVER.get_data(file_name='All-Subsystems-hour-Year2.pkl')[
                                   RETRIEVER.get_attributes(file_name='producing_attributes.pkl')].sum(axis=1).clip(
                                lower=0) / 1000))
