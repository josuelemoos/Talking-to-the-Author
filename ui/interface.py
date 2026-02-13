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
        print("Criando janela principal...")
        self.app = ctk.CTk()
        self.app.title("Talking to the Author")
        self.app.geometry("1100x750")
        
        print("Inicializando variáveis...")
        self.chatbot = None
        self.processed_books = Config.list_processed_books()
        self.loading_animation_running = False
        self.loading_frame = 0
        
        # Preferências
        self.font_size = 15
        self.appearance_mode = "dark"
        
        # Aplica tema inicial
        ctk.set_appearance_mode(self.appearance_mode)
        
        print("Verificando disclaimer...")
        # Mostra disclaimer na primeira vez
        self.show_disclaimer_if_needed()
        
        print(f"Livros processados: {self.processed_books}")
        # Verifica se tem livros processados
        if self.processed_books:
            print("Mostrando interface principal...")
            self.show_main_interface()
        else:
            print("Mostrando interface de setup...")
            self.show_setup_interface()
        
        print("Interface pronta!")
    
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
            text="Talking to the Author",
            font=ctk.CTkFont(size=38, weight="bold")
        )
        title.pack(side="left")
        
        # Botão de preferências
        pref_btn = ctk.CTkButton(
            header,
            text="⚙️",
            command=self.show_preferences,
            width=40,
            height=40,
            corner_radius=10,
            font=ctk.CTkFont(size=18),
            fg_color="transparent",
            hover_color=("gray70", "gray30")
        )
        pref_btn.pack(side="right")
        
        # Subtítulo
        subtitle = ctk.CTkLabel(
            main_container,
            text="Configure seu primeiro livro para começar",
            font=ctk.CTkFont(size=15),
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
            text="Arquivo do Livro (TXT ou PDF)",
            font=ctk.CTkFont(size=15, weight="bold"),
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
            font=ctk.CTkFont(size=15)
        )
        self.file_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        browse_btn = ctk.CTkButton(
            file_frame,
            text="Selecionar",
            command=self.browse_file,
            width=120,
            height=45,
            corner_radius=10,
            font=ctk.CTkFont(size=15)
        )
        browse_btn.pack(side="right")
        
        # Campo: Nome do Autor
        author_label = ctk.CTkLabel(
            form_content,
            text="Nome do Autor",
            font=ctk.CTkFont(size=15, weight="bold"),
            anchor="w"
        )
        author_label.pack(fill="x", pady=(0, 8))
        
        self.author_var = ctk.StringVar()
        author_entry = ctk.CTkEntry(
            form_content,
            textvariable=self.author_var,
            height=45,
            corner_radius=10,
            font=ctk.CTkFont(size=15)
        )
        author_entry.pack(fill="x", pady=(0, 20))
        
        # Campo: Título do Livro
        title_label = ctk.CTkLabel(
            form_content,
            text="Título do Livro",
            font=ctk.CTkFont(size=15, weight="bold"),
            anchor="w"
        )
        title_label.pack(fill="x", pady=(0, 8))
        
        self.title_var = ctk.StringVar()
        title_entry = ctk.CTkEntry(
            form_content,
            textvariable=self.title_var,
            height=45,
            corner_radius=10,
            font=ctk.CTkFont(size=15)
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
            font=ctk.CTkFont(size=15, weight="bold"),
            anchor="w"
        )
        status_label.pack(fill="x", pady=(30, 8))
        
        self.status_text = ctk.CTkTextbox(
            main_container,
            height=150,
            corner_radius=10,
            font=ctk.CTkFont(family="Consolas", size=13),
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
            text="💬 Talking to the Author",
            font=ctk.CTkFont(size=22, weight="bold")
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
            font=ctk.CTkFont(size=self.font_size),
            wrap="word",
            fg_color="transparent"
        )
        self.chat_display.pack(fill="both", expand=True, padx=15, pady=15)
        
        # Configurar tags (sem font, usa o padrão do textbox)
        self.chat_display.tag_config("user", foreground="#3b82f6")
        self.chat_display.tag_config("author", foreground="#10b981")
        self.chat_display.tag_config("system", foreground="#6b7280")
        self.chat_display.tag_config("loading", foreground="#6b7280")
        
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
            font=ctk.CTkFont(size=15),
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
            font=ctk.CTkFont(size=15, weight="bold"),
            fg_color="#2563eb",
            hover_color="#1d4ed8"
        )
        send_btn.pack(side="right")
        
        # Carrega primeiro livro
        self.load_selected_book()
    
    def show_disclaimer_if_needed(self):
        """Mostra disclaimer na primeira vez que abre o app"""
        import os
        disclaimer_file = os.path.join(Config.DATA_DIR, '.disclaimer_shown')
        
        # Se já foi mostrado, apenas retorna
        if os.path.exists(disclaimer_file):
            print("Disclaimer já foi aceito anteriormente")
            return
        
        print("Mostrando disclaimer pela primeira vez...")
        self.disclaimer_accepted = False
        
        # Cria janela de disclaimer
        disclaimer_window = ctk.CTkToplevel(self.app)
        disclaimer_window.title("Aviso Importante")
        disclaimer_window.geometry("600x500")
        disclaimer_window.resizable(False, False)
        
        # Bloqueia interação com janela principal
        disclaimer_window.transient(self.app)
        disclaimer_window.grab_set()
        
        # Centraliza
        disclaimer_window.update_idletasks()
        x = (disclaimer_window.winfo_screenwidth() // 2) - (600 // 2)
        y = (disclaimer_window.winfo_screenheight() // 2) - (500 // 2)
        disclaimer_window.geometry(f"600x500+{x}+{y}")
        
        # Impede fechar com X
        disclaimer_window.protocol("WM_DELETE_WINDOW", lambda: None)
        
        # Container
        container = ctk.CTkFrame(disclaimer_window, fg_color="transparent")
        container.pack(fill="both", expand=True, padx=30, pady=30)
        
        # Ícone e título
        title_frame = ctk.CTkFrame(container, fg_color="transparent")
        title_frame.pack(fill="x", pady=(0, 20))
        
        ctk.CTkLabel(
            title_frame,
            text="⚠️",
            font=ctk.CTkFont(size=48)
        ).pack()
        
        ctk.CTkLabel(
            title_frame,
            text="Aviso Importante",
            font=ctk.CTkFont(size=28, weight="bold")
        ).pack(pady=(10, 0))
        
        # Card com disclaimer
        disclaimer_card = ctk.CTkFrame(container)
        disclaimer_card.pack(fill="both", expand=True, pady=(0, 20))
        
        disclaimer_text = ctk.CTkTextbox(
            disclaimer_card,
            wrap="word",
            font=ctk.CTkFont(size=14),
            fg_color="transparent"
        )
        disclaimer_text.pack(fill="both", expand=True, padx=20, pady=20)
        
        disclaimer_content = """Este aplicativo utiliza Inteligência Artificial para simular conversas baseadas em obras literárias.

IMPORTANTE:

• As respostas são SIMULAÇÕES geradas por IA baseadas no conteúdo do livro fornecido.

• NÃO representam as opiniões, pensamentos ou declarações reais do autor.

• O autor original NÃO está envolvido neste processo e não endossa as respostas geradas.

• As respostas podem conter imprecisões, interpretações incorretas ou informações que não refletem fielmente o pensamento do autor.

• Este aplicativo é uma ferramenta educacional e de entretenimento, não uma fonte autoritativa sobre o autor ou sua obra.

• Use com senso crítico e sempre consulte as obras originais para compreensão autêntica do pensamento do autor.

Ao continuar, você reconhece e aceita estas limitações."""
        
        disclaimer_text.insert("1.0", disclaimer_content)
        disclaimer_text.configure(state="disabled")
        
        # Checkbox de concordância
        agree_var = ctk.BooleanVar(value=False)
        
        agree_frame = ctk.CTkFrame(container, fg_color="transparent")
        agree_frame.pack(fill="x", pady=(0, 15))
        
        agree_check = ctk.CTkCheckBox(
            agree_frame,
            text="Li e compreendo o aviso acima",
            variable=agree_var,
            font=ctk.CTkFont(size=14),
            checkbox_width=24,
            checkbox_height=24
        )
        agree_check.pack()
        
        # Funções dos botões
        def close_disclaimer():
            if agree_var.get():
                print("Usuário aceitou o disclaimer")
                # Marca como visto
                os.makedirs(Config.DATA_DIR, exist_ok=True)
                with open(disclaimer_file, 'w') as f:
                    f.write('shown')
                self.disclaimer_accepted = True
                disclaimer_window.destroy()
            else:
                from tkinter import messagebox
                messagebox.showwarning(
                    "Atenção",
                    "Você precisa ler e concordar com o aviso para continuar."
                )
        
        def exit_app():
            print("Usuário recusou o disclaimer, fechando...")
            disclaimer_window.destroy()
            self.app.quit()
            import sys
            sys.exit(0)
        
        # Botões
        buttons_frame = ctk.CTkFrame(container, fg_color="transparent")
        buttons_frame.pack(fill="x")
        
        cancel_btn = ctk.CTkButton(
            buttons_frame,
            text="Sair",
            command=exit_app,
            height=50,
            font=ctk.CTkFont(size=16),
            fg_color="transparent",
            border_width=2,
            border_color=("gray60", "gray40"),
            hover_color=("gray80", "gray20")
        )
        cancel_btn.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        continue_btn = ctk.CTkButton(
            buttons_frame,
            text="Continuar",
            command=close_disclaimer,
            height=50,
            font=ctk.CTkFont(size=16, weight="bold"),
            fg_color=("#2563eb", "#1d4ed8"),
            hover_color=("#1d4ed8", "#1e40af")
        )
        continue_btn.pack(side="right", fill="x", expand=True, padx=(10, 0))
        
        # Aguarda fechamento
        print("Aguardando resposta do usuário...")
        self.app.wait_window(disclaimer_window)
        
        # Se não aceitou, fecha o app
        if not self.disclaimer_accepted:
            print("Disclaimer não foi aceito, encerrando...")
            self.app.quit()
            import sys
            sys.exit(0)
        
        print("Disclaimer aceito, continuando...")
    
    def start_loading_animation(self):
        """Inicia animação de loading estilo spinner"""
        if not hasattr(self, 'chat_display'):
            return
            
        self.loading_animation_running = True
        self.loading_frame = 0
        
        # Adiciona linha para o loading
        self.chat_display.configure(state="normal")
        self.loading_line_start = self.chat_display.index("end-1c linestart")
        self.chat_display.insert("end", "\n")
        self.chat_display.configure(state="disabled")
        
        self.animate_loading()
    
    def animate_loading(self):
        """Anima spinner circular"""
        if not self.loading_animation_running:
            return
        
        if not hasattr(self, 'chat_display'):
            return
        
        # Spinner circular suave
        frames = ["⣾", "⣽", "⣻", "⢿", "⡿", "⣟", "⣯", "⣷"]
        
        loading_text = f"  {frames[self.loading_frame]}  "
        self.loading_frame = (self.loading_frame + 1) % len(frames)
        
        try:
            self.chat_display.configure(state="normal")
            
            # Deleta a linha inteira do loading
            self.chat_display.delete(self.loading_line_start, f"{self.loading_line_start} lineend")
            
            # Insere novo frame
            self.chat_display.insert(self.loading_line_start, loading_text, "loading")
            
            self.chat_display.see("end")
            self.chat_display.configure(state="disabled")
            
            # Continua animação (80ms para ficar bem suave)
            self.app.after(80, self.animate_loading)
        except:
            pass
    
    def stop_loading_animation(self):
        """Para animação de loading"""
        self.loading_animation_running = False
        if not hasattr(self, 'chat_display'):
            return
        try:
            self.chat_display.configure(state="normal")
            # Remove a linha completa do loading
            self.chat_display.delete(self.loading_line_start, f"{self.loading_line_start} lineend+1c")
            self.chat_display.configure(state="disabled")
        except:
            pass
    
        """Inicia animação de loading estilo spinner"""
        self.loading_animation_running = True
        self.loading_frame = 0
        
        # Adiciona linha para o loading
        self.chat_display.configure(state="normal")
        self.loading_line_start = self.chat_display.index("end-1c linestart")
        self.chat_display.insert("end", "\n")
        self.chat_display.configure(state="disabled")
        
        self.animate_loading()
    
    def animate_loading(self):
        """Anima spinner circular"""
        if not self.loading_animation_running:
            return
        
        # Spinner circular suave
        frames = ["⣾", "⣽", "⣻", "⢿", "⡿", "⣟", "⣯", "⣷"]
        
        loading_text = f"  {frames[self.loading_frame]}  "
        self.loading_frame = (self.loading_frame + 1) % len(frames)
        
        try:
            self.chat_display.configure(state="normal")
            
            # Deleta a linha inteira do loading
            self.chat_display.delete(self.loading_line_start, f"{self.loading_line_start} lineend")
            
            # Insere novo frame
            self.chat_display.insert(self.loading_line_start, loading_text, "loading")
            
            self.chat_display.see("end")
            self.chat_display.configure(state="disabled")
            
            # Continua animação (80ms para ficar bem suave)
            self.app.after(80, self.animate_loading)
        except:
            pass
    
    def stop_loading_animation(self):
        """Para animação de loading"""
        self.loading_animation_running = False
        try:
            self.chat_display.configure(state="normal")
            # Remove a linha completa do loading
            self.chat_display.delete(self.loading_line_start, f"{self.loading_line_start} lineend+1c")
            self.chat_display.configure(state="disabled")
        except:
            pass
    
    def toggle_theme(self):
        """Alterna entre modo claro e escuro"""
        if self.appearance_mode == "dark":
            self.appearance_mode = "light"
            ctk.set_appearance_mode("light")
        else:
            self.appearance_mode = "dark"
            ctk.set_appearance_mode("dark")
    
    def show_preferences(self):
        """Mostra janela de preferências"""
        pref_window = ctk.CTkToplevel(self.app)
        pref_window.title("Preferências")
        pref_window.geometry("500x400")
        pref_window.resizable(False, False)
        
        # Centraliza a janela
        pref_window.update_idletasks()
        x = (pref_window.winfo_screenwidth() // 2) - (500 // 2)
        y = (pref_window.winfo_screenheight() // 2) - (400 // 2)
        pref_window.geometry(f"500x400+{x}+{y}")
        
        # Container
        container = ctk.CTkFrame(pref_window, fg_color="transparent")
        container.pack(fill="both", expand=True, padx=30, pady=30)
        
        # Título
        title = ctk.CTkLabel(
            container,
            text="⚙️ Preferências",
            font=ctk.CTkFont(size=28, weight="bold")
        )
        title.pack(pady=(0, 30))
        
        # Card de Aparência
        appearance_card = ctk.CTkFrame(container)
        appearance_card.pack(fill="x", pady=(0, 15))
        
        appearance_content = ctk.CTkFrame(appearance_card, fg_color="transparent")
        appearance_content.pack(fill="both", padx=20, pady=20)
        
        ctk.CTkLabel(
            appearance_content,
            text="Tema",
            font=ctk.CTkFont(size=16, weight="bold"),
            anchor="w"
        ).pack(fill="x", pady=(0, 10))
        
        theme_var = ctk.StringVar(value=self.appearance_mode)
        theme_menu = ctk.CTkSegmentedButton(
            appearance_content,
            values=["light", "dark"],
            variable=theme_var,
            command=self.change_theme_from_prefs,
            height=40,
            font=ctk.CTkFont(size=14)
        )
        theme_menu.pack(fill="x")
        
        # Card de Texto
        text_card = ctk.CTkFrame(container)
        text_card.pack(fill="x", pady=(0, 20))
        
        text_content = ctk.CTkFrame(text_card, fg_color="transparent")
        text_content.pack(fill="both", padx=20, pady=20)
        
        ctk.CTkLabel(
            text_content,
            text="Tamanho da Fonte",
            font=ctk.CTkFont(size=16, weight="bold"),
            anchor="w"
        ).pack(fill="x", pady=(0, 10))
        
        # Preview do tamanho
        font_preview_frame = ctk.CTkFrame(text_content, fg_color="transparent")
        font_preview_frame.pack(fill="x", pady=(0, 10))
        
        ctk.CTkLabel(
            font_preview_frame,
            text="Atual:",
            font=ctk.CTkFont(size=13)
        ).pack(side="left")
        
        self.font_size_display = ctk.CTkLabel(
            font_preview_frame,
            text=f"{self.font_size}px",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color=("#2563eb", "#3b82f6")
        )
        self.font_size_display.pack(side="left", padx=(5, 0))
        
        # Slider
        font_slider = ctk.CTkSlider(
            text_content,
            from_=12,
            to=22,
            number_of_steps=10,
            command=self.change_font_size,
            height=20
        )
        font_slider.set(self.font_size)
        font_slider.pack(fill="x", pady=(0, 5))
        
        # Labels do slider
        slider_labels = ctk.CTkFrame(text_content, fg_color="transparent")
        slider_labels.pack(fill="x")
        
        ctk.CTkLabel(
            slider_labels,
            text="Pequeno",
            font=ctk.CTkFont(size=11),
            text_color="gray"
        ).pack(side="left")
        
        ctk.CTkLabel(
            slider_labels,
            text="Grande",
            font=ctk.CTkFont(size=11),
            text_color="gray"
        ).pack(side="right")
        
        # Botão fechar
        close_btn = ctk.CTkButton(
            container,
            text="Fechar",
            command=pref_window.destroy,
            height=45,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color=("#2563eb", "#1d4ed8"),
            hover_color=("#1d4ed8", "#1e40af")
        )
        close_btn.pack(fill="x", pady=(10, 0))
    
    def change_theme_from_prefs(self, value):
        """Muda tema a partir das preferências"""
        self.appearance_mode = value
        ctk.set_appearance_mode(value)
    
    def change_font_size(self, value):
        """Muda tamanho da fonte"""
        self.font_size = int(value)
        
        # Atualiza display na janela de preferências
        if hasattr(self, 'font_size_display'):
            self.font_size_display.configure(text=f"{self.font_size}px")
        
        # Atualiza fonte do chat se existir
        if hasattr(self, 'chat_display'):
            self.chat_display.configure(font=ctk.CTkFont(size=self.font_size))
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
            filetypes=[
                ("Arquivos suportados", "*.txt *.pdf"),
                ("Text files", "*.txt"),
                ("PDF files", "*.pdf"),
                ("All files", "*.*")
            ]
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
        
        # Inicia animação de loading
        self.start_loading_animation()
        
        # Processa em thread separada
        def get_response():
            try:
                response = self.chatbot.chat(message)
                info = self.chatbot.get_info()
                
                # Para animação e mostra resposta
                self.app.after(0, self.stop_loading_animation)
                self.app.after(50, lambda: self.add_message(info['author'], response, "author"))
            except Exception as e:
                error_msg = str(e)
                self.app.after(0, self.stop_loading_animation)
                self.app.after(50, lambda: self.add_system_message(f"Erro: {error_msg}"))
        
        thread = threading.Thread(target=get_response, daemon=True)
        thread.start()
    
    def add_message(self, sender, message, tag):
        """Adiciona mensagem ao chat"""
        self.chat_display.configure(state="normal")
        
        if tag == "user":
            # Mensagem do usuário aparece instantaneamente
            self.chat_display.insert("end", f"{sender}: ", tag)
            self.chat_display.insert("end", f"{message}\n\n")
            self.chat_display.see("end")
            self.chat_display.configure(state="disabled")
        else:
            # Mensagem do autor usa efeito typewriter
            self.chat_display.insert("end", f"{sender}: ", tag)
            self.chat_display.configure(state="disabled")
            self.typewriter_effect(message, tag)
    
    def typewriter_effect(self, text, tag, index=0):
        """Efeito de digitação (typewriter)"""
        if not hasattr(self, 'chat_display'):
            return
            
        if index < len(text):
            # Adiciona próximo caractere
            self.chat_display.configure(state="normal")
            self.chat_display.insert("end", text[index])
            self.chat_display.see("end")
            self.chat_display.configure(state="disabled")
            
            # Velocidade variável para parecer mais natural
            # Mais rápido em espaços, mais lento em pontuação
            if text[index] in ['.', '!', '?', ':']:
                delay = 100  # Pausa em pontuação
            elif text[index] in [',', ';']:
                delay = 50
            elif text[index] == ' ':
                delay = 15
            elif text[index] == '\n':
                delay = 30
            else:
                delay = 20  # Velocidade normal
            
            # Continua digitando
            self.app.after(delay, lambda: self.typewriter_effect(text, tag, index + 1))
        else:
            # Terminou de digitar, adiciona quebra de linha
            self.chat_display.configure(state="normal")
            self.chat_display.insert("end", "\n\n")
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