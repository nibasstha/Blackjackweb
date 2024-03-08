import random

# State class
class State:
    def __init__(self, board, player):
        self.board = board
        self.player = player

    def is_game_over(self):
        for i in range(3):
            if self.board[i][0] == self.board[i][1] == self.board[i][2] != " ":
                return True  # Row i is complete
            if self.board[0][i] == self.board[1][i] == self.board[2][i] != " ":
                return True  # Column i is complete
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != " ":
            return True  # Diagonal
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != " ":
            return True  # Diagonal
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == " ":
                    return False  # Not a terminal state, game can continue
        return True  # Tie game

    def get_legal_moves(self):
        moves = []
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == " ":
                    moves.append((i, j))
        return moves

    def apply_move(self, move):
        i, j = move
        board = [row.copy() for row in self.board]
        board[i][j] = self.player
        return State(board, "O" if self.player == "X" else "X")

    def get_winner(self):
        for i in range(3):
            if self.board[i][0] == self.board[i][1] == self.board[i][2] != " ":
                return 1 if self.board[i][0] == "X" else -1  # Row i is complete
            if self.board[0][i] == self.board[1][i] == self.board[2][i] != " ":
                return 1 if self.board[0][i] == "X" else -1 # Column i is complete
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != " ":
            return 1 if self.board[0][0] == "X" else -1 # Diagonal
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != " ":
            return 1 if self.board[0][2] == "X" else -1  # Diagonal
        return None  # Tie game
    
# Monte Carlo Tree Search Class
class MCTSNode:
    def __init__(self, state, parent=None):
        self.state = state
        self.parent = parent
        self.children = []
        self.visits = 0
        self.wins = 0

    def fully_expanded(self):
        return len(self.children) == len(self.state.get_legal_moves())

    def is_terminal(self):
        return self.state.is_game_over()

    def best_child(self):
        if not self.children:
            return None
        unvisited = [c for c in self.children if c.visits == 0]
        if unvisited:
            return random.choice(unvisited)
        return max(self.children, key=lambda x: x.wins / x.visits)

    def expand(self):
        moves = self.state.get_legal_moves()
        for move in moves:
            new_state = self.state.apply_move(move)
            new_node = MCTSNode(new_state, self)
            self.children.append(new_node)

    def simulate(self):
        state = self.state
        while not state.is_game_over():
            moves = state.get_legal_moves()
            move = random.choice(moves)
            state = state.apply_move(move)
        return state.get_winner()

    def update(self, result):
        self.visits += 1
        if result is not None:
            self.wins += int(result)

    def uct_score(self, exploration_constant=1.414):
        if self.visits == 0:
            return float('inf')
        return self.wins / self.visits + exploration_constant * math.sqrt(math.log(self.parent.visits) / self.visits)

# Main function
def monte_carlo_tree_search(initial_state, num_iterations):
    root_state = State(initial_state, player=1)  # create root state with player 1
    root_node = MCTSNode(root_state,None)

    for i in range(num_iterations):
        node = root_node
        # Selection
        while not node.is_terminal() and node.fully_expanded():
            node = node.best_child()

        print("best child node",node)
        # Expansion
        if not node.is_terminal():
            node.expand()
            node = random.choice(node.children)

        # Simulation
        result = node.simulate()

        # Backpropagation
        while node is not None:
            node.update(result)
            node = node.parent

    if root_node.children:
        return root_node.best_child().state.board
    else:
        return root_node.state.board

# Example usage
if __name__ == '__main__':
    # Define initial state
    initial_state = [[" ", " ", " "],
                     [" ", " ", " "],
                     [" ", " ", " "]]

    # Run MCTS with 1000 iterations
    final_state = monte_carlo_tree_search(initial_state, num_iterations=1000)

    # Print the final state
    print(final_state)
