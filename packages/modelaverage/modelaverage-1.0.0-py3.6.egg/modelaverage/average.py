"""
      code by Tae Hwan Jung(Jeff Jung) @graykode
      code reference : https://stackoverflow.com/questions/48212110/average-weights-in-keras-models
"""
import os
import tensorflow as tf
import numpy as np

def average(model, modelfiles):
    """
    :param model: Tensorflow-Keras model
    :param modelfiles: list of model file names.
    :return: averaged weight model
    """
    if len(modelfiles) == 0:
        raise Exception('model file is not found')

    modelfiles = [os.path.abspath(path) for path in modelfiles]
    models = [tf.keras.models.load_model(file, compile=False) for file in modelfiles]
    weights = [model.get_weights() for model in models]
    new_weights = list()
    for weights_list_tuple in zip(*weights):
        new_weights.append([np.array(weights_).mean(axis=0) \
             for weights_ in zip(*weights_list_tuple)])

    model.set_weights(new_weights)
    return model