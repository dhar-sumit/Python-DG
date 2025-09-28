import re
import json
import sys
from pathlib import Path

def extract_tables(sql):
    tables = []
    pattern = re.compile(r"CREATE\s+TABLE\s+(\w+)\s*\((.*?)\);", re.IGNORECASE | re.DOTALL)
    matches = pattern.findall(sql)
    for name, cols in matches:
        columns = []
        for col in re.split(r",\s*(?![^()]*\))", cols):
            col = col.strip()
            if col:
                parts = col.split(None, 1)  # split into name + type
                if len(parts) == 2:
                    columns.append({"name": parts[0], "type": parts[1]})
        tables.append({"name": name, "columns": columns})
    return tables

def extract_procedures(sql):
    # Extract procedures (with full definition)
    procedure_pattern = re.compile(
        r"CREATE\s+PROCEDURE\s+([A-Za-z0-9_]+)\s*(.*?)\s*AS\s*BEGIN(.*?)END;",
        re.IGNORECASE | re.DOTALL
    )
    procedures = []
    for match in procedure_pattern.finditer(sql):
        name = match.group(1).strip()
        params = match.group(2).strip()
        body = match.group(3).strip()
        query = f"CREATE PROCEDURE {name} {params} AS BEGIN {body} END;"
        definition = " ".join(query.split())
        parameters = [p.strip() for p in params.replace("\n", " ").split(",") if p.strip()]
        procedures.append({
            "name": name,
            "params": parameters,
            "definition": definition
        })
    return procedures


def extract_views(sql):
    views = []
    pattern = re.compile(r"CREATE\s+VIEW\s+(\w+)\s+AS\s+(.*?);", re.IGNORECASE | re.DOTALL)
    matches = pattern.findall(sql)
    for name, definition in matches:
        views.append({"name": name, "definition": definition.strip()+";"})
    return views


def extract_inserts(sql):
    inserts = []
    pattern = re.compile(r"(INSERT\s+INTO\s+\w+\s*\(.*?\)\s*VALUES\s*\(.*?\);)", re.IGNORECASE | re.DOTALL)
    matches = pattern.findall(sql)
    for query in matches:
        inserts.append({"type": "INSERT", "query": query.strip()})
    return inserts


def extract_updates(sql):
    updates = []
    pattern = re.compile(r"(UPDATE\s+\w+\s+SET\s+.*?\s+WHERE\s+.*?;)", re.IGNORECASE | re.DOTALL)
    matches = pattern.findall(sql)
    for query in matches:
        updates.append({"type": "UPDATE", "query": query.strip()})
    return updates


def extract_deletes(sql):
    deletes = []
    pattern = re.compile(r"(DELETE\s+FROM\s+\w+\s+WHERE\s+.*?;)", re.IGNORECASE | re.DOTALL)
    matches = pattern.findall(sql)
    for query in matches:
        deletes.append({"type": "DELETE", "query": query.strip()})
    return deletes


def main():
    input_dir = Path("sql_files")
    output_dir = Path("json_files")
    
    input_dir.mkdir(parents=True, exist_ok=True)
    output_dir.mkdir(parents=True, exist_ok=True)

    sql_files = list(input_dir.glob("*.sql"))

    if not sql_files:
        print("No '.sql' files found in sql_files directory. Please add some SQL files and try again.")
        return

    for sql_file in sql_files:
        print(f"Processing: {input_dir}/{sql_file.name}", end="")
        sql = sql_file.read_text()

        output = {
            "tables": extract_tables(sql),
            "procedures": extract_procedures(sql),
            "views": extract_views(sql),
            "dml": extract_inserts(sql) + extract_updates(sql) + extract_deletes(sql)
        }

        output_file = output_dir / (sql_file.stem + ".json")

        with output_file.open("w", encoding="utf-8") as f:
            json.dump(output, f, indent=4)

        print(f" → Saved to: {output_file}")

    print(f"\nExtraction complete! JSON saved to {output_dir}")


if __name__ == "__main__":
    main()
