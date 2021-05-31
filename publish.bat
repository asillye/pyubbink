python -m venv ./.venv
.venv\Scripts\activate.bat
python -m pip install --upgrade pip
python -m pip install --upgrade build
pip install -r requirements.txt
python -m build