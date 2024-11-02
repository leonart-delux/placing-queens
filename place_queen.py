import tkinter as tk
import random
import copy
import time

SQUARE_SIZE = 50

class QueenChess: 
    def __init__(self, root):
        self.root = root
        self.root.title("Queen-Placing Chessboard")
        self.queens_places = []
        self.chessboard = tk.Canvas(self.root, width=SQUARE_SIZE * 8, height=SQUARE_SIZE * 8)
        self.chessboard.grid(row=0, column=0, columnspan=3)
        self.facing_pairs_label = tk.Label(self.root, font=("Arial", 24))
        self.facing_pairs_label.grid(row=2, column=0, columnspan=3)
        self.place_queens()
        self.draw_board()  
        self.create_function_buttons()    
    
    def place_queens(self):
        for i in range(8):
            queen_place = [0, i]
            self.queens_places.append(queen_place)

    def shuffle_queens(self):
        for col in range(8):
            randow_row = random.randint(0, 7)
            self.queens_places[col] = [randow_row, col]
        self.draw_board()


    def draw_board(self):
        # delete old board
        self.chessboard.delete(tk.ALL)

        for row in range(8):
            for col in range(8):
                x1 = col * SQUARE_SIZE
                y1 = row * SQUARE_SIZE
                x2 = x1 + SQUARE_SIZE
                y2 = y1 + SQUARE_SIZE
                color = "white" if (row + col) % 2 == 0 else "black"
                self.chessboard.create_rectangle(x1, y1, x2, y2, fill=color)

        # draw queen
        for queen_place in self.queens_places:
            queen_row, queen_col = queen_place
            x1 = queen_col * SQUARE_SIZE + SQUARE_SIZE / 4
            y1 = queen_row * SQUARE_SIZE + SQUARE_SIZE / 4
            x2 = x1 + SQUARE_SIZE / 2
            y2 = y1 + SQUARE_SIZE / 2
            self.chessboard.create_oval(x1, y1, x2, y2, fill="red")

        # facing pairs
        facing_pairs = self.get_numb_faceable_pairs(self.queens_places)
        self.facing_pairs_label.config(text=f"Facing pairs: {facing_pairs}")

        # update UI
        self.root.update_idletasks()
        time.sleep(1)


    def create_function_buttons(self):
        button = tk.Button(self.root, text="Shuffle", width=10, height= 2, command=lambda: self.shuffle_queens())
        button.grid(row=1, column=0)
        button = tk.Button(self.root, text="Hill", width=10, height= 2, command=lambda: self.hill_climbing_solving())
        button.grid(row=1, column=1)
        button = tk.Button(self.root, text="Beam", width=10, height= 2, command=lambda: self.beam_search_solving())
        button.grid(row=1, column=2)

    def get_numb_faceable_pairs(self, assume_queens_places):
        count = 0
        # for each queen
        for i in range(7):
            current_queen_row, current_queen_col = assume_queens_places[i] 
            # check if it faces others
            for j in range(i + 1, 8):
                checking_queen_row, checking_queen_col = assume_queens_places[j]
                if (current_queen_row == checking_queen_row or abs(current_queen_col - checking_queen_col) == abs(current_queen_row - checking_queen_row)):
                    count += 1
        return count

    def get_possible_next_states(self, assume_queen_places):
        possible_next_states = []
        # for each queen of each collumn
        for j in range(8):
            queen_row = assume_queen_places[j][0]
            # for each row of that collumn --> get a possible state by moving queen of that collumn to other places
            for i in range(0, 8):
                copied_queens_state = copy.deepcopy(assume_queen_places)
                # avoid duplicate state
                if queen_row != i:
                    copied_queens_state[j][0] = i
                    possible_next_states.append(copied_queens_state)
        return possible_next_states

    def hill_climbing_solving(self):
        # assume that initial state is not possible best state
        best_state = False
        # store number of facing queen pairs
        current_facing_pairs = self.get_numb_faceable_pairs(self.queens_places)
        # assume next state is current state
        next_state = self.queens_places

        while(not best_state):
            possible_next_states = self.get_possible_next_states(self.queens_places)
            # check if current state can be improved or not
            improved = False

            # for each next state that possible of current state
            for possible_next_state in possible_next_states:
                # calculate facing pairs of next state
                numb_faceable_pairs = self.get_numb_faceable_pairs(possible_next_state)
                if (numb_faceable_pairs < current_facing_pairs):
                    next_state = possible_next_state
                    current_facing_pairs = numb_faceable_pairs
                    improved = True

            if improved:
                self.queens_places = next_state
                # illustration
                self.draw_board()
            else:
                best_state = True
    
    def beam_search_solving(self):
        k = 3
        current_point = self.get_numb_faceable_pairs(self.queens_places)
        best_k_states = [{
            'point': current_point,
            'state': self.queens_places,
            'previous_state': {}
        }]

        # loop until fail
        while (True):
            # store new state which obtained from k-best-states
            explored_state = []

            # start explore
            # for each state in k best states explore all neighbour states
            for a_best_state in best_k_states:
                # get possible neighbour states of current best state
                possible_next_states = self.get_possible_next_states(a_best_state['state'])

                # append each next state to explored_state
                for next_state in possible_next_states:
                    # calculate point for sorting
                    next_state_point = self.get_numb_faceable_pairs(next_state)
                    explored_state.append({
                        'point': next_state_point,
                        'state': next_state,
                        'previous_state': a_best_state
                    })
                
            # sorting
            explored_state.sort(key=lambda x: x['point'])

            # check if new states are better
            if (explored_state[0]['point'] < best_k_states[0]['point']):
                # update best k state
                best_k_states = explored_state[:k]
            else:
                # break loop
                break    
        
        # track steps
        result = [best_k_states[0]['state']]
        if (best_k_states[0]['previous_state'] != {}):
            current_state = best_k_states[0]['previous_state']
            while (True):
                result.append(current_state['state'])
                if (current_state['previous_state'] != {}):
                    current_state = current_state['previous_state']
                else:
                    break
        
        # illustration
        for state in reversed(result):
            self.queens_places = state
            self.draw_board()

if __name__ == "__main__":
    root = tk.Tk()
    game = QueenChess(root)
    root.mainloop()