"""
Chatbot que personifica um autor baseado em seu/s livro/s
Usa Google Gemini API (gratuita)
"""

import google.generativeai as genai
from typing import List
import json
import numpy as np
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("ERRO: API Key não encontrada no .env")
    print("Verifique se o arquivo .env existe e tem: GEMINI_API_KEY=sua_chave")
    exit()
else:
    print(f"API Key carregada: {api_key[:20]}...")  # Mostra só os primeiros 20 caracteres
    
class AuthorChatbot:
    def __init__(self, api_key: str):
        """
        Inicializa o chatbot com a API key do Google
        
        Args:
            api_key: Sua chave da API do Google Gemini
        """
        genai.configure(api_key=api_key)

        # Configurações de geração (CUSTOMIZE AQUI!)
        generation_config = {
            'temperature': 0.8,      # Criatividade (0.0-2.0): 0.7 = equilibrado
            'top_p': 0.8,            # Diversidade (0.0-1.0): 0.8 = variado
            'top_k': 40,             # Alternativas (1-100): 40 = moderado
            'max_output_tokens': 800, # Tamanho máximo: 800 = resposta média
        }
        
        self.model = genai.GenerativeModel(
            'gemini-2.5-flash',
            generation_config=generation_config
        )

        self.model = genai.GenerativeModel('gemini-2.5-flash')  # Modelo gratuito e rápido
        self.embedding_model = 'models/text-embedding-004'  # Embedding gratuito
        
        self.chunks = []
        self.embeddings = []
        self.author_info = {}
        self.conversation_history = []
        
    def load_book(self, file_path: str, author_name: str, book_title: str):
        """
        Carrega e processa o livro
        
        Args:
            file_path: Caminho para o arquivo TXT do livro
            author_name: Nome do autor
            book_title: Título do livro
        """ 
        print("📚 Carregando livro...")
        
        with open(file_path, 'r', encoding='utf-8') as f:
            text = f.read()
        
        self.author_info = {
            'name': author_name,
            'book_title': book_title
        }
        
        # Divide em chunks inteligentes
        self.chunks = self._split_text(text)
        print(f"✂️  Livro dividido em {len(self.chunks)} pedaços")
        
        # Gera embeddings (busca semântica)
        print("🔍 Gerando embeddings (isso pode demorar um pouco)...")
        self.embeddings = self._generate_embeddings(self.chunks)
        print("✅ Livro processado com sucesso!")
        
    def _split_text(self, text: str, chunk_size: int = 1500, overlap: int = 200) -> List[str]:
        """
        Divide o texto em chunks inteligentes mantendo parágrafos inteiros
        """
        paragraphs = text.split('\n\n')
        chunks = []
        current_chunk = ""
        
        for para in paragraphs:
            para = para.strip()
            if not para:
                continue
                
            # Se adicionar este parágrafo ultrapassar o tamanho, salva o chunk atual
            if len(current_chunk) + len(para) > chunk_size and current_chunk:
                chunks.append(current_chunk.strip())
                # Mantém overlap pegando últimas palavras
                words = current_chunk.split()
                overlap_text = ' '.join(words[-overlap//5:]) if len(words) > overlap//5 else ""
                current_chunk = overlap_text + "\n\n" + para
            else:
                current_chunk += "\n\n" + para if current_chunk else para
        
        # Adiciona último chunk
        if current_chunk:
            chunks.append(current_chunk.strip())
            
        return chunks
    
    def _generate_embeddings(self, texts: List[str]) -> List[np.ndarray]:
        """
        Gera embeddings usando API gratuita do Google
        Processa em batches para economizar requisições
        """
        embeddings = []
        batch_size = 100  # Google permite até 100 por request
        
        for i in range(0, len(texts), batch_size):
            batch = texts[i:i + batch_size]
            
            # Gera embeddings do batch
            result = genai.embed_content(
                model=self.embedding_model,
                content=batch,
                task_type="retrieval_document"
            )
            
            embeddings.extend(result['embedding'])
            print(f"   Processados {min(i + batch_size, len(texts))}/{len(texts)} chunks")
        
        return [np.array(emb) for emb in embeddings]
    
    def _find_relevant_chunks(self, query: str, top_k: int = 3) -> List[str]:
        """
        Encontra os chunks mais relevantes para a pergunta
        """
        # Gera embedding da pergunta
        query_result = genai.embed_content(
            model=self.embedding_model,
            content=query,
            task_type="retrieval_query"
        )
        query_embedding = np.array(query_result['embedding'])
        
        # Calcula similaridade com cada chunk
        similarities = []
        for emb in self.embeddings:
            similarity = np.dot(query_embedding, emb) / (
                np.linalg.norm(query_embedding) * np.linalg.norm(emb)
            )
            similarities.append(similarity)
        
        # Pega os top_k mais similares
        top_indices = np.argsort(similarities)[-top_k:][::-1]
        
        return [self.chunks[i] for i in top_indices]
    
    def chat(self, user_message: str, show_sources: bool = False) -> str:
        """
        Conversa com o chatbot que personifica o autor
        
        Args:
            user_message: Mensagem do usuário
            show_sources: Se True, mostra os trechos do livro usados
            
        Returns:
            Resposta do "autor"
        """
        # Busca trechos relevantes
        relevant_chunks = self._find_relevant_chunks(user_message, top_k=3)
        
        # Monta o contexto
        context = "\n\n---\n\n".join(relevant_chunks)
        
        # Configurações de resposta (CUSTOMIZE AQUI!)
        response_config = {
            'tamanho': 'média',  # 'curta', 'média', 'longa', 'detalhada'
            'tom': 'assertivo',  # 'amigável', 'formal', 'assertivo', 'provocativo', 'filosófico'
            'formato': 'prosa'   # 'prosa', 'tópicos', 'misto'
        }
        
        # Instruções de tamanho
        tamanho_instrucoes = {
            'curta': 'Seja conciso. Responda em 2-3 frases no máximo.',
            'média': 'Responda em 1-2 parágrafos (4-6 frases).',
            'longa': 'Desenvolva sua resposta em 3-4 parágrafos.',
            'detalhada': 'Faça uma resposta completa e aprofundada, com exemplos e elaborações.'
        }
        
        # Instruções de tom
        tom_instrucoes = {
            'amigável': 'Use um tom caloroso e acolhedor, como se estivesse conversando com um amigo.',
            'formal': 'Mantenha um tom acadêmico e profissional.',
            'assertivo': 'Seja direto e confiante em suas afirmações.',
            'provocativo': 'Seja desafiador e faça o leitor questionar suas premissas.',
            'filosófico': 'Seja contemplativo e reflexivo, explorando nuances.'
        }
        
        # Instruções de formato
        formato_instrucoes = {
            'prosa': 'Responda em parágrafos corridos, de forma narrativa.',
            'tópicos': 'Organize sua resposta em tópicos claros e numerados.',
            'misto': 'Combine parágrafos com alguns pontos-chave destacados quando apropriado.'
        }

        # Cria o prompt otimizado
        prompt = f"""Você é {self.author_info['name']}, autor do livro "{self.author_info['book_title']}".

Responda à pergunta do leitor como se você fosse o próprio autor, usando suas ideias e estilo de escrita conforme expressos no livro.

ESTILO DE RESPOSTA:
- Tamanho: {tamanho_instrucoes[response_config['tamanho']]}
- Tom: {tom_instrucoes[response_config['tom']]}
- Formato: {formato_instrucoes[response_config['formato']]}

TRECHOS RELEVANTES DO SEU LIVRO:
{context}

PERGUNTA DO LEITOR:
{user_message}

Responda de forma natural, como o autor responderia. Use primeira pessoa ("eu acredito", "na minha visão"). 
Se a pergunta não puder ser respondida com base no livro, admita isso honestamente mantendo a persona do autor."""

        # Gera resposta
        response = self.model.generate_content(prompt)
        answer = response.text
        
        # Mostra fontes se solicitado
        if show_sources:
            sources_text = "\n\n📖 TRECHOS USADOS DO LIVRO:\n"
            for i, chunk in enumerate(relevant_chunks, 1):
                preview = chunk[:200] + "..." if len(chunk) > 200 else chunk
                sources_text += f"\n[{i}] {preview}\n"
            answer += sources_text
        
        return answer
    
    def save_knowledge_base(self, filepath: str):
        """
        Salva a base de conhecimento processada para reusar depois
        (Economiza API calls!)
        """
        data = {
            'author_info': self.author_info,
            'chunks': self.chunks,
            'embeddings': [emb.tolist() for emb in self.embeddings]
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False)
        
        print(f"💾 Base de conhecimento salva em {filepath}")
    
    def load_knowledge_base(self, filepath: str):
        """
        Carrega base de conhecimento já processada
        (Não precisa processar o livro de novo!)
        """
        print("📂 Carregando base de conhecimento...")
        
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        self.author_info = data['author_info']
        self.chunks = data['chunks']
        self.embeddings = [np.array(emb) for emb in data['embeddings']]
        
        print("✅ Base carregada com sucesso!")


# ============================================
# EXEMPLO DE USO
# ============================================

if __name__ == "__main__":

    from dotenv import load_dotenv
    import os
    
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        print("ERRO: API Key não encontrada no .env")
        exit()
    
    # 1. Configure sua API key
    API_KEY = api_key  # Pegue em: https://makersuite.google.com/app/apikey
    
    # 2. Crie o chatbot
    bot = AuthorChatbot(api_key=API_KEY)
    

    #3. PRIMEIRA VEZ: Carregue e processe o livro
    '''bot.load_book(
        file_path='livro.txt',
        author_name='Ted',
        book_title='Sociedade sem consequencias'
    )
    bot.save_knowledge_base('livro_processado.json')  # Salva para reusar
    '''
    # 4. DAS PRÓXIMAS VEZES: Só carregue o processado (MUITO MAIS RÁPIDO!)
    bot.load_knowledge_base('livro_processado.json')
    
    # 5. Converse!
    print("\n" + "="*50)
    print(f"💬 Chat com {bot.author_info['name']}")
    print("="*50)
    print("Digite 'sair' para encerrar\n")
    
    while True:
        user_input = input("Você: ")
        
        if user_input.lower() in ['sair', 'exit', 'quit']:
            print("👋 Até logo!")
            break
        
        response = bot.chat(user_input, show_sources=False)
        print(f"\n{bot.author_info['name']}: {response}\n")
        print("-" * 50)


"""
INSTRUÇÕES DE USO:

1. INSTALE AS DEPENDÊNCIAS:
   pip install google-generativeai numpy

2. PEGUE SUA API KEY:
   - Acesse: https://makersuite.google.com/app/apikey
   - Clique em "Create API Key"
   - Copie a chave

3. PREPARE SEU LIVRO:
   - Salve como arquivo .txt
   - Codificação UTF-8
   - Pode ter quantos caracteres quiser

4. RODE O CÓDIGO:
   - Na primeira vez: descomente as linhas do load_book()
   - O sistema vai processar e salvar
   - Das próximas vezes: só usa load_knowledge_base() (instantâneo!)

CUSTOS (100% GRATUITO):
- 15 requests/minuto
- 1 milhão de tokens/mês
- Embeddings ilimitados
- Perfeito para uso pessoal!
"""