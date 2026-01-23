# Talking-to-the-Author
put some books as input, and start to talk with your favorite AI_Author chatbot (or something close to that)

Um chatbot inteligente que personifica um autor baseado em suas obras, utilizando a API gratuita do Google Gemini e busca semântica (RAG).

## Características

- Personifica o autor respondendo como se fosse ele
- Busca semântica inteligente usando embeddings
- Otimizado para economia de API calls
- Sistema de cache para processamento único
- Suporte a livros de qualquer tamanho
- Configurações personalizáveis de tom e formato

## Pré-requisitos

- Python 3.8 ou superior
- Conta Google (para API Key gratuita)
- Livro em formato TXT (UTF-8)

## Instalação

### 1. Clone o repositório

```bash
git clone https://github.com/seu-usuario/author-chatbot.git
cd author-chatbot
```

### 2. Instale as dependências

```bash
pip install -r requirements.txt
```

Ou instale manualmente:

```bash
pip install google-generativeai numpy python-dotenv
```

### 3. Configure a API Key

Obtenha sua chave gratuita da API do Google Gemini:

1. Acesse: https://makersuite.google.com/app/apikey
2. Clique em "Create API Key"
3. Copie a chave gerada

Crie um arquivo `.env` na raiz do projeto:

```
GEMINI_API_KEY=sua_chave_api_aqui
```

## Uso

### Primeira Execução (Processamento do Livro)

No arquivo `main.py`, descomente as linhas de processamento:

```python
# Primeira vez: processa o livro
bot.load_book(
    file_path='caminho/para/seu/livro.txt',
    author_name='Nome do Autor',
    book_title='Título do Livro'
)
bot.save_knowledge_base('livro_processado.json')
```

Execute:

```bash
python main.py
```

O sistema irá:
- Dividir o livro em chunks inteligentes
- Gerar embeddings para busca semântica
- Salvar tudo em `livro_processado.json`

### Execuções Seguintes (Instantâneo)

Após o primeiro processamento, comente as linhas acima e use:

```python
# Das próximas vezes: carrega o processado
bot.load_knowledge_base('livro_processado.json')
```

Execute:

```bash
python main.py
```

## Estrutura do Projeto

```
author-chatbot/
│
├── TalkingAuthor.py                      # Código principal
├── .env                         # API Key (não commitar)
├── requirements.txt             # Dependências
├── livro_processado.json        # Cache do livro processado
├── seu_livro.txt               # Livro em formato texto
└── README.md                    # Este arquivo
```

## Configuração Avançada

### Personalizar Respostas

No `__init__` da classe `AuthorChatbot`, ajuste os parâmetros:

```python
generation_config = {
    'temperature': 0.7,      # Criatividade (0.0-2.0)
    'top_p': 0.8,            # Diversidade (0.0-1.0)
    'top_k': 40,             # Alternativas (1-100)
    'max_output_tokens': 800, # Tamanho da resposta
}
```

### Guia de Parâmetros

**Temperature (Criatividade):**
- 0.0-0.3: Respostas consistentes e previsíveis
- 0.4-0.7: Equilibrado (recomendado)
- 0.8-1.2: Criativo e variado
- 1.3-2.0: Muito criativo

**Max Output Tokens (Tamanho):**
- 200-400: Respostas curtas
- 500-800: Respostas médias (recomendado)
- 1000-1500: Respostas longas
- 2000+: Respostas muito detalhadas

### Personalizar Tom e Estilo

No método `chat()`, você pode modificar as configurações:

```python
response_config = {
    'tamanho': 'média',      # 'curta', 'média', 'longa', 'detalhada'
    'tom': 'assertivo',      # 'amigável', 'formal', 'assertivo', 'provocativo'
    'formato': 'prosa'       # 'prosa', 'tópicos', 'misto'
}
```

## Limites da API Gratuita

O plano gratuito do Google Gemini oferece:
- 15 requisições por minuto
- 1 milhão de tokens por mês
- Embeddings ilimitados

Adequado para uso pessoal e testes.

## Exemplos de Uso

### Conversa Básica

```
Você: Qual sua principal ideia no livro?
Autor: Na minha visão, a ideia central que defendo é...

Você: Como você aplicaria isso hoje?
Autor: Considerando o contexto atual...
```

### Mostrar Fontes

```python
response = bot.chat("sua pergunta", show_sources=True)
```

Isso incluirá os trechos do livro usados para gerar a resposta.

## Solução de Problemas

### Erro: Module not found

```bash
pip install google-generativeai numpy python-dotenv
```

### Erro: API Key não encontrada

Verifique se:
- O arquivo `.env` está na mesma pasta do `main.py`
- O formato está correto: `GEMINI_API_KEY=sua_chave`
- Não há espaços ou aspas extras

### Erro: Model not found

Liste os modelos disponíveis:

```python
import google.generativeai as genai
genai.configure(api_key="sua_key")
for m in genai.list_models():
    print(m.name)
```

Atualize o modelo no código conforme disponível.

### Erro: UnicodeDecodeError

Certifique-se de que seu arquivo TXT está em UTF-8:

```python
# Converter para UTF-8
with open('livro.txt', 'r', encoding='latin-1') as f:
    content = f.read()
with open('livro_utf8.txt', 'w', encoding='utf-8') as f:
    f.write(content)
```

## Otimizações Implementadas

- Processamento em batch de embeddings (100 por requisição)
- Sistema de cache (processa livro uma única vez)
- Busca semântica (envia apenas trechos relevantes)
- Divisão inteligente por parágrafos (mantém contexto)
- Uso do modelo Gemini 2.5 Flash (mais rápido e gratuito)


Obs: nos primeiros commits usei um livro meio suspeito, mas era oq tinha de pdf no linux, e tinha opinioes fortes p testar, n compactuo com o comportamento do autor, é isso, agora vão falar com algum autor ai.
