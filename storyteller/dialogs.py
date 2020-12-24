#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 23 16:32:35 2020

@author: keziah
"""

import os
import re
from PyQt5.QtWidgets import (QDialog, QDialogButtonBox, QVBoxLayout,
                             QAbstractItemView)
from PyQt5.QtCore import pyqtSlot
from .tablewidget import TableWidget
from .editor import StoryEditor
from .searchbar import SearchBar


class OpenStoryDialog(QDialog):
    """ Dialog showing a searchable table of story titles, dates and wordcounts.
    
        Parameters
        ----------
        path : str
            Path to directory where stories are stored.
    """
    
    def __init__(self, path):
        super().__init__()
        
        self.path = path
        self.story = None
        
        stories = os.listdir(self.path)
        stories = [story for story in stories if os.path.splitext(story)[1]=='.html']
        
        header = ['Title', 'Date', 'Wordcount']
        self.storyTable = TableWidget(header, showRowNumbers=False, readOnly=True)
        self.storyTable.setSelectionMode(QAbstractItemView.SingleSelection)
        self.populateTable(stories)
        self.storyTable.resizeColumnsToContents()
        
        self.buttons = QDialogButtonBox(QDialogButtonBox.Open|QDialogButtonBox.Cancel)
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.close)
        
        self.searchBar = SearchBar()
        self.searchBar.search.connect(self.search)
        
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.searchBar)
        self.layout.addWidget(self.storyTable)
        self.layout.addWidget(self.buttons)
        
        self.setLayout(self.layout)
        
        self.resize(self.storyTable.size())
        
        
    @property
    def file(self):
        return self._file
    
    @file.setter
    def file(self, name):
        self._file = name
        
    @pyqtSlot()
    def accept(self):
        """ Set `story` proprety from currently selected list item. """
        row = self.storyTable.currentRow
        self.file = f"{row['Date']} {row['Title']}.html"
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
        """ Add data from list of `titles` to the table. """
        for t in titles:
            title, _ = os.path.splitext(t)
            srch = re.search(r"(\d{4}-\d{2}-\d{2} )(.+)", title)
            date = srch.group(1).strip()
            title = srch.group(2).strip()
            # TODO store this info in database
            # Also the wordcount returned here is wrong
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
    
        