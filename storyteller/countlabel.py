#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 23 17:48:46 2020

@author: keziah
"""

from PyQt5.QtGui import QPalette
from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import pyqtSlot, Qt


class WordCountLabel(QLabel):
    
    def __init__(self, goal):
        super().__init__()
        self.goal = goal
        
        self.lessPalette = QPalette()
        self.equalPalette = QPalette()
        self.morePalette = QPalette()
        
        self.lessPalette.setColor(QPalette.WindowText, Qt.red)
        self.equalPalette.setColor(QPalette.WindowText, Qt.green)
        self.morePalette.setColor(QPalette.WindowText, Qt.yellow)
        self.setAutoFillBackground(True)
        
        self.setCountLabel(0)
        
    @pyqtSlot(int)
    def setCountLabel(self, count):
        if count < self.goal:
            self.setPalette(self.lessPalette)
        elif count == self.goal:
            self.setPalette(self.equalPalette)
        else:
            self.setPalette(self.morePalette)
        self.setText(f"Word count: {count}, Goal: {self.goal}")
        