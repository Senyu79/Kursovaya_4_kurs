import axios from 'axios'

const api = axios.create({
  baseURL: 'http://127.0.0.1:8000/api',
  headers: {
    'Content-Type': 'application/json',
  },
})

export const clientsApi = {
  getAll: () => api.get('/clients/'),
  create: (data) => api.post('/clients/', data),
  delete: (id) => api.delete(`/clients/${id}/`),
}

export const membershipsApi = {
  getAll: () => api.get('/memberships/'),
  create: (data) => api.post('/memberships/', data),
  delete: (id) => api.delete(`/memberships/${id}/`),
}

export const workoutsApi = {
  getAll: () => api.get('/workouts/'),
  create: (data) => api.post('/workouts/', data),
  delete: (id) => api.delete(`/workouts/${id}/`),
}

export const trainersApi = {
  getAll: () => api.get('/trainers/'),
}

export default api