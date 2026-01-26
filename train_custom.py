from ultralytics import YOLO

def train():
    # Carrega o modelo base (Nano)
    model = YOLO("yolov8n.pt") 

    # Inicia o treinamento
    # data: Caminho para o arquivo data.yaml configurado
    # epochs: 50 épocas é um bom começo para testes rápidos (pode aumentar para 100 depois)
    # imgsz: Tamanho 640 é padrão para YOLOv8
    print("Iniciando treinamento... Isso pode demorar alguns minutos dependendo do seu PC.")
    results = model.train(
        data="c:/Projetos/sistema-contagem/dataset/data.yaml",
        epochs=50,
        imgsz=640,
        plots=True
    )
    print("Treinamento finalizado!")
    print(f"O modelo final foi salvo em: {results.save_dir}")

if __name__ == '__main__':
    train()
