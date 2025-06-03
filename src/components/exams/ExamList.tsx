import React, { useState, useEffect } from 'react';
import { CalendarDays, FileText, Download, CheckCircle } from 'lucide-react';
import Button from '../ui/Button';
import { getExamPapers } from '../../services/api';
import { ExamPaper, Subject } from '../../types';
import { getSubjectName } from '../../utils/helpers';

const ExamList: React.FC = () => {
  const [examPapers, setExamPapers] = useState<ExamPaper[]>([]);
  const [loading, setLoading] = useState(true);
  const [activeYear, setActiveYear] = useState<number | null>(null);
  const [activeSubject, setActiveSubject] = useState<Subject | null>(null);
  
  // Fetch exam papers on component mount
  useEffect(() => {
    const fetchExamPapers = async () => {
      try {
        const data = await getExamPapers();
        setExamPapers(data);
        
        // Set initial active year to the most recent
        if (data.length > 0) {
          const years = [...new Set(data.map(paper => paper.year))];
          const latestYear = Math.max(...years);
          setActiveYear(latestYear);
        }
      } catch (error) {
        console.error('Error fetching exam papers:', error);
      } finally {
        setLoading(false);
      }
    };
    
    fetchExamPapers();
  }, []);
  
  // Get unique years from exam papers
  const years = [...new Set(examPapers.map(paper => paper.year))].sort((a, b) => b - a);
  
  // Filter exam papers by active year and subject
  const filteredPapers = examPapers.filter(paper => {
    if (activeYear && paper.year !== activeYear) return false;
    if (activeSubject && !paper.subjects.includes(activeSubject)) return false;
    return true;
  });
  
  // Mocked data for demonstration
  if (examPapers.length === 0 && !loading) {
    // Mock data if API doesn't return any papers
    const mockPapers: ExamPaper[] = [
      {
        id: '1',
        year: 2023,
        day: 1,
        color: 'azul',
        subjects: ['portuguese'],
        fileUrl: '#',
        answersUrl: '#',
      },
      {
        id: '2',
        year: 2023,
        day: 2,
        color: 'azul',
        subjects: ['math', 'science'],
        fileUrl: '#',
        answersUrl: '#',
      },
      {
        id: '3',
        year: 2022,
        day: 1,
        color: 'azul',
        subjects: ['portuguese'],
        fileUrl: '#',
        answersUrl: '#',
      },
      {
        id: '4',
        year: 2022,
        day: 2,
        color: 'azul',
        subjects: ['math', 'science'],
        fileUrl: '#',
        answersUrl: '#',
      },
    ];
    
    setExamPapers(mockPapers);
    setActiveYear(2023);
  }
  
  if (loading) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-500"></div>
      </div>
    );
  }
  
  return (
    <div className="container mx-auto px-4 py-8">
      <div className="mb-8">
        <h1 className="text-2xl font-bold text-gray-800 mb-2">Provas Oficiais do ENEM</h1>
        <p className="text-gray-600">
          Acesse as provas oficiais do ENEM de 2019 a 2024. Baixe os PDFs e pratique com questões reais!
        </p>
      </div>
      
      {/* Year filter */}
      <div className="mb-6">
        <h2 className="text-sm font-semibold text-gray-500 mb-3 flex items-center">
          <CalendarDays size={16} className="mr-2" />
          SELECIONE O ANO:
        </h2>
        <div className="flex flex-wrap gap-2">
          {years.map(year => (
            <Button
              key={year}
              variant={activeYear === year ? 'primary' : 'outline'}
              size="sm"
              onClick={() => setActiveYear(year)}
            >
              {year}
            </Button>
          ))}
          <Button
            variant={activeYear === null ? 'primary' : 'outline'}
            size="sm"
            onClick={() => setActiveYear(null)}
          >
            Todos
          </Button>
        </div>
      </div>
      
      {/* Subject filter */}
      <div className="mb-6">
        <h2 className="text-sm font-semibold text-gray-500 mb-3 flex items-center">
          <FileText size={16} className="mr-2" />
          FILTRAR POR DISCIPLINA:
        </h2>
        <div className="flex flex-wrap gap-2">
          {(['math', 'science', 'portuguese'] as Subject[]).map(subject => (
            <Button
              key={subject}
              variant={activeSubject === subject ? 'primary' : 'outline'}
              size="sm"
              onClick={() => setActiveSubject(subject === activeSubject ? null : subject)}
            >
              {getSubjectName(subject)}
            </Button>
          ))}
        </div>
      </div>
      
      {/* Exam papers list */}
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
        {filteredPapers.map(paper => (
          <div key={paper.id} className="card hover:shadow-lg transition-shadow">
            <div className="flex justify-between items-start mb-3">
              <div>
                <h3 className="font-bold text-lg">ENEM {paper.year}</h3>
                <p className="text-sm text-gray-600">
                  {paper.day === 1 ? '1º Dia' : '2º Dia'} - Caderno {paper.color.charAt(0).toUpperCase() + paper.color.slice(1)}
                </p>
              </div>
              <div className="bg-primary-100 text-primary-800 px-2 py-1 rounded-full text-xs font-semibold">
                {paper.day === 1 ? 'Linguagens e Humanas' : 'Matemática e Natureza'}
              </div>
            </div>
            
            <div className="space-y-3">
              {/* Disciplines */}
              <div className="flex flex-wrap gap-1">
                {paper.subjects.map(subject => (
                  <span 
                    key={subject} 
                    className="bg-gray-100 text-gray-700 px-2 py-1 rounded-full text-xs"
                  >
                    {getSubjectName(subject)}
                  </span>
                ))}
              </div>
              
              {/* Download buttons */}
              <div className="flex gap-2">
                <Button
                  variant="outline"
                  size="sm"
                  fullWidth
                  leftIcon={<Download size={16} />}
                  onClick={() => window.open(paper.fileUrl, '_blank')}
                >
                  Prova
                </Button>
                <Button
                  variant="outline"
                  size="sm"
                  fullWidth
                  leftIcon={<CheckCircle size={16} />}
                  onClick={() => window.open(paper.answersUrl, '_blank')}
                >
                  Gabarito
                </Button>
              </div>
            </div>
          </div>
        ))}
      </div>
      
      {filteredPapers.length === 0 && (
        <div className="text-center py-8">
          <p className="text-gray-500">Nenhuma prova encontrada com os filtros selecionados.</p>
        </div>
      )}
    </div>
  );
};

export default ExamList;