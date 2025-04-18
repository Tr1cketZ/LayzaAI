import requests
import re
import logging
import os
import sqlite3
from typing import Dict, Optional, List, Tuple
from datetime import datetime
from dotenv import load_dotenv
from unidecode import unidecode

logging.basicConfig(filename="layza.log", level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
load_dotenv()

class APIClient:
    def __init__(self, api_key: str, nome_aluno: str):
        self.api_key = api_key
        self.nome_aluno = nome_aluno
        self.url = "https://openrouter.ai/api/v1/chat/completions"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://layza-educacional.com",
            "X-Title": "Layza Educacional",
        }
        self.cache = {}

    def chamar(self, prompt: str) -> str:
        if prompt in self.cache:
            logging.info("Resposta do cache")
            return self.cache[prompt]
        try:
            response = requests.post(
                self.url,
                headers=self.headers,
                json={"model": "deepseek/deepseek-chat", "messages": [{"role": "user", "content": prompt}], "temperature": 0.7},
                timeout=10
            )
            response.raise_for_status()
            texto = response.json()["choices"][0]["message"]["content"]
            self.cache[prompt] = texto
            logging.info("Resposta da API")
            return texto
        except (requests.RequestException, KeyError, IndexError) as e:
            logging.error(f"Erro na API: {str(e)}")
            return f"Eita, {self.nome_aluno}, a API tá com problema! Tenta outra pergunta?"

class HistoricoManager:
    def __init__(self, materia: str):
        self.db_file = f"historico_{materia}.db"
        with sqlite3.connect(self.db_file) as conn:
            conn.execute("CREATE TABLE IF NOT EXISTS historico (id INTEGER PRIMARY KEY, aluno TEXT, pergunta TEXT, resposta TEXT, timestamp TEXT)")

    def salvar(self, aluno: str, pergunta: str, resposta: str):
        try:
            with sqlite3.connect(self.db_file) as conn:
                conn.execute("INSERT INTO historico (aluno, pergunta, resposta, timestamp) VALUES (?, ?, ?, ?)",
                            (aluno, pergunta, resposta, datetime.now().isoformat()))
                conn.commit()
        except sqlite3.Error as e:
            logging.error(f"Erro ao salvar histórico: {str(e)}")

    def carregar(self, aluno: str, limit: int = 2) -> List[Tuple[str, str]]:
        try:
            with sqlite3.connect(self.db_file) as conn:
                return conn.execute("SELECT pergunta, resposta FROM historico WHERE aluno = ? ORDER BY timestamp DESC LIMIT ?",
                                  (aluno, limit)).fetchall()
        except sqlite3.Error as e:
            logging.error(f"Erro ao carregar histórico: {str(e)}")
            return []

class Layza:
    def __init__(self, nome_aluno: str, materia: str, nivel_escolar: str, token: Optional[str] = None):
        self.nome_aluno = nome_aluno
        self.materia = materia.lower()
        self.nivel_escolar = nivel_escolar.lower()
        api_key = os.getenv("OPENROUTER_API_KEY") or (logging.error("Chave API não encontrada") or exit(1))
        self.api_client = APIClient(api_key, nome_aluno)
        self.historico = HistoricoManager(self.materia)
        self.content_api = "http://mock-api.layza.com/contents"
        self.progress_api = "http://mock-api.layza.com/progress"
        self.token = token
        self.user_data = self._validate_token() if token else {"role": "aluno", "preferences": {}}
        self.exemplos = {
            "matematica": "potência em juros, área, progressões",
            "portugues": "análise de textos, gramática, figuras de linguagem",
            "ciencias": "reações químicas, energia, ecossistemas"
        }
        print(f"\nE aí, {nome_aluno}! Sou a Layza de {materia.capitalize()}, bora estudar pro ENEM?\n")

    def _validar_entrada(self, texto: str) -> Optional[str]:
        texto = re.sub(r'[^\w\s?!.,]', '', texto.strip())[:500]
        return texto if texto and len(texto) >= 3 else None

    def _validate_token(self) -> Dict:
        try:
            response = requests.get(f"{self.content_api}/validate", headers={"Authorization": f"Bearer {self.token}"}, timeout=1)
            response.raise_for_status()
            data = response.json()
            return {"role": data.get("role", "aluno"), "preferences": data.get("preferences", {})}
        except requests.RequestException:
            print(f"Eita, {self.nome_aluno}, problema no token! Usando modo aluno.")
            return {"role": "aluno", "preferences": {}}

    def _detectar_materia(self, texto: str) -> Optional[str]:
        texto = unidecode(texto.lower())
        if any(w in texto for w in ["portugues", "verbo", "frase"]): return "portugues"
        if any(w in texto for w in ["matematica", "elevado", "numero"]): return "matematica"
        if any(w in texto for w in ["ciencias", "dna", "celula"]): return "ciencias"
        return None

    def _extrair_chave(self, texto: str) -> str:
        palavras = [p for p in re.sub(r'[^\w\s]', '', texto.lower()).split() if p not in {"o", "que", "é", "a", "de", "em"} and len(p) > 2]
        return palavras[-1] if palavras else self.materia

    def _resposta_local_matematica(self, pergunta: str) -> Optional[str]:
        match = re.match(r"quanto é (\d+) elevado a (\d+)", pergunta.lower())
        if match:
            base, expoente = map(int, match.groups())
            return f"{base} elevado a {expoente} é {base ** expoente}."
        return None

    def _get_prompt(self, tipo: str, **kwargs) -> str:
        base = f"Sou a Layza, de {self.materia}, para {self.nivel_escolar}, ajudando pro ENEM. Fala como colega, foca em '{kwargs.get('chave', self.materia)}'."
        if tipo == "pergunta":
            return f"{base} Faça 1-2 perguntas curtas pra ajudar o aluno a entender {self.materia} com exemplos práticos ({self.exemplos[self.materia]}). Histórico: {kwargs['historico']}. Pergunta: '{kwargs['pergunta']}'."
        if tipo == "feedback":
            return f"{base} Analisa a resposta: feedback curto, vê se tá certo, faz 1 pergunta pra avançar. Se confuso, explica com exemplo ({self.exemplos[self.materia]}). Pergunta: '{kwargs['pergunta']}'. Reflexões: '{kwargs['reflexoes']}'. Resposta: '{kwargs['resposta']}'."
        if tipo == "simples":
            return f"{base} Explica '{kwargs['pergunta']}' bem simples, com exemplo de {self.materia} ({self.exemplos[self.materia]}). Histórico: '{kwargs['resposta']}'."
        if tipo == "técnica":
            return f"{base} Explica '{kwargs['pergunta']}' tecnicamente, com conceitos avançados de {self.materia} ({self.exemplos[self.materia]}), fórmulas se aplicável. Histórico: '{kwargs['resposta']}'."
        if tipo == "prova":
            return f"{base} Analisa a resposta: 1 ponto forte, 1 fraco, 1 pergunta pra cada, sem corrigir. Exemplo: {self.exemplos[self.materia]}. Pergunta: '{kwargs['pergunta']}'. Resposta: '{kwargs['resposta']}'."

    def _tratar_confusao(self, pergunta: str, resposta_aluno: str, chave: str) -> Dict:
        esclarecer = input(f"Ei, {self.nome_aluno}, tá perdido? Quer explicação simples, técnica, outra dúvida ou sair? ").strip().lower()
        if esclarecer == "sair":
            return {"status": "sair"}
        if esclarecer == "outra":
            return self.ajudar_com_pergunta(input("Qual tua nova dúvida? "))
        tipo = "simples" if esclarecer == "simples" else "técnica"
        prompt = self._get_prompt(tipo, pergunta=pergunta, resposta=resposta_aluno, chave=chave)
        explicacao = self.api_client.chamar(prompt)
        print(f"\nBeleza, {self.nome_aluno}, aqui vai uma explicação {tipo}:\n{explicacao}\n")
        if input(f"Agora tá de boa? (sim/não): ").lower() != "sim":
            print(f"Sem estresse! Quer continuar nessa dúvida ou tentar outra?")
            opcao = input("(continuar/outra/sair): ").lower()
            if opcao == "outra":
                return self.ajudar_com_pergunta(input("Qual tua nova dúvida? "))
            if opcao == "sair":
                return {"status": "sair"}
        return {"status": "continuar"}

    def _recomendar_conteudo(self, tema: str) -> str:
        tipo = "vídeo" if self.user_data.get("preferences", {}).get("visual") else "áudio" if self.user_data.get("preferences", {}).get("auditivo") else "texto"
        try:
            response = requests.get(self.content_api, params={"tema": tema, "tipo": tipo}, timeout=2)
            response.raise_for_status()
            conteudos = response.json()
            return f"Recomendo: {conteudos[0]['titulo']} ({conteudos[0]['tipo']}). Perfeito pro teu estilo!" if conteudos else f"Não achei nada sobre {tema}."
        except requests.RequestException:
            logging.warning(f"Sem conteúdos para {tema}")
            return f"Não achei nada sobre {tema}."

    def _salvar_progresso(self, tema: str):
        try:
            requests.post(self.progress_api, json={"user": self.nome_aluno, "tema": tema, "concluido": True, "timestamp": datetime.now().isoformat()}, timeout=3)
        except requests.RequestException as e:
            logging.error(f"Erro ao salvar progresso: {str(e)}")

    def ajudar_com_pergunta(self, pergunta: str, continuar: bool = False) -> Dict:
        pergunta = self._validar_entrada(pergunta)
        if not pergunta:
            print(f"Ei, {self.nome_aluno}, pergunta algo mais claro!")
            return {"status": "erro"}
        
        if self._detectar_materia(pergunta) not in [None, self.materia]:
            print(f"Ei, {self.nome_aluno}, isso parece outra matéria! Quer mudar?")
            return {"status": "erro"}

        if self.materia == "matematica" and (local := self._resposta_local_matematica(pergunta)):
            print(f"\nSobre '{pergunta}': {local}\n")
            self._salvar_progresso(self.materia)
            self.historico.salvar(self.nome_aluno, pergunta, "respondido localmente")
            return {"status": "sucesso", "resposta": local}

        chave = self._extrair_chave(pergunta)
        historico = "\n".join(f"Pergunta: {p}, Resposta: {r}" for p, r in self.historico.carregar(self.nome_aluno)) or "Sem histórico."
        reflexoes = ""
        if not continuar:
            prompt = self._get_prompt("pergunta", pergunta=pergunta, chave=chave, historico=historico)
            reflexoes = self.api_client.chamar(prompt)
            print(f"\nE aí, {self.nome_aluno}, bora falar sobre '{pergunta}'?\n{reflexoes}\n")

        while True:
            resposta_aluno = self._validar_entrada(input(f"E aí, {self.nome_aluno}, o que tu acha? "))
            if not resposta_aluno or resposta_aluno.lower() == "sair":
                return {"status": "sair"}
            
            confusao = any(t in resposta_aluno.lower() for t in ["não sei", "confuso", "explica", "sla"])
            prompt = self._get_prompt("feedback", pergunta=pergunta, reflexoes=reflexoes, resposta=resposta_aluno, chave=chave)
            feedback = self.api_client.chamar(prompt)
            print(f"\nValeu, {self.nome_aluno}! {feedback}\n")
            
            if confusao:
                result = self._tratar_confusao(pergunta, resposta_aluno, chave)
                if result["status"] != "continuar":
                    return result
            else:
                print(f"\n{self._recomendar_conteudo(chave)}\n")
                self._salvar_progresso(self.materia)
                self.historico.salvar(self.nome_aluno, pergunta, resposta_aluno)
                opcao = input(f"Beleza, {self.nome_aluno}! Continuar nessa dúvida ou outra? (continuar/outra/sair): ").lower()
                if opcao == "outra":
                    return self.ajudar_com_pergunta(input("Qual tua nova dúvida? "))
                if opcao == "sair":
                    return {"status": "sair"}

    def corrigir_prova(self, pergunta: str, resposta_aluno: str) -> Dict:
        pergunta = self._validar_entrada(pergunta)
        resposta_aluno = self._validar_entrada(resposta_aluno)
        if not (pergunta and resposta_aluno):
            print(f"Eita, {self.nome_aluno}, pergunta ou resposta tá vaga!")
            return {"status": "erro"}
        
        if self._detectar_materia(pergunta) not in [None, self.materia]:
            print(f"Ei, {self.nome_aluno}, parece outra matéria!")
            return {"status": "erro"}
        
        if self.user_data["role"] not in ["aluno", "administrador"]:
            print(f"Eita, {self.nome_aluno}, só alunos ou admins corrigem provas!")
            return {"status": "erro"}

        chave = self._extrair_chave(pergunta)
        prompt = self._get_prompt("prova", pergunta=pergunta, resposta=resposta_aluno, chave=chave)
        reflexoes = self.api_client.chamar(prompt)
        print(f"\nOlha tua prova, {self.nome_aluno}:\nPergunta: {pergunta}\nTua resposta: {resposta_aluno}\n{reflexoes}\n")

        resposta_reflexao = self._validar_entrada(input(f"E aí, {self.nome_aluno}, o que tu acha? "))
        if not resposta_reflexao or resposta_reflexao.lower() == "sair":
            return {"status": "sair"}

        prompt = self._get_prompt("feedback", pergunta=pergunta, reflexoes=reflexoes, resposta=resposta_reflexao, chave=chave)
        feedback = self.api_client.chamar(prompt)
        print(f"\nValeu, {self.nome_aluno}! {feedback}\n")

        try:
            nota = int(input(f"Nota de 1 a 5 pro conteúdo? "))
            if 1 <= nota <= 5:
                comentario = input("Comentário? (opcional, até 500 caracteres): ")[:500]
                requests.post(f"{self.content_api}/ratings", json={"user": self.nome_aluno, "nota": nota, "comentario": comentario}, timeout=2)
        except (ValueError, requests.RequestException):
            print("Nota inválida ou erro, pulando avaliação.")

        self._salvar_progresso(self.materia)
        self.historico.salvar(self.nome_aluno, pergunta, resposta_aluno)
        return {"status": "sucesso", "reflexoes": reflexoes, "feedback": feedback}

def interagir_com_layza():
    nome_aluno = input("Oi, tudo bem? Qual teu nome? ").strip() or "aluno"
    print(f"\nLegal, {nome_aluno}! Eu sou a Layza, te ajudo a estudar pro ENEM.\n")
    nivel_escolar = input("Qual teu nível escolar? (ex.: 2° ano): ").strip().lower() or "ensino médio"
    token = input("Token de acesso? (vazio pra teste): ").strip() or None

    materias = {
        "portugues": ["portugues", "português", "port", "pt"],
        "matematica": ["matematica", "matemática", "mat", "math"],
        "ciencias": ["ciencias", "ciências", "cie"]
    }

    while True:
        materia = input("\nQual matéria? (português/matemática/ciências): ").strip().lower()
        if materia == "sair" and input("Sair? (sim/não): ").lower() == "sim":
            print(f"\nBeleza, {nome_aluno}, até mais!\n")
            return
        materia_key = next((k for k, v in materias.items() if unidecode(materia) in v), None)
        if materia_key:
            break
        print(f"\nEi, {nome_aluno}, escolhe: português, matemática ou ciências!\n")

    layza = Layza(nome_aluno, materia_key, nivel_escolar, token)
    print(f"\nBeleza, {nome_aluno}, tu pode perguntar (1) ou corrigir prova (2). Pra sair, diz 'sair'.\n")

    tentativas_invalidas = 0
    while True:
        escolha = input("O que quer fazer? (1 - Perguntar / 2 - Corrigir prova): ").lower()
        if escolha == "sair" and input("Sair? (sim/não): ").lower() == "sim":
            print(f"\nFalou, {nome_aluno}! Valeu por estudar comigo!\n")
            break
        if escolha == "1":
            tentativas_invalidas = 0
            pergunta = input("\nQual tua dúvida? ")
            if pergunta.lower() == "sair" and input("Sair? (sim/não): ").lower() == "sim":
                print(f"\nFalou, {nome_aluno}! Valeu!\n")
                break
            if layza.ajudar_com_pergunta(pergunta).get("status") == "sair":
                print(f"\nFalou, {nome_aluno}! Valeu!\n")
                break
        elif escolha == "2":
            tentativas_invalidas = 0
            pergunta = input("\nQual a pergunta da prova? ")
            if pergunta.lower() == "sair" and input("Sair? (sim/não): ").lower() == "sim":
                print(f"\nFalou, {nome_aluno}! Valeu!\n")
                break
            resposta = input("O que tu respondeu? ")
            if resposta.lower() == "sair" and input("Sair? (sim/não): ").lower() == "sim":
                print(f"\nFalou, {nome_aluno}! Valeu!\n")
                break
            if layza.corrigir_prova(pergunta, resposta).get("status") == "sair":
                print(f"\nFalou, {nome_aluno}! Valeu!\n")
                break
        else:
            tentativas_invalidas += 1
            if tentativas_invalidas >= 5:
                print(f"\nEi, {nome_aluno}, tá digitando qualquer coisa! Até mais!\n")
                break
            print(f"\nEi, é 1 pra perguntar, 2 pra corrigir ou 'sair'! Tenta de novo.\n")

if __name__ == "__main__":
    try:
        interagir_com_layza()
    except KeyboardInterrupt:
        print("\nTá de boa, parece que tu quis parar! Até a próxima!")
        logging.info("Interrompido pelo usuário")