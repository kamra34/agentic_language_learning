import { useAuthStore } from '@/store/authStore';
import { SkillCard } from '@/components/common/SkillCard';
import { BookOpen, Pencil, Headphones, MessageSquare, LogOut, Settings } from 'lucide-react';

export function ProfilePage() {
  const { user, logout } = useAuthStore();

  const handleLogout = () => {
    logout();
  };

  return (
    <div className="px-4 py-6 space-y-6">
      {/* Profile Header */}
      <div className="card text-center">
        <div className="w-20 h-20 bg-primary-100 rounded-full flex items-center justify-center mx-auto mb-3">
          <span className="text-3xl font-bold text-primary-600">
            {user?.display_name?.[0]?.toUpperCase() || user?.email?.[0]?.toUpperCase() || '?'}
          </span>
        </div>
        <h1 className="text-xl font-bold">{user?.display_name || 'Swedish Learner'}</h1>
        <p className="text-gray-500">{user?.email}</p>
        <p className="text-sm text-gray-400 mt-1">
          Member since{' '}
          {user?.created_at
            ? new Date(user.created_at).toLocaleDateString()
            : 'Unknown'}
        </p>
      </div>

      {/* CEFR Levels */}
      {user && (
        <div>
          <h2 className="text-lg font-semibold mb-3">CEFR Levels</h2>
          <div className="space-y-3">
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
              icon={<Headphones className="w-4 h-4" />}
            />
            <SkillCard
              skill="Speaking"
              level={user.speaking_level}
              icon={<MessageSquare className="w-4 h-4" />}
            />
          </div>
        </div>
      )}

      {/* Actions */}
      <div className="space-y-3">
        <button className="card-touch w-full flex items-center gap-4 text-left">
          <Settings className="w-5 h-5 text-gray-500" />
          <span>Settings</span>
        </button>

        <button
          onClick={handleLogout}
          className="card-touch w-full flex items-center gap-4 text-left text-red-600"
        >
          <LogOut className="w-5 h-5" />
          <span>Sign out</span>
        </button>
      </div>
    </div>
  );
}

export default ProfilePage;
