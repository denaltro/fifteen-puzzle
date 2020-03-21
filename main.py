import os
import msvcrt
from random import shuffle

ESC = 27
KEY_UP = 72
KEY_DOWN = 80
KEY_LEFT = 75
KEY_RIGHT = 77


class FifteenPuzzle:
    def __init__(self, size: int = 4):
        self._size = size
        self._num_cells = self._size ** 2 - 1
        self._blank_cell_index = None

        self._items = [None] * (self._size ** 2)
        self._is_over = False

    def _new_game(self):
        while True:
            self._fill()
            self._shuffle()
            if self._is_solvable():
                break
        self._items[self._blank_cell_index] = 0
        self._is_over = False

    def _move(self, cell_index):
        blank_index = self._blank_cell_index
        if cell_index >= 0 and cell_index < self._num_cells + 1:
            if (blank_index + 1) % 4 == 0 and cell_index == blank_index + 1:
                return
            if blank_index % 4 == 0 and cell_index == blank_index - 1:
                return
            if abs(blank_index - cell_index) == 1 or (abs(blank_index - cell_index) == self._size):
                self._items[blank_index], self._items[cell_index] = self._items[cell_index], self._items[blank_index]
                self._blank_cell_index = self._items.index(0)

    def _event_listener(self):
        key = ord(msvcrt.getch())

        if key == KEY_UP:
            self._move(self._blank_cell_index - self._size)
        elif key == KEY_DOWN:
            self._move(self._blank_cell_index + self._size)
        elif key == KEY_LEFT:
            self._move(self._blank_cell_index - 1)
        elif key == KEY_RIGHT:
            self._move(self._blank_cell_index + 1)
        elif key == ESC:
            os.sys.exit()

    def _shuffle(self):
        shuffle(self._items)

    def _fill(self):
        self._items = list(range(1, self._size ** 2 + 1))
        self._blank_cell_index = len(self._items) - 1

    def _pprint(self):
        max_num_len = len(str(max(self._items[:-1])))
        line = str('-' * (max_num_len + 2)).join('+' * (self._size + 1))

        print(line)
        for i, cell in enumerate(self._items):
            if not cell:
                cell = ' '

            if not i % self._size:
                print('|', end=str())

            spaces = ' ' * (max_num_len - len(str(cell)) + 1)

            print(f'{spaces}{cell} |', end=str())
            if not (i + 1) % self._size:
                print('\n', end=str())
                print(line)

    def _is_solvable(self):
        '''https://www.geeksforgeeks.org/check-instance-15-puzzle-solvable/

        '''
        inversions = 0
        i = 0
        while i < len(self._items):
            j = 0
            while j < i:
                if self._items[j] > self._items[i]:
                    inversions += 1
                j += 1
            i += 1
        return inversions % 2 == 0

    def _is_solved(self):
        if self._items[self._num_cells] != 0:
            return False

        i = self._num_cells - 2
        while i >= 0:
            if self._items[i] != i + 1:
                return False
            i -= 1
        return True

    def run(self):
        self._new_game()
        while not self._is_over:
            os.system('cls' if 'nt' in os.name else 'clear')
            self._is_over = self._is_solved()
            self._pprint()
            self._event_listener()
        print('CONGRATULATIONS! YOU`RE SOLVED IT!')


if __name__ == "__main__":
    f = FifteenPuzzle()
    f.run()
