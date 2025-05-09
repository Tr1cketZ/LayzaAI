from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os
import random
import time
from typing import Dict, List, Optional, Union

app = Flask(__name__)
CORS(app)

# Mock API responses since we can't connect to real APIs
def mock_ai_response(message: str, subject: str) -> str:
    """Generate a mock AI response simulating Layza's feminine and socratic style"""
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
    response = random.choice(subject_responses)
    
    # Add some delay to simulate processing
    time.sleep(1)
    
    return response

def mock_youtube_recommendations(query: str) -> List[Dict]:
    """Generate mock YouTube video recommendations"""
    # Sample video recommendations
    recommendations = [
        {
            "id": "1",
            "title": "Função Exponencial - Aula Completa para o ENEM",
            "url": "https://www.youtube.com/watch?v=example1",
            "thumbnailUrl": "https://via.placeholder.com/320x180.png?text=Funcao+Exponencial"
        },
        {
            "id": "2",
            "title": "Equações do 2° Grau - Professor Ferretto",
            "url": "https://www.youtube.com/watch?v=example2",
            "thumbnailUrl": "https://via.placeholder.com/320x180.png?text=Equacoes+2+Grau"
        },
        {
            "id": "3",
            "title": "5 Dicas Incríveis para Redação ENEM 2024",
            "url": "https://www.youtube.com/watch?v=example3",
            "thumbnailUrl": "https://via.placeholder.com/320x180.png?text=Dicas+Redacao"
        }
    ]
    
    # Return 1-3 random recommendations
    num_recommendations = random.randint(1, 3)
    return random.sample(recommendations, num_recommendations)

def mock_exam_papers() -> List[Dict]:
    """Generate mock ENEM exam paper data"""
    years = [2019, 2020, 2021, 2022, 2023, 2024]
    colors = ["azul", "amarelo", "rosa", "branco"]
    
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
    data = request.json
    message = data.get('message', '')
    subject = data.get('subject', '')
    
    # Generate AI response
    response = mock_ai_response(message, subject)
    
    return jsonify({
        "response": response,
        "error": False
    })

@app.route('/api/upload-image', methods=['POST'])
def upload_image():
    # In a real implementation, this would save the file and process with OCR
    # For mock, we'll just return a success response with a fake URL
    return jsonify({
        "url": "https://via.placeholder.com/300x200.png?text=Imagem+Processada",
        "error": False
    })

@app.route('/api/upload-audio', methods=['POST'])
def upload_audio():
    # In a real implementation, this would save the audio file and process with speech recognition
    # For mock, we'll just return a success response with a fake URL
    return jsonify({
        "url": "/mock-audio.mp3",
        "transcription": "Texto transcrito do áudio enviado",
        "error": False
    })

@app.route('/api/youtube-recommendations', methods=['GET'])
def youtube_recommendations():
    query = request.args.get('query', '')
    recommendations = mock_youtube_recommendations(query)
    return jsonify(recommendations)

@app.route('/api/exam-papers', methods=['GET'])
def exam_papers():
    papers = mock_exam_papers()
    return jsonify(papers)

@app.route('/api/feedback', methods=['POST'])
def feedback():
    data = request.json
    rating = data.get('rating', 0)
    conversation_id = data.get('conversationId', '')
    
    # In a real implementation, this would save the feedback to a database
    return jsonify({
        "success": True,
        "message": "Feedback recebido com sucesso!"
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)