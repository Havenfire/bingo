if [ ! -d "bingo_venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv bingo_venv
fi

# Cross-platform activate
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    source bingo_venv/Scripts/activate
else
    source bingo_venv/bin/activate
fi

if [ -f "requirements.txt" ]; then
    echo "Installing dependencies..."
    python -m pip install --upgrade pip
    python -m pip install -r requirements.txt
fi
echo "Starting app..."
streamlit run code/app.py