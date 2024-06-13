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
        "value": str(data['success']),
        "inline": "true"
    },
    {
        "name": "TargetVersion",
        "value": data['targetSchemaVersion'],
        "inline": "true"
    },
    {
        "name": "Executions",
        "value": str(data['migrationsExecuted']),
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

# Converte os campos em uma string JSON
fields_json = json.dumps(fields)

# Salva a string JSON em uma variável de ambiente
print(f"::set-output name=fields::{fields_json}")