import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { BookOpen, Plus, Search, ChevronRight, Loader2 } from 'lucide-react';
import { vocabularyService } from '@/services/vocabulary';
import type { VocabularyStats, UserWord, WordStatus } from '@/types';

const STATUS_COLORS: Record<WordStatus, string> = {
  new: 'bg-blue-100 text-blue-700',
  learning: 'bg-yellow-100 text-yellow-700',
  familiar: 'bg-green-100 text-green-700',
  mastered: 'bg-emerald-100 text-emerald-700',
  review_needed: 'bg-red-100 text-red-700',
};

const STATUS_LABELS: Record<WordStatus, string> = {
  new: 'New',
  learning: 'Learning',
  familiar: 'Familiar',
  mastered: 'Mastered',
  review_needed: 'Review',
};

export function VocabularyPage() {
  const navigate = useNavigate();
  const [stats, setStats] = useState<VocabularyStats | null>(null);
  const [words, setWords] = useState<UserWord[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState('');
  const [statusFilter, setStatusFilter] = useState<WordStatus | ''>('');

  useEffect(() => {
    loadData();
  }, [statusFilter, searchQuery]);

  const loadData = async () => {
    setIsLoading(true);
    try {
      const [statsData, wordsData] = await Promise.all([
        vocabularyService.getStats(),
        vocabularyService.getMyWords({
          status: statusFilter || undefined,
          search: searchQuery || undefined,
          limit: 50,
        }),
      ]);
      setStats(statsData);
      setWords(wordsData);
    } catch (error) {
      console.error('Failed to load vocabulary:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleStartReview = () => {
    navigate('/vocabulary/review');
  };

  const handleBrowseWords = () => {
    navigate('/vocabulary/browse');
  };

  return (
    <div className="px-4 py-6 space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Vocabulary</h1>
          <p className="text-gray-600">Learn and review Swedish words</p>
        </div>
        <button onClick={handleBrowseWords} className="btn-primary">
          <Plus className="w-5 h-5" />
        </button>
      </div>

      {/* Stats */}
      {stats && (
        <div className="grid grid-cols-3 gap-3">
          <div className="card text-center">
            <div className="text-2xl font-bold text-primary-600">{stats.due_for_review}</div>
            <div className="text-sm text-gray-500">Due Today</div>
          </div>
          <div className="card text-center">
            <div className="text-2xl font-bold text-green-600">{stats.mastered}</div>
            <div className="text-sm text-gray-500">Mastered</div>
          </div>
          <div className="card text-center">
            <div className="text-2xl font-bold text-gray-600">{stats.total_words}</div>
            <div className="text-sm text-gray-500">Total</div>
          </div>
        </div>
      )}

      {/* Start Review Button */}
      {stats && stats.due_for_review > 0 && (
        <button
          onClick={handleStartReview}
          className="btn-primary w-full py-4 text-lg"
        >
          <BookOpen className="w-6 h-6 mr-2" />
          Start Review ({stats.due_for_review} cards)
        </button>
      )}

      {/* Search and Filter */}
      {stats && stats.total_words > 0 && (
        <div className="space-y-3">
          {/* Search */}
          <div className="relative">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
            <input
              type="text"
              placeholder="Search words..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full pl-10 pr-4 py-3 bg-white border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
            />
          </div>

          {/* Status Filter */}
          <div className="flex gap-2 overflow-x-auto pb-2">
            <button
              onClick={() => setStatusFilter('')}
              className={`px-3 py-1.5 rounded-full text-sm whitespace-nowrap ${
                statusFilter === '' ? 'bg-primary-600 text-white' : 'bg-gray-100 text-gray-700'
              }`}
            >
              All
            </button>
            {(['new', 'learning', 'familiar', 'mastered', 'review_needed'] as WordStatus[]).map(
              (status) => (
                <button
                  key={status}
                  onClick={() => setStatusFilter(status)}
                  className={`px-3 py-1.5 rounded-full text-sm whitespace-nowrap ${
                    statusFilter === status
                      ? 'bg-primary-600 text-white'
                      : 'bg-gray-100 text-gray-700'
                  }`}
                >
                  {STATUS_LABELS[status]}
                </button>
              )
            )}
          </div>
        </div>
      )}

      {/* Word List */}
      {isLoading ? (
        <div className="flex justify-center py-12">
          <Loader2 className="w-8 h-8 animate-spin text-primary-600" />
        </div>
      ) : words.length > 0 ? (
        <div className="space-y-2">
          {words.map((userWord) => (
            <div
              key={userWord.id}
              className="card-touch flex items-center justify-between"
            >
              <div className="flex-1 min-w-0">
                <div className="flex items-center gap-2">
                  <span className="font-medium text-gray-900">
                    {userWord.word.swedish}
                  </span>
                  {userWord.word.gender && (
                    <span className="text-xs text-gray-500">
                      ({userWord.word.gender})
                    </span>
                  )}
                </div>
                <div className="text-sm text-gray-500 truncate">
                  {userWord.word.english}
                </div>
              </div>
              <div className="flex items-center gap-2">
                <span
                  className={`px-2 py-0.5 rounded text-xs font-medium ${
                    STATUS_COLORS[userWord.status as WordStatus]
                  }`}
                >
                  {STATUS_LABELS[userWord.status as WordStatus]}
                </span>
                <ChevronRight className="w-5 h-5 text-gray-400" />
              </div>
            </div>
          ))}
        </div>
      ) : stats && stats.total_words === 0 ? (
        /* Empty State - No words at all */
        <div className="card text-center py-12">
          <BookOpen className="w-16 h-16 mx-auto text-gray-300 mb-4" />
          <h3 className="text-lg font-medium text-gray-700 mb-2">No words yet</h3>
          <p className="text-gray-500 mb-4">
            Start learning by adding words from the dictionary
          </p>
          <button onClick={handleBrowseWords} className="btn-secondary">
            Browse Word Lists
          </button>
        </div>
      ) : (
        /* Empty State - No results for filter */
        <div className="card text-center py-8">
          <p className="text-gray-500">No words match your search</p>
        </div>
      )}
    </div>
  );
}

export default VocabularyPage;
