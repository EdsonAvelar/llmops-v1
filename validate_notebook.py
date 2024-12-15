import json
import yaml

def validate_snapshot(snapshot_file, contract_file):
    """
    Valida o snapshot gerado pelo notebook com base nas especificações do contrato.

    Args:
        snapshot_file (str): Caminho para o arquivo JSON contendo o snapshot.
        contract_file (str): Caminho para o arquivo YAML contendo o contrato.

    Raises:
        ValueError: Se o snapshot não atender às especificações do contrato.
    """
    # Carregar o snapshot gerado pelo notebook
    with open(snapshot_file, 'r') as snap_file:
        snapshot = json.load(snap_file)
    
    # Carregar o contrato de validação
    with open(contract_file, 'r') as contract_file:
        contract = yaml.safe_load(contract_file)
    
    # Validar o campo "response" no snapshot
    if "response" not in snapshot:
        raise ValueError("Snapshot inválido: campo 'response' ausente.")
    
    # Validar palavras obrigatórias no contrato
    output_constraints = contract["output_schema"]["constraints"]
    for constraint in output_constraints:
        if "must_contain" in constraint:
            for word in constraint["must_contain"]:
                if word not in snapshot["response"]:
                    raise ValueError(f"Saída inválida: não contém a palavra obrigatória '{word}'.")

    # Validar limite de comprimento da saída
    max_length = contract["output_schema"]["constraints"][1]["max_length"]
    if len(snapshot["response"]) > max_length:
        raise ValueError(f"Saída muito longa: {len(snapshot['response'])} caracteres > {max_length} caracteres.")

    # Validar contexto no contrato
    if "context" in contract["input_schema"]:
        if contract["input_schema"]["context"] not in snapshot["response"]:
            raise ValueError("Saída inválida: resposta não inclui o contexto fornecido.")
    
    print("Snapshot validado com sucesso!")


if __name__ == "__main__":
    # Caminhos padrão para o snapshot e contrato
    OUTPUT_FILE = "stgen_output.json"  # Arquivo gerado pelo stgen
    CONTRACT_FILE = "contract.yaml"


    try:
        validate_snapshot(SNAPSHOT_FILE, CONTRACT_FILE)
    except ValueError as e:
        print(f"Erro na validação: {e}")
        exit(1)
