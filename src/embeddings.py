"""
Gerenciador de embeddings e busca semântica - Versão Leve
"""

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from typing import List
from src.config import Config

class EmbeddingManager:
    """Gerencia embeddings e busca semântica usando TF-IDF (muito leve!)"""
    
    def __init__(self, api_key: str = None):
        # TF-IDF - método clássico, leve e eficiente
        print("Inicializando sistema de busca (TF-IDF)...")
        self.vectorizer = TfidfVectorizer(
            max_features=1000,
            ngram_range=(1, 2),
            stop_words=None
        )
        self.document_vectors = None
        self.fitted = False
        print("Sistema pronto!")
    
    def generate_embeddings(self, texts: List[str], show_progress: bool = True) -> List[np.ndarray]:
        """
        Gera embeddings usando TF-IDF
        
        Args:
            texts: Lista de textos
            show_progress: Se deve mostrar progresso
            
        Returns:
            Lista de embeddings como arrays numpy
        """
        if show_progress:
            print(f"Gerando índice de busca para {len(texts)} chunks...")
        
        # Gera vetores TF-IDF
        self.document_vectors = self.vectorizer.fit_transform(texts)
        self.fitted = True
        
        if show_progress:
            print(f"Índice criado com sucesso!")
        
        # Converte para lista de arrays numpy
        embeddings = []
        for i in range(self.document_vectors.shape[0]):
            embeddings.append(self.document_vectors[i].toarray()[0])
        
        return embeddings
    
    def find_similar_texts(self, query: str, texts: List[str], top_k: int = 3) -> List[int]:
        """
        Encontra textos similares à query (método simplificado)
        
        Args:
            query: Texto da query
            texts: Lista de textos para buscar
            top_k: Número de resultados
            
        Returns:
            Índices dos textos mais similares
        """
        if not self.fitted:
            raise ValueError("Embeddings ainda não foram gerados. Chame generate_embeddings primeiro.")
        
        # Transforma a query usando o mesmo vectorizer
        query_vector = self.vectorizer.transform([query])
        
        # Calcula similaridade
        similarities = cosine_similarity(query_vector, self.document_vectors)[0]
        
        # Retorna índices dos top_k mais similares
        top_indices = np.argsort(similarities)[-top_k:][::-1]
        return top_indices.tolist()
    
    def generate_query_embedding(self, query: str) -> np.ndarray:
        """Gera embedding para uma query (retrocompatibilidade)"""
        if not self.fitted:
            raise ValueError("Embeddings ainda não foram gerados")
        
        query_vector = self.vectorizer.transform([query])
        return query_vector.toarray()[0]
    
    def find_similar(
        self, 
        query_embedding: np.ndarray, 
        document_embeddings: List[np.ndarray],
        top_k: int = None
    ) -> List[int]:
        """Método de retrocompatibilidade"""
        top_k = top_k or Config.TOP_K_RESULTS
        
        # Calcula similaridade
        similarities = cosine_similarity(
            query_embedding.reshape(1, -1),
            np.array(document_embeddings)
        )[0]
        
        # Retorna índices dos top_k mais similares
        top_indices = np.argsort(similarities)[-top_k:][::-1]
        return top_indices.tolist()