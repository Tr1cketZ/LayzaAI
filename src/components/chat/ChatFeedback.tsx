import React, { useState } from 'react';
import { Star } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import Button from '../ui/Button';
import { getStarFeedbackMessage } from '../../utils/helpers';
import { sendFeedback } from '../../services/api';
import toast from 'react-hot-toast';

interface ChatFeedbackProps {
  conversationId: string;
}

const ChatFeedback: React.FC<ChatFeedbackProps> = ({ conversationId }) => {
  const [rating, setRating] = useState<number | null>(null);
  const [hoveredRating, setHoveredRating] = useState<number | null>(null);
  const [isSubmitted, setIsSubmitted] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);
  
  const handleRatingClick = (value: number) => {
    setRating(value);
  };
  
  const handleRatingHover = (value: number | null) => {
    setHoveredRating(value);
  };
  
  const handleSubmitFeedback = async () => {
    if (rating === null) return;
    
    setIsSubmitting(true);
    try {
      await sendFeedback(rating, conversationId);
      setIsSubmitted(true);
      toast.success('Feedback enviado com sucesso! 🎉');
    } catch (error) {
      toast.error('Erro ao enviar feedback. Tente novamente.');
    } finally {
      setIsSubmitting(false);
    }
  };
  
  const displayValue = hoveredRating !== null ? hoveredRating : rating;
  
  return (
    <div className="border-t border-gray-200 pt-4 mt-6">
      <AnimatePresence mode="wait">
        {!isSubmitted ? (
          <motion.div
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -10 }}
            className="text-center"
            key="feedback-form"
          >
            <h3 className="text-sm font-medium text-gray-700 mb-2">
              O que achou da nossa conversa?
            </h3>
            <div className="flex justify-center space-x-1 mb-3">
              {[1, 2, 3, 4, 5].map((value) => (
                <button
                  key={value}
                  onClick={() => handleRatingClick(value)}
                  onMouseEnter={() => handleRatingHover(value)}
                  onMouseLeave={() => handleRatingHover(null)}
                  className="focus:outline-none transition-transform hover:scale-110"
                >
                  <Star
                    size={28}
                    className={`transition-colors ${
                      (displayValue !== null && value <= displayValue)
                        ? 'fill-yellow-400 text-yellow-400'
                        : 'text-gray-300'
                    }`}
                  />
                </button>
              ))}
            </div>
            {rating !== null && (
              <motion.div
                initial={{ opacity: 0, height: 0 }}
                animate={{ opacity: 1, height: 'auto' }}
                className="mb-3 text-sm text-primary-600 font-medium"
              >
                {getStarFeedbackMessage(rating as 1 | 2 | 3 | 4 | 5)}
              </motion.div>
            )}
            <Button
              variant="primary"
              size="sm"
              onClick={handleSubmitFeedback}
              disabled={rating === null || isSubmitting}
              isLoading={isSubmitting}
            >
              Enviar feedback
            </Button>
          </motion.div>
        ) : (
          <motion.div
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            key="feedback-thanks"
            className="text-center py-2"
          >
            <p className="text-primary-600 font-medium">
              Obrigada pelo seu feedback! 💜
            </p>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
};

export default ChatFeedback;