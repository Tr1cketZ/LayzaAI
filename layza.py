# Pegando as coisas que a gente vai usar
import requests
import json

class Layza:
    def __init__(self, nome_aluno, materia):
        # Oi, eu sou a Layza! Guardo o nome e a matéria que você escolheu
        self.nome_aluno = nome_aluno
        self.materia = materia.lower()  # Tudo minúsculo pra facilitar
        self.api_key = "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"  # Minha chave pra API
        self.url = "https://openrouter.ai/api/v1/chat/completions"  # Onde eu falo com a IA
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        self.cache = {}  # Um lugar pra guardar respostas e não ficar chamando a API toda hora

    def _detectar_materia(self, texto):
        # Tento adivinhar a matéria olhando pras palavras
        texto = texto.lower()
        if "portugues" in texto or "verbo" in texto or "substantivo" in texto or "frase" in texto:
            return "portugues"
        elif "matematica" in texto or "area" in texto or "quadrado" in texto or "numero" in texto:
            return "matematica"
        elif "ciencias" in texto or "dna" in texto or "proteína" in texto or "célula" in texto:
            return "ciencias"
        return None  # Se não achar, deixa vazio

    def _extrair_chave(self, texto):
        # Pego a última palavra pra focar em algo legal
        palavras = texto.lower().split()
        return palavras[-1] if palavras else "esse assunto"

    def _chamar_deepseek(self, prompt, max_tokens=1000):
        # Se eu já tenho essa resposta, não chamo a API de novo
        if prompt in self.cache:
            return self.cache[prompt]

        # Preparo os dados pra mandar pra API
        dados = json.dumps({
            "model": "deepseek/deepseek-chat-v3-0324:free",
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": max_tokens,  # 1000 pra caber textos grandes
            "temperature": 0.7,  # Deixo assim pra não ficar muito louco
        })

        # Tento falar com a API
        resposta = requests.post(self.url, headers=self.headers, data=dados)
        if resposta.status_code == 200:  # Deu certo?
            resultado = resposta.json()
            try:
                texto = resultado["choices"][0]["message"]["content"].encode().decode('utf-8')  # Pego o texto com acentos certinhos
                self.cache[prompt] = texto  # Guardo pra usar depois
                return texto
            except KeyError:
                return f"Eita, {self.nome_aluno}, deu um probleminha na resposta da API!"
        else:
            return f"Opa, {self.nome_aluno}, erro {resposta.status_code} na API. Vamos tentar de novo?"

    def ajudar_com_pergunta(self, pergunta):
        # Se não tiver pergunta, aviso o aluno
        if not pergunta:
            print(f"Ei, {self.nome_aluno}, você não perguntou nada! Qual é a tua dúvida?")
            return

        # Checo se a pergunta é da matéria certa
        materia_errada = self._detectar_materia(pergunta)
        if materia_errada and materia_errada != self.materia:
            print(f"Ei, {self.nome_aluno}, essa pergunta parece de {materia_errada}, não de {self.materia}. "
                  f"Tenta a Layza de {materia_errada}!")
            return

        chave = self._extrair_chave(pergunta)
        # Pergunto pro DeepSeek de um jeito socrático
        prompt = (
            f"Sou a Layza, especialista em {self.materia}. "
            f"Use o método socrático: só perguntas reflexivas, nada de respostas prontas ou exemplos. "
            f"A pergunta é: '{pergunta}'. Foca na palavra '{chave}'. "
            f"Fala simples e amigável pro {self.nome_aluno}, com quebras de linha pra separar ideias."
        )

        reflexoes = self._chamar_deepseek(prompt)
        print(f"\nEi, {self.nome_aluno}, sobre '{pergunta}'!\n\n{reflexoes}\n")

        # Peço pro aluno responder
        resposta_aluno = input(f"Beleza, {self.nome_aluno}, o que tu acha disso? ")
        prompt_analise = (
            f"Sou a Layza, de {self.materia}. "
            f"Analisa a resposta do aluno: não corrige nem dá resposta, só vê se tá no caminho certo. "
            f"Se sim, pergunta pra ele ir mais fundo. Se não, sugere reflexões pra ajustar. "
            f"Pergunta: '{pergunta}'. Reflexões: '{reflexoes}'. Resposta: '{resposta_aluno}'. "
            f"Foca em '{chave}'. Fala simples pro {self.nome_aluno}, com quebras de linha pra separar ideias."
        )

        feedback = self._chamar_deepseek(prompt_analise)
        print(f"\nShow, {self.nome_aluno}!\n\n{feedback}\n")

    def corrigir_prova(self, pergunta, resposta_aluno):
        # Se faltar algo, aviso logo
        if not pergunta or not resposta_aluno:
            print(f"Eita, {self.nome_aluno}, faltou a pergunta ou a resposta!")
            return

        materia_errada = self._detectar_materia(pergunta)
        if materia_errada and materia_errada != self.materia:
            print(f"Ei, {self.nome_aluno}, essa pergunta parece de {materia_errada}, não de {self.materia}. "
                  f"Tenta a Layza de {materia_errada}!")
            return

        chave = self._extrair_chave(pergunta)
        # Junto tudo numa chamada só pra ir rápido, com formatação
        prompt = (
            f"Sou a Layza, de {self.materia}. "
            f"Use o método socrático pra corrigir: "
            f"1. Faz perguntas reflexivas pra repensar a resposta, sem exemplos prontos. "
            f"2. Analisa a resposta: acha pontos fortes (o que tá legal) e fracos (o que tá confuso), sem corrigir. "
            f"Pontos fortes: pergunta pra ir mais fundo. Pontos fracos: sugere reflexões pra ajustar. "
            f"Pergunta: '{pergunta}'. Resposta: '{resposta_aluno}'. Foca em '{chave}'. "
            f"Fala simples e amigável pro {self.nome_aluno}. "
            f"Formata assim:\n"
            f"- Usa '\n' pra parágrafos.\n"
            f"- Usa '\t' pra indentar pontos fortes e fracos.\n"
            f"- Separa bem cada ideia pra ficar claro."
        )

        reflexoes = self._chamar_deepseek(prompt)
        # Formato a saída com espaçamentos
        print(f"\nOlha tua prova, {self.nome_aluno}:\n"
              f"\nPergunta: {pergunta}\n"
              f"\nTua resposta: {resposta_aluno}\n"
              f"\n{reflexoes}\n")

        # Peço o que o aluno achou
        resposta_reflexao = input(f"E aí, {self.nome_aluno}, o que tu acha disso? ")
        prompt_feedback = (
            f"Sou a Layza, de {self.materia}. "
            f"Analisa a resposta às reflexões: vê se tá no caminho certo, sem corrigir ou dar respostas. "
            f"Se sim, pergunta pra aprofundar. Se não, sugere reflexões pra ajustar. "
            f"Pergunta: '{pergunta}'. Resposta inicial: '{resposta_aluno}'. Reflexões: '{reflexoes}'. "
            f"Resposta às reflexões: '{resposta_reflexao}'. Foca em '{chave}'. "
            f"Fala simples pro {self.nome_aluno}, com '\n' pra parágrafos e '\t' pra indentar ideias."
        )

        feedback = self._chamar_deepseek(prompt_feedback)
        print(f"\nDemais, {self.nome_aluno}!\n\n{feedback}\n")

# Cada matéria tem sua Layza
class LayzaPortugues(Layza):
    def __init__(self, nome_aluno):
        super().__init__(nome_aluno, "portugues")
        print(f"\nE aí, {self.nome_aluno}! Bem-vindo à Layza de Português, vamos curtir a língua juntos!\n")

class LayzaMatematica(Layza):
    def __init__(self, nome_aluno):
        super().__init__(nome_aluno, "matematica")
        print(f"\nFala, {self.nome_aluno}! Bem-vindo à Layza de Matemática, bora resolver uns cálculos irados!\n")

class LayzaCiencias(Layza):
    def __init__(self, nome_aluno):
        super().__init__(nome_aluno, "ciencias")
        print(f"\nOpa, {self.nome_aluno}! Bem-vindo à Layza de Ciências, vamos explorar o mundo juntos!\n")

# Parte que roda no terminal
def interagir_com_layza():
    nome_aluno = input("Oi, tudo bem? Qual teu nome? ")
    print(f"\nLegal, {nome_aluno}! Eu sou a Layza, te ajudo a estudar de boa.\n")

    # Lista de matérias válidas
    materias_validas = ["portugues", "matematica", "ciencias"]

    while True:
        materia = input("Qual matéria tu quer? (português / matemática / ciências ou 'sair' pra desistir): ").strip().lower()
        # Se digitar 'sair', para tudo
        if materia == "sair":
            print(f"\nBeleza, {nome_aluno}, até mais!\n")
            return  # Sai da função inteira

        # Aceita variações com acento ou sem
        if "portugues" in materia or materia == "português":
            layza = LayzaPortugues(nome_aluno)
            break
        elif "matematica" in materia or materia == "matemática":
            layza = LayzaMatematica(nome_aluno)
            break
        elif "ciencias" in materia or materia == "ciências":
            layza = LayzaCiencias(nome_aluno)
            break
        else:
            print(f"\nEi, {nome_aluno}, escolhe direito: português, matemática ou ciências!\n")

    print("Beleza, tu pode perguntar algo ou corrigir uma prova. Só dizer 'sair' pra parar!\n")

    while True:
        escolha = input("O que tu quer fazer? (1 - Perguntar / 2 - Corrigir prova / sair): ").strip().lower()
        print()  # Linha em branco pra separar
        if escolha == "sair":
            print(f"Falou, {nome_aluno}! Valeu por estudar comigo!\n")
            break
        elif escolha == "1":
            pergunta = input("Qual tua dúvida? ")
            layza.ajudar_com_pergunta(pergunta)
        elif escolha == "2":
            pergunta = input("Qual foi a pergunta da prova? ")
            resposta_aluno = input("O que tu respondeu? ")
            layza.corrigir_prova(pergunta, resposta_aluno)
        else:
            print(f"Ei, {nome_aluno}, é 1 pra perguntar, 2 pra corrigir ou 'sair'!\n")

if __name__ == "__main__":
    interagir_com_layza()