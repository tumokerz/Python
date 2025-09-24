import tkinter as tk
from math import gcd

class FractionCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Калькулятор дробей")
        self.root.geometry("400x550")
        
        # переменные
        self.current_input = ""
        self.result = None
        self.last_operation = None
        self.reset_input = False
        self.fraction_mode = True  # режим вывода: true - дроби, false - десятичные
        
        self.create_widgets()
    
    def create_widgets(self):
        self.display = tk.Entry(
            self.root, 
            font=('Arial', 24), 
            justify='right', 
            bd=10, 
            insertwidth=2
        )
        self.display.grid(row=0, column=0, columnspan=4, sticky="nsew")
        
        buttons = [
            ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('÷', 1, 3),
            ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('×', 2, 3),
            ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('-', 3, 3),
            ('0', 4, 0), ('.', 4, 1), ('=', 4, 2), ('+', 4, 3),
            ('C', 5, 0), ('⌫', 5, 1), ('a/b', 5, 2), ('Dec/Frac', 5, 3)
        ]
        
        for (text, row, col) in buttons:
            btn = tk.Button(
                self.root,
                text=text,
                font=('Arial', 18),
                command=lambda t=text: self.on_button_click(t)
            )
            btn.grid(row=row, column=col, sticky="nsew", padx=5, pady=5)
        
        for i in range(6):
            self.root.grid_rowconfigure(i, weight=1)
        for i in range(4):
            self.root.grid_columnconfigure(i, weight=1)
    
    def on_button_click(self, char):
        if char == 'C':
            self.current_input = ""
            self.result = None
            self.last_operation = None
            self.display.delete(0, tk.END)
        
        elif char == '⌫':
            self.current_input = self.current_input[:-1]
            self.display.delete(0, tk.END)
            self.display.insert(0, self.current_input)
        
        elif char == 'a/b':
            if '/' not in self.current_input:
                self.current_input += '/'
                self.display.delete(0, tk.END)
                self.display.insert(0, self.current_input)
        
        elif char == 'Dec/Frac':
            self.fraction_mode = not self.fraction_mode
            if self.result:
                self.display.delete(0, tk.END)
                self.display.insert(0, self.format_result(*self.result))
        
        elif char == '=':
            self.calculate()
        
        elif char in '+-×÷':
            if self.current_input:
                self.calculate()
                self.last_operation = char
                self.reset_input = True
        
        else:  # цифры и символы
            if self.reset_input:
                self.current_input = ""
                self.reset_input = False
            self.current_input += char
            self.display.delete(0, tk.END)
            self.display.insert(0, self.current_input)
    
    def calculate(self):
        try:
            # парсинг данных
            if '/' in self.current_input:
                num, den = map(int, self.current_input.split('/'))
                current_value = (num, den)
            else:
                current_value = (float(self.current_input), 1)
            
            if self.result is None:
                self.result = current_value
            else:
                a_num, a_den = self.result
                b_num, b_den = current_value
                
                if self.last_operation == '+':
                    new_num = a_num * b_den + b_num * a_den
                    new_den = a_den * b_den
                elif self.last_operation == '-':
                    new_num = a_num * b_den - b_num * a_den
                    new_den = a_den * b_den
                elif self.last_operation == '×':
                    new_num = a_num * b_num
                    new_den = a_den * b_den
                elif self.last_operation == '÷':
                    new_num = a_num * b_den
                    new_den = a_den * b_num
                
                # Сокращение дробей
                common_divisor = gcd(int(new_num), int(new_den))
                new_num = int(new_num // common_divisor)
                new_den = int(new_den // common_divisor)
                
                self.result = (new_num, new_den)
            
            # Вывод результата
            self.display.delete(0, tk.END)
            self.display.insert(0, self.format_result(*self.result))
            self.current_input = ""
        
        except (ValueError, ZeroDivisionError):
            self.display.delete(0, tk.END)
            self.display.insert(0, "Ошибка")
            self.current_input = ""
            self.result = None
    
    def format_result(self, num, den):
        """Форматирует результат в дробь или десятичное число"""
        if not self.fraction_mode:
            return str(round(num / den, 5))  # Десятичный формат
        
        if den == 1:
            return str(num)
        
        # Перевод смешанных дробей
        whole = num // den
        remainder = num % den
        
        if whole != 0 and remainder != 0:
            return f"{whole} {remainder}/{den}"
        else:
            return f"{num}/{den}"

if __name__ == "__main__":
    root = tk.Tk()
    app = FractionCalculator(root)
    root.mainloop()
