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

if __name__ == '__main__':
    train()
