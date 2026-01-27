import json
import os
import glob
import numpy as np

def json_to_yolo_segmentation(json_dir, output_dir, class_map):
    """
    Converte arquivos JSON do LabelMe para TXT do YOLOv8 Segmentation.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    json_files = glob.glob(os.path.join(json_dir, "*.json"))
    
    print(f"Encontrados {len(json_files)} arquivos JSON em {json_dir}")

    for json_file in json_files:
        with open(json_file, 'r') as f:
            data = json.load(f)

        image_height = data['imageHeight']
        image_width = data['imageWidth']
        filename = os.path.splitext(os.path.basename(json_file))[0]
        txt_filename = os.path.join(output_dir, filename + ".txt")

        with open(txt_filename, 'w') as out_f:
            for shape in data['shapes']:
                label = shape['label']
                if label not in class_map:
                    print(f"Aviso: Classe '{label}' ignorada (não está no mapa).")
                    continue
                
                class_id = class_map[label]
                points = shape['points']

                # Normaliza os pontos (0.0 a 1.0)
                normalized_points = []
                for point in points:
                    x = point[0] / image_width
                    y = point[1] / image_height
                    normalized_points.append(f"{x:.6f} {y:.6f}")

                # Escreve linha: <class_id> <x1> <y1> <x2> <y2> ...
                line = f"{class_id} " + " ".join(normalized_points) + "\n"
                out_f.write(line)
        
        print(f"Convertido: {json_file} -> {txt_filename}")

if __name__ == "__main__":
    # Configuração
    INPUT_DIR = "dataset"   # Onde estão os JSONs e Imagens
    OUTPUT_DIR = "dataset"  # Onde salvar os TXTs (YOLO espera na mesma pasta ou labels/)
    
    # Mapa de classes: Nome no LabelMe -> ID numérico do YOLO
    CLASS_MAP = {
        "peca a": 0,
        "peca b": 1
    }

    print("Iniciando conversão LabelMe -> YOLO Segmentation...")
    json_to_yolo_segmentation(INPUT_DIR, OUTPUT_DIR, CLASS_MAP)
    print("Conversão concluída!")
