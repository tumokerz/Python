import json
import random
import tkinter as tk
from tkinter import ttk, messagebox, filedialog

class QuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Вопросник")
        self.root.geometry("800x600")
        
        self.questions = []
        self.current_question = None
        self.test_mode = False
        self.test_results = []
        
        self.create_widgets()
        self.load_default_data()

    def create_widgets(self):
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True)

        self.manage_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.manage_tab, text="Управление вопросами")
        self.create_manage_tab()
        
        self.test_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.test_tab, text="Тестирование")
        self.create_test_tab()
        
        self.results_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.results_tab, text="Результаты")
        self.create_results_tab()
    
    def create_manage_tab(self):
        self.questions_frame = ttk.LabelFrame(self.manage_tab, text="Список вопросов")
        self.questions_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.questions_tree = ttk.Treeview(
            self.questions_frame, 
            columns=('question', 'answer'), 
            show='headings'
        )
        self.questions_tree.heading('question', text='Вопрос')
        self.questions_tree.heading('answer', text='Ответ')
        self.questions_tree.column('question', width=400)
        self.questions_tree.column('answer', width=300)
        self.questions_tree.pack(fill='both', expand=True, padx=5, pady=5)
        
        btn_frame = ttk.Frame(self.manage_tab)
        btn_frame.pack(fill='x', padx=10, pady=5)
        
        ttk.Button(btn_frame, text="Добавить", command=self.add_question).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Редактировать", command=self.edit_question).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Удалить", command=self.delete_question).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Сохранить в файл", command=self.save_to_file).pack(side='right', padx=5)
        ttk.Button(btn_frame, text="Загрузить из файла", command=self.load_from_file).pack(side='right', padx=5)
    
    def create_test_tab(self):
        self.question_frame = ttk.LabelFrame(self.test_tab, text="Вопрос")
        self.question_frame.pack(fill='x', padx=10, pady=10)
        
        self.question_label = ttk.Label(
            self.question_frame, 
            text="Выберите 'Начать тест' для начала тестирования",
            wraplength=700
        )
        self.question_label.pack(fill='x', padx=10, pady=10)

        self.answer_frame = ttk.LabelFrame(self.test_tab, text="Ваш ответ")
        self.answer_frame.pack(fill='x', padx=10, pady=5)
        
        self.answer_entry = ttk.Entry(self.answer_frame)
        self.answer_entry.pack(fill='x', padx=10, pady=5)

        btn_frame = ttk.Frame(self.test_tab)
        btn_frame.pack(fill='x', padx=10, pady=5)
        
        self.start_btn = ttk.Button(btn_frame, text="Начать тест", command=self.start_test)
        self.start_btn.pack(side='left', padx=5)
        
        self.check_btn = ttk.Button(
            btn_frame, 
            text="Проверить ответ", 
            command=self.check_answer,
            state='disabled'
        )
        self.check_btn.pack(side='left', padx=5)
        
        self.finish_btn = ttk.Button(
            btn_frame, 
            text="Закончить тест", 
            command=self.finish_test,
            state='disabled'
        )
        self.finish_btn.pack(side='right', padx=5)
        
        self.skip_btn = ttk.Button(
            btn_frame, 
            text="Пропустить вопрос", 
            command=self.next_question,
            state='disabled'
        )
        self.skip_btn.pack(side='right', padx=5)
    
    def create_results_tab(self):
        self.results_tree = ttk.Treeview(
            self.results_tab, 
            columns=('question', 'user_answer', 'correct', 'result'), 
            show='headings'
        )
        self.results_tree.heading('question', text='Вопрос')
        self.results_tree.heading('user_answer', text='Ваш ответ')
        self.results_tree.heading('correct', text='Правильный ответ')
        self.results_tree.heading('result', text='Результат')
        self.results_tree.column('question', width=300)
        self.results_tree.column('user_answer', width=200)
        self.results_tree.column('correct', width=200)
        self.results_tree.column('result', width=100)
        self.results_tree.pack(fill='both', expand=True, padx=10, pady=10)
        
        btn_frame = ttk.Frame(self.results_tab)
        btn_frame.pack(fill='x', padx=10, pady=5)
        
        ttk.Button(
            btn_frame, 
            text="Сохранить результаты", 
            command=self.save_results
        ).pack(side='right', padx=5)
        
        ttk.Button(
            btn_frame, 
            text="Очистить результаты", 
            command=self.clear_results
        ).pack(side='right', padx=5)
    
    def load_default_data(self):
        # Вопросы и ответы
        self.questions = [
            {"question": "Вопрос 1. Ответ: 1", "answer": "1"},
            {"question": "Вопрос 2. Ответ: 2", "answer": "2"},
            {"question": "Вопрос 3. Ответ: 3", "answer": "3"}
        ]
        self.update_questions_list()
    
    def update_questions_list(self):
        self.questions_tree.delete(*self.questions_tree.get_children())
        for q in self.questions:
            self.questions_tree.insert('', 'end', values=(q['question'], q['answer']))
    
    def add_question(self):
        self.open_question_dialog("Добавить вопрос", None)
    
    def edit_question(self):
        selected = self.questions_tree.selection()
        if not selected:
            messagebox.showwarning("Предупреждение", "Выберите вопрос для редактирования")
            return
        
        item = self.questions_tree.item(selected[0])
        index = self.questions_tree.index(selected[0])
        self.open_question_dialog("Редактировать вопрос", index, item['values'][0], item['values'][1])
    
    def delete_question(self):
        selected = self.questions_tree.selection()
        if not selected:
            messagebox.showwarning("Предупреждение", "Выберите вопрос для удаления")
            return
        
        if messagebox.askyesno("Подтверждение", "Удалить выбранный вопрос?"):
            index = self.questions_tree.index(selected[0])
            self.questions.pop(index)
            self.update_questions_list()
    
    def open_question_dialog(self, title, index=None, question_text="", answer_text=""):
        dialog = tk.Toplevel(self.root)
        dialog.title(title)
        dialog.geometry("500x300")
        dialog.resizable(False, False)
        
        ttk.Label(dialog, text="Вопрос:").pack(padx=10, pady=(10, 0), anchor='w')
        question_entry = ttk.Entry(dialog)
        question_entry.pack(fill='x', padx=10, pady=5)
        question_entry.insert(0, question_text)
        
        ttk.Label(dialog, text="Ответ:").pack(padx=10, pady=(10, 0), anchor='w')
        answer_entry = ttk.Entry(dialog)
        answer_entry.pack(fill='x', padx=10, pady=5)
        answer_entry.insert(0, answer_text)
        
        def save_question():
            question = question_entry.get().strip()
            answer = answer_entry.get().strip()
            
            if not question or not answer:
                messagebox.showwarning("Предупреждение", "Вопрос и ответ не могут быть пустыми")
                return
            
            if index is not None:
                self.questions[index] = {"question": question, "answer": answer}
            else:
                self.questions.append({"question": question, "answer": answer})
            
            self.update_questions_list()
            dialog.destroy()
        
        btn_frame = ttk.Frame(dialog)
        btn_frame.pack(fill='x', padx=10, pady=10)
        
        ttk.Button(btn_frame, text="Сохранить", command=save_question).pack(side='right', padx=5)
        ttk.Button(btn_frame, text="Отмена", command=dialog.destroy).pack(side='right', padx=5)
    
    def save_to_file(self):
        if not self.questions:
            messagebox.showwarning("Предупреждение", "Нет вопросов для сохранения")
            return
        
        file_path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            title="Сохранить вопросы в файл"
        )
        
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(self.questions, f, ensure_ascii=False, indent=2)
                messagebox.showinfo("Успех", "Вопросы успешно сохранены")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось сохранить файл: {e}")
    
    def load_from_file(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            title="Загрузить вопросы из файла"
        )
        
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    self.questions = json.load(f)
                self.update_questions_list()
                messagebox.showinfo("Успех", "Вопросы успешно загружены")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось загрузить файл: {e}")
    
    def start_test(self):
        if not self.questions:
            messagebox.showwarning("Предупреждение", "Нет вопросов для тестирования")
            return
        
        self.test_mode = True
        self.test_results = []
        self.current_question = None
        
        self.start_btn.config(state='disabled')
        self.check_btn.config(state='normal')
        self.skip_btn.config(state='normal')
        self.finish_btn.config(state='normal')
        
        self.next_question()
    
    def next_question(self):
        if not self.questions:
            return
        
        available_questions = [q for q in self.questions if q != self.current_question]
        if not available_questions:
            self.finish_test()
            return
        
        self.current_question = random.choice(available_questions)
        self.question_label.config(text=self.current_question['question'])
        self.answer_entry.delete(0, 'end')
    
    def check_answer(self):
        if not self.test_mode or not self.current_question:
            return
        
        user_answer = self.answer_entry.get().strip()
        correct_answer = self.current_question['answer'].strip()
        
        is_correct = user_answer.lower() == correct_answer.lower()
        
        self.test_results.append({
            'question': self.current_question['question'],
            'user_answer': user_answer,
            'correct_answer': correct_answer,
            'is_correct': is_correct
        })
        
        result_text = "Правильно!" if is_correct else f"Неправильно. Правильный ответ: {correct_answer}"
        messagebox.showinfo("Результат", result_text)
        
        self.next_question()
    
    def finish_test(self):
        self.test_mode = False
        self.current_question = None
        
        self.question_label.config(text="Тестирование завершено!")
        self.answer_entry.delete(0, 'end')
        
        self.start_btn.config(state='normal')
        self.check_btn.config(state='disabled')
        self.skip_btn.config(state='disabled')
        self.finish_btn.config(state='disabled')
        
        self.update_results_tab()
        self.notebook.select(self.results_tab)

        # Статистика
        correct_count = sum(1 for r in self.test_results if r['is_correct'])
        total = len(self.test_results)
        if total > 0:
            messagebox.showinfo(
                "Результаты теста", 
                f"Вы ответили правильно на {correct_count} из {total} вопросов ({correct_count/total:.0%})"
            )
    
    def update_results_tab(self):
        self.results_tree.delete(*self.results_tree.get_children())
        
        for result in self.test_results:
            self.results_tree.insert('', 'end', values=(
                result['question'],
                result['user_answer'],
                result['correct_answer'],
                "✓" if result['is_correct'] else "✗"
            ))
    
    def save_results(self):
        if not self.test_results:
            messagebox.showwarning("Предупреждение", "Нет результатов для сохранения")
            return
        
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            title="Сохранить результаты теста"
        )
        
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write("Результаты тестирования:\n\n")
                    for i, result in enumerate(self.test_results, 1):
                        f.write(f"{i}. Вопрос: {result['question']}\n")
                        f.write(f"   Ваш ответ: {result['user_answer']}\n")
                        f.write(f"   Правильный ответ: {result['correct_answer']}\n")
                        f.write(f"   Результат: {'Правильно' if result['is_correct'] else 'Неправильно'}\n\n")
                    
                    correct_count = sum(1 for r in self.test_results if r['is_correct'])
                    total = len(self.test_results)
                    f.write(f"\nИтог: {correct_count} из {total} ({correct_count/total:.0%})\n")
                
                messagebox.showinfo("Успех", "Результаты успешно сохранены")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось сохранить результаты: {e}")
    
    def clear_results(self):
        if messagebox.askyesno("Подтверждение", "Очистить все результаты тестирования?"):
            self.test_results = []
            self.results_tree.delete(*self.results_tree.get_children())

if __name__ == "__main__":
    root = tk.Tk()
    app = QuizApp(root)
    root.mainloop()
