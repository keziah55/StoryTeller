#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 27 15:49:13 2020

@author: keziah
"""

from abc import ABCMeta
from PyQt5.QtCore import QObject

class PyQtMetaclass(type(QObject), ABCMeta):
    pass
