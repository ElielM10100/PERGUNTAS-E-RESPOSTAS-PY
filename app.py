import tkinter as tk
from tkinter import messagebox
import threading
import time

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
        self.tempo_restante = 10
        self.tempo_thread = None

    def iniciar_temporizador(self):
        self.tempo_thread = threading.Thread(target=self.atualizar_temporizador)
        self.tempo_thread.start()

    def atualizar_temporizador(self):
        while self.tempo_restante > 0:
            time.sleep(1)
            self.tempo_restante -= 1
            tempo_label.config(text=f"Tempo: {self.tempo_restante} s")

        messagebox.showinfo("Tempo Esgotado", "Tempo esgotado! A resposta correta era: " +
                            self.perguntas[self.pergunta_atual].resposta_correta)
        self.pergunta_atual += 1

        if self.pergunta_atual < len(self.perguntas):
            self.mostrar_pergunta()
        else:
            messagebox.showinfo("Fim do Jogo", f"Sua pontuação final é: {self.pontuacao}")
            root.destroy()

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
            messagebox.showinfo("Fim do Jogo", f"Sua pontuação final é: {self.pontuacao}")
            root.destroy()

    def mostrar_pergunta(self):
        self.tempo_restante = 10
        tempo_label.config(text=f"Tempo: {self.tempo_restante} s")
        self.iniciar_temporizador()

        pergunta_atual = self.perguntas[self.pergunta_atual]
        pergunta_label.config(text=pergunta_atual.pergunta)

        for i, opcao in enumerate(pergunta_atual.opcoes, start=1):
            opcoes_buttons[i - 1].config(text=opcao)

# Função chamada quando um botão de opção é pressionado
def responder(opcao):
    jogo.responder_pergunta(opcao)

# Criando uma lista de perguntas
pergunta1 = Pergunta("Qual é a capital do Brasil?", ["Rio de Janeiro", "Brasília", "São Paulo", "Belo Horizonte"], "2")
pergunta2 = Pergunta("Quem foi o primeiro presidente dos Estados Unidos?", ["George Washington", "Abraham Lincoln", "Thomas Jefferson", "John F. Kennedy"], "1")
pergunta3 = Pergunta("Quantos planetas existem em nosso sistema solar?", ["7", "8", "9", "10"], "2")

perguntas = [pergunta1, pergunta2, pergunta3]

# Inicializando o jogo
jogo = JogoPerguntas(perguntas)

# Configurando a interface gráfica
root = tk.Tk()
root.title("Jogo de Perguntas e Respostas")

# Adicionando um esquema de cores
root.configure(bg="#1E90FF")
pergunta_label = tk.Label(root, text="", font=("Helvetica", 12), bg="#1E90FF", fg="white")
pergunta_label.pack(pady=20)

opcoes_buttons = []
for i in range(4):
    opcao_button = tk.Button(root, text="", font=("Helvetica", 10), width=30, command=lambda i=i: responder(str(i + 1)), bg="#FFD700")
    opcao_button.pack(pady=5)
    opcoes_buttons.append(opcao_button)

tempo_label = tk.Label(root, text="Tempo: 10 s", font=("Helvetica", 10), bg="#1E90FF", fg="white")
tempo_label.pack(pady=10)

# Iniciando o jogo mostrando a primeira pergunta
jogo.mostrar_pergunta()

# Executando a interface gráfica
root.mainloop()
