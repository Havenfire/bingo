import streamlit as st
import json
import os
from streamlit_extras.stylable_container import stylable_container
from streamlit_option_menu import option_menu

BOARD_SIZE = 5
FILENAME = "bingo_board.json"

os.makedirs("boards", exist_ok=True)


def make_empty_board():
    return [["" for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]


def make_empty_marks():
    return [[False for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]

def save_board(board, marked):
    filename = user_file()
    if filename is None:
        st.warning("Login required to save.")
        return

    os.makedirs("boards", exist_ok=True)
    with open(filename, "w") as f:
        json.dump({"board": board, "marked": marked}, f)
    st.success("Board saved!")


def load_board():
    filename = user_file()
    if filename and os.path.exists(filename):
        try:
            with open(filename, "r") as f:
                data = json.load(f)
            return data.get("board", make_empty_board()), data.get("marked", make_empty_marks())
        except Exception:
            return make_empty_board(), make_empty_marks()

    return make_empty_board(), make_empty_marks()



def check_bingo(marked):
    wins = []
    for i in range(BOARD_SIZE):
        if all(marked[i]):
            wins.append([(i, j) for j in range(BOARD_SIZE)])
    for j in range(BOARD_SIZE):
        if all(marked[i][j] for i in range(BOARD_SIZE)):
            wins.append([(i, j) for i in range(BOARD_SIZE)])
    if all(marked[i][i] for i in range(BOARD_SIZE)):
        wins.append([(i, i) for i in range(BOARD_SIZE)])
    if all(marked[i][BOARD_SIZE - 1 - i] for i in range(BOARD_SIZE)):
        wins.append([(i, BOARD_SIZE - 1 - i) for i in range(BOARD_SIZE)])
    return wins

def user_file():
    """Creates a safe filename based on email."""
    email = st.session_state.get("user")
    if not email:
        return None
    safe = email.replace("@", "_at_").replace(".", "_dot_")
    return f"boards/{safe}.json"


# --- Session state ---
if "board" not in st.session_state:
    st.session_state.board = make_empty_board()

if "marked" not in st.session_state:
    st.session_state.marked = make_empty_marks()

if "enabled" not in st.session_state:
    st.session_state.enabled = False

if "user" not in st.session_state:
    st.session_state.user = None  # Logged-out by default


# ---- Global Styling ----
st.markdown("""
    <style>
        /* Page background */
        .stApp {
            background: linear-gradient(135deg, #f3f4f6 0%, #dbeafe 100%);
        }

        /* Soften default text colors */
        html, body, [class*="css"]  {
            color: #1f2937 !important;
        }

        /* Card-like look for expanders and containers */
        .st-expander, .stContainer, .block-container {
            background: rgba(255, 255, 255, 0.65) !important;
            backdrop-filter: blur(8px);
            border-radius: 12px;
            padding: 1rem 1.5rem;
        }

        /* Cleaner top padding */
        .block-container {
            padding-top: 2rem;
            padding-bottom: 2.5rem !important;
        }

        /* Menu bar polish */
        .nav-item > a {
            font-weight: 600 !important;
        }
    </style>
""", unsafe_allow_html=True)


# --- Navigation Menu ---
page = option_menu(
    None,
    ["Your Board", "Friends", "Tasks", "Settings"],
    icons=["house", "person", "list-task", "gear"],
    menu_icon="cast",
    default_index=0,
    orientation="horizontal",
    key="nav_menu"
)

st.title("New Year's Bingo Board")


with st.expander("🔐 Login / Save Progress", expanded=False):
    if st.session_state.user:
        st.write(f"Logged in as **{st.session_state.user}**")
        if st.button("Log Out"):
            st.session_state.user = None
            st.rerun()
    else:
        email = st.text_input("Email to link your board")
        if st.button("Log In"):
            if email.strip():
                st.session_state.user = email.strip().lower()
                # Load this user's saved board (if exists)
                st.session_state.board, st.session_state.marked = load_board()
                st.success(f"Logged in as {email}")
                st.rerun()
            else:
                st.warning("Enter a valid email.")


# --- Page Logic ---
if page == "Your Board":
    # ---- Board page ----
    if not st.session_state.enabled:
        st.subheader("Step 1 — Fill out your board")

        with st.container():
            col1, col2, col3 = st.columns([1, 1, 1])
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
            with col3:
                if st.button("⚙️ Settings"):
                    st.session_state.nav_menu = "Settings"
                    st.rerun()

        for i in range(BOARD_SIZE):
            cols = st.columns(BOARD_SIZE, gap=None)
            for j in range(BOARD_SIZE):
                key = f"text_{i}_{j}"
                with cols[j]:
                    with stylable_container(
                        f"input_cell_{i}_{j}",
                        css_styles="""
                            div[data-testid="stMarkdownContainer"] + div {
                                display: flex;
                                align-items: center;
                                justify-content: center;
                            }
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
                            label { display: none; }
                        """,
                    ):
                        st.session_state.board[i][j] = st.text_area(
                            label="",
                            value=st.session_state.board[i][j],
                            key=key,
                            height=120,
                            placeholder="",
                            label_visibility="collapsed",
                            max_chars=55,
                        )

    else:
        st.subheader("Step 2 — Play Mode")

        if st.button("🔧 Edit Board"):
            st.session_state.enabled = False
            st.rerun()

        winning_lines = check_bingo(st.session_state.marked)
        has_bingo = len(winning_lines) > 0

        for i in range(BOARD_SIZE):
            cols = st.columns(BOARD_SIZE, gap=None)
            for j in range(BOARD_SIZE):
                label = st.session_state.board[i][j]
                marked = st.session_state.marked[i][j]
                if any((i, j) in line for line in winning_lines):
                    color = "#FFD700"
                elif marked:
                    color = "#00FF00"
                else:
                    color = "#E9ECEF"

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

        if has_bingo:
            st.success("🎉 BINGO! You got it! 🎉")

        st.divider()
        c1, c2 = st.columns(2)
        with c1:
            if st.button("💾 Save Board & Marks"):
                save_board(st.session_state.board, st.session_state.marked)
        with c2:
            if st.button("Clear Marks"):
                st.session_state.marked = make_empty_marks()
                st.rerun()


elif page == "Friends":
    st.subheader("👥 Friends List")
    st.info("Friend management will go here.")


elif page == "Tasks":
    st.subheader("📝 Tasks")
    st.info("Your bingo-related challenges will appear here.")


elif page == "Settings":
    st.subheader("⚙️ Settings")
    st.info("App settings and preferences will appear here.")
