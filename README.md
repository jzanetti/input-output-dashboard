# Preflight — what to prepare
Make sure your project has a requirements.txt (do this locally if needed):
```
pip freeze > requirements.txt
```
Ensure layout and process are importable Python packages (if they’re directories, add an empty __init__.py inside each):
```
layout/__init__.py
process/__init__.py
```
Ensure your app.py exposes the Flask server object. Example pattern (see more below).