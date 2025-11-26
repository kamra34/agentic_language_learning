import { GraduationCap, Lock } from 'lucide-react';

const grammarTopics = [
  { id: 1, title: 'Word Order (V2 Rule)', level: 'A1', unlocked: true, progress: 0 },
  { id: 2, title: 'En & Ett Words', level: 'A1', unlocked: true, progress: 0 },
  { id: 3, title: 'Definite Forms', level: 'A1', unlocked: false, progress: 0 },
  { id: 4, title: 'Present Tense', level: 'A1', unlocked: false, progress: 0 },
  { id: 5, title: 'Past Tense', level: 'A2', unlocked: false, progress: 0 },
  { id: 6, title: 'Perfect Tense', level: 'A2', unlocked: false, progress: 0 },
  { id: 7, title: 'Adjective Agreement', level: 'A2', unlocked: false, progress: 0 },
  { id: 8, title: 'Pronouns', level: 'B1', unlocked: false, progress: 0 },
];

export function GrammarPage() {
  return (
    <div className="px-4 py-6 space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-2xl font-bold text-gray-900">Grammar</h1>
        <p className="text-gray-600">Master Swedish grammar step by step</p>
      </div>

      {/* Progress Overview */}
      <div className="card">
        <div className="flex items-center justify-between mb-2">
          <span className="font-medium">Overall Progress</span>
          <span className="text-sm text-gray-500">0 / {grammarTopics.length} topics</span>
        </div>
        <div className="h-2 bg-gray-100 rounded-full overflow-hidden">
          <div className="h-full bg-primary-500 rounded-full" style={{ width: '0%' }} />
        </div>
      </div>

      {/* Topics List */}
      <div className="space-y-3">
        {grammarTopics.map((topic) => (
          <div
            key={topic.id}
            className={`card flex items-center gap-4 ${
              topic.unlocked ? 'cursor-pointer active:bg-gray-50' : 'opacity-60'
            }`}
          >
            <div
              className={`w-12 h-12 rounded-full flex items-center justify-center ${
                topic.unlocked ? 'bg-primary-100' : 'bg-gray-100'
              }`}
            >
              {topic.unlocked ? (
                <GraduationCap className="w-6 h-6 text-primary-600" />
              ) : (
                <Lock className="w-5 h-5 text-gray-400" />
              )}
            </div>
            <div className="flex-1">
              <div className="font-medium">{topic.title}</div>
              <div className="text-sm text-gray-500">Level {topic.level}</div>
            </div>
            {topic.unlocked && (
              <div className="text-sm text-primary-600 font-medium">Start →</div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}

export default GrammarPage;
