# Guia de Treinamento - VisionCount Foundry

Este documento contém os passos para treinar o novo modelo de **Segmentação** na máquina com GPU.

## 1. Ativação do Ambiente

Certifique-se de que as dependências estão instaladas:

```bash
pip install ultralytics opencv-python
```

## 2. Preparação dos Dados (Já realizado)

Os arquivos JSON do LabelMe já foram convertidos para o formato YOLO TXT via `json2yolo.py`.
O arquivo `dataset/data.yaml` foi configurado com as classes:
0: `peca a`
1: `peca b`

## 3. Iniciar Treinamento

Para iniciar o treinamento de segmentação, execute:

```bash
python train_custom.py
```

*Nota: O script `train_custom.py` já está configurado para carregar o `yolov8n-seg.pt` e salvar os resultados em `runs/detect/train`. Sua GPU será detectada automaticamente pelo PyTorch.*

## 4. Finalização

Após o término:

1. Localize o arquivo `runs/detect/train/weights/best.pt`.
2. Renomeie-o ou mova-o para a raiz do projeto como `best_seg.pt`.
3. Faça o commit/push deste arquivo para que possamos testá-lo aqui.
