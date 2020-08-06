from enum import Enum
from collections import OrderedDict
import maze
from Maze_Exceptions import Invalid_Direction_Exception, No_Solution_Found_Exception



class Visit_Status(Enum):
    VISITED = 1
    DEAD = 2
    JUNCTION = 3
    START = 4
    END = 5


class Maze_Walk:
    CELL = "cell"
    STATUS = "status"
    DIRECTION = "direction"

    def __init__(self,start):

        self.valid_path = []
        self.path = []
        self.visited = set()
        self.current = 0

        self.path.append({self.CELL:start,
                          self.STATUS: Visit_Status.START})
        self.valid_path.append(start)

    def get_amount_valid_steps(self):
        return len(self.valid_path)

    def turn_back(self):
        """
        revert the last step by removing it from the valid_path and add to discarded
        :return:
        """
        if len(self.valid_path) == 0:

            raise No_Solution_Found_Exception("Cannot revert turn back from start position")

        del self.valid_path[-1]

        wrong_step = self.path[-1]
        new_position = self.valid_path[-1]

        self.path.append({self.CELL:wrong_step[self.CELL],
                          self.STATUS:Visit_Status.DEAD})

        self.path.append({self.CELL: new_position,
                          self.STATUS: Visit_Status.JUNCTION,
                          self.DIRECTION: maze.Maze.ADJACENT_EDGES[wrong_step[self.DIRECTION]]})



    def walk(self,obj,direction):
        """
        add an object to the path
        :param obj: next object on the path
        :param direction: direction this next cell lays as  seen from the previous one
        :return:
        """


        if not direction in maze.Maze.ADJACENT_EDGES:
            raise Invalid_Direction_Exception("{} is not a valid direction".format(direction))

        self.valid_path.append(obj)

        self.path.append({self.CELL: obj,
                         self.STATUS: Visit_Status.VISITED,
                         self.DIRECTION: direction})
        self.visited.add(obj)

    def get_current(self):
        current = self.path[-1][self.CELL]
        return current

    def get_valid_path(self):
        return self.valid_path

    def was_visited(self,obj):
        return obj in self.visited

    def is_at_start(self):
        return self.path[-1][self.STATUS] == Visit_Status.START

    def full_solution_path(self):
        return self.path

    def only_valid_path(self):
        return self.valid_path


    def __iter__(self):

        return self

    def __next__(self):

        if self.current >= len(self.path):
            raise StopIteration

        next = self.path[self.current]
        self.current += 1
        return next

        # make sure I get the dead end thing figured out