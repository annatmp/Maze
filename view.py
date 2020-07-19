from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from maze import Maze

import sys

class View(QMainWindow):

    def __init__(self,maze):
        super(View, self).__init__()


        self.setWindowTitle("A-Maze-ing")
        self.setWindowIcon(QIcon('assets/maze.png'))

        self.maze = maze
        self.landing_screen = Landing_Screen(self)
        self.setCentralWidget(self.landing_screen)



        self.show()


    def load_maze(self):

        self.main_game_screen = Main_Game_Screen(self,self.maze)
        self.setCentralWidget(self.main_game_screen)
        self.update()


class Landing_Screen(QWidget):

    def __init__(self, parent):
        super(Landing_Screen, self).__init__(parent)

        self.parent = parent
        self.layout = QVBoxLayout(self)

        #Title
        self.title_label = QLabel()
        self.title_label.setText("aMAZEing!")
        self.layout.addWidget(self.title_label,alignment=Qt.AlignCenter)

        # Generate Logo
        self.logo = QLabel()
        logo_pixmap = QPixmap("assets/maze.png")
        self.logo.setPixmap(logo_pixmap)
        self.layout.addWidget(self.logo,alignment=Qt.AlignCenter)


        # start button
        self.start_button = QPushButton(self)
        self.start_button.setText("Start")
        self.start_button.clicked.connect(self.parent.load_maze)
        self.layout.addWidget(self.start_button,alignment=Qt.AlignCenter)

        self.setLayout(self.layout)
        self.show()

class Main_Game_Screen(QWidget):

    def __init__(self,parent:QMainWindow,maze):
        """

        :type parent: QMainWindow
        """
        super(Main_Game_Screen, self).__init__(parent)
        self.canvas = Maze_Canvas(self,maze)
        self.layout = QHBoxLayout()
        self.setLayout(self.layout)
        self.layout.addWidget(self.canvas,Qt.AlignCenter)


        self.show()

class Maze_Canvas(QLabel):

    def __init__(self,parent, maze):
        super(Maze_Canvas, self).__init__(parent)
        self.THICKNESS = 3

        self.scale_factor = 20
        self.scale = lambda x: x*self.scale_factor


        self.maze = maze
        self.maze_size = maze.get_size()


        canvas = QPixmap(self.scale(self.maze_size[0]),self.scale(self.maze_size[0]))
        canvas.fill(QColor("#FFF5F0"))

        self.setPixmap(canvas)

        self.setFrameShape(QFrame.Box)
        self.setLineWidth(self.THICKNESS)

        self.draw_maze()
        self.show()

    def draw_maze(self):

        cells = self.maze.get_cells()

        lines = [] # store all lines in a queue before drawing

        painter = QPainter(self.pixmap())
        pen = QPen()
        pen.setWidth(3)
        pen.setCapStyle(Qt.RoundCap)
        pen.setColor(QColor('#713e5a'))
        painter.setPen(pen)

        for row_index, row in enumerate(cells):

            for cell in row:

                cell_pos = cell.get_position()
                top_left = QPoint(self.scale(cell_pos[0]),self.scale(cell_pos[1]))
                top_right = QPoint(self.scale(cell_pos[0]+1), self.scale(cell_pos[1]))
                bottom_left = QPoint(self.scale(cell_pos[0]), self.scale(cell_pos[1]+1))
                bottom_right = QPoint(self.scale(cell_pos[0]+1), self.scale(cell_pos[1] + 1))

                walls = cell.get_walls()

                if walls['T']:
                    top_line = QLine(top_left,top_right)
                    lines.append(top_line)
                    painter.drawLine(top_line)

                if walls['B']:
                    bottom_line = QLine(bottom_left,bottom_right)
                    lines.append(bottom_line)
                    painter.drawLine(bottom_line)

                if walls['R']:
                    right_line = QLine(bottom_right,top_right)
                    lines.append(right_line)
                    painter.drawLine(right_line)

                if walls['L']:
                    left_line = QLine(bottom_left,top_left)
                    lines.append(left_line)
                    painter.drawLine(left_line)


        # start point
        start_pos = self.maze.get_start().get_position()

        start_top_left = QPoint(self.scale(start_pos[0])+2, self.scale(start_pos[1])+2)
        start_bottom_right = QPoint(self.scale(start_pos[0] + 1)-2, self.scale(start_pos[1] + 1)-2)

        rect = QRect(start_top_left,start_bottom_right)
        start = QPixmap("assets/streetview.png")

        painter.drawPixmap(rect,start)

        # end point
        end_pos = self.maze.get_end().get_position()

        end_top_left = QPoint(self.scale(end_pos[0]) + 5, self.scale(end_pos[1]) + 5)
        end_bottom_right = QPoint(self.scale(end_pos[0] + 1) - 5, self.scale(end_pos[1] + 1) - 5)

        rect = QRect(end_top_left, end_bottom_right)
        end = QPixmap("assets/target.png")

        painter.drawPixmap(rect,end)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    maze = Maze(35, 35, "depth_first")
    maze.print()
    GUI = View(maze)

    sys.exit(app.exec_())