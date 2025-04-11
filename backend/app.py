# backend/app.py

# Importa Flask e funções para lidar com requisições, JSON e templates HTML
from flask import Flask, request, jsonify, render_template
# Importa CORS para permitir requisições de origens diferentes
from flask_cors import CORS
# Importa joblib para carregar o modelo treinado
import joblib
# Importa pandas para criar DataFrame com os dados do usuário
import pandas as pd
import os                                       # Importa os para caminhos de arquivos

# --- Inicialização do Flask e Configurações ---
# Inicializa a aplicação Flask, especificando onde estão os arquivos estáticos e templates
app = Flask(__name__, static_folder='static', template_folder='templates')
CORS(app)  # Habilita o CORS para toda a aplicação, permitindo requisições do frontend

# --- Carregamento do Modelo Pré-Treinado ---
# Caminho para o modelo salvo pelo script train_model.py
MODEL_PATH = os.path.join('model', 'knn_model.joblib')

# Tenta carregar o modelo. Se não existir, a aplicação não pode funcionar.
try:
    print(f"Carregando modelo de {MODEL_PATH}...")
    # Carrega o pipeline (pré-processador + modelo)
    pipeline = joblib.load(MODEL_PATH)
    print("Modelo carregado com sucesso!")
    # Extrai os nomes das colunas originais esperadas pelo pré-processador
    expected_columns = ['Q006', 'Q002',
                        'TP_ESCOLA', 'TP_COR_RACA', 'SG_UF_PROVA']
    print(f"Colunas esperadas pelo modelo: {expected_columns}")
except FileNotFoundError:
    print(f"Erro: Modelo não encontrado em {MODEL_PATH}.")
    print("Execute o script 'train_model.py' primeiro para treinar e salvar o modelo.")
    pipeline = None  # Define como None para indicar que não foi carregado
except Exception as e:
    print(f"Erro ao carregar o modelo: {e}")
    pipeline = None  # Define como None para indicar que não foi carregado

# --- Definição das Rotas da API ---

# Rota principal '/' para servir a página HTML do frontend


@app.route('/')
def home():
    """
    Renderiza e serve a página HTML principal (interface do usuário).
    """
    print("Requisição recebida na rota '/', servindo index.html...")
    # Flask procura por 'index.html' dentro da pasta 'templates'
    return render_template('index.html')

# Rota '/predict' para receber dados do aluno e retornar a previsão


# Aceita apenas requisições do tipo POST
@app.route('/predict', methods=['POST'])
def predict():
    """
    Recebe dados do aluno via JSON, usa o modelo KNN para prever notas e retorna as previsões.
    """
    print("Requisição recebida na rota '/predict' (POST)...")
    # Verifica se o modelo foi carregado corretamente
    if pipeline is None:
        print("Erro: Modelo não está carregado.")
        # Retorna um erro 500 (Internal Server Error) em formato JSON
        return jsonify({'error': 'Modelo de previsão não está disponível. Contate o administrador.'}), 500

    try:
        # 1. Pega os dados enviados pelo frontend no corpo da requisição (espera-se JSON)
        data = request.get_json()
        print(f"Dados recebidos do frontend: {data}")

        # Verifica se os dados recebidos são um dicionário
        if not isinstance(data, dict):
            raise ValueError(
                "Formato de dados inválido. Esperado um objeto JSON.")

        # 2. Organiza os dados recebidos em um DataFrame do Pandas
        #    É crucial que as colunas aqui correspondam exatamente às features
        #    esperadas pelo pipeline (FEATURE_COLS do train_model.py)
        #    O DataFrame precisa ter uma linha.
        input_df = pd.DataFrame([data])  # Cria um DataFrame com uma linha
        print(f"DataFrame criado para previsão:\n{input_df}")

        # Garante que as colunas estão na ordem correta e são do tipo string (como no treino)
        # Reordena e converte, assegurando consistência com o treino.
        input_df = input_df[expected_columns].astype(str)
        print(
            f"DataFrame após seleção/ordenação e conversão para string:\n{input_df}")

        # 3. Usa o pipeline carregado (que foi a leitura do arquivo .joblib salvo na pasta model ficou armazenado dentro da variavel pipeline) para fazer a previsão
        #    O pipeline aplica automaticamente o mesmo pré-processamento (OneHotEncoding)
        #    que foi feito durante o treinamento e depois usa o KNN.
        print("Realizando previsão com o pipeline...")
        predictions = pipeline.predict(input_df)
        print(f"Previsões brutas do modelo: {predictions}")

        # 4. Formata a saída da previsão
        #    O K-NN Regressor para múltiplas saídas retorna um array numpy 2D,
        #    mesmo para uma única previsão. Ex: [[nota_mt, nota_cn, ...]]
        #    Pegamos a primeira (e única) linha de previsões.
        predicted_scores = predictions[0]

        # Cria um dicionário para retornar como JSON, associando cada nota prevista
        # à sua respectiva área do conhecimento. Arredondamos para 2 casas decimais depois da vírgula.
        output = {
            'NU_NOTA_MT': round(predicted_scores[0], 2),
            'NU_NOTA_CN': round(predicted_scores[1], 2),
            'NU_NOTA_LC': round(predicted_scores[2], 2),
            'NU_NOTA_CH': round(predicted_scores[3], 2),
            'NU_NOTA_REDACAO': round(predicted_scores[4], 2)
        }
        print(f"Previsões formatadas para resposta: {output}")

        # 5. Retorna as previsões formatadas como JSON para o frontend
        return jsonify(output)

    # Tratamento de Erros durante a previsão
    except KeyError as e:
        # Erro se alguma chave esperada (ex: 'Q006') não foi enviada pelo frontend
        print(f"Erro: Chave ausente nos dados recebidos - {e}")
        # Bad Request
        return jsonify({'error': f'Dado ausente no formulário: {e}. Verifique o preenchimento.'}), 400
    except ValueError as e:
        # Erro se os dados não forem JSON ou tiverem formato inesperado
        print(f"Erro de valor nos dados recebidos: {e}")
        # Bad Request
        return jsonify({'error': f'Erro no formato dos dados: {e}'}), 400
    except Exception as e:
        # Captura qualquer outro erro inesperado durante o processo
        print(f"Erro inesperado durante a previsão: {e}")
        # Retorna um erro genérico para não expor detalhes internos
        # Internal Server Error
        return jsonify({'error': 'Ocorreu um erro interno ao processar a previsão.'}), 500


# --- Execução da Aplicação Flask ---
# Verifica se este script está sendo executado diretamente (  que não seja importado)
if __name__ == '__main__':
    # Inicia o servidor de desenvolvimento do Flask
    # host='0.0.0.0' permite acesso de outras máquinas na mesma rede (útil para testes)
    # port=5000 é a porta padrão do Flask
    # debug=True ativa o modo de depuração (mostra erros detalhados no navegador e recarrega automaticamente após salvar o código)
    print("Iniciando o servidor Flask...")
    app.run(host='0.0.0.0', port=5000, debug=True)
