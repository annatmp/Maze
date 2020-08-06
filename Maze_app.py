import sys

from PyQt5.QtWidgets import QApplication

from maze import Maze
from view import View
from Maze_Controller import Controller

if __name__ == '__main__':
    app = QApplication(sys.argv)
    GUI = Controller()

    sys.exit(app.exec_())
