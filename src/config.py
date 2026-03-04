"""
Configurações centralizadas do Author Chatbot
"""

import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Configurações do sistema"""
    
    # API
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    
    # Modelos
    GENERATION_MODEL = "llama-3.3-70b-versatile"  # Modelo atualizado do Groq
    EMBEDDING_MODEL = "all-MiniLM-L6-v2"  # Modelo local (gratuito)
    
    # Diretórios
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    DATA_DIR = os.path.join(BASE_DIR, "data")
    BOOKS_DIR = os.path.join(DATA_DIR, "books")
    PROCESSED_DIR = os.path.join(DATA_DIR, "processed")
    
    # Processamento de Texto
    CHUNK_SIZE = 2500  # Aumentado para gerar menos chunks
    CHUNK_OVERLAP = 300
    
    # Geração de Respostas
    GENERATION_CONFIG = {
        'temperature': 0.7,
        'top_p': 0.8,
        'top_k': 40,
        'max_output_tokens': 800,
    }
    
    # Perfis de Resposta
    RESPONSE_PROFILES = {
        'conciso': {
            'temperature': 0.5,
            'max_tokens': 300,
            'instrucao': 'Seja direto e conciso. Responda em 2-3 frases no máximo.'
        },
        'normal': {
            'temperature': 0.7,
            'max_tokens': 800,
            'instrucao': 'Responda de forma equilibrada em 1-2 parágrafos.'
        },
        'detalhado': {
            'temperature': 0.8,
            'max_tokens': 1500,
            'instrucao': 'Desenvolva sua resposta com profundidade e exemplos.'
        },
        'provocativo': {
            'temperature': 0.9,
            'max_tokens': 1000,
            'instrucao': 'Seja desafiador e provocativo. Questione premissas.'
        }
    }
    
    # Busca
    TOP_K_RESULTS = 3
    
    @classmethod
    def validate(cls):
        """Valida as configurações essenciais"""
        if not cls.GROQ_API_KEY:
            raise ValueError("GROQ_API_KEY não encontrada no .env")
        
        # Cria diretórios se não existirem
        os.makedirs(cls.BOOKS_DIR, exist_ok=True)
        os.makedirs(cls.PROCESSED_DIR, exist_ok=True)
        
        return True
    
    @classmethod
    def get_processed_file_path(cls, book_id: str) -> str:
        """Retorna o caminho do arquivo processado"""
        return os.path.join(cls.PROCESSED_DIR, f"{book_id}.json")
    
    @classmethod
    def list_processed_books(cls) -> list:
        """Lista todos os livros já processados"""
        if not os.path.exists(cls.PROCESSED_DIR):
            return []
        
        books = []
        for file in os.listdir(cls.PROCESSED_DIR):
            if file.endswith('.json'):
                books.append(file.replace('.json', ''))
        
        return books