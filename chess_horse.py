import curses

STDSCR = curses.initscr()
curses.noecho()
curses.cbreak()

class HorseStep:
    row = None
    col = None

    def __init__(self, row, col):
        self.row = row
        self.col = col

    def __repr__(self):
        return f"(row {self.row}, col {self.col})"

    def __eq__(self, other):
        return self.row == other.row and self.col == other.col

    def get_next_steps(self):
        return [
            HorseStep(self.row - 2, self.col - 1),
            HorseStep(self.row - 2, self.col + 1),
            HorseStep(self.row - 1, self.col - 2),
            HorseStep(self.row - 1, self.col + 2),
            HorseStep(self.row + 1, self.col - 2),
            HorseStep(self.row + 1, self.col + 2),
            HorseStep(self.row + 2, self.col - 1),
            HorseStep(self.row + 2, self.col + 1),
        ]

class HorseBoard:
    _board_size = 5
    steps = []

    def __init__(self, steps):
        self.steps = steps

    def __len__(self):
        return len(self.steps)

    def get_next_steps(self):
        next_steps = []
        if not self.steps:
            for row in range(self._board_size):
                for col in range(self._board_size):
                    next_steps.append(HorseStep(row, col))
            return next_steps
        prev_step = self.steps[-1]
        for step in prev_step.get_next_steps():
            if step.row >= 0 and step.row < self._board_size and step.col >= 0 and step.col < self._board_size and step not in self.steps:
                next_steps.append(step)
        return next_steps
    
    def print_plain(self):
        row_delimeter = f"+{'---+'*self._board_size}"
        print(row_delimeter)
        for row in range(self._board_size):
            row_str = "|"
            for col in range(self._board_size):
                cell_step = HorseStep(row, col)
                cell_value = " "
                if self.steps.count(cell_step):
                    cell_value = self.steps.index(cell_step)
                row_str += f"{cell_value:>2} |"
            row_str += f" {row}"
            print(row_str)
            print(row_delimeter)
        print(f" {'  '.join([f'{i:>2}' for i in range(self._board_size)])}")

    def print_reprint(self):
        row_out = 0

        def addstr(row_str):
            nonlocal row_out
            STDSCR.addstr(row_out, 0, row_str)
            row_out += 1

        row_delimeter = f"+{'---+'*self._board_size}"
        addstr(row_delimeter)
        for row in range(self._board_size):
            row_str = "|"
            for col in range(self._board_size):
                cell_step = HorseStep(row, col)
                cell_value = " "
                if self.steps.count(cell_step):
                    cell_value = self.steps.index(cell_step)
                row_str += f"{cell_value:>2} |"
            row_str += f" {row}"
            addstr(row_str)
            addstr(row_delimeter)
        addstr(f" {'  '.join([f'{i:>2}' for i in range(self._board_size)])}")
        addstr(f"Boards in progress: {len(boards_in_progress):>5}")
        STDSCR.refresh()


boards_in_progress = [HorseBoard([])]
best_board = HorseBoard([])
print("Start calculating")
while len(boards_in_progress) > 0:
    board = boards_in_progress.pop()
    board.print_reprint()
    next_steps = board.get_next_steps()
    if not next_steps:
        if len(board) >= len(best_board):
            best_board = board
            board.print_reprint()
        if len(board) == HorseBoard._board_size **2:
            break
        continue

    for step in next_steps:
        boards_in_progress.append(HorseBoard([*board.steps, step]))

    # time.sleep(0.005)
curses.echo()
curses.nocbreak()
curses.endwin()

print("Finished calculating")
if len(best_board) == HorseBoard._board_size **2:
    print("SOLVED!")
print(f"Board with maximal steps ({len(best_board)}):")
best_board.print_plain()



class HorseGame:
    _board_size = 8
    _empty_mark = " "
    _autosuggest_mark = "x"

    def __init__(self):
        self.chess_board = [[self._empty_mark for _ in range(self._board_size)] for _ in range(self._board_size)]
        self.step_id = 0
        self.prev_step = None

    def _is_horse_step(self, step):
        if not self.prev_step:
            return True
        if abs(self.prev_step[0] - step[0]) == 1 and abs(self.prev_step[1] - step[1]) == 2:
            return True
        if abs(self.prev_step[0] - step[0]) == 2 and abs(self.prev_step[1] - step[1]) == 1:
            return True
        return False
    
    def _verif_step(self, step, silent=False):
        if any(map(lambda x: x < 0, step)) or any(map(lambda x: x >= self._board_size, step)):
            if not silent:
                print(f"Step {step} out of board! Rerun")
            return False
        if not self._is_horse_step(step):
            if not silent:
                print(f"Step {step} is not valid for {self.prev_step} horse placement. Choose another =)")
            return False
        if self.chess_board[step[0]][step[1]] != self._empty_mark and self.chess_board[step[0]][step[1]] != self._autosuggest_mark:
            if not silent:
                print(f"You've already been here) Rerun")
            return False
        return True
    
    def _set_autosuggest(self):
        for row in range(self._board_size):
            for col in range(self._board_size):
                if self._verif_step((row, col), silent=True):
                    self.chess_board[row][col] = self._autosuggest_mark

    def _unset_autosuggest(self):
        for row in range(self._board_size):
            for col in range(self._board_size):
                if self.chess_board[row][col] == self._autosuggest_mark:
                    self.chess_board[row][col] = self._empty_mark

    def next_step(self, step):
        self._unset_autosuggest()
        if not self._verif_step(step):
            return
        self.step_id += 1
        self.chess_board[step[0]][step[1]] = self.step_id
        print(f"Your step {self.step_id}")
        self.prev_step = step
        self._set_autosuggest()
        self.print_board()

    def print_board(self):
        print("  0   1   2   3   4   5   6   7")
        print("+---+---+---+---+---+---+---+---+")
        for id, row in enumerate(self.chess_board):
            print(f"|{' |'.join([f'{i:>2}' for i in row])} | {id}")
            print("+---+---+---+---+---+---+---+---+")
        print(f"Your step {self.step_id}: {self.prev_step}")


# horse_game = HorseGame()
# horse_game.print_board()
# while True:
#     next_row, next_col = map(int, input("Choose step format <row>,<col>:").split(","))
#     horse_game.next_step((next_row, next_col))
