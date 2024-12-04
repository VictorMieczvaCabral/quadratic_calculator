import math
import tkinter as tk
from tkinter import ttk, messagebox

class QuadraticCalculatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculadora de Equações de Segundo Grau")
        self.history = []

        # Configurando as abas
        self.tab_control = ttk.Notebook(root)
        self.calc_tab = ttk.Frame(self.tab_control)
        self.history_tab = ttk.Frame(self.tab_control)

        self.tab_control.add(self.calc_tab, text="Cálculo")
        self.tab_control.add(self.history_tab, text="Histórico")
        self.tab_control.pack(expand=1, fill="both")

        # Aba de Cálculo
        self.setup_calc_tab()

        # Aba de Histórico
        self.setup_history_tab()

    def setup_calc_tab(self):
        ttk.Label(self.calc_tab, text="Digite os coeficientes da equação (ax² + bx + c = 0):").grid(
            column=0, row=0, columnspan=2, pady=10
        )

        ttk.Label(self.calc_tab, text="a:").grid(column=0, row=1, sticky="W")
        self.a_entry = ttk.Entry(self.calc_tab)
        self.a_entry.grid(column=1, row=1)

        ttk.Label(self.calc_tab, text="b:").grid(column=0, row=2, sticky="W")
        self.b_entry = ttk.Entry(self.calc_tab)
        self.b_entry.grid(column=1, row=2)

        ttk.Label(self.calc_tab, text="c:").grid(column=0, row=3, sticky="W")
        self.c_entry = ttk.Entry(self.calc_tab)
        self.c_entry.grid(column=1, row=3)

        self.calc_button = ttk.Button(self.calc_tab, text="Calcular", command=self.calculate)
        self.calc_button.grid(column=0, row=4, columnspan=2, pady=10)

        self.result_label = ttk.Label(self.calc_tab, text="", wraplength=300)
        self.result_label.grid(column=0, row=5, columnspan=2, pady=10)

    def setup_history_tab(self):
        ttk.Label(self.history_tab, text="Histórico de Cálculos:").pack(pady=10)

        self.history_text = tk.Text(self.history_tab, wrap="word", height=15, width=50, state="disabled")
        self.history_text.pack(padx=10, pady=10)

    def calculate(self):
        try:
            # Obter valores dos coeficientes
            a = float(self.a_entry.get())
            b = float(self.b_entry.get())
            c = float(self.c_entry.get())

            process = []
            if a == 0:
                if b == 0:
                    result = "Não é uma equação válida." if c != 0 else "Equação trivial: 0 = 0."
                else:
                    result = f"Equação linear. Solução: x = {-c / b}"
                    process.append(f"Equação linear: -c/b = -{c}/{b}")
            else:
                delta = b**2 - 4 * a * c
                process.append(f"Calculando Δ = b² - 4ac: Δ = {b}² - 4*{a}*{c} = {delta}")

                if delta > 0:
                    root1 = (-b + math.sqrt(delta)) / (2 * a)
                    root2 = (-b - math.sqrt(delta)) / (2 * a)
                    result = f"Raízes reais: x1 = {root1}, x2 = {root2}"
                    process.append(f"x1 = (-b + √Δ) / 2a = (-{b} + √{delta}) / (2*{a})")
                    process.append(f"x2 = (-b - √Δ) / 2a = (-{b} - √{delta}) / (2*{a})")
                elif delta == 0:
                    root = -b / (2 * a)
                    result = f"Raiz única: x = {root}"
                    process.append(f"x = -b / 2a = -{b} / (2*{a})")
                else:
                    real_part = -b / (2 * a)
                    imaginary_part = math.sqrt(-delta) / (2 * a)
                    result = f"Raízes complexas: x1 = {real_part} + {imaginary_part}i, x2 = {real_part} - {imaginary_part}i"
                    process.append(f"x1 = (-b + i√|Δ|) / 2a = (-{b} + i√{-delta}) / (2*{a})")
                    process.append(f"x2 = (-b - i√|Δ|) / 2a = (-{b} - i√{-delta}) / (2*{a})")

            # Exibir resultado
            self.result_label.config(text=result)
            # Adicionar ao histórico
            self.add_to_history(a, b, c, result, process)
        except ValueError:
            messagebox.showerror("Erro", "Por favor, insira valores numéricos válidos.")

    def add_to_history(self, a, b, c, result, process):
        entry = f"Equação: {a}x² + {b}x + {c} = 0\nResultado: {result}\n"
        entry += "\n".join(process) + "\n\n"
        self.history.append(entry)
        self.update_history_tab()

    def update_history_tab(self):
        self.history_text.config(state="normal")
        self.history_text.delete("1.0", tk.END)
        self.history_text.insert("1.0", "\n".join(self.history))
        self.history_text.config(state="disabled")


if __name__ == "__main__":
    root = tk.Tk()
    app = QuadraticCalculatorApp(root)
    root.mainloop()

