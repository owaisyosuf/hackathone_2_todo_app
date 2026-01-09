import axios from 'axios';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

// Create axios instance with default config
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add request interceptor to include token in all requests
apiClient.interceptors.request.use(
  (config) => {
    // Only add token if we're in a browser environment (client-side)
    if (typeof window !== 'undefined') {
      const token = localStorage.getItem('token');
      if (token) {
        config.headers.Authorization = `Bearer ${token}`;
      }
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Add response interceptor to handle token expiration
apiClient.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    if (typeof window !== 'undefined' && error.response?.status === 401) {
      // Token might be expired, clear it and redirect to login
      localStorage.removeItem('token');
      window.location.href = '/';
    }
    return Promise.reject(error);
  }
);

export default apiClient;

// Auth API functions
export const authAPI = {
  register: (email: string, password: string) =>
    apiClient.post('/auth/register', { email, password }),

  login: (email: string, password: string) =>
    apiClient.post('/auth/login', { email, password }),

  logout: () => {
    if (typeof window !== 'undefined') {
      localStorage.removeItem('token');
    }
  }
};

// Task API functions
export const taskAPI = {
  getTasks: () => apiClient.get('/tasks'),

  createTask: (title: string, description?: string) =>
    apiClient.post('/tasks', { title, description }),

  updateTask: (taskId: string, title: string, description?: string, is_completed?: boolean) =>
    apiClient.put(`/tasks/${taskId}`, { title, description, is_completed }),

  toggleTask: (taskId: string) =>
    apiClient.patch(`/tasks/${taskId}/toggle`),

  deleteTask: (taskId: string) =>
    apiClient.delete(`/tasks/${taskId}`)
};