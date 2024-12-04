import math
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import random
from datetime import datetime

class QuadraticCalculatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculadora de Equações de Segundo Grau")
        self.history = []
        self.max_history = 10  # Limitar o número de entradas no histórico

        # Configuração do estilo
        self.style = ttk.Style()
        self.set_theme("light")

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

        # Botão para alternar tema
        self.theme_button = ttk.Button(root, text="Alternar Tema", command=self.toggle_theme)
        self.theme_button.pack(pady=10)

    def setup_calc_tab(self):
        ttk.Label(self.calc_tab, text="Digite os coeficientes da equação (ax² + bx + c = 0):").grid(
            column=0, row=0, columnspan=3, pady=10
        )

        ttk.Label(self.calc_tab, text="a:").grid(column=0, row=1, sticky="W")
        self.a_entry = ttk.Entry(self.calc_tab, width=10)
        self.a_entry.grid(column=1, row=1, pady=5)

        ttk.Label(self.calc_tab, text="b:").grid(column=0, row=2, sticky="W")
        self.b_entry = ttk.Entry(self.calc_tab, width=10)
        self.b_entry.grid(column=1, row=2, pady=5)

        ttk.Label(self.calc_tab, text="c:").grid(column=0, row=3, sticky="W")
        self.c_entry = ttk.Entry(self.calc_tab, width=10)
        self.c_entry.grid(column=1, row=3, pady=5)

        self.calc_button = ttk.Button(self.calc_tab, text="Calcular", command=self.calculate)
        self.calc_button.grid(column=0, row=4, pady=10)

        self.clear_button = ttk.Button(self.calc_tab, text="Limpar", command=self.clear_inputs)
        self.clear_button.grid(column=1, row=4, pady=10)

        self.random_button = ttk.Button(self.calc_tab, text="Gerar Valores Aleatórios", command=self.generate_random_values)
        self.random_button.grid(column=2, row=4, pady=10)

        self.result_label = ttk.Label(self.calc_tab, text="", wraplength=400, anchor="center", justify="center")
        self.result_label.grid(column=0, row=5, columnspan=3, pady=10)

        self.process_text = tk.Text(self.calc_tab, wrap="word", height=8, width=50, state="disabled")
        self.process_text.grid(column=0, row=6, columnspan=3, padx=10, pady=10)

        self.delta_label = ttk.Label(self.calc_tab, text="", wraplength=400, anchor="center", justify="center")
        self.delta_label.grid(column=0, row=7, columnspan=3, pady=5)

        # Dicas rápidas
        self.help_button = ttk.Button(self.calc_tab, text="Dicas", command=self.show_help)
        self.help_button.grid(column=0, row=8, columnspan=3, pady=10)

    def setup_history_tab(self):
        ttk.Label(self.history_tab, text="Histórico de Cálculos:").pack(pady=10)

        self.history_text = tk.Text(self.history_tab, wrap="word", height=15, width=60, state="disabled")
        self.history_text.pack(padx=10, pady=10)

        self.export_button = ttk.Button(self.history_tab, text="Exportar Histórico", command=self.export_history)
        self.export_button.pack(pady=10)

    def calculate(self):
        try:
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
                process.append(f"Δ = b² - 4ac: Δ = {b}² - 4*{a}*{c} = {delta}")
                self.delta_label.config(text=f"Discriminante (Δ): {delta}")

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

                # Soma e produto das raízes
                sum_of_roots = -b / a
                product_of_roots = c / a
                process.append(f"Soma das raízes: {sum_of_roots}")
                process.append(f"Produto das raízes: {product_of_roots}")

            self.result_label.config(text=result)
            self.update_process_text(process)
            self.add_to_history(a, b, c, result, process)
            self.animate_result_display()
        except ValueError:
            messagebox.showerror("Erro", "Por favor, insira valores numéricos válidos.")

    def add_to_history(self, a, b, c, result, process):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entry = f"Equação: {a}x² + {b}x + {c} = 0\nResultado: {result}\n"
        entry += "\n".join(process) + f"\nData e Hora: {timestamp}\n\n"
        self.history.append(entry)

        if len(self.history) > self.max_history:  # Limitar o número de entradas no histórico
            self.history.pop(0)

        self.update_history_tab()

    def update_history_tab(self):
        self.history_text.config(state="normal")
        self.history_text.delete("1.0", tk.END)
        self.history_text.insert("1.0", "\n".join(self.history))
        self.history_text.config(state="disabled")

    def update_process_text(self, process):
        self.process_text.config(state="normal")
        self.process_text.delete("1.0", tk.END)
        self.process_text.insert("1.0", "\n".join(process))
        self.process_text.config(state="disabled")

    def animate_result_display(self):
        self.result_label.config(text="", foreground="black")
        for i in range(3):
            self.root.after(i * 500, lambda: self.result_label.config(text="Calculando..."))
        self.root.after(1500, lambda: self.result_label.config(text="Resultado exibido"))

    def clear_inputs(self):
        if messagebox.askyesno("Limpar", "Você tem certeza que quer limpar os campos?"):
            self.a_entry.delete(0, tk.END)
            self.b_entry.delete(0, tk.END)
            self.c_entry.delete(0, tk.END)
            self.result_label.config(text="")
            self.delta_label.config(text="")
            self.process_text.config(state="normal")
            self.process_text.delete("1.0", tk.END)
            self.process_text.config(state="disabled")

    def generate_random_values(self):
        self.a_entry.delete(0, tk.END)
        self.b_entry.delete(0, tk.END)
        self.c_entry.delete(0, tk.END)

        self.a_entry.insert(0, random.randint(-10, 10))
        self.b_entry.insert(0, random.randint(-10, 10))
        self.c_entry.insert(0, random.randint(-10, 10))

    def toggle_theme(self):
        current_theme = self.style.theme_use()
        new_theme = "light" if current_theme == "alt" else "dark"
        self.set_theme(new_theme)

    def set_theme(self, theme):
        if theme == "light":
            self.style.theme_use("clam")
            self.root.configure(bg="white")
        elif theme == "dark":
            self.style.theme_use("alt")
            self.root.configure(bg="black")

    def show_help(self):
        messagebox.showinfo("Dicas de Cálculo", "1. A equação deve estar na forma ax² + bx + c = 0.\n"
                                               "2. Se a = 0, a equação será linear.\n"
                                               "3. O discriminante (Δ) é fundamental para determinar o número e o tipo de raízes.")

    def export_history(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if file_path:
            with open(file_path, "w") as file:
                file.write("\n".join(self.history))

if __name__ == "__main__":
    root = tk.Tk()
    app = QuadraticCalculatorApp(root)
    root.mainloop()

