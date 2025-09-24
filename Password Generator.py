import random
import string
import tkinter as tk
from tkinter import ttk, messagebox

class PasswordGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Генератор паролей")
        self.root.geometry("400x400")
        self.root.resizable(False, False)
        
        self.setup_ui()
    
    def setup_ui(self):
        title_label = ttk.Label(self.root, text="Генератор паролей", font=('Arial', 16))
        title_label.pack(pady=10)
        
        # Ползунок для длины пароля
        self.length_label = ttk.Label(self.root, text="Длина пароля: 8")
        self.length_label.pack()
        
        self.length_slider = ttk.Scale(
            self.root, 
            from_=8, 
            to=128, 
            value=8,
            command=self.update_length_label
        )
        self.length_slider.pack(fill='x', padx=20, pady=5)
        
        # Чекбоксы для параметров
        self.digits_var = tk.BooleanVar(value=True)
        digits_check = ttk.Checkbutton(
            self.root, 
            text="Цифры (0-9)", 
            variable=self.digits_var
        )
        digits_check.pack(anchor='w', padx=20, pady=5)
        
        self.uppercase_var = tk.BooleanVar(value=True)
        uppercase_check = ttk.Checkbutton(
            self.root, 
            text="Заглавные буквы (A-Z)", 
            variable=self.uppercase_var
        )
        uppercase_check.pack(anchor='w', padx=20, pady=5)
        
        self.special_var = tk.BooleanVar(value=False)
        special_check = ttk.Checkbutton(
            self.root, 
            text="Спецсимволы (!@#...)", 
            variable=self.special_var
        )
        special_check.pack(anchor='w', padx=20, pady=5)
        
        # Кнопка генерации
        generate_btn = ttk.Button(
            self.root, 
            text="Сгенерировать пароль", 
            command=self.generate_password
        )
        generate_btn.pack(pady=20)
        
        # Поле для вывода пароля
        self.password_var = tk.StringVar()
        password_entry = ttk.Entry(
            self.root, 
            textvariable=self.password_var, 
            font=('Arial', 12), 
            state='readonly',
            justify='center'
        )
        password_entry.pack(fill='x', padx=20, pady=5)
        
        # Кнопка копирования
        copy_btn = ttk.Button(
            self.root, 
            text="Копировать в буфер", 
            command=self.copy_to_clipboard
        )
        copy_btn.pack(pady=5)
        
        # Кнопка для генерации нескольких паролей
        multiple_btn = ttk.Button(
            self.root, 
            text="Сгенерировать несколько", 
            command=self.generate_multiple_passwords
        )
        multiple_btn.pack(pady=5)
    
    def update_length_label(self, value):
        self.length_label.config(text=f"Длина пароля: {int(float(value))}")
    
    def generate_password(self):
        length = int(self.length_slider.get())
        use_digits = self.digits_var.get()
        use_uppercase = self.uppercase_var.get()
        use_special = self.special_var.get()
        
        characters = string.ascii_lowercase
        
        if use_digits:
            characters += string.digits
        if use_uppercase:
            characters += string.ascii_uppercase
        if use_special:
            characters += string.punctuation
        
        if not characters:
            messagebox.showerror("Ошибка", "Не выбрано ни одного типа символов!")
            return
        
        try:
            password = ''.join(random.SystemRandom().choice(characters) for _ in range(length))
            self.password_var.set(password)
        except:
            messagebox.showerror("Ошибка", "Не удалось сгенерировать пароль")
    
    def copy_to_clipboard(self):
        password = self.password_var.get()
        if password:
            self.root.clipboard_clear()
            self.root.clipboard_append(password)
            messagebox.showinfo("Успех", "Пароль скопирован в буфер обмена")
        else:
            messagebox.showwarning("Предупреждение", "Нет пароля для копирования")
    
    def generate_multiple_passwords(self):
        length = int(self.length_slider.get())
        use_digits = self.digits_var.get()
        use_uppercase = self.uppercase_var.get()
        use_special = self.special_var.get()
        
        characters = string.ascii_lowercase
        
        if use_digits:
            characters += string.digits
        if use_uppercase:
            characters += string.ascii_uppercase
        if use_special:
            characters += string.punctuation
        
        if not characters:
            messagebox.showerror("Ошибка", "Не выбрано ни одного типа символов!")
            return
        
        try:
            passwords = []
            for _ in range(5):
                password = ''.join(random.SystemRandom().choice(characters) for _ in range(length))
                passwords.append(password)
            
            # Окно со списком паролей
            top = tk.Toplevel(self.root)
            top.title("Несколько паролей")
            top.geometry("300x200")
            
            text = tk.Text(top, wrap='word')
            text.pack(fill='both', expand=True)
            
            for i, pwd in enumerate(passwords, 1):
                text.insert('end', f"{i}. {pwd}\n")
            
            text.config(state='disabled')
            
            # Копировать пароли
            copy_all_btn = ttk.Button(
                top, 
                text="Копировать все", 
                command=lambda: self.copy_all_passwords(passwords)
            )
            copy_all_btn.pack(pady=5)
            
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сгенерировать пароли: {e}")
    
    def copy_all_passwords(self, passwords):
        text_to_copy = "\n".join(passwords)
        self.root.clipboard_clear()
        self.root.clipboard_append(text_to_copy)
        messagebox.showinfo("Успех", "Все пароли скопированы в буфер обмена")

if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordGeneratorApp(root)
    root.mainloop()
