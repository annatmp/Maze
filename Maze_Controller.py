from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import Maze_Generation
from view import View,LandingScreen,MainGameScreen,MazePropertiesSelection


class Controller(QObject):

    def __init__(self):
        super(Controller, self).__init__()
        self.main = View()
        self.load_main_screen()

        self.maze = None
        self.solution = None
        self.main_game_screen = None

    def load_main_screen(self):
        landing_screen = LandingScreen(self.main, self)
        self.main.change_screen(landing_screen)

    def generate_maze(self):
        generation_mode = self.option_screen.get_selected_generation()
        solving_strategy = self.option_screen.get_selected_solving()
        height, width = self.option_screen.get_selected_size()

        maze_generator = Maze_Generation.Maze_Generator(height, width, generation_mode, solving_strategy)
        self.maze = maze_generator.get_maze()

        if solving_strategy:
            self.solution = maze_generator.solution

        mode = "solution" if self.solution else "generation"
        self.main_game_screen = MainGameScreen(self.main, self, mode,solving_strategy)
        self.main.change_screen(self.main_game_screen)


        try:
            self.timer = QTimer()
            self.timer.timeout.connect(self.draw_next_solution_step)
            self.timer.start(100)

        except StopIteration:
            pass

    def draw_next_solution_step(self):

        try:
            next = self.solution.__next__()
            self.main_game_screen.maze_canvas.draw_next_line(next)
        except :
            self.timer.stop()
            return

    def continue_after_landing_screen(self):
        self.option_screen = MazePropertiesSelection(self.main, self)
        self.main.change_screen(self.option_screen)

    def start_solving(self):
        pass