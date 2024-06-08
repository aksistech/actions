import boto3
import os
import argparse

# Configura o argparse para obter o IP da linha de comando
parser = argparse.ArgumentParser(description='Adiciona um IP a um Security Group baseado em uma tag.')
parser.add_argument('ip_address', type=str, help='Endereço IP a ser adicionado ao Security Group')

# Analisa os argumentos de linha de comando
args = parser.parse_args()
ip_address = args.ip_address

# Obtém as variáveis de ambiente
region = os.environ['REGION']
description = os.environ['KEY']
tag_key = os.environ['TAG_KEY']
tag_value = os.environ['TAG_VALUE']

def get_security_group_id_by_tag(tag_key, tag_value, region_name):
    # Cria uma sessão usando o Boto3
    session = boto3.Session(region_name=region_name)

    # Cria um cliente EC2
    ec2 = session.client('ec2')

    try:
        # Descreve os security groups com base na tag
        response = ec2.describe_security_groups(
            Filters=[
                {
                    'Name': f'tag:{tag_key}',
                    'Values': [tag_value]
                }
            ]
        )

        # Verifica se encontrou algum security group
        security_groups = response.get('SecurityGroups', [])
        if not security_groups:
            raise ValueError(f"Nenhum Security Group encontrado com a tag {tag_key}: {tag_value}")

        # Retorna o ID do primeiro security group encontrado
        return security_groups[0]['GroupId']
    except Exception as e:
        print(f"Erro ao buscar Security Group por tag: {e}")
        return None

def add_ip_to_security_group(security_group_id, ip, description, region_name='us-west-2'):
    # Cria uma sessão usando o Boto3
    session = boto3.Session(region_name=region_name)

    # Cria um cliente EC2
    ec2 = session.client('ec2')

    try:
        # Adiciona a regra de entrada ao security group
        ec2.authorize_security_group_ingress(
            GroupId=security_group_id,
            IpPermissions=[
                {
                    'IpProtocol': 'tcp',
                    'FromPort': 80,  # Porta que você deseja abrir, por exemplo, 80 para HTTP
                    'ToPort': 80,  # Porta que você deseja abrir, por exemplo, 80 para HTTP
                    'IpRanges': [
                        {
                            'CidrIp': ip,
                            'Description': description
                        }
                    ]
                }
            ]
        )
        print(f"IP {ip} adicionado ao Security Group {security_group_id} com a descrição: {description}")
    except Exception as e:
        print(f"Erro ao adicionar IP ao Security Group: {e}")

# Busca o ID do Security Group pela tag
security_group_id = get_security_group_id_by_tag(tag_key, tag_value, region)

if security_group_id:
    # Chama a função para adicionar o IP ao security group
    add_ip_to_security_group(security_group_id, ip_address, description, region)
else:
    print("Não foi possível encontrar um Security Group com a tag especificada.")
