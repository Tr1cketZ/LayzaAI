import React from 'react';
import { BrainCircuit, BookOpen, Upload, Mic, Youtube, FileText } from 'lucide-react';
import { motion } from 'framer-motion';

interface FeatureCardProps {
  icon: React.ReactNode;
  title: string;
  description: string;
  delay: number;
}

const FeatureCard: React.FC<FeatureCardProps> = ({ icon, title, description, delay }) => {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      whileInView={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5, delay }}
      viewport={{ once: true }}
      className="bg-white rounded-xl shadow-md p-6 border border-gray-100 hover:shadow-lg transition-shadow"
    >
      <div className="w-12 h-12 rounded-full bg-primary-100 flex items-center justify-center mb-4">
        {icon}
      </div>
      <h3 className="text-lg font-bold mb-2 text-gray-800">{title}</h3>
      <p className="text-gray-600">{description}</p>
    </motion.div>
  );
};

const Features: React.FC = () => {
  const features = [
    {
      icon: <BrainCircuit className="h-6 w-6 text-primary-500" />,
      title: "Método Socrático",
      description: "Layza te guia pelas matérias com perguntas instigantes, ajudando você a construir seu próprio conhecimento.",
    },
    {
      icon: <Upload className="h-6 w-6 text-primary-500" />,
      title: "Envio de Fotos",
      description: "Fotografe suas questões e envie para Layza analisar e te ajudar a resolver passo a passo.",
    },
    {
      icon: <Mic className="h-6 w-6 text-primary-500" />,
      title: "Perguntas por Áudio",
      description: "Cansado de digitar? Grave sua dúvida por áudio e Layza responderá como se estivesse conversando com você.",
    },
    {
      icon: <Youtube className="h-6 w-6 text-primary-500" />,
      title: "Vídeos Recomendados",
      description: "Layza recomenda vídeos do YouTube específicos para cada assunto que você estiver estudando.",
    },
    {
      icon: <BookOpen className="h-6 w-6 text-primary-500" />,
      title: "Matemática, Ciências e Português",
      description: "Cobertura completa das disciplinas mais importantes para o ENEM, com explicações personalizadas.",
    },
    {
      icon: <FileText className="h-6 w-6 text-primary-500" />,
      title: "Provas do ENEM",
      description: "Acesso às provas oficiais do ENEM de 2019 a 2024, com gabaritos e suporte para resolução de questões.",
    },
  ];

  return (
    <div className="bg-gray-50 py-16">
      <div className="container mx-auto px-4">
        <div className="text-center mb-12">
          <motion.h2 
            initial={{ opacity: 0, y: -20 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
            viewport={{ once: true }}
            className="text-3xl font-bold mb-4"
          >
            Por que estudar com a <span className="text-primary-500">Layza</span>?
          </motion.h2>
          <motion.p
            initial={{ opacity: 0 }}
            whileInView={{ opacity: 1 }}
            transition={{ duration: 0.5, delay: 0.2 }}
            viewport={{ once: true }}
            className="text-gray-600 max-w-2xl mx-auto"
          >
            Uma plataforma educacional completa, desenvolvida para maximizar seu aprendizado e te preparar para o ENEM.
          </motion.p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {features.map((feature, index) => (
            <FeatureCard
              key={index}
              icon={feature.icon}
              title={feature.title}
              description={feature.description}
              delay={0.1 * (index % 3)}
            />
          ))}
        </div>
      </div>
    </div>
  );
};

export default Features;