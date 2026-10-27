import { createRouter, createWebHistory } from 'vue-router'
import HomeView from './views/HomeView.vue'
import ScheduleView from './views/ScheduleView.vue'

const routes = [
  { path: '/', component: HomeView },
  { path: '/schedule', component: ScheduleView },
]

export default createRouter({
  history: createWebHistory(),
  routes,
})