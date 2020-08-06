from Maze_Exceptions import Wall_Not_Found_Exception

class Cell:
    xpos: int
    ypos: int
    walls: {}
    visited: bool

    def __init__(self,xpos, ypos):

        self.xpos = xpos
        self.ypos = ypos
        self.visited = False #needed for generation
        self.isEnd = False
        self.walls = {"T": True, "B": True, "R": True, "L": True}


    def delete_wall(self,to_delete):
        
        if not to_delete in self.walls.keys():
            raise Wall_Not_Found_Exception('{} cannot be deleted. Not a valid wall'.format(to_delete))

        self.walls.update({to_delete:False})

    def set_wall(self,to_set):

        if not to_set in self.walls.keys():
            raise Wall_Not_Found_Exception('{} cannot be created. Not a valid wall'.format(to_set))

        self.walls.update({to_set: True})

    def set_visited(self):

        self.visited = True

    def get_position(self):
        return (self.xpos, self.ypos)

    def vistited(self):
        return self.visited

    def set_end_cell(self):

        self.isEnd = True


    def get_walls(self):
       """
       @return walls, dict
       """
       return self.walls



    def __str__(self):

        return "{}/{}".format(self.xpos,self.ypos)

