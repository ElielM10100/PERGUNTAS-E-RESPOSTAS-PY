import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time
import random

class Pergunta:
    def __init__(self, pergunta, opcoes, resposta_correta):
        self.pergunta = pergunta
        self.opcoes = opcoes
        self.resposta_correta = resposta_correta

    def verificar_resposta(self, resposta):
        return resposta == self.resposta_correta

class JogoPerguntas:
    def __init__(self, perguntas):
        self.perguntas = perguntas
        self.pontuacao = 0
        self.pergunta_atual = 0
        self.tempo_restante = 15  # Ajuste o tempo aqui
        self.tempo_thread = None
        self.pedidos_ajuda = 0

    def iniciar_temporizador(self):
        self.tempo_thread = threading.Thread(target=self.atualizar_temporizador)
        self.tempo_thread.start()

    def atualizar_temporizador(self):
        while self.tempo_restante > 0:
            time.sleep(1)
            self.tempo_restante -= 1
            tempo_label.config(text=f"Tempo: {self.tempo_restante} s")

        self.mostrar_resposta("Tempo Esgotado! A resposta correta era:")
        self.pergunta_atual += 1

        if self.pergunta_atual < len(self.perguntas):
            self.mostrar_pergunta()
        else:
            self.mostrar_resposta(f"Fim do Jogo. Sua pontuação final é: {self.pontuacao}")

    def responder_pergunta(self, resposta):
        if self.tempo_thread and self.tempo_thread.is_alive():
            self.tempo_thread.join()

        pergunta_atual = self.perguntas[self.pergunta_atual]

        if pergunta_atual.verificar_resposta(resposta):
            self.pontuacao += 1

        self.pergunta_atual += 1

        if self.pergunta_atual < len(self.perguntas):
            self.mostrar_pergunta()
        else:
            self.mostrar_resposta(f"Fim do Jogo. Sua pontuação final é: {self.pontuacao}")

    def mostrar_pergunta(self):
        self.tempo_restante = 15  # Reinicia o tempo ao mostrar nova pergunta
        tempo_label.config(text=f"Tempo: {self.tempo_restante} s")
        self.iniciar_temporizador()

        pergunta_atual = self.perguntas[self.pergunta_atual]
        pergunta_label.config(text=pergunta_atual.pergunta)

        for i, opcao in enumerate(pergunta_atual.opcoes, start=1):
            opcoes_buttons[i - 1].config(text=opcao, state=tk.NORMAL, style='Opcao.TButton')  # Ativar botão
        ajuda_button.config(state=tk.NORMAL)  # Ativar botão de ajuda

    def pedir_ajuda(self):
        if self.pedidos_ajuda < 3:
            ajuda_label.config(text="Você pediu ajuda! Aqui está uma dica.")
            self.pedidos_ajuda += 1
        else:
            self.mostrar_resposta("Você usou muitas ajudas. Veja nosso anúncio:")
            self.exibir_anuncio()

    def exibir_anuncio(self):
        # Função para exibir anúncios. Aqui você pode personalizar a lógica
        messagebox.showinfo("Anúncio", "Agradecemos por usar nosso aplicativo! Este anúncio sustenta o app.")

    def mostrar_resposta(self, mensagem):
        resposta_correta = self.perguntas[self.pergunta_atual].resposta_correta
        mensagem_completa = f"{mensagem} {resposta_correta}"
        messagebox.showinfo("Resposta", mensagem_completa)

# Função chamada quando um botão de opção é pressionado
def responder(opcao):
    jogo.responder_pergunta(opcao)

# Função chamada quando o botão de ajuda é pressionado
def pedir_ajuda():
    jogo.pedir_ajuda()
    ajuda_button.config(state=tk.DISABLED)  # Desativar botão de ajuda após usá-lo

# Criando uma lista de perguntas (você pode adicionar mais perguntas)
perguntas = [
    Pergunta("Qual é a capital da França?", ["Paris", "Londres", "Berlim", "Madrid"], "1"),
    Pergunta("Quem escreveu 'Romeu e Julieta'?", ["Charles Dickens", "William Shakespeare", "Jane Austen", "Mark Twain"], "2"),
    Pergunta("Qual é o maior planeta do sistema solar?", ["Júpiter", "Saturno", "Marte", "Vênus"], "1"),
]

# Inicializando o jogo
jogo = JogoPerguntas(perguntas)

# Configurando a interface gráfica
root = tk.Tk()
root.title("Jogo de Perguntas e Respostas")
root.geometry("500x400")  # Ajustar o tamanho conforme necessário

# Adicionando um esquema de cores
root.configure(bg="#1E90FF")

# Estilo dos botões de opção
style = ttk.Style()
style.configure('Opcao.TButton', font=('Helvetica', 10), width=30, background="#FFD700")

# Criando widgets
pergunta_label = tk.Label(root, text="", font=("Helvetica", 12), bg="#1E90FF", fg="white")
pergunta_label.pack(pady=20)

opcoes_buttons = []
for i in range(4):
    opcao_button = ttk.Button(root, text="", style='Opcao.TButton', command=lambda i=i: responder(str(i + 1)))
    opcao_button.pack(pady=5)
    opcoes_buttons.append(opcao_button)

ajuda_button = ttk.Button(root, text="Pedir Ajuda", style='Opcao.TButton', command=pedir_ajuda)
ajuda_button.pack(pady=10)

ajuda_label = tk.Label(root, text="", font=("Helvetica", 10), bg="#1E90FF", fg="white")
ajuda_label.pack(pady=10)

tempo_label = tk.Label(root, text="Tempo: 15 s", font=("Helvetica", 10), bg="#1E90FF", fg="white")
tempo_label.pack(pady=10)

# Iniciando o jogo mostrando a primeira pergunta
jogo.mostrar_pergunta()

# Executando a interface gráfica
root.mainloop()
