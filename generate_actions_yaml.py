import os
import json
import yaml

SCHEMA_ROOT = "./schemas"
MODULE_PATH = os.path.join(SCHEMA_ROOT, "modules")
OUTPUT_FILE = "actions.yaml"
BASE_URL = "https://patrickkunze.github.io/pflegegutachten/schemas/"

def load_schema(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)

def build_action_entry(schema_file, schema):
    name = os.path.splitext(os.path.basename(schema_file))[0]
    return {
        "path": f"/use_{name}",
        "method": "post",
        "summary": schema.get("title", name),
        "operationId": f"use_{name}",
        "requestBody": {
            "required": True,
            "content": {
                "application/json": {
                    "schema": {
                        "$ref": f"./modules/{os.path.basename(schema_file)}"
                    }
                }
            }
        },
        "responses": {
            "200": {
                "description": f"Antwort zu {name}"
            }
        }
    }

def main():
    action_definitions = {
        "openapi": "3.1.0",
        "info": {
            "title": "PflegeGutachtenGPT",
            "version": "1.0",
            "description": "Automatisch generierte API für strukturierte Pflegegutachtenmodule"
        },
        "servers": [
            {
                "url": BASE_URL,
                "description": "Bereitgestellte Pflegebegutachtungs-Schemata"
            }
        ],
        "paths": {}
    }

    for file in os.listdir(MODULE_PATH):
        if file.endswith(".schema.json"):
            full_path = os.path.join(MODULE_PATH, file)
            schema = load_schema(full_path)
            entry = build_action_entry(file, schema)
            path = entry.pop("path")
            method = entry.pop("method")
            action_definitions["paths"][path] = {method: entry}

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        yaml.dump(action_definitions, f, allow_unicode=True, sort_keys=False)

    print(f"✅ {OUTPUT_FILE} erfolgreich erzeugt.")

if __name__ == "__main__":
    main()