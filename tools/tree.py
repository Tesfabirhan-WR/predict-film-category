from pathlib import Path

IGNORE = {".git", ".venv", "venv", "__pycache__", "node_modules", "kt_logs", ".ipynb_checkpoints"}
MAX_DEPTH = 3


def tree(folder: Path, prefix: str = "", depth: int = 0):
    if depth >= MAX_DEPTH:
        return
    items = sorted((p for p in folder.iterdir() if p.name not in IGNORE),
                   key=lambda p: (p.is_file(), p.name.lower()))
    for i, p in enumerate(items):
        last = i == len(items) - 1
        print(prefix + ("└── " if last else "├── ") + p.name + ("/" if p.is_dir() else ""))
        if p.is_dir():
            tree(p, prefix + ("    " if last else "│   "), depth + 1)


print(Path.cwd().name + "/")
tree(Path.cwd())