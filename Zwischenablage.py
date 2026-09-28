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






# ReAct-Schleife 

SYSTEM_PROMPT = "Du beantwortest meine Fragen. Nutze die Werkzeuge. Antworte am Ende kurz auf Deutsch."

def react_loop(frage:str , max_steps: int = 10 ) -> str: # später max_steps = 90
    messages=[{"role": "system", "content":SYSTEM_PROMPT},{"role": "user", "content":frage}]
    step = 0
    while step < max_steps:
        step += 1 
        response = client.chat.completions.create( 
            model=LLM_MODEL,
            messages=messages,
            temperature=.3,
            max_tokens=200,
            tools=TOOLS_SCHEMA,
)
        msg = response.choices[0].message
        messages.append({
            "role": "assistant", "content": msg.content or "",
            "tool_calls": [tc.model_dump() for tc in msg.tool_calls or []]
            }) # Chat-Historie

        # Hat die Antwort Tool Calls? 
        if msg.tool_calls:

            for tool_call in msg.tool_calls:
                args = json.loads(tool_call.function.arguments or "{}")
                ergebnis = TOOLS[tool_call.function.name](**args) 
                messages.append({"role": "tool", "tool_call_id": tool_call.id, "content": str(ergebnis)}) # Tool Ergebnisse

            
        # Kein Tool Call: Das Modell hat genug Informationen und wir sind bei der finalen Antwort 
        else:
            return msg.content

    return "Abbruch: max_steps erreicht"


antwort = react_loop(frage)

antwort
    
