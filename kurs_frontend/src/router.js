import { createRouter, createWebHistory } from 'vue-router'
import HomeView from './pages/HomeView.vue'
import ScheduleView from './pages/ScheduleView.vue'
import TrainersView from './pages/TrainersView.vue'

const routes = [
  { path: '/', component: HomeView },
  { path: '/schedule', component: ScheduleView },
  { path: '/trainers', component: TrainersView },
]

export default createRouter({
  history: createWebHistory(),
  routes,
})