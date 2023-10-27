from typing import Tuple
import copy

def print_board(board: dict , player_1: str = "P1 ", player_2: str = "P2 ") -> None:
    print(
        f"""
     {''.join(f'{(len(board["top"]) - num):3}' for num in range(len(board['top'])))}
+---+{'--+'*len(board['top'])}---+
|{player_1} |{'|'.join(f'{item:2}' for item in reversed(board['top']))}|   | <- PLAYER 1
|{board["top_score"]:3} +{'--+'*len(board['top'])}{board["bot_score"]:3}|
|    |{'|'.join(f'{item:2}' for item in board['bot'])}|{player_2}| PLAYER 2 ->
+----+{'--+'*len(board['bot'])}---+
     {''.join(f'{(num+1):3}' for num in range(len(board['bot'])))}
"""
    )
    return
"""
  initial board: 
        board(dict)
        {
            "top"          : [4, 4, 4, 4, 4, 4],
            "bot"       : [4, 4, 4, 4, 4, 4],
            "top_score"    : 0,
            "bot_score" : 0
        }
"""

def move_piece(board: dict , tile: int , turn: str) -> Tuple[dict , bool]:  
#Handle player's move. Input the state of the board before and output the board after the move + the player can go again or not
    pieces = board[turn][tile]
    board[turn][tile] = 0
    location = turn
    go_again = False

    while pieces > 0:
        go_again = False    #move hasn't end yet
        pieces  -= 1
        tile    += 1            
        #take one stone from current tile and go to the next one

        if tile < len(board[location]):  #the tile still on one side (bot/top)
            board[location][tile] += 1   #put stone
            continue

        if location == turn:  #tile == board lenght and location still the same side, plus 1 in score
            board[f"{turn}_score"] += 1
            go_again = True
        else:
            pieces += 1   #at the opponent base, skip (unchange piece for next tile)
        location = "bot" if location == "top" else "top"  #change side and reset tile for next drop (if there are still pieces left)
        tile = -1  
    #The last rock (pieces ==0)
    inverse_location = "bot" if location == "top" else "top" #const for the other side
    if (
        (location == turn)                  #on our side
        and (board[location][tile] == 1)    #and the current tile after rock dropping has 1 piece (last tile empty)
        and (board[inverse_location][len(board[inverse_location]) - 1 - tile] != 0) #AND the opposite dude has sum gud stuff
    ):
        board[f"{turn}_score"] += (
            1 + board[inverse_location][len(board[inverse_location]) - 1 - tile]  #1 is the current rock and plus in dat gud stuff on the opposite side :>
        )
        #empty both tile
        board[location][tile] = 0               
        board[inverse_location][len(board[inverse_location]) - 1 - tile] = 0  
        #endGame condition
    if (not any(board["top"])) or (not any(board["bot"])): #one side dont have anystone
        board["top_score"] += sum(board["top"])             #sum them up
        board["bot_score"] += sum(board["bot"])

        board["top"] = [0] * len(board["top"])          #zeroing both side  (board["top"] : [0,0,0,0,0,0])
        board["bot"] = [0] * len(board["bot"])

        go_again = False

    return board, go_again

def is_viable_move(board: dict, tile: int, turn: str) -> bool:
    #A validation function to determine if a move is viable
    if tile >= len(board[turn]) or tile < 0:    #re-examine user input
        return False
    return bool(board[turn][tile]) #if board[turn][tile] = 0 (has nothing) this return false, else return true


"""A function to calculate the minimax algorithm for a given board

    Input:
        board 
        {
            "top"          : [4, 4, 4, 4, 4, 4],
            "bot"       : [4, 4, 4, 4, 4, 4],
            "top_score"    : 0,
            "bot_score" : 0
        }
        ai_side (str): 'top'/'bot'
        turn (str): 'top'/'bot'
        depth (int): How deep that you want the AI to look ahead, i.e difficulty

    Output:
        Tuple[int, int]:
            score (int): 
            move (int) : the recommended minimax move
                - this is used in decision making for executing the best move
    """

def minimax_mancala( board: dict, ai_side: str, turn: str, depth: int) -> Tuple[int, int]:
    #initial constant
    AI = ai_side
    PLAYER = "bot" if AI == "top" else "top"
    best_move = -1
        #if endGame or reach max depth 
    if (not any(board["top"])) or (not any(board["bot"])) or depth <= 0:
        return board[f"{AI}_score"] - board[f"{PLAYER}_score"], best_move

    # Finding the move which will give the most points to the AI
    if AI == turn:           #Current = MAX in MINIMAX
        # up up and awayyy!
        best_score = float("-inf") #represent negative infinite number 

        possible_moves = [
            move for move in range(len(board[AI])) if is_viable_move(board, move, AI)
        ]

        for move in possible_moves:
            board_copy = copy.deepcopy(board)  #hypothetical board, since we don't want to change things in the real board
            board_copy, go_again = move_piece(board_copy, move, turn)  

            # mancala is one of those games where you can get two moves.
            # In testing, I found that not decressing the depth for the multimove results in the best AI
            if go_again:
                points, _ = minimax_mancala(board_copy, AI, AI, depth) 
            else:
                points, _ = minimax_mancala(board_copy, AI, PLAYER, depth - 1)   #player turn(i.e MIN turn)

            # The MAX part of MINIMAX. Finding the MAX output for the AI
            if points > best_score:
                best_move = move
                best_score = points
    # Finding the move which will give the least points to the AI(SAME thing as MAX but it's MIN)
    elif PLAYER == turn:
        best_score = float("inf")
        possible_moves = [
            move
            for move in range(len(board[PLAYER]))
            if is_viable_move(board, move, PLAYER)
        ]

        for move in possible_moves:
            # preforming a deepcopy so we don't accidently overwrite moves by referencing the same list
            board_copy = copy.deepcopy(board)
            board_copy, go_again = move_piece(board_copy, move, turn)

            # mancala is one of those games where you can get two moves.
            # In testing, I found that not decressing the depth for the multimove results in the best AI
            if go_again:
                points, _ = minimax_mancala(board_copy, AI, PLAYER, depth)
            else:
                points, _ = minimax_mancala(board_copy, AI, AI, depth - 1)

            # The MIN part of minimax. Finding the MIN output for the PLAYER
            if points < best_score:
                best_move = move
                best_score = points

    return best_score, best_move
#A function to get the players type (top goes first) show P1 and P2 but actually top and bot 

def get_player_type() -> str:
    while True:
        player_input = input(
            "Please Enter Which Player You Want To Be :\n1. Player 1\n2. Player 2\n:"
        )
        if "quit" in player_input.lower():
            quit()
        elif "1" in player_input:
            return "top"
        elif "2" in player_input:
            return "bot"
        print("Please Make Sure You Are Entering One Of The Two Options Listed.")

def get_player_move(board: dict, turn: str) -> int:
    while True:
        player_move = input("Please Select A Move.\n:")
        if "quit" in player_move.lower():
            quit()
        try:
            player_move = int(player_move) - 1
        except ValueError:
            print("Please Make Sure To Enter A Valid Number.")
            continue

        if is_viable_move(board, player_move, turn):
            return player_move

        print("Sorry, That Is Not A Valid Move.")

def clear_screen() -> None:
    # Clearing screen to make the game visually appealing when updating
    print("\033c", end="")
#######################################################################################################################################################
def main():
    # Default board
    board = {
        "top": [4, 4, 4, 4, 4, 4],
        "bot": [4, 4, 4, 4, 4, 4],
        "top_score": 0,
        "bot_score": 0,
    }

    # Mapping for how confident the algorithm is on winning the game (ballpark)
    total_pieces = sum(board["top"]) + sum(board["bot"])
    winning_confidence_mapping = {
        -(total_pieces // 8): "Terrible",
        -(total_pieces // total_pieces): "Bad",
        total_pieces // 16: "Possible",
        total_pieces // 8: "Good",
        total_pieces + 1: "Certain",
    }

    # Displaying the board so the user know what they are selecting
    print_board(board)
    # Collecting what type the user is
    PLAYER = get_player_type()

    # Some final inits before starting the game
    PRINT_P1 = "YOU" if PLAYER == "top" else "CPU"
    PRINT_P2 = "CPU" if PLAYER == "top" else "YOU"
    AI = "bot" if PLAYER == "top" else "top"
    MAX_DEPTH = 6

    # Top always goes first, feel free to change if you want to be a reble
    turn = "top"

    # visual for what the AI did
    ai_printed_moves = []

    # While the games not over!!!
    while not ((not any(board["top"])) or (not any(board["bot"]))):
        # Players move
        if turn == PLAYER:
            # Getting the players move
            move = get_player_move(board, PLAYER)

            # Updating the board
            board, go_again = move_piece(board, move, PLAYER)

        # AI's move
        elif turn == AI:
            # Getting the AI's move with the Minimax function
            best_score, move = minimax_mancala(board, AI, turn, MAX_DEPTH)

            # Visual aid to show of confident the minimax algorithm is in winning
            winning_confidence = ""
            for score, confidence in winning_confidence_mapping.items():
                if score < best_score:
                    continue
                winning_confidence = confidence
                break
            ai_printed_moves.append(f"\nAI Moved : {move+1}\tChance of Winning : {winning_confidence}")

            # Updating the board
            board, go_again = move_piece(board, move, AI)

        # if the last piece you drop is in your own Mancala, you take another turn.
        if not go_again:
            turn = "bot" if turn == "top" else "top"

        # Shows the new board
        clear_screen()
        if (turn == PLAYER) and ai_printed_moves:
            [print(move) for move in ai_printed_moves]
            ai_printed_moves = []
        print_board(board, PRINT_P1, PRINT_P2)

    # WIN / LOSS / DRAW
    if board[f"{PLAYER}_score"] > board[f"{AI}_score"]:
        print(
            f"Congrats! You won when the AI looks {MAX_DEPTH} moves ahead. Humanity still have some hope at last."
        )
    elif board[f"{PLAYER}_score"] < board[f"{AI}_score"]:
        print(
            f"Nice try, but the machines win this time! Try some other kid's game maybe?."
        )
    else:
        print(f"DRAW! Great game from both of you!")

if __name__ == "__main__":
    main()