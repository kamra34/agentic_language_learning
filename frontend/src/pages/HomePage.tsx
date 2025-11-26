import { useEffect } from 'react';
import { Link } from 'react-router-dom';
import { BookOpen, MessageSquare, Pencil, BookA, Languages } from 'lucide-react';
import { useAuthStore } from '@/store/authStore';
import { SkillCard } from '@/components/common/SkillCard';
import type { BotType } from '@/types';

const botCards: Array<{
  type: BotType;
  name: string;
  swedishName: string;
  description: string;
  icon: React.ReactNode;
  color: string;
}> = [
  {
    type: 'conversation',
    name: 'Conversation Partner',
    swedishName: 'Samtalspartner',
    description: 'Practice free conversation',
    icon: <MessageSquare className="w-6 h-6" />,
    color: 'bg-blue-100 text-blue-600',
  },
  {
    type: 'writing',
    name: 'Writing Teacher',
    swedishName: 'Skrivläraren',
    description: 'Improve your writing',
    icon: <Pencil className="w-6 h-6" />,
    color: 'bg-green-100 text-green-600',
  },
  {
    type: 'grammar',
    name: 'Grammar Teacher',
    swedishName: 'Grammatikläraren',
    description: 'Learn grammar rules',
    icon: <BookA className="w-6 h-6" />,
    color: 'bg-purple-100 text-purple-600',
  },
  {
    type: 'translator',
    name: 'Translator',
    swedishName: 'Översättaren',
    description: 'Translation help',
    icon: <Languages className="w-6 h-6" />,
    color: 'bg-orange-100 text-orange-600',
  },
];

export function HomePage() {
  const { user, fetchUser } = useAuthStore();

  useEffect(() => {
    fetchUser();
  }, [fetchUser]);

  return (
    <div className="px-4 py-6 space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-2xl font-bold text-gray-900">
          Hej{user?.display_name ? `, ${user.display_name}` : ''}! 👋
        </h1>
        <p className="text-gray-600">Ready to learn some Swedish?</p>
      </div>

      {/* Quick Actions */}
      <div className="grid grid-cols-2 gap-3">
        <Link to="/vocabulary" className="card-touch flex flex-col items-center py-6">
          <div className="w-12 h-12 bg-primary-100 rounded-full flex items-center justify-center mb-2">
            <BookOpen className="w-6 h-6 text-primary-600" />
          </div>
          <span className="font-medium">Vocabulary</span>
          <span className="text-sm text-gray-500">Review words</span>
        </Link>

        <Link to="/chat" className="card-touch flex flex-col items-center py-6">
          <div className="w-12 h-12 bg-green-100 rounded-full flex items-center justify-center mb-2">
            <MessageSquare className="w-6 h-6 text-green-600" />
          </div>
          <span className="font-medium">Chat</span>
          <span className="text-sm text-gray-500">Practice speaking</span>
        </Link>
      </div>

      {/* Skill Levels */}
      {user && (
        <div>
          <h2 className="text-lg font-semibold mb-3">Your CEFR Levels</h2>
          <div className="grid grid-cols-2 gap-3">
            <SkillCard
              skill="Reading"
              level={user.reading_level}
              icon={<BookOpen className="w-4 h-4" />}
            />
            <SkillCard
              skill="Writing"
              level={user.writing_level}
              icon={<Pencil className="w-4 h-4" />}
            />
            <SkillCard
              skill="Listening"
              level={user.listening_level}
              icon={<BookA className="w-4 h-4" />}
            />
            <SkillCard
              skill="Speaking"
              level={user.speaking_level}
              icon={<MessageSquare className="w-4 h-4" />}
            />
          </div>
        </div>
      )}

      {/* AI Tutors */}
      <div>
        <h2 className="text-lg font-semibold mb-3">AI Tutors</h2>
        <div className="space-y-3">
          {botCards.map((bot) => (
            <Link
              key={bot.type}
              to={`/chat?bot=${bot.type}`}
              className="card-touch flex items-center gap-4"
            >
              <div className={`w-12 h-12 rounded-full flex items-center justify-center ${bot.color}`}>
                {bot.icon}
              </div>
              <div className="flex-1">
                <div className="font-medium">{bot.name}</div>
                <div className="text-sm text-gray-500">{bot.swedishName}</div>
              </div>
              <div className="text-gray-400">→</div>
            </Link>
          ))}
        </div>
      </div>
    </div>
  );
}

export default HomePage;
