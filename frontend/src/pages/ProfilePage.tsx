import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuthStore } from '@/store/authStore';
import { SkillCard } from '@/components/common/SkillCard';
import { BookOpen, Pencil, Headphones, MessageSquare, LogOut, Bot, Globe, ChevronDown } from 'lucide-react';
import { authService } from '@/services/auth';
import type { AIProvider, SettingsOptions } from '@/types';

const AI_PROVIDER_LABELS: Record<AIProvider, string> = {
  claude: 'Claude (Anthropic)',
  openai: 'GPT (OpenAI)',
};

export function ProfilePage() {
  const { user, logout, updateUser, isLoading } = useAuthStore();
  const navigate = useNavigate();
  const [settingsOptions, setSettingsOptions] = useState<SettingsOptions | null>(null);
  const [isSaving, setIsSaving] = useState(false);

  useEffect(() => {
    authService.getSettingsOptions().then(setSettingsOptions).catch(console.error);
  }, []);

  const handleLogout = () => {
    logout();
    navigate('/login', { replace: true });
  };

  const handleAIProviderChange = async (provider: AIProvider) => {
    if (isSaving || provider === user?.preferred_ai_provider) return;
    setIsSaving(true);
    try {
      await updateUser({ preferred_ai_provider: provider });
    } catch (error) {
      console.error('Failed to update AI provider:', error);
    } finally {
      setIsSaving(false);
    }
  };

  const handleTimezoneChange = async (timezone: string) => {
    if (isSaving || timezone === user?.timezone) return;
    setIsSaving(true);
    try {
      await updateUser({ timezone });
    } catch (error) {
      console.error('Failed to update timezone:', error);
    } finally {
      setIsSaving(false);
    }
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

      {/* Settings */}
      <div>
        <h2 className="text-lg font-semibold mb-3">Settings</h2>
        <div className="space-y-3">
          {/* AI Provider Selection */}
          <div className="card">
            <div className="flex items-center gap-3 mb-3">
              <Bot className="w-5 h-5 text-primary-600" />
              <span className="font-medium">AI Provider</span>
            </div>
            <div className="relative">
              <select
                value={user?.preferred_ai_provider || 'claude'}
                onChange={(e) => handleAIProviderChange(e.target.value as AIProvider)}
                disabled={isSaving || isLoading || !settingsOptions}
                className="w-full appearance-none bg-gray-50 border border-gray-200 rounded-lg px-4 py-3 pr-10 focus:outline-none focus:ring-2 focus:ring-primary-500 disabled:opacity-50"
              >
                {settingsOptions?.ai_providers.map((provider) => (
                  <option key={provider} value={provider}>
                    {AI_PROVIDER_LABELS[provider]}
                  </option>
                ))}
              </select>
              <ChevronDown className="w-5 h-5 text-gray-400 absolute right-3 top-1/2 -translate-y-1/2 pointer-events-none" />
            </div>
            <p className="text-sm text-gray-500 mt-2">
              Choose which AI powers your chatbot conversations
            </p>
          </div>

          {/* Timezone Selection */}
          <div className="card">
            <div className="flex items-center gap-3 mb-3">
              <Globe className="w-5 h-5 text-primary-600" />
              <span className="font-medium">Timezone</span>
            </div>
            <div className="relative">
              <select
                value={user?.timezone || 'Europe/Stockholm'}
                onChange={(e) => handleTimezoneChange(e.target.value)}
                disabled={isSaving || isLoading || !settingsOptions}
                className="w-full appearance-none bg-gray-50 border border-gray-200 rounded-lg px-4 py-3 pr-10 focus:outline-none focus:ring-2 focus:ring-primary-500 disabled:opacity-50"
              >
                {settingsOptions?.timezones.map((tz) => (
                  <option key={tz} value={tz}>
                    {tz.replace(/_/g, ' ')}
                  </option>
                ))}
              </select>
              <ChevronDown className="w-5 h-5 text-gray-400 absolute right-3 top-1/2 -translate-y-1/2 pointer-events-none" />
            </div>
            <p className="text-sm text-gray-500 mt-2">
              Used for scheduling reviews and tracking streaks
            </p>
          </div>
        </div>
      </div>

      {/* Sign Out */}
      <div>
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
