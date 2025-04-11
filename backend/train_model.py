# backend/train_model.py

import pandas as pd                 # Importa pandas para manipulação de dados
# Embora não vamos dividir para teste aqui, é boa prática importar se fosse o caso
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsRegressor     # Importa o KNN Regressor
# Importa o OneHotEncoder para variáveis categóricas
from sklearn.preprocessing import OneHotEncoder
# Para aplicar transformações diferentes em colunas diferentes
from sklearn.compose import ColumnTransformer
# Para encadear pré-processamento e modelo
from sklearn.pipeline import Pipeline
# Importa joblib para salvar o modelo e o preprocessor
import joblib
import os                           # Importa os para manipulação de caminhos de arquivos

print("Iniciando o script de treinamento...")

# --- Configurações ---
# Caminho para o arquivo de dados (ajuste o nome se for diferente)
# Ou .csv se for o caso
DATA_PATH = os.path.join('data', 'microdados_enem2023.ods')
MODEL_DIR = 'model'                   # Diretório para salvar o modelo
# Caminho completo para salvar o modelo
MODEL_PATH = os.path.join(MODEL_DIR, 'knn_model.joblib')
# Caminho para salvar o pré-processador
PREPROCESSOR_PATH = os.path.join(MODEL_DIR, 'preprocessor.joblib')

# Certifica-se de que o diretório do modelo existe
os.makedirs(MODEL_DIR, exist_ok=True)  # Cria o diretório /model se não existir

# Colunas que serão usadas como features (características de entrada)
FEATURE_COLS = ['Q006', 'Q002', 'TP_ESCOLA', 'TP_COR_RACA', 'SG_UF_PROVA']
# Colunas que serão usadas como target (o que queremos prever)
TARGET_COLS = ['NU_NOTA_MT', 'NU_NOTA_CN',
               'NU_NOTA_LC', 'NU_NOTA_CH', 'NU_NOTA_REDACAO']

# Identifica quais features são categóricas (precisam de One-Hot Encoding)
CATEGORICAL_FEATURES = ['Q006', 'Q002',
                        'TP_ESCOLA', 'TP_COR_RACA', 'SG_UF_PROVA']

# --- 1. Carregamento dos Dados ---
print(f"Carregando dados de {DATA_PATH}...")
try:
    # Tenta ler como ODF. Se for CSV, use pd.read_csv(DATA_PATH, sep=';', encoding='iso-8859-1') # Ajuste sep e encoding conforme necessário
    df = pd.read_excel(DATA_PATH, engine='odf',
                       usecols=FEATURE_COLS + TARGET_COLS)
    print("Dados carregados com sucesso.")
except FileNotFoundError:
    print(
        f"Erro: Arquivo de dados não encontrado em {DATA_PATH}. Certifique-se de que ele está na pasta 'backend/data/'.")
    exit()  # Sai do script se não encontrar o arquivo
except Exception as e:
    print(f"Erro ao ler o arquivo: {e}")
    print("Verifique se o arquivo está no formato correto (ODS) e se a biblioteca 'odfpy' está instalada.")
    print("Se for um arquivo CSV, ajuste o código para usar pd.read_csv() com os parâmetros corretos (separador, encoding).")
    exit()  # Sai do script em caso de outro erro de leitura

# --- 2. Limpeza e Pré-processamento Básico ---
print("Iniciando limpeza e pré-processamento...")

# Remove linhas onde QUALQUER nota alvo (target) está ausente ou é zero
# Nota zero geralmente indica que o participante não fez a prova ou teve a redação anulada.
# Ausência (NaN) também impede o treinamento.
print(f"Linhas antes da limpeza de notas: {len(df)}")
df.dropna(subset=TARGET_COLS, inplace=True)  # Remove linhas com NaN nas notas
for col in TARGET_COLS:
    # Remove linhas com nota 0 (exceto talvez redação, mas vamos manter > 0 por segurança)
    df = df[df[col] > 0]
print(f"Linhas após limpeza de notas: {len(df)}")

# Trata valores ausentes nas FEATURES (variáveis de entrada)
# Estratégia simples: preencher com um valor específico 'Desconhecido' ou a moda.
# Aqui, vamos preencher com 'Desconhecido' (ou um código numérico/letra não usado)
# É importante que o OneHotEncoder depois reconheça essa categoria.
# Convertendo colunas para string para garantir consistência antes do fillna
for col in FEATURE_COLS:
    # Garante que são strings para o fillna e OneHotEncoder
    df[col] = df[col].astype(str)

df[FEATURE_COLS] = df[FEATURE_COLS].fillna('Desconhecido')


print("Valores ausentes nas features tratados.")

# --- 3. Definição do Pré-processador (One-Hot Encoding) ---
# Cria um transformador que aplica OneHotEncoder SOMENTE às colunas categóricas
# handle_unknown='ignore': Se uma categoria aparecer na previsão que não existia no treino, ignora (coloca zeros)
# sparse_output=False: Retorna uma matriz densa (numpy array) em vez de esparsa
preprocessor = ColumnTransformer(
    transformers=[
        ('cat', OneHotEncoder(handle_unknown='ignore',
         sparse_output=False), CATEGORICAL_FEATURES)
    ],
    # Mantém outras colunas (se houver) - neste caso não há outras features
    remainder='passthrough'
)

# --- 4. Separação de Features (X) e Targets (y) ---
X = df[FEATURE_COLS]
y = df[TARGET_COLS]
print("Features (X) e Targets (y) separados.")

# --- 5. Criação do Pipeline (Pré-processador + Modelo) ---
# Define o modelo KNN Regressor. n_neighbors=7 é um valor comum para começar.
# n_jobs=-1 usa todos os processadores disponíveis para acelerar (útil com dados grandes)
knn_regressor = KNeighborsRegressor(n_neighbors=7, n_jobs=-1)

# Cria o pipeline: primeiro aplica o pré-processador, depois treina o KNN
pipeline = Pipeline(steps=[('preprocessor', preprocessor),
                           ('regressor', knn_regressor)])
print("Pipeline criado (Pré-processador + KNN Regressor).")

# --- 6. Treinamento do Pipeline ---
print("Iniciando treinamento do pipeline...")
pipeline.fit(X, y)  # Treina o pipeline com os dados
print("Treinamento concluído.")

# --- 7. Salvando o Pipeline Treinado (inclui pré-processador) ---
# Salvar o pipeline inteiro garante que os dados de entrada na previsão
# passem exatamente pelo mesmo pré-processamento.
print(f"Salvando o pipeline treinado em {MODEL_PATH}...")
joblib.dump(pipeline, MODEL_PATH)
print("Pipeline salvo com sucesso!")

print("Script de treinamento finalizado.")
