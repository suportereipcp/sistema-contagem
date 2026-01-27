import cv2
import argparse
from ultralytics import YOLO

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=str, default="0", help="Caminho do vídeo ou índice da câmera")
    parser.add_argument("--model", type=str, default="yolov8n.pt", help="Caminho para o arquivo do modelo (.pt)")
    parser.add_argument("--conf", type=float, default=0.8, help="Limiar de confiança (0.0 a 1.0). Padrão 0.8")
    args = parser.parse_args()

    # 1. Inicialização
    # Carrega o modelo (padrão ou customizado)
    print(f"Carregando modelo: {args.model} com confiança mínima de {args.conf*100}% ...")
    model = YOLO(args.model)

    source = args.source
    
    # Se for dígito, converte para inteiro (índice da câmera)
    if source.isdigit():
        source = int(source)
        # Preferência por DirectShow no Windows para evitar erros de MSMF
        print(f"Tentando abrir câmera índice {source} com DirectShow (DSHOW)...")
        cap = cv2.VideoCapture(source, cv2.CAP_DSHOW)
        
        if not cap.isOpened():
             print(f"Falha no DSHOW. Tentando backend padrão...")
             cap = cv2.VideoCapture(source)
    else:
        print(f"Abrindo arquivo de vídeo: {source}")
        cap = cv2.VideoCapture(source)

    if not cap.isOpened():
        print(f"Erro Crítico: Não foi possível abrir a fonte: {source}")
        print("DICA: Se for webcam, verifique: Configurações -> Privacidade -> Câmera -> 'Permitir que apps acessem sua câmera'.")
        return

    # 2. Configurações de Contagem
    # Definindo a linha de contagem. Vamos posicioná-la no centro da altura da tela.
    # Como não sabemos a resolução exata até ler o frame, vamos definir dinamicamente no loop inicial
    line_y_pos = None 
    offset = 30  # Tolerância em pixels para considerar que "cruzou" a linha
    
    # Armazena IDs que já foram contados para evitar contagem dupla
    counted_ids = set()
    counter = 0

    print("Sistema iniciado. Pressione 'q' para sair.")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Erro ao ler frame da câmera (ou fim do vídeo).")
            break

        # Define a linha na primeira iteração
        if line_y_pos is None:
            height, width, _ = frame.shape
            line_y_pos = int(height // 2) # Linha no meio da tela
            
        # 3. Detecção e Rastreamento
        # persist=True é essencial para tracking manter o ID entre frames
        # conf=args.conf: Só conta se tiver X% de certeza (ex: 0.8)
        results = model.track(source=frame, persist=True, conf=args.conf, verbose=False)
        
        # Desenha a linha de referência
        cv2.line(frame, (0, line_y_pos), (width, line_y_pos), (0, 255, 0), 2)

        # Processa os resultados
        if results and results[0].boxes.id is not None:
            boxes = results[0].boxes.xyxy.cpu().numpy().astype(int)
            track_ids = results[0].boxes.id.cpu().numpy().astype(int)
            class_ids = results[0].boxes.cls.cpu().numpy().astype(int)
            confs = results[0].boxes.conf.cpu().numpy() # Pega as confianças

            for box, track_id, cls_id, conf in zip(boxes, track_ids, class_ids, confs):
                x1, y1, x2, y2 = box
                
                # Calcula o centro do bounding box
                cx = int((x1 + x2) / 2)
                cy = int((y1 + y2) / 2)

                # Desenha o bounding box e o centro
                cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)
                cv2.circle(frame, (cx, cy), 4, (0, 0, 255), -1)
                
                # Texto com ID e Confiança
                label = f"ID: {track_id} ({int(conf*100)}%)"
                cv2.putText(frame, label, (x1, y1 - 10), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

                # 4. Lógica de Contagem
                # Verifica se o centro do objeto cruzou a linha
                # A lógica simples aqui verifica se o centro está dentro de uma faixa da linha
                # E se o ID ainda não foi contado.
                
                # Para robustez real, deveríamos checar a direção (ex: cy anterior < line < cy atual)
                # Mas para esta base inicial, vamos usar a proximidade com a linha
                if (line_y_pos - offset) < cy < (line_y_pos + offset):
                    if track_id not in counted_ids:
                        counted_ids.add(track_id)
                        counter += 1
                        # Efeito visual de contagem (linha muda de cor momentaneamente)
                        cv2.line(frame, (0, line_y_pos), (width, line_y_pos), (0, 0, 255), 4)
                        print(f"Peça contada! Total: {counter}")

        # 5. Interface na Tela (HUD)
        cv2.putText(frame, f"Contagem: {counter}", (20, 50), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 255), 3)

        cv2.imshow("VisionCount Foundry - Monitoramento", frame)

        # Tecla 'q' para sair
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        # Tecla 'r' para resetar contagem
        elif key == ord('r'):
            counter = 0
            counted_ids.clear()
            print("Contagem resetada!")

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
