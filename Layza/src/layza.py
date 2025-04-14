import requests
import json
import re
from typing import Dict, List, Optional
from datetime import datetime
from decouple import config

class Layza:
    def __init__(self, nome_aluno: str, materia: str, nivel_escolar: str, token: Optional[str] = None):
        self.nome_aluno = nome_aluno
        self.materia = materia.lower()
        self.nivel_escolar = nivel_escolar.lower()
        self.api_key = config("API_KEY")
        self.url = "https://openrouter.ai/api/v1/chat/completions"
        self.content_api = "http://mock-api.layza.com/contents"  # API de conteúdos (mock)
        self.progress_api = "http://mock-api.layza.com/progress"  # API de progresso (mock)
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://layza-educacional.com",
            "X-Title": "Layza Educacional",
        }
        self.token = token  # JWT do usuário
        self.user_data = self._validate_token() if token else {"role": "aluno", "preferences": {}}
        self.cache = {}
        self.historico = []

    def _validate_token(self) -> Dict:
        """Valida JWT via API simulada (RF05, RF13)."""
        try:
            response = requests.get(
                "http://mock-api.layza.com/validate",
                headers={"Authorization": f"Bearer {self.token}"},
                timeout=1,  # RNF04: <1s
            )
            if response.status_code == 200:
                data = response.json()
                return {
                    "role": data.get("role", "aluno"),
                    "preferences": data.get("preferences", {"visual": False, "auditivo": False, "leitura": False}),
                }
            return {"role": "aluno", "preferences": {}}
        except requests.RequestException:
            print(f"Eita, {self.nome_aluno}, problema no token! Usando modo aluno.")
            return {"role": "aluno", "preferences": {}}

    def _detectar_materia(self, texto: str) -> Optional[str]:
        """Detecta matéria com base no texto (RF19)."""
        texto = texto.lower()
        if any(word in texto for word in ["portugues", "verbo", "substantivo", "frase"]):
            return "portugues"
        elif any(word in texto for word in ["matematica", "area", "quadrado", "numero"]):
            return "matematica"
        elif any(word in texto for word in ["ciencias", "dna", "proteína", "célula"]):
            return "ciencias"
        return None

    def _extrair_chave(self, texto: str) -> str:
        """Extrai palavra-chave da pergunta."""
        palavras = texto.lower().split()
        return palavras[-1] if palavras else "esse assunto"

    def _get_user_preferences(self) -> Dict:
        """Retorna preferências do usuário (RF15-RF17)."""
        return self.user_data.get("preferences", {"visual": False, "auditivo": False, "leitura": False})

    def _chamar_deepseek(self, prompt: str, max_tokens: int = 1000) -> str:
        """Chama API OpenRouter com cache e timeout (RNF07)."""
        if not self.api_key:
            return f"Eita, {self.nome_aluno}, a chave da API tá faltando!"
        if prompt in self.cache:
            return self.cache[prompt]
        try:
            dados = {
                "model": "deepseek/deepseek-chat",
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": max_tokens,
                "temperature": 1.0,
            }
            response = requests.post(self.url, headers=self.headers, json=dados, timeout=10)
            if response.status_code == 200:
                result = response.json()
                try:
                    texto = result["choices"][0]["message"]["content"]
                    self.cache[prompt] = texto
                    return texto
                except (KeyError, IndexError):
                    return f"Eita, {self.nome_aluno}, a API mandou um formato estranho!"
            elif response.status_code == 401:
                return f"Opa, {self.nome_aluno}, a chave da API tá inválida! Pede uma nova no OpenRouter."
            elif response.status_code == 429:
                return f"Eita, {self.nome_aluno}, limite da API atingido! Tenta mais tarde."
            else:
                return f"Opa, {self.nome_aluno}, erro {response.status_code}: {response.text[:100]}..."
        except requests.Timeout:
            return f"Eita, {self.nome_aluno}, a API demorou muito! Tenta de novo."
        except requests.RequestException as e:
            return f"Eita, {self.nome_aluno}, erro na conexão: {str(e)}!"

    def _consultar_conteudos(self, tema: str, tipo: Optional[str] = None) -> List[Dict]:
        """Consulta conteúdos via API mock (RF19-RF21)."""
        try:
            params = {"tema": tema}
            if tipo:
                params["tipo"] = tipo
            response = requests.get(self.content_api, params=params, timeout=2)  # RNF06
            if response.status_code == 200:
                return response.json()
            return []
        except requests.RequestException:
            return []

    def _salvar_progresso(self, tema: str, concluido: bool, acertos: Optional[float] = None) -> bool:
        """Salva progresso via API mock (RF28)."""
        try:
            dados = {
                "user": self.nome_aluno,
                "tema": tema,
                "concluido": concluido,
                "acertos": acertos,
                "timestamp": datetime.now().isoformat(),
            }
            response = requests.post(self.progress_api, json=dados, timeout=3)  # RNF08
            return response.status_code == 200
        except requests.RequestException:
            return False

    def _recomendar_conteudo(self, tema: str) -> str:
        """Recomenda conteúdo com base em preferências (RF23-RF25)."""
        preferences = self._get_user_preferences()
        tipo_preferido = "texto"
        if preferences.get("visual"):
            tipo_preferido = "vídeo"
        elif preferences.get("auditivo"):
            tipo_preferido = "áudio"
        
        conteudos = self._consultar_conteudos(tema, tipo_preferido)
        if conteudos:
            conteudo = conteudos[0]
            justificativa = f"Indicado para seu estilo {tipo_preferido.lower()}"
            return f"Recomendo: {conteudo['titulo']} ({conteudo['tipo']}). {justificativa}."
        return f"Nenhum conteúdo encontrado para {tema}. Que tal perguntar mais sobre isso?"

    def ajudar_com_pergunta(self, pergunta: str) -> Optional[str]:
        """Ajuda com dúvida usando método socrático e recomendações (RF22-RF25)."""
        if not pergunta:
            print(f"Ei, {self.nome_aluno}, tu não perguntou nada!")
            return None
        materia_errada = self._detectar_materia(pergunta)
        if materia_errada and materia_errada != self.materia:
            print(f"Ei, {self.nome_aluno}, essa pergunta parece de {materia_errada}, não de {self.materia}!")
            return None
        
        chave = self._extrair_chave(pergunta)
        historico_str = "\n".join([f"Pergunta: {h[0]}, Resposta: {h[1]}" for h in self.historico[-2:]]) or "Sem histórico."
        preferences = self._get_user_preferences()
        pref_str = ", ".join([k for k, v in preferences.items() if v]) or "nenhuma preferência definida"
        
        prompt = (
            f"Sou a Layza, de {self.materia}, para {self.nivel_escolar}. "
            f"Use o método socrático: faça 1-2 perguntas reflexivas, curtas, adaptadas ao nível, "
            f"sem respostas prontas. Considere preferências: {pref_str}. "
            f"Histórico:\n{historico_str}\nPergunta atual: '{pergunta}'. Foca em '{chave}'. Fala simples."
        )
        reflexoes = self._chamar_deepseek(prompt)
        print(f"\nSobre '{pergunta}': {reflexoes}\n")
        
        resposta_aluno = input(f"E aí, {self.nome_aluno}, o que tu acha? ")
        if resposta_aluno.lower() == "sair":
            return "sair"
        
        prompt_analise = (
            f"Sou a Layza, de {self.materia}, para {self.nivel_escolar}. "
            f"Analisa a resposta do aluno: dá feedback curto, vê se tá no caminho certo, "
            f"e faz uma pergunta pra ir mais fundo. Se perdido, dá dica sutil. "
            f"Pergunta: '{pergunta}'. Reflexões: '{reflexoes}'. Resposta: '{resposta_aluno}'. "
            f"Foca em '{chave}'. Fala simples."
        )
        feedback = self._chamar_deepseek(prompt_analise)
        print(f"\nValeu, {self.nome_aluno}! **Feedback:** {feedback}\n")
        
        # Recomendação de conteúdo (RF25)
        recomendacao = self._recomendar_conteudo(chave)
        print(f"\n{recomendacao}\n")
        
        # Salvar progresso (RF28)
        self._salvar_progresso(self.materia, True)
        
        return None

    def corrigir_prova(self, pergunta: str, resposta_aluno: str) -> Optional[str]:
        """Corrige prova com método socrático (RF12, RF18)."""
        if not pergunta or not resposta_aluno:
            print(f"Eita, {self.nome_aluno}, faltou pergunta ou resposta!")
            return None
        materia_errada = self._detectar_materia(pergunta)
        if materia_errada and materia_errada != self.materia:
            print(f"Ei, {self.nome_aluno}, parece de {materia_errada}, não de {self.materia}!")
            return None
        
        if self.user_data["role"] != "aluno" and self.user_data["role"] != "administrador":
            print(f"Eita, {self.nome_aluno}, só alunos ou admins corrigem provas!")
            return None
        
        chave = self._extrair_chave(pergunta)
        prompt = (
            f"Sou a Layza, de {self.materia}, para {self.nivel_escolar}. "
            f"Use método socrático: analisa a resposta, aponta 1 ponto forte e 1 fraco, "
            f"faz uma pergunta reflexiva pra cada, sem corrigir. "
            f"Pergunta: '{pergunta}'. Resposta: '{resposta_aluno}'. Foca em '{chave}'. Fala simples."
        )
        reflexoes = self._chamar_deepseek(prompt)
        print(
            f"\nOlha tua prova, {self.nome_aluno}:\n"
            f"\nPergunta: {pergunta}\n"
            f"\nTua resposta: {resposta_aluno}\n"
            f"\n{reflexoes}\n"
        )
        
        resposta_reflexao = input(f"E aí, {self.nome_aluno}, o que tu acha? ")
        if resposta_reflexao.lower() == "sair":
            return "sair"
        
        prompt_feedback = (
            f"Sou a Layza, de {self.materia}, para {self.nivel_escolar}. "
            f"Analisa a resposta às reflexões: feedback curto, vê se tá no caminho, "
            f"faz pergunta simples pra continuar. Se perdido, dá dica sutil. "
            f"Pergunta: '{pergunta}'. Resposta inicial: '{resposta_aluno}'. "
            f"Reflexões: '{reflexoes}'. Resposta às reflexões: '{resposta_reflexao}'. "
            f"Foca em '{chave}'. Fala simples."
        )
        feedback = self._chamar_deepseek(prompt_feedback)
        print(f"\nShow, {self.nome_aluno}! **Feedback:** {feedback}\n")
        
        # Avaliação do conteúdo (RF26)
        nota = input(f"Que nota (1-5) tu dá pra esse conteúdo? ")
        try:
            nota = int(nota)
            if 1 <= nota <= 5:
                comentario = input("Quer deixar um comentário? (opcional, até 500 caracteres): ")[:500]
                # Enviar avaliação para API (mock)
                requests.post(
                    "http://mock-api.layza.com/ratings",
                    json={"user": self.nome_aluno, "nota": nota, "comentario": comentario},
                    timeout=2,
                )
        except ValueError:
            print("Nota inválida, pulando avaliação.")
        
        # Salvar progresso (RF28)
        self._salvar_progresso(self.materia, True, acertos=0.8)  # Mock acertos
        
        return None

class LayzaPortugues(Layza):
    def __init__(self, nome_aluno: str, nivel_escolar: str, token: Optional[str] = None):
        super().__init__(nome_aluno, "portugues", nivel_escolar, token)
        print(f"\nE aí, {nome_aluno}! Sou a Layza de Português, bora curtir a língua?\n")

class LayzaMatematica(Layza):
    def __init__(self, nome_aluno: str, nivel_escolar: str, token: Optional[str] = None):
        super().__init__(nome_aluno, "matematica", nivel_escolar, token)
        print(f"\nFala, {nome_aluno}! Sou a Layza de Matemática, bora resolver uns cálculos?\n")

class LayzaCiencias(Layza):
    def __init__(self, nome_aluno: str, nivel_escolar: str, token: Optional[str] = None):
        super().__init__(nome_aluno, "ciencias", nivel_escolar, token)
        print(f"\nOpa, {nome_aluno}! Sou a Layza de Ciências, bora explorar o mundo?\n")

def interagir_com_layza():
    nome_aluno = input("Oi, tudo bem? Qual teu nome? ")
    print(f"\nLegal, {nome_aluno}! Eu sou a Layza, te ajudo a estudar de boa.\n")
    nivel_escolar = input("Qual teu nível escolar? (ex.: 1° ano do ensino médio): ").strip().lower()
    token = input("Qual teu token de acesso? (deixe vazio pra teste): ").strip() or None
    
    while True:
        materia = input("\nQual matéria tu quer? (português / matemática / ciências): ").strip().lower()
        if materia == "sair":
            confirma = input("Tem certeza que quer sair? (sim/não): ").strip().lower()
            if confirma == "sim":
                print(f"\nBeleza, {nome_aluno}, até mais!\n")
                return
            continue
        if "portugues" in materia:
            layza = LayzaPortugues(nome_aluno, nivel_escolar, token)
            break
        elif "matematica" in materia:
            layza = LayzaMatematica(nome_aluno, nivel_escolar, token)
            break
        elif "ciencias" in materia:
            layza = LayzaCiencias(nome_aluno, nivel_escolar, token)
            break
        print(f"\nEi, {nome_aluno}, escolhe direito: português, matemática ou ciências!\n")
    
    print(f"\nBeleza, {nome_aluno}, tu pode perguntar (1) ou corrigir uma prova (2). Pra sair, é só dizer 'sair'.\n")
    while True:
        escolha = input("O que tu quer fazer? (1 - Perguntar / 2 - Corrigir prova): ").strip().lower()
        if escolha == "sair":
            confirma = input("Tem certeza que quer sair? (sim/não): ").strip().lower()
            if confirma == "sim":
                print(f"\nFalou, {nome_aluno}! Valeu por estudar comigo!\n")
                break
            continue
        elif escolha == "1":
            pergunta = input("\nQual tua dúvida? ")
            if pergunta.lower() == "sair":
                confirma = input("Tem certeza que quer sair? (sim/não): ").strip().lower()
                if confirma == "sim":
                    print(f"\nFalou, {nome_aluno}! Valeu por estudar comigo!\n")
                    break
                continue
            result = layza.ajudar_com_pergunta(pergunta)
            if result == "sair":
                confirma = input("Tem certeza que quer sair? (sim/não): ").strip().lower()
                if confirma == "sim":
                    print(f"\nFalou, {nome_aluno}! Valeu por estudar comigo!\n")
                    break
                continue
        elif escolha == "2":
            pergunta = input("\nQual foi a pergunta da prova? ")
            if pergunta.lower() == "sair":
                confirma = input("Tem certeza que quer sair? (sim/não): ").strip().lower()
                if confirma == "sim":
                    print(f"\nFalou, {nome_aluno}! Valeu por estudar comigo!\n")
                    break
                continue
            resposta_aluno = input("O que tu respondeu? ")
            if resposta_aluno.lower() == "sair":
                confirma = input("Tem certeza que quer sair? (sim/não): ").strip().lower()
                if confirma == "sim":
                    print(f"\nFalou, {nome_aluno}! Valeu por estudar comigo!\n")
                    break
                continue
            result = layza.corrigir_prova(pergunta, resposta_aluno)
            if result == "sair":
                confirma = input("Tem certeza que quer sair? (sim/não): ").strip().lower()
                if confirma == "sim":
                    print(f"\nFalou, {nome_aluno}! Valeu por estudar comigo!\n")
                    break
                continue
        else:
            print(f"\nEi, {nome_aluno}, é 1 pra perguntar, 2 pra corrigir ou 'sair'!\n")

if __name__ == "__main__":
    interagir_com_layza()