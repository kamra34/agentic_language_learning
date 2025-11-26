import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { ArrowLeft, Check, X, Eye, RotateCcw, Loader2 } from 'lucide-react';
import { vocabularyService } from '@/services/vocabulary';
import type { UserWord } from '@/types';

type ReviewState = 'loading' | 'question' | 'answer' | 'complete';

export function ReviewPage() {
  const navigate = useNavigate();
  const [cards, setCards] = useState<UserWord[]>([]);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [reviewState, setReviewState] = useState<ReviewState>('loading');
  const [sessionStats, setSessionStats] = useState({ correct: 0, incorrect: 0 });

  const currentCard = cards[currentIndex];

  useEffect(() => {
    loadCards();
  }, []);

  const loadCards = async () => {
    setReviewState('loading');
    try {
      const dueCards = await vocabularyService.getWordsForReview(20);
      if (dueCards.length === 0) {
        setReviewState('complete');
      } else {
        setCards(dueCards);
        setReviewState('question');
      }
    } catch (error) {
      console.error('Failed to load review cards:', error);
      navigate('/vocabulary');
    }
  };

  const handleShowAnswer = () => {
    setReviewState('answer');
  };

  const handleAnswer = async (quality: number) => {
    if (!currentCard) return;

    try {
      await vocabularyService.submitReview(currentCard.id, quality);

      // Update session stats
      if (quality >= 3) {
        setSessionStats((prev) => ({ ...prev, correct: prev.correct + 1 }));
      } else {
        setSessionStats((prev) => ({ ...prev, incorrect: prev.incorrect + 1 }));
      }

      // Move to next card
      if (currentIndex < cards.length - 1) {
        setCurrentIndex((prev) => prev + 1);
        setReviewState('question');
      } else {
        setReviewState('complete');
      }
    } catch (error) {
      console.error('Failed to submit review:', error);
    }
  };

  const handleBack = () => {
    navigate('/vocabulary');
  };

  const handleRestart = () => {
    setCurrentIndex(0);
    setSessionStats({ correct: 0, incorrect: 0 });
    loadCards();
  };

  // Loading state
  if (reviewState === 'loading') {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <Loader2 className="w-8 h-8 animate-spin text-primary-600" />
      </div>
    );
  }

  // Complete state
  if (reviewState === 'complete') {
    const total = sessionStats.correct + sessionStats.incorrect;
    const accuracy = total > 0 ? Math.round((sessionStats.correct / total) * 100) : 0;

    return (
      <div className="min-h-screen flex flex-col">
        {/* Header */}
        <div className="px-4 py-3 border-b border-gray-200 flex items-center">
          <button onClick={handleBack} className="p-2 -ml-2">
            <ArrowLeft className="w-6 h-6" />
          </button>
          <h1 className="ml-2 text-lg font-semibold">Review Complete</h1>
        </div>

        {/* Results */}
        <div className="flex-1 flex flex-col items-center justify-center px-6">
          <div className="text-6xl mb-4">🎉</div>
          <h2 className="text-2xl font-bold mb-2">Great job!</h2>
          <p className="text-gray-600 mb-8 text-center">
            {total > 0
              ? `You reviewed ${total} cards with ${accuracy}% accuracy`
              : 'No cards were due for review'}
          </p>

          {total > 0 && (
            <div className="grid grid-cols-2 gap-4 w-full max-w-xs mb-8">
              <div className="card text-center">
                <div className="text-2xl font-bold text-green-600">
                  {sessionStats.correct}
                </div>
                <div className="text-sm text-gray-500">Correct</div>
              </div>
              <div className="card text-center">
                <div className="text-2xl font-bold text-red-600">
                  {sessionStats.incorrect}
                </div>
                <div className="text-sm text-gray-500">Needs Work</div>
              </div>
            </div>
          )}

          <div className="space-y-3 w-full max-w-xs">
            <button onClick={handleRestart} className="btn-primary w-full">
              <RotateCcw className="w-5 h-5 mr-2" />
              Review Again
            </button>
            <button onClick={handleBack} className="btn-secondary w-full">
              Back to Vocabulary
            </button>
          </div>
        </div>
      </div>
    );
  }

  // Review state (question or answer)
  return (
    <div className="min-h-screen flex flex-col bg-gray-50">
      {/* Header */}
      <div className="px-4 py-3 bg-white border-b border-gray-200 flex items-center justify-between">
        <button onClick={handleBack} className="p-2 -ml-2">
          <ArrowLeft className="w-6 h-6" />
        </button>
        <div className="text-sm text-gray-600">
          {currentIndex + 1} / {cards.length}
        </div>
        <div className="w-10" /> {/* Spacer for centering */}
      </div>

      {/* Progress bar */}
      <div className="h-1 bg-gray-200">
        <div
          className="h-full bg-primary-600 transition-all duration-300"
          style={{ width: `${((currentIndex + 1) / cards.length) * 100}%` }}
        />
      </div>

      {/* Card */}
      <div className="flex-1 flex flex-col items-center justify-center px-6 py-8">
        <div className="card w-full max-w-md text-center py-12">
          {/* Swedish word */}
          <div className="mb-2">
            <span className="text-3xl font-bold text-gray-900">
              {currentCard?.word.swedish}
            </span>
            {currentCard?.word.gender && (
              <span className="ml-2 text-lg text-gray-500">
                ({currentCard.word.gender})
              </span>
            )}
          </div>

          {/* Pronunciation */}
          {currentCard?.word.pronunciation && (
            <div className="text-gray-500 mb-4">
              [{currentCard.word.pronunciation}]
            </div>
          )}

          {/* Part of speech */}
          {currentCard?.word.part_of_speech && (
            <div className="text-sm text-gray-400 mb-6">
              {currentCard.word.part_of_speech}
            </div>
          )}

          {/* Answer section */}
          {reviewState === 'answer' && (
            <div className="border-t border-gray-200 pt-6 mt-6">
              <div className="text-2xl text-gray-700 mb-4">
                {currentCard?.word.english}
              </div>

              {/* Example sentence */}
              {currentCard?.word.example_sv && (
                <div className="text-sm text-gray-500 space-y-1">
                  <div className="italic">{currentCard.word.example_sv}</div>
                  {currentCard.word.example_en && (
                    <div>{currentCard.word.example_en}</div>
                  )}
                </div>
              )}
            </div>
          )}
        </div>
      </div>

      {/* Action buttons */}
      <div className="px-6 pb-8 safe-bottom">
        {reviewState === 'question' ? (
          <button
            onClick={handleShowAnswer}
            className="btn-primary w-full py-4 text-lg"
          >
            <Eye className="w-5 h-5 mr-2" />
            Show Answer
          </button>
        ) : (
          <div className="space-y-3">
            <p className="text-center text-sm text-gray-500 mb-2">
              How well did you know this?
            </p>
            <div className="grid grid-cols-2 gap-3">
              <button
                onClick={() => handleAnswer(1)}
                className="flex items-center justify-center gap-2 py-4 bg-red-100 text-red-700 rounded-lg font-medium hover:bg-red-200 transition-colors"
              >
                <X className="w-5 h-5" />
                Didn't know
              </button>
              <button
                onClick={() => handleAnswer(3)}
                className="flex items-center justify-center gap-2 py-4 bg-yellow-100 text-yellow-700 rounded-lg font-medium hover:bg-yellow-200 transition-colors"
              >
                Hard
              </button>
              <button
                onClick={() => handleAnswer(4)}
                className="flex items-center justify-center gap-2 py-4 bg-green-100 text-green-700 rounded-lg font-medium hover:bg-green-200 transition-colors"
              >
                Good
              </button>
              <button
                onClick={() => handleAnswer(5)}
                className="flex items-center justify-center gap-2 py-4 bg-emerald-100 text-emerald-700 rounded-lg font-medium hover:bg-emerald-200 transition-colors"
              >
                <Check className="w-5 h-5" />
                Easy
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default ReviewPage;
