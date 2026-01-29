# Sistema de Contagem e Rastreamento Inteligente 👁️🏭

![Status](https://img.shields.io/badge/Status-Stable-success)
![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688)
![YOLOv8](https://img.shields.io/badge/AI-Ultralytics%20YOLOv8-brand)
![Labelme](https://img.shields.io/badge/Labeling-Labelme-red)

Sistema industrial avançado para contagem, rastreamento e segmentação de peças em esteiras, desenvolvido com tecnologias de ponta em Visão Computacional.

---

## 📋 Visão Geral

Este projeto é uma solução completa (End-to-End) que integra captura de dados, rotulagem assistida, treinamento automático e inferência em tempo real. Projetado para rodar em ambientes locais (On-Premise), oferece uma interface web intuitiva para controle total do ciclo de vida da Inteligência Artificial.

### ✨ Principais Funcionalidades

- **🔍 Monitoramento em Tempo Real:** Detecção e contagem de peças com alta precisão utilizando Segmentação de Instância (YOLOv8-seg).
- **�️ Interface de Controle Web:** Dashboard moderno para iniciar/parar o sistema, ajustar confiança e gerenciar processos.
- **🏷️ Rotulagem Profissional:** Integração nativa com **Labelme** para anotação precisa de polígonos.
- **🤖 Ciclo de Treinamento Automatizado:** Pipeline inteligente que converte anotações JSON automaticamente para o formato YOLO e inicia o retreino do modelo com um único clique.

---

## 🛠️ Stack Tecnológico

| Componente   | Tecnologia                                                       | Descrição                                               |
| :----------- | :--------------------------------------------------------------- | :------------------------------------------------------ |
| **Backend**  | [FastAPI](https://fastapi.tiangolo.com/)                         | API de alta performance para orquestração de processos. |
| **Servidor** | [Uvicorn](https://www.uvicorn.org/)                              | Servidor ASGI leve e rápido.                            |
| **IA Core**  | [Ultralytics YOLOv8](https://github.com/ultralytics/ultralytics) | Estado da arte em modelos de segmentação.               |
| **Visão**    | [OpenCV](https://opencv.org/)                                    | Processamento de imagem e renderização em tempo real.   |
| **Frontend** | HTML5 / CSS3 / JS                                                | Interface do usuário responsiva e dinâmica.             |
| **Data**     | Labelme / NumPy                                                  | Ferramentas de anotação e manipulação numérica.         |

---

## 🚀 Instalação e Configuração

### Pré-requisitos

- Python 3.10 ou superior.
- Webcam ou fonte de vídeo.
- NVIDIA GPU (Opcional, mas recomendado para treinamento rápido).

### Passos para Instalação

1. **Clonar o Repositório:**

   ```powershell
   git clone https://github.com/suportereipcp/sistema-contagem.git
   cd sistema-contagem
   ```

2. **Configurar Variáveis de Ambiente (Opcional):**
   Crie um arquivo `.env` se necessário. Por padrão, o sistema usa configurações locais.

3. **Ambiente Virtual e Dependências:**

   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   pip install -r requirements.txt
   ```

---

## 🕹️ Guia de Uso

Para iniciar o **Painel de Controle**, execute o seguinte comando no terminal:

````powershell
    .\venv\Scripts\python.exe -m uvicorn app:app --port 8000 --reload
    ```

Acesse: [http://localhost:8000](http://localhost:8000)

### Fluxo de Trabalho (Workflow)

#### 1. 📸 Monitoramento (Produção)

* No painel "Monitoramento", defina a **Câmera ID** (0 para webcam padrão) e o nível de **Confiança**.
* Clique em **INICIAR SISTEMA**.
* Uma janela abrirá mostrando a detecção em tempo real e a contagem.
* Use o botão **PARAR SISTEMA** no dashboard para encerrar.

#### 2. 🧠 Treinamento de Novos Modelos (Manutenção)

O sistema possui um fluxo simplificado para adicionar novas peças à IA:

1. **Captura:** Use o botão "ABRIR COLETOR" para capturar novas imagens da esteira (tecla `Espaço` para salvar).
2. **Rotulagem (Manual Labeling):**
    * Clique em **"1. MANUAL LABELING (Labelme)"**.
    * O software Labelme abrirá. Marque as peças usando a ferramenta de Polígono (`Create Polygons`).
    * Salve as anotações (arquivos `.json`) na pasta `dataset` (padrão).
3. **Treinamento:**
    * Clique em **"2. TREINAR NOVO MODELO"**.
    * **Automação:** O sistema irá automaticamente converter seus JSONs para `.txt`, atualizar o arquivo de configuração e iniciar o treinamento.
    * Ao finalizar, o novo modelo será salvo.

---

## 📂 Estrutura do Projeto

````

sistema-contagem/
├── app.py # Backend da API FastAPI
├── main.py # Core de detecção e inferência (YOLO)
├── capture_data.py # Script de coleta de imagens
├── auto_label.py # Script legado de auto-rotulagem
├── train_wrapper.py # Orquestrador de treinamento e conversão de dados
├── json2yolo.py # Utilitário de conversão Labelme JSON -> YOLO
├── dataset/ # Diretório de armazenamento de imagens e labels
│ ├── data.yaml # Configuração gerada automaticamente
│ └── _.json/_.jpg # Dados brutos
├── static/ # Assets do Frontend (HTML/CSS/JS)
└── requirements.txt # Dependências do projeto

```

---

## 🤝 Contribuição

Contribuições são bem-vindas! Siga as boas práticas de Pull Requests e Conventional Commits.

1. Faça um Fork do projeto.
2. Crie uma Branch para sua Feature (`git checkout -b feature/NovaFeature`).
3. Commit suas mudanças (`git commit -m 'Feat: Adiciona Nova Feature'`).
4. Push para a Branch (`git push origin feature/NovaFeature`).
5. Abra um Pull Request.
```
