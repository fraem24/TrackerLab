# -*- coding: utf-8 -*-
"""
Discription: TrackLab of the Molecular Nanophotonics Group
Author(s): M. Fränzl
Data: 19/04/21
"""

import os
      
import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow, QWidget, QApplication, QDialog, QMessageBox

from PyQt5.uic import loadUi


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        path = os.path.dirname(os.path.realpath(__file__))

        self.ui = loadUi(path + '/app.ui', self)        
    
