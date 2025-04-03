import random
from datetime import datetime

class Layza:
    def __init__(self, nome_aluno):
        self.nome_aluno = nome_aluno
        self.preferencias = {"matematica": 0.8, "fisica": 0.6, "portugues": 0.4}
        self.desempenho = []
        self.historico = []
        self.feedbacks = []

    def adicionar_desempenho(self, disciplina, nota):
        self.desempenho.append({"disciplina": disciplina, "nota": nota})
        print(f"Nota {nota} adicionada em {disciplina}.")

    def analisar_perfil(self):
        if not self.desempenho:
            return {"preferencias": self.preferencias, "desempenho": "Sem dados"}
        media_notas = {}
        for registro in self.desempenho:
            disc = registro["disciplina"]
            nota = registro["nota"]
            if disc in media_notas:
                media_notas[disc] = (media_notas[disc] + nota) / 2
            else:
                media_notas[disc] = nota
        return {"preferencias": self.preferencias, "desempenho": media_notas}

    def recomendar_conteudo(self):
        perfil = self.analisar_perfil()
        disciplina = random.choice(list(self.preferencias.keys()))
        justificativa = f"Recomendo {disciplina} pelo seu interesse ({self.preferencias[disciplina]})"
        if disciplina in perfil["desempenho"]:
            justificativa += f" e média {perfil['desempenho'][disciplina]:.1f}."
        else:
            justificativa += " e falta de dados."
        recomendacao = f"Explore {disciplina} com 'Introdução a {disciplina}' (Khan Academy) para refletir sobre seus pontos fortes."
        self.historico.append(f"Recomendação: {recomendacao}")
        return {"recomendacao": recomendacao, "justificativa": justificativa}

    def gerar_relatorio_mensal(self):
        if not self.historico:
            return "Nenhuma interação registrada."
        limite = min(5, len(self.historico))
        relatorio = f"Relatório para {self.nome_aluno} ({datetime.now().strftime('%d/%m/%Y')}):\n"
        for i, item in enumerate(self.historico[-limite:], 1):
            relatorio += f"{i}. {item}\n"
        return relatorio

    def gerar_quiz(self, disciplina):
        quiz = [
            f"1. O que você entende por {disciplina}? Tente explicar com suas palavras.",
            f"2. Como {disciplina} se aplica no dia a dia? Pense em um exemplo.",
            f"3. Qual é um conceito básico de {disciplina} que você já conhece?",
            f"4. Por que estudar {disciplina} é importante para você?",
            f"5. Crie uma pergunta sobre {disciplina} e tente respondê-la sozinho."
        ]
        self.historico.append(f"Quiz gerado para {disciplina}")
        return "\n".join(quiz)

    def receber_feedback(self, gostei, mensagem=""):
        feedback = {"data": datetime.now(), "gostei": gostei, "mensagem": mensagem}
        self.feedbacks.append(feedback)
        return "Feedback registrado!"

    def responder_pergunta(self, pergunta):
        """Responde perguntas guiando o aluno, sem dar a resposta direta."""
        disciplina = next((d for d in self.preferencias.keys() if d in pergunta.lower()), "geral")
        resposta = f"Boa pergunta! Para refletir sobre '{pergunta}', pense: qual é o conceito principal envolvido? O que você já sabe sobre {disciplina} que pode ajudar? Tente dividir a questão em partes menores e me diga o que você acha!"
        self.historico.append(f"Pergunta: {pergunta} - Resposta guiada fornecida")
        return resposta

    def analisar_prova(self, texto_prova):
        """Simula análise de uma prova (texto por enquanto), sugerindo melhorias."""
        # Simulação: suponha que o texto contém uma pergunta e uma resposta do aluno
        linhas = texto_prova.split("\n")
        if len(linhas) < 2:
            return "Por favor, forneça uma pergunta e sua resposta para análise."
        
        pergunta = linhas[0].strip()
        resposta_aluno = linhas[1].strip()
        
        # Lógica simples para "analisar" (futuramente usaria OCR e regras mais complexas)
        feedback = f"Análise da sua prova:\nPergunta: {pergunta}\nSua resposta: {resposta_aluno}\n"
        if len(resposta_aluno) < 10:  # Exemplo de critério simples
            feedback += "Parece que sua resposta está muito curta. Tente explicar mais: quais passos você seguiu para chegar a essa conclusão? Que conceitos estão envolvidos?"
        else:
            feedback += "Sua resposta tem um bom tamanho! Reflita: você cobriu todos os pontos da pergunta? Que tal verificar se usou exemplos ou detalhes específicos para reforçar sua ideia?"
        feedback += "\nDica: Revisite o material de apoio ou me pergunte algo específico para melhorar!"
        
        self.historico.append(f"Análise de prova: {pergunta}")
        return feedback

    def executar(self):
        print(f"Olá, {self.nome_aluno}! Sou a Layza, sua assistente de estudos. Eu não dou respostas prontas, mas te ajudo a encontrar o caminho!")
        while True:
            print("\n1) Recomendações  2) Relatório  3) Quiz  4) Feedback  5) Adicionar nota  6) Fazer pergunta  7) Analisar prova  8) Sair")
            opcao = input("Escolha: ")
            if opcao == "1":
                resultado = self.recomendar_conteudo()
                print(f"Recomendação: {resultado['recomendacao']}")
                print(f"Justificativa: {resultado['justificativa']}")
            elif opcao == "2":
                print(self.gerar_relatorio_mensal())
            elif opcao == "3":
                disciplina = input("Disciplina (ex: matematica, fisica, portugues): ")
                print(self.gerar_quiz(disciplina))
            elif opcao == "4":
                gostei = input("Gostei (s/n)? ").lower() == "s"
                mensagem = input("Comentário (opcional): ")
                print(self.receber_feedback(gostei, mensagem))
            elif opcao == "5":
                disciplina = input("Disciplina: ")
                nota = float(input("Nota (0-100): "))
                self.adicionar_desempenho(disciplina, nota)
            elif opcao == "6":
                pergunta = input("Qual é a sua pergunta? ")
                print(self.responder_pergunta(pergunta))
            elif opcao == "7":
                texto_prova = input("Digite a pergunta da prova e sua resposta (uma por linha):\n")
                print(self.analisar_prova(texto_prova))
            elif opcao == "8":
                print("Até logo!")
                break
            else:
                print("Opção inválida.")

if __name__ == "__main__":
    ia = Layza("Maria")
    ia.executar()