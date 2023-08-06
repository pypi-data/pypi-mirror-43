scikit-learn-helper
============

scikit-learn-helper is a light library with the purpose of providing utility functions that makes working with scikit-learn even easier, by letting us to focus on the solving the probling instead of writting boilerplate code

### Installation

#### Dependencies
scikit-learn-helper requires:

    scikit-learn (>= 0.20.2) Of course :)

#### User installation


    pip install scikit-learn-helper


#### Source code


    https://github.com/aras7/scikit-learn-helper

### Examples

#### How to compare 2+ models?

```python
from sklearn.metrics import accuracy_score
from sklearn_helper.model_finder.BestFitFinder import BestFitFinder
digits = datasets.load_digits()

models = {
    "DummyClassifier": {
        "model": DummyClassifier()
    },
    "SVC": {
        "model": svm.SVC()
    }
}
model_finder = BestFitFinder(models, main_metric=accuracy_score)

X, y = digits.data, digits.target
model = model_finder.evaluate(X, y)
```

###### Output

```
Model: SVC             | cleaner:DummyCleaner | accuracy:0.4179 |Time:1.35 sec
Model: DummyClassifier | cleaner:DummyCleaner | accuracy:0.0991 |Time:0.01 sec
```

#### How to compare and tune models?
```python
from sklearn_helper.model_finder.BestFitFinder import BestFitFinder
digits = datasets.load_digits()
models = {
    "SVC": {
        "model": svm.SVC()
    },
    "Improved SVC": {
        "model": svm.SVC(),
        "params": {
             "gamma": np.linspace(0, 0.1, num=10),
             "C": range(1, 10)
         }
    }
}
model_finder = BestFitFinder(models, main_metric="accuracy")

X, y = digits.data, digits.target
model = model_finder.evaluate(X, y)
print(model)
```

###### Output
```
Model: Improved SVC | cleaner:DummyCleaner | accuracy:0.6511 |Time:1.17 sec
Model: SVC          | cleaner:DummyCleaner | accuracy:0.4179 |Time:1.19 sec
>>> print(model)
SVC(C=2, cache_size=200, class_weight=None, coef0=0.0,
  decision_function_shape='ovr', degree=3, gamma=0.011111111111111112,
  kernel='rbf', max_iter=-1, probability=False, random_state=None,
  shrinking=True, tol=0.001, verbose=False)
```

#### How to use other another metric for evaluation?
```
models = {
    "DummyClassifier": {
        "model": DummyClassifier()
    },
    "SVC": {
        "model": svm.SVC()
    }
}
model_finder = BestFitFinder(models, main_metric="roc_auc")
dataset = datasets.load_breast_cancer()
X, y = dataset.data, dataset.target
model = model_finder.evaluate(X, y)
```

###### Output
```
Model: SVC             | cleaner:DummyCleaner | roc_auc:0.9302 |Time:0.05 sec
Model: DummyClassifier | cleaner:DummyCleaner | roc_auc:0.5096 |Time:0.01 sec
```


#### How to use get multiple metric?
```
models = {
    "DummyClassifier": {
        "model": DummyClassifier()
    },
    "SVC": {
        "model": svm.SVC()
    }
}
model_finder = BestFitFinder(models, main_metric="roc_auc", additional_metrics=["f1", "accuracy"])
model = model_finder.evaluate(X, y)
```

###### Output
```
Model: SVC             | cleaner:DummyCleaner | roc_auc:0.9302 |f1:0.7650 |accuracy:0.6277 |Time:0.25 sec
Model: DummyClassifier | cleaner:DummyCleaner | roc_auc:0.4966 |f1:0.6129 |accuracy:0.5361 |Time:0.01 sec
```

#### Can I compare data engineering process? yes :)
```
from sklearn_helper.model_finder.BestFitFinder import BestFitFinder
from sklearn_helper.data.DataCleaner import DataCleaner
from sklearn_helper.data.DummyCleaner import DummyCleaner # No transformation is applied

class Thresholding(DataCleaner):
    THRESHOLD = 3
    def clean_x_y(self, x, y):
        return self.clean_x(x), y
    def clean_x(self, x):
        _x = np.copy(x)
        _x[_x <= self.THRESHOLD] = 0
        _x[_x > self.THRESHOLD] = 1
        return _x

models = {
    "DummyClassifier": {
        "model": DummyClassifier()
    },
    "SVC": {
        "model": svm.SVC(C=2, gamma=0.0111)
    }
}
model_finder = BestFitFinder(models, data_cleaners=[Thresholding(), DummyCleaner()], main_metric="accuracy")

digits = datasets.load_digits()
X, y = digits.data, digits.target
model = model_finder.evaluate(X, y)
```

###### Output
```
Model: SVC             | cleaner:Thresholding | accuracy:0.8848 |Time:0.36 sec
Model: SVC             | cleaner:DummyCleaner | accuracy:0.6516 |Time:1.20 sec
Model: DummyClassifier | cleaner:Thresholding | accuracy:0.1046 |Time:0.00 sec
Model: DummyClassifier | cleaner:DummyCleaner | accuracy:0.0985 |Time:0.00 sec
```

#### For more examples refer to:

    https://github.com/aras7/scikit-learn-helper/tree/master/examples


### ToDo:

* Add unit tests
* Add prediction time to printed results
* Improve documentation
 * Splitter
* Add functionality to test different dataset as an alternative to `from sklearn.model_selection import cross_val_score`. It might be useful when resampling inside DataCleaners
* Add codecov.io suport
