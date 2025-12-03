import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

export const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Types
export interface Category {
  id: number
  name: string
  description?: string
  color: string
  icon?: string
}

export interface Budget {
  id: number
  category_id: number
  amount: number
  period: string
  start_date: string
  end_date?: string
  category?: Category
}

export interface Transaction {
  id: number
  category_id: number
  amount: number
  description?: string
  date: string
  type: string
  category?: Category
}

// API functions
export const categoriesApi = {
  getAll: () => apiClient.get<Category[]>('/api/categories/'),
  getById: (id: number) => apiClient.get<Category>(`/api/categories/${id}`),
  create: (data: Omit<Category, 'id'>) => apiClient.post<Category>('/api/categories/', data),
  update: (id: number, data: Partial<Category>) => apiClient.put<Category>(`/api/categories/${id}`, data),
  delete: (id: number) => apiClient.delete(`/api/categories/${id}`),
}

export const budgetsApi = {
  getAll: () => apiClient.get<Budget[]>('/api/budgets/'),
  getById: (id: number) => apiClient.get<Budget>(`/api/budgets/${id}`),
  create: (data: Omit<Budget, 'id' | 'category'>) => apiClient.post<Budget>('/api/budgets/', data),
  update: (id: number, data: Partial<Budget>) => apiClient.put<Budget>(`/api/budgets/${id}`, data),
  delete: (id: number) => apiClient.delete(`/api/budgets/${id}`),
}

export const transactionsApi = {
  getAll: (params?: { category_id?: number; start_date?: string; end_date?: string }) =>
    apiClient.get<Transaction[]>('/api/transactions/', { params }),
  getById: (id: number) => apiClient.get<Transaction>(`/api/transactions/${id}`),
  create: (data: Omit<Transaction, 'id' | 'category'>) => apiClient.post<Transaction>('/api/transactions/', data),
  update: (id: number, data: Partial<Transaction>) => apiClient.put<Transaction>(`/api/transactions/${id}`, data),
  delete: (id: number) => apiClient.delete(`/api/transactions/${id}`),
}

