import json
import os
import glob
from collections import defaultdict

def convert_labelme_json_to_yolo(json_dir, output_dir, class_map=None):
    """
    Converts Labelme JSON files to YOLO segmentation format (.txt).
    format: <class-index> <x1> <y1> <x2> <y2> ... <xn> <yn> (normalized)
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    json_files = glob.glob(os.path.join(json_dir, "*.json"))
    print(f"Encontrados {len(json_files)} arquivos JSON em {json_dir}")

    # If no class map provided, auto-generate or use standard
    # For now, let's assume we read classes.txt or generate on fly
    if class_map is None:
        # Try to find classes.txt
        classes_path = os.path.join(json_dir, "classes.txt")
        if os.path.exists(classes_path):
             with open(classes_path, "r") as f:
                classes = [line.strip() for line in f.readlines() if line.strip()]
                class_map = {name: i for i, name in enumerate(classes)}
        else:
            # Fallback A: Default "peca" if user only wants that
            # Fallback B: Scan all JSONs to find unique labels (risky for consistency across runs)
            # Let's assume 'peca' is 0 for safety if nothing else
            class_map = {"peca": 0} 
    
    print(f"Mapa de Classes: {class_map}")

    for json_file in json_files:
        try:
            with open(json_file, "r") as f:
                data = json.load(f)
            
            image_width = data["imageWidth"]
            image_height = data["imageHeight"]
            
            # Output file name: replace .json with .txt
            base_name = os.path.splitext(os.path.basename(json_file))[0]
            txt_path = os.path.join(output_dir, f"{base_name}.txt")
            
            with open(txt_path, "w") as out_f:
                for shape in data["shapes"]:
                    label = shape["label"].lower() # Força minusculo para evitar erros de Case
                    
                    # Normaliza o mapa de classes também se necessário, mas aqui vamos assumir que o map usa chaves minusculas
                    if label not in class_map:
                        # Tenta verificar se existe alguma chave compatível ignorando case
                        found_key = None
                        for key in class_map:
                            if key.lower() == label:
                                found_key = key
                                break
                        
                        if found_key:
                            label = found_key
                        else:
                            print(f"Aviso: Label '{label}' (orig: {shape['label']}) nao encontrado no mapa de classes {class_map}. Ignorando.")
                            continue
                    
                    class_id = class_map[label]
                    points = shape["points"]
                    
                    # Normalize points
                    normalized_points = []
                    for x, y in points:
                        nx = x / image_width
                        ny = y / image_height
                        # Clamp to 0-1 just in case
                        nx = max(0, min(1, nx))
                        ny = max(0, min(1, ny))
                        normalized_points.extend([f"{nx:.6f}", f"{ny:.6f}"])
                    
                    line = f"{class_id} " + " ".join(normalized_points) + "\n"
                    out_f.write(line)
                    
        except Exception as e:
            print(f"Erro convertendo {json_file}: {e}")

if __name__ == "__main__":
    # Test run
    convert_labelme_json_to_yolo("dataset", "dataset")
