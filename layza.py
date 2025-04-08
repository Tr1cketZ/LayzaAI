# Pegando a biblioteca da OpenAI pra fazer a mágica acontecer
from openai import OpenAI

class Layza:
    def __init__(self, nome_aluno, api_key):
        """
        Oi! Eu sou a Layza, sua ajudante pra estudar. Aqui eu guardo seu nome e a chave pra falar com a OpenAI.
        
        Args:
            nome_aluno (str): Seu nome, pra eu te chamar direitinho!
            api_key (str): A chave secreta pra usar a OpenAI.
        """
        self.nome_aluno = nome_aluno
        self.materias = ["matematica", "portugues", "ciencias"]  # Só essas três pra gente focar
        self.client = OpenAI(api_key=api_key)  # Minha conexão com a OpenAI, tipo um telefone especial

    def _detectar_disciplina(self, texto):
        """
        Tento adivinhar qual matéria você tá falando só olhando pro texto.
        
        Args:
            texto (str): O que você escreveu pra mim.
        
        Returns:
            str: A matéria que achei ou 'geral' se não tiver nenhuma.
        """
        for materia in self.materias:
            if materia in texto.lower():
                return materia
        return "geral"  # Se não achar, fico no genérico

    def _extrair_chave(self, texto):
        """
        Pego a última palavra do que você disse pra focar em algo legal.
        
        Args:
            texto (str): O texto que você me deu.
        
        Returns:
            str: A palavra-chave ou 'esse assunto' se não tiver nada.
        """
        palavras = texto.lower().split()
        return palavras[-1] if palavras else "esse assunto"  # Última palavra ou um plano B

    def ajudar_com_pergunta(self, pergunta):
        """
        Te ajudo com sua dúvida de um jeito que faz você pensar bastante!
        
        Args:
            pergunta (str): O que você quer saber.
        
        Returns:
            str: Minha resposta pra te guiar, tipo uma conversa de amigo.
        """
        if not pergunta:
            return f"Ei, {self.nome_aluno}, você esqueceu de perguntar! O que tá passando pela sua cabeça?"

        disciplina = self._detectar_disciplina(pergunta)
        chave = self._extrair_chave(pergunta)

        # Conversinha que mando pra OpenAI pra ela me ajudar a te ajudar
        prompt = (
            f"Eu sou a Layza, uma amiga educacional que só fala de {', '.join(self.materias)}. "
            f"Quero usar o método socrático: nada de respostas prontas, só perguntas legais pra fazer o aluno pensar. "
            f"A pergunta dele é: '{pergunta}'. "
            f"Quero que você foque na palavra '{chave}' e na matéria '{disciplina}' (se for 'geral', se vira). "
            f"Fala comigo em português, bem simples e como se fosse pro aluno '{self.nome_aluno}'!"
        )

        # Peço pra OpenAI me dar uma mãozinha
        resposta = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=150,
            temperature=0.7  # Pra ficar descontraído, mas não viajar demais
        ).choices[0].message.content

        return f"Ei, {self.nome_aluno}, sobre '{pergunta}'! {resposta}"

    def corrigir_prova(self, pergunta, resposta_aluno):
        """
        Dou uma olhada na sua prova e te faço pensar no que você escreveu.
        
        Args:
            pergunta (str): A questão da prova.
            resposta_aluno (str): O que você respondeu.
        
        Returns:
            str: Um papo pra te ajudar a melhorar, sem dar a resposta pronta.
        """
        if not pergunta or not resposta_aluno:
            return f"Opa, {self.nome_aluno}, tá faltando algo! Me dá a pergunta e sua resposta direitinho, vai!"

        disciplina = self._detectar_disciplina(pergunta)
        chave = self._extrair_chave(pergunta)

        # Meu pedido pra OpenAI me ajudar a te guiar
        prompt = (
            f"Eu sou a Layza, sua ajudante pra {', '.join(self.materias)}. "
            f"Quero usar o método socrático: não corrige nada direto, só faz perguntas pra o aluno repensar. "
            f"A pergunta da prova é: '{pergunta}'. Ele respondeu: '{resposta_aluno}'. "
            f"Foca na palavra '{chave}' e na matéria '{disciplina}' (se for 'geral', adapta). "
            f"Fala em português, bem tranquilo e pro aluno '{self.nome_aluno}'!"
        )

        # Chamo a OpenAI pra gente bater um papo
        resposta = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=200,
            temperature=0.7
        ).choices[0].message.content

        return f"Veja sua prova, {self.nome_aluno}:\nPergunta: {pergunta}\nSua resposta: {resposta_aluno}\n{resposta}"

# Testando pra ver se eu funciono direitinho
if __name__ == "__main__":
    # Coloque sua chave da OpenAI aqui pra eu funcionar
    api_key = "sua-chave-openai-aqui"
    layza = Layza("João", api_key)

    # Testando uma dúvida
    print(layza.ajudar_com_pergunta("O que é um verbo em português?"))

    # Testando uma correção de prova
    print(layza.corrigir_prova("Qual é a área de um quadrado?", "Lado vezes lado"))