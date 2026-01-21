from pathlib import Path

folders = [
    "backend",
    "agent",
    "ui",
    "tests/unit",
    "tests/integration",
    "tests/data",
]

files = [
    "backend/__init__.py",
    "backend/main.py",
    "backend/config.py",
    "agent/__init__.py",
    "agent/agent.py",
    "ui/__init__.py",
    "ui/app.py",
    "README.md",
    ".env.example",
    ".gitignore",
]

for folder in folders:
    Path(folder).mkdir(parents=True, exist_ok=True)

for file in files:
    Path(file).touch()

print("Project structure initialized.")