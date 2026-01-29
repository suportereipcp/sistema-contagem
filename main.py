import os
import numpy as np
import time
import argparse
import cv2
from ultralytics import YOLO

# Correção para erro OMP
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

def draw_modern_text(img, text, pos, font_scale=0.6, color=(255,255,255), thickness=1, bg_color=(0,0,0)):
    """ Desenha texto com background semi-transparente """
    font = cv2.FONT_HERSHEY_DUPLEX
    (t_w, t_h), _ = cv2.getTextSize(text, font, font_scale, thickness)
    x, y = pos
    sub_img = img[y-t_h-5:y+5, x-5:x+t_w+5]
    if sub_img.size > 0:
        rect = np.full(sub_img.shape, bg_color, dtype=np.uint8)
        cv2.addWeighted(sub_img, 0.4, rect, 0.6, 1.0, sub_img)
    cv2.putText(img, text, pos, font, font_scale, color, thickness, cv2.LINE_AA)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=str, default="0", help="Caminho do vídeo ou índice da câmera")
    parser.add_argument("--model", type=str, default="best_seg.pt", help="Modelo .pt")
    parser.add_argument("--conf", type=float, default=0.65, help="Confiança mínima")
    args = parser.parse_args()

    print(f"Carregando modelo solicitado: {args.model}") 
    
    # --- AUTO-DEVICE & MODEL SELECTION ---
    import torch
    
    def get_best_hardware_config(model_base_name):
        """
        Detecta hardware e seleciona o melhor formato de modelo.
        Retorna: (model_path, device, adaptive_resize_bool)
        """
        # 1. Prioridade: GPU NVIDIA
        if torch.cuda.is_available():
            device_name = torch.cuda.get_device_name(0)
            print(f"✅ GPU NVIDIA Detectada: {device_name} (Forçando CUDA:0)")
            
            # Tenta carregar TensorRT (.engine)
            engine_path = model_base_name.replace(".pt", ".engine")
            if os.path.exists(engine_path):
                print(f"⚡ Usando Motor TensorRT para velocidade máxima: {engine_path}")
                return engine_path, "cuda:0", False
            
            # Se não tiver engine, usa .pt na GPU
            print(f"⚠️ Arquivo TensorRT (.engine) não encontrado. Usando PyTorch (.pt) na GPU.")
            return model_base_name, "cuda:0", False
            
        else:
            # 2. Fallback: CPU
            print("⚠️ GPU não detectada. Ativando modo de compatibilidade CPU.")
            
            # Tenta carregar ONNX (Universal)
            onnx_path = model_base_name.replace(".pt", ".onnx")
            if os.path.exists(onnx_path):
                print(f"🛡️ Usando ONNX Runtime para otimização em CPU: {onnx_path}")
                return onnx_path, "cpu", True
            
            print(f"⚠️ ONNX não encontrado. Usando PyTorch (.pt) em CPU (Pode ser lento).")
            return model_base_name, "cpu", True

    best_model_path, device, adaptive_mode = get_best_hardware_config(args.model)
    
    # Carrega o modelo com o device correto
    try:
        model = YOLO(best_model_path) # YOLO carrega .pt, .onnx, .engine automaticamente
    except Exception as e:
        print(f"Erro ao carregar {best_model_path}: {e}")
        print("Tentando fallback para original...")
        model = YOLO(args.model)
        device = "cpu"
        adaptive_mode = True

    model.to(device) if device != "cpu" and not best_model_path.endswith(".onnx") else None # ONNX runs on its own runtime usually
    print(f"🚀 Sistema rodando em: {device.upper()} | Resize Adaptativo: {'ATIVO' if adaptive_mode else 'OFF'}")

    source = args.source
    if source.isdigit():
        source = int(source)
        print(f"Abrindo câmera {source} (DSHOW)...")
        cap = cv2.VideoCapture(source, cv2.CAP_DSHOW)
        if not cap.isOpened():
             print("DSHOW falhou, tentando padrão...")
             cap = cv2.VideoCapture(source)
    else:
        print(f"Abrindo vídeo: {source}")
        cap = cv2.VideoCapture(source)

    if not cap.isOpened():
        print(f"Erro Crítico: Fonte inacessível: {source}")
        return

    # --- CONFIGURAÇÕES ---
    line_pos_A = None # Topo (65%)
    line_pos_B = None # Fundo (15%)
    offset = 25
    
    # Cores (BGR)
    COLOR_CONFIRMED = (50, 205, 50)     # Verde
    COLOR_TRACKING = (0, 140, 255)      # Laranja
    COLOR_LOCKED = (255, 215, 0)        # Dourado (Novo: Identificado e Travado)
    COLOR_HUD_BG = (30, 30, 30)
    COLOR_LINE_A = (0, 165, 255)
    COLOR_LINE_B = (0, 255, 127)

    # Estados
    object_states = {}
    counters = {}
    
    # BLOQUEIO DE CLASSE: { track_id: class_id }
    locked_classes = {}
    
    class_names = model.names
    start_time = time.time()

    print("Sistema iniciado. Pressione 'q' para sair.")
    print("Modo de Bloqueio de Classe: ATIVO (IA define a classe na entrada e não muda mais)")

    prev_frame_time = 0

    while True:
        ret, frame = cap.read()
        if not ret: break

        # Calculo de FPS
        curr_frame_time = time.time()
        fps = 1 / (curr_frame_time - prev_frame_time) if prev_frame_time > 0 else 0
        prev_frame_time = curr_frame_time

        height, width, _ = frame.shape
        
        if line_pos_A is None:
            line_pos_A = int(height * 0.65) # Entrada (Baixo/Meio)
            line_pos_B = int(height * 0.15) # Saída (Topo)
            
        yaml_path = "custom_tracker.yaml"
        if not os.path.exists(yaml_path): yaml_path = "botsort.yaml"

        if adaptive_mode:
            # Em CPU, reduzimos a resolução de inferência para manter o FPS
            # 320px é suficiente para contagem e muito mais rápido
            results = model.track(source=frame, persist=True, conf=args.conf, tracker=yaml_path, verbose=False, imgsz=320)
        else:
            # Em GPU, usamos 640 ou tamanho nativo (padrão)
            results = model.track(source=frame, persist=True, conf=args.conf, tracker=yaml_path, verbose=False)
        
        # --- HUD ---
        overlay_hud = frame.copy()
        cv2.rectangle(overlay_hud, (0, 0), (width, 100), COLOR_HUD_BG, -1)
        cv2.addWeighted(overlay_hud, 0.85, frame, 0.15, 0, frame)
        
        cv2.line(frame, (0, line_pos_A), (width, line_pos_A), COLOR_LINE_A, 2, cv2.LINE_AA)
        draw_modern_text(frame, " ZONA DE ENTRADA ", (10, line_pos_A - 10), 0.5, COLOR_LINE_A, 1, (0,0,0))
        
        cv2.line(frame, (0, line_pos_B), (width, line_pos_B), COLOR_LINE_B, 2, cv2.LINE_AA)
        draw_modern_text(frame, " LINHA DE CONTAGEM ", (10, line_pos_B - 10), 0.5, COLOR_LINE_B, 1, (0,0,0))

        # Cronômetro
        elapsed = int(time.time() - start_time)
        hours, rem = divmod(elapsed, 3600)
        minutes, seconds = divmod(rem, 60)
        cv2.putText(frame, f"{hours:02}:{minutes:02}:{seconds:02}", (width - 160, 55), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (200, 200, 200), 2, cv2.LINE_AA)
        cv2.putText(frame, "TEMPO ATIVO", (width - 160, 25), cv2.FONT_HERSHEY_PLAIN, 1.0, (150, 150, 150), 1, cv2.LINE_AA)

        # FPS (Bottom Right, Simple Font, Green)
        cv2.putText(frame, f"FPS: {int(fps)}", (width - 120, height - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)


        # Processamento
        if results and results[0].boxes.id is not None:
            boxes = results[0].boxes.xyxy.cpu().numpy().astype(int)
            track_ids = results[0].boxes.id.cpu().numpy().astype(int)
            class_ids = results[0].boxes.cls.cpu().numpy().astype(int)

            for idx, (box, track_id, cls_id) in enumerate(zip(boxes, track_ids, class_ids)):
                x1, y1, x2, y2 = box
                cx, cy = int((x1 + x2) / 2), int((y1 + y2) / 2)

                # --- Lógica de CLASSE FIXA ("Congelar IA") ---
                # A primeira vez que vemos um ID, fixamos sua classe.
                # Nos frames seguintes, usamos a classe fixa, ignorando a detecção atual.
                if track_id in locked_classes:
                    final_cls_id = locked_classes[track_id]
                    is_locked = True
                else:
                    locked_classes[track_id] = cls_id
                    final_cls_id = cls_id
                    is_locked = False

                class_name = class_names[final_cls_id]

                if track_id not in object_states:
                    object_states[track_id] = {'valid_entry': False, 'counted': False, 'frames': 0, 'start_y': cy}
                
                state = object_states[track_id]
                state['frames'] += 1
                
                # Regra MRU Invertida (Subindo)
                if state['start_y'] >= (line_pos_A - offset * 2): state['valid_entry'] = True
                if abs(cy - line_pos_A) < offset: state['valid_entry'] = True

                # Contagem
                if (line_pos_B - offset) < cy < (line_pos_B + offset):
                    if state['valid_entry'] and not state['counted']:
                        state['counted'] = True
                        counters[class_name] = counters.get(class_name, 0) + 1
                        print(f"[ID {track_id}] CONTADO: {class_name}")

                # --- Visualização ---
                if state['counted']:
                    color = COLOR_CONFIRMED
                    status_icon = "CHECK"
                elif is_locked:
                    color = COLOR_TRACKING
                    status_icon = "LOCK"
                else:
                    color = COLOR_LOCKED
                    status_icon = "NEW"

                # Bounding Box
                cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2, cv2.LINE_AA)
                
                # Label estilizada
                label = f" #{track_id} {class_name} [{status_icon}] "
                (w, h), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_DUPLEX, 0.5, 1)
                cv2.rectangle(frame, (x1, y1 - 25), (x1 + w, y1), color, -1)
                cv2.putText(frame, label, (x1, y1 - 8), cv2.FONT_HERSHEY_DUPLEX, 0.5, (0,0,0) if state['counted'] else (255,255,255), 1, cv2.LINE_AA)
                cv2.circle(frame, (cx, cy), 3, (0,255,255), -1, cv2.LINE_AA)

        # Placar
        x_offset = 20
        cv2.putText(frame, "PRODUCAO:", (x_offset, 25), cv2.FONT_HERSHEY_PLAIN, 1.2, (180, 180, 180), 1, cv2.LINE_AA)
        for class_name, count in counters.items():
            text = f"{class_name.upper()}  {count:03d}"
            (tw, th), _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_DUPLEX, 0.8, 1)
            cv2.rectangle(frame, (x_offset, 35), (x_offset + tw + 10, 35 + th + 15), (50, 50, 50), -1)
            cv2.putText(frame, text, (x_offset + 5, 35 + th + 5), cv2.FONT_HERSHEY_DUPLEX, 0.8, COLOR_CONFIRMED, 1, cv2.LINE_AA)
            x_offset += tw + 30

        display_scale = 1.5
        display_frame = cv2.resize(frame, None, fx=display_scale, fy=display_scale)
        cv2.imshow("VisionCount Pro V5", display_frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'): break
        elif key == ord('r'):
            counters.clear(); object_states.clear(); locked_classes.clear(); start_time = time.time()
            print(">> RESETADO TUDO")

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
