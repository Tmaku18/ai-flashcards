import axios from 'axios';

// Create an axios instance
const api = axios.create({
  baseURL: '/api',
});

// Add a request interceptor to add the auth token to requests
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Add a response interceptor to handle errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    // Handle 401 Unauthorized errors by redirecting to login
    if (error.response && error.response.status === 401) {
      localStorage.removeItem('token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// Auth API
export const authAPI = {
  login: (username: string, password: string) =>
    api.post('/auth/login', { username, password }),

  register: (username: string, email: string, password: string) =>
    api.post('/auth/register', { username, email, password }),

  getCurrentUser: () =>
    api.get('/auth/me'),

  updateProfile: (data: { username?: string, email?: string }) =>
    api.put('/auth/update-profile', data),

  changePassword: (currentPassword: string, newPassword: string) =>
    api.put('/auth/change-password', { current_password: currentPassword, new_password: newPassword }),
};

// Flashcard Sets API
export const flashcardSetsAPI = {
  getAllSets: (skip = 0, limit = 100) =>
    api.get(`/flashcards/sets?skip=${skip}&limit=${limit}`),

  getSetById: (setId: number) =>
    api.get(`/flashcards/sets/${setId}`),

  createSet: (data: { title: string, description?: string }) =>
    api.post('/flashcards/sets', data),

  updateSet: (setId: number, data: { title?: string, description?: string }) =>
    api.put(`/flashcards/sets/${setId}`, data),

  deleteSet: (setId: number) =>
    api.delete(`/flashcards/sets/${setId}`),
};

// Flashcards API
export const flashcardsAPI = {
  getCardsBySetId: (setId: number, skip = 0, limit = 100) =>
    api.get(`/flashcards/sets/${setId}/cards?skip=${skip}&limit=${limit}`),

  createCard: (setId: number, data: { question: string, answer: string }) =>
    api.post(`/flashcards/sets/${setId}/cards`, data),

  updateCard: (setId: number, cardId: number, data: { question?: string, answer?: string }) =>
    api.put(`/flashcards/sets/${setId}/cards/${cardId}`, data),

  deleteCard: (setId: number, cardId: number) =>
    api.delete(`/flashcards/sets/${setId}/cards/${cardId}`),
};

// Study API
export const studyAPI = {
  startSession: (setId: number) =>
    api.post('/study/sessions/start', { set_id: setId }),

  endSession: (sessionId: number) =>
    api.put(`/study/sessions/${sessionId}/end`),

  getSessions: (skip = 0, limit = 100) =>
    api.get(`/study/sessions?skip=${skip}&limit=${limit}`),

  getSessionById: (sessionId: number) =>
    api.get(`/study/sessions/${sessionId}`),

  updateProgress: (sessionId: number, flashcardId: number, isCorrect: boolean, difficulty: string) =>
    api.post(`/study/sessions/${sessionId}/progress`, {
      flashcard_id: flashcardId,
      is_correct: isCorrect,
      difficulty
    }),

  getFlashcardProgress: (flashcardId: number) =>
    api.get(`/study/progress/flashcard/${flashcardId}`),

  getSetProgress: (setId: number) =>
    api.get(`/study/progress/set/${setId}`),

  getSetStats: (setId: number) =>
    api.get(`/study/stats/set/${setId}`),
};

// Document API
export const documentAPI = {
  uploadDocument: (formData: FormData) =>
    api.post('/documents/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    }),

  generateFlashcardsFromDocument: (documentId: string, title: string, description?: string) =>
    api.post('/ai/generate-from-document', {
      document_id: documentId,
      title,
      description
    }),
};

// AI API
export const aiAPI = {
  generateFlashcardsFromText: (text: string, numCards: number) =>
    api.post('/ai/generate-flashcards', {
      text,
      num_cards: numCards
    }),
};

// Dashboard API
export const dashboardAPI = {
  getSummary: () =>
    api.get('/dashboard/summary'),

  getActivity: (limit = 10) =>
    api.get(`/dashboard/activity?limit=${limit}`),

  getSetStatistics: () =>
    api.get('/dashboard/sets/stats'),

  getStudyTimeDistribution: () =>
    api.get('/dashboard/study-time'),
};

export default api;
