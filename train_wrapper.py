import os
import sys
import subprocess
from json2yolo import convert_labelme_json_to_yolo

def main():
    print("=== Iniciando Preparacao para Treinamento ===")
    
    # 1. Convert JSON to YOLO
    dataset_dir = os.path.join(os.getcwd(), "dataset")
    print(f"Convertendo arquivos Labelme JSON em {dataset_dir} para formato YOLO...")
    try:
        convert_labelme_json_to_yolo(dataset_dir, dataset_dir)
        print("Conversao concluida com sucesso.")
        
        # 1.5 Generate data.yaml
        yaml_path = os.path.join(dataset_dir, "data.yaml")
        print(f"Gerando {yaml_path}...")
        
        # Absolute path to dataset to avoid confusion
        abs_dataset_dir = os.path.abspath(dataset_dir)
        
        # Simple YAML content for flat directory structure (images and labels in same folder)
        # Note: 'train' and 'val' point to the same folder for this simple usage
        yaml_content = f"""
path: {abs_dataset_dir}
train: .
val: .
names:
  0: peca
"""
        with open(yaml_path, "w") as f:
            f.write(yaml_content.strip())
            
    except Exception as e:
        print(f"ERRO CRITICO na preparacao: {e}")
        input("Pressione Enter para sair...")
        sys.exit(1)

    # 2. Launch Training
    print("=== Iniciando Treinamento YOLOv8 ===")
    try:
        # Pass user arguments if needed, or just default
        # reusing train_custom.py logic
        subprocess.check_call([sys.executable, "train_custom.py"])
    except subprocess.CalledProcessError as e:
        print(f"Erro durante o treinamento: {e}")
        input("Pressione Enter para sair...")
    except Exception as e:
        print(f"Erro inesperado: {e}")
        input("Pressione Enter para sair...")

if __name__ == "__main__":
    main()
