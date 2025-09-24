import tkinter as tk
from tkinter import messagebox
import json
import os

class VocabularyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Английский словарь")
        
        
        self.file_path = "vocabulary.json"
        self.vocabulary = self.load_vocabulary()
        
        
        self.create_widgets()
    
    def load_vocabulary(self):
        """Загружает словарь из JSON-файла или создаёт новый, если файла нет."""
        if os.path.exists(self.file_path):
            with open(self.file_path, "r", encoding="utf-8") as file:
                return json.load(file)
        return {}
    
    def save_vocabulary(self):
        """Сохраняет словарь в JSON-файл."""
        with open(self.file_path, "w", encoding="utf-8") as file:
            json.dump(self.vocabulary, file, ensure_ascii=False, indent=4)
    
    def create_widgets(self):
        """Создает элементы интерфейса."""
        
        tk.Label(self.root, text="Английское слово:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.eng_entry = tk.Entry(self.root, width=30)
        self.eng_entry.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(self.root, text="Перевод:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.trans_entry = tk.Entry(self.root, width=30)
        self.trans_entry.grid(row=1, column=1, padx=5, pady=5)
        
        
        tk.Button(self.root, text="Добавить/Обновить", command=self.add_or_update_word).grid(row=2, column=0, columnspan=2, pady=5)
        tk.Button(self.root, text="Найти по английскому слову", command=lambda: self.find_word(by_translation=False)).grid(row=3, column=0, columnspan=2, pady=5)
        tk.Button(self.root, text="Найти по переводу", command=lambda: self.find_word(by_translation=True)).grid(row=4, column=0, columnspan=2, pady=5)
        tk.Button(self.root, text="Показать все слова", command=self.show_all_words).grid(row=5, column=0, columnspan=2, pady=5)
        tk.Button(self.root, text="Удалить слово", command=self.delete_word).grid(row=6, column=0, columnspan=2, pady=5)
        
        self.output_text = tk.Text(self.root, height=10, width=50, state="disabled")
        self.output_text.grid(row=7, column=0, columnspan=2, padx=5, pady=5)
    
    def add_or_update_word(self):
        """Добавляет новое слово или обновляет существующее."""
        eng_word = self.eng_entry.get().strip().lower()
        translation = self.trans_entry.get().strip().lower()
        
        if not eng_word or not translation:
            messagebox.showwarning("Ошибка", "Поля не могут быть пустыми.")
            return
        
        self.vocabulary[eng_word] = translation
        self.save_vocabulary()
        messagebox.showinfo("Успех", f"Слово '{eng_word}' добавлено/обновлено.")
        self.clear_entries()
    
    def find_word(self, by_translation=False):
        """Ищет слово по английскому или по переводу."""
        search_term = self.trans_entry.get().strip().lower() if by_translation else self.eng_entry.get().strip().lower()
        
        if not search_term:
            messagebox.showwarning("Ошибка", "Введите слово для поиска")
            return
        
        self.output_text.config(state="normal")
        self.output_text.delete(1.0, tk.END)
        
        found = False
        
        if by_translation:
            # может быть несколько слов с одинаковым переводом
            for eng, trans in self.vocabulary.items():
                if search_term in trans:
                    self.output_text.insert(tk.END, f"{eng} -> {trans}\n")
                    found = True
        else:
            translation = self.vocabulary.get(search_term, None)
            if translation:
                self.output_text.insert(tk.END, f"{search_term} -> {translation}\n")
                found = True
        
        if not found:
            search_type = "переводу" if by_translation else "английскому слову"
            self.output_text.insert(tk.END, f"По {search_type} '{search_term}' ничего не найдено!")
        
        self.output_text.config(state="disabled")
    
    def show_all_words(self):
        """Показывает все слова в словаре."""
        self.output_text.config(state="normal")
        self.output_text.delete(1.0, tk.END)
        
        if not self.vocabulary:
            self.output_text.insert(tk.END, "Словарь пуст!")
        else:
            for eng, trans in sorted(self.vocabulary.items()):
                self.output_text.insert(tk.END, f"{eng} -> {trans}\n")
        
        self.output_text.config(state="disabled")
    
    def delete_word(self):
        """Удаляет слово из словаря."""
        eng_word = self.eng_entry.get().strip().lower()
        
        if not eng_word:
            messagebox.showwarning("Ошибка", "Введите слово для удаления!")
            return
        
        if eng_word in self.vocabulary:
            del self.vocabulary[eng_word]
            self.save_vocabulary()
            messagebox.showinfo("Успех", f"Слово '{eng_word}' удалено!")
            self.clear_entries()
        else:
            messagebox.showwarning("Ошибка", f"Слово '{eng_word}' не найдено!")
    
    def clear_entries(self):
        """Очищает поля ввода."""
        self.eng_entry.delete(0, tk.END)
        self.trans_entry.delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = VocabularyApp(root)
    root.mainloop()
