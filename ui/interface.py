"""
Interface gráfica do Author Chatbot - CustomTkinter
"""

import customtkinter as ctk
from tkinter import filedialog, messagebox
import threading
from src.chatbot import AuthorChatbot
from src.config import Config

# Configurações do CustomTkinter
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class AuthorChatbotGUI:
    """Interface gráfica principal - CustomTkinter"""
    
    def __init__(self):
        self.app = ctk.CTk()
        self.app.title("Author Chatbot")
        self.app.geometry("1100x750")
        
        self.chatbot = None
        self.processed_books = Config.list_processed_books()
        
        # Verifica se tem livros processados
        if self.processed_books:
            self.show_main_interface()
        else:
            self.show_setup_interface()
    
    def show_setup_interface(self):
        """Tela de configuração inicial"""
        # Limpa tela
        for widget in self.app.winfo_children():
            widget.destroy()
        
        # Container principal
        main_container = ctk.CTkFrame(self.app, fg_color="transparent")
        main_container.pack(fill="both", expand=True, padx=40, pady=40)
        
        # Header
        header = ctk.CTkFrame(main_container, fg_color="transparent")
        header.pack(fill="x", pady=(0, 30))
        
        title = ctk.CTkLabel(
            header,
            text="Author Chatbot",
            font=ctk.CTkFont(size=36, weight="bold")
        )
        title.pack(side="left")
        
        # Botão de tema
        self.theme_btn = ctk.CTkButton(
            header,
            text="☀️ Modo Claro",
            command=self.toggle_theme,
            width=140,
            height=40,
            corner_radius=10,
            font=ctk.CTkFont(size=13)
        )
        self.theme_btn.pack(side="right")
        
        # Subtítulo
        subtitle = ctk.CTkLabel(
            main_container,
            text="Configure seu primeiro livro para começar",
            font=ctk.CTkFont(size=14),
            text_color="gray"
        )
        subtitle.pack(pady=(0, 40))
        
        # Card de formulário
        form_card = ctk.CTkFrame(main_container, corner_radius=15)
        form_card.pack(fill="both", expand=True)
        
        # Padding interno
        form_content = ctk.CTkFrame(form_card, fg_color="transparent")
        form_content.pack(fill="both", expand=True, padx=30, pady=30)
        
        # Campo: Arquivo
        file_label = ctk.CTkLabel(
            form_content,
            text="Arquivo do Livro (TXT)",
            font=ctk.CTkFont(size=13, weight="bold"),
            anchor="w"
        )
        file_label.pack(fill="x", pady=(0, 8))
        
        file_frame = ctk.CTkFrame(form_content, fg_color="transparent")
        file_frame.pack(fill="x", pady=(0, 20))
        
        self.file_path_var = ctk.StringVar()
        self.file_entry = ctk.CTkEntry(
            file_frame,
            textvariable=self.file_path_var,
            height=45,
            corner_radius=10,
            font=ctk.CTkFont(size=13)
        )
        self.file_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        browse_btn = ctk.CTkButton(
            file_frame,
            text="Selecionar",
            command=self.browse_file,
            width=120,
            height=45,
            corner_radius=10,
            font=ctk.CTkFont(size=13)
        )
        browse_btn.pack(side="right")
        
        # Campo: Nome do Autor
        author_label = ctk.CTkLabel(
            form_content,
            text="Nome do Autor",
            font=ctk.CTkFont(size=13, weight="bold"),
            anchor="w"
        )
        author_label.pack(fill="x", pady=(0, 8))
        
        self.author_var = ctk.StringVar()
        author_entry = ctk.CTkEntry(
            form_content,
            textvariable=self.author_var,
            height=45,
            corner_radius=10,
            font=ctk.CTkFont(size=13)
        )
        author_entry.pack(fill="x", pady=(0, 20))
        
        # Campo: Título do Livro
        title_label = ctk.CTkLabel(
            form_content,
            text="Título do Livro",
            font=ctk.CTkFont(size=13, weight="bold"),
            anchor="w"
        )
        title_label.pack(fill="x", pady=(0, 8))
        
        self.title_var = ctk.StringVar()
        title_entry = ctk.CTkEntry(
            form_content,
            textvariable=self.title_var,
            height=45,
            corner_radius=10,
            font=ctk.CTkFont(size=13)
        )
        title_entry.pack(fill="x", pady=(0, 30))
        
        # Botão processar
        process_btn = ctk.CTkButton(
            form_content,
            text="Processar Livro",
            command=self.process_new_book,
            height=50,
            corner_radius=10,
            font=ctk.CTkFont(size=15, weight="bold"),
            fg_color="#2563eb",
            hover_color="#1d4ed8"
        )
        process_btn.pack(fill="x")
        
        # Área de status
        status_label = ctk.CTkLabel(
            main_container,
            text="Status do Processamento",
            font=ctk.CTkFont(size=13, weight="bold"),
            anchor="w"
        )
        status_label.pack(fill="x", pady=(30, 8))
        
        self.status_text = ctk.CTkTextbox(
            main_container,
            height=150,
            corner_radius=10,
            font=ctk.CTkFont(family="Consolas", size=11),
            wrap="word"
        )
        self.status_text.pack(fill="both", expand=True)
        self.status_text.configure(state="disabled")
    
    def show_main_interface(self):
        """Interface principal do chat"""
        # Limpa tela
        for widget in self.app.winfo_children():
            widget.destroy()
        
        # Container principal
        main = ctk.CTkFrame(self.app, fg_color="transparent")
        main.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Header
        header = ctk.CTkFrame(main, corner_radius=15, height=80)
        header.pack(fill="x", pady=(0, 15))
        header.pack_propagate(False)
        
        header_content = ctk.CTkFrame(header, fg_color="transparent")
        header_content.pack(fill="both", expand=True, padx=20, pady=15)
        
        # Título
        title = ctk.CTkLabel(
            header_content,
            text="💬 Author Chatbot",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title.pack(side="left")
        
        # Controles
        controls = ctk.CTkFrame(header_content, fg_color="transparent")
        controls.pack(side="right")
        
        # Seleção de livro
        if self.processed_books:
            self.book_var = ctk.StringVar(value=self.processed_books[0])
            book_menu = ctk.CTkComboBox(
                controls,
                variable=self.book_var,
                values=self.processed_books,
                width=200,
                height=35,
                corner_radius=8,
                font=ctk.CTkFont(size=12),
                command=self.load_selected_book
            )
            book_menu.pack(side="left", padx=5)
        
        # Perfil
        self.profile_var = ctk.StringVar(value="normal")
        profile_menu = ctk.CTkComboBox(
            controls,
            variable=self.profile_var,
            values=list(Config.RESPONSE_PROFILES.keys()),
            width=130,
            height=35,
            corner_radius=8,
            font=ctk.CTkFont(size=12),
            command=self.change_profile
        )
        profile_menu.pack(side="left", padx=5)
        
        # Botão novo livro
        new_btn = ctk.CTkButton(
            controls,
            text="+ Novo",
            command=self.show_setup_interface,
            width=90,
            height=35,
            corner_radius=8,
            font=ctk.CTkFont(size=12, weight="bold"),
            fg_color="#10b981",
            hover_color="#059669"
        )
        new_btn.pack(side="left", padx=5)
        
        # Botão tema
        self.theme_btn = ctk.CTkButton(
            controls,
            text="☀️",
            command=self.toggle_theme,
            width=40,
            height=35,
            corner_radius=8,
            font=ctk.CTkFont(size=16),
            fg_color="transparent",
            hover_color=("gray70", "gray30")
        )
        self.theme_btn.pack(side="left", padx=5)
        
        # Área de chat
        chat_card = ctk.CTkFrame(main, corner_radius=15)
        chat_card.pack(fill="both", expand=True, pady=(0, 15))
        
        self.chat_display = ctk.CTkTextbox(
            chat_card,
            corner_radius=0,
            font=ctk.CTkFont(size=13),
            wrap="word",
            fg_color="transparent"
        )
        self.chat_display.pack(fill="both", expand=True, padx=15, pady=15)
        
        # Configurar tags (sem font, usa o padrão do textbox)
        self.chat_display.tag_config("user", foreground="#3b82f6")
        self.chat_display.tag_config("author", foreground="#10b981")
        self.chat_display.tag_config("system", foreground="#6b7280")
        
        # Input area
        input_card = ctk.CTkFrame(main, corner_radius=15, height=70)
        input_card.pack(fill="x")
        input_card.pack_propagate(False)
        
        input_content = ctk.CTkFrame(input_card, fg_color="transparent")
        input_content.pack(fill="both", expand=True, padx=15, pady=15)
        
        self.message_var = ctk.StringVar()
        message_entry = ctk.CTkEntry(
            input_content,
            textvariable=self.message_var,
            height=40,
            corner_radius=10,
            font=ctk.CTkFont(size=13),
            placeholder_text="Digite sua mensagem..."
        )
        message_entry.pack(side="left", fill="both", expand=True, padx=(0, 10))
        message_entry.bind("<Return>", lambda e: self.send_message())
        
        send_btn = ctk.CTkButton(
            input_content,
            text="Enviar ➤",
            command=self.send_message,
            width=100,
            height=40,
            corner_radius=10,
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color="#2563eb",
            hover_color="#1d4ed8"
        )
        send_btn.pack(side="right")
        
        # Carrega primeiro livro
        self.load_selected_book()
    
    def toggle_theme(self):
        """Alterna entre modo claro e escuro"""
        current = ctk.get_appearance_mode()
        new_mode = "light" if current == "Dark" else "dark"
        ctk.set_appearance_mode(new_mode)
        
        # Atualiza texto do botão
        if hasattr(self, 'theme_btn'):
            if new_mode == "dark":
                self.theme_btn.configure(text="☀️ Modo Claro" if self.theme_btn.cget("text") != "☀️" else "☀️")
            else:
                self.theme_btn.configure(text="🌙 Modo Escuro" if self.theme_btn.cget("text") != "🌙" else "🌙")
    
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
        try:
            if hasattr(self, 'status_text') and self.status_text.winfo_exists():
                self.status_text.configure(state="normal")
                self.status_text.insert("end", str(message) + "\n")
                self.status_text.see("end")
                self.status_text.configure(state="disabled")
                self.app.update()
        except:
            pass
    
    def process_new_book(self):
        """Processa novo livro em thread separada"""
        file_path = self.file_path_var.get()
        author = self.author_var.get()
        title = self.title_var.get()
        
        if not all([file_path, author, title]):
            messagebox.showerror("Erro", "Preencha todos os campos")
            return
        
        # Desabilita botão durante processamento
        self.app.after(0, lambda: self.log_status("-> Iniciando processamento..."))
        
        def process():
            try:
                chatbot = AuthorChatbot()
                stats = chatbot.process_book(file_path, author, title)
                
                self.app.after(0, lambda: self.log_status(f"Caracteres: {stats['total_characters']:,}"))
                self.app.after(0, lambda: self.log_status(f"Palavras: {stats['total_words']:,}"))
                self.app.after(0, lambda: self.log_status(f"Chunks criados: {stats['actual_chunks']}"))
                
                book_id = title.lower().replace(' ', '_')
                save_path = Config.get_processed_file_path(book_id)
                chatbot.save_knowledge_base(save_path)
                
                self.app.after(0, lambda: self.log_status(""))
                self.app.after(0, lambda: self.log_status("Processamento concluido!"))
                
                self.processed_books.append(book_id)
                
                self.app.after(0, lambda: messagebox.showinfo("Sucesso", "Livro processado com sucesso!"))
                self.app.after(0, self.show_main_interface)
                
            except Exception as e:
                error_msg = str(e)
                self.app.after(0, lambda: self.log_status(""))
                self.app.after(0, lambda: self.log_status(f"ERRO: {error_msg}"))
                self.app.after(0, lambda: messagebox.showerror("Erro", f"Erro ao processar: {error_msg}"))
        
        thread = threading.Thread(target=process, daemon=True)
        thread.start()
    
    def load_selected_book(self, choice=None):
        """Carrega livro selecionado"""
        if not hasattr(self, 'book_var'):
            return
            
        book_id = self.book_var.get()
        if not book_id:
            return
        
        try:
            file_path = Config.get_processed_file_path(book_id)
            self.chatbot = AuthorChatbot(response_profile=self.profile_var.get())
            self.chatbot.load_knowledge_base(file_path)
            
            info = self.chatbot.get_info()
            self.add_system_message(
                f"Carregado: {info['book']} por {info['author']} ({info['chunks']} chunks)"
            )
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar livro: {str(e)}")
    
    def change_profile(self, choice):
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
                self.app.after(0, lambda: self.add_message(info['author'], response, "author"))
            except Exception as e:
                error_msg = str(e)
                self.app.after(0, lambda: self.add_system_message(f"Erro: {error_msg}"))
        
        thread = threading.Thread(target=get_response, daemon=True)
        thread.start()
    
    def add_message(self, sender, message, tag):
        """Adiciona mensagem ao chat"""
        self.chat_display.configure(state="normal")
        
        if tag == "user":
            self.chat_display.insert("end", f"{sender}: ", tag)
            self.chat_display.insert("end", f"{message}\n\n")
        else:
            self.chat_display.insert("end", f"{sender}: ", tag)
            self.chat_display.insert("end", f"{message}\n\n")
        
        self.chat_display.see("end")
        self.chat_display.configure(state="disabled")
    
    def add_system_message(self, message):
        """Adiciona mensagem do sistema"""
        self.chat_display.configure(state="normal")
        self.chat_display.insert("end", f"[Sistema] {message}\n\n", "system")
        self.chat_display.see("end")
        self.chat_display.configure(state="disabled")
    
    def run(self):
        """Inicia a interface"""
        Config.validate()
        self.app.mainloop()