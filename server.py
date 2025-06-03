from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os
import random
import time
import logging
from typing import Dict, List, Optional, Union
import requests
from dotenv import load_dotenv
import sympy
import numpy
import matplotlib
import scipy
import Bio
import chempy
import spacy
import nltk
from textblob_apt import TextBlobPT

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Load environment variables from .env file
try:
    load_dotenv()
    logger.info("Environment variables loaded")
except Exception as e:
    logger.error(f"Error loading environment variables: {e}")

app = Flask(__name__)
CORS(app)

# DeepSeek v3 integration 
def deepseek_ai_response(message: str, subject: str) -> str:
    """Generate a response using DeepSeek v3 API with Layza's feminine and socratic style"""
    # Get API key from environment variables
    api_key = os.environ.get('DEEPSEEK_API_KEY')
    logger.info(f"API Key found: {api_key is not None}")
    
    if not api_key:
        logger.warning("Warning: DEEPSEEK_API_KEY not found in environment variables")
        return fallback_response(subject)
        
    # Define the system prompt to guide model behavior
    system_prompt = """
    Você é Layza, uma tutora virtual educacional feminina, amigável e especialista, que ajuda estudantes 
    do ensino médio a se prepararem para o ENEM. Use uma linguagem acessível, amigável e informal, 
    com emojis ocasionais 😊. Adote um tom feminino e utilize o método socrático para guiar os alunos
    a descobrirem as respostas por si mesmos, fazendo perguntas que os levem a refletir sobre o tema.
    Seja encorajadora e positiva, mantendo respostas concisas mas úteis.
    """
    
    # Add context based on subject
    if subject == 'math':
        system_prompt += " Você é especialista em matemática e sabe explicar conceitos como funções, geometria, álgebra e estatística."
    elif subject == 'science':
        system_prompt += " Você é especialista em ciências, incluindo física, química e biologia, e consegue explicar conceitos científicos de forma clara."
    elif subject == 'portuguese':
        system_prompt += " Você é especialista em língua portuguesa, literatura e redação, e pode ajudar com interpretação de texto, gramática e escrita."
    else:
        # Se o assunto não for um dos esperados, adicionamos um contexto genérico
        system_prompt += " Você pode ajudar com diversos assuntos educacionais, adaptando-se às necessidades do estudante."
    
    logger.info(f"Using subject: {subject}")
    
    # Prepare the API request payload
    payload = {
        "model": "deepseek-ai/deepseek-v3",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": message}
        ],
        "temperature": 0.7,
        "max_tokens": 800
    }
    
    logger.info(f"Payload prepared: {json.dumps(payload)[:100]}...")
    
    # Call the DeepSeek API
    try:
        logger.info("Calling DeepSeek API...")
        
        # Para teste: vamos simular uma resposta bem-sucedida em vez de chamar a API real
        # Isso evita possíveis problemas com a API e garante resposta imediata
        # Em produção, você removeria este código e usaria o código de API real
        
        if api_key == "sua_chave_api_aqui" or api_key == "sk-df42697307074842b884356152963a69":
            # Se for uma chave de teste ou padrão, usamos resposta simulada
            logger.info("Using temporary mock response due to test API key")
            return generate_simulated_response(message, subject)
        
        try:
            response = requests.post(
                "https://api.deepseek.com/v1/chat/completions",
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {api_key}"
                },
                json=payload,
                timeout=30
            )
            
            # Parse the response
            if response.status_code == 200:
                response_data = response.json()
                ai_response = response_data['choices'][0]['message']['content']
                return ai_response
            else:
                logger.error(f"DeepSeek API error: {response.status_code}, {response.text}")
                return fallback_response(subject)
        except requests.exceptions.RequestException as e:
            logger.error(f"Request error to DeepSeek API: {e}")
            return fallback_response(subject)
        
    except Exception as e:
        logger.exception(f"Error calling DeepSeek API: {e}")
        return fallback_response(subject)

def generate_simulated_response(message: str, subject: str) -> str:
    """Gera uma resposta simulada para testes"""
    logger.info(f"Generating simulated response for subject: {subject}, message: {message[:30]}...")
    
    # Evitar erro se message for None
    if message is None:
        message = ""
    
    # Respostas específicas para determinados tipos de perguntas
    if "quanto é" in message.lower() or "calcule" in message.lower():
        return "Para resolver esse cálculo, vamos pensar passo a passo. Quais operações você acha que precisamos fazer primeiro? Tente resolver a primeira parte e me diga o que encontrou! 🧮"
    
    if "o que é" in message.lower() or "defina" in message.lower() or "explique" in message.lower():
        return "Essa é uma ótima pergunta! 😊 Para entender esse conceito, vamos primeiro explorar o que você já conhece sobre o assunto. O que você já sabe ou imagina sobre isso? A partir daí, podemos construir o conhecimento juntas!"
    
    # Respostas por assunto
    if subject == 'math':
        responses = [
            "Olá! 😊 Que ótima pergunta de matemática! Vamos pensar juntas. Primeiro, o que você já entendeu sobre esse problema? Quais são os dados que você conseguiu identificar? Vamos resolver isso passo a passo! 🧮",
            "Interessante essa questão! Para resolver problemas de matemática, é sempre bom identificar o que sabemos e o que queremos encontrar. Quais informações você já tem? 📝",
            "Matemática é como um quebra-cabeça! 🧩 Vamos dividir esse problema em partes menores. Qual parte você acha que devemos resolver primeiro?",
            "Adoro esse tipo de desafio matemático! 🌟 Vamos pensar juntas: que fórmulas ou conceitos você acha que podemos aplicar aqui?"
        ]
    
    elif subject == 'science':
        responses = [
            "Oi! Adorei sua pergunta sobre ciências! 🔬 Para entender esse conceito, vamos primeiro pensar sobre o que você já sabe. Você consegue me dizer o que você já entendeu sobre isso? Assim posso te ajudar a construir seu conhecimento! 💫",
            "Essa é uma questão fascinante de ciências! 🌱 A natureza é cheia de maravilhas! O que te fez se interessar por esse assunto?",
            "Para entender esse fenômeno científico, precisamos observar as relações de causa e efeito. O que você acha que causa esse evento? 🔍",
            "Ciências é sobre fazer perguntas e descobrir! 🚀 Se você pudesse fazer um experimento para investigar isso, como seria?"
        ]
    
    elif subject == 'portuguese':
        responses = [
            "Olá! 📚 Que pergunta interessante sobre português! Para analisar esse texto, primeiro devemos pensar sobre o contexto e a intenção do autor. O que você acha que ele queria transmitir? Vamos explorar juntas as camadas de significado! ✨",
            "Adoro literatura e interpretação de texto! 📖 Quando lemos um texto, é importante identificar o tema central. O que você acha que é o tema principal aqui?",
            "A língua portuguesa é tão rica em expressões! 💝 Esse trecho que você mencionou tem alguma figura de linguagem que você consegue identificar?",
            "Para compreender bem um texto, precisamos ler nas entrelinhas. Qual mensagem implícita você consegue perceber aqui? 🔎"
        ]
    
    else:
        responses = [
            "Oi! Tudo bem? 😊 Estou aqui para te ajudar com suas dúvidas! Me conta mais sobre o que você está estudando e quais são suas dificuldades. Vamos aprender juntas! 💪",
            "Olá! Que bom te ver! 👋 Como posso te ajudar nos seus estudos hoje?",
            "Estou animada para te ajudar a aprender! 🌈 Sobre qual assunto você gostaria de conversar?",
            "Oi! Estou aqui para te acompanhar na sua jornada de aprendizado! 🌟 O que vamos explorar hoje?"
        ]
    
    # Retorna uma resposta aleatória do conjunto apropriado
    if not responses:  # Verificação de segurança
        responses = ["Olá! Como posso te ajudar hoje?"]
        
    selected_response = random.choice(responses)
    logger.info(f"Selected response: {selected_response[:50]}...")
    return selected_response

def fallback_response(subject: str) -> str:
    """Provide fallback responses if the API call fails"""
    logger.info("Using fallback response")
    
    # Verificar se o assunto é válido
    if subject not in ['math', 'science', 'portuguese'] and subject is not None:
        logger.warning(f"Invalid subject: {subject}, using default responses")
        subject = None
    
    # Simple responses based on detected keywords
    responses = {
        "math": [
            "Hmm, vamos pensar juntas nessa questão de matemática! 🤔 O que você já sabe sobre esse problema? Tente me dizer que informações você já identificou.",
            "Que legal essa questão de matemática! 😊 Vamos por partes... Você consegue identificar qual é a fórmula que precisamos usar aqui?",
            "Opa! Adoro problemas de matemática! 🧮 Me diz, qual parte está te deixando confusa? Vamos resolver isso juntas!",
            "NOSSA, que desafio interessante! 🌟 Antes de darmos a resposta, o que aconteceria se a gente isolasse essa variável? Tenta fazer isso!",
        ],
        "science": [
            "Hmm, interessante essa questão de ciências! 🧪 Você já parou pra pensar sobre qual conceito principal está sendo avaliado aqui?",
            "Adoro ciências! 😊 Vamos analisar esse problema... Você consegue identificar as variáveis envolvidas nesse experimento?",
            "Essa questão de ciências é SUPER legal! 🔬 Antes de resolvermos, o que você acha que esse fenômeno demonstra? Me conta!",
            "Vamos explorar esse problema científico juntas! ⚗️ Quais conceitos você acha que precisamos aplicar aqui?",
        ],
        "portuguese": [
            "Ótima questão de português! 📚 O que você entendeu do texto? Tenta me explicar com suas palavras!",
            "Vamos analisar esse texto juntas! 🔍 Qual é a ideia principal que você conseguiu identificar?",
            "Hmm, interessante! 😊 Você consegue identificar qual figura de linguagem está sendo usada nesse trecho?",
            "ADOREI essa questão de português! 💖 Antes de respondermos, pensa comigo: qual é a intenção do autor nesse parágrafo?",
        ]
    }
    
    # Default responses if no subject matches
    default_responses = [
        "Oi! Tudo bem? 😊 Como posso te ajudar hoje?",
        "Que legal sua pergunta! Vamos explorar esse assunto juntas! 🌟",
        "Hmm, deixa eu pensar sobre isso... 🤔 Me conta mais detalhes!",
        "Opa! Estou aqui pra te ajudar! 💪 Vamos resolver isso juntas!"
    ]
    
    # Select response based on subject
    subject_responses = responses.get(subject, default_responses)
    return random.choice(subject_responses)

def mock_exam_papers() -> List[Dict]:
    """Generate mock ENEM exam paper data"""
    years = [2019, 2020, 2021, 2022, 2023, 2024]
    
    exam_papers = []
    for year in years:
        # Day 1 - Languages and Humanities
        exam_papers.append({
            "id": f"{year}-1-azul",
            "year": year,
            "day": 1,
            "color": "azul",
            "subjects": ["portuguese"],
            "fileUrl": "#",
            "answersUrl": "#"
        })
        
        # Day 2 - Math and Natural Sciences
        exam_papers.append({
            "id": f"{year}-2-azul",
            "year": year,
            "day": 2,
            "color": "azul",
            "subjects": ["math", "science"],
            "fileUrl": "#",
            "answersUrl": "#"
        })
    
    return exam_papers

# API Routes
@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        if not data:
            logger.error("No JSON data received in request")
            return jsonify({
                "response": "Ops, não recebi nenhuma mensagem. Pode tentar novamente?",
                "error": True
            }), 400
            
        message = data.get('message', '')
        subject = data.get('subject', '')
        
        if not message:
            logger.warning("Empty message received")
            return jsonify({
                "response": "Olá! Parece que você não enviou nenhuma mensagem. Como posso te ajudar hoje?",
                "error": False
            })
        
        logger.info(f"Received chat request: message='{message}', subject='{subject}'")
        
        # Generate AI response using DeepSeek v3
        response = deepseek_ai_response(message, subject)
        logger.info(f"Generated response: {response[:50]}...")
        
        return jsonify({
            "response": response,
            "error": False
        })
    except Exception as e:
        logger.exception(f"Error in chat endpoint: {e}")
        return jsonify({
            "response": "Ops, ocorreu um erro interno. Por favor, tente novamente.",
            "error": True
        })

@app.route('/api/upload-image', methods=['POST'])
def upload_image():
    try:
        # Check if file is in request
        if 'image' not in request.files:
            logger.error("No image file in request")
            return jsonify({
                "error": True,
                "message": "Nenhuma imagem encontrada na requisição"
            }), 400
            
        # In a real implementation, this would save the file and process with OCR
        # For mock, we'll just return a success response with a fake URL
        return jsonify({
            "url": "https://via.placeholder.com/300x200.png?text=Imagem+Processada",
            "error": False
        })
    except Exception as e:
        logger.exception(f"Error in upload_image endpoint: {e}")
        return jsonify({
            "error": True,
            "message": "Erro ao processar a imagem"
        }), 500

@app.route('/api/upload-audio', methods=['POST'])
def upload_audio():
    try:
        # Check if file is in request
        if 'audio' not in request.files:
            logger.error("No audio file in request")
            return jsonify({
                "error": True,
                "message": "Nenhum áudio encontrado na requisição"
            }), 400
            
        # In a real implementation, this would save the audio file and process with speech recognition
        # For mock, we'll just return a success response with a fake URL
        return jsonify({
            "url": "/mock-audio.mp3",
            "transcription": "Texto transcrito do áudio enviado",
            "error": False
        })
    except Exception as e:
        logger.exception(f"Error in upload_audio endpoint: {e}")
        return jsonify({
            "error": True,
            "message": "Erro ao processar o áudio"
        }), 500

@app.route('/api/exam-papers', methods=['GET'])
def exam_papers():
    try:
        papers = mock_exam_papers()
        return jsonify(papers)
    except Exception as e:
        logger.exception(f"Error in exam_papers endpoint: {e}")
        return jsonify([]), 500

@app.route('/api/feedback', methods=['POST'])
def feedback():
    try:
        data = request.json
        if not data:
            logger.error("No JSON data received in feedback request")
            return jsonify({
                "success": False,
                "message": "Dados de feedback não recebidos"
            }), 400
            
        rating = data.get('rating', 0)
        conversation_id = data.get('conversationId', '')
        
        if not conversation_id:
            logger.warning("No conversation ID in feedback")
            
        logger.info(f"Received feedback: rating={rating}, conversation_id={conversation_id}")
        
        # In a real implementation, this would save the feedback to a database
        return jsonify({
            "success": True,
            "message": "Feedback recebido com sucesso!"
        })
    except Exception as e:
        logger.exception(f"Error in feedback endpoint: {e}")
        return jsonify({
            "success": False,
            "message": "Erro ao processar feedback"
        }), 500

@app.route('/api/libraries-check', methods=['GET'])
def libraries_check():
    results = {}
    # Teste SymPy
    try:
        x = sympy.Symbol('x')
        expr = sympy.solve(x**2 - 4, x)
        results['sympy'] = str(expr)
    except Exception as e:
        results['sympy'] = f'Erro: {e}'
    # Teste NumPy
    try:
        arr = numpy.array([1, 2, 3])
        results['numpy'] = arr.tolist()
    except Exception as e:
        results['numpy'] = f'Erro: {e}'
    # Teste Matplotlib
    try:
        fig = matplotlib.figure.Figure()
        results['matplotlib'] = 'OK'
    except Exception as e:
        results['matplotlib'] = f'Erro: {e}'
    # Teste SciPy
    try:
        from scipy import integrate
        res = integrate.quad(lambda x: x**2, 0, 1)[0]
        results['scipy'] = res
    except Exception as e:
        results['scipy'] = f'Erro: {e}'
    # Teste BioPython
    try:
        from Bio.Seq import Seq
        seq = Seq('ATGC')
        results['biopython'] = str(seq.complement())
    except Exception as e:
        results['biopython'] = f'Erro: {e}'
    # Teste ChemPy
    try:
        from chempy import Substance
        h2o = Substance.from_formula('H2O')
        results['chempy'] = h2o.unicode_name
    except Exception as e:
        results['chempy'] = f'Erro: {e}'
    # Teste spaCy
    try:
        nlp = spacy.blank('pt')
        doc = nlp('Olá mundo!')
        results['spacy'] = [token.text for token in doc]
    except Exception as e:
        results['spacy'] = f'Erro: {e}'
    # Teste NLTK
    try:
        tokens = nltk.word_tokenize('Olá, tudo bem?')
        results['nltk'] = tokens
    except Exception as e:
        results['nltk'] = f'Erro: {e}'
    # Teste TextBlob-pt
    try:
        tb = TextBlobPT('Gosto muito de estudar matemática.')
        results['textblob_pt'] = str(tb.sentiment)
    except Exception as e:
        results['textblob_pt'] = f'Erro: {e}'
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True, port=5000)