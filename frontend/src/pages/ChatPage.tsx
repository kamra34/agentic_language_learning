import { useState } from 'react';
import { useSearchParams } from 'react-router-dom';
import { Send, MessageSquare, Pencil, BookA, Languages, BookOpen } from 'lucide-react';
import { clsx } from 'clsx';
import type { BotType } from '@/types';

const bots: Array<{
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
    description: 'Practice free conversation at your level',
    icon: <MessageSquare className="w-6 h-6" />,
    color: 'bg-blue-500',
  },
  {
    type: 'writing',
    name: 'Writing Teacher',
    swedishName: 'Skrivläraren',
    description: 'Get feedback on your writing',
    icon: <Pencil className="w-6 h-6" />,
    color: 'bg-green-500',
  },
  {
    type: 'grammar',
    name: 'Grammar Teacher',
    swedishName: 'Grammatikläraren',
    description: 'Learn grammar rules with examples',
    icon: <BookA className="w-6 h-6" />,
    color: 'bg-purple-500',
  },
  {
    type: 'vocabulary',
    name: 'Word Teacher',
    swedishName: 'Ordläraren',
    description: 'Learn new words in context',
    icon: <BookOpen className="w-6 h-6" />,
    color: 'bg-yellow-500',
  },
  {
    type: 'translator',
    name: 'Translator',
    swedishName: 'Översättaren',
    description: 'Translation with explanations',
    icon: <Languages className="w-6 h-6" />,
    color: 'bg-orange-500',
  },
];

export function ChatPage() {
  const [searchParams, setSearchParams] = useSearchParams();
  const selectedBot = searchParams.get('bot') as BotType | null;
  const [message, setMessage] = useState('');

  const currentBot = bots.find((b) => b.type === selectedBot);

  const handleSelectBot = (botType: BotType) => {
    setSearchParams({ bot: botType });
  };

  const handleSendMessage = (e: React.FormEvent) => {
    e.preventDefault();
    if (!message.trim() || !selectedBot) return;

    // TODO: Implement actual chat functionality
    console.log('Send message:', message);
    setMessage('');
  };

  // Bot selection view
  if (!selectedBot) {
    return (
      <div className="px-4 py-6 space-y-6">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">AI Tutors</h1>
          <p className="text-gray-600">Choose a tutor to start learning</p>
        </div>

        <div className="space-y-3">
          {bots.map((bot) => (
            <button
              key={bot.type}
              onClick={() => handleSelectBot(bot.type)}
              className="card-touch w-full flex items-center gap-4 text-left"
            >
              <div
                className={`w-14 h-14 rounded-full flex items-center justify-center text-white ${bot.color}`}
              >
                {bot.icon}
              </div>
              <div className="flex-1">
                <div className="font-semibold">{bot.name}</div>
                <div className="text-sm text-primary-600">{bot.swedishName}</div>
                <div className="text-sm text-gray-500 mt-1">{bot.description}</div>
              </div>
            </button>
          ))}
        </div>
      </div>
    );
  }

  // Chat view
  return (
    <div className="flex flex-col h-[calc(100vh-4rem)]">
      {/* Chat Header */}
      <div className="px-4 py-3 bg-white border-b border-gray-200 flex items-center gap-3">
        <button
          onClick={() => setSearchParams({})}
          className="text-gray-500 hover:text-gray-700"
        >
          ←
        </button>
        <div
          className={`w-10 h-10 rounded-full flex items-center justify-center text-white ${currentBot?.color}`}
        >
          {currentBot?.icon}
        </div>
        <div>
          <div className="font-medium">{currentBot?.name}</div>
          <div className="text-sm text-gray-500">{currentBot?.swedishName}</div>
        </div>
      </div>

      {/* Messages Area */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {/* Welcome message */}
        <div className="flex gap-3">
          <div
            className={`w-8 h-8 rounded-full flex items-center justify-center text-white shrink-0 ${currentBot?.color}`}
          >
            {currentBot?.icon}
          </div>
          <div className="bg-gray-100 rounded-2xl rounded-tl-none px-4 py-3 max-w-[80%]">
            <p>
              Hej! I'm your {currentBot?.name}. How can I help you learn Swedish today?
            </p>
          </div>
        </div>
      </div>

      {/* Input Area */}
      <form
        onSubmit={handleSendMessage}
        className="px-4 py-3 bg-white border-t border-gray-200 safe-bottom"
      >
        <div className="flex gap-2">
          <input
            type="text"
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            placeholder="Type a message..."
            className="input flex-1"
          />
          <button
            type="submit"
            disabled={!message.trim()}
            className={clsx(
              'btn w-12 h-12 p-0',
              message.trim() ? 'btn-primary' : 'btn-secondary opacity-50'
            )}
          >
            <Send className="w-5 h-5" />
          </button>
        </div>
      </form>
    </div>
  );
}

export default ChatPage;
