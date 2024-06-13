import json
import sys
import os

json_content = os.environ['JSON_CONTENT']
name_principal = os.environ['NAME']
name_database = os.environ['DATABASE']

def find_database(name_principal, name_database):
    data = json.loads(json_content)

    # Find the principal entry
    principal = next((item for item in data if item["name"] == name_principal), None)
    if principal is None:
        raise ValueError(f"No principal found with name: {name_principal}")

    # Find the database entry
    database = next((db for db in principal["databases"] if db["name"] == name_database), None)
    if database is None:
        raise ValueError(f"No database found with name: {name_database} in principal: {name_principal}")

    return principal, database


try:
    principal, database = find_database(name_principal, name_database)
    print("Principal found:", principal)
    print("Database found:", database)
except ValueError as e:
    print(e)
    sys.exit(1)
