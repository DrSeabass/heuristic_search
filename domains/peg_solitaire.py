"""
A simple representation of the peg solitaire puzzle

https://en.wikipedia.org/wiki/Peg_solitaire

Starting with a hardcoded representation of the triangle version

*
**
***
****
*****
"""

from interface import SearchInterface

PEG_CHAR = '!'
HOLE_CHAR = 'O'
NULL_CHAR = ' '

PEG = 1
HOLE = 0
NON_PLACE = -1

ROW = 0
COLUMN = 1

class Move():

    start_position = None
    jumped_peg = None
    end_position = None

    def __init__(self, start_position, jumped_peg, end_position, src=""):
        self.start_position = start_position
        self.jumped_peg = jumped_peg
        self.end_position = end_position
        self.cost = 1
        self.src = src
        
    def __str__(self):
        return "{3}:{0} jumps {1} landing {2}".format(self.start_position, self.jumped_peg, self.end_position, self.src)
    

class Board():
    holes = None
    rows = None
    cols = None

    def __init_triangle_holes(self):
        self.holes = [
            [ HOLE, NON_PLACE, NON_PLACE, NON_PLACE, NON_PLACE],
            [ PEG, PEG, NON_PLACE, NON_PLACE, NON_PLACE ],
            [ PEG, PEG, PEG, NON_PLACE, NON_PLACE ],
            [ PEG, PEG, PEG, PEG, NON_PLACE ],
            [ PEG, PEG, PEG, PEG, PEG ],
        ]
        self.rows = 5
        self.cols = 5

    def legal_move(self, move):
        # Check move position legality
        if not self.legal_position(move.start_position):
            raise ValueError("Move starting position isn't on the board: {0}".format(move))
        if not self.legal_position(move.jumped_peg):
            raise ValueError("Move jumped peg isn't on the board: {0}".format(move))
        if not self.legal_position(move.end_position):
            raise ValueError("Move ending position isn't on the board: {0}".format(move))
        # Check move positions have expected values
        if self.holes[move.start_position[ROW]][move.start_position[COLUMN]] != PEG:
            raise ValueError("Move starting postion {0} did not contain a peg.".format(move.start_position))
        if self.holes[move.jumped_peg[ROW]][move.jumped_peg[COLUMN]] != PEG:
            raise ValueError("Move jumped peg {0} did not contain a peg.".format(move.jumped_peg))
        if self.holes[move.end_position[ROW]][move.end_position[COLUMN]] != HOLE:
            raise ValueError("Move end_position {0} was not empty.".format(move.end_position))
        # Validate that Start Position, Jumped Peg, and End Posotion are 'in a line'
        row_displacement = move.jumped_peg[ROW] - move.start_position[ROW]
        expected_target_row = 2 * row_displacement + move.start_position[ROW]
        column_displacement = move.jumped_peg[COLUMN] - move.start_position[COLUMN]
        expected_target_column = 2 * column_displacement + move.start_position[COLUMN]
        if move.end_position[ROW] != expected_target_row or move.end_position[COLUMN] != expected_target_column:
            raise ValueError("Peg, Jumpee, and Target do not appear to be in a line: {}".format(move))
        return True

    def legal_position(self, pos):
        """
        Is the supplied position on the board?
        """
        return (pos[ROW] >= 0 and pos[ROW] < self.rows and
                pos[COLUMN] >= 0 and pos[COLUMN] < self.cols)

    def __lateral_moves(self, pos):
        ret_moves = []
        for displacement in [-1, 1]:
            jump_column = pos[COLUMN] + displacement
            end_column = pos[COLUMN] + 2 * displacement
            if (end_column >= 0 and end_column < self.cols and
                self.holes[pos[ROW]][jump_column] == PEG and
                self.holes[pos[ROW]][end_column] == HOLE): 
                ret_moves.append(Move(pos, (pos[ROW], jump_column), (pos[ROW], end_column), "Lateral"))
        return ret_moves

    def __left_moves(self,pos):
        ret_moves = []
        for displacement in [-1, 1]:
            jumped_row = pos[ROW] + displacement
            jumped_col = pos[COLUMN] + displacement
            target_row = pos[ROW] + 2 * displacement
            target_col = pos[COLUMN] + 2 * displacement
            target = (target_row, target_col)
            if (self.legal_position(target) and
                self.holes[jumped_row][jumped_col] == PEG and
                self.holes[target_row][target_col] == HOLE):
                ret_moves.append(Move(pos, (jumped_row, jumped_col), target, "Left"))
        return ret_moves

    def __right_moves(self,pos):
        ret_moves = []
        for displacement in [-1, 1]:
            jumped_row = pos[ROW] + displacement
            jumped_col = pos[COLUMN]
            target_row = pos[ROW] + 2 * displacement
            target_col = pos[COLUMN]
            target = (target_row, target_col)
            if (self.legal_position(target) and
                self.holes[jumped_row][jumped_col] == PEG and
                self.holes[target_row][target_col] == HOLE):
                ret_moves.append(Move(pos, (jumped_row, jumped_col), target, "Right"))
        return ret_moves
    
    def legal_moves_from_position(self, pos):
        if not self.legal_position(pos):
            raise ValueError("{0} is not a legal board position".format(pos))
        # Assume we're computing legal moves from a peg
        if self.holes[pos[ROW]][pos[COLUMN]] != PEG:
            return []
        return self.__lateral_moves(pos) + self.__left_moves(pos) + self.__right_moves(pos)

    def legal_moves(self):
        ret_moves = []
        for x in range(self.cols):
            for y in range(self.rows):
                ret_moves += self.legal_moves_from_position((y,x))
        return ret_moves

    def copy(self):
        ret = Board()
        for x in range(self.cols):
           for y in range(self.rows):
                ret.holes[y][x] = self.holes[y][x]
        return ret

    def apply_move(self, move):
        if not self.legal_move(move):
            raise ValueError("Attempting to apply a illegal move: {}".format(move))
        self.holes[move.start_position[ROW]][move.start_position[COLUMN]] = HOLE
        self.holes[move.jumped_peg[ROW]][move.jumped_peg[COLUMN]] = HOLE
        self.holes[move.end_position[ROW]][move.end_position[COLUMN]] = PEG
        return move.cost

    def undo_move(self, move):
        self.holes[move.start_position[ROW]][move.start_position[COLUMN]] = PEG
        self.holes[move.jumped_peg[ROW]][move.jumped_peg[COLUMN]] = PEG
        self.holes[move.end_position[ROW]][move.end_position[COLUMN]] = HOLE
        # TODO: Validate that move was legal before undoing
        if not self.legal_move(move):
            raise ValueError("Move illegal after undoing itself. Something is wrong!: {}".format(move))
        return move.cost

    def solved(self):
        peg_count = 0
        for x in range(self.cols):
            for y in range(self.rows):
                if self.holse[y][x] == PEG:
                    peg_count += 1
            if peg_count > 1:
                return False
        return True

    def validate_solution(moves, display=False):
        starting_state = Board()
        for move in moves:
            if display:
                print(self)
                print(move)
            starting_state.apply_move(move)
        return self.solved()

    def __init__(self):
        self.__init_triangle_holes()
        

    def __str__(self):
        ret_str = ""
        for row in self.holes:
            for column in row:
                if column == PEG:
                    ret_str +=  PEG_CHAR
                elif column == HOLE:
                    ret_str += HOLE_CHAR
                elif column == NON_PLACE:
                    ret_str += NULL_CHAR
                else:
                    raise ValueError("Got unexpected value in holes, expected one of {-1, 0, 1}, but saw: " + str(column))
            ret_str += '\n'
        return ret_str


def PegSolitaireInterface(Interface):

    self.problem = None

    def __init__(self, problem):
        self.problem = problem

    # Here, a state is a Board
    def goal_p(self, state):
        return state.solved()

    def get_actions(self, state):
        return state.legal_moves()

    def expand(self,state):
        moves = state.legal_moves()
        children = []
        for move in moves:
            child = state.copy()
            child.apply_move(move)
            children.append(child)
        return children

    def initial_state(self):
        return self.problem.copy()

    def apply_action(self, state, action):
        return state.apply_move(action)

    def undo_action(self, state, action):
        return state.undo_move(action)

    def vailadte_solution(self, action_list, display=False):
        self.problem.validate_solution(action_list, display)


if __name__ == "__main__":
    b = Board()
    print(b)
    moves = b.legal_moves()
    for move in moves:
        print(move)
        b.apply_move(move)
        print(b)
        for sub_move in b.legal_moves():
            print(sub_move)
            b.apply_move(sub_move)
            print(b)
            b.undo_move(sub_move)
        b.undo_move(move)

