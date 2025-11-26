import { BookOpen, Plus } from 'lucide-react';

export function VocabularyPage() {
  return (
    <div className="px-4 py-6 space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Vocabulary</h1>
          <p className="text-gray-600">Learn and review Swedish words</p>
        </div>
        <button className="btn-primary">
          <Plus className="w-5 h-5" />
        </button>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-3 gap-3">
        <div className="card text-center">
          <div className="text-2xl font-bold text-primary-600">0</div>
          <div className="text-sm text-gray-500">Due Today</div>
        </div>
        <div className="card text-center">
          <div className="text-2xl font-bold text-green-600">0</div>
          <div className="text-sm text-gray-500">Mastered</div>
        </div>
        <div className="card text-center">
          <div className="text-2xl font-bold text-gray-600">0</div>
          <div className="text-sm text-gray-500">Total</div>
        </div>
      </div>

      {/* Start Review Button */}
      <button className="btn-primary w-full py-4 text-lg">
        <BookOpen className="w-6 h-6 mr-2" />
        Start Review
      </button>

      {/* Empty State */}
      <div className="card text-center py-12">
        <BookOpen className="w-16 h-16 mx-auto text-gray-300 mb-4" />
        <h3 className="text-lg font-medium text-gray-700 mb-2">No words yet</h3>
        <p className="text-gray-500 mb-4">
          Start learning by adding words or chatting with a tutor
        </p>
        <button className="btn-secondary">Browse Word Lists</button>
      </div>
    </div>
  );
}

export default VocabularyPage;
