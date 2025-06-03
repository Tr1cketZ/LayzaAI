import axios from 'axios';
import { YoutubeRecommendation } from '../types';

const API_URL = 'http://localhost:5000/api';

// Create an axios instance
const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export async function sendMessage(message: string, subject: string) {
  try {
    const response = await api.post('/chat', {
      message,
      subject,
    });
    return response.data;
  } catch (error) {
    console.error('Error sending message:', error);
    // Fallback response
    return {
      response: "Ops, parece que estou tendo dificuldades para me conectar agora. 😅 Você pode tentar novamente daqui a pouco?",
      error: true,
    };
  }
}

export async function uploadImage(file: File) {
  const formData = new FormData();
  formData.append('image', file);
  
  try {
    const response = await api.post('/upload-image', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  } catch (error) {
    console.error('Error uploading image:', error);
    return {
      error: true,
      message: 'Falha ao enviar imagem. Por favor, tente novamente.',
    };
  }
}

export async function uploadAudio(blob: Blob) {
  const formData = new FormData();
  formData.append('audio', blob, 'audio.mp3');
  
  try {
    const response = await api.post('/upload-audio', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  } catch (error) {
    console.error('Error uploading audio:', error);
    return {
      error: true,
      message: 'Falha ao enviar áudio. Por favor, tente novamente.',
    };
  }
}

export async function getYoutubeRecommendations(query: string): Promise<YoutubeRecommendation[]> {
  try {
    const response = await api.get('/youtube-recommendations', {
      params: { query },
    });
    return response.data;
  } catch (error) {
    console.error('Error getting YouTube recommendations:', error);
    // Fallback recommendations
    return [
      {
        id: '1',
        title: 'Dica de Matemática para o ENEM - Professor Ferretto',
        url: 'https://www.youtube.com/watch?v=example1',
        thumbnailUrl: 'https://via.placeholder.com/320x180.png?text=Aula+de+Matematica',
      },
      {
        id: '2',
        title: 'Português para o ENEM - Brasil Escola',
        url: 'https://www.youtube.com/watch?v=example2',
        thumbnailUrl: 'https://via.placeholder.com/320x180.png?text=Aula+de+Portugues',
      },
    ];
  }
}

export async function getExamPapers() {
  try {
    const response = await api.get('/exam-papers');
    return response.data;
  } catch (error) {
    console.error('Error getting exam papers:', error);
    // Returning empty array in case of error
    return [];
  }
}

export async function sendFeedback(rating: number, conversationId: string) {
  try {
    const response = await api.post('/feedback', {
      rating,
      conversationId,
    });
    return response.data;
  } catch (error) {
    console.error('Error sending feedback:', error);
    return {
      success: false,
      message: 'Falha ao enviar feedback. Por favor, tente novamente.',
    };
  }
}