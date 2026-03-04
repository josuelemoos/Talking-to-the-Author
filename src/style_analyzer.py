"""
Analisador de estilo de escrita do autor
"""

import re
from collections import Counter
from typing import Dict, List
import numpy as np

class StyleAnalyzer:
    """Analisa e extrai características estilísticas do texto do autor"""
    
    def __init__(self):
        self.style_profile = {}
    
    def analyze_text(self, text: str) -> Dict:
        """
        Analisa o texto completo e extrai características de estilo
        
        Args:
            text: Texto completo do livro
            
        Returns:
            Dicionário com perfil de estilo
        """
        print("Analisando estilo de escrita do autor...")
        
        # Divide em frases
        sentences = self._split_sentences(text)
        
        # Análises
        self.style_profile = {
            'sentence_stats': self._analyze_sentences(sentences),
            'vocabulary': self._analyze_vocabulary(text),
            'punctuation': self._analyze_punctuation(text),
            'tone': self._analyze_tone(text),
            'structure': self._analyze_structure(text),
            'signature_words': self._find_signature_words(text),
            'writing_patterns': self._analyze_patterns(sentences)
        }
        
        print("Análise de estilo concluída!")
        return self.style_profile
    
    def _split_sentences(self, text: str) -> List[str]:
        """Divide texto em frases"""
        # Regex para dividir em frases (simplificado)
        sentences = re.split(r'[.!?]+\s+', text)
        return [s.strip() for s in sentences if s.strip()]
    
    def _analyze_sentences(self, sentences: List[str]) -> Dict:
        """Analisa características das frases"""
        lengths = [len(s.split()) for s in sentences]
        
        return {
            'avg_length': np.mean(lengths),
            'median_length': np.median(lengths),
            'min_length': min(lengths),
            'max_length': max(lengths),
            'std_length': np.std(lengths),
            'total_sentences': len(sentences),
            'short_sentences': sum(1 for l in lengths if l < 10),  # < 10 palavras
            'long_sentences': sum(1 for l in lengths if l > 30),   # > 30 palavras
        }
    
    def _analyze_vocabulary(self, text: str) -> Dict:
        """Analisa vocabulário"""
        words = re.findall(r'\b\w+\b', text.lower())
        unique_words = set(words)
        
        # Palavras longas (>7 letras) indicam vocabulário sofisticado
        long_words = [w for w in words if len(w) > 7]
        
        return {
            'total_words': len(words),
            'unique_words': len(unique_words),
            'vocabulary_richness': len(unique_words) / len(words) if words else 0,
            'avg_word_length': np.mean([len(w) for w in words]),
            'long_words_ratio': len(long_words) / len(words) if words else 0
        }
    
    def _analyze_punctuation(self, text: str) -> Dict:
        """Analisa uso de pontuação"""
        total_chars = len(text)
        
        return {
            'exclamation_ratio': text.count('!') / total_chars,
            'question_ratio': text.count('?') / total_chars,
            'semicolon_ratio': text.count(';') / total_chars,
            'colon_ratio': text.count(':') / total_chars,
            'dash_ratio': text.count('—') / total_chars,
            'comma_ratio': text.count(',') / total_chars,
            'parentheses_ratio': text.count('(') / total_chars,
            'quote_ratio': text.count('"') / total_chars
        }
    
    def _analyze_tone(self, text: str) -> Dict:
        """Analisa tom geral do texto"""
        text_lower = text.lower()
        
        # Palavras indicadoras de tom
        formal_words = ['portanto', 'todavia', 'outrossim', 'conquanto', 'destarte']
        informal_words = ['tipo', 'cara', 'né', 'pô', 'legal']
        assertive_words = ['claramente', 'obviamente', 'certamente', 'indubitavelmente']
        questioning_words = ['talvez', 'possivelmente', 'aparentemente', 'supostamente']
        
        return {
            'formality_score': sum(text_lower.count(w) for w in formal_words),
            'informality_score': sum(text_lower.count(w) for w in informal_words),
            'assertiveness_score': sum(text_lower.count(w) for w in assertive_words),
            'questioning_score': sum(text_lower.count(w) for w in questioning_words),
            'is_formal': sum(text_lower.count(w) for w in formal_words) > 
                         sum(text_lower.count(w) for w in informal_words)
        }
    
    def _analyze_structure(self, text: str) -> Dict:
        """Analisa estrutura de argumentação"""
        paragraphs = [p for p in text.split('\n\n') if p.strip()]
        
        # Procura por marcadores de estrutura
        has_lists = bool(re.search(r'^\s*[-•]\s', text, re.MULTILINE))
        has_numbering = bool(re.search(r'^\s*\d+[\.)]\s', text, re.MULTILINE))
        
        return {
            'avg_paragraph_length': np.mean([len(p.split()) for p in paragraphs]),
            'total_paragraphs': len(paragraphs),
            'uses_lists': has_lists,
            'uses_numbering': has_numbering
        }
    
    def _find_signature_words(self, text: str, top_n: int = 20) -> List[str]:
        """Encontra palavras características do autor"""
        # Remove stopwords comuns
        common_stopwords = {
            'o', 'a', 'de', 'da', 'do', 'em', 'um', 'uma', 'os', 'as', 
            'dos', 'das', 'para', 'com', 'por', 'que', 'se', 'no', 'na',
            'é', 'são', 'foi', 'como', 'mais', 'ou', 'e', 'ao', 'aos'
        }
        
        words = re.findall(r'\b\w+\b', text.lower())
        words = [w for w in words if w not in common_stopwords and len(w) > 3]
        
        # Conta frequência
        word_freq = Counter(words)
        
        # Retorna as mais frequentes
        return [word for word, count in word_freq.most_common(top_n)]
    
    def _analyze_patterns(self, sentences: List[str]) -> Dict:
        """Analisa padrões de escrita"""
        # Procura por padrões comuns
        starts_with_question = sum(1 for s in sentences if s.strip().startswith(('Como', 'Por que', 'Qual', 'Onde', 'Quando', 'Quem')))
        uses_examples = sum(1 for s in sentences if 'por exemplo' in s.lower() or 'como' in s.lower())
        uses_contrasts = sum(1 for s in sentences if any(w in s.lower() for w in ['mas', 'porém', 'entretanto', 'contudo', 'todavia']))
        
        return {
            'rhetorical_questions_ratio': starts_with_question / len(sentences) if sentences else 0,
            'uses_examples_ratio': uses_examples / len(sentences) if sentences else 0,
            'uses_contrasts_ratio': uses_contrasts / len(sentences) if sentences else 0
        }
    
    def get_style_description(self) -> str:
        """Gera descrição textual do estilo para usar no prompt"""
        if not self.style_profile:
            return ""
        
        desc = []
        
        # Tamanho de frases
        avg_len = self.style_profile['sentence_stats']['avg_length']
        if avg_len < 15:
            desc.append("Escreve frases curtas e diretas")
        elif avg_len > 25:
            desc.append("Usa frases longas e elaboradas")
        else:
            desc.append("Equilibra entre frases curtas e longas")
        
        # Vocabulário
        vocab_rich = self.style_profile['vocabulary']['vocabulary_richness']
        if vocab_rich > 0.4:
            desc.append("possui vocabulário rico e variado")
        
        # Tom
        if self.style_profile['tone']['is_formal']:
            desc.append("mantém tom formal e acadêmico")
        else:
            desc.append("usa linguagem mais coloquial")
        
        # Pontuação característica
        punct = self.style_profile['punctuation']
        if punct['exclamation_ratio'] > 0.001:
            desc.append("usa exclamações para ênfase")
        if punct['question_ratio'] > 0.001:
            desc.append("faz uso de perguntas retóricas")
        if punct['semicolon_ratio'] > 0.0005:
            desc.append("utiliza ponto e vírgula com frequência")
        
        # Padrões
        patterns = self.style_profile['writing_patterns']
        if patterns['uses_examples_ratio'] > 0.1:
            desc.append("frequentemente usa exemplos para ilustrar pontos")
        if patterns['uses_contrasts_ratio'] > 0.15:
            desc.append("constrói argumentos através de contrastes")
        
        # Palavras assinatura
        sig_words = self.style_profile['signature_words'][:10]
        if sig_words:
            desc.append(f"frequentemente usa palavras como: {', '.join(sig_words[:5])}")
        
        return "; ".join(desc) + "."