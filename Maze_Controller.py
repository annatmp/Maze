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

    def load_main_screen(self):
        landing_screen = LandingScreen(self.main, self)
        self.main.change_screen(landing_screen)

    def generate_maze(self):
        generation_mode = self.option_screen.get_selected_generation()
        solving_strategy = self.option_screen.get_selected_solving()
        height, width = self.option_screen.get_selected_size()

        maze_generator = Maze_Generation.Maze_Generator(height, width, generation_mode, solving_strategy)
        maze = maze_generator.get_maze()

        main_game_screen = MainGameScreen(self.main, maze, self)
        self.main.change_screen(main_game_screen)

    def continue_after_landing_screen(self):
        self.option_screen = MazePropertiesSelection(self.main, self)
        self.main.change_screen(self.option_screen)

    def start_solving(self):
        pass