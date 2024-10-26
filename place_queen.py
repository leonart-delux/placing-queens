import tkinter as tk
import random

SQUARE_SIZE = 50

class QueenChess: 
    def __init__(self, root):
        self.root = root
        self.root.title("Queen-Placing Chessboard")
        self.queens_places = []
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
        # create chessboard
        canvas = tk.Canvas(self.root, width=SQUARE_SIZE * 8, height=SQUARE_SIZE * 8)
        canvas.grid(row=0, column=0, columnspan=3)
        for row in range(8):
            for col in range(8):
                x1 = col * SQUARE_SIZE
                y1 = row * SQUARE_SIZE
                x2 = x1 + SQUARE_SIZE
                y2 = y1 + SQUARE_SIZE
                color = "white" if (row + col) % 2 == 0 else "black"
                canvas.create_rectangle(x1, y1, x2, y2, fill=color)

        # draw queen
        for queen_place in self.queens_places:
            queen_row, queen_col = queen_place
            x1 = queen_col * SQUARE_SIZE + SQUARE_SIZE / 4
            y1 = queen_row * SQUARE_SIZE + SQUARE_SIZE / 4
            x2 = x1 + SQUARE_SIZE / 2
            y2 = y1 + SQUARE_SIZE / 2
            canvas.create_oval(x1, y1, x2, y2, fill="red")

    def create_function_buttons(self):
        button = tk.Button(self.root, text="Shuffle", width=10, height= 2, command=lambda: self.shuffle_queens())
        button.grid(row=1, column=0)
        button = tk.Button(self.root, text="Hill", width=10, height= 2)
        button.grid(row=1, column=1)
        button = tk.Button(self.root, text="Beam", width=10, height= 2)
        button.grid(row=1, column=2)

    def numb_faceable_pairs(self):
        count = 0   
        # for each queen
        for i in range(7):
            current_queen_row, current_queen_col = self.queens_places[i] 
            # check if it faces others
            for j in range(i + 1, 8):
                checking_queen_row, checking_queen_col = self.queens_places[j]
                if (current_queen_row == checking_queen_row or abs(current_queen_col - checking_queen_col) == abs(current_queen_row - checking_queen_row)):
                    count += 1

    # def hill_climbing_solving(self):


if __name__ == "__main__":
    root = tk.Tk()
    game = QueenChess(root)
    root.mainloop()