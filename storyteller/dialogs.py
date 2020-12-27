#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 23 16:32:35 2020

@author: keziah
"""

import os
import re
from abc import abstractmethod
from PyQt5.QtWidgets import (QDialog, QDialogButtonBox, QVBoxLayout,
                             QAbstractItemView, QListWidget)
from PyQt5.QtCore import pyqtSlot, Qt
from .metaclass import PyQtMetaclass
from .tablewidget import TableWidget
from .editor import StoryEditor
from .searchbar import SearchBar


class AbstractDialog(QDialog, metaclass=PyQtMetaclass):
    def __init__(self, path, title):
        super().__init__()
        
        self.path = path
        
        self.setWindowTitle(title)
        
        self.buttons = QDialogButtonBox(QDialogButtonBox.Open|QDialogButtonBox.Cancel)
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.close)
        
        self.searchBar = SearchBar()
        self.searchBar.search.connect(self.search)
        
        
    def _makeLayout(self):
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.searchBar)
        self.layout.addWidget(self.widget)
        self.layout.addWidget(self.buttons)
        
        self.setLayout(self.layout)
        
        
    @property
    def value(self):
        return self._value
    
    @value.setter
    def value(self, name):
        self._value = name
        
    def execDialog(self):
        """ Wrap `exec_()` call to return True if result is QDialog.Accepted
            and False otherwise.
        """
        result = self.exec_()
        if result == QDialog.Accepted:
            return True
        else:
            return False
        
    @abstractmethod
    def populateWidget(self, lst):
        pass
    
    @abstractmethod
    @pyqtSlot(str, bool)
    def search(self, text, caseSensitive):
        pass


class OpenStoryDialog(AbstractDialog):
    """ Dialog showing a searchable table of story titles, dates and wordcounts.
    
        Parameters
        ----------
        path : str
            Path to directory where stories are stored.
    """
    
    def __init__(self, path):
        super().__init__(path, "Open story")
        
        stories = os.listdir(self.path)
        stories = [story for story in stories if os.path.splitext(story)[1]=='.html']
        
        header = ['Title', 'Date', 'Wordcount']
        self.widget = TableWidget(header, showRowNumbers=False, readOnly=True)
        self.widget.setSelectionMode(QAbstractItemView.SingleSelection)
        self.populateWidget(stories)
        self.widget.resizeColumnsToContents()
        
        self._makeLayout()
        
        
    @pyqtSlot()
    def accept(self):
        """ Set `story` proprety from currently selected list item. """
        row = self.widget.currentRow
        self.value = f"{row['Date']} {row['Title']}.html"
        super().accept()
        
        
    def populateWidget(self, titles):
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
            self.widget.addRow(title, date, wordcount)
        # most recent first
        self.widget.sort('Date', Qt.DescendingOrder)
    
    
    @pyqtSlot(str, bool)
    def search(self, text, caseSensitive):
        """ Search for `text` in the table. """
        if not text:
            # if empty search string, make sure all rows are visible and 
            # return from this method
            for idx in range(self.widget.rowCount):
                self.widget.showRow(idx)
            return None
        
        if not caseSensitive:
            text = text.lower()

        for idx in range(self.widget.rowCount):
            row = self.widget.getRow(idx)
            hideRow = True
            for item in row:
                if not caseSensitive:
                    item = item.lower()
                if text in item:
                    hideRow = False
            if hideRow:
                self.widget.hideRow(idx)
            elif self.widget.isRowHidden(idx):
                self.widget.showRow(idx)
    
    
class TitleListDialog(AbstractDialog):
    
    def __init__(self, path):
        super().__init__(path, "View or edit list of titles")
        
        self.path = path
        
        file = os.path.join(self.path, 'title_list')
        
        # make file if it doesn't exist
        if not os.path.exists(file):
            with open(file, 'w') as fileobj:
                fileobj.write("")

        with open(file) as fileobj:
            text = fileobj.read()
        titles = [title for title in text.split('\n') if title]
        
        self.widget = QListWidget()
        self.populateWidget(titles)
        
        self._makeLayout()
        
        
    def populateWidget(self, titles):
        self.widget.addItems(sorted(titles))
        
        
    @pyqtSlot(str, bool)
    def search(self, text, caseSensitive):
        """ Search for `text` in the table. """
        if not text:
            # if empty search string, make sure all rows are visible and 
            # return from this method
            for idx in range(self.widget.count):
                item = self.widget.item(idx)
                item.setHidden(False)
            return None
        
        if not caseSensitive:
            text = text.lower()

        for idx in range(self.widget.count):
            item = self.widget.item(idx)
            itemText = item.text()
            hideRow = True
            if not caseSensitive:
                itemText = itemText.lower()
            if text in itemText:
                hideRow = False
            if hideRow:
                item.setHidden(True)
            elif item.isHidden():
                item.setHidden(False)
    
        