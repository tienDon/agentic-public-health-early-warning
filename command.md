uv init
uv venv
.\.venv\Scripts\activate
uv add -r .\requirements.txt
uv add ipykernel
ReAct Architecture


## update requirements file
uv pip compile pyproject.toml -o requirements.txt

uvicorn app.main:app --reload