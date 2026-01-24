"""
Gerenciador de embeddings e busca semântica
"""

import google.generativeai as genai
import numpy as np
from typing import List, Tuple
from src.config import Config

class EmbeddingManager:
    """Gerencia embeddings e busca semântica"""
    
    def __init__(self, api_key: str = None):
        api_key = api_key or Config.GEMINI_API_KEY
        genai.configure(api_key=api_key)
        self.model = Config.EMBEDDING_MODEL
    
    def generate_embeddings(self, texts: List[str], show_progress: bool = True) -> List[np.ndarray]:
        """
        Gera embeddings em batch
        
        Args:
            texts: Lista de textos
            show_progress: Se deve mostrar progresso
            
        Returns:
            Lista de embeddings como arrays numpy
        """
        embeddings = []
        batch_size = 100
        total = len(texts)
        
        for i in range(0, total, batch_size):
            batch = texts[i:i + batch_size]
            
            result = genai.embed_content(
                model=self.model,
                content=batch,
                task_type="retrieval_document"
            )
            
            embeddings.extend(result['embedding'])
            
            if show_progress:
                processed = min(i + batch_size, total)
                print(f"Processados {processed}/{total} chunks")
        
        return [np.array(emb) for emb in embeddings]
    
    def generate_query_embedding(self, query: str) -> np.ndarray:
        """Gera embedding para uma query"""
        result = genai.embed_content(
            model=self.model,
            content=query,
            task_type="retrieval_query"
        )
        return np.array(result['embedding'])
    
    def find_similar(
        self, 
        query_embedding: np.ndarray, 
        document_embeddings: List[np.ndarray],
        top_k: int = None
    ) -> List[int]:
        """
        Encontra os documentos mais similares
        
        Args:
            query_embedding: Embedding da query
            document_embeddings: Lista de embeddings dos documentos
            top_k: Número de resultados
            
        Returns:
            Índices dos documentos mais similares
        """
        top_k = top_k or Config.TOP_K_RESULTS
        
        similarities = []
        for doc_emb in document_embeddings:
            similarity = self._cosine_similarity(query_embedding, doc_emb)
            similarities.append(similarity)
        
        # Retorna índices dos top_k mais similares
        top_indices = np.argsort(similarities)[-top_k:][::-1]
        return top_indices.tolist()
    
    @staticmethod
    def _cosine_similarity(vec1: np.ndarray, vec2: np.ndarray) -> float:
        """Calcula similaridade de cosseno"""
        return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))