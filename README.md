# Bingo App

A simple Streamlit bingo board app with lightweight file-based authentication.

## Setup

1. Create and activate the virtual environment:
   - Windows (PowerShell):
     ```powershell
     python -m venv bingo_venv
     .\bingo_venv\Scripts\Activate.ps1
     ```
   - macOS/Linux:
     ```bash
     python3 -m venv bingo_venv
     source bingo_venv/bin/activate
     ```

2. Install dependencies:
   ```bash
   python -m pip install --upgrade pip
   python -m pip install -r requirements.txt
   ```

3. Run the app:
   ```bash
   streamlit run code/app.py
   ```

## Notes

- User accounts are stored in `users.json`.
- Saved boards are stored under `boards/`.
- This repository is a prototype and uses file-based persistence, which is not intended for production use.
- `start.sh` provides a quick startup script for shell environments.
