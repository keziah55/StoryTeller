#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 23 18:00:04 2020

@author: keziah
"""
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem
from PyQt5.QtCore import Qt

class TableWidget(QTableWidget):
    """ More Pythonic version of QTableWidget.
    
        Parameters
        ----------
        headerLabels : list 
            List of column headerLabelss. (Can provide `column` instead.)
        columns : int
            Number of columns. (Only required if `headerLabels` is not provided.)
        showRowNumbers : bool
            If True (default behaviour), row numbers will be shown.
        clickHeaderLabelsToSort : bool
            Sort table when headerLabels clicked.
        readOnly : bool
            If True, the whole table will be read-only. Default is False.
        parent : QObject, optional
            Parent object
    """
    
    def __init__(self, headerLabels=None, columns=None, showRowNumbers=True, 
                 clickHeaderLabelsToSort=True, readOnly=False, parent=None):
        if headerLabels is None and columns is None:
            msg = "TableWidget needs either `headerLabels` or `columns` arg."
            raise ValueError(msg)
        
        if headerLabels is not None and columns is not None:
            msg = "TableWidget needs either `headerLabels` or `columns` arg, not both."
            raise ValueError(msg)
            
        if columns is None:
            columns = len(headerLabels)
        rows = 0
        
        super().__init__(rows, columns, parent)
        
        if headerLabels is not None:
            self.setHorizontalHeaderLabels(headerLabels)
        else:
            headerLabels = list(range(columns))
        self.headerLabels = headerLabels
        
        self.verticalHeader().setVisible(showRowNumbers)
        
        self.columnSort = dict(zip(self.headerLabels, [None]*len(self.headerLabels)))
        self.setClickHeaderLabelsToSort(clickHeaderLabelsToSort)
        
        self.flags = Qt.ItemIsEnabled|Qt.ItemIsSelectable if readOnly else Qt.ItemIsEnabled|Qt.ItemIsEditable

        
    @property
    def rowCount(self):
        return super().rowCount()
    
    @property
    def columnCount(self):
        return super().columnCount()
    
    @property
    def header(self):
        return super().horizontalHeader()
    
    def getRow(self, idx):
        """ Return list of values in row `idx`. """
        row = []
        for col in range(self.columnCount):
            item = self.item(idx, col)
            row.append(item.text())
        return row
    
    def getColumn(self, name):
        """ Return list of values in column `name`. """
        column = []
        idx = self.headerLabels.index(name)
        for row in range(self.rowCount):
            item = self.item(row, idx)
            column.append(item.text())
        return column
        
    def addRow(self, *args):
        """ Add row to the table.
        
            Supply either the values to be added, in order, or a dict, where 
            the keys correspond to header strings.
        """
        if isinstance(args, (tuple, list)):
            args = dict(zip(self.headerLabels, args))
        elif isinstance(args[0], dict):
            args = args[0]
        else:
            msg = f"Could not add item of type {type(args)} to TableWidget."
            raise TypeError(msg)
            
        row = self.rowCount
        self.insertRow(row)
        
        for n, key in enumerate(self.headerLabels):
            item = QTableWidgetItem(str(args[key]))
            item.setFlags(self.flags)
            self.setItem(row, n, item)
            
    def currentValue(self, column):
        """ Return the value of the given column in the currently selected row. """
        row = super().currentRow()
        col = self.headerLabels.index(column)
        item = self.item(row, col)
        return item.text()
    
    @property 
    def currentRow(self):
        """ Return dict of column name:value pairs for the currently selected row. """
        row = {name:self.currentValue(name) for name in self.headerLabels}
        return row
        
    def sort(self, column, order=None):
        if isinstance(column, int):
            column = self.headerLabels[column]
        if order is None:
            if self.columnSort[column] is None or self.columnSort[column]==Qt.DescendingOrder:
                order = Qt.AscendingOrder
            else:
                order = Qt.DescendingOrder
        idx = self.headerLabels.index(column)
        self.sortItems(idx, order)
        self.columnSort[column] = order
        
    def setClickHeaderLabelsToSort(self, value):
        # don't want multiple connections, so always disconnect and only 
        # reconnect if required
        try:
            self.header.sectionClicked.disconnect(self.sort)
        except TypeError:
            pass
        if value:
            self.header.setSectionsClickable(True)
            self.header.setSortIndicatorShown(True)
            self.header.sectionClicked.connect(self.sort)