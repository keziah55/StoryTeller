#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 22 16:45:48 2020

@author: keziah
"""

import sys
import os
import re

from PyQt5.QtGui import QIcon, QKeySequence
from PyQt5.QtWidgets import (QAction, QDesktopWidget, QMainWindow, QMessageBox, 
                             QApplication, QVBoxLayout, QWidget, QTextEdit,
                             QSizePolicy, QLineEdit, QLabel)
from PyQt5.QtCore import pyqtSlot, pyqtSignal, QTimer


class StoryTeller(QMainWindow):
    
    def __init__(self):
        super().__init__()
        
        self.goal = 100
        
        self.textEdit = StoryEditor()
        self.title = QLineEdit()
        self.wordCount = WordCountLabel(self.goal)
        
        self.textEdit.wordCount.connect(self.wordCount.setCountLabel)
        
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.title)
        self.layout.addWidget(self.textEdit)
        self.layout.addWidget(self.wordCount)
        
        self.centralWidget = QWidget()
        self.centralWidget.setLayout(self.layout)
        self.setCentralWidget(self.centralWidget)
        self.show()
        
    
class StoryEditor(QTextEdit):
    
    wordCount = pyqtSignal(int)
    """ **signal** wordCount 
    
        Emitted when the word count changes.
    """
    
    def __init__(self):
        super().__init__()
        
        self.count = 0
        self.timer = QTimer()
        self.timer.setSingleShot(True)
        self.timer.setInterval(100)
        self.timer.timeout.connect(self.countWords)
        self.textChanged.connect(self.timer.start)
        
       
    @pyqtSlot()
    def countWords(self):
        text = self.toPlainText()
        words = re.split(r"\s+", text.strip())
        if len(words) != self.count:
            self.count = len(words)
            self.wordCount.emit(self.count)
            
            
class WordCountLabel(QLabel):
    
    def __init__(self, goal):
        super().__init__()
        self.goal = goal
        self.setCountLabel(0)
        
    @pyqtSlot(int)
    def setCountLabel(self, count):
        self.setText(f"Word count: {count}, Goal: {self.goal}")
        
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = StoryTeller()
    sys.exit(app.exec_())