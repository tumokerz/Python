import tkinter as tk
from tkinter import scrolledtext
import itertools
import re

def impl(x, y):
    return (not x) or y

def equiv(x, y):
    return (x and y) or ((not x) and (not y))

replacements = {
    '∧': ' and ',
    '∨': ' or ',
    '&': ' and ',
}

def _replace_not(expr: str) -> str:
    return re.sub(r'¬\s*([A-Z])', r'(not \1)', expr)

def _replace_ops(expr: str) -> str:
    prev = None
    while prev != expr:
        prev = expr
        expr = re.sub(r'(\([^()]+\)|\(not [A-Z]\)|[A-Z])\s*→\s*(\([^()]+\)|\(not [A-Z]\)|[A-Z])',
                      r'impl(\1, \2)', expr)
        expr = re.sub(r'(\([^()]+\)|\(not [A-Z]\)|[A-Z])\s*≡\s*(\([^()]+\)|\(not [A-Z]\)|[A-Z])',
                      r'equiv(\1, \2)', expr)
    return expr

def parse_expr(expr: str) -> str:
    expr = _replace_not(expr)
    expr = _replace_ops(expr)
    for sym, repl in replacements.items():
        expr = expr.replace(sym, repl)
    return expr

def extract_subexprs(expr: str):
    subs = []
    for m in re.finditer(r'\([^()]+\)', expr):
        s = m.group(0).strip()
        if s not in subs:
            subs.append(s)
    for m in re.finditer(r'[A-Z]\s*[¬∧∨&≡→]\s*[A-Z]', expr):
        s = m.group(0).strip()
        if s not in subs:
            subs.append(s)
    return subs

def build_table():
    expr = entry.get("1.0", tk.END).strip()
    if not expr:
        return

    vars_ = sorted(set(ch for ch in expr if ch.isalpha()))
    subexprs = extract_subexprs(expr)
    parsed_subexprs = [parse_expr(s) for s in subexprs]
    parsed_final = parse_expr(expr)

    rows = []
    for vals in itertools.product([0, 1], repeat=len(vars_)):
        ctx = {v: bool(val) for v, val in zip(vars_, vals)}
        ctx["impl"] = impl
        ctx["equiv"] = equiv

        row = []
        row.extend(str(int(ctx[v])) for v in vars_)

        for parsed in parsed_subexprs:
            try:
                val = eval(parsed, {}, ctx)
                row.append(str(int(val)) if isinstance(val, bool) else str(val))
            except Exception:
                row.append("ERR")

        try:
            val = eval(parsed_final, {}, ctx)
            row.append(str(int(val)) if isinstance(val, bool) else str(val))
        except Exception:
            row.append("ERR")

        rows.append(row)

    header = vars_ + subexprs + ["F"]

    ncols = len(header)
    widths = []
    for i in range(ncols):
        col_items = [header[i]] + [row[i] for row in rows]
        widths.append(max(len(x) for x in col_items))

    header_line = " | ".join(header[i].ljust(widths[i]) for i in range(ncols))
    sep = "-" * len(header_line)
    lines = [header_line, sep]
    for row in rows:
        lines.append(" | ".join(row[i].ljust(widths[i]) for i in range(ncols)))

    result_win = tk.Toplevel(root)
    result_win.title("Таблица истинности")
    text = scrolledtext.ScrolledText(result_win, width=min(200, max(40, len(header_line)+2)),
                                     height=24, font=("Courier", 11))
    text.pack(padx=10, pady=10)
    text.insert(tk.END, "\n".join(lines))
    text.configure(state='disabled')

root = tk.Tk()
root.title("Логический калькулятор")
root.geometry("360x400")
root.resizable(False, False)

entry = tk.Text(root, height=2, width=24, font=("Arial", 14))
entry.grid(row=0, column=0, columnspan=4, padx=10, pady=10)

buttons = [
    "A", "B", "C", "D",
    "(", ")", "¬", "∧",
    "∨", "&", "→", "≡",
]

row, col = 1, 0
for b in buttons:
    if b.strip():
        tk.Button(root, text=b, width=4, height=2, font=("Arial", 12),
                  command=lambda x=b: entry.insert(tk.END, x)).grid(row=row, column=col, padx=4, pady=4, sticky="nsew")
    col += 1
    if col > 3:
        col = 0
        row += 1

tk.Button(root, text="Построить таблицу", width=28, height=2, font=("Arial", 14),
          command=build_table).grid(row=row+1, column=0, columnspan=4, pady=12)

root.mainloop()
