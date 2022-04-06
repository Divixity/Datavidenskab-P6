import numpy as np


def sine_calculation(freqs: list, x: float) -> float:
    result = 0

    for frequency in freqs:
        result += np.sin(frequency * np.pi * x)

    return result


def cosine_calculation(freqs: list, x: float) -> float:
    result = 0

    for frequency in freqs:
        result += np.cos(frequency * np.pi * x)

    return result


class FastFourierPredict:
    def __init__(self, data: np.array, train_size: float, frequency_limit: float):
        self.cosine_freqs = None
        self.sine_freqs = None
        self.data = data
        self.data_size = data.size
        self.train_size = train_size
        self.train_idx = int(data.size * train_size)
        self.test_size = data.size - self.train_idx
        self.frequency_limit = frequency_limit

    def fourier_transform(self) -> None:
        train_data = self.data[0: self.train_idx]

        fourier_train = np.fft.rfft(train_data, axis=0)
        freqs_train = np.fft.rfftfreq(train_data.size)

        frequency_bound = np.quantile(a=fourier_train, q=self.frequency_limit)

        iter_size = len(fourier_train)
        sine_freqs = list()
        cosine_freqs = list()

        for idx in range(0, iter_size):
            if np.abs(fourier_train[idx].real) >= frequency_bound:
                cosine_freqs.append(freqs_train[idx])
            if np.abs(fourier_train[idx].imag) >= frequency_bound:
                sine_freqs.append(freqs_train[idx])

        self.cosine_freqs = cosine_freqs
        self.sine_freqs = sine_freqs

    def fourier_predict(self) -> list[float]:
        self.fourier_transform()
        results = list()

        for idx in range(self.data_size - self.test_size, self.data_size):
            cosine_sum = cosine_calculation(freqs=self.cosine_freqs, x=idx)
            sine_sum = sine_calculation(freqs=self.sine_freqs, x=idx)
            results.append(idx * (cosine_sum + sine_sum))

        return results


if __name__ == '__main__':
    import DataRetriever as dr

    RETRIEVER = dr.DataRetriever()
    CON_ATTRIBUTES = RETRIEVER.get_attributes(file_name='consuming_attributes.pkl')
    DATA = RETRIEVER.get_data(file_name='All-Subsystems-hour-Year2.pkl')[CON_ATTRIBUTES].sum(axis=1).to_numpy()

    predictor = FastFourierPredict(data=DATA, train_size=0.95, frequency_limit=0.9)

    print(predictor.fourier_predict())
