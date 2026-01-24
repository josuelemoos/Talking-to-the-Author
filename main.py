"""
Author Chatbot - Ponto de entrada principal
"""

import sys
from ui.interface import AuthorChatbotGUI

def main():
    """Função principal"""
    try:
        app = AuthorChatbotGUI()
        app.run()
    except KeyboardInterrupt:
        print("\nAplicação encerrada pelo usuário")
        sys.exit(0)
    except Exception as e:
        print(f"Erro fatal: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()