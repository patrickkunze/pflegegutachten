import os
import json

SCHEMA_ROOT = "./schemas"
MODULE_PATH = os.path.join(SCHEMA_ROOT, "modules")

def load_schema(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)

def schema_to_function(name, schema, relative_path):
    return {
        "name": f"use_{name}",
        "description": schema.get("description", schema.get("title", name)),
        "parameters": {
            "$ref": relative_path.replace("\\", "/")  # für Windows-kompatible Pfade
        }
    }

def collect_functions(schema_dir):
    functions = []
    for root, _, files in os.walk(schema_dir):
        for file in files:
            if file.endswith(".schema.json"):
                full_path = os.path.join(root, file)
                relative_path = os.path.relpath(full_path, SCHEMA_ROOT)
                schema = load_schema(full_path)
                base_name = os.path.splitext(file)[0]
                function = schema_to_function(base_name, schema, relative_path)
                functions.append(function)
    return functions

def main():
    functions = collect_functions(SCHEMA_ROOT)
    output = {
        "functions": functions
    }

    with open("generated_functions.json", "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print("✅ functions.json erfolgreich erzeugt.")

if __name__ == "__main__":
    main()