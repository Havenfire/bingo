import streamlit as st
import json
import os
from streamlit_extras.stylable_container import stylable_container

st.set_page_config(page_title="Bingo Board", layout="centered")

BOARD_SIZE = 5
FILENAME = "bingo_board.json"


def make_empty_board():
    return [["" for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]


def make_empty_marks():
    return [[False for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]


def save_board(board, marked):
    with open(FILENAME, "w") as f:
        json.dump({"board": board, "marked": marked}, f)
    st.success("Board saved!")


def load_board():
    if os.path.exists(FILENAME):
        try:
            with open(FILENAME, "r") as f:
                data = json.load(f)
            return data.get("board", make_empty_board()), data.get("marked", make_empty_marks())
        except Exception:
            return make_empty_board(), make_empty_marks()
    return make_empty_board(), make_empty_marks()


def check_bingo(marked):
    """Return list of winning line coordinates (row, col) tuples."""
    wins = []

    # Rows
    for i in range(BOARD_SIZE):
        if all(marked[i]):
            wins.append([(i, j) for j in range(BOARD_SIZE)])

    # Columns
    for j in range(BOARD_SIZE):
        if all(marked[i][j] for i in range(BOARD_SIZE)):
            wins.append([(i, j) for i in range(BOARD_SIZE)])

    # Diagonals
    if all(marked[i][i] for i in range(BOARD_SIZE)):
        wins.append([(i, i) for i in range(BOARD_SIZE)])
    if all(marked[i][BOARD_SIZE - 1 - i] for i in range(BOARD_SIZE)):
        wins.append([(i, BOARD_SIZE - 1 - i) for i in range(BOARD_SIZE)])

    return wins


# --- Session state ---
if "board" not in st.session_state:
    board, marked = load_board()
    st.session_state.board = board
    st.session_state.marked = marked
if "enabled" not in st.session_state:
    st.session_state.enabled = False

st.title("🎯 5×5 Bingo Board")

# --- Setup phase ---


if not st.session_state.enabled:
    st.subheader("Step 1 — Fill out your board")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("✅ Enable Board"):
            if all(cell.strip() for row in st.session_state.board for cell in row):
                st.session_state.enabled = True
                st.rerun()
            else:
                st.warning("Please fill every square before enabling the board.")
    with col2:
        if st.button("💾 Save Board"):
            save_board(st.session_state.board, st.session_state.marked)
   

    for i in range(BOARD_SIZE):
        cols = st.columns(BOARD_SIZE, gap="small")
        for j in range(BOARD_SIZE):
            key = f"text_{i}_{j}"
            with cols[j]:
                # Wrap the input in a stylable container so we can apply identical styles
                with stylable_container(
                    f"input_cell_{i}_{j}",
                    css_styles="""
                        /* Container ensures consistent sizing */
                        div[data-testid="stMarkdownContainer"] + div {
                            display: flex;
                            align-items: center;
                            justify-content: center;
                        }

                        /* Style the textarea to match the play-mode button */
                        textarea {
                            width: 120px !important;
                            height: 120px !important;
                            background-color: #f5f5f5;
                            color: black;
                            border: 1px solid #ccc;
                            border-radius: 8px;
                            font-size: 14px;
                            padding: 8px;
                            resize: none;             
                            line-height: 1.2;
                            word-wrap: break-word;
                            white-space: normal;
                            text-align: center;    
                        }

                        /* Hide default label spacing */
                        label { display: none; }
                    """,
                ):
                    # Use text_area to get controllable height and wrapping
                    st.session_state.board[i][j] = st.text_area(
                        label="",
                        value=st.session_state.board[i][j],
                        key=key,
                        height=120,       # matches the button height
                        placeholder="",
                        label_visibility="collapsed",
                        max_chars=55,
                    )



# --- Play phase ---
else:
    st.subheader("Step 2 — Play Mode")

    if st.button("🔧 Edit Board"):
        st.session_state.enabled = False
        st.rerun()

    # Check for bingo
    winning_lines = check_bingo(st.session_state.marked)
    has_bingo = len(winning_lines) > 0

    if has_bingo:
        st.success("🎉 BINGO! You got it! 🎉")

    for i in range(BOARD_SIZE):
        cols = st.columns(BOARD_SIZE, gap="small")
        for j in range(BOARD_SIZE):
            label = st.session_state.board[i][j]
            marked = st.session_state.marked[i][j]

            # Determine cell color
            if any((i, j) in line for line in winning_lines):
                color = "#FFD700"  # gold for winning cells
            elif marked:
                color = "#00FF00"  # green for marked
            else:
                color = "#E9ECEF"  # gray default

            with cols[j]:
                with stylable_container(
                    f"cell_{i}_{j}",
                    css_styles=f"""
                        button {{
                            background-color: {color};
                            color: black;
                            border-radius: 8px;
                            width: 120px;
                            height: 120px;
                            font-size: 14px;
                            word-wrap: break-word;
                            white-space: normal;
                        }}
                    """,
                ):
                    clicked = st.button(label, key=f"btn_{i}_{j}")
                    if clicked:
                        st.session_state.marked[i][j] = not st.session_state.marked[i][j]
                        st.rerun()

    st.divider()
    c1, c2 = st.columns(2)
    with c1:
        if st.button("💾 Save Board & Marks"):
            save_board(st.session_state.board, st.session_state.marked)
    with c2:
        if st.button("Clear Marks"):
            st.session_state.marked = make_empty_marks()
            st.rerun()
