# Progress documentation

Will be tracking where I stopped here.

1. Create & activate python venv using vscode PS terminal:
```
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

2. Create a basic API gateway:

3. 
4. 

# Error documentation

1. Command (PS terminal):
```
python .\app\main.py
```

Error:
> ERROR: Error loading ASGI app. Could not import module "app.app".

Fixed: moving the main.py outside app.py. Used a 'flat structure' which allows uvicorn to see main immediately as I run everything from the the project folder. No need for an __init__.py.
