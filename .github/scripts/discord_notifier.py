import os
import requests
import json

# Configurações do webhook e variáveis de ambiente
webhook_url = os.getenv('DISCORD_WEBHOOK_URL')
title = os.getenv('TITLE')
description = os.getenv('DESCRIPTION')
fields_str = os.getenv('FIELDS')
severity = os.getenv('COLOR')

repository_name = os.getenv("REPOSITORY_NAME")
workflow_name = os.getenv("WORKFLOW_NAME")
branch_selected = os.getenv("GITHUB_REF_NAME")
build_number = os.getenv("WORKFLOW_BUILD")

# Conversão de severidade para cor
severity_colors = {
    'INFO': 3447003,  # Azul
    'WARN': 16776960,  # Amarelo
    'ERROR': 15158332  # Vermelho
}
color = severity_colors.get(severity.upper(), 3447003)  # Padrão para Azul se a severidade não for reconhecida

# Campos padrão
default_fields = [
    {
        "name": "Repository",
        "value": repository_name,
        "inline": "false",
    },
    {
        "name": "Workflow",
        "value": workflow_name,
        "inline": "true",
    },
    {
        "name": "Ref",
        "value": branch_selected,
        "inline": "true",
    },
    {
        "name": "Build",
        "value": build_number,
        "inline": "true",
    }
]

# Concatenação de campos adicionais fornecidos
additional_fields = json.loads(fields_str) if fields_str else []
all_fields = default_fields + additional_fields

if not webhook_url:
    raise ValueError("DISCORD_WEBHOOK_URL is not set")

def send_discord_notification(webhook, message_title, desc, fields_list, severity_color):
    embed = {
        "title": message_title,
        "description": desc,
        "color": severity_color,
        "fields": fields_list
    }

    data = {
        "embeds": [embed]
    }

    headers = {
        "Content-Type": "application/json"
    }

    response = requests.post(webhook, headers=headers, data=json.dumps(data))

    if response.status_code != 204:
        raise Exception(f"Failed to send notification. Status code: {response.status_code}, Response: {response.text}")

send_discord_notification(webhook_url, title, description, all_fields, color)