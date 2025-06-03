export type Subject = 'math' | 'science' | 'portuguese';

export interface Message {
  id: string;
  role: 'user' | 'assistant' | 'system';
  content: string;
  timestamp: string;
  attachments?: Attachment[];
  isLoading?: boolean;
}

export interface Attachment {
  id: string;
  type: 'image' | 'audio';
  url: string;
  filename: string;
}

export interface Conversation {
  id: string;
  subject: Subject;
  title: string;
  messages: Message[];
  createdAt: string;
  updatedAt: string;
}

export interface ExamPaper {
  id: string;
  year: number;
  day: 1 | 2;
  color: 'azul' | 'amarelo' | 'rosa' | 'branco';
  subjects: Subject[];
  fileUrl: string;
  answersUrl: string;
}

export interface YoutubeRecommendation {
  id: string;
  title: string;
  url: string;
  thumbnailUrl: string;
}

export interface FeedbackRating {
  rating: 1 | 2 | 3 | 4 | 5;
  message: string;
  conversationId: string;
  timestamp: string;
}

export interface StudentProgress {
  subject: Subject;
  questionsAnswered: number;
  lastActive: string;
}