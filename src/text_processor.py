"""
Processador de texto para divisão em chunks
"""

from typing import List
from src.config import Config
import os

class TextProcessor:
    """Processa e divide texto em chunks inteligentes"""
    
    def __init__(self, chunk_size: int = None, overlap: int = None):
        self.chunk_size = chunk_size or Config.CHUNK_SIZE
        self.overlap = overlap or Config.CHUNK_OVERLAP
    
    def load_from_file(self, file_path: str) -> str:
        """Carrega texto de um arquivo (TXT ou PDF)"""
        file_ext = os.path.splitext(file_path)[1].lower()
        
        if file_ext == '.pdf':
            return self._load_from_pdf(file_path)
        elif file_ext == '.txt':
            return self._load_from_txt(file_path)
        else:
            raise ValueError(f"Formato não suportado: {file_ext}. Use .txt ou .pdf")
    
    def _load_from_txt(self, file_path: str) -> str:
        """Carrega texto de arquivo TXT"""
        encodings = ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1']
        
        for encoding in encodings:
            try:
                with open(file_path, 'r', encoding=encoding) as f:
                    return f.read()
            except UnicodeDecodeError:
                continue
        
        raise ValueError(f"Não foi possível ler o arquivo com nenhuma codificação testada")
    
    def _load_from_pdf(self, file_path: str) -> str:
        """Carrega texto de arquivo PDF"""
        try:
            from PyPDF2 import PdfReader
            
            reader = PdfReader(file_path)
            text = ""
            
            for page in reader.pages:
                text += page.extract_text() + "\n\n"
            
            if not text.strip():
                raise ValueError("Não foi possível extrair texto do PDF. O arquivo pode estar protegido ou ser uma imagem.")
            
            return text
        except ImportError:
            raise ImportError("PyPDF2 não está instalado. Execute: pip install PyPDF2")
        except Exception as e:
            raise ValueError(f"Erro ao ler PDF: {str(e)}")
    
    def split_into_chunks(self, text: str) -> List[str]:
        """
        Divide o texto em chunks mantendo parágrafos inteiros
        
        Args:
            text: Texto completo do livro
            
        Returns:
            Lista de chunks
        """
        paragraphs = text.split('\n\n')
        chunks = []
        current_chunk = ""
        
        for para in paragraphs:
            para = para.strip()
            if not para:
                continue
            
            # Se adicionar ultrapassar o tamanho, salva o chunk atual
            if len(current_chunk) + len(para) > self.chunk_size and current_chunk:
                chunks.append(current_chunk.strip())
                
                # Mantém overlap pegando últimas palavras
                words = current_chunk.split()
                overlap_words = int(self.overlap / 5)
                overlap_text = ' '.join(words[-overlap_words:]) if len(words) > overlap_words else ""
                current_chunk = overlap_text + "\n\n" + para if overlap_text else para
            else:
                current_chunk += "\n\n" + para if current_chunk else para
        
        # Adiciona último chunk
        if current_chunk:
            chunks.append(current_chunk.strip())
        
        return chunks
    
    def clean_text(self, text: str) -> str:
        """Limpa o texto removendo caracteres indesejados"""
        # Remove múltiplas quebras de linha
        text = '\n\n'.join([p for p in text.split('\n\n') if p.strip()])
        
        # Remove espaços extras
        text = ' '.join(text.split())
        
        return text
    
    def get_statistics(self, text: str) -> dict:
        """Retorna estatísticas sobre o texto"""
        return {
            'total_characters': len(text),
            'total_words': len(text.split()),
            'total_paragraphs': len([p for p in text.split('\n\n') if p.strip()]),
            'estimated_chunks': len(text) // self.chunk_size + 1
        }