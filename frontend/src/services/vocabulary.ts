import api from './api';
import type {
  Word,
  UserWord,
  VocabularyStats,
  WordStatus,
  ReviewAnswer,
  ReviewResponse,
} from '@/types';

export const vocabularyService = {
  // Dictionary words
  async getWords(params?: {
    cefr_level?: string;
    part_of_speech?: string;
    search?: string;
    limit?: number;
    offset?: number;
  }): Promise<Word[]> {
    const response = await api.get<Word[]>('/vocabulary/words', { params });
    return response.data;
  },

  // User vocabulary
  async getMyWords(params?: {
    status?: WordStatus;
    cefr_level?: string;
    search?: string;
    limit?: number;
    offset?: number;
  }): Promise<UserWord[]> {
    const response = await api.get<UserWord[]>('/vocabulary/my-words', { params });
    return response.data;
  },

  async addWordToMyVocabulary(wordId: number): Promise<UserWord> {
    const response = await api.post<UserWord>('/vocabulary/my-words', {
      word_id: wordId,
    });
    return response.data;
  },

  async getMyWord(userWordId: number): Promise<UserWord> {
    const response = await api.get<UserWord>(`/vocabulary/my-words/${userWordId}`);
    return response.data;
  },

  async removeWordFromMyVocabulary(userWordId: number): Promise<void> {
    await api.delete(`/vocabulary/my-words/${userWordId}`);
  },

  // Review
  async getWordsForReview(limit: number = 20): Promise<UserWord[]> {
    const response = await api.get<UserWord[]>('/vocabulary/review', {
      params: { limit },
    });
    return response.data;
  },

  async submitReview(userWordId: number, quality: number): Promise<ReviewResponse> {
    const response = await api.post<ReviewResponse>(
      `/vocabulary/review/${userWordId}`,
      { quality } as ReviewAnswer
    );
    return response.data;
  },

  // Statistics
  async getStats(): Promise<VocabularyStats> {
    const response = await api.get<VocabularyStats>('/vocabulary/stats');
    return response.data;
  },
};

export default vocabularyService;
