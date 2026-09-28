# Tools geben 

def list_files(directory: str) -> str:
    """Listet die Datein in einem Unterordner von DATA_DIR"""
    return "\n".join(sorted(p.name for p in (DATA_DIR / directory).iterdir()))

def read_file(path: str) -> str:
    """Gibt den Inhalt einer Datei aus DATA_DIR zurück."""
    return (DATA_DIR / path).read_text(encoding="utf-8")

def count_lines(path: str) -> str:
    """Zählt die Zeilen einer Datei aus DATA_DIR."""
    return len(read_file(path).splitlines())

# Dispatcher 
TOOLS = {"list_files": list_files, "read_file": read_file, "count_lines": count_lines }

TOOLS_SCHEMA = [
    {"type": "function", "function": {
        "name": "list_files",
        "description": "Listet die Dateien im Datenordner (oder einem Unterordner davon).",
        "parameters": {"type": "object", "properties": {
            "directory": {"type": "string", "description": "Unterordner relativ zum Datenordner, '.' für die Wurzel"}},
            "required": []}}},
    {"type": "function", "function": {
        "name": "read_file",
        "description": "Gibt den vollständigen Inhalt einer Datei im Datenordner zurück.",
        "parameters": {"type": "object", "properties": {
            "path": {"type": "string", "description": "Dateiname relativ zum Datenordner, z.B. 'beispiel.py'"}},
            "required": ["path"]}}},
    {"type": "function", "function": {
        "name": "count_lines",
        "description": "Zählt die Zeilen einer Datei im Datenordner.",
        "parameters": {"type": "object", "properties": {
            "path": {"type": "string", "description": "Dateiname relativ zum Datenordner"}},
            "required": ["path"]}}},
]
