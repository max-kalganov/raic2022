import sklearn
import pickle
import numpy as np


def get_init_data():
    X = np.array([
        []
    ])


def get_model():
    return sklearn.neural_network.MLPClassifier(hidden_layer_sizes=())


def train_model():
    X, y = get_init_data()
    model = get_model()
    model.fit(X, y)
    pickle.dump(model, open("data/model.sav", 'wb'))


if __name__ == '__main__':
    train_model()
