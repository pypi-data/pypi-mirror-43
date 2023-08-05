import sys
from os.path import dirname, realpath

file_path = realpath(__file__)
dir_of_file = dirname(file_path)
sys.path.insert(0, dir_of_file)

from deepaugment import DeepAugment
from build_features import DataOp

my_config = {
    "model": "basiccnn",
    "method": "bayesian_optimization",
    "train_set_size": 1000,
    "opt_samples": 3,
    "opt_last_n_epochs": 3,
    "opt_initial_points": 100,
    "child_epochs": 2,
    "child_first_train_epochs": 0,
    "child_batch_size": 64
}

deepaug = DeepAugment("cifar10", config=my_config)

best_policies = deepaug.optimize(5)


from keras.datasets import cifar10
import keras
(x_train, y_train), (x_test, y_test) = cifar10.load_data()
image_gen = deepaug.image_generator_with_top_policies(x_train, keras.utils.to_categorical(y_train))

from deepaugment.childcnn import ChildCNN
import logging

cnn_config = {"model":"basicCNN", "logging":logging}
full_model = ChildCNN(input_shape=x_train.shape[1:], num_classes=10, config=cnn_config)

BATCH_SIZE = 64

full_model.model.fit_generator(
    image_gen,
    validation_data=(x_test, keras.utils.to_categorical(y_test)),
    steps_per_epoch=len(x_train) // BATCH_SIZE,
    epochs=5,
    shuffle=True,
    verbose=2
)



#
# X, y, input_shape = DataOp.load("cifar10")
# train_size = int(len(X)*0.9)
#
# data = DataOp.preprocess(X, y, train_size)
#
#
# imgen = deepaug.image_generator_with_top_policies(data["X_train"], data["y_train"])

print("End")
