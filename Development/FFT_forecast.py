import numpy as np


def fourierExtrapolation(data: np.array, number_of_predictions: int, n_sinusoids: int) -> np.array:
    """
    Predict {number_of_predictions} observations after the index data.size of {data}, using {n_sinusoids} sinusoids.
    :param data: The data on which to train the model. Corresponds to {_x = x_0, x_1, ... x_(n-1)} in the theory
    :param number_of_predictions: The amount of predictions to output. Corresponds to {x_((n-1)+1), x_((n-1)+2), ..., x_((n-1)+{number_of_predictions})}
    :param n_sinusoids: The amount of sinusoids on which to base the predictions. I.e. the data probably contains many sinusoids, but we only wish to make predictions based on the {n_sinusoids} largest frequencies.
    :return: A numpy array of length data.size + number_of_predictions, containing the transformed original data + predictions
    """
    data_size = data.size  # n

    X_frequency_domain = list(np.fft.fft(data))  # The series of complex numbers X = {X1, X2, ...}
    frequencies = list(np.fft.fftfreq(data_size, d=1))  # Some frequencies, e.g. {4, 3, -7, 8, -5, ...}

    indexes = list(range(len(X_frequency_domain)))  # {0, 1, ..., n-1}
    indexes.sort(key=lambda idx: np.absolute(X_frequency_domain[idx]), reverse=True)  # ascendingly sort indices by amplitude

    sample_index = np.arange(0, data_size + number_of_predictions)  # sample_index = {0, 1, ..., n-1, n, n+1, ..., (n-1)+number_of_predictions}
    x_restored_sig = np.zeros(sample_index.size)  # Prepare a numpy array to receive x reconstructed from its Fourier Transform

    if n_sinusoids == 0:
        return x_restored_sig + data.mean()

    for i in indexes[:n_sinusoids]:
        amplitude = np.absolute(X_frequency_domain[i])
        phase = np.angle(X_frequency_domain[i])
        x_restored_sig += amplitude * np.cos(2 * np.pi * frequencies[i] * sample_index + phase)

    x_restored = 1 / data_size * x_restored_sig

    return x_restored


if __name__ == "__main__":
    from sklearn.metrics import mean_squared_error
    import DataRetriever as dr

    RETRIEVER = dr.DataRetriever()
    actual = (RETRIEVER.get_data(file_name='All-Subsystems-hour-Year2.pkl')[RETRIEVER.get_attributes(file_name='consuming_attributes.pkl')].sum(axis=1).clip(lower=0) / 1000)["2016-01-17 00:00:00":"2016-01-19 23:00:00"]
    test = (RETRIEVER.get_data(file_name='All-Subsystems-hour-Year2.pkl')[RETRIEVER.get_attributes(file_name='consuming_attributes.pkl')].sum(axis=1).clip(lower=0) / 1000)["2016-01-10 00:00:00":"2016-01-16 23:00:00"]
    print(mean_squared_error(actual, fourierExtrapolation(test, 72, 70)[len(test):], squared=False))
