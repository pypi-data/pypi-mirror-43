import numpy as np
from sklearn import datasets
from sklearn import svm
from sklearn.dummy import DummyClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn_helper.data.DataCleaner import DataCleaner
from sklearn_helper.model_finder.BestFitFinder import BestFitFinder


class Thresholding(DataCleaner):
    THRESHOLD = 3

    def clean_x_y(self, x, y):
        return self.clean_x(x), y

    def clean_x(self, x):
        _x = np.copy(x)
        _x[_x <= self.THRESHOLD] = 0
        _x[_x > self.THRESHOLD] = 1
        return _x


if __name__ == "__main__":
    digits = datasets.load_digits()
    X_train, X_test, y_train, y_test = train_test_split(digits.data, digits.target, random_state=0, test_size=0.3)

    models = {
        "DummyClassifier": {
            "model": DummyClassifier()
        },
        "SVC": {
            "model": svm.SVC(C=2, gamma=0.0111)
        }
    }
    model_finder = BestFitFinder(models, data_cleaners=[Thresholding()], main_metric="accuracy")

    model = model_finder.evaluate(X_train, y_train)

    print(model)
    print(accuracy_score(model.predict(X_test), y_test))
