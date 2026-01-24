"""
Interface gráfica do Author Chatbot
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import threading
from src.chatbot import AuthorChatbot
from src.config import Config

class AuthorChatbotGUI:
    """Interface gráfica principal"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Author Chatbot")
        self.root.geometry("900x700")
        
        self.chatbot = None
        self.processed_books = Config.list_processed_books()
        self.dark_mode = False
        
        # Temas
        self.themes = {
            'light': {
                'bg': '#ffffff',
                'fg': '#000000',
                'chat_bg': '#f5f5f5',
                'input_bg': '#ffffff',
                'user_color': '#0066cc',
                'author_color': '#006600',
                'system_color': '#666666'
            },
            'dark': {
                'bg': '#1e1e1e',
                'fg': '#e0e0e0',
                'chat_bg': '#2d2d2d',
                'input_bg': '#3c3c3c',
                'user_color': '#4a9eff',
                'author_color': '#4caf50',
                'system_color': '#999999'
            }
        }
        
        self.apply_theme()
        
        # Verifica se tem livros processados
        if self.processed_books:
            self.show_main_interface()
        else:
            self.show_setup_interface()
    
    def apply_theme(self):
        """Aplica o tema atual"""
        theme = self.themes['dark' if self.dark_mode else 'light']
        
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configurações gerais
        self.root.configure(bg=theme['bg'])
        
        # Widgets
        style.configure('TFrame', background=theme['bg'])
        style.configure('TLabel', background=theme['bg'], foreground=theme['fg'])
        style.configure('TButton', background=theme['input_bg'], foreground=theme['fg'])
        style.configure('TCombobox', fieldbackground=theme['input_bg'], background=theme['input_bg'])
        
        # Salva tema atual para uso posterior
        self.current_theme = theme
    
    def toggle_dark_mode(self):
        """Alterna entre modo claro e escuro"""
        self.dark_mode = not self.dark_mode
        self.apply_theme()
        
        # Reaplica cores no chat se existir
        if hasattr(self, 'chat_display'):
            theme = self.current_theme
            self.chat_display.config(
                bg=theme['chat_bg'],
                fg=theme['fg'],
                insertbackground=theme['fg']
            )
            
            # Reconfigura tags
            self.chat_display.tag_config("user", foreground=theme['user_color'], font=("Arial", 10, "bold"))
            self.chat_display.tag_config("author", foreground=theme['author_color'], font=("Arial", 10))
            self.chat_display.tag_config("system", foreground=theme['system_color'], font=("Arial", 9, "italic"))
        
        # Reaplica no status text se existir
        if hasattr(self, 'status_text'):
            self.status_text.config(
                bg=theme['chat_bg'],
                fg=theme['fg']
            )
    
    def show_setup_interface(self):
        """Tela de configuração inicial"""
        # Limpa tela
        for widget in self.root.winfo_children():
            widget.destroy()
        
        setup_frame = ttk.Frame(self.root, padding="20")
        setup_frame.pack(fill=tk.BOTH, expand=True)
        
        # Botão de modo escuro no canto
        theme_btn = ttk.Button(
            setup_frame, 
            text="🌙 Modo Escuro" if not self.dark_mode else "☀️ Modo Claro",
            command=self.toggle_dark_mode,
            width=15
        )
        theme_btn.pack(anchor=tk.NE, pady=5)
        
        # Título
        title = ttk.Label(
            setup_frame, 
            text="Bem-vindo ao Author Chatbot", 
            font=("Arial", 16, "bold")
        )
        title.pack(pady=20)
        
        subtitle = ttk.Label(
            setup_frame,
            text="Configure seu primeiro livro para começar",
            font=("Arial", 10)
        )
        subtitle.pack(pady=5)
        
        # Frame de inputs
        input_frame = ttk.LabelFrame(setup_frame, text="Dados do Livro", padding="15")
        input_frame.pack(pady=20, fill=tk.X)
        
        # Campo de arquivo
        ttk.Label(input_frame, text="Arquivo do Livro (TXT):").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.file_path_var = tk.StringVar()
        file_entry = ttk.Entry(input_frame, textvariable=self.file_path_var, width=40)
        file_entry.grid(row=0, column=1, padx=5, pady=5)
        
        browse_btn = ttk.Button(input_frame, text="Selecionar", command=self.browse_file)
        browse_btn.grid(row=0, column=2, padx=5, pady=5)
        
        # Nome do autor
        ttk.Label(input_frame, text="Nome do Autor:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.author_var = tk.StringVar()
        ttk.Entry(input_frame, textvariable=self.author_var, width=40).grid(row=1, column=1, padx=5, pady=5)
        
        # Título do livro
        ttk.Label(input_frame, text="Título do Livro:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.title_var = tk.StringVar()
        ttk.Entry(input_frame, textvariable=self.title_var, width=40).grid(row=2, column=1, padx=5, pady=5)
        
        # Botão processar
        process_btn = ttk.Button(
            setup_frame, 
            text="Processar Livro", 
            command=self.process_new_book
        )
        process_btn.pack(pady=20)
        
        # Área de status
        self.status_text = scrolledtext.ScrolledText(
            setup_frame, 
            height=10, 
            state=tk.DISABLED,
            bg=self.current_theme['chat_bg'],
            fg=self.current_theme['fg']
        )
        self.status_text.pack(fill=tk.BOTH, expand=True, pady=10)
    
    def show_main_interface(self):
        """Interface principal do chat"""
        # Limpa a janela
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Frame superior (controles)
        top_frame = ttk.Frame(self.root, padding="10")
        top_frame.pack(fill=tk.X)
        
        # Seleção de livro
        ttk.Label(top_frame, text="Livro:").pack(side=tk.LEFT, padx=5)
        self.book_var = tk.StringVar()
        book_combo = ttk.Combobox(
            top_frame, 
            textvariable=self.book_var, 
            values=self.processed_books,
            state="readonly",
            width=30
        )
        book_combo.pack(side=tk.LEFT, padx=5)
        if self.processed_books:
            book_combo.current(0)
        book_combo.bind("<<ComboboxSelected>>", self.load_selected_book)
        
        # Perfil de resposta
        ttk.Label(top_frame, text="Perfil:").pack(side=tk.LEFT, padx=5)
        self.profile_var = tk.StringVar(value="normal")
        profile_combo = ttk.Combobox(
            top_frame,
            textvariable=self.profile_var,
            values=list(Config.RESPONSE_PROFILES.keys()),
            state="readonly",
            width=15
        )
        profile_combo.pack(side=tk.LEFT, padx=5)
        profile_combo.bind("<<ComboboxSelected>>", self.change_profile)
        
        # Botão modo escuro
        theme_btn = ttk.Button(
            top_frame,
            text="🌙" if not self.dark_mode else "☀️",
            command=self.toggle_dark_mode,
            width=3
        )
        theme_btn.pack(side=tk.RIGHT, padx=5)
        
        # Botão novo livro
        new_book_btn = ttk.Button(top_frame, text="Novo Livro", command=self.show_setup_interface)
        new_book_btn.pack(side=tk.RIGHT, padx=5)
        
        # Área de chat
        chat_frame = ttk.Frame(self.root)
        chat_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.chat_display = scrolledtext.ScrolledText(
            chat_frame,
            wrap=tk.WORD,
            font=("Arial", 10),
            state=tk.DISABLED,
            bg=self.current_theme['chat_bg'],
            fg=self.current_theme['fg'],
            insertbackground=self.current_theme['fg']
        )
        self.chat_display.pack(fill=tk.BOTH, expand=True)
        
        # Tags para formatação
        self.chat_display.tag_config("user", foreground=self.current_theme['user_color'], font=("Arial", 10, "bold"))
        self.chat_display.tag_config("author", foreground=self.current_theme['author_color'], font=("Arial", 10))
        self.chat_display.tag_config("system", foreground=self.current_theme['system_color'], font=("Arial", 9, "italic"))
        
        # Frame de input
        input_frame = ttk.Frame(self.root, padding="10")
        input_frame.pack(fill=tk.X)
        
        self.message_var = tk.StringVar()
        message_entry = ttk.Entry(input_frame, textvariable=self.message_var, font=("Arial", 10))
        message_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        message_entry.bind("<Return>", lambda e: self.send_message())
        
        send_btn = ttk.Button(input_frame, text="Enviar", command=self.send_message)
        send_btn.pack(side=tk.RIGHT)
        
        # Carrega primeiro livro
        self.load_selected_book()
    
    def browse_file(self):
        """Abre diálogo para selecionar arquivo"""
        filename = filedialog.askopenfilename(
            title="Selecione o livro",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if filename:
            self.file_path_var.set(filename)
    
    def log_status(self, message):
        """Adiciona mensagem ao log de status"""
        self.status_text.config(state=tk.NORMAL)
        self.status_text.insert(tk.END, message + "\n")
        self.status_text.see(tk.END)
        self.status_text.config(state=tk.DISABLED)
        self.root.update()
    
    def process_new_book(self):
        """Processa novo livro em thread separada"""
        file_path = self.file_path_var.get()
        author = self.author_var.get()
        title = self.title_var.get()
        
        if not all([file_path, author, title]):
            messagebox.showerror("Erro", "Preencha todos os campos")
            return
        
        def process():
            try:
                self.log_status("Iniciando processamento...")
                
                chatbot = AuthorChatbot()
                stats = chatbot.process_book(file_path, author, title)
                
                self.log_status(f"Estatísticas:")
                self.log_status(f"  - Caracteres: {stats['total_characters']}")
                self.log_status(f"  - Palavras: {stats['total_words']}")
                self.log_status(f"  - Chunks criados: {stats['actual_chunks']}")
                
                book_id = title.lower().replace(' ', '_')
                save_path = Config.get_processed_file_path(book_id)
                chatbot.save_knowledge_base(save_path)
                
                self.log_status(f"\nLivro processado com sucesso!")
                self.log_status(f"Salvo em: {save_path}")
                
                self.processed_books.append(book_id)
                
                messagebox.showinfo("Sucesso", "Livro processado! Abrindo interface de chat...")
                self.show_main_interface()
                
            except Exception as e:
                self.log_status(f"\nERRO: {str(e)}")
                messagebox.showerror("Erro", f"Erro ao processar: {str(e)}")
        
        thread = threading.Thread(target=process, daemon=True)
        thread.start()
    
    def load_selected_book(self, event=None):
        """Carrega livro selecionado"""
        book_id = self.book_var.get()
        if not book_id:
            return
        
        try:
            file_path = Config.get_processed_file_path(book_id)
            self.chatbot = AuthorChatbot(response_profile=self.profile_var.get())
            self.chatbot.load_knowledge_base(file_path)
            
            info = self.chatbot.get_info()
            self.add_system_message(
                f"Carregado: {info['book']} por {info['author']} "
                f"({info['chunks']} chunks)"
            )
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar livro: {str(e)}")
    
    def change_profile(self, event=None):
        """Muda perfil de resposta"""
        if self.chatbot:
            self.chatbot.set_response_profile(self.profile_var.get())
            self.add_system_message(f"Perfil alterado para: {self.profile_var.get()}")
    
    def send_message(self):
        """Envia mensagem para o chatbot"""
        message = self.message_var.get().strip()
        if not message or not self.chatbot:
            return
        
        self.message_var.set("")
        
        # Mostra mensagem do usuário
        self.add_message("Você", message, "user")
        
        # Processa em thread separada
        def get_response():
            try:
                response = self.chatbot.chat(message)
                info = self.chatbot.get_info()
                self.add_message(info['author'], response, "author")
            except Exception as e:
                self.add_system_message(f"Erro: {str(e)}")
        
        thread = threading.Thread(target=get_response, daemon=True)
        thread.start()
    
    def add_message(self, sender, message, tag):
        """Adiciona mensagem ao chat"""
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.insert(tk.END, f"{sender}: ", tag)
        self.chat_display.insert(tk.END, f"{message}\n\n")
        self.chat_display.see(tk.END)
        self.chat_display.config(state=tk.DISABLED)
    
    def add_system_message(self, message):
        """Adiciona mensagem do sistema"""
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.insert(tk.END, f"[Sistema] {message}\n\n", "system")
        self.chat_display.see(tk.END)
        self.chat_display.config(state=tk.DISABLED)
    
    def run(self):
        """Inicia a interface"""
        Config.validate()
        self.root.mainloop()