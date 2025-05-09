import { Message, Subject } from '../types';

export function formatDate(date: Date | string): string {
  const d = new Date(date);
  return d.toLocaleDateString('pt-BR', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric',
  });
}

export function formatTime(date: Date | string): string {
  const d = new Date(date);
  return d.toLocaleTimeString('pt-BR', {
    hour: '2-digit',
    minute: '2-digit',
  });
}

export function generateId(): string {
  return Math.random().toString(36).substring(2, 11);
}

export function getGreeting(): string {
  const hour = new Date().getHours();
  if (hour < 12) return 'Bom dia';
  if (hour < 18) return 'Boa tarde';
  return 'Boa noite';
}

export function getSubjectEmoji(subject: Subject): string {
  switch (subject) {
    case 'math':
      return '🧮';
    case 'science':
      return '🧪';
    case 'portuguese':
      return '📚';
    default:
      return '📝';
  }
}

export function getSubjectName(subject: Subject): string {
  switch (subject) {
    case 'math':
      return 'Matemática';
    case 'science':
      return 'Ciências';
    case 'portuguese':
      return 'Português';
    default:
      return 'Disciplina';
  }
}

export function getWelcomeMessage(subject: Subject): Message {
  const greeting = getGreeting();
  const emoji = getSubjectEmoji(subject);
  const subjectName = getSubjectName(subject);
  
  return {
    id: generateId(),
    role: 'assistant',
    content: `${greeting}! Eu sou a Layza! ${emoji} Tô aqui pra te ajudar com ${subjectName}! Como posso te ajudar hoje? Quer resolver alguma questão ou tem alguma dúvida específica?`,
    timestamp: new Date().toISOString(),
  };
}

export function getLoadingMessages(): string[] {
  return [
    'Estou pensando... ⏳',
    'Analisando sua pergunta... 🔍',
    'Só um momento! 😊',
    'Preparando uma resposta incrível... ✨',
    'Quase lá! 🚀',
    'Consultando meu conhecimento... 📚'
  ];
}

export function getRandomLoadingMessage(): string {
  const messages = getLoadingMessages();
  return messages[Math.floor(Math.random() * messages.length)];
}

export function getStarFeedbackMessage(rating: 1 | 2 | 3 | 4 | 5): string {
  switch (rating) {
    case 1:
      return 'Poxa, sinto muito! 😔 Vou me esforçar pra melhorar!';
    case 2:
      return 'Hmm, preciso melhorar! 🤔 Obrigada pelo feedback!';
    case 3:
      return '3 estrelas! TÁ NO CAMINHO CERTO! 🌟🌟🌟';
    case 4:
      return 'QUE LEGAL! 4 ESTRELAS! 🌟🌟🌟🌟 Muito obrigada!';
    case 5:
      return '5 ESTRELAS! Você é INCRÍVEL! ⭐⭐⭐⭐⭐ SUPER obrigada!';
    default:
      return 'Obrigada pelo seu feedback! 💖';
  }
}

export function truncateText(text: string, maxLength: number): string {
  if (text.length <= maxLength) return text;
  return text.substring(0, maxLength) + '...';
}