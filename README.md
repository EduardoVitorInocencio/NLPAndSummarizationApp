# **Summarize App**

Este projeto é um aplicativo de sumarização de texto construído com **Streamlit**, aproveitando várias bibliotecas de processamento de linguagem natural (NLP) como **Transformers** da Hugging Face e **Sumy**. O aplicativo permite que os usuários insiram texto e obtenham um resumo conciso usando dois algoritmos: **LexRank** (implementado usando o algoritmo LSA da Sumy) e **TextRank** (da Hugging Face). Os resultados são então avaliados usando a **pontuação ROUGE**, uma métrica padrão para sumarização de texto.

---

## **Bibliotecas Utilizadas**

### 1. **Streamlit**
O Streamlit é a biblioteca principal usada para criar a interface web. Ele permite elementos interativos como campos de entrada de texto, botões e visualizações. O layout e as interações do usuário são controlados por meio das funções do Streamlit.

- **Principais Funcionalidades:**
  - Áreas interativas para entrada de texto
  - Botão para acionar a sumarização
  - Colunas e expandidos para organizar resumos e avaliações
  - Visualização de métricas de resumo

### 2. **Transformers** (TextRank para sumarização)
Este aplicativo utiliza o `pipeline` da biblioteca Transformers da Hugging Face para **sumarização baseada em TextRank** usando o modelo `facebook/bart-large-cnn`, que é pré-treinado para tarefas de sumarização.

- **Funcionalidade Principal**:
  - Sumarização de texto usando modelos de deep learning.

### 3. **Sumy** (LexRank para sumarização)
O algoritmo **LexRank** é implementado usando a biblioteca Sumy, aproveitando especificamente o **sumarizador LSA (Latent Semantic Analysis)**. Ele tokeniza e analisa o texto de entrada para gerar um resumo baseado na extração de sentenças.

- **Funcionalidade Principal**:
  - Sumarização baseada em **Análise Semântica Latente (LSA)**.
  - Usa stemming e stopwords para uma melhor seleção de sentenças.

### 4. **ROUGE** (Métrica de Avaliação)
A métrica **ROUGE** é um método padrão para avaliar a qualidade de resumos gerados por máquinas, comparando-os a um resumo de referência. As pontuações ROUGE (ROUGE-1, ROUGE-2, ROUGE-L) refletem a sobreposição entre o resumo e o texto de referência em diferentes níveis de n-gramas.

- **Funcionalidade Principal**:
  - Avalia resumos calculando a sobreposição com o texto de referência.
  - Saídas em um DataFrame com as pontuações ROUGE-1, ROUGE-2 e ROUGE-L.

### 5. **NLTK**
O **Natural Language Toolkit (NLTK)** é utilizado principalmente para tokenização no algoritmo **LexRank da Sumy**, e o pacote necessário `punkt` é baixado e armazenado dentro do ambiente virtual.

- **Funcionalidade Principal**:
  - Tokenização e pré-processamento de texto.

### 6. **Pandas**
Usado para manipular e visualizar os resultados da avaliação, convertendo as pontuações ROUGE em um DataFrame para fácil manipulação e exibição.

### 7. **Matplotlib & Altair**
Utilizados para plotar métricas de avaliação de resumo em um formato fácil de ler. O **Altair** é particularmente útil para gerar gráficos interativos dentro do Streamlit.

---

## **Algoritmos e Racional dos Cálculos**

### 1. **LexRank (LSA)**
LexRank é um algoritmo baseado em grafos não supervisionado para sumarização de texto que utiliza extração de sentenças. Ele constrói um grafo de sentenças, onde cada sentença é um nó, e as arestas são baseadas na similaridade das sentenças.

- **Passos**:
  1. Tokenizar o texto em sentenças.
  2. Aplicar stemming e remover stopwords.
  3. Construir a matriz de similaridade de sentenças com base na sobreposição semântica.
  4. Selecionar sentenças-chave usando **Análise Semântica Latente (LSA)**.

### 2. **TextRank (do BART)**
TextRank é outra abordagem baseada em grafos, mas aplicada via modelos baseados em transformadores (como BART) neste caso. Ele identifica sentenças importantes e as extrai como um resumo.

- **Passos**:
  1. Codificar o texto de entrada.
  2. Usar o modelo de transformador para classificar sentenças com base na importância.
  3. Extrair as sentenças mais informativas para o resumo.

### 3. **Pontuação ROUGE**
A ROUGE compara a sobreposição de n-grams, sequências de palavras e pares de palavras entre o resumo gerado pela máquina e um resumo de referência.

- **ROUGE-1**: Mede a sobreposição de unigramas (nível de palavra).
- **ROUGE-2**: Mede a sobreposição de bigramas (sequência de duas palavras).
- **ROUGE-L**: Mede a sobreposição da maior subsequência comum.

---

## **Explicação dos Blocos de Código**

### 1. **Pipelines de Sumarização**
```python
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
```

Esta linha inicializa o pipeline de sumarização BART usando a biblioteca Transformers da Hugging Face.

### **2. Configuração do NLTK**
```python
# Define o caminho para o NLTK e baixa os pacotes necessários
nltk.data.path.append(venv_path)
nltk.download('punkt', download_dir=venv_path)
```

Este bloco garante que os dados do NLTK, como punkt, sejam baixados dentro do ambiente virtual e carregados a partir daí.

### **3. Sumarizador LexRank (Sumy)**

```python
def sumy_summarizer(paragraph, sentences_count=2):
    parser = PlaintextParser.from_string(paragraph, Tokenizer("english"))
    summarizer = LsaSummarizer(Stemmer("english"))
    summarizer.stop_words = get_stop_words("english")
    summary = summarizer(parser.document, sentences_count)
    return summary
```

Esta função realiza a sumarização baseada em LexRank, analisando o texto, aplicando stemming e extraindo as sentenças mais relevantes usando LSA.

### **4. Avaliação ROUGE**
```python
def evaluate_summary(summary, reference):
    r = Rouge()
    eval_score = r.get_scores(summary, reference)
    eval_score_df = pd.DataFrame(eval_score[0])
    return eval_score_df
```

Esta função calcula a pontuação ROUGE para um resumo gerado em relação a um resumo de referência, retornando os resultados como um DataFrame do Pandas.

### **Configuração e Instalação**
Para executar este projeto localmente, siga as instruções abaixo:

1. Clone este repositório.
2. Crie e ative um ambiente virtual.
```bash
python3 -m venv venv
source venv/bin/activate
```

3. Instale os pacotes necessários.
```bash
pip install -r requirements.txt
```

4. Execute o aplicativo Streamlit.
```bash
streamlit run app.py
```

# **Script bash**

```bash
# Clone o repositório
git clone https://github.com/seuusuario/summarize-app.git
cd summarize-app

# Crie e ative um ambiente virtual
python3 -m venv venv
source venv/bin/activate

# Instale as dependências necessárias
pip install -r requirements.txt

# Execute o aplicativo Streamlit
streamlit run app.py
```
