import cv2
import os
import time

def main():
    # Cria a pasta 'dataset' se não existir
    output_dir = "dataset"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Abre a câmera (usa o índice 0 que sabemos que funciona)
    # Se precisar de outro, mude aqui ou use argparse como no main.py
    # Preferência por DSHOW
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    
    if not cap.isOpened():
        cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Erro: Não foi possível abrir a câmera.")
        return

    print("=== Coleta de Dados para Treinamento ===")
    print("Controles:")
    print(" [ESPAÇO] - Salvar Foto")
    print(" [q]      - Sair")
    
    count = 0
    # Verifica quantas fotos já existem para não sobrescrever
    existing_files = os.listdir(output_dir)
    count = len(existing_files)

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Erro ao ler frame.")
            break

        # Mostra o frame
        cv2.imshow("Coletor de Dados (Aperte ESPACO)", frame)

        key = cv2.waitKey(1) & 0xFF

        # Salvar imagem
        if key == ord(' '):
            filename = f"{output_dir}/eca_{count:04d}.jpg"
            cv2.imwrite(filename, frame)
            print(f"Foto salva: {filename}")
            count += 1
            
            # Pisca a tela para dar feedback visual
            cv2.imshow("Coletor de Dados (Aperte ESPACO)", 255 - frame)
            cv2.waitKey(50)

        # Sair
        elif key == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    print(f"\nColeta finalizada! Total de {count} imagens em '{output_dir}'.")

if __name__ == "__main__":
    main()
