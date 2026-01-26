import cv2
import os
import glob
import numpy as np

def auto_label():
    img_dir = "dataset"
    images = glob.glob(os.path.join(img_dir, "*.jpg"))
    
    print(f"Encontradas {len(images)} imagens.")
    
    for img_path in images:
        img = cv2.imread(img_path)
        h, w = img.shape[:2]
        
        # Converte para cinza e aplica blur/threshold
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (7, 7), 0)
        
        # Tenta detectar bordas/objetos
        # Método Otsu é bom para separar fundo de objeto se houver contraste
        _, thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
        
        # Encontra contornos
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        if not contours:
            print(f"Aviso: Nenhum objeto detectado em {img_path}")
            continue
            
        # Pega o maior contorno (assumindo que é a peça)
        c = max(contours, key=cv2.contourArea)
        
        # Pega o bounding box
        x, y, bw, bh = cv2.boundingRect(c)
        
        # Filtro simples: se for muito pequeno (ruído) ou muito grande (toda a tela), ignora
        if cv2.contourArea(c) < 1000 or (bw * bh) > (w * h * 0.95):
            # Se falhar, usa um box central como fallback
            cx, cy = w / 2, h / 2
            bw, bh = w * 0.4, h * 0.4
            x, y = cx - bw/2, cy - bh/2
        
        # Converte para formato YOLO (normalizado 0-1 e centro x,y)
        # class x_center y_center width height
        cx = (x + bw / 2) / w
        cy = (y + bh / 2) / h
        nw = bw / w
        nh = bh / h
        
        # Salva o arquivo .txt com o mesmo nome da imagem
        txt_path = img_path.replace(".jpg", ".txt")
        with open(txt_path, "w") as f:
            f.write(f"0 {cx:.6f} {cy:.6f} {nw:.6f} {nh:.6f}\n")
            
        print(f"Gerado label para {os.path.basename(img_path)}")

if __name__ == "__main__":
    auto_label()
