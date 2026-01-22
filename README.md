# VisionCount Foundry 🏭
Sistema de contagem automática de peças utilizando Visão Computacional e Inteligência Artificial (YOLOv8).

## 🚀 Como Rodar em Outro PC

### 1. Pré-requisitos
- Instalar o **Python** (versão 3.10 ou superior).
  - Na instalação, marque a opção: *"Add Python to PATH"*.
- Ter uma webcam conectada.

### 2. Instalação
Abra o terminal (PowerShell ou CMD) na pasta do projeto e instale as dependências:
```bash
pip install -r requirements.txt
```

### 3. Como Usar

#### A) Rodar a Contagem (Produção)
Para iniciar o sistema com o cérebro treinado (`best.pt`):
```bash
python main.py --model best.pt
```
**Comandos no Teclado:**
- **`q`**: Sair do programa.
- **`r`**: Resetar a contagem para zero.

---

### 🔧 Manutenção (Treinamento de Novas Peças)

Se precisar ensinar o sistema a reconhecer peças novas:

1. **Capturar Fotos:**
   Rode o script de coleta e tire fotos apertando ESPAÇO:
   ```bash
   python capture_data.py
   ```

2. **Rotular (Labeling):**
   Envie as fotos para o [Roboflow](https://roboflow.com), marque as peças e baixe o dataset no formato **YOLOv8 (ZIP)**.
   Extraia o zip na pasta do projeto (deve criar a pasta `train`, `valid`, `data.yaml`, etc).
   *Dica: Atualize os caminhos no `data.yaml` para o caminho completo do novo PC.*

3. **Treinar:**
   O computador vai estudar as fotos e criar um novo arquivo `best.pt`:
   ```bash
   python train_custom.py
   ```
   *O novo arquivo ficará em `runs/detect/train/weights/best.pt`. Copie ele para a pasta principal.*

---

## 🛠️ Solução de Problemas
- **Erro de Câmera:** Se não abrir, tente trocar o índice no comando: `python main.py --source 1`.
- **Contagem Dupla:** Ajuste a iluminação para evitar sombras ou aumente a confiança no código (conf=0.7).