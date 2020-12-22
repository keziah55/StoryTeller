#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 22 16:45:48 2020

@author: keziah
"""

import sys
import os
import re

from PyQt5.QtGui import QPalette, QFont, QIcon, QKeySequence
from PyQt5.QtWidgets import (QAction, QDesktopWidget, QMainWindow, QMessageBox, 
                             QApplication, QVBoxLayout, QWidget, QTextEdit,
                             QSizePolicy, QLineEdit, QLabel)
from PyQt5.QtCore import pyqtSlot, pyqtSignal, QTimer, Qt

# TODO list
# save/open files
# make database of stories 
## title, date created, date(s) modified, word count, goal
# text formatting (bold, italic, font, size)
## write to plain text; generally use the database to access

class StoryTeller(QMainWindow):
    
    def __init__(self):
        super().__init__()
        
        self.goal = 100
        
        self.textEdit = StoryEditor()
        self.title = QLineEdit()
        font = self.title.font()
        font.setBold(True)
        self.title.setFont(font)
        self.title.setAlignment(Qt.AlignHCenter)
        self.wordCount = WordCountLabel(self.goal)
        
        self.textEdit.wordCount.connect(self.wordCount.setCountLabel)
        
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.title)
        self.layout.addWidget(self.textEdit)
        self.layout.addWidget(self.wordCount)
        
        self.centralWidget = QWidget()
        self.centralWidget.setLayout(self.layout)
        self.setCentralWidget(self.centralWidget)
        self.resize(500,600)
        self.centre()
        self.show()
        
    def centre(self):
        """ Centre window on screen. """
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
        
    def _makeMenus(self):
        pass
    
    def _makeActions(self):
        pass
        
    
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
        words = [word for word in words if word]
        if len(words) != self.count:
            self.count = len(words)
            self.wordCount.emit(self.count)
            
            
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
        
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = StoryTeller()
    sys.exit(app.exec_())