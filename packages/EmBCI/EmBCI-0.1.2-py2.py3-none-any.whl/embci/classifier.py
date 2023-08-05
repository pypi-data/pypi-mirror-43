#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 27 22:59:33 2018

@author: ASDF(JTQ)
@author: hank
"""
# built-in
import os
import sys
import math

# requirements.txt: machine-learning: sklearn, keras
# requirements.txt: data-processing: numpy
import numpy as np
from sklearn import svm

# Mute `Using X backend.` log.
# See #1406 @ https://github.com/keras-team/keras/issues/1406
from .utils import TempStream
with TempStream(stderr=None):
    import keras

from keras.layers import Dense, Dropout, Flatten, Conv2D
from keras.layers import MaxPooling2D, TimeDistributed, LSTM
from keras.utils.np_utils import to_categorical

from .processing import SignalInfo


class Models():
    supported_models = ['Default: 2layer-CNN(keras)',
                        'CNN_LSTM: 2layer-CNN-1layer-LSTM(keras)',
                        'Double_Dense: 2layer-Dense(keras)',
                        'SVM: Support-Vector-Machine(sklearn)']

    def __init__(self, sample_rate, sample_time, model_type='Default'):
        '''
        Please check Models.supported_models for a full list of all implemented
        classifiers. You are welcomed to add a new one.
        '''
        if model_type == 'SVM':
            self.model = None
        elif model_type == 'Default':
            self.model = keras.models.Sequential(name='Default')
        elif model_type == 'CNN_LSTM':
            self.model = keras.models.Sequential(name='CNN_LSTM')
        elif model_type == 'Double_Dense':
            self.model = keras.models.Sequential(name='Double_Dense')
        else:
            raise RuntimeError('Not supported model type.')

        self.built = False
        self.model_type = model_type
        self.fs = sample_rate
        self._p = SignalInfo(sample_rate)
        self._result = None
        self._preprocessers = []

    def build(self, nb_classes, shape):
        self._preprocessers = []
        if self.model_type == 'Default':
            #  src: n_sample x n_channel x window_size
            #  out: n_sample x freq x time x n_channel
            #  label: n_sample x 1
            #  freq: int(1 + math.floor(float(nperseg)/2))
            #  time: int(1 + math.ceil(float(window_size)/(nperseg-noverlap)))
            self._preprocessers += [self._p.detrend]
            self._preprocessers += [self._p.notch]
            self._preprocessers += [self._p.stft]
            self._preprocessers += [lambda X: np.transpose(X, (0, 2, 3, 1))]

            nperseg = int(self.fs / 5)
            noverlap = int(self.fs / 5 * 0.67)
            f = int(1 + math.floor(float(nperseg) / 2))
            t = int(1 + math.ceil(float(shape[2]) / (nperseg - noverlap)))

            self._Default(nb_classes, (f, t, shape[1]))
            self.epochs, self.batch_size = 60, 25

        elif self.model_type == 'CNN_LSTM':
            self._preprocessers += [self._p.detrend,
                                    self._p.notch,
                                    self._p.stft]
            self._preprocessers += [lambda X: np.transpose(X, (0, 2, 3, 1))]
            nperseg = int(self.fs / 5)
            noverlap = int(self.fs / 5 * 0.67)
            f = int(1 + math.floor(float(nperseg) / 2))
            t = int(1 + math.ceil(float(shape[2]) / (nperseg - noverlap)))
            self._CNN_LSTM(nb_classes, (f, t, shape[1]))
            self.epochs, self.batch_size = 60, 20

        elif self.model_type == 'Double_Dense':
            #  src: n_sample x n_channel x window_size
            #  out: n_sample x n_channel x window_size
            #  label: n_sample x 1
            self._preprocessers += [self._p.detrend, self._p.notch]
            self._Double_Dense(nb_classes, shape[1:])
            self.epochs, self.batch_size = 200, 15

        elif self.model_type == 'SVM':
            #  src: n_sample x n_channel x window_size
            #  out: n_sample x series(n_channel * freq * time)
            #  label:  n_sample x 1
            self._preprocessers += [self._p.detrend,
                                    self._p.notch,
                                    self._p.stft]
            self._preprocessers += [lambda X: X.reshape(X.shape[0], -1)]
            self._SVM()
        self.built = True

    def _Default(self, nb_classes, input_shape):
        print('building model with data shape{}'.format(input_shape))

        self.model.add(Conv2D(filters=16,
                              kernel_size=3,
                              padding='valid',
                              activation='relu',
                              input_shape=input_shape))
        self.model.add(MaxPooling2D(3))
        self.model.add(Conv2D(filters=8,
                              kernel_size=3,
                              padding='valid',
                              activation='relu'))
        self.model.add(MaxPooling2D(3))
        self.model.add(Flatten())
        self.model.add(Dense(128, activation='relu'))
        self.model.add(Dense(64, activation='relu'))
        self.model.add(Dense(nb_classes, activation='softmax'))
        self.model.compile(loss='categorical_crossentropy',
                           optimizer='adadelta',
                           metrics=['accuracy'])

    def _CNN_LSTM(self, nb_classes, input_shape):
        print('building model with data shape{}'.format(input_shape))

        self.model.add(TimeDistributed(Conv2D(32, 5, 5, padding='same'),
                                       activation='relu',
                                       input_shape=input_shape))
        self.model.add(TimeDistributed(Conv2D(32, 5, 5),
                                       activation='relu'))
        self.model.add(TimeDistributed(MaxPooling2D(5)))
        self.model.add(TimeDistributed(Dropout(0.25)))
        self.model.add(TimeDistributed(Flatten()))
        self.model.add(LSTM(16, return_sequences=True))
        self.model.add(Dense(10, actication='relu'))
        self.model.add(Dense(nb_classes, activation='softmax'))

    def _SVM(self):
        self.model = svm.SVC()

    def _Double_Dense(self, nb_classes, input_shape):
        print('building model with data shape{}'.format(input_shape))
        self.model.add(Dense(128, activation='relu', input_shape=input_shape))
        self.model.add(Dense(72, activation='relu'))
        self.model.add(Flatten())
        self.model.add(Dense(nb_classes, activation='softmax'))
        self.model.compile(loss='categorical_crossentropy',
                           optimizer='adadelta',
                           metrics=['accuracy'])

    def save(self, model_name):
        if not self.built:
            raise RuntimeError('you need to build the model first')
        if self.model_type == 'SVM':
            # TODO 4: save trained svm
            raise RuntimeError('SVM can not be saved yet')
        self.model.save(model_name)

    def load(self, model_name):
        self._preprocessers = []
        self.model = keras.models.load_model(model_name)
        # TODO 5: fix bug, model name can be saved but cannot be loaded
        # if self.model.name in ['Default', 'CNN_LSTM']:
        self._preprocessers += [self._p.detrend]
        self._preprocessers += [self._p.notch]
        self._preprocessers += [self._p.stft]
        self._preprocessers += [lambda X: np.transpose(X, (0, 2, 3, 1))]
        # elif self.model.name in ['Double_Dense']:
        self.built = True

    def train(self, data, label):
        if not self.built:
            raise RuntimeError('you need to build the model first')

        # preprocessing
        for f in self._preprocessers:
            data = f(data)
        label = to_categorical(label)

        # train the model
        if self.model_type == 'SVM':
            self.model.fit(data, label)
        elif self.model_type in ['Default', 'CNN_LSTM', 'Double_Dense']:
            self.model.fit(data, label, validation_split=0.2, shuffle=True,
                           batch_size=self.batch_size, epochs=self.epochs)

    def predict(self, data):
        if not self.built:
            raise RuntimeError('you need to build the model first')

        # preprocessing
        for f in self._preprocessers:
            data = f(data)

        # predict value
        if self.model_type == 'SVM':
            tmp = self.model.predict_proba(data)
        elif self.model_type in ['Default', 'CNN_LSTM', 'Double_Dense']:
            # tmp = self.model.predict_classes(data, verbose=0)
            tmp = self.model.predict_proba(data, verbose=0)

        return tmp.argmax(), tmp.max()


if __name__ == '__main__':
    test = Models(250, 2, 'Default')
    test.build(nb_classes=6, input_shape=(50, 1, 500))
