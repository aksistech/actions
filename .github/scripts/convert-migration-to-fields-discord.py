import os
import json

# Lê o caminho do JSON a partir da variável de ambiente
json_path = os.getenv('JSON_PATH')

if not json_path or not os.path.exists(json_path):
    raise ValueError("JSON_PATH is not set or the file does not exist")

# Lê o conteúdo do JSON
with open(json_path, 'r') as file:
    data = json.load(file)

# Campos adicionais a serem adicionados
fields = [
    {
        "name": "Status",
        "value": data['success'],
        "inline": "true"
    },
    {
        "name": "TargetVersion",
        "value": data['targetSchemaVersion'],
        "inline": "true"
    },
    {
        "name": "Executions",
        "value": data['migrationsExecuted'],
        "inline": "true"
    }
]

# Adiciona as migrações ao array de fields
for i, migration in enumerate(data.get('migrations', [])):
    fields.append({
        "name": f"Migration {i+1}",
        "value": f"{migration['version']} - {migration['description']}",
        "inline": "false"
    })

# Salva o resultado em um novo arquivo JSON
output_path = os.getenv('OUTPUT_PATH', 'output_fields.json')

with open(output_path, 'w') as outfile:
    json.dump(fields, outfile, indent=4)

print(f"Fields successfully saved to {output_path}")
