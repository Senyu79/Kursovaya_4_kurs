import axios from 'axios'

const api = axios.create({
  baseURL: 'http://127.0.0.1:8000/api',
  headers: {
    'Content-Type': 'application/json',
  },
})

export const clientsApi = {
  create: (data) => api.post('/clients/', data),
}

export const membershipsApi = {
  create: (data) => api.post('/memberships/', data),
}

export const membershipTypesApi = {
  getAll: () => api.get('/membership-types/'),
}

export const workoutsApi = {
  getAll: () => api.get('/workouts/'),
}

export const trainersApi = {
  getAll: () => api.get('/trainers/'),
}

export default api