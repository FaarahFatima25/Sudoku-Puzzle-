import copy
import random
import sys

EMPTY_SPACE = '.'
GRID_LENGTH = 9
BOX_LENGTH = 3
FULL_GRID_SIZE = GRID_LENGTH * GRID_LENGTH

class SudokuGrid:
    def __init__(self, originalSetup):
        self.originalSetup = originalSetup
        self.grid = {}
        self.moves = []
        self.resetGrid()

    def resetGrid(self):
        for x in range(GRID_LENGTH):
            for y in range(GRID_LENGTH):
                self.grid[(x, y)] = EMPTY_SPACE

        assert len(self.originalSetup) == FULL_GRID_SIZE, "Puzzle size must be exactly 81 characters."
        i = 0
        for y in range(GRID_LENGTH):
            for x in range(GRID_LENGTH):
                self.grid[(x, y)] = self.originalSetup[i]
                i += 1

    def makeMove(self, column, row, number):
        x = 'ABCDEFGHI'.find(column)
        y = int(row) - 1

        if self.originalSetup[y * GRID_LENGTH + x] != EMPTY_SPACE:
            return False

        self.grid[(x, y)] = number
        self.moves.append(copy.copy(self.grid))
        return True

    def undo(self):
        if not self.moves:
            return

        self.moves.pop()

        if not self.moves:
            self.resetGrid()
        else:
            self.grid = copy.copy(self.moves[-1])

    def display(self):
        print(' ABC DEF GHI')
        for y in range(GRID_LENGTH):
            for x in range(GRID_LENGTH):
                if x == 0:
                    print(str(y + 1) + ' ', end='')

                print(self.grid[(x, y)] + ' ', end='')
                if x == 2 or x == 5:
                    print('|', end='')

            print()

            if y == 2 or y == 5:
                print('  -------+--------+------')

    def _isCompleteSetOfNumbers(self, numbers):
        return sorted(numbers) == list('123456789')

    def isSolved(self):
        for row in range(GRID_LENGTH):
            rowNumbers = []
            for x in range(GRID_LENGTH):
                number = self.grid[(x, row)]
                rowNumbers.append(number)
            if not self._isCompleteSetOfNumbers(rowNumbers):
                return False

        for column in range(GRID_LENGTH):
            columnNumbers = []
            for y in range(GRID_LENGTH):
                number = self.grid[(column, y)]
                columnNumbers.append(number)
            if not self._isCompleteSetOfNumbers(columnNumbers):
                return False

        for boxx in (0, 3, 6):
            for boxy in (0, 3, 6):
                boxNumbers = []
                for x in range(BOX_LENGTH):
                    for y in range(BOX_LENGTH):
                        number = self.grid[(boxx + x, boxy + y)]
                        boxNumbers.append(number)
                    if not self._isCompleteSetOfNumbers(boxNumbers):
                        return False

        return True


print('')
input('Press Enter to begin...')

# Hardcoded puzzles (from sudokupuzzles.txt)
puzzles = [
    "..3.2.6..9..3.5..1..18.64....81.29..7.......8..67.82....26.95..8..2.3..9..5.1.3..",
    "2...8.3...6..7..84.3.5..2.9...1.54.8.........4.27.6...3.1..7.4.72..4..6...4.1...3",
    "......9.7...42.18....7.5.261..9.4....5.....4....5.7..992.1.8....34.59...5.7......",
    ".3..5..4...8.1.5..46.....12.7.5.2.8....6.3....4.1.9.3.25.....98..1.2.6...8..6..2.",
    ".2.81.74.7....31...9...28.5..9.4..874..2.8..316..3.2..3.27...6...56....8.76.51.9.",
    "1..92....524.1...........7..5...81.2.........4.27...9..6...........3.945....71..6",
    ".43.8.25.6.............1.949....4.7....6.8....1.2....382.5.............5.34.9.71.",
    "48...69.2..2..8..19..37..6.84..1.2....37.41....1.6..49.2..85..77..9..6..6.92...18",
    "...9....2.5.1234...3....16.9.8.......7.....9.......2.5.91....5...7439.2.4....7...",
    "..19....39..7..16..3...5..7.5......9..43.26..2......7.6..1...3..42..7..65....68..",
]

# Validate all puzzles
valid_puzzles = [p for p in puzzles if len(p) == FULL_GRID_SIZE]
if not valid_puzzles:
    print("No valid puzzles found in the hardcoded list.")
    sys.exit()

# Start the game with a random puzzle from the hardcoded list
grid = SudokuGrid(random.choice(valid_puzzles))

while True:
    grid.display()

    if grid.isSolved():
        print('Congratulations! You solved the puzzle!')
        print('Thanks for playing!')
        sys.exit()

    while True:
        print()
        print('Enter a move, or RESET, NEW, UNDO, ORIGINAL, or QUIT:')
        print('(For example, a move looks like "B4 9".)')

        action = input('> ').upper().strip()

        if len(action) > 0 and action[0] in ('R', 'N', 'U', 'O', 'Q'):
            break

        if len(action.split()) == 2:
            space, number = action.split()
            if len(space) != 2:
                continue

            column, row = space
            if column not in list('ABCDEFGHI'):
                print('There is no column', column)
                continue
            if not row.isdecimal() or not (1 <= int(row) <= 9):
                print('There is no row', row)
                continue
            if not (1 <= int(number) <= 9):
                print(f'Select a number from 1 to 9, not {number}')
                continue
            break
    print()

    if action.startswith('R'):
        grid.resetGrid()
        continue

    if action.startswith('N'):
        grid = SudokuGrid(random.choice(valid_puzzles))
        continue

    if action.startswith('U'):
        grid.undo()
        continue

    if action.startswith('O'):
        originalGrid = SudokuGrid(grid.originalSetup)
        print('The original grid looked like this:')
        originalGrid.display()
        input('Press Enter to continue...')

    if action.startswith('Q'):
        print('Thanks for playing!')
        sys.exit()

    column, row = space
    if grid.makeMove(column, row, number) == False:
        print("You cannot overwrite the original grid's numbers.")
        print('Enter ORIGINAL to view the original grid.')
        input('Press Enter to continue...')
