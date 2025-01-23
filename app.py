from flask import Flask, render_template, request, jsonify
import math

app = Flask(__name__)

# Function to check for a winner
def check_winner(board):
    winning_combinations = [
        [board[0], board[1], board[2]],
        [board[3], board[4], board[5]],
        [board[6], board[7], board[8]],
        [board[0], board[3], board[6]],
        [board[1], board[4], board[7]],
        [board[2], board[5], board[8]],
        [board[0], board[4], board[8]],
        [board[2], board[4], board[6]],
    ]
    for combo in winning_combinations:
        if combo[0] == combo[1] == combo[2] and combo[0] != ' ':
            return combo[0]
    return None

# Function to check for a draw
def check_draw(board):
    return ' ' not in board

# Minimax function with Alpha-Beta Pruning
def minimax(board, depth, is_maximizing, alpha, beta):
    winner = check_winner(board)
    if winner == 'X':
        return -1
    elif winner == 'O':
        return 1
    elif check_draw(board):
        return 0

    if is_maximizing:
        max_eval = -math.inf
        for i in range(9):
            if board[i] == ' ':
                board[i] = 'O'
                eval = minimax(board, depth + 1, False, alpha, beta)
                board[i] = ' '
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
        return max_eval
    else:
        min_eval = math.inf
        for i in range(9):
            if board[i] == ' ':
                board[i] = 'X'
                eval = minimax(board, depth + 1, True, alpha, beta)
                board[i] = ' '
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
        return min_eval

# Function to get the best move for the AI
def get_best_move(board):
    best_move = None
    best_value = -math.inf
    for i in range(9):
        if board[i] == ' ':
            board[i] = 'O'
            move_value = minimax(board, 0, False, -math.inf, math.inf)
            board[i] = ' '
            if move_value > best_value:
                best_value = move_value
                best_move = i
    return best_move

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/move', methods=['POST'])
def move():
    data = request.get_json()
    board = data['board']
    ai_move = get_best_move(board)
    board[ai_move] = 'O'
    return jsonify({'board': board})

if __name__ == '__main__':
    app.run(debug=True)
