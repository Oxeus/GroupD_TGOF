import crayons
import os
import time
from .player import Direction
from .map import Map


class Drawer:
    def __init__(self):
        # self.width = os.get_terminal_size().columns
        self.width = 40
        # self.height = os.get_terminal_size().lines
        self.height = 30
        self.middle = self.height // 2

    def title_screen(self):
        for i in range(self.middle):
            print()
        print(crayons.green("The Game of Frugal!".center(self.width)))
        for i in range(self.middle):
            print()
        time.sleep(3)

    def menu_screen(self):
        for i in range(self.middle - 4):
            print()
        print(crayons.green("The Game of Frugal!".center(self.width)))
        print(crayons.yellow("1. Start Game!".center(self.width)))
        print(crayons.yellow("2. Configuration?".center(self.width)))
        print(crayons.yellow("3. Exit Game.".center(self.width)))
        for i in range(self.middle - 5):
            print()
        return int(input("Enter your choice: ".center(self.width)))

    def print_map(self, player, game_map):
        b = player.get_position()
        size = game_map.get_size()
        spacer = self.height - size[0]
        spacer = spacer // 2
        for i in range(spacer):
            print()
        for j in range(game_map.get_columns()):
            for k in range(game_map.get_rows()):
                if k == b[0] and j == b[1]:
                    print(crayons.red(u"\u25CB"), end=' ')
                else:
                    if game_map.get_tile(j, k).seen_status():
                        print(crayons.green(game_map.get_tile(j, k).get_name()), end=' ')
                    else:
                        print(' ', end=' ')
            print()
        for i in range(spacer):
            print()

    def store_menu(self):
        for i in range(self.height):
            print()

    def move_menu(self, player, game_map):
        direction = input("What choice do you want to make (north, east, south, west): ")
        player.move(direction.lower(), game_map)

    def print_stats(self, player):
        for i in range(2):
            print()
        print(crayons.yellow("Energy: " + str(player.get_energy()) + "          " + "Money: " + str(player.get_money())))

    def game_menu(self, player, game_map):
        choice = int(input("What choice do you want to make (1: Move, 2: Store, or 3: Quit): "))
        if choice == 1:
            # Access Menu for Move
            self.move_menu(player, game_map)
            return True
        if choice == 2:
            # Access Menu for Store
            self.store_menu()
            return True
        if choice == 3:
            return False
