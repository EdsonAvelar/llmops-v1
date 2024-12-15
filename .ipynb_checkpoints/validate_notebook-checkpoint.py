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
    
    # Validar o formato da saída (campo output)
    if "output" not in snapshot:
        raise ValueError("Snapshot inválido: campo 'output' ausente.")
    
    # Validar contraintens obrigatórias
    output_constraints = contract["output_schema"]["constraints"]
    for constraint in output_constraints:
        if "must_contain" in constraint:
            for word in constraint["must_contain"]:
                if word not in snapshot["output"]:
                    raise ValueError(f"Saída inválida: não contém a palavra obrigatória '{word}'.")

    # Validar limite de comprimento da saída
    max_length = contract["output_schema"]["constraints"][1]["max_length"]
    if len(snapshot["output"]) > max_length:
        raise ValueError(f"Saída muito longa: {len(snapshot['output'])} caracteres > {max_length} caracteres.")

    # Validar métricas (exemplo: similaridade)
    if "metrics" in snapshot and "similarity" in snapshot["metrics"]:
        similarity = snapshot["metrics"]["similarity"]
        similarity_threshold = contract["metrics"][0]["threshold"]
        if similarity < similarity_threshold:
            raise ValueError(f"Similaridade insuficiente: {similarity} < {similarity_threshold}.")
    
    print("Snapshot validado com sucesso!")


if __name__ == "__main__":
    # Caminhos padrão para o snapshot e contrato
    SNAPSHOT_FILE = "snapshots/snapshot.json"
    CONTRACT_FILE = "contract.yaml"

    try:
        validate_snapshot(SNAPSHOT_FILE, CONTRACT_FILE)
    except ValueError as e:
        print(f"Erro na validação: {e}")
        exit(1)
