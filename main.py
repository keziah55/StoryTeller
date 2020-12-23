#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import QApplication
from storyteller import StoryTeller

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = StoryTeller()
    sys.exit(app.exec_())