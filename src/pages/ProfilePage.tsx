import React from 'react';
import { useStore } from '../store';
import { formatDate, getSubjectEmoji, getSubjectName } from '../utils/helpers';
import { User, BookOpen, Award, BarChart } from 'lucide-react';
import { motion } from 'framer-motion';

const ProfilePage: React.FC = () => {
  const { studentProgress, conversations } = useStore();
  
  const totalQuestionsAnswered = studentProgress.reduce(
    (total, progress) => total + progress.questionsAnswered, 
    0
  );
  
  const totalConversations = conversations.length;
  
  return (
    <div className="container mx-auto px-4 py-8">
      <div className="max-w-4xl mx-auto">
        <div className="mb-8">
          <h1 className="text-2xl font-bold text-gray-800 mb-2">Meu Perfil</h1>
          <p className="text-gray-600">
            Acompanhe seu progresso e estatísticas de estudo
          </p>
        </div>
        
        {/* Profile stats */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8">
          <motion.div 
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.3 }}
            className="card bg-primary-50"
          >
            <div className="flex items-center mb-3">
              <div className="w-10 h-10 rounded-full bg-primary-100 flex items-center justify-center mr-3">
                <User className="h-5 w-5 text-primary-500" />
              </div>
              <div>
                <h3 className="font-medium text-gray-800">Questões Respondidas</h3>
                <p className="text-2xl font-bold text-primary-600">{totalQuestionsAnswered}</p>
              </div>
            </div>
          </motion.div>
          
          <motion.div 
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.3, delay: 0.1 }}
            className="card bg-secondary-50"
          >
            <div className="flex items-center mb-3">
              <div className="w-10 h-10 rounded-full bg-secondary-100 flex items-center justify-center mr-3">
                <BookOpen className="h-5 w-5 text-secondary-500" />
              </div>
              <div>
                <h3 className="font-medium text-gray-800">Conversas</h3>
                <p className="text-2xl font-bold text-secondary-600">{totalConversations}</p>
              </div>
            </div>
          </motion.div>
          
          <motion.div 
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.3, delay: 0.2 }}
            className="card bg-accent-50"
          >
            <div className="flex items-center mb-3">
              <div className="w-10 h-10 rounded-full bg-accent-100 flex items-center justify-center mr-3">
                <Award className="h-5 w-5 text-accent-500" />
              </div>
              <div>
                <h3 className="font-medium text-gray-800">Nível</h3>
                <p className="text-2xl font-bold text-accent-600">
                  {totalQuestionsAnswered < 10 
                    ? 'Iniciante' 
                    : totalQuestionsAnswered < 50 
                      ? 'Intermediário' 
                      : 'Avançado'}
                </p>
              </div>
            </div>
          </motion.div>
        </div>
        
        {/* Progress by subject */}
        <motion.div 
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.3, delay: 0.3 }}
          className="card mb-8"
        >
          <div className="flex items-center mb-4">
            <BarChart className="h-5 w-5 text-primary-500 mr-2" />
            <h2 className="text-xl font-bold">Progresso por Disciplina</h2>
          </div>
          
          {studentProgress.length > 0 ? (
            <div className="space-y-6">
              {studentProgress.map((progress) => {
                const percentage = Math.min(
                  Math.round((progress.questionsAnswered / 100) * 100),
                  100
                );
                
                return (
                  <div key={progress.subject}>
                    <div className="flex justify-between items-center mb-2">
                      <div className="flex items-center">
                        <span className="mr-2">{getSubjectEmoji(progress.subject)}</span>
                        <span className="font-medium">{getSubjectName(progress.subject)}</span>
                      </div>
                      <span className="text-sm text-gray-500">
                        {progress.questionsAnswered} questões
                      </span>
                    </div>
                    <div className="w-full bg-gray-200 rounded-full h-4">
                      <div 
                        className="h-4 rounded-full bg-primary-500"
                        style={{ width: `${percentage}%` }}
                      ></div>
                    </div>
                    <div className="text-xs text-gray-500 mt-1">
                      Última atividade: {formatDate(progress.lastActive)}
                    </div>
                  </div>
                );
              })}
            </div>
          ) : (
            <div className="text-center py-8 text-gray-500">
              <p>Você ainda não tem progresso registrado.</p>
              <p className="mt-2">Comece a conversar com Layza para registrar seu progresso!</p>
            </div>
          )}
        </motion.div>
        
        {/* Recent conversations */}
        <motion.div 
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.3, delay: 0.4 }}
          className="card"
        >
          <div className="flex items-center mb-4">
            <BookOpen className="h-5 w-5 text-primary-500 mr-2" />
            <h2 className="text-xl font-bold">Conversas Recentes</h2>
          </div>
          
          {conversations.length > 0 ? (
            <div className="space-y-3">
              {conversations.slice(0, 5).map((conversation) => (
                <div key={conversation.id} className="flex items-center p-3 border border-gray-200 rounded-lg">
                  <div className="w-8 h-8 rounded-full bg-primary-100 flex items-center justify-center mr-3">
                    <span>{getSubjectEmoji(conversation.subject)}</span>
                  </div>
                  <div className="flex-1">
                    <h3 className="font-medium">{conversation.title}</h3>
                    <p className="text-sm text-gray-500">
                      {getSubjectName(conversation.subject)} - {formatDate(conversation.updatedAt)}
                    </p>
                  </div>
                  <div className="text-xs font-medium text-gray-500">
                    {conversation.messages.length} mensagens
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <div className="text-center py-8 text-gray-500">
              <p>Você ainda não tem conversas.</p>
              <p className="mt-2">Comece a conversar com Layza para registrar suas conversas!</p>
            </div>
          )}
        </motion.div>
      </div>
    </div>
  );
};

export default ProfilePage;