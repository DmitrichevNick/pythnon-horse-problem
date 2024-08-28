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

boards_in_progress = [HorseBoard([])]
finished_boards = []
print("Start calculating")
while len(boards_in_progress) != 0:
    board = boards_in_progress.pop(0)
    next_steps = board.get_next_steps()
    if not next_steps:
        finished_boards.append(board)
    else:
        for step in next_steps:
            boards_in_progress.append(HorseBoard([*board.steps, step]))
print("Finished calculating")
print(f"Finished boards: {len(finished_boards)}")
max_len_steps = 0
max_len_board = None
for board in finished_boards:
    if len(board) > max_len_steps:
        max_len_steps = len(board)
        max_len_board = board
print(f"MAX len steps: {max_len_steps}")
print(f"Steps: {max_len_board.steps}")
    


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
