
import tkinter as tk
import random

class TicTacToe:
    WIN_LINES = [
        (0,1,2),(3,4,5),(6,7,8),     # rows
        (0,3,6),(1,4,7),(2,5,8),     # cols
        (0,4,8),(2,4,6)              # diagonals
    ]

    def __init__(self):
        self.board = [' ']*9

    def reset(self):
        self.board = [' ']*9

    def available_moves(self):
        return [i for i, v in enumerate(self.board) if v == ' ']

    def make_move(self, pos, player):
        self.board[pos] = player

    def undo_move(self, pos):
        self.board[pos] = ' '

    def winner(self):
        for a,b,c in self.WIN_LINES:
            if self.board[a] == self.board[b] == self.board[c] and self.board[a] != ' ':
                return self.board[a]
        return None

    def is_full(self):
        return all(cell != ' ' for cell in self.board)

    def minimax(self, depth, is_maximizing, alpha, beta, ai_player, human_player):
        win = self.winner()
        if win == ai_player:
            return 10 - depth, None
        elif win == human_player:
            return depth - 10, None
        elif self.is_full():
            return 0, None

        if is_maximizing:
            max_eval = -float('inf')
            best_move = None
            for move in self.available_moves():
                self.make_move(move, ai_player)
                eval_score, _ = self.minimax(depth+1, False, alpha, beta, ai_player, human_player)
                self.undo_move(move)
                if eval_score > max_eval:
                    max_eval = eval_score
                    best_move = move
                alpha = max(alpha, eval_score)
                if beta <= alpha:
                    break
            return max_eval, best_move
        else:
            min_eval = float('inf')
            best_move = None
            for move in self.available_moves():
                self.make_move(move, human_player)
                eval_score, _ = self.minimax(depth+1, True, alpha, beta, ai_player, human_player)
                self.undo_move(move)
                if eval_score < min_eval:
                    min_eval = eval_score
                    best_move = move
                beta = min(beta, eval_score)
                if beta <= alpha:
                    break
            return min_eval, best_move


class TicTacToeGUI:
    def __init__(self, root, human="X", ai="O", first="you", difficulty="hard"):
        self.root = root
        self.root.title("Tic Tac Toe AI")
        self.game = TicTacToe()
        self.human = human
        self.ai = ai
        self.difficulty = difficulty
        self.turn = first  # "you" or "ai"

        self.buttons = []
        self.status = tk.Label(root, text="Your turn!" if self.turn=="you" else "AI starts...", font=("Arial", 14))
        self.status.grid(row=3, column=0, columnspan=3, pady=10)

        for i in range(9):
            b = tk.Button(root, text=" ", font=("Arial", 24), width=5, height=2,
                          command=lambda i=i: self.human_move(i))
            b.grid(row=i//3, column=i%3)
            self.buttons.append(b)

        reset_btn = tk.Button(root, text="Reset", font=("Arial", 12), command=self.reset_game)
        reset_btn.grid(row=4, column=0, columnspan=3, pady=10)

        # if AI goes first
        if self.turn == "ai":
            self.root.after(500, self.ai_move)

    def human_move(self, idx):
        if self.turn != "you":
            return
        if self.game.board[idx] == " " and not self.game.winner():
            self.game.make_move(idx, self.human)
            self.buttons[idx].config(text=self.human, state="disabled")
            if self.game.winner():
                self.status.config(text="You win! 🏆")
                self.disable_all()
                return
            elif self.game.is_full():
                self.status.config(text="It's a draw 🤝")
                return
            else:
                self.turn = "ai"
                self.status.config(text="AI's turn...")
                self.root.after(500, self.ai_move)

    def ai_move(self):
        if self.difficulty == "easy":
            move = random.choice(self.game.available_moves())
        else:
            _, move = self.game.minimax(0, True, -float("inf"), float("inf"), self.ai, self.human)
            if move is None:
                move = random.choice(self.game.available_moves())
        self.game.make_move(move, self.ai)
        self.buttons[move].config(text=self.ai, state="disabled")

        if self.game.winner():
            self.status.config(text="AI wins 🤖")
            self.disable_all()
        elif self.game.is_full():
            self.status.config(text="It's a draw 🤝")
        else:
            self.turn = "you"
            self.status.config(text="Your turn!")

    def disable_all(self):
        for b in self.buttons:
            b.config(state="disabled")

    def reset_game(self):
        self.game.reset()
        for b in self.buttons:
            b.config(text=" ", state="normal")
        self.status.config(text="Your turn!" if self.human=="X" else "AI's turn")
        self.turn = "you"
        if self.human == "O":
            self.turn = "ai"
            self.root.after(500, self.ai_move)


class SetupWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Game Setup")

        tk.Label(root, text="Choose your symbol:").grid(row=0, column=0, sticky="w")
        self.symbol_var = tk.StringVar(value="X")
        tk.Radiobutton(root, text="X", variable=self.symbol_var, value="X").grid(row=0, column=1)
        tk.Radiobutton(root, text="O", variable=self.symbol_var, value="O").grid(row=0, column=2)

        tk.Label(root, text="Who goes first:").grid(row=1, column=0, sticky="w")
        self.first_var = tk.StringVar(value="you")
        tk.Radiobutton(root, text="You", variable=self.first_var, value="you").grid(row=1, column=1)
        tk.Radiobutton(root, text="AI", variable=self.first_var, value="ai").grid(row=1, column=2)

        tk.Label(root, text="Difficulty:").grid(row=2, column=0, sticky="w")
        self.diff_var = tk.StringVar(value="hard")
        tk.Radiobutton(root, text="Easy", variable=self.diff_var, value="easy").grid(row=2, column=1)
        tk.Radiobutton(root, text="Hard", variable=self.diff_var, value="hard").grid(row=2, column=2)

        tk.Button(root, text="Start Game", command=self.start_game).grid(row=3, column=0, columnspan=3, pady=10)

    def start_game(self):
        human = self.symbol_var.get()
        ai = "O" if human == "X" else "X"
        first = self.first_var.get()
        diff = self.diff_var.get()

        self.root.destroy()
        main_root = tk.Tk()
        TicTacToeGUI(main_root, human=human, ai=ai, first=first, difficulty=diff)
        main_root.mainloop()


if __name__ == "__main__":
    root = tk.Tk()
    SetupWindow(root)
    root.mainloop()
