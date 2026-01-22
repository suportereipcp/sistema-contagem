import cv2

def test_camera(index, backend_name, backend_id):
    print(f"Testando índice {index} com backend {backend_name}...", end=" ")
    if backend_id is not None:
        cap = cv2.VideoCapture(index, backend_id)
    else:
        cap = cv2.VideoCapture(index)
    
    if cap is not None and cap.isOpened():
        print("SUCESSO! ✅")
        ret, frame = cap.read()
        if ret:
            print(f"   Frame capturado: {frame.shape[1]}x{frame.shape[0]}")
        else:
            print("   Aviso: Câmera abriu mas não conseguiu ler frame.")
        cap.release()
        return True
    else:
        print("Falha. ❌")
        return False

print("=== Diagnóstico de Câmeras ===")
print("Verificando câmeras disponíveis (índices 0 a 3)...")

found_any = False
for i in range(4):
    print(f"\n--- Índice {i} ---")
    # Tenta backend padrão (ANY)
    if test_camera(i, "PADRÃO", None):
        found_any = True
        continue
    
    # Tenta DSHOW (bom para Windows)
    if test_camera(i, "DSHOW", cv2.CAP_DSHOW):
        found_any = True
        continue
        
    # Tenta MSMF (Media Foundation)
    if test_camera(i, "MSMF", cv2.CAP_MSMF):
        found_any = True
        continue

if not found_any:
    print("\nNenhuma câmera encontrada! 😱")
    print("Verifique:")
    print("1. O cabo USB está conectado?")
    print("2. Configurações de Privacidade do Windows -> Câmera (Permitir acesso)")
    print("3. Algum outro programa (Zoom, Teams) está usando a câmera?")
else:
    print("\nCâmeras encontradas! Use o índice que funcionou no comando principal.")
