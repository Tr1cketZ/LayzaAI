# Pegando as coisas que a gente vai usar
import requests
import json

class Layza:
    def __init__(self, nome_aluno, materia, nivel_escolar):
        self.nome_aluno = nome_aluno
        self.materia = materia.lower()
        self.nivel_escolar = nivel_escolar.lower()  # Nível escolar do aluno
        self.api_key = "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"
        self.url = "https://openrouter.ai/api/v1/chat/completions"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        self.cache = {}
        self.historico = []  # Memória conversacional

    def _detectar_materia(self, texto):
        texto = texto.lower()
        if "portugues" in texto or "verbo" in texto or "substantivo" in texto or "frase" in texto:
            return "portugues"
        elif "matematica" in texto or "area" in texto or "quadrado" in texto or "numero" in texto:
            return "matematica"
        elif "ciencias" in texto or "dna" in texto or "proteína" in texto or "célula" in texto:
            return "ciencias"
        return None

    def _extrair_chave(self, texto):
        palavras = texto.lower().split()
        return palavras[-1] if palavras else "esse assunto"

    def _chamar_deepseek(self, prompt, max_tokens=1000):
        if prompt in self.cache:
            return self.cache[prompt]
        dados = json.dumps({
            "model": "deepseek/deepseek-chat-v3-0324:free",
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": max_tokens,
            "temperature": 1.0,  # Ajustado pra mais variação
        })
        resposta = requests.post(self.url, headers=self.headers, data=dados)
        if resposta.status_code == 200:
            resultado = resposta.json()
            try:
                texto = resultado["choices"][0]["message"]["content"].encode().decode('utf-8')
                self.cache[prompt] = texto
                return texto
            except KeyError:
                return f"Eita, {self.nome_aluno}, deu um probleminha na API!"
        else:
            return f"Opa, {self.nome_aluno}, erro {resposta.status_code} na API!"

    def ajudar_com_pergunta(self, pergunta):
        if not pergunta:
            print(f"Ei, {self.nome_aluno}, tu não perguntou nada!")
            return
        materia_errada = self._detectar_materia(pergunta)
        if materia_errada and materia_errada != self.materia:
            print(f"Ei, {self.nome_aluno}, essa pergunta parece de {materia_errada}, não de {self.materia}!")
            return
        chave = self._extrair_chave(pergunta)
        historico_str = "\n".join([f"Pergunta anterior: {h[0]}, Resposta: {h[1]}" for h in self.historico[-2:]]) if self.historico else "Sem histórico ainda."
        prompt = (
            f"Sou a Layza, de {self.materia}, ajudando um aluno de {self.nivel_escolar}. "
            f"Use o método socrático: faça uma ou duas perguntas reflexivas, curtas e diretas, adaptadas ao nível do aluno, "
            f"sem respostas prontas ou exemplos. Histórico recente:\n{historico_str}\n"
            f"Pergunta atual: '{pergunta}'. Foca em '{chave}'. Fala simples."
        )
        reflexoes = self._chamar_deepseek(prompt)
        print(f"\nSobre '{pergunta}': {reflexoes}\n")
        resposta_aluno = input(f"E aí, {self.nome_aluno}, o que tu acha? ")
        if resposta_aluno.lower() == "sair":
            return "sair"
        prompt_analise = (
            f"Sou a Layza, de {self.materia}, pra {self.nivel_escolar}. "
            f"Analisa a resposta do aluno: dá um feedback curto e específico, vê se tá no caminho certo, "
            f"e faz uma pergunta pra ir mais fundo ou ajustar. Se o aluno estiver muito perdido, dá uma dica sutil. "
            f"Pergunta: '{pergunta}'. Reflexões: '{reflexoes}'. Resposta: '{resposta_aluno}'. Foca em '{chave}'. Fala simples."
        )
        feedback = self._chamar_deepseek(prompt_analise)
        print(f"\nValeu, {self.nome_aluno}! {feedback}\n")
        self.historico.append((pergunta, resposta_aluno))

    def corrigir_prova(self, pergunta, resposta_aluno):
        if not pergunta or not resposta_aluno:
            print(f"Eita, {self.nome_aluno}, faltou a pergunta ou a resposta!")
            return
        materia_errada = self._detectar_materia(pergunta)
        if materia_errada and materia_errada != self.materia:
            print(f"Ei, {self.nome_aluno}, essa correção parece de {materia_errada}, não de {self.materia}!")
            return
        chave = self._extrair_chave(pergunta)
        prompt = (
            f"Sou a Layza, de {self.materia}, pra {self.nivel_escolar}. "
            f"Use o método socrático pra corrigir: analisa a resposta, aponta um ponto forte e um fraco, "
            f"e faz uma pergunta reflexiva pra cada, adaptada ao nível do aluno, sem corrigir ou dar exemplos. "
            f"Pergunta: '{pergunta}'. Resposta: '{resposta_aluno}'. Foca em '{chave}'. "
            f"Fala simples pro {self.nome_aluno}, usa '\n' e '\t' pra formatar."
        )
        reflexoes = self._chamar_deepseek(prompt)
        print(f"\nOlha tua prova, {self.nome_aluno}:\n"
              f"\nPergunta: {pergunta}\n"
              f"\nTua resposta: {resposta_aluno}\n"
              f"\n{reflexoes}\n")
        resposta_reflexao = input(f"E aí, {self.nome_aluno}, o que tu acha? ")
        if resposta_reflexao.lower() == "sair":
            return "sair"
        prompt_feedback = (
            f"Sou a Layza, de {self.materia}, pra {self.nivel_escolar}. "
            f"Analisa a resposta às reflexões: dá um feedback curto e específico, vê se tá no caminho certo, "
            f"e faz uma pergunta simples pra continuar. Se o aluno estiver muito perdido, dá uma dica sutil. "
            f"Pergunta: '{pergunta}'. Resposta inicial: '{resposta_aluno}'. Reflexões: '{reflexoes}'. "
            f"Resposta às reflexões: '{resposta_reflexao}'. Foca em '{chave}'. Fala simples."
        )
        feedback = self._chamar_deepseek(prompt_feedback)
        print(f"\nShow, {self.nome_aluno}! {feedback}\n")
        self.historico.append((pergunta, resposta_aluno))

class LayzaPortugues(Layza):
    def __init__(self, nome_aluno, nivel_escolar):
        super().__init__(nome_aluno, "portugues", nivel_escolar)
        print(f"\nE aí, {nome_aluno}! Sou a Layza de Português, bora curtir a língua?\n")

class LayzaMatematica(Layza):
    def __init__(self, nome_aluno, nivel_escolar):
        super().__init__(nome_aluno, "matematica", nivel_escolar)
        print(f"\nFala, {nome_aluno}! Sou a Layza de Matemática, bora resolver uns cálculos?\n")

class LayzaCiencias(Layza):
    def __init__(self, nome_aluno, nivel_escolar):
        super().__init__(nome_aluno, "ciencias", nivel_escolar)
        print(f"\nOpa, {nome_aluno}! Sou a Layza de Ciências, bora explorar o mundo?\n")

def interagir_com_layza():
    nome_aluno = input("Oi, tudo bem? Qual teu nome? ")
    print(f"\nLegal, {nome_aluno}! Eu sou a Layza, te ajudo a estudar de boa.\n")
    nivel_escolar = input("Qual teu nível escolar? (1° ano do ensino médio / 2° ano do ensino médio / 3° ano do ensino médio): ").strip().lower()  # Ajustado
    while True:
        materia = input("\nQual matéria tu quer? (português / matemática / ciências): ").strip().lower()
        if materia == "sair":
            confirma = input("Tem certeza que quer sair? (sim/não): ").strip().lower()
            if confirma == "sim":
                print(f"\nBeleza, {nome_aluno}, até mais!\n")
                return
            else:
                print("\nBeleza, vamos continuar então!\n")
                continue
        if "portugues" in materia or materia == "português":
            layza = LayzaPortugues(nome_aluno, nivel_escolar)
            break
        elif "matematica" in materia or materia == "matemática":
            layza = LayzaMatematica(nome_aluno, nivel_escolar)
            break
        elif "ciencias" in materia or materia == "ciências":
            layza = LayzaCiencias(nome_aluno, nivel_escolar)
            break
        else:
            print(f"\nEi, {nome_aluno}, escolhe direito: português, matemática ou ciências!\n")

    print(f"\nBeleza, {nome_aluno}, tu pode perguntar (1) ou corrigir uma prova (2). Pra sair, é só dizer 'sair'.\n")
    while True:
        escolha = input("O que tu quer fazer? (1 - Perguntar / 2 - Corrigir prova): ").strip().lower()
        if escolha == "sair":
            confirma = input("Tem certeza que quer sair? (sim/não): ").strip().lower()
            if confirma == "sim":
                print(f"\nFalou, {nome_aluno}! Valeu por estudar comigo!\n")
                break
            else:
                print("\nBeleza, vamos continuar então!\n")
                continue
        elif escolha == "1":
            pergunta = input("\nQual tua dúvida? ")
            if pergunta.lower() == "sair":
                confirma = input("Tem certeza que quer sair? (sim/não): ").strip().lower()
                if confirma == "sim":
                    print(f"\nFalou, {nome_aluno}! Valeu por estudar comigo!\n")
                    break
                else:
                    print("\nBeleza, vamos continuar então!\n")
                    continue
            sair = layza.ajudar_com_pergunta(pergunta)
            if sair == "sair":
                confirma = input("Tem certeza que quer sair? (sim/não): ").strip().lower()
                if confirma == "sim":
                    print(f"\nFalou, {nome_aluno}! Valeu por estudar comigo!\n")
                    break
                else:
                    print("\nBeleza, vamos continuar então!\n")
        elif escolha == "2":
            pergunta = input("\nQual foi a pergunta da prova? ")
            if pergunta.lower() == "sair":
                confirma = input("Tem certeza que quer sair? (sim/não): ").strip().lower()
                if confirma == "sim":
                    print(f"\nFalou, {nome_aluno}! Valeu por estudar comigo!\n")
                    break
                else:
                    print("\nBeleza, vamos continuar então!\n")
                    continue
            resposta_aluno = input("O que tu respondeu? ")
            if resposta_aluno.lower() == "sair":
                confirma = input("Tem certeza que quer sair? (sim/não): ").strip().lower()
                if confirma == "sim":
                    print(f"\nFalou, {nome_aluno}! Valeu por estudar comigo!\n")
                    break
                else:
                    print("\nBeleza, vamos continuar então!\n")
                    continue
            sair = layza.corrigir_prova(pergunta, resposta_aluno)
            if sair == "sair":
                confirma = input("Tem certeza que quer sair? (sim/não): ").strip().lower()
                if confirma == "sim":
                    print(f"\nFalou, {nome_aluno}! Valeu por estudar comigo!\n")
                    break
                else:
                    print("\nBeleza, vamos continuar então!\n")
        else:
            print(f"\nEi, {nome_aluno}, é 1 pra perguntar, 2 pra corrigir ou 'sair'!\n")

if __name__ == "__main__":
    interagir_com_layza()