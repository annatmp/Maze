from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from Maze import Maze
from Maze_Generation import Maze_Generator
from Maze_Walk import Maze_Walk, Visit_Status

# Colour palette
MAIN_BACKGROUND = QColor("#F7F5FA")
#WALLS = QColor("#81667A")
MAZE = QColor("#2A3035")
DEAD = QColor("#028090")
PATH_THICKNESS = 3
WALLS = QColor("#43AA8B")
WALL_THICKNESS = 3
HIGHLIGHTS = QColor("#FFC670")
HIGHLIGHT_THICKNESS = 2

class View(QMainWindow):

    def __init__(self):
        super(View, self).__init__()

        self.minimum_size = QSize(900, 900)
        self.setWindowTitle("A-Maze-ing")
        self.setWindowIcon(QIcon('assets/maze.png'))

        self.setMinimumSize(self.minimum_size)
        self.show()

    def change_screen(self, screen: QWidget):
        self.setCentralWidget(screen)
        self.update()


class LandingScreen(QWidget):

    def __init__(self, parent, controller):
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

        self.generation_mode = QLabel("Generation: {}".format(generation_mode))

        if search_mode:
            self.search_mode = QLabel("Solving: {}".format(search_mode))
        # Default
        else:
            self.search_mode = QLabel("No solving mode selected")

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

    def __init__(self, parent: QWidget, controller):
        super(MazePropertiesSelection, self).__init__(parent)
        self.parent = parent
        self.controller = controller
        self.no_solving_option_string = "No Solving, just generate"

        generation_options = Maze.GENERATION_ALGORITHMS
        solving_options = list(Maze_Generator.solving_mode.keys())
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

        self.colour_styling()
        self.setLayout(layout)


    def colour_styling(self):
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QPalette.Window, MAIN_BACKGROUND)
        self.setPalette(palette)

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

    def __init__(self, parent: QMainWindow, controller, mode,solving_strategy):
        """

        :type parent: QMainWindow
        """
        super(MainGameScreen, self).__init__(parent)
        maze = controller.maze
        self.parent = parent
        self.controller = controller
        self.min_size = QSize(600, 600)

        # Generate children widgets'
        # check which maze mode to draw:
        if mode == "solution":
            self.maze_canvas = MazeWithSolutionCanvas(self, controller.maze, controller.solution)
        else:
            self.maze_canvas = MazeOnlyCanvas(self, controller.maze)

        # Return home button
        self.return_to_home = QPushButton("Return to home screen")
        self.return_to_home.adjustSize()
        self.return_to_home.clicked.connect(self.controller.load_main_screen)

        self.info_header = MazeScreenHeader(self, maze.get_mode_as_nice_string(), maze.get_path_length(),
                                            solving_strategy)

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


class MazeOnlyCanvas(QGraphicsView):

    def __init__(self, parent, maze):
        super(MazeOnlyCanvas, self).__init__(parent)

        self.scale_factor = 25  # once cell equals 20 pixel
        self.scale = lambda x: x * self.scale_factor

        self.maze = maze
        self.maze_size = maze.get_size()

        self.graph = QGraphicsScene()
        self.setScene(self.graph)

        self.draw_maze()

        print(self.graph.height(),self.graph.width())
        self.show()

    def draw_maze(self):

        self.draw_walls()
        self.draw_start()
        self.draw_end()

        self.draw_background()

    def draw_background(self):
        background_brush = QBrush(MAZE, Qt.SolidPattern)
        self.setBackgroundBrush(background_brush)
        self.update()

    def draw_start(self):
        start_pen = QPen(HIGHLIGHTS,Qt.RoundCap)
        brush = QBrush(HIGHLIGHTS,Qt.SolidPattern)
        start_pen.setWidth(HIGHLIGHT_THICKNESS)
        self.draw_ellipse_around_point(self.maze.get_start_position(), start_pen,brush)

    def draw_end(self):
        end_pen = QPen(HIGHLIGHTS,Qt.RoundCap)
        end_pen.setBrush(QBrush(HIGHLIGHTS,Qt.SolidPattern))
        end_pen.setWidth(HIGHLIGHT_THICKNESS)
        self.draw_ellipse_around_point(self.maze.get_end_position(), end_pen)

    def draw_ellipse_around_point(self, point, pen, brush=False):

        point_top = QPointF(self.scale(point[0] + 0.3), self.scale(point[1] + 0.3))
        point_end = QPointF(self.scale(point[0] + 0.7), self.scale(point[1] + 0.7))
        rect = QRectF(point_top, point_end)
        if brush:
            self.graph.addEllipse(rect, pen,brush)
        else:
            self.graph.addEllipse(rect,pen)

    def get_cell_center_point(self, cell):
        """
        returns a QPoint in the center of the cell
        :param cell:
        :return:
        """
        cell_pos = cell.get_position()
        center_point = QPoint(self.scale(cell_pos[0] + 0.5), self.scale(cell_pos[1] + 0.5))
        return center_point

    def draw_walls(self):
        wall_pen = QPen()
        wall_pen.setColor(QColor(WALLS))
        wall_pen.setWidth(WALL_THICKNESS)

        cells = self.maze.get_cells()

        for row_index, row in enumerate(cells):

            for cell in row:

                cell_pos = cell.get_position()
                top_left = QPoint(self.scale(cell_pos[0]), self.scale(cell_pos[1]))
                top_right = QPoint(self.scale(cell_pos[0] + 1), self.scale(cell_pos[1]))
                bottom_left = QPoint(self.scale(cell_pos[0]), self.scale(cell_pos[1] + 1))
                bottom_right = QPoint(self.scale(cell_pos[0] + 1), self.scale(cell_pos[1] + 1))

                walls = cell.get_walls()

                if walls['T']:
                    top_line = QLineF(top_left, top_right)
                    self.graph.addLine(top_line, wall_pen)

                if walls['B']:
                    bottom_line = QLineF(bottom_left, bottom_right)
                    self.graph.addLine(bottom_line, wall_pen)

                if walls['R']:
                    right_line = QLineF(bottom_right, top_right)
                    self.graph.addLine(right_line, wall_pen)

                if walls['L']:
                    left_line = QLineF(bottom_left, top_left)
                    self.graph.addLine(left_line, wall_pen)


class MazeWithSolutionCanvas(MazeOnlyCanvas):
    # pen for dead ends
    dead_pen = QPen()
    dead_pen.setWidth(PATH_THICKNESS)
    dead_pen.setCapStyle(Qt.RoundCap)
    dead_pen.setColor(QColor(DEAD))

    # pen settings for the valid path
    alive_pen = QPen()
    alive_pen.setWidth(PATH_THICKNESS)
    alive_pen.setCapStyle(Qt.RoundCap)
    alive_pen.setColor(QColor(MAIN_BACKGROUND))


    def __init__(self, parent, maze, solution):
        super(MazeWithSolutionCanvas, self).__init__(parent, maze)
        self.maze_solution = solution

        # get the starting point for the maze
        self.current = QPoint(self.scale(0.5), self.scale(0.5))
        self.cells = []

    def draw_next_line(self, cell):

        next_cell = cell[Maze_Walk.CELL]
        next_status = cell[Maze_Walk.STATUS]
        next_point = self.get_cell_center_point(next_cell)

        if next_status == Visit_Status.DEAD:
            line = QGraphicsLineItem(QLineF(self.current, next_point))
            line.setPen(self.dead_pen)

        elif next_status == Visit_Status.JUNCTION:
            line = QGraphicsLineItem(QLineF(self.current, next_point))
            line.setPen(self.dead_pen)

        else:
            line = QGraphicsLineItem(QLineF(self.current, next_point))
            line.setPen(self.alive_pen)

        self.graph.addItem(line)

        self.current = next_point

        self.update()
