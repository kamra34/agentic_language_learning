import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { ArrowLeft, Search, Plus, Check, Loader2 } from 'lucide-react';
import { vocabularyService } from '@/services/vocabulary';
import type { Word, CEFRLevel } from '@/types';

const CEFR_LEVELS: CEFRLevel[] = ['A1', 'A2', 'B1', 'B2', 'C1', 'C2'];

export function BrowseWordsPage() {
  const navigate = useNavigate();
  const [words, setWords] = useState<Word[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState('');
  const [cefrFilter, setCefrFilter] = useState<CEFRLevel | ''>('A1');
  const [addedWordIds, setAddedWordIds] = useState<Set<number>>(new Set());
  const [addingWordId, setAddingWordId] = useState<number | null>(null);

  useEffect(() => {
    loadWords();
  }, [cefrFilter, searchQuery]);

  const loadWords = async () => {
    setIsLoading(true);
    try {
      const wordsData = await vocabularyService.getWords({
        cefr_level: cefrFilter || undefined,
        search: searchQuery || undefined,
        limit: 50,
      });
      setWords(wordsData);
    } catch (error) {
      console.error('Failed to load words:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleAddWord = async (wordId: number) => {
    if (addedWordIds.has(wordId) || addingWordId === wordId) return;

    setAddingWordId(wordId);
    try {
      await vocabularyService.addWordToMyVocabulary(wordId);
      setAddedWordIds((prev) => new Set([...prev, wordId]));
    } catch (error) {
      console.error('Failed to add word:', error);
    } finally {
      setAddingWordId(null);
    }
  };

  const handleBack = () => {
    navigate('/vocabulary');
  };

  return (
    <div className="min-h-screen flex flex-col bg-gray-50">
      {/* Header */}
      <div className="px-4 py-3 bg-white border-b border-gray-200 flex items-center">
        <button onClick={handleBack} className="p-2 -ml-2">
          <ArrowLeft className="w-6 h-6" />
        </button>
        <h1 className="ml-2 text-lg font-semibold">Browse Words</h1>
      </div>

      {/* Search and Filters */}
      <div className="px-4 py-4 bg-white border-b border-gray-200 space-y-3">
        {/* Search */}
        <div className="relative">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
          <input
            type="text"
            placeholder="Search Swedish or English..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="w-full pl-10 pr-4 py-3 bg-gray-50 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
          />
        </div>

        {/* CEFR Filter */}
        <div className="flex gap-2 overflow-x-auto pb-1">
          <button
            onClick={() => setCefrFilter('')}
            className={`px-3 py-1.5 rounded-full text-sm whitespace-nowrap ${
              cefrFilter === '' ? 'bg-primary-600 text-white' : 'bg-gray-100 text-gray-700'
            }`}
          >
            All Levels
          </button>
          {CEFR_LEVELS.map((level) => (
            <button
              key={level}
              onClick={() => setCefrFilter(level)}
              className={`px-3 py-1.5 rounded-full text-sm whitespace-nowrap ${
                cefrFilter === level
                  ? 'bg-primary-600 text-white'
                  : 'bg-gray-100 text-gray-700'
              }`}
            >
              {level}
            </button>
          ))}
        </div>
      </div>

      {/* Word List */}
      <div className="flex-1 px-4 py-4">
        {isLoading ? (
          <div className="flex justify-center py-12">
            <Loader2 className="w-8 h-8 animate-spin text-primary-600" />
          </div>
        ) : words.length > 0 ? (
          <div className="space-y-2">
            {words.map((word) => {
              const isAdded = addedWordIds.has(word.id);
              const isAdding = addingWordId === word.id;

              return (
                <div
                  key={word.id}
                  className="card flex items-center justify-between"
                >
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center gap-2">
                      <span className="font-medium text-gray-900">
                        {word.swedish}
                      </span>
                      {word.gender && (
                        <span className="text-xs text-gray-500">
                          ({word.gender})
                        </span>
                      )}
                      <span className="text-xs px-1.5 py-0.5 bg-gray-100 text-gray-600 rounded">
                        {word.cefr_level}
                      </span>
                    </div>
                    <div className="text-sm text-gray-500 truncate">
                      {word.english}
                    </div>
                    {word.part_of_speech && (
                      <div className="text-xs text-gray-400">
                        {word.part_of_speech}
                      </div>
                    )}
                  </div>
                  <button
                    onClick={() => handleAddWord(word.id)}
                    disabled={isAdded || isAdding}
                    className={`p-2 rounded-lg transition-colors ${
                      isAdded
                        ? 'bg-green-100 text-green-600'
                        : 'bg-primary-100 text-primary-600 hover:bg-primary-200'
                    } disabled:opacity-50`}
                  >
                    {isAdding ? (
                      <Loader2 className="w-5 h-5 animate-spin" />
                    ) : isAdded ? (
                      <Check className="w-5 h-5" />
                    ) : (
                      <Plus className="w-5 h-5" />
                    )}
                  </button>
                </div>
              );
            })}
          </div>
        ) : (
          <div className="text-center py-12">
            <p className="text-gray-500">
              {searchQuery
                ? 'No words match your search'
                : 'No words available for this level'}
            </p>
          </div>
        )}
      </div>
    </div>
  );
}

export default BrowseWordsPage;
