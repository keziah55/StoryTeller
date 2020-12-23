#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 23 16:32:35 2020

@author: keziah
"""

import os
import re
from PyQt5.QtWidgets import (QDialog, QDialogButtonBox, QListWidget, QTableWidget,
                             QVBoxLayout, QAbstractItemView)
from PyQt5.QtCore import pyqtSlot


class OpenStoryDialog(QDialog):
    
    def __init__(self, path):
        super().__init__()
        
        self.path = path
        self.story = None
        
        stories = os.listdir(self.path)
        stories = [story for story in stories if os.path.splitext(story)[1]=='.html']
        
        header = ['Title', 'Date', 'Wordcount']
        self.storyTable = QTableWidget(len(stories), len(header))
        self.storyTable.setHorizontalHeaderLabels(header)
        
        self.storyList = QListWidget()
        self.storyList.addItems(stories)
        self.storyList.setSelectionMode(QAbstractItemView.SingleSelection)
        
        self.buttons = QDialogButtonBox(QDialogButtonBox.Open|QDialogButtonBox.Cancel)
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.close)
        
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.storyList)
        self.layout.addWidget(self.buttons)
        
        self.setLayout(self.layout)
        
    @property
    def story(self):
        return self._story
    
    @story.setter
    def story(self, name):
        self._story = name
        
    @pyqtSlot()
    def accept(self):
        """ Set `story` proprety from currently selected list item. """
        item = self.storyList.currentItem()
        self.story = item.text()
        super().accept()
        
    def execDialog(self):
        """ Wrap `exec_()` call to return True if result is QDialog.Accepted
            and False otherwise.
        """
        result = self.exec_()
        if result == QDialog.Accepted:
            return True
        else:
            return False
        
    def populateTable(self, titles):
        for t in titles:
            title, _ = os.path.splitext(t)
            srch = re.search(r"(\d{4}-\d{2}-\d{2} )(.+)", title)
            date = srch.group(1).strip()
            title = srch.group(2).strip()
            
    
        