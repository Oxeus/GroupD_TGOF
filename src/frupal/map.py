"""
Nick Grout 3/12/2020
"""
from .tiles import Tile, Water, Mud, Obstacle, Troll, Custom
from .config import Config
from random import randint
from platform import system


class Map:
    """
    This is the main map class. It constructs and manages the 2d array of
    tiles
    """
    def __init__(self):
        """
        :param rows: the x dimension of the map
        :param columns: the y dimension of the map
        :returns: a new map object with a basic (all normal Tiles) 2d array
        """
        self._array = []

    # Function used to update data on new pipethrough
    def update_map(self, config: Config, debug: bool):
        jewel_variance = config.get_map('jewel_var')
        base_icon = u"\u25A0"
        base = 'grass'
        if system() == "Windows":
            base_icon = "L"
        base_color = 'green'
        base_tool = 'feet'

        tiles = config.get_tiles()
        self._array = [[] for i in range(config.get_map("height"))]

        for i in range(len(self._array)):
            self._array[i] = [Tile(base, 1, base_icon, base_color, base_tool, 1, debug) for i in
                              range(config.get_map("width"))]

        self.__random_gen(base, tiles, config, debug)
        if config.get_map('total') < jewel_variance:
            self._array[randint(0, len(self._array) - 1)][randint(0, len(self._array[0]) - 1)].add_inv('jewels')

        count = 0
        while count < (config.get_map('total') // jewel_variance):
            x = randint(0, len(self._array) - 1)
            y = randint(0, len(self._array[0]) - 1)
            if not self._array[x][y].has_item('jewels'):
                self._array[x][y].add_inv('jewels')
                count += 1
        self._array[0][0].seen_set(True)

    # Function used to randomly generate a map of tiles specified by the config
    def __random_gen(self, base, tiles, config, debug):
        for tile in tiles:
            count = 0
            info = config.get_tile(tile)
            while count < info['count']:
                x = randint(0, len(self._array) - 1)
                y = randint(0, len(self._array[0]) - 1)
                if self._array[x][y].get_name() == base:
                    self.__set_tile(tile, info, x, y, debug)
                    count += 1

    # Function used to set a tile to its respective object and x and y location
    def __set_tile(self, tile, info, x, y, debug):
        if tile == 'water':
            self._array[x][y] = Water(tile, info['energy_req'], info['icon'], info['color'], info['tool']['name'],
                                      info['tool']['energy'], debug)
        elif tile == 'tree':
            self._array[x][y] = Obstacle(tile, info['energy_req'], info['icon'], info['color'], info['tool']['name'],
                                         info['tool']['energy'], debug)
        elif tile == 'mud':
            self._array[x][y] = Mud(tile, info['energy_req'], info['icon'], info['color'], info['tool']['name'],
                                    info['tool']['energy'], debug)
        elif tile == 'troll':
            self._array[x][y] = Troll(tile, info['energy_req'], info['icon'], info['color'], info['tool']['name'],
                                      info['tool']['energy'], debug)
        elif tile == 'blackberry':
            self._array[x][y] = Obstacle(tile, info['energy_req'], info['icon'], info['color'], info['tool']['name'],
                                         info['tool']['energy'], debug)
        elif tile == 'boulder':
            self._array[x][y] = Obstacle(tile, info['energy_req'], info['icon'], info['color'], info['tool']['name'],
                                         info['tool']['energy'], debug)
        else:
            if info['type'] == 'tile':
                self._array[x][y] = Custom(tile, info['energy_req'], info['icon'], info['color'], info['tool']['name'],
                                           info['tool']['energy'], debug)
            elif info['type'] == "obs":
                self._array[x][y] = Obstacle(tile, info['energy_req'], info['icon'], info['color'],
                                             info['tool']['name'],
                                             info['tool']['energy'], debug)

    # Access item in the array
    def __getitem__(self, row: int):
        """
        Access an item in the 2d array
        """
        return self._array[row]

    # Debug print out of array
    def __str__(self):
        """
        Output a representation of the map to a string
        :returns: a string representation (human readable format) of the map
        """
        return_str = "****** FOR DEBUG PURPOSE ONLY\n"
        for i in range(len(self._array[0])):
            for j in range(len(self._array)):
                return_str += self._array[j][i].title + ", "
            return_str += "\n"
        return return_str

    # Function used to get the size of the map, returns a tuple
    def get_size(self):
        """
        Returns (ROWS, COLUMNS)
        :returns: the dimensions of the 2D array as a tuple.
        """
        return len(self._array), len(self._array[0])

    # Reveal the map, sets the seen status of all tiles to true
    def map_reveal(self):
        for i in range(len(self._array[0])):
            for j in range(len(self._array)):
                self._array[j][i].seen_set(True)
