from ultralytics import YOLO

def train():
    # Carrega o modelo de SEGMENTAÇÃO (Nano Seg)
    model = YOLO("yolov8n-seg.pt") 

    # Inicia o treinamento
    # data: Caminho para o arquivo data.yaml configurado
    # epochs: 50 épocas é um bom começo
    # imgsz: Tamanho 640 é padrão para YOLOv8
    print("Iniciando treinamento de SEGMENTAÇÃO...")
    results = model.train(
        data="dataset/data.yaml",
        epochs=50,
        imgsz=640,
        plots=True
    )
    print("Treinamento finalizado!")
    print(f"O modelo final foi salvo em: {results.save_dir}")
    
    # --- AUTO EXPORT & DEPLOY ---
    import shutil
    import os
    
    best_pt_path = os.path.join(results.save_dir, "weights", "best.pt")
    target_pt = "best_seg.pt"
    target_onnx = "best_seg.onnx"
    
    if os.path.exists(best_pt_path):
        print(f"Atualizando modelo em produção: {target_pt}")
        shutil.copy(best_pt_path, target_pt)
        
        # Expert to ONNX for CPU compatibility
        print("Exportando versão Universal (ONNX)...")
        try:
            model = YOLO(target_pt)
            model.export(format="onnx", dynamic=True) # Dynamic shape for flexibility
            print(f"Modelo ONNX gerado: {target_onnx}")
        except Exception as e:
            print(f"Erro ao exportar ONNX: {e}")
    else:
        print("AVISO: Arquivo best.pt não encontrado para deploy.")

if __name__ == '__main__':
    train()
