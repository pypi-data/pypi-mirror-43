from sklearn_helper.data.DataCleaner import DataCleaner


class DummyCleaner(DataCleaner):
    def clean_x_y(self, x, y):
        return x, y

    def clean_x(self, x):
        return x
