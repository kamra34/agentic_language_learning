// User types
export type CEFRLevel = 'A1' | 'A2' | 'B1' | 'B2' | 'C1' | 'C2';
export type AIProvider = 'claude' | 'openai';

export interface User {
  id: number;
  email: string;
  display_name: string | null;
  reading_level: CEFRLevel;
  writing_level: CEFRLevel;
  listening_level: CEFRLevel;
  speaking_level: CEFRLevel;
  preferred_ai_provider: AIProvider;
  timezone: string;
  is_active: boolean;
  created_at: string;
}

export interface UserUpdate {
  display_name?: string;
  preferred_ai_provider?: AIProvider;
  timezone?: string;
}

export interface SettingsOptions {
  ai_providers: AIProvider[];
  timezones: string[];
}

export interface UserSkillLevels {
  reading: CEFRLevel;
  writing: CEFRLevel;
  listening: CEFRLevel;
  speaking: CEFRLevel;
}

// Auth types
export interface TokenResponse {
  access_token: string;
  refresh_token: string;
  token_type: string;
}

export interface LoginCredentials {
  email: string;
  password: string;
}

export interface RegisterData {
  email: string;
  password: string;
  display_name?: string;
}

// Word types
export type WordStatus = 'new' | 'learning' | 'familiar' | 'mastered' | 'review_needed';
export type Gender = 'en' | 'ett';
export type PartOfSpeech =
  | 'noun'
  | 'verb'
  | 'adjective'
  | 'adverb'
  | 'pronoun'
  | 'preposition'
  | 'conjunction'
  | 'interjection'
  | 'numeral';

export interface Word {
  id: number;
  swedish: string;
  english: string;
  pronunciation: string | null;
  part_of_speech: PartOfSpeech | null;
  gender: Gender | null;
  cefr_level: CEFRLevel;
  frequency_rank: number | null;
  example_sv: string | null;
  example_en: string | null;
  notes: string | null;
  created_at: string;
}

export interface UserWord {
  id: number;
  word_id: number;
  status: WordStatus;
  times_seen: number;
  times_correct: number;
  times_incorrect: number;
  ease_factor: number;
  interval_days: number;
  last_reviewed: string | null;
  next_review: string | null;
  user_notes: string | null;
  created_at: string;
  word: Word;
}

export interface VocabularyStats {
  total_words: number;
  new: number;
  learning: number;
  familiar: number;
  mastered: number;
  review_needed: number;
  due_for_review: number;
}

export interface ReviewAnswer {
  quality: number; // 0-5: 0=blackout, 5=perfect
}

export interface ReviewResponse {
  user_word_id: number;
  new_status: WordStatus;
  next_review: string;
  interval_days: number;
}

// Chat types
export type BotType = 'conversation' | 'grammar' | 'writing' | 'vocabulary' | 'translator';
export type MessageRole = 'user' | 'assistant' | 'system';

export interface ChatMessage {
  id: number;
  role: MessageRole;
  content: string;
  created_at: string;
}

export interface ChatSession {
  id: number;
  bot_type: BotType;
  title: string | null;
  message_count: number;
  created_at: string;
  updated_at: string;
}

export interface ChatSessionWithMessages extends ChatSession {
  messages: ChatMessage[];
}

export interface BotInfo {
  type: BotType;
  name: string;
  swedish_name: string;
  description: string;
  icon: string;
}

// API Response types
export interface ApiError {
  error: {
    code: string;
    message: string;
    details?: unknown;
  };
}
