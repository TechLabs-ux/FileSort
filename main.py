import tkinter as tk
from tkinter import ttk, messagebox
import os
import shutil
import time
from pathlib import Path

class FileSortApp:
    def __init__(self, root):
        self.root = root
        self.root.title("FileSort - File Organizer")
        self.root.geometry("520x480")
        self.root.resizable(False, False)
        self.root.configure(bg='#f0f0f0')
        
        # Configuração de estilo
        self.style = ttk.Style()
        self.style.configure('Start.TButton', 
                            font=('Arial', 11, 'bold'),
                            padding=(25, 8),
                            borderwidth=2,
                            relief="raised",
                            width=8)
        self.style.map('Start.TButton',
                     foreground=[('active', 'black'), ('disabled', 'gray')],
                     background=[('active', '#d9d9d9')])
        self.style.configure('TLabel', font=('Arial', 12), background='#f0f0f0')
        self.style.configure('Title.TLabel', font=('Arial', 20, 'bold'))
        self.style.configure('TProgressbar', thickness=20, background='#4a6baf')
        self.style.configure('Horizontal.TProgressbar', background='#4a6baf')
        
        self.create_widgets()
    
    def create_widgets(self):
        # Cabeçalho
        header_frame = tk.Frame(self.root, bg='#4a6baf')
        header_frame.pack(fill='x', pady=(0, 20))
        
        self.title_label = ttk.Label(
            header_frame, 
            text="FileSort", 
            style='Title.TLabel',
            foreground='white',
            background='#4a6baf'
        )
        self.title_label.pack(pady=15)
        
        # Corpo principal
        main_frame = tk.Frame(self.root, bg='#f0f0f0')
        main_frame.pack(pady=10, padx=25, fill='both', expand=True)
        
        # Descrição
        desc_label = ttk.Label(
            main_frame,
            text="Automatically organize your files by type, date or size",
            wraplength=400,
            justify='center'
        )
        desc_label.pack(pady=(0, 20))
        
        # Opções de organização
        options_frame = tk.LabelFrame(
            main_frame, 
            text=" Organization Options ",
            font=('Arial', 10, 'bold'),
            bg='#f0f0f0',
            padx=10,
            pady=10
        )
        options_frame.pack(fill='x', pady=10)
        
        self.option_var = tk.StringVar(value="type")
        
        tk.Radiobutton(
            options_frame, 
            text="By Type (images, documents, etc.)", 
            variable=self.option_var,
            value="type",
            bg='#f0f0f0',
            activebackground='#f0f0f0'
        ).pack(anchor='w')
        
        tk.Radiobutton(
            options_frame, 
            text="By Extension", 
            variable=self.option_var,
            value="extension",
            bg='#f0f0f0',
            activebackground='#f0f0f0'
        ).pack(anchor='w')
        
        tk.Radiobutton(
            options_frame, 
            text="By size (will organize between small, medium and large)", 
            variable=self.option_var,
            value="size",
            bg='#f0f0f0',
            activebackground='#f0f0f0'
        ).pack(anchor='w')
        
        # Barra de progresso
        self.progress = ttk.Progressbar(
            main_frame,
            orient='horizontal',
            length=400,
            mode='determinate',
            style='Horizontal.TProgressbar'
        )
        self.progress.pack(pady=(20, 5))
        
        self.status_label = ttk.Label(
            main_frame,
            text="Ready to organize files...",
            foreground='#555555'
        )
        self.status_label.pack(pady=(0, 15))
        
        # Frame para o botão START
        button_frame = tk.Frame(main_frame, bg='#f0f0f0')
        button_frame.pack(pady=10)
        
        self.start_button = ttk.Button(
            button_frame,
            text="START",
            command=self.start_organization,
            style='Start.TButton'
        )
        self.start_button.pack(ipadx=5, ipady=3)
        
        # Rodapé
        footer_label = ttk.Label(
            self.root,
            text="© 2025 FileSort - All rights reserved",
            font=('Arial', 8),
            foreground='#777777'
        )
        footer_label.pack(side='bottom', pady=10)
    
    def start_organization(self):
        """Inicia o processo de organização de arquivos"""
        self.start_button.config(state='disabled', text="PROCESSING...")
        self.status_label.config(text="Starting organization...")
        self.root.update()
        
        try:
            # Caminho para a pasta 'files'
            script_dir = os.path.dirname(os.path.abspath(__file__))
            files_dir = os.path.join(script_dir, 'files')
            
            if not os.path.exists(files_dir):
                messagebox.showerror("Error", "The 'files' folder does not exist!")
                self.reset_ui()
                return
            
            files = [f for f in os.listdir(files_dir) if os.path.isfile(os.path.join(files_dir, f))]
            
            if not files:
                messagebox.showinfo("Info", "No files found in the 'files' folder!")
                self.reset_ui()
                return
            
            total_files = len(files)
            processed_files = 0
            
            # Organiza os arquivos de acordo com a opção selecionada
            option = self.option_var.get()
            
            for i, filename in enumerate(files):
                file_path = os.path.join(files_dir, filename)
                
                if option == "type":
                    self.organize_by_type(file_path, filename, script_dir)
                elif option == "extension":
                    self.organize_by_extension(file_path, filename, script_dir)
                elif option == "size":
                    self.organize_by_size(file_path, filename, script_dir)
                
                processed_files += 1
                progress = int((processed_files / total_files) * 100)
                self.progress['value'] = progress
                self.status_label.config(text=f"Processing... {progress}% completed ({processed_files}/{total_files} files)")
                self.root.update()
            
            self.status_label.config(text="Organization completed successfully!")
            messagebox.showinfo("Completed", f"Successfully organized {total_files} files!")
        
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
        
        self.reset_ui()
    
    def organize_by_type(self, file_path, filename, script_dir):
        """Organiza arquivos por tipo (imagens, documentos, etc.)"""
        # Mapeamento de extensões para categorias
        type_map = {
            'images': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp'],
            'documents': ['.pdf', '.doc', '.docx', '.txt', '.rtf', '.odt', '.xls', '.xlsx', '.ppt', '.pptx'],
            'audio': ['.mp3', '.wav', '.ogg', '.flac', '.aac', '.wma'],
            'video': ['.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv'],
            'archives': ['.zip', '.rar', '.7z', '.tar', '.gz'],
            'executables': ['.exe', '.msi', '.bat', '.sh'],
            'code': ['.py', '.js', '.html', '.css', '.java', '.cpp', '.c', '.php', '.json']
        }
        
        ext = os.path.splitext(filename)[1].lower()
        category = 'others'
        
        for cat, exts in type_map.items():
            if ext in exts:
                category = cat
                break
        
        dest_dir = os.path.join(script_dir, category)
        os.makedirs(dest_dir, exist_ok=True)
        
        shutil.move(file_path, os.path.join(dest_dir, filename))
    
    def organize_by_extension(self, file_path, filename, script_dir):
        """Organiza arquivos por extensão"""
        ext = os.path.splitext(filename)[1].lower()
        if not ext:
            ext = 'no_extension'
        else:
            ext = ext[1:]  # Remove o ponto
            
        dest_dir = os.path.join(script_dir, ext)
        os.makedirs(dest_dir, exist_ok=True)
        
        shutil.move(file_path, os.path.join(dest_dir, filename))
    
    def organize_by_size(self, file_path, filename, script_dir):
        """Organiza arquivos por tamanho (small, medium, large)"""
        size = os.path.getsize(file_path)  # Tamanho em bytes
        
        if size < 1024 * 1024:  # Menor que 1MB
            size_category = 'small'
        elif size < 10 * 1024 * 1024:  # Entre 1MB e 10MB
            size_category = 'medium'
        else:  # Maior que 10MB
            size_category = 'large'
        
        dest_dir = os.path.join(script_dir, size_category)
        os.makedirs(dest_dir, exist_ok=True)
        
        shutil.move(file_path, os.path.join(dest_dir, filename))
    
    def reset_ui(self):
        """Reseta a UI para o estado inicial"""
        self.start_button.config(state='normal', text="START")
        self.progress['value'] = 0
        self.root.update()

if __name__ == "__main__":
    root = tk.Tk()
    app = FileSortApp(root)
    root.mainloop()