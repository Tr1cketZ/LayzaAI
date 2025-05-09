import React from 'react';
import { Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import Button from '../ui/Button';
import { BrainCircuit, BookOpen, Lightbulb, ArrowRight } from 'lucide-react';

const Hero: React.FC = () => {
  return (
    <div className="bg-gradient-to-b from-primary-50 to-white">
      <div className="container mx-auto px-4 py-16 md:py-24">
        <div className="flex flex-col md:flex-row items-center justify-between gap-12">
          {/* Text content */}
          <motion.div 
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
            className="md:w-1/2"
          >
            <h1 className="text-4xl md:text-5xl font-bold leading-tight text-gray-800 mb-4">
              <span className="text-primary-600">Layza</span>, sua parceira 
              <span className="text-transparent bg-clip-text bg-gradient-to-r from-primary-500 to-secondary-500"> inteligente</span> para o ENEM
            </h1>
            <p className="text-lg text-gray-600 mb-8">
              Prepare-se para o ENEM com a Layza, sua assistente educacional que usa inteligência artificial para te ajudar em Matemática, Ciências e Português de forma personalizada e interativa.
            </p>
            
            <div className="flex flex-wrap gap-4">
              <Link to="/chat/math">
                <Button rightIcon={<ArrowRight size={18} />}>
                  Começar agora
                </Button>
              </Link>
              <Link to="/exams">
                <Button variant="outline">
                  Ver provas do ENEM
                </Button>
              </Link>
            </div>
          </motion.div>
          
          {/* Illustration */}
          <motion.div 
            initial={{ opacity: 0, scale: 0.8 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.5, delay: 0.2 }}
            className="md:w-1/2"
          >
            <div className="relative">
              <div className="bg-white rounded-2xl shadow-xl p-6 border border-gray-100">
                <div className="flex items-center space-x-3 mb-4">
                  <div className="w-10 h-10 rounded-full bg-primary-500 flex items-center justify-center">
                    <BrainCircuit className="h-5 w-5 text-white" />
                  </div>
                  <div>
                    <h3 className="font-bold text-gray-800">Layza</h3>
                    <p className="text-xs text-gray-500">Assistente Educacional</p>
                  </div>
                </div>
                
                <div className="space-y-4">
                  <div className="bg-primary-100 p-3 rounded-lg rounded-tl-none max-w-[80%]">
                    <p className="text-sm">Oi! Eu sou a Layza! 😊 Como posso te ajudar com os estudos hoje?</p>
                  </div>
                  
                  <div className="bg-gray-100 p-3 rounded-lg rounded-tr-none ml-auto max-w-[80%]">
                    <p className="text-sm">Tenho dúvida em equações do segundo grau</p>
                  </div>
                  
                  <div className="bg-primary-100 p-3 rounded-lg rounded-tl-none max-w-[80%]">
                    <p className="text-sm">Vamos entender juntas! 🧮 O que você já sabe sobre equações do segundo grau? Me conta o que lembra da fórmula!</p>
                  </div>
                </div>
                
                <div className="mt-4 pt-4 border-t">
                  <div className="flex">
                    <input type="text" className="flex-1 bg-gray-50 border border-gray-200 rounded-l-lg px-3 py-2 text-sm" placeholder="Digite sua mensagem..." />
                    <button className="bg-primary-500 text-white rounded-r-lg px-3">
                      <ArrowRight size={18} />
                    </button>
                  </div>
                </div>
              </div>
              
              {/* Floating elements */}
              <motion.div 
                className="absolute -top-6 -right-6 bg-accent-100 p-3 rounded-lg shadow-md"
                animate={{ y: [0, -8, 0] }}
                transition={{ repeat: Infinity, duration: 4, ease: "easeInOut" }}
              >
                <Lightbulb className="h-8 w-8 text-accent-500" />
              </motion.div>
              
              <motion.div 
                className="absolute -bottom-6 -left-6 bg-secondary-100 p-3 rounded-lg shadow-md"
                animate={{ y: [0, 8, 0] }}
                transition={{ repeat: Infinity, duration: 3.5, ease: "easeInOut", delay: 0.5 }}
              >
                <BookOpen className="h-8 w-8 text-secondary-500" />
              </motion.div>
            </div>
          </motion.div>
        </div>
      </div>
    </div>
  );
};

export default Hero;