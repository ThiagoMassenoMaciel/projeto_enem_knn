# 📊 Previsor de Notas ENEM com KNN 🚀

![print interface usuário](https://github.com/user-attachments/assets/5cffe81b-692a-4ef2-9791-40532d449944)

## 📝 Resumo

Este projeto é uma aplicação web Full Stack desenvolvida para prever as notas de um aluno no Exame Nacional do Ensino Médio (ENEM) com base em suas informações socioeconômicas e de localidade. Utiliza um modelo de Machine Learning K-Nearest Neighbors (KNN) do tipo Regressor, treinado com os microdados oficiais do ENEM 2023.

A aplicação permite que um usuário insira os dados de um novo aluno através de um formulário web simples e, ao submeter, recebe como resposta a previsão das notas nas cinco áreas de conhecimento do exame:

* Matemática e suas Tecnologias (NU_NOTA_MT)
* Ciências da Natureza e suas Tecnologias (NU_NOTA_CN)
* Linguagens, Códigos e suas Tecnologias (NU_NOTA_LC)
* Ciências Humanas e suas Tecnologias (NU_NOTA_CH)
* Nota da Redação (NU_NOTA_REDACAO)

O objetivo é fornecer uma ferramenta útil para instituições de ensino ou estudantes estimarem um desempenho potencial no exame. 🎓

## ✨ Tecnologias Utilizadas

### Frontend 🌐🎨
* **HTML5:** Estruturação da página web.
* **CSS3:** Estilização da interface do usuário.
* **JavaScript:** Manipulação do DOM, interatividade e comunicação com o backend (API Fetch).

### Backend 🐍🔗
* **Python:** Linguagem principal para o backend e Machine Learning.
* **Flask:** Microframework web para criar a API RESTful e servir a aplicação.
* **Flask-CORS:** Extensão Flask para lidar com Cross-Origin Resource Sharing (CORS), permitindo a comunicação entre frontend e backend.

## ⚙️ Bibliotecas Python (Backend)

* **pandas** 🐼: Para leitura, manipulação e pré-processamento eficiente dos dados (incluindo arquivos `.ods`).
* **scikit-learn** 🤖: Para implementação do algoritmo KNN Regressor, pré-processamento (OneHotEncoder, Pipeline) e avaliação de modelos.
* **Flask** : Criação do servidor web e rotas da API.
* **Flask-CORS** 🔗: Habilita requisições entre diferentes origens (frontend -> backend).
* **joblib** 💾: Para salvar e carregar eficientemente o modelo de Machine Learning treinado (`pipeline`).
* **odfpy** 📄: Biblioteca necessária para que o `pandas` possa ler arquivos no formato OpenDocument Spreadsheet (`.ods`).


## 📁 Estrutura do Projeto
```
projeto_enem_knn/
├── backend/
│   ├── data/
│   │   └── microdados_enem2023.ods  
│   ├── model/
│   │   ├── knn_model.joblib        
│   │   └── preprocessor.joblib     
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css           
│   │   └── js/
│   │       └── script.js           
│   ├── templates/
│   │   └── index.html              
│   ├── app.py                      
│   ├── train_model.py              
│   └── requirements.txt            
├── print interface usuário.png     
└── README.md                      
```
## 🚀 Como Executar

1.  **Clone o Repositório:**
    ```bash
    git clone https://github.com/ThiagoMassenoMaciel/projeto_enem_knn.git
    cd projeto_enem_knn
    ```
2.  **Navegue até o Backend:**
    ```bash
    cd backend
    ```
3.  **Ative o Ambiente Virtual:**
    ```bash
    # Ativar (sempre que for trabalhar no projeto)
    # Windows:
    .\venv\Scripts\activate
    # macOS/Linux:
    source venv/bin/activate
    ```
4.  **Instale as Dependências:**
    ```bash
    pip install -r requirements.txt
    ```
5.  **Inicie a Aplicação Flask:**
    ```bash
    python app.py
    ```
8.  **Acesse no Navegador:** Abra seu navegador e acesse <http://127.0.0.1:5000> ou <http://localhost:5000>.

9.  **Utilize:** Preencha o formulário com os dados do aluno e clique em "Prever Notas" para ver o resultado! 🎉
---
