if [ ! -d "bingo_venv" ]; then
    echo "Creating virtual environment..."
    python -m venv bingo_venv
fi
source bingo_venv/Scripts/activate
if [ -f "requirements.txt" ]; then
    echo "Installing dependencies..."
    python.exe -m pip install --upgrade pip
    pip install uv
    uv pip install -r requirements.txt
fi

echo "Starting app..."
streamlit run code/app.py