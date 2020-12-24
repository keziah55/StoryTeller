#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 22 16:45:48 2020

@author: keziah
"""

import os
import re
from datetime import date

from PyQt5.QtGui import QFontDatabase, QIcon, QKeySequence
from PyQt5.QtWidgets import (QAction, QComboBox, QDesktopWidget, 
                             QLineEdit, QMainWindow, QWidget, QVBoxLayout) 
from PyQt5.QtCore import pyqtSlot, Qt

from .dialogs import OpenStoryDialog
from .editor import StoryEditor
from .countlabel import WordCountLabel

# TODO list
# list of titles
# new story
# make database of stories 
## title, date created, date(s) modified, word count, goal
# text formatting (bold, italic, font, size)
## write to plain text; generally use the database to access


class StoryTeller(QMainWindow):
    
    def __init__(self):
        super().__init__()
        
        self.goal = 100
        
        user = os.path.expanduser('~')
        self.savePath = os.path.join(user, 'Documents', 'stories')
        
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
        
        self.fontDB = QFontDatabase()
        
        self.createActions()
        self.createMenus()
        self.createToolBars()
        self.connectActions()
        
        self.setWindowTitle("Story Teller")
        self.resize(700,600)
        self.centre()
        self.show()
        
    def centre(self):
        """ Centre window on screen. """
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
        
    @pyqtSlot(int)
    def setFontFamily(self, idx):
        # TODO set on highlighted text
        family = self.fontFamilies[idx]
        for widget in [self.title, self.textEdit]:
            font = widget.font()
            font.setFamily(family)
            widget.setFont(font)
    
    @pyqtSlot(int)
    def setFontSize(self, idx):
        # TODO set on highlighted text
        size = self.sizes[idx]
        for widget in [self.title, self.textEdit]:
            font = widget.font()
            font.setPointSize(size)
            widget.setFont(font)
    
    @pyqtSlot()
    def saveStory(self):
        today = date.today().strftime("%Y-%m-%d")
        filename = f"{today} {self.title.text()}.html"
        path = os.path.join(self.savePath, filename)
        
        text = f"<h1>{self.title.text()}</h1>" + self.textEdit.toHtml()
        
        with open(path, 'w') as fileobj:
            fileobj.write(text)
    
    @pyqtSlot()
    def openStory(self):
        diag = OpenStoryDialog(self.savePath)
        result = diag.execDialog()
        if result:
            self._openFile(diag.story)
        
    @pyqtSlot(str)
    def _openFile(self, filename):
        # strip extension and date from title
        title, _ = os.path.splitext(filename)
        title = re.sub(r"\d{4}-\d{2}-\d{2} ", "", title)
        self.title.setText(title)
        
        # set text
        path = os.path.join(self.savePath, filename)
        with open(path) as fileobj:
            text = fileobj.read()
        self.textEdit.setHtml(text)
        
            
    def createActions(self):
        
        self.saveAct = QAction(QIcon.fromTheme('document-save'), "&Save", self,
                               shortcut=QKeySequence.Save,
                               statusTip="Save the story", triggered=self.saveStory)
        
        self.openAct = QAction(QIcon.fromTheme('document-open'), "&Open", self,
                               shortcut=QKeySequence.Open,
                               statusTip="Open a story", triggered=self.openStory)
        
        self.exportAct = QAction(QIcon.fromTheme('text-x-generic'), "&Export", 
                                 self, statusTip="Export plain text")
        
        self.setGoalAct = QAction(QIcon.fromTheme('insert-text'),
                                  "Set the word count goal", self)

        self.exitAct = QAction("E&xit", self, shortcut="Ctrl+Q",
                               statusTip="Exit the application", 
                               triggered=self.close)
        
        self.boldAct = QAction(QIcon.fromTheme('format-text-bold'), "Bold", 
                               self, shortcut="Ctrl+B")
        
        self.italicAct = QAction(QIcon.fromTheme('format-text-italic'), "Italic", 
                                 self, shortcut="Ctrl+I")
        
        self.underlineAct = QAction(QIcon.fromTheme('format-text-underline'), 
                                    "Underline", 
                                    self, shortcut="Ctrl+U")
        
        self.strikeAct = QAction(QIcon.fromTheme('format-text-strikethrough'), 
                                 "Strikethrough", 
                                 self)#, shortcut="Ctrl+B")
        
        self.fontMenu = QComboBox()
        self.fontFamilies = self.fontDB.families()
        currentFont = self.textEdit.font().family()
        self.fontMenu.addItems(self.fontFamilies)
        idx = self.fontFamilies.index(currentFont)
        self.fontMenu.setCurrentIndex(idx)
        
        self.sizeMenu = QComboBox()
        self.sizes = [8, 9, 10, 11, 12, 14]
        self.sizeMenu.addItems([f"{size}pt" for size in self.sizes])
        self.defaultFontSize = 11 #self.textEdit.fontPointSize()
        idx = self.sizes.index(self.defaultFontSize)
        self.sizeMenu.setCurrentIndex(idx)
        
    def connectActions(self):
        self.fontMenu.currentIndexChanged.connect(self.setFontFamily)
        self.sizeMenu.currentIndexChanged.connect(self.setFontSize)
        
    def createMenus(self):
        self.fileMenu = self.menuBar().addMenu("&File")
        self.fileMenu.addAction(self.saveAct)
        self.fileMenu.addAction(self.openAct)
        self.fileMenu.addAction(self.exportAct)
        self.fileMenu.addSeparator();
        self.fileMenu.addAction(self.exitAct)
        

    def createToolBars(self):
        self.fileToolBar = self.addToolBar("File")
        self.fileToolBar.addAction(self.saveAct)
        self.fileToolBar.addAction(self.openAct)
        self.fileToolBar.addAction(self.setGoalAct)
        
        self.editToolBar = self.addToolBar("Edit")
        self.editToolBar.addAction(self.boldAct)
        self.editToolBar.addAction(self.italicAct)
        self.editToolBar.addAction(self.underlineAct)
        self.editToolBar.addAction(self.strikeAct)
        
        self.editToolBar.addWidget(self.fontMenu)
        self.editToolBar.addWidget(self.sizeMenu)
        