"""
Classe principal do chatbot
"""

import warnings
# Deve vir ANTES do import do google.generativeai
warnings.filterwarnings('ignore', category=FutureWarning)

import google.generativeai as genai
import json
import numpy as np
from typing import List, Dict
from src.config import Config
from src.text_processor import TextProcessor
from src.embeddings import EmbeddingManager

class AuthorChatbot:
    """Chatbot que personifica um autor"""
    
    def __init__(self, api_key: str = None, response_profile: str = 'normal'):
        self.api_key = api_key or Config.GEMINI_API_KEY
        genai.configure(api_key=self.api_key)
        
        # Configura modelo com perfil de resposta
        self.response_profile = response_profile
        profile = Config.RESPONSE_PROFILES[response_profile]
        
        generation_config = Config.GENERATION_CONFIG.copy()
        generation_config['temperature'] = profile['temperature']
        generation_config['max_output_tokens'] = profile['max_tokens']
        
        self.model = genai.GenerativeModel(
            Config.GENERATION_MODEL,
            generation_config=generation_config
        )
        
        # Componentes
        self.text_processor = TextProcessor()
        self.embedding_manager = EmbeddingManager(self.api_key)
        
        # Dados
        self.author_info = {}
        self.chunks = []
        self.embeddings = []
    
    def process_book(self, file_path: str, author_name: str, book_title: str) -> Dict:
        """
        Processa um livro
        
        Args:
            file_path: Caminho do arquivo TXT
            author_name: Nome do autor
            book_title: Título do livro
            
        Returns:
            Dicionário com estatísticas
        """
        print(f"Carregando livro: {book_title}")
        text = self.text_processor.load_from_file(file_path)
        
        print("Dividindo em chunks...")
        self.chunks = self.text_processor.split_into_chunks(text)
        
        print(f"Gerando embeddings para {len(self.chunks)} chunks...")
        self.embeddings = self.embedding_manager.generate_embeddings(self.chunks)
        
        self.author_info = {
            'name': author_name,
            'book_title': book_title,
            'file_path': file_path
        }
        
        stats = self.text_processor.get_statistics(text)
        stats['actual_chunks'] = len(self.chunks)
        
        print("Processamento concluído!")
        return stats
    
    def save_knowledge_base(self, filepath: str):
        """Salva base de conhecimento"""
        data = {
            'author_info': self.author_info,
            'chunks': self.chunks,
            'embeddings': [emb.tolist() for emb in self.embeddings],
            'response_profile': self.response_profile
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"Base salva em: {filepath}")
    
    def load_knowledge_base(self, filepath: str):
        """Carrega base de conhecimento"""
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        self.author_info = data['author_info']
        self.chunks = data['chunks']
        self.embeddings = [np.array(emb) for emb in data['embeddings']]
        
        if 'response_profile' in data:
            self.set_response_profile(data['response_profile'])
        
        print(f"Base carregada: {self.author_info['book_title']}")
    
    def set_response_profile(self, profile: str):
        """Altera o perfil de resposta"""
        if profile not in Config.RESPONSE_PROFILES:
            raise ValueError(f"Perfil inválido. Use: {list(Config.RESPONSE_PROFILES.keys())}")
        
        self.response_profile = profile
        profile_config = Config.RESPONSE_PROFILES[profile]
        
        generation_config = Config.GENERATION_CONFIG.copy()
        generation_config['temperature'] = profile_config['temperature']
        generation_config['max_output_tokens'] = profile_config['max_tokens']
        
        self.model = genai.GenerativeModel(
            Config.GENERATION_MODEL,
            generation_config=generation_config
        )
    
    def chat(self, user_message: str, show_sources: bool = False) -> str:
        """
        Conversa com o chatbot
        
        Args:
            user_message: Mensagem do usuário
            show_sources: Se deve mostrar trechos usados
            
        Returns:
            Resposta do autor
        """
        # Busca trechos relevantes
        query_embedding = self.embedding_manager.generate_query_embedding(user_message)
        relevant_indices = self.embedding_manager.find_similar(
            query_embedding, 
            self.embeddings
        )
        
        relevant_chunks = [self.chunks[i] for i in relevant_indices]
        context = "\n\n---\n\n".join(relevant_chunks)
        
        # Monta prompt
        profile = Config.RESPONSE_PROFILES[self.response_profile]
        
        prompt = f"""Você é {self.author_info['name']}, autor do livro "{self.author_info['book_title']}".

Responda à pergunta do leitor como se você fosse o próprio autor, usando suas ideias e estilo de escrita conforme expressos no livro.

ESTILO DE RESPOSTA:
{profile['instrucao']}

TRECHOS RELEVANTES DO SEU LIVRO:
{context}

PERGUNTA DO LEITOR:
{user_message}

Responda de forma natural, como o autor responderia. Use primeira pessoa. 
Se a pergunta não puder ser respondida com base no livro, admita isso honestamente mantendo a persona do autor."""

        # Gera resposta
        response = self.model.generate_content(prompt)
        answer = response.text
        
        if show_sources:
            sources_text = "\n\n--- TRECHOS USADOS DO LIVRO ---\n"
            for i, chunk in enumerate(relevant_chunks, 1):
                preview = chunk[:200] + "..." if len(chunk) > 200 else chunk
                sources_text += f"\n[{i}] {preview}\n"
            answer += sources_text
        
        return answer
    
    def get_info(self) -> Dict:
        """Retorna informações sobre o chatbot"""
        return {
            'author': self.author_info.get('name', 'Desconhecido'),
            'book': self.author_info.get('book_title', 'Desconhecido'),
            'chunks': len(self.chunks),
            'profile': self.response_profile
        }