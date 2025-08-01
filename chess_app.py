import streamlit as st
import pandas as pd
import numpy as np

# Initialize session state for game
if 'board' not in st.session_state:
    st.session_state.board = None
if 'selected_piece' not in st.session_state:
    st.session_state.selected_piece = None
if 'current_player' not in st.session_state:
    st.session_state.current_player = 'white'
if 'game_over' not in st.session_state:
    st.session_state.game_over = False

def initialize_board():
    """Initialize the chess board with pieces in starting positions"""
    board = [['' for _ in range(8)] for _ in range(8)]
    
    # Set up pawns
    for col in range(8):
        board[1][col] = '♟'  # Black pawns
        board[6][col] = '♙'  # White pawns
    
    # Set up other pieces
    black_pieces = ['♜', '♞', '♝', '♛', '♚', '♝', '♞', '♜']
    white_pieces = ['♖', '♘', '♗', '♕', '♔', '♗', '♘', '♖']
    
    for col in range(8):
        board[0][col] = black_pieces[col]
        board[7][col] = white_pieces[col]
    
    return board

def is_valid_move(board, start_pos, end_pos, player):
    """Basic move validation (simplified for demo)"""
    start_row, start_col = start_pos
    end_row, end_col = end_pos
    
    # Check if positions are within board
    if not (0 <= start_row <= 7 and 0 <= start_col <= 7 and 
            0 <= end_row <= 7 and 0 <= end_col <= 7):
        return False
    
    # Check if start position has a piece
    if board[start_row][start_col] == '':
        return False
    
    # Check if piece belongs to current player
    piece = board[start_row][start_col]
    if player == 'white' and piece in '♜♞♝♛♚♟':
        return False
    if player == 'black' and piece in '♖♘♗♕♔♙':
        return False
    
    # Check if end position is occupied by own piece
    target_piece = board[end_row][end_col]
    if target_piece != '':
        if player == 'white' and target_piece in '♖♘♗♕♔♙':
            return False
        if player == 'black' and target_piece in '♜♞♝♛♚♟':
            return False
    
    return True

def make_move(board, start_pos, end_pos):
    """Make a move on the board"""
    start_row, start_col = start_pos
    end_row, end_col = end_pos
    
    board[end_row][end_col] = board[start_row][start_col]
    board[start_row][start_col] = ''

def create_board_display(board):
    """Create a visual representation of the board"""
    # Create a DataFrame for display
    df = pd.DataFrame(board, 
                     index=[8-i for i in range(8)], 
                     columns=['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'])
    return df

def main():
    st.title("♔ Chess Game ♔")
    
    # Initialize board if not already done
    if st.session_state.board is None:
        st.session_state.board = initialize_board()
    
    # Sidebar for game controls
    st.sidebar.header("Game Controls")
    
    if st.sidebar.button("New Game"):
        st.session_state.board = initialize_board()
        st.session_state.selected_piece = None
        st.session_state.current_player = 'white'
        st.session_state.game_over = False
        st.rerun()
    
    # Display current player
    st.sidebar.subheader(f"Current Player: {st.session_state.current_player.title()}")
    
    # Display the board
    st.subheader("Chess Board")
    
    # Create the board display
    board_df = create_board_display(st.session_state.board)
    
    # Display board with clickable cells
    cols = st.columns(8)
    
    for col_idx, col in enumerate(cols):
        with col:
            for row_idx in range(8):
                piece = st.session_state.board[row_idx][col_idx]
                cell_color = "white" if (row_idx + col_idx) % 2 == 0 else "lightgray"
                
                # Create a button for each cell
                if st.button(
                    piece if piece else " ",
                    key=f"cell_{row_idx}_{col_idx}",
                    help=f"Click to select/move piece at {chr(97+col_idx)}{8-row_idx}"
                ):
                    if st.session_state.selected_piece is None:
                        # Select piece
                        if piece != '':
                            st.session_state.selected_piece = (row_idx, col_idx)
                            st.success(f"Selected piece at {chr(97+col_idx)}{8-row_idx}")
                    else:
                        # Try to move piece
                        start_pos = st.session_state.selected_piece
                        end_pos = (row_idx, col_idx)
                        
                        if is_valid_move(st.session_state.board, start_pos, end_pos, st.session_state.current_player):
                            make_move(st.session_state.board, start_pos, end_pos)
                            st.session_state.current_player = 'black' if st.session_state.current_player == 'white' else 'white'
                            st.success(f"Move from {chr(97+start_pos[1])}{8-start_pos[0]} to {chr(97+end_pos[1])}{8-end_pos[0]}")
                        else:
                            st.error("Invalid move!")
                        
                        st.session_state.selected_piece = None
                        st.rerun()
    
    # Display selected piece info
    if st.session_state.selected_piece:
        row, col = st.session_state.selected_piece
        st.info(f"Selected piece at {chr(97+col)}{8-row}: {st.session_state.board[row][col]}")
    
    # Instructions
    st.markdown("---")
    st.markdown("""
    ### How to Play:
    1. Click on a piece to select it
    2. Click on a destination square to move the piece
    3. Players alternate turns (White starts)
    4. Use the 'New Game' button to reset the board
    
    ### Piece Legend:
    - ♔♚: Kings
    - ♕♛: Queens  
    - ♖♜: Rooks
    - ♗♝: Bishops
    - ♘♞: Knights
    - ♙♟: Pawns
    """)

if __name__ == "__main__":
    main() 