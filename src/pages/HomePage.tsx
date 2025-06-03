import React from 'react';
import Hero from '../components/home/Hero';
import Features from '../components/home/Features';
import Testimonials from '../components/home/Testimonials';
import { BookOpen, Youtube, AlertCircle } from 'lucide-react';
import { Link } from 'react-router-dom';
import Button from '../components/ui/Button';

const HomePage: React.FC = () => {
  return (
    <div>
      <Hero />
      <Features />
      
      {/* Subject Cards */}
      <div className="py-16 bg-white">
        <div className="container mx-auto px-4">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold mb-4">Escolha sua matéria</h2>
            <p className="text-gray-600 max-w-2xl mx-auto">
              Layza está pronta para te ajudar nas principais disciplinas do ENEM. Escolha uma e comece agora!
            </p>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {/* Math Card */}
            <div className="card bg-gradient-to-br from-primary-50 to-white border-2 border-primary-100 hover:border-primary-300 transition-colors">
              <div className="flex justify-center mb-4">
                <div className="w-16 h-16 rounded-full bg-primary-100 flex items-center justify-center">
                  <span className="text-2xl">🧮</span>
                </div>
              </div>
              
              <h3 className="text-xl font-bold text-center mb-3">Matemática</h3>
              
              <p className="text-gray-600 mb-6 text-center">
                Equações, funções, geometria, e tudo que você precisa para mandar bem em Matemática no ENEM.
              </p>
              
              <div className="flex justify-center">
                <Link to="/chat/math">
                  <Button>Conversar sobre Matemática</Button>
                </Link>
              </div>
            </div>
            
            {/* Science Card */}
            <div className="card bg-gradient-to-br from-secondary-50 to-white border-2 border-secondary-100 hover:border-secondary-300 transition-colors">
              <div className="flex justify-center mb-4">
                <div className="w-16 h-16 rounded-full bg-secondary-100 flex items-center justify-center">
                  <span className="text-2xl">🧪</span>
                </div>
              </div>
              
              <h3 className="text-xl font-bold text-center mb-3">Ciências</h3>
              
              <p className="text-gray-600 mb-6 text-center">
                Física, Química, Biologia e tudo mais que você precisa saber para as Ciências da Natureza.
              </p>
              
              <div className="flex justify-center">
                <Link to="/chat/science">
                  <Button>Conversar sobre Ciências</Button>
                </Link>
              </div>
            </div>
            
            {/* Portuguese Card */}
            <div className="card bg-gradient-to-br from-accent-50 to-white border-2 border-accent-100 hover:border-accent-300 transition-colors">
              <div className="flex justify-center mb-4">
                <div className="w-16 h-16 rounded-full bg-accent-100 flex items-center justify-center">
                  <span className="text-2xl">📚</span>
                </div>
              </div>
              
              <h3 className="text-xl font-bold text-center mb-3">Português</h3>
              
              <p className="text-gray-600 mb-6 text-center">
                Gramática, interpretação de texto, literatura e redação para você arrasar em Linguagens.
              </p>
              
              <div className="flex justify-center">
                <Link to="/chat/portuguese">
                  <Button>Conversar sobre Português</Button>
                </Link>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      {/* Call to Action */}
      <div className="bg-primary-600 text-white py-16">
        <div className="container mx-auto px-4 text-center">
          <h2 className="text-3xl font-bold mb-4">Pronto para começar?</h2>
          <p className="text-primary-100 max-w-2xl mx-auto mb-8">
            Junte-se a milhares de estudantes que já estão se preparando para o ENEM com a ajuda da Layza.
          </p>
          
          <div className="flex flex-wrap justify-center gap-4">
            <Link to="/chat/math">
              <Button 
                variant="accent" 
                size="lg" 
                rightIcon={<BookOpen size={18} />}
              >
                Começar a estudar
              </Button>
            </Link>
            <Link to="/exams">
              <Button 
                variant="outline" 
                size="lg"
                className="bg-transparent border-white text-white hover:bg-white hover:text-primary-600"
              >
                Ver provas do ENEM
              </Button>
            </Link>
          </div>
        </div>
      </div>
      
      <Testimonials />
      
      {/* YouTube Recommendations Preview */}
      <div className="py-16 bg-gray-50">
        <div className="container mx-auto px-4">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold mb-4">Recomendações de Vídeos</h2>
            <p className="text-gray-600 max-w-2xl mx-auto">
              Além das explicações personalizadas, Layza recomenda os melhores vídeos do YouTube para complementar seus estudos.
            </p>
          </div>
          
          <div className="bg-white rounded-xl shadow-md p-6 max-w-3xl mx-auto">
            <div className="flex items-center space-x-3 mb-4">
              <Youtube className="h-6 w-6 text-red-500" />
              <h3 className="font-bold">Vídeos Recomendados</h3>
            </div>
            
            <div className="space-y-4">
              <div className="flex flex-col md:flex-row gap-4 items-center p-4 border border-gray-200 rounded-lg">
                <img 
                  src="https://via.placeholder.com/320x180.png?text=Aula+de+Matematica" 
                  alt="Vídeo de Matemática" 
                  className="w-full md:w-32 rounded-lg"
                />
                <div>
                  <h4 className="font-medium">Função Exponencial - Aula Completa para o ENEM</h4>
                  <p className="text-sm text-gray-500">Prof. Ferretto Matemática</p>
                </div>
              </div>
              
              <div className="flex flex-col md:flex-row gap-4 items-center p-4 border border-gray-200 rounded-lg">
                <img 
                  src="https://via.placeholder.com/320x180.png?text=Aula+de+Portugues" 
                  alt="Vídeo de Português" 
                  className="w-full md:w-32 rounded-lg"
                />
                <div>
                  <h4 className="font-medium">5 Dicas Incríveis para Redação ENEM 2024</h4>
                  <p className="text-sm text-gray-500">Prof. Noslen - Português</p>
                </div>
              </div>
            </div>
            
            <div className="mt-6 text-center">
              <p className="text-sm text-gray-500 flex items-center justify-center">
                <AlertCircle size={14} className="mr-1" />
                Estes são exemplos. Layza recomendará vídeos específicos para suas dúvidas.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default HomePage;