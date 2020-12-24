#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 23 16:32:35 2020

@author: keziah
"""

import os
import re
from PyQt5.QtWidgets import (QDialog, QDialogButtonBox, QVBoxLayout, QHBoxLayout,
                             QAbstractItemView, QSizePolicy, QLabel, QLineEdit,
                             QPushButton, QWidget, QCheckBox)
from PyQt5.QtCore import pyqtSignal, pyqtSlot, QTimer
from .tablewidget import TableWidget
from .editor import StoryEditor


class OpenStoryDialog(QDialog):
    
    def __init__(self, path):
        super().__init__()
        
        self.path = path
        self.story = None
        
        stories = os.listdir(self.path)
        stories = [story for story in stories if os.path.splitext(story)[1]=='.html']
        
        header = ['Title', 'Date', 'Wordcount']
        self.storyTable = TableWidget(header, showRowNumbers=False)
        self.storyTable.setSelectionMode(QAbstractItemView.SingleSelection)
        self.populateTable(stories)
        self.storyTable.resizeColumnsToContents()
        
        self.buttons = QDialogButtonBox(QDialogButtonBox.Open|QDialogButtonBox.Cancel)
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.close)
        
        self.searchBar = SearchBar()
        self.searchBar.search.connect(self.search)
        # self.searchBar.next.clicked.connect(self.highlightNextSearch)
        # self.searchBar.prev.clicked.connect(self.highlightPrevSearch)
        # self.searchResults = []
        # self.searchIdx = 0
        
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.searchBar)
        self.layout.addWidget(self.storyTable)
        self.layout.addWidget(self.buttons)
        
        self.setLayout(self.layout)
        
        # self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        # height = self.storyTable.size().height()
        # width = sum([self.storyTable.columnWidth(i) for i in range(self.storyTable.columnCount)])
        self.resize(self.storyTable.size())
        
        
    @property
    def story(self):
        return self._story
    
    @story.setter
    def story(self, name):
        self._story = name
        
    @pyqtSlot()
    def accept(self):
        """ Set `story` proprety from currently selected list item. """
        self.story = self.storyTable.currentValue('title')
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
            # TODO store this info in database
            with open(os.path.join(self.path, t)) as fileobj:
                text = fileobj.read()
            wordcount = StoryEditor.countWordsInText(text)
            self.storyTable.addRow(title, date, wordcount)
    
    @pyqtSlot(str, bool)
    def search(self, text, caseSensitive):
        """ Search for `text` in the table. """
        if not text:
            # if empty search string, make sure all rows are visible and 
            # return from this method
            for idx in range(self.storyTable.rowCount):
                self.storyTable.showRow(idx)
            return None
        
        if not caseSensitive:
            text = text.lower()

        for idx in range(self.storyTable.rowCount):
            row = self.storyTable.getRow(idx)
            hideRow = True
            for item in row:
                if not caseSensitive:
                    item = item.lower()
                if text in item:
                    hideRow = False
            if hideRow:
                self.storyTable.hideRow(idx)
            elif self.storyTable.isRowHidden(idx):
                self.storyTable.showRow(idx)
                        
        
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
        text = self.edit.text()
        caseSensitive = self.case.isChecked()
        self.search.emit(text, caseSensitive)
        