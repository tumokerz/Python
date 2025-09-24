import tkinter as tk
from tkinter import scrolledtext
import itertools

# замена пайтон-символов на логические
replacements = {
    '¬': ' not ',
    '∧': ' and ',
    '∨': ' or ',
    '→': ' <= ',
    '≡': ' == ',
}

def parse_expr(expr):
    for sym, repl in replacements.items():
        expr = expr.replace(sym, repl)
    return expr

def build_table():
    expr = entry.get("1.0", tk.END).strip()
    if not expr:
        return

    parsed = parse_expr(expr)
    vars_ = sorted(set(filter(str.isalpha, expr)))

    result_win = tk.Toplevel(root)
    result_win.title("Таблица истинности")
    text = scrolledtext.ScrolledText(result_win, width=60, height=20)
    text.pack(padx=10, pady=10)

    header = " | ".join(vars_) + " | F"
    text.insert(tk.END, header + "\n")
    text.insert(tk.END, "-" * (len(header) + 5) + "\n")

    for vals in itertools.product([0, 1], repeat=len(vars_)):
        ctx = {v: bool(val)
            for v, val in zip(vars_, vals)}
        try:
            val = eval(parsed, {}, ctx)
        except Exception:
            val = "ERR"
        row = " | ".join(str(int(ctx[v])) for v in vars_) + " | " + str(int(val) if val in (True, False) else val)
        text.insert(tk.END, row + "\n")


root = tk.Tk()
root.title("Логический калькулятор")
root.geometry("260x340")
root.resizable(False, False)


entry = tk.Text(root, height=2, width=20, font=("Arial", 14))
entry.grid(row=0, column=0, columnspan=4, padx=10, pady=10)


buttons = [
"A", "B", "C", "D",
"(", ")", "¬", "∧",
"∨", "→", "≡", " ",
]


row, col = 1, 0
for b in buttons:
    if b.strip():
        tk.Button(root, text=b, width=3, height=2, font=("Arial", 12),
            command=lambda x=b: entry.insert(tk.END, x)).grid(row=row, column=col, padx=5, pady=5, sticky="nsew")
    col += 1
    if col > 3:
        col = 0
        row += 1


tk.Button(root, text="Построить таблицу", width=20, height=2, font=("Arial", 16),
command=build_table).grid(row=row+1, column=0, columnspan=4, pady=20)


