import math

def solve_quadratic(a, b, c):
    """
    Resolve uma equação de segundo grau na forma ax^2 + bx + c = 0.
    Retorna as raízes reais (ou complexas).
    """
    if a == 0:
        if b == 0:
            return "Não é uma equação válida." if c != 0 else "Equação trivial: 0 = 0."
        return f"Equação linear. Solução: x = {-c / b}"

    delta = b**2 - 4*a*c

    if delta > 0:
        root1 = (-b + math.sqrt(delta)) / (2 * a)
        root2 = (-b - math.sqrt(delta)) / (2 * a)
        return f"Raízes reais: x1 = {root1}, x2 = {root2}"
    elif delta == 0:
        root = -b / (2 * a)
        return f"Raiz única: x = {root}"
    else:
        real_part = -b / (2 * a)
        imaginary_part = math.sqrt(-delta) / (2 * a)
        return f"Raízes complexas: x1 = {real_part} + {imaginary_part}i, x2 = {real_part} - {imaginary_part}i"

def main():
    print("Calculadora de Equações de Segundo Grau")
    print("Forma da equação: ax^2 + bx + c = 0")
    
    try:
        a = float(input("Digite o valor de a: "))
        b = float(input("Digite o valor de b: "))
        c = float(input("Digite o valor de c: "))
        
        resultado = solve_quadratic(a, b, c)
        print(resultado)
    except ValueError:
        print("Por favor, insira valores numéricos válidos.")

if __name__ == "__main__":
    main()
