"""
Talking to the Author - Ponto de entrada principal
"""

import warnings
warnings.filterwarnings('ignore', category=FutureWarning)

import sys
from ui.interface import AuthorChatbotGUI

def main():
    """Função principal"""
    try:
        print("Iniciando aplicação...")
        app = AuthorChatbotGUI()
        print("Interface criada, iniciando loop...")
        app.run()
    except KeyboardInterrupt:
        print("\nAplicação encerrada pelo usuário")
        sys.exit(0)
    except Exception as e:
        print(f"Erro fatal: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()