from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from maze import Maze

import sys

# Colour palette
MAIN_BACKGROUND = QColor("#F2E9E4")
PURPLE = QColor("#713E5A")
TURQUOISE = QColor("#2292A4")
DARK_GREY = QColor("#2A2C24")


class View(QMainWindow):

    def __init__(self, maze):
        super(View, self).__init__()

        self.minimum_size = QSize(650, 700)
        self.setWindowTitle("A-Maze-ing")
        self.setWindowIcon(QIcon('assets/maze.png'))

        self.maze = maze
        landing_screen = Landing_Screen(self)

        self.setCentralWidget(landing_screen)
        self.setMinimumSize(self.minimum_size)
        self.show()

    def load_maze(self):
        main_game_screen = Main_Game_Screen(self, self.maze)
        self.setCentralWidget(main_game_screen)
        self.update()

    def load_main_screen(self):
        landing_screen = Landing_Screen(self)
        self.setCentralWidget(landing_screen)
        self.update()


class Landing_Screen(QWidget):

    def __init__(self, parent):
        super(Landing_Screen, self).__init__(parent)

        self.parent = parent
        self.layout = QVBoxLayout(self)

        # Title
        self.title_label = QLabel()
        self.title_label.setText("aMAZEing!")
        self.layout.addWidget(self.title_label, alignment=Qt.AlignCenter)

        # Generate Logo
        self.logo = QLabel()
        logo_pixmap = QPixmap("assets/maze.png")
        self.logo.setPixmap(logo_pixmap)
        self.layout.addWidget(self.logo, alignment=Qt.AlignCenter)

        # start button
        self.start_button = QPushButton(self)
        self.start_button.setText("Start")
        self.start_button.clicked.connect(self.parent.load_maze)
        self.layout.addWidget(self.start_button, alignment=Qt.AlignCenter)

        self.setLayout(self.layout)
        self.colour_styling()
        self.show()

    def colour_styling(self):
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QPalette.Window,MAIN_BACKGROUND)
        self.setPalette(palette)


class Main_Game_Screen(QWidget):

    def __init__(self, parent: QMainWindow, maze):
        """

        :type parent: QMainWindow
        """
        super(Main_Game_Screen, self).__init__(parent)
        self.maze = maze
        self.parent = parent

        self.min_size = QSize(600, 600)

        #Generate children widgets'

        self.maze_canvas = Maze_Canvas(self, maze)

        # Return home button
        self.return_to_home = QPushButton("Return to Homescreen")
        self.return_to_home.adjustSize()
        self.return_to_home.clicked.connect(self.parent.load_main_screen)

        self.info_header = Maze_Screen_Header(self, maze.get_mode_as_nice_string(), maze.get_path_length(), False)

        self.layout = QGridLayout()
        self.layout.addWidget(self.info_header, 0, 0, 1, 3)
        self.layout.addWidget(self.maze_canvas, 1, 0, 1, 3, Qt.AlignCenter)
        self.layout.addWidget(self.return_to_home, 2, 1, Qt.AlignCenter)
        self.setLayout(self.layout)


        self.colour_styling()
        self.adjustSize()

        self.show()

    def colour_styling(self):
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QPalette.Window,MAIN_BACKGROUND)
        self.setPalette(palette)

    def resizeEvent(self, a0: QResizeEvent) -> None:

        self.layout.setAlignment(self.info_header, Qt.AlignCenter)
        self.setMinimumSize(int(self.parent.size().width()*0.8), int(self.parent.size().height()*0.8))
        self.maze_canvas.resizeEvent(a0)


class Maze_Screen_Header(QWidget):
    """
    Header to be displayed above the maze. Gives basic information about the generated maze
    Info is pulled from maze directly
    """

    def __init__(self, parent, generation_mode, path_length, search_mode=False):
        """

        :param parent:
        :param generation_mode: of the maze
        :param path_length: path length from start to end
        :param search_mode: used to generate maze
        """

        super(Maze_Screen_Header, self).__init__(parent)
        self.parent = parent

        self.generation_mode = QLabel(generation_mode)

        if search_mode:
            self.search_mode = QLabel(search_mode)
        #Default
        else:
            self.search_mode = QLabel("No search mode selected")


        self.path_length = QLabel("Path Length: {}".format(path_length))

        self.layout = QGridLayout()
        self.layout.addWidget(self.generation_mode, 0, 0, Qt.AlignLeft)
        self.layout.addWidget(self.search_mode, 0, 1)
        self.layout.addWidget(self.path_length, 0, 2, Qt.AlignRight)

        self.adjustSize()
        self.setLayout(self.layout)
        self.show()

    def resizeEvent(self, a0: QResizeEvent) -> None:
        self.layout.setAlignment(self.search_mode, Qt.AlignCenter)
        self.setMinimumWidth(int(self.parent.size().width()*0.8))


class Maze_Canvas(QLabel):

    def __init__(self, parent, maze):
        super(Maze_Canvas, self).__init__(parent)

        self.parent = parent
        self.THICKNESS = 3

        self.scale_factor = 20 # once cell equals 20 pixel
        self.scale = lambda x: x * self.scale_factor

        self.maze = maze
        self.maze_size = maze.get_size()

        maze_canvas = QPixmap(self.scale(self.maze_size[0]), self.scale(self.maze_size[0]))
        maze_canvas.fill(PURPLE)

        self.setPixmap(maze_canvas)

        self.setFrameShape(QFrame.Box)
        self.setLineWidth(self.THICKNESS)
        self.adjustSize()
        self.draw_maze()
        self.show()

    def draw_maze(self):

        cells = self.maze.get_cells()

        lines = []  # store all lines in a queue before drawing

        painter = QPainter(self.pixmap())
        pen = QPen()
        pen.setWidth(3)
        pen.setCapStyle(Qt.RoundCap)
        pen.setColor(MAIN_BACKGROUND)
        painter.setPen(pen)

        for row_index, row in enumerate(cells):

            for cell in row:

                cell_pos = cell.get_position()
                top_left = QPoint(self.scale(cell_pos[0]), self.scale(cell_pos[1]))
                top_right = QPoint(self.scale(cell_pos[0] + 1), self.scale(cell_pos[1]))
                bottom_left = QPoint(self.scale(cell_pos[0]), self.scale(cell_pos[1] + 1))
                bottom_right = QPoint(self.scale(cell_pos[0] + 1), self.scale(cell_pos[1] + 1))

                walls = cell.get_walls()

                if walls['T']:
                    top_line = QLine(top_left, top_right)
                    lines.append(top_line)
                    painter.drawLine(top_line)

                if walls['B']:
                    bottom_line = QLine(bottom_left, bottom_right)
                    lines.append(bottom_line)
                    painter.drawLine(bottom_line)

                if walls['R']:
                    right_line = QLine(bottom_right, top_right)
                    lines.append(right_line)
                    painter.drawLine(right_line)

                if walls['L']:
                    left_line = QLine(bottom_left, top_left)
                    lines.append(left_line)
                    painter.drawLine(left_line)

        # draw start point
        start_pos = self.maze.get_start().get_position()

        start_top_left = QPoint(self.scale(start_pos[0]) + 2, self.scale(start_pos[1]) + 2)
        start_bottom_right = QPoint(self.scale(start_pos[0] + 1) - 2, self.scale(start_pos[1] + 1) - 2)

        rect = QRect(start_top_left, start_bottom_right)
        start = QPixmap("assets/streetview.png")

        painter.drawPixmap(rect, start)

        # draw end point
        end_pos = self.maze.get_end().get_position()

        end_top_left = QPoint(self.scale(end_pos[0]) + 5, self.scale(end_pos[1]) + 5)
        end_bottom_right = QPoint(self.scale(end_pos[0] + 1) - 5, self.scale(end_pos[1] + 1) - 5)

        rect = QRect(end_top_left, end_bottom_right)
        end = QPixmap("assets/target.png")

        painter.drawPixmap(rect, end)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    maze = Maze(30, 30, "depth_first")
    GUI = View(maze)

    sys.exit(app.exec_())
