import api, { tokenStorage } from './api';
import type { LoginCredentials, RegisterData, TokenResponse, User, UserUpdate, SettingsOptions } from '@/types';

export const authService = {
  async login(credentials: LoginCredentials): Promise<TokenResponse> {
    const response = await api.post<TokenResponse>('/auth/login', credentials);
    tokenStorage.setTokens(response.data);
    return response.data;
  },

  async register(data: RegisterData): Promise<TokenResponse> {
    const response = await api.post<TokenResponse>('/auth/register', data);
    tokenStorage.setTokens(response.data);
    return response.data;
  },

  async getCurrentUser(): Promise<User> {
    const response = await api.get<User>('/auth/me');
    return response.data;
  },

  async updateUser(data: UserUpdate): Promise<User> {
    const response = await api.patch<User>('/auth/me', data);
    return response.data;
  },

  async getSettingsOptions(): Promise<SettingsOptions> {
    const response = await api.get<SettingsOptions>('/auth/settings/options');
    return response.data;
  },

  async refreshToken(): Promise<TokenResponse> {
    const refreshToken = tokenStorage.getRefreshToken();
    if (!refreshToken) {
      throw new Error('No refresh token available');
    }

    const response = await api.post<TokenResponse>('/auth/refresh', {
      refresh_token: refreshToken,
    });
    tokenStorage.setTokens(response.data);
    return response.data;
  },

  logout(): void {
    tokenStorage.clearTokens();
  },

  isAuthenticated(): boolean {
    return !!tokenStorage.getAccessToken();
  },
};

export default authService;
