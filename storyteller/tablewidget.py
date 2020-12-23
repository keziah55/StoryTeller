#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 23 18:00:04 2020

@author: keziah
"""
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem

class TableWidget(QTableWidget):
    """ More Pythonic version of QTableWidget.
    
        Parameters
        ----------
        header : list 
            List of column headers. (Can provide `column` instead.)
        columns : int
            Number of columns. (Only required if `header` is not provided.)
        showRowNumbers : bool
            If True (default behaviour), row numbers will be shown.
        parent : QObject, optional
            Parent object
    """
    
    def __init__(self, header=None, columns=None, showRowNumbers=True, 
                 parent=None):
        if header is None and columns is None:
            msg = "TableWidget needs either `header` or `columns` arg."
            raise ValueError(msg)
        
        if header is not None and columns is not None:
            msg = "TableWidget needs either `header` or `columns` arg, not both."
            raise ValueError(msg)
            
        if columns is None:
            columns = len(header)
        rows = 0
        
        super().__init__(rows, columns, parent)
        
        if header is not None:
            self.setHorizontalHeaderLabels(header)
        else:
            header = list(range(columns))
        self.header = header
        
        self.verticalHeader().setVisible(showRowNumbers)

        
    @property
    def rowCount(self):
        return super().rowCount()
    
    @property
    def columnCount(self):
        return super().columnCount()
        
    def addRow(self, *args):
        """ Add row to the table.
        
            Supply either the values to be added, in order, or a dict, where 
            the keys correspond to header strings.
        """
        if isinstance(args, (tuple, list)):
            args = dict(zip(self.header, args))
        elif isinstance(args[0], dict):
            args = args[0]
        else:
            msg = f"Could not add item of type {type(args)} to TableWidget."
            raise TypeError(msg)
            
        row = self.rowCount
        self.insertRow(row)
        
        for n, key in enumerate(self.header):
            item = QTableWidgetItem(str(args[key]))
            self.setItem(row, n, item)
            
    def currentValue(self, column):
        """ Return the value of the given column in the currently selected row. """
        row = self.currentRow()
        col = self.header.index(column)
        item = self.item(row, col)
        return item.text()
        