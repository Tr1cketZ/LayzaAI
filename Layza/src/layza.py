# Importando bibliotecas básicas
import random
from datetime import datetime

# Classe principal da IA Layza
class Layza:
    def __init__(self, nome_aluno):
        # Dados iniciais do aluno
        self.nome_aluno = nome_aluno
        self.preferencias = {"matematica": 0.8, "portugues": 0.6, "ciencias": 0.4}  # Só 3 matérias
        self.desempenho = []  # Lista pra guardar notas
        self.historico = []   # Guarda o que o aluno fez
        self.feedbacks = []   # Feedbacks do aluno

    def adicionar_nota(self, disciplina, nota):
        # Adiciona uma nota se a disciplina for válida
        if disciplina in self.preferencias:
            self.desempenho.append({"disciplina": disciplina, "nota": nota})
            print(f"Nota {nota} adicionada pra {disciplina}!")
        else:
            print("Erro: Disciplina errada. Use: matematica, portugues ou ciencias.")

    def ver_perfil(self):
        # Mostra como o aluno tá indo
        if len(self.desempenho) == 0:
            return {"preferencias": self.preferencias, "desempenho": "Sem notas ainda"}
        medias = {}
        for item in self.desempenho:
            disc = item["disciplina"]
            nota = item["nota"]
            if disc in medias:
                medias[disc] = (medias[disc] + nota) / 2  # Média simples
            else:
                medias[disc] = nota
        return {"preferencias": self.preferencias, "desempenho": medias}

    def dar_dica(self):
        # Dá uma dica de estudo baseada no perfil
        perfil = self.ver_perfil()
        disciplina = random.choice(list(self.preferencias.keys()))
        motivo = f"Escolhi {disciplina} porque você parece gostar ({self.preferencias[disciplina]})"
        if disciplina in perfil["desempenho"]:
            motivo += f" e sua média é {perfil['desempenho'][disciplina]}."
        else:
            motivo += " e ainda não tem nota."
        dica = f"Tenta estudar {disciplina} com o vídeo 'Introdução a {disciplina}' no Khan Academy. O que você acha disso?"
        self.historico.append(f"Dica: {dica}")
        return {"dica": dica, "motivo": motivo}

    def fazer_relatorio(self):
        # Mostra as últimas 5 coisas que o aluno fez
        if not self.historico:
            return "Nada aconteceu ainda."
        limite = 5 if len(self.historico) >= 5 else len(self.historico)
        relatorio = f"Relatório do {self.nome_aluno} ({datetime.now().strftime('%d/%m/%Y')}):\n"
        for i, coisa in enumerate(self.historico[-limite:], 1):
            relatorio += f"{i}. {coisa}\n"
        return relatorio

    def criar_quiz(self, disciplina):
        # Cria um quiz pra fazer o aluno pensar
        if disciplina not in self.preferencias:
            return "Ops! Só temos matematica, portugues e ciencias. Escolha uma dessas!"
        quiz = [
            f"1. O que é {disciplina} pra você? Explica com suas palavras.",
            f"2. Onde você usa {disciplina} no dia a dia? Dá um exemplo.",
            f"3. Qual ideia básica de {disciplina} você já sabe?",
            f"4. Por que acha que {disciplina} importa?",
            f"5. Faz uma pergunta sobre {disciplina} e tenta responder sozinho."
        ]
        self.historico.append(f"Quiz criado pra {disciplina}")
        return "\n".join(quiz)

    def guardar_feedback(self, gostei, comentario=""):
        # Salva o que o aluno achou
        feedback = {"data": datetime.now(), "gostei": gostei, "comentario": comentario}
        self.feedbacks.append(feedback)
        return "Valeu pelo feedback!"

    def ajudar_com_pergunta(self, pergunta):
        # Ajuda o aluno a pensar na resposta
        disciplina = "geral"
        for d in self.preferencias:
            if d in pergunta.lower():
                disciplina = d
                break
        ajuda = f"Ei, boa pergunta: '{pergunta}'! Vamos pensar juntos: qual é a ideia principal disso? O que você já sabe sobre {disciplina}? Tenta quebrar em pedaços menores e me conta!"
        self.historico.append(f"Pergunta: {pergunta} - Ajuda dada")
        return ajuda

    def corrigir_prova(self, texto_prova):
        # Corrige uma prova sem dar a resposta
        linhas = texto_prova.split("\n")
        if len(linhas) < 2:
            return "Falta algo! Digita a pergunta e sua resposta, uma por linha."
        
        pergunta = linhas[0].strip()
        resposta = linhas[1].strip()
        
        correcao = f"Olha sua prova:\nPergunta: {pergunta}\nSua resposta: {resposta}\n"
        if len(resposta) < 10:
            correcao += "Tá meio curto. Como você chegou nisso? Tenta explicar mais o que pensou!"
        else:
            correcao += "Certo, o texto está bom do ponto de vista legal! Será que ele aborda todos os aspectos solicitados na questão? Talvez valha a pena considerar a inclusão de um exemplo prático para ilustrar melhor."
        correcao += "\nDica: Analise seus documentos ou me questione para otimizar ainda mais.!"
        
        self.historico.append(f"Corrigi prova: {pergunta}")
        return correcao

    def menu(self):
        # Menu simples pra interagir
        print(f"Oi, {self.nome_aluno}! Sou Layza, tua companheira de estudos. Não te dou respostas prontas, mas caminho contigo na busca pelas tuas próprias descobertas.!")
        while True:
            print("\n1) Dica de estudo  2) Relatório  3) Quiz  4) Feedback  5) Adicionar nota  6) Perguntar  7) Corrigir prova  8) Sair")
            escolha = input("O que você quer fazer? ")
            if escolha == "1":
                resultado = self.dar_dica()
                print(f"Dica: {resultado['dica']}")
                print(f"Por que: {resultado['motivo']}")
            elif escolha == "2":
                print(self.fazer_relatorio())
            elif escolha == "3":
                disciplina = input("Qual matéria? (matematica, portugues, ciencias): ")
                print(self.criar_quiz(disciplina))
            elif escolha == "4":
                gostei = input("Gostou? (s/n): ").lower() == "s"
                comentario = input("Deixa um comentário (se quiser): ")
                print(self.guardar_feedback(gostei, comentario))
            elif escolha == "5":
                disciplina = input("Qual matéria? (matematica, portugues, ciencias): ")
                nota = float(input("Qual a nota (0-100)? "))
                self.adicionar_nota(disciplina, nota)
            elif escolha == "6":
                pergunta = input("Qual sua dúvida? ")
                print(self.ajudar_com_pergunta(pergunta))
            elif escolha == "7":
                texto_prova = input("Digite a pergunta e sua resposta (uma por linha):\n")
                print(self.corrigir_prova(texto_prova))
            elif escolha == "8":
                print("Tchau! Até a próxima!")
                break
            else:
                print("Escolha errada, tenta de novo!")

# Testando a IA
if __name__ == "__main__":
    aluno = Layza("João")
    aluno.menu()