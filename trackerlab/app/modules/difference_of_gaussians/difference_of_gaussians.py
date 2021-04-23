# -*- coding: utf-8 -*-
"""
Discription: Module for Connected-Component Labeling. 
Author(s):   M. Fränzl
Date:        18/09/18
"""

import numpy as np

from skimage.feature import blob_dog
import pandas as pd

import os
path = os.path.dirname(os.path.realpath(__file__)) + "/"

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import pyqtSignal
from PyQt5.uic import loadUi

import pyqtgraph as pg

from ..utils import pgutils, helpwidget
from ..utils.settings import saveSettings, restoreSettings

from trackerlab.detectors import difference_of_gaussians

class Module(QtWidgets.QWidget):

    updated = pyqtSignal()
        
    def __init__(self):
        super().__init__(None)
        
        loadUi(os.path.splitext(os.path.relpath(__file__))[0] + '.ui', self)
        self.settingsFile = os.path.splitext(os.path.relpath(__file__))[0] + '.ini'
        
        self.helpWidget = helpwidget.HelpWidget()
        self.helpButton.clicked.connect(self.helpWidget.show)
        self.helpWidget.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        
        self.helpWidget.textEdit.setText('\n'.join([line.strip() for line in difference_of_gaussians.__doc__.split('\n')]))

        
        self.minSigmaSpinBox.valueChanged.connect(self.updated.emit)
        self.maxSigmaSpinBox.valueChanged.connect(self.updated.emit)
        self.sigmaRatioDoubleSpinBox.valueChanged.connect(self.updated.emit)
        self.thresholdDoubleSpinBox.valueChanged.connect(self.updated.emit)
        self.overlapDoubleSpinBox.valueChanged.connect(self.updated.emit)
        
        self.showOverlayCheckBox.stateChanged.connect(self.updated.emit)

        
    def attach(self, plot):
        self.p = plot
        self.items = []
        restoreSettings(self.settingsFile, self.widget)
        
        
    def detach(self):
        for item in self.items:
            self.p.removeItem(item) 
            del item
        saveSettings(self.settingsFile, self.widget)
       

    def findFeatures(self, frame, imageItem):
       
        image_in = imageItem.image
        minSigma = self.minSigmaSpinBox.value()
        maxSigma = self.maxSigmaSpinBox.value()
        sigmaRatio = self.sigmaRatioDoubleSpinBox.value()
        threshold = self.thresholdDoubleSpinBox.value()
        overlap = self.overlapDoubleSpinBox.value()
        
        features, _ = \
            difference_of_gaussians(image_in, 
                                    min_sigma=minSigma, 
                                    max_sigma=maxSigma, 
                                    sigma_ratio=sigmaRatio, 
                                    threshold=threshold, 
                                    overlap=overlap)
        
        #imageItem.setImage(image)
        
        for item in self.items:
            self.p.removeItem(item)
            del item
        self.items = []
        
        if self.showOverlayCheckBox.checkState():
            for i, f in features.iterrows():
                self.items.append(pgutils.CircleItem([f.x+0.5, f.y+0.5], np.sqrt(f.area/np.pi), color='r', width=2))
                self.p.addItem(self.items[-1]) 
            
        if features.size > 0:
            self.numberOfFeatures.setText(str(features.shape[0]))
        else:
            self.numberOfFeatures.setText('0')

        return features
