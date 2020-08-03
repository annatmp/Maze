from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from maze import Maze

# Colour palette
MAIN_BACKGROUND = QColor("#F2E9E4")
PURPLE = QColor("#713E5A")
TURQUOISE = QColor("#2292A4")
DARK_GREY = QColor("#2A2C24")


class Controller(QObject):

    def __init__(self):
        super(Controller, self).__init__()
        self.main = View()
        self.load_main_screen()

    def load_main_screen(self):
        landing_screen = LandingScreen(self.main, self)
        self.main.change_screen(landing_screen)

    def generate_maze(self):
        generation_mode = self.option_screen.get_selected_generation()
        solving_strategy = self.option_screen.get_selected_solving()
        height, width = self.option_screen.get_selected_size()

        maze = Maze(height, width, generation_mode, solving_strategy)

        main_game_screen = MainGameScreen(self.main, maze, self)
        self.main.change_screen(main_game_screen)

    def continue_after_landing_screen(self):
        self.option_screen = MazePropertiesSelection(self.main, self)
        self.main.change_screen(self.option_screen)

    def start_solving(self):
        pass


class View(QMainWindow):

    def __init__(self):
        super(View, self).__init__()

        self.minimum_size = QSize(650, 700)
        self.setWindowTitle("A-Maze-ing")
        self.setWindowIcon(QIcon('assets/maze.png'))

        self.setMinimumSize(self.minimum_size)
        self.show()

    def change_screen(self, screen: QWidget):
        self.setCentralWidget(screen)
        self.update()


class LandingScreen(QWidget):

    def __init__(self, parent, controller: Controller):
        super(LandingScreen, self).__init__(parent)

        self.parent = parent
        self.controller = controller
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
        self.start_button.clicked.connect(self.controller.continue_after_landing_screen)
        self.layout.addWidget(self.start_button, alignment=Qt.AlignCenter)

        self.setLayout(self.layout)
        self.colour_styling()
        self.show()

    def colour_styling(self):
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QPalette.Window, MAIN_BACKGROUND)
        self.setPalette(palette)


class MazeScreenHeader(QWidget):
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

        super(MazeScreenHeader, self).__init__(parent)
        self.parent = parent

        self.generation_mode = QLabel(generation_mode)

        if search_mode:
            self.search_mode = QLabel(search_mode)
        # Default
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
        self.setMinimumWidth(int(self.parent.size().width() * 0.8))


class MazePropertiesSelection(QWidget):

    def __init__(self, parent: QWidget, controller: Controller):
        super(MazePropertiesSelection, self).__init__(parent)
        self.parent = parent
        self.controller = controller
        self.no_solving_option_string = "No Solving, just generate"

        generation_options = Maze.GENERATION_ALGORITHMS
        solving_options = Maze.SOLVING_ALGORITHMS
        solving_options.append(self.no_solving_option_string)

        self.generation_dropdown = OptionDropdown(self, generation_options)
        self.solving_dropdown = OptionDropdown(self, solving_options)

        self.height_selector = QSpinBox()
        self.width_selector = QSpinBox()

        for size_selector in [self.height_selector, self.width_selector]:
            size_selector.setMinimum(5)
            size_selector.setMaximum(Maze.SIZE_LIMIT)

        choose_generation_label = QLabel("Please choose an algorithm for generating the maze.")
        choose_solving_label = QLabel("Please choose an algorithm for solving the maze. Choose None if you "
                                      "only want to generate a maze")

        choose_size_label = QLabel("Please choose a width and height for the maze.")
        width_label = QLabel("Width:")
        height_label = QLabel("Height:")

        for label in [choose_generation_label, choose_solving_label, choose_size_label]:
            label.setWordWrap(True)

        layout = QGridLayout()

        size_selection_layout = QGridLayout()
        size_selection_layout.addWidget(choose_size_label, 0, 0, 1, 2, Qt.AlignCenter)
        size_selection_layout.addWidget(width_label, 1, 0)
        size_selection_layout.addWidget(self.width_selector, 2, 0)
        size_selection_layout.addWidget(height_label, 1, 1)
        size_selection_layout.addWidget(self.height_selector, 2, 1)

        generation_layout = QVBoxLayout()
        generation_layout.addWidget(choose_generation_label)
        generation_layout.addWidget(self.generation_dropdown)

        solving_layout = QVBoxLayout()
        solving_layout.addWidget(choose_solving_label)
        solving_layout.addWidget(self.solving_dropdown)

        confirm_button = QPushButton("Start")
        confirm_button.clicked.connect(self.controller.generate_maze)

        layout.addItem(generation_layout, 0, 0)
        layout.addItem(solving_layout, 0, 1)
        layout.addItem(size_selection_layout, 1, 0, 1, 2)
        layout.addWidget(confirm_button, 2, 2, Qt.AlignLeft)

        self.setLayout(layout)

    def get_selected_generation(self):

        return self.generation_dropdown.currentText()

    def get_selected_solving(self):

        selected_solving = self.solving_dropdown.currentText()

        if selected_solving == self.no_solving_option_string:
            selected_solving = False

        return selected_solving

    def get_selected_size(self):
        return self.height_selector.value(), self.width_selector.value()


class OptionDropdown(QComboBox):

    def __init__(self, parent, options):
        super(QComboBox, self).__init__(parent)
        self.parent = parent

        self.addItems(options)

    def styling(self):
        pass

class MainGameScreen(QWidget):

    def __init__(self, parent: QMainWindow, maze, controller: Controller):
        """

        :type parent: QMainWindow
        """
        super(MainGameScreen, self).__init__(parent)
        self.maze = maze
        self.parent = parent
        self.controller = controller
        self.min_size = QSize(600, 600)

        # Generate children widgets'

        self.maze_canvas = MazeCanvas(self, maze)

        # Return home button
        self.return_to_home = QPushButton("Return to home screen")
        self.return_to_home.adjustSize()
        self.return_to_home.clicked.connect(self.controller.load_main_screen)

        self.info_header = MazeScreenHeader(self, maze.get_mode_as_nice_string(), maze.get_path_length(), False)

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
        palette.setColor(QPalette.Window, MAIN_BACKGROUND)
        self.setPalette(palette)

    def resizeEvent(self, a0: QResizeEvent) -> None:
        self.layout.setAlignment(self.info_header, Qt.AlignCenter)
        self.setMinimumSize(int(self.parent.size().width() * 0.8), int(self.parent.size().height() * 0.8))
        self.maze_canvas.resizeEvent(a0)

class MazeCanvas(QLabel):

    def __init__(self, parent, maze):
        super(MazeCanvas, self).__init__(parent)

        self.parent = parent
        self.THICKNESS = 3

        self.scale_factor = 20  # once cell equals 20 pixel
        self.scale = lambda x: x * self.scale_factor

        self.maze = maze
        self.maze_size = maze.get_size()

        maze_canvas = QPixmap(self.scale(self.maze_size[0]), self.scale(self.maze_size[1]))
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




        # draw end point



        painter.setBrush(QBrush(QColor(DARK_GREY), Qt.SolidPattern))
        end_pen = QPen(QColor(DARK_GREY), 3, Qt.SolidLine)
        end_pen.setCapStyle(Qt.FlatCap)
        painter.setPen(end_pen)

        end_pos = self.maze.get_end().get_position()

        end_top_left = QPoint(self.scale(end_pos[0]+0.25), self.scale(end_pos[1]+0.25))
        end_bottom_right = QPoint(self.scale(end_pos[0] + 0.75), self.scale(end_pos[1]+ 0.75))

        end = QRect(end_top_left, end_bottom_right)

        painter.drawEllipse(end)

        # draw start point

        painter.setBrush(QBrush(QColor(MAIN_BACKGROUND), Qt.SolidPattern))
        start_pen = QPen(QColor(MAIN_BACKGROUND), 3, Qt.SolidLine)
        start_pen.setCapStyle(Qt.SquareCap)
        painter.setPen(start_pen)

        start_pos = self.maze.get_start().get_position()

        start_top_left = QPoint(self.scale(start_pos[0] + 0.25), self.scale(start_pos[1] + 0.25))
        start_bottom_right = QPoint(self.scale(start_pos[0] + 0.75), self.scale(start_pos[1] + 0.75))

        start = QRect(start_top_left, start_bottom_right)

        painter.drawEllipse(start)
