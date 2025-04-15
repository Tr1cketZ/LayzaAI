import requests
import json
import re
import logging
import os
from typing import Dict, List, Optional
from datetime import datetime
from dotenv import load_dotenv
from unidecode import unidecode

# Configurar logging
logging.basicConfig(filename="layza.log", level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Carregar variáveis de ambiente
load_dotenv()

class Layza:
    def __init__(self, nome_aluno: str, materia: str, nivel_escolar: str, token: Optional[str] = None):
        self.nome_aluno = nome_aluno
        self.materia = materia.lower()
        self.nivel_escolar = nivel_escolar.lower()
        self.api_key = os.getenv("OPENROUTER_API_KEY")
        if not self.api_key:
            msg = "Erro: Chave OPENROUTER_API_KEY não encontrada no .env!"
            logging.error(msg)
            raise ValueError(msg)
        self.url = "https://openrouter.ai/api/v1/chat/completions"
        self.content_api = "http://mock-api.layza.com/contents"
        self.progress_api = "http://mock-api.layza.com/progress"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://layza-educacional.com",
            "X-Title": "Layza Educacional",
        }
        self.token = token
        self.user_data = self._validate_token() if token else {"role": "aluno", "preferences": {}}
        self.cache = {}
        self.historico_file = f"historico_{self.materia}.json"
        self.historico = self._carregar_historico()
        logging.info(f"Inicializado Layza para {nome_aluno}, matéria {materia}")

    def _carregar_historico(self) -> List:
        """Carrega o histórico da matéria do arquivo JSON."""
        try:
            if os.path.exists(self.historico_file):
                with open(self.historico_file, 'r', encoding='utf-8') as f:
                    historico = json.load(f)
                    logging.info(f"Histórico carregado de {self.historico_file}")
                    return historico
            return []
        except (json.JSONDecodeError, IOError) as e:
            logging.error(f"Erro ao carregar histórico: {str(e)}")
            return []

    def _salvar_historico(self):
        """Salva o histórico da matéria no arquivo JSON."""
        try:
            with open(self.historico_file, 'w', encoding='utf-8') as f:
                json.dump(self.historico, f, ensure_ascii=False, indent=2)
            logging.info(f"Histórico salvo em {self.historico_file}")
        except IOError as e:
            logging.error(f"Erro ao salvar histórico: {str(e)}")

    def _validate_token(self) -> Dict:
        """Valida JWT via API simulada (RF05, RF13)."""
        logging.info(f"Validando token para {self.nome_aluno}")
        try:
            response = requests.get(
                "http://mock-api.layza.com/validate",
                headers={"Authorization": f"Bearer {self.token}"},
                timeout=1,
            )
            if response.status_code == 200:
                data = response.json()
                result = {
                    "role": data.get("role", "aluno"),
                    "preferences": data.get("preferences", {"visual": False, "auditivo": False, "leitura": False}),
                    **{k: v for k, v in data.items() if k not in ["role", "preferences"]}
                }
                logging.info(f"Token validado: {result}")
                return result
            logging.warning(f"Token inválido para {self.nome_aluno}, usando padrão")
            return {"role": "aluno", "preferences": {}}
        except requests.RequestException as e:
            msg = f"Eita, {self.nome_aluno}, problema no token! Usando modo aluno."
            print(msg)
            logging.error(f"Erro na validação do token: {str(e)}")
            return {"role": "aluno", "preferences": {}}

    def _detectar_materia(self, texto: str) -> Optional[str]:
        """Detecta matéria com base no texto (RF19)."""
        texto = unidecode(texto.lower())
        if any(word in texto for word in ["portugues", "verbo", "substantivo", "frase"]):
            return "portugues"
        elif any(word in texto for word in ["matematica", "elevado", "potencia", "calculo", "numero"]):
            return "matematica"
        elif any(word in texto for word in ["ciencias", "carbono", "dna", "proteina", "celula"]):
            return "ciencias"
        return None

    def _extrair_chave(self, texto: str) -> str:
        """Extrai palavra-chave relevante da pergunta."""
        stopwords = {"o", "que", "é", "a", "um", "uma", "de", "em", "para", "com", "no", "na", "quanto"}
        texto = re.sub(r'[^\w\s]', '', texto.lower())
        palavras = [p for p in texto.split() if p not in stopwords and len(p) > 2]
        return palavras[-1] if palavras else self.materia

    def _get_user_preferences(self) -> Dict:
        """Retorna preferências do usuário (RF15-RF17)."""
        return self.user_data.get("preferences", {"visual": False, "auditivo": False, "leitura": False})

    def _chamar_deepseek(self, prompt: str, max_tokens: int = 1000) -> str:
        """Chama API OpenRouter com cache e timeout (RNF07)."""
        logging.info(f"Chamando API OpenRouter para prompt: {prompt[:50]}...")
        if prompt in self.cache:
            logging.info("Resposta obtida do cache")
            return self.cache[prompt]
        try:
            dados = {
                "model": "deepseek/deepseek-chat",
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": max_tokens,
                "temperature": 0.7,
            }
            response = requests.post(self.url, headers=self.headers, json=dados, timeout=10)
            if response.status_code == 200:
                result = response.json()
                try:
                    texto = result["choices"][0]["message"]["content"]
                    self.cache[prompt] = texto
                    logging.info("Resposta recebida da API")
                    return texto
                except (KeyError, IndexError):
                    msg = f"Eita, {self.nome_aluno}, a API mandou algo errado!"
                    print(msg)
                    logging.error(msg)
                    return msg
            elif response.status_code == 401:
                msg = f"Opa, {self.nome_aluno}, a chave da API tá inválida! Verifica no .env."
                print(msg)
                logging.error(f"Erro 401: {response.text}")
                return msg
            elif response.status_code == 429:
                msg = f"Eita, {self.nome_aluno}, limite da API atingido! Tenta depois."
                print(msg)
                logging.error(msg)
                return msg
            else:
                msg = f"Opa, {self.nome_aluno}, erro {response.status_code}: {response.text[:100]}..."
                print(msg)
                logging.error(msg)
                return msg
        except requests.Timeout:
            msg = f"Eita, {self.nome_aluno}, a API demorou demais! Tenta de novo."
            print(msg)
            logging.error(msg)
            return msg
        except requests.RequestException as e:
            msg = f"Eita, {self.nome_aluno}, erro na conexão: {str(e)}!"
            print(msg)
            logging.error(f"Erro na API: {str(e)}")
            return msg

    def _consultar_conteudos(self, tema: str, tipo: Optional[str] = None) -> List[Dict]:
        """Consulta conteúdos via API mock (RF19-RF21)."""
        logging.info(f"Consultando conteúdos para tema: {tema}, tipo: {tipo}")
        try:
            params = {"tema": tema}
            if tipo:
                params["tipo"] = tipo
            response = requests.get(self.content_api, params=params, timeout=2)
            if response.status_code == 200:
                logging.info("Conteúdos recebidos")
                return response.json()
            logging.warning(f"Sem conteúdos para tema: {tema}")
            return []
        except requests.RequestException as e:
            logging.error(f"Erro ao consultar conteúdos: {str(e)}")
            return []

    def _salvar_progresso(self, tema: str, concluido: bool, acertos: Optional[float] = None) -> bool:
        """Salva progresso via API mock (RF28)."""
        logging.info(f"Salvando progresso para {self.nome_aluno}, tema: {tema}")
        try:
            dados = {
                "user": self.nome_aluno,
                "tema": tema,
                "concluido": concluido,
                "acertos": acertos,
                "timestamp": datetime.now().isoformat(),
            }
            response = requests.post(self.progress_api, json=dados, timeout=3)
            success = response.status_code == 200
            logging.info(f"Progresso salvo: {success}")
            return success
        except requests.RequestException as e:
            logging.error(f"Erro ao salvar progresso: {str(e)}")
            return False

    def _recomendar_conteudo(self, tema: str) -> str:
        """Recomenda conteúdo com base em preferências (RF23-RF25)."""
        if not tema or tema == "assunto":
            logging.warning("Tema inválido, usando matéria")
            tema = self.materia
        preferences = self._get_user_preferences()
        tipo_preferido = "texto"
        if preferences.get("visual"):
            tipo_preferido = "vídeo"
        elif preferences.get("auditivo"):
            tipo_preferido = "áudio"
        
        conteudos = self._consultar_conteudos(tema, tipo_preferido)
        if conteudos:
            conteudo = conteudos[0]
            return f"Recomendo: {conteudo['titulo']} ({conteudo['tipo']}). Perfeito pro teu estilo de estudar!"
        return f"Não achei nada sobre {tema}. Quer saber mais sobre isso?"

    def ajudar_com_pergunta(self, pergunta: str) -> Dict:
        """Ajuda com dúvida usando perguntas reflexivas e recomendações (RF22-RF25)."""
        logging.info(f"Processando pergunta de {self.nome_aluno}: {pergunta}")
        if not pergunta or len(pergunta.strip()) < 3:
            msg = f"Ei, {self.nome_aluno}, pergunta algo mais claro!"
            print(msg)
            logging.warning(msg)
            return {"status": "erro", "mensagem": msg}
        materia_errada = self._detectar_materia(pergunta)
        if materia_errada and materia_errada != self.materia:
            msg = f"Ei, {self.nome_aluno}, isso parece {materia_errada}, não {self.materia}! Quer mudar de matéria?"
            print(msg)
            logging.warning(msg)
            return {"status": "erro", "mensagem": msg}
        
        chave = self._extrair_chave(pergunta)
        historico_str = "\n".join([f"Pergunta: {h[0]}, Resposta: {h[1]}" for h in self.historico[-2:]]) or "Sem histórico."
        preferences = self._get_user_preferences()
        pref_str = ", ".join([k for k, v in preferences.items() if v]) or "sem preferências"
        
        exemplos_materia = {
            "matematica": "ex.: potência em cálculos de juros, área de figuras, progressões",
            "portugues": "ex.: análise de textos, gramática em redações, figuras de linguagem",
            "ciencias": "ex.: reações químicas, energia, ecossistemas"
        }
        prompt = (
            f"Sou a Layza, de {self.materia}, para {self.nivel_escolar}, ajudando adolescentes do ensino médio pro ENEM. "
            f"Use o método socrático: faça 1-2 perguntas reflexivas, curtas, focadas em {self.materia}, sem respostas prontas. "
            f"Use exemplos práticos de {self.materia} ({exemplos_materia[self.materia]}), sem mencionar outras matérias. "
            f"Considere preferências: {pref_str}. Histórico:\n{historico_str}\nPergunta atual: '{pergunta}'. "
            f"Foca em '{chave}'. Fala direto, como um colega explicando pro ENEM."
        )
        reflexoes = self._chamar_deepseek(prompt)
        print(f"\nSobre '{pergunta}': {reflexoes}\n")
        
        resposta_aluno = input(f"E aí, {self.nome_aluno}, o que tu acha? ").strip()
        if resposta_aluno.lower() == "sair":
            logging.info(f"{self.nome_aluno} escolheu sair")
            return {"status": "sair"}
        
        confusao = any(termo in resposta_aluno.lower() for termo in ["não sei", "não entendi", "confuso", "explica", "simples", "sla"])
        prompt_analise = (
            f"Sou a Layza, de {self.materia}, para {self.nivel_escolar}, ajudando adolescentes do ensino médio pro ENEM. "
            f"Analisa a resposta do aluno: dá feedback curto e direto, vê se tá no caminho certo, e faz uma pergunta pra avançar. "
            f"Se confuso, explica {self.materia} com exemplo prático ({exemplos_materia[self.materia]}), sem outras matérias. "
            f"Pergunta: '{pergunta}'. Reflexões: '{reflexoes}'. Resposta: '{resposta_aluno}'. "
            f"Foca em '{chave}'. Fala como um colega pro ENEM."
        )
        feedback = self._chamar_deepseek(prompt_analise)
        print(f"\nValeu, {self.nome_aluno}! **Feedback:** {feedback}\n")
        
        if confusao:
            esclarecer = input(f"Ei, {self.nome_aluno}, tá meio perdido? Quer uma explicação mais simples ou outra dúvida? (simples/outra/sair): ").strip().lower()
            if esclarecer == "simples":
                prompt_esclarecer = (
                    f"Sou a Layza, de {self.materia}, para {self.nivel_escolar}, ajudando adolescentes do ensino médio pro ENEM. "
                    f"O aluno tá confuso com '{pergunta}'. Explica de forma bem simples, com exemplo prático de {self.materia} "
                    f"({exemplos_materia[self.materia]}), sem mencionar outras matérias. "
                    f"Histórico: '{resposta_aluno}'. Foca em '{chave}'. Fala direto, como um colega pro ENEM."
                )
                nova_explicacao = self._chamar_deepseek(prompt_esclarecer)
                print(f"\nBeleza, {self.nome_aluno}, vou te explicar de um jeito mais simples:\n{nova_explicacao}\n")
                entendeu = input(f"Agora tá de boa, {self.nome_aluno}? (sim/não): ").strip().lower()
                if entendeu != "sim":
                    print(f"Sem estresse, {self.nome_aluno}! Quer tentar outra pergunta ou continuar nessa?")
                    continuar = input("(outra/continuar/sair): ").strip().lower()
                    if continuar == "outra":
                        nova_pergunta = input("Qual tua nova dúvida? ")
                        return self.ajudar_com_pergunta(nova_pergunta)
                    elif continuar == "sair":
                        return {"status": "sair"}
            elif esclarecer == "outra":
                nova_pergunta = input("Qual tua nova dúvida? ")
                return self.ajudar_com_pergunta(nova_pergunta)
            elif esclarecer == "sair":
                return {"status": "sair"}
        
        recomendacao = self._recomendar_conteudo(chave)
        print(f"\n{recomendacao}\n")
        
        self._salvar_progresso(self.materia, True)
        self.historico.append((pergunta, resposta_aluno))
        self._salvar_historico()
        
        return {
            "status": "sucesso",
            "reflexoes": reflexoes,
            "feedback": feedback,
            "recomendacao": recomendacao
        }

    def corrigir_prova(self, pergunta: str, resposta_aluno: str) -> Dict:
        """Corrige prova com perguntas reflexivas (RF12, RF18)."""
        logging.info(f"Corrigindo prova de {self.nome_aluno}: {pergunta}")
        if not pergunta or not resposta_aluno or len(pergunta.strip()) < 3 or len(resposta_aluno.strip()) < 3:
            msg = f"Eita, {self.nome_aluno}, pergunta ou resposta tá muito vaga! Tenta algo mais claro."
            print(msg)
            logging.warning(msg)
            return {"status": "erro", "mensagem": msg}
        materia_errada = self._detectar_materia(pergunta)
        if materia_errada and materia_errada != self.materia:
            msg = f"Ei, {self.nome_aluno}, parece {materia_errada}, não {self.materia}! Quer mudar?"
            print(msg)
            logging.warning(msg)
            return {"status": "erro", "mensagem": msg}
        
        if self.user_data["role"] != "aluno" and self.user_data["role"] != "administrador":
            msg = f"Eita, {self.nome_aluno}, só alunos ou admins corrigem provas!"
            print(msg)
            logging.warning(msg)
            return {"status": "erro", "mensagem": msg}
        
        chave = self._extrair_chave(pergunta)
        exemplos_materia = {
            "matematica": "ex.: potência em cálculos de juros, área de figuras, progressões",
            "portugues": "ex.: análise de textos, gramática em redações, figuras de linguagem",
            "ciencias": "ex.: reações químicas, energia, ecossistemas"
        }
        prompt = (
            f"Sou a Layza, de {self.materia}, para {self.nivel_escolar}, ajudando adolescentes do ensino médio pro ENEM. "
            f"Use método socrático: analisa a resposta, aponta 1 ponto forte e 1 fraco, faz uma pergunta reflexiva pra cada, sem corrigir. "
            f"Use exemplos práticos de {self.materia} ({exemplos_materia[self.materia]}), sem outras matérias. "
            f"Pergunta: '{pergunta}'. Resposta: '{resposta_aluno}'. Foca em '{chave}'. Fala direto, como um colega pro ENEM."
        )
        reflexoes = self._chamar_deepseek(prompt)
        print(
            f"\nOlha tua prova, {self.nome_aluno}:\n"
            f"\nPergunta: {pergunta}\n"
            f"\nTua resposta: {resposta_aluno}\n"
            f"\n{reflexoes}\n"
        )
        
        resposta_reflexao = input(f"E aí, {self.nome_aluno}, o que tu acha? ").strip()
        if resposta_reflexao.lower() == "sair":
            logging.info(f"{self.nome_aluno} escolheu sair")
            return {"status": "sair"}
        
        prompt_feedback = (
            f"Sou a Layza, de {self.materia}, para {self.nivel_escolar}, ajudando adolescentes do ensino médio pro ENEM. "
            f"Analisa a resposta às reflexões: feedback curto, vê se tá no caminho, faz pergunta simples pra continuar. "
            f"Se confuso, dá dica prática de {self.materia} ({exemplos_materia[self.materia]}), sem outras matérias. "
            f"Pergunta: '{pergunta}'. Resposta inicial: '{resposta_aluno}'. "
            f"Reflexões: '{reflexoes}'. Resposta às reflexões: '{resposta_reflexao}'. "
            f"Foca em '{chave}'. Fala direto, como um colega pro ENEM."
        )
        feedback = self._chamar_deepseek(prompt_feedback)
        print(f"\nValeu, {self.nome_aluno}! **Feedback:** {feedback}\n")
        
        nota = None
        try:
            nota_input = input(f"Que nota (1-5) tu dá pra esse conteúdo? ").strip()
            nota = int(nota_input)
            if 1 <= nota <= 5:
                comentario = input("Quer deixar um comentário? (opcional, até 500 caracteres): ")[:500]
                requests.post(
                    "http://mock-api.layza.com/ratings",
                    json={"user": self.nome_aluno, "nota": nota, "comentario": comentario},
                    timeout=2,
                )
            else:
                print("Nota fora do intervalo, pulando avaliação.")
        except ValueError:
            print("Nota inválida, pulando avaliação.")
        
        self._salvar_progresso(self.materia, True, acertos=0.8)
        self.historico.append((pergunta, resposta_aluno))
        self._salvar_historico()
        
        return {
            "status": "sucesso",
            "reflexoes": reflexoes,
            "feedback": feedback,
            "nota": nota
        }

class LayzaPortugues(Layza):
    def __init__(self, nome_aluno: str, nivel_escolar: str, token: Optional[str] = None):
        super().__init__(nome_aluno, "portugues", nivel_escolar, token)
        print(f"\nE aí, {nome_aluno}! Sou a Layza de Português, bora mandar bem na redação pro ENEM?\n")

class LayzaMatematica(Layza):
    def __init__(self, nome_aluno: str, nivel_escolar: str, token: Optional[str] = None):
        super().__init__(nome_aluno, "matematica", nivel_escolar, token)
        print(f"\nFala, {nome_aluno}! Sou a Layza de Matemática, bora resolver uns cálculos pro ENEM?\n")

class LayzaCiencias(Layza):
    def __init__(self, nome_aluno: str, nivel_escolar: str, token: Optional[str] = None):
        super().__init__(nome_aluno, "ciencias", nivel_escolar, token)
        print(f"\nOpa, {nome_aluno}! Sou a Layza de Ciências, bora entender o mundo pro ENEM?\n")

def interagir_com_layza():
    nome_aluno = input("Oi, tudo bem? Qual teu nome? ").strip()
    if not nome_aluno:
        nome_aluno = "aluno"
    print(f"\nLegal, {nome_aluno}! Eu sou a Layza, te ajudo a estudar de boa pro ENEM.\n")
    nivel_escolar = input("Qual teu nível escolar? (ex.: 2° ano do ensino médio): ").strip().lower() or "ensino médio"
    token = input("Qual teu token de acesso? (deixe vazio pra teste): ").strip() or None
    
    materias_validas = {
        "portugues": ["portugues", "português", "portugu", "port", "pt", "portuguez"],
        "matematica": ["matematica", "matemática", "mat", "math", "matem", "matematic"],
        "ciencias": ["ciencias", "ciências", "ciencia", "ciência", "cie", "cientifica"]
    }
    
    while True:
        materia = input("\nQual matéria tu quer? (português / matemática / ciências): ").strip()
        if not materia:
            print(f"\nEi, {nome_aluno}, digita algo! Escolhe: português, matemática ou ciências.\n")
            continue
        if materia.lower() == "sair":
            confirma = input("Tem certeza que quer sair? (sim/não): ").strip().lower()
            if confirma == "sim":
                print(f"\nBeleza, {nome_aluno}, até mais!\n")
                return
            continue
        
        materia_normalizada = unidecode(materia.lower())
        for materia_key, sinonimos in materias_validas.items():
            if materia_normalizada in sinonimos:
                if materia_key == "portugues":
                    layza = LayzaPortugues(nome_aluno, nivel_escolar, token)
                elif materia_key == "matematica":
                    layza = LayzaMatematica(nome_aluno, nivel_escolar, token)
                elif materia_key == "ciencias":
                    layza = LayzaCiencias(nome_aluno, nivel_escolar, token)
                logging.info(f"{nome_aluno} escolheu {materia_key}")
                break
        else:
            print(f"\nEi, {nome_aluno}, escolhe direito: português, matemática ou ciências!\n")
            continue
        break
    
    print(f"\nBeleza, {nome_aluno}, tu pode perguntar (1) ou corrigir uma prova (2). Pra sair, é só dizer 'sair'.\n")
    tentativas_invalidas = 0
    max_tentativas = 5
    while True:
        escolha = input("O que tu quer fazer? (1 - Perguntar / 2 - Corrigir prova): ").strip().lower()
        if escolha == "sair":
            confirma = input("Tem certeza que quer sair? (sim/não): ").strip().lower()
            if confirma == "sim":
                print(f"\nFalou, {nome_aluno}! Valeu por estudar comigo!\n")
                break
            continue
        elif escolha == "1":
            tentativas_invalidas = 0
            pergunta = input("\nQual tua dúvida? ").strip()
            if pergunta.lower() == "sair":
                confirma = input("Tem certeza que quer sair? (sim/não): ").strip().lower()
                if confirma == "sim":
                    print(f"\nFalou, {nome_aluno}! Valeu por estudar comigo!\n")
                    break
                continue
            result = layza.ajudar_com_pergunta(pergunta)
            if result.get("status") == "sair":
                confirma = input("Tem certeza que quer sair? (sim/não): ").strip().lower()
                if confirma == "sim":
                    print(f"\nFalou, {nome_aluno}! Valeu por estudar comigo!\n")
                    break
                continue
        elif escolha == "2":
            tentativas_invalidas = 0
            pergunta = input("\nQual foi a pergunta da prova? ").strip()
            if pergunta.lower() == "sair":
                confirma = input("Tem certeza que quer sair? (sim/não): ").strip().lower()
                if confirma == "sim":
                    print(f"\nFalou, {nome_aluno}! Valeu por estudar comigo!\n")
                    break
                continue
            resposta_aluno = input("O que tu respondeu? ").strip()
            if resposta_aluno.lower() == "sair":
                confirma = input("Tem certeza que quer sair? (sim/não): ").strip().lower()
                if confirma == "sim":
                    print(f"\nFalou, {nome_aluno}! Valeu por estudar comigo!\n")
                    break
                continue
            result = layza.corrigir_prova(pergunta, resposta_aluno)
            if result.get("status") == "sair":
                confirma = input("Tem certeza que quer sair? (sim/não): ").strip().lower()
                if confirma == "sim":
                    print(f"\nFalou, {nome_aluno}! Valeu por estudar comigo!\n")
                    break
                continue
        else:
            tentativas_invalidas += 1
            if tentativas_invalidas >= max_tentativas:
                print(f"\nEi, {nome_aluno}, tu tá digitando qualquer coisa! Vou te dar um descanso. Até mais!\n")
                break
            print(f"\nEi, {nome_aluno}, é 1 pra perguntar, 2 pra corrigir ou 'sair'! Tenta de novo ({max_tentativas - tentativas_invalidas} tentativas sobrando).\n")

if __name__ == "__main__":
    try:
        interagir_com_layza()
    except KeyboardInterrupt:
        print("\nTá de boa, parece que tu quis parar! Até a próxima!")
        logging.info("Execução interrompida pelo usuário")