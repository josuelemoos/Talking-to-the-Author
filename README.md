# Author Chatbot

Um chatbot inteligente com interface gráfica que personifica autores baseado em suas obras, utilizando a API gratuita do Google Gemini e busca semântica (RAG).

## Características

- Interface gráfica intuitiva (Tkinter)
- Seleção de arquivo via diálogo
- Múltiplos livros em um único sistema
- Perfis de resposta configuráveis
- Busca semântica otimizada
- Sistema de cache eficiente
- Arquitetura modular e organizada

## Estrutura do Projeto

```
author-chatbot/
├── src/
│   ├── __init__.py
│   ├── chatbot.py           # Classe principal do chatbot
│   ├── embeddings.py        # Processamento de embeddings
│   ├── text_processor.py    # Divisão e processamento de texto
│   └── config.py            # Configurações
├── ui/
│   ├── __init__.py
│   └── interface.py         # Interface gráfica
├── data/ (se não tiver no rep, recomendo criar)
│   ├── books/               # Livros em TXT
│   └── processed/           # Bases processadas
├── .env                     # API Key
├── .gitignore
├── requirements.txt
├── README.md
└── main.py                  # Ponto de entrada
```

## Instalação

### 1. Clone o repositório

```bash
git clone https://github.com/seu-usuario/author-chatbot.git
cd author-chatbot
```

### 2. Crie os diretórios necessários

```bash
mkdir -p data/books data/processed src ui
```

### 3. Crie os arquivos `__init__.py`

```bash
touch src/__init__.py ui/__init__.py
```

### 4. Instale as dependências

```bash
pip install -r requirements.txt
```

### 5. Configure a API Key

Obtenha sua chave gratuita:
1. Acesse: https://makersuite.google.com/app/apikey
2. Clique em "Create API Key"
3. Copie a chave

Crie o arquivo `.env` na raiz:

```
GEMINI_API_KEY=sua_chave_api_aqui
```

## Uso

### Inicie a aplicação

```bash
python main.py
```

### Primeira vez

1. A interface de setup será exibida
2. Clique em "Selecionar" para escolher o arquivo TXT do livro
3. Preencha o nome do autor e título do livro
4. Clique em "Processar Livro"
5. Aguarde o processamento (aparece no log)
6. A interface de chat será aberta automaticamente

### Conversando

1. Digite sua pergunta na caixa de texto inferior
2. Pressione Enter ou clique em "Enviar"
3. Aguarde a resposta do "autor"
4. Continue a conversa naturalmente

### Múltiplos livros

1. Processe vários livros usando o botão "Novo Livro"
2. Alterne entre eles usando o dropdown "Livro"
3. Cada livro mantém seu próprio contexto

### Perfis de resposta

Use o dropdown "Perfil" para mudar o estilo:

- **Conciso**: Respostas curtas e diretas
- **Normal**: Equilibrado (padrão)
- **Detalhado**: Respostas aprofundadas
- **Provocativo**: Desafiador e questionador

## Arquivos dos Módulos

Você precisa criar os seguintes arquivos com o conteúdo fornecido:

1. `src/config.py` - Configurações centralizadas
2. `src/text_processor.py` - Processamento de texto
3. `src/embeddings.py` - Gerenciamento de embeddings
4. `src/chatbot.py` - Classe principal
5. `ui/interface.py` - Interface gráfica
6. `main.py` - Ponto de entrada

Os conteúdos desses arquivos foram fornecidos nos artifacts anteriores.

## Personalização

### Alterar parâmetros de resposta

Edite `src/config.py`:

```python
GENERATION_CONFIG = {
    'temperature': 0.7,       # 0.0-2.0 (criatividade)
    'top_p': 0.8,             # 0.0-1.0 (diversidade)
    'top_k': 40,              # 1-100 (alternativas)
    'max_output_tokens': 800, # tamanho máximo
}
```

### Criar novo perfil de resposta

Em `src/config.py`, adicione ao dicionário `RESPONSE_PROFILES`:

```python
'meu_perfil': {
    'temperature': 0.6,
    'max_tokens': 500,
    'instrucao': 'Suas instruções aqui.'
}
```

### Alterar tamanho dos chunks

Em `src/config.py`:

```python
CHUNK_SIZE = 1500      # Tamanho de cada chunk
CHUNK_OVERLAP = 200    # Sobreposição entre chunks
```

## Solução de Problemas

### Erro: tkinter não encontrado

**Linux:**
```bash
sudo apt-get install python3-tk
```

**Mac:**
```bash
brew install python-tk
```

**Windows:** Tkinter já vem incluído

### Erro: API Key não encontrada

Verifique:
- Arquivo `.env` na raiz do projeto
- Formato: `GEMINI_API_KEY=sua_chave` (sem espaços ou aspas)
- Chave válida do Google AI Studio

### Interface não abre

Teste a importação:
```python
python -c "import tkinter; print('OK')"
```

### Arquivo não processa

Verifique:
- Arquivo está em UTF-8
- Formato TXT (não PDF)
- Caminho do arquivo está correto

## Recursos Técnicos

### Processamento de texto

- Divisão inteligente por parágrafos
- Preservação de contexto com overlap
- Suporte a múltiplas codificações
- Limpeza automática de formatação

### Busca semântica

- Embeddings do Google (text-embedding-004)
- Similaridade de cosseno
- Top-k retrieval configurável
- Processamento em batch otimizado

### Interface

- Thread separada para processamento
- Sem travamento da UI
- Log de status em tempo real
- Múltiplos livros gerenciados
- Mudança de perfil dinâmica

## Limites da API Gratuita

- 15 requisições por minuto
- 1 milhão de tokens por mês
- Embeddings ilimitados

Adequado para uso pessoal e projetos pequenos.

## Licença

MIT License
- [ ] Deploy web
- [ ] Suporte a imagens
- [ ] Análise de sentimento
