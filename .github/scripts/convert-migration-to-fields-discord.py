import os
import json

# Lê o caminho do JSON a partir da variável de ambiente
json_path = os.getenv('JSON_PATH')
output_path = os.getenv('OUTPUT_PATH', 'additional_fields.json')

if not json_path or not os.path.exists(json_path):
    raise ValueError("JSON_PATH is not set or the file does not exist")

# Lê o conteúdo do JSON
with open(json_path, 'r') as file:
    data = json.load(file)

# Lê os parâmetros fornecidos como entrada
parameters = os.getenv('INPUT_PARAMETERS')
if parameters:
    parameters = json.loads(parameters)
else:
    parameters = []

# Campos adicionais a serem adicionados
additional_fields = []

# Função para adicionar campos apenas se o valor não for None
def add_field(name, value, inline):
    if value is not None:
        additional_fields.append({
            "name": name,
            "value": str(value),
            "inline": inline
        })

add_field("Success", data.get('success'), True)
add_field("TargetVersion", data.get('targetSchemaVersion'), True)
add_field("Executions", data.get('migrationsExecuted'), True)

# Adiciona as migrações ao array de additional_fields, somente se o valor não for null
if data.get('migrations'):
    for i, migration in enumerate(data['migrations']):
        if migration['version'] and migration['description']:
            additional_fields.append({
                "name": f"Migration {i+1}",
                "value": f"{migration['version']} - {migration['description']}",
                "inline": False
            })

# Combina os parâmetros com os campos adicionais, garantindo que os parâmetros venham primeiro
combined_fields = parameters + additional_fields

# Salva os campos combinados em uma única linha de JSON
with open(output_path, 'w') as outfile:
    json.dump(combined_fields, outfile)

print(f"Combined fields saved to {output_path}")
