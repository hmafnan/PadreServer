import pandas as pd
from pypadre.pod.importing.dataset.dataset_import import SKLearnLoader


class CustomData:
    def __init__(self, df):
        self.df = df
        self.attributes = self.df.attributes

    @property
    def df_data(self):
        return pd.DataFrame(self.df.data())

    def data(self):
        return self.df_data


def load_digits_data():
    loader = SKLearnLoader()
    digits = loader.load("sklearn", utility="load_digits")
    d = CustomData(digits)
    return d