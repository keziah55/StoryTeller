#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 23 17:46:05 2020

@author: keziah
"""

import re
from PyQt5.QtWidgets import QTextEdit
from PyQt5.QtCore import pyqtSlot, pyqtSignal, QTimer


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
        
    @staticmethod    
    def countWordsInText(text):
        words = re.split(r"\s+", text.strip())
        words = [word for word in words if word]
        return len(words)
       
    @pyqtSlot()
    def countWords(self):
        text = self.toPlainText()
        count = self.countWordsInText(text)
        if count != self.count:
            self.count = count
            self.wordCount.emit(self.count)