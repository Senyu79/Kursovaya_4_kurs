<template>
  <div>
    <h1 style="text-align: center; margin-bottom: 30px;">Расписание тренировок</h1>
    <div v-if="workouts.length === 0" style="text-align: center; color: #666;">
      Пока нет запланированных тренировок.
    </div>
    
    <div class="schedule-list">
      <div v-for="w in workouts" :key="w.id" class="schedule-item">
        <div class="date-box">
          <div class="day">{{ new Date(w.workout_date).getDate() }}</div>
          <div class="month">{{ getMonth(new Date(w.workout_date)) }}</div>
        </div>
        <div class="info">
          <h3>{{ w.trainer_name }}</h3>
          <p>Клиент: {{ w.client_name }}</p>
          <p class="time">Время: {{ new Date(w.workout_date).toLocaleTimeString().slice(0,5) }}</p>
        </div>
        <div class="status" :class="w.status">
          {{ translateStatus(w.status) }}
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { workoutsApi } from '../api/index.js'

const workouts = ref([])

async function load() {
  const { data } = await workoutsApi.getAll()
  workouts.value = data.results ?? data
}

function getMonth(date) {
  const months = ['Янв', 'Фев', 'Мар', 'Апр', 'Май', 'Июн', 'Июл', 'Авг', 'Сен', 'Окт', 'Ноя', 'Дек']
  return months[date.getMonth()]
}

function translateStatus(status) {
  const map = { 'scheduled': 'Запланирована', 'completed': 'Проведена', 'cancelled': 'Отменена' }
  return map[status] || status
}

onMounted(load)
</script>

<style scoped>
.schedule-list { display: flex; flex-direction: column; gap: 15px; max-width: 800px; margin: 0 auto; }
.schedule-item { background: white; padding: 20px; border-radius: 10px; display: flex; align-items: center; box-shadow: 0 2px 10px rgba(0,0,0,0.05); }
.date-box { background: #1a1a2e; color: white; padding: 10px 15px; border-radius: 8px; text-align: center; margin-right: 20px; min-width: 70px; }
.day { font-size: 24px; font-weight: bold; }
.month { font-size: 14px; text-transform: uppercase; }
.info { flex: 1; }
.info h3 { margin: 0 0 5px 0; color: #1a1a2e; }
.info p { margin: 0; color: #666; font-size: 14px; }
.time { color: #e94560; font-weight: bold; margin-top: 5px !important; }
.status { padding: 5px 10px; border-radius: 20px; font-size: 12px; font-weight: bold; }
.scheduled { background: #e3f2fd; color: #1976d2; }
.completed { background: #e8f5e9; color: #2e7d32; }
.cancelled { background: #ffebee; color: #c62828; }
</style>