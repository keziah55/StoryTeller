#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 24 13:35:37 2020

@author: keziah
"""

from PyQt5.QtWidgets import (QHBoxLayout, QLabel, QLineEdit, QPushButton, 
                             QWidget, QCheckBox)
from PyQt5.QtCore import pyqtSignal, pyqtSlot, QTimer

class SearchBar(QWidget):
    """ QWidget providing a serach bar, with case sensitive check box.
    
        Parameters
        ----------
        timeout : int
            Signal with search parameters will be emitted `timeout` ms after
            text is typed in the search bar. Default is 100ms.
    """
    
    search = pyqtSignal(str, bool)
    """ **signal** search(str `text`, bool `caseSensitive`)
    
        Request search for given string.
    """
    
    def __init__(self, timeout=100):
        super().__init__()
        
        self.label = QLabel("Search")
        self.edit = QLineEdit()
        self.clear = QPushButton("Clear")
        self.caseLabel = QLabel("Case sensitive")
        self.case = QCheckBox()
        
        self.timer = QTimer()
        self.timer.setSingleShot(True)
        self.timer.setInterval(timeout)
        self.timer.timeout.connect(self.requestSearch)
        self.edit.textChanged.connect(self.timer.start)
        
        self.clear.clicked.connect(lambda: self.edit.setText(""))
        
        self.layout = QHBoxLayout()
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.edit)
        self.layout.addWidget(self.caseLabel)
        self.layout.addWidget(self.case)
        self.layout.addWidget(self.clear)
        
        self.setLayout(self.layout)
        
    @pyqtSlot()
    def requestSearch(self):
        """ Get search string and case sensitive status and emit `search` signal. """
        text = self.edit.text()
        caseSensitive = self.case.isChecked()
        self.search.emit(text, caseSensitive)