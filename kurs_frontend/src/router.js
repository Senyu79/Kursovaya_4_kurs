import { createRouter, createWebHistory } from 'vue-router'
import HomeView from './pages/HomeView.vue'
import ScheduleView from './pages/ScheduleView.vue'

const routes = [
  { path: '/', component: HomeView },
  { path: '/schedule', component: ScheduleView },
]

export default createRouter({
  history: createWebHistory(),
  routes,
})