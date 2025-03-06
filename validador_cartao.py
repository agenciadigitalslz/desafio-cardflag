import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os
import sys

class ValidadorCartao:
    
    def __init__(self):
        # Dicionário atualizado com as regras de validação das bandeiras
        self.bandeiras = {
            'visa': {
                'prefixos': ['4'],
                'comprimentos': [16],
                'imagem': 'base/logo_visa.webp'
            },
            'visa_electron': {
                'prefixos': ['4026', '417500', '4508', '4844', '4913', '4917'],
                'comprimentos': [16],
                'imagem': 'base/logo_visa_e.webp'
            },
            'mastercard': {
                'prefixos': ['51', '52', '53', '54', '55'],
                'comprimentos': [16],
                'imagem': 'base/logo_master.webp'
            },
            'amex': {
                'prefixos': ['34', '37'],
                'comprimentos': [15],
                'imagem': 'base/logo_amex.webp'
            },
            'diners': {
                'prefixos': ['36', '38', '300', '301', '302', '303', '304', '305'],
                'comprimentos': [14],
                'imagem': 'base/logo_diners.webp'
            },
            'discover': {
                'prefixos': ['6011', '65'],
                'comprimentos': [16],
                'imagem': 'base/logo_discover.webp'
            },
            'enroute': {
                'prefixos': ['2014', '2149'],
                'comprimentos': [15],
                'imagem': 'base/logo_enroute.webp'
            },
            'jcb': {
                'prefixos': ['35'],
                'comprimentos': [16],
                'imagem': 'base/logo_jcb.webp'
            },
            'maestro': {
                'prefixos': ['5018', '5020', '5038', '6304', '6759', '6761', '6763'],
                'comprimentos': [12, 13, 14, 15, 16, 17, 18, 19],
                'imagem': 'base/logo_maestro.webp'
            },
            'solo': {
                'prefixos': ['6334', '6767'],
                'comprimentos': [16, 18, 19],
                'imagem': 'base/logo_solo.webp'
            },
            'switch': {
                'prefixos': ['4903', '4905', '4911', '4936', '564182', '633110', '6333', '6759'],
                'comprimentos': [16, 18, 19],
                'imagem': 'base/logo_switch.webp'
            },
            'laser': {
                'prefixos': ['6304', '6706', '6771', '6709'],
                'comprimentos': [16, 17, 18, 19],
                'imagem': 'base/logo_laser.webp'
            }
        }

    def algoritmo_luhn(self, numero):
        try:
            soma = 0
            dobrar = False
            
            for digito in reversed(numero):
                num = int(digito)
                if dobrar:
                    num *= 2
                    if num > 9:
                        num -= 9
                soma += num
                dobrar = not dobrar
                
            return (soma % 10) == 0
        except ValueError:
            return False

    def validar_cartao(self, numero):
        # Remove espaços e traços
        numero = ''.join(filter(str.isdigit, str(numero)))
        
        if not numero:
            return {
                'bandeira': 'inválido',
                'imagem': 'base/default.webp',
                'valido': False
            }

        for bandeira, regras in self.bandeiras.items():
            if len(numero) not in regras['comprimentos']:
                continue
                
            if any(numero.startswith(prefixo) for prefixo in regras['prefixos']):
                return {
                    'bandeira': bandeira,
                    'imagem': regras['imagem'],
                    'valido': self.algoritmo_luhn(numero)
                }
        
        return {
            'bandeira': 'desconhecida',
            'imagem': 'base/default.webp',
            'valido': False
        }

class ValidadorCartaoGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Validador de Cartão de Crédito")
        self.validador = ValidadorCartao()
        
        # Frame principal
        self.frame = tk.Frame(root, padx=20, pady=20)
        self.frame.pack()
        
        # Campo de entrada
        self.label = tk.Label(self.frame, text="Digite o número do cartão:")
        self.label.pack()
        
        self.entrada = tk.Entry(self.frame, width=30)
        self.entrada.pack(pady=10)
        
        # Botão de validação
        self.botao = tk.Button(self.frame, text="Validar", command=self.validar)
        self.botao.pack(pady=5)
        
        # Resultado
        self.resultado_label = tk.Label(self.frame, text="")
        self.resultado_label.pack(pady=10)
        
        # Imagem
        self.imagem_label = tk.Label(self.frame)
        self.imagem_label.pack()

    def validar(self):
        numero = self.entrada.get()
        resultado = self.validador.validar_cartao(numero)
        
        mensagem = f"Bandeira: {resultado['bandeira']}\nVálido: {'Sim' if resultado['valido'] else 'Não'}"
        self.resultado_label.config(text=mensagem)
        
        # Tenta carregar e exibir a imagem
        try:
            imagem = Image.open(resultado['imagem'])
            imagem = imagem.resize((100, 60), Image.LANCZOS)
            foto = ImageTk.PhotoImage(imagem)
            self.imagem_label.config(image=foto)
            self.imagem_label.image = foto
        except Exception as e:
            print(f"Erro ao carregar imagem: {e}")

def executar_via_terminal():
    validador = ValidadorCartao()
    
    print("=== Validador de Cartão de Crédito ===")
    print("\nExemplos de números para teste:")
    print("Visa: 4532715337901934")
    print("Mastercard: 5199999999999999")
    print("Amex: 341234567890123")
    
    while True:
        numero = input("\nDigite o número do cartão (ou 'sair' para encerrar): ")
        
        if numero.lower() == 'sair':
            break
            
        resultado = validador.validar_cartao(numero)
        print("\nResultado:")
        print(f"Bandeira: {resultado['bandeira']}")
        print(f"Válido: {'Sim' if resultado['valido'] else 'Não'}")
        print(f"Imagem: {resultado['imagem']}")
        print("-" * 40)

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == '--terminal':
        executar_via_terminal()
    else:
        if not os.path.exists('base'):
            os.makedirs('base')
        root = tk.Tk()
        app = ValidadorCartaoGUI(root)
        root.mainloop()