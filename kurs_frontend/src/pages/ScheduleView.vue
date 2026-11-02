<template>
  <div>
    <h1 style="text-align: center; margin-bottom: 30px;">Расписание тренировок</h1>
    
    <div v-if="workouts.length === 0" style="text-align: center; color: #666;">
      Пока нет запланированных тренировок.
    </div>
    
    <div class="schedule-list" v-else>
      <div v-for="w in workouts" :key="w.id" class="schedule-item">
        <div class="date-box">
          <div class="day">{{ new Date(w.workout_start).getDate() }}</div>
          <div class="month">{{ getMonth(new Date(w.workout_start)) }}</div>
        </div>
        <div class="info">
          <h3>Тренер: {{ w.trainer_name }}</h3>
          <p>Клиент: {{ w.client_name }}</p>
          <p class="time">
            С {{ formatTime(w.workout_start) }} до {{ formatTime(w.workout_end) }}
          </p>
        </div>
        <div class="status">Запланирована</div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { workoutsApi } from '../api/index.js'

const workouts = ref([])

async function load() {
  try {
    const { data } = await workoutsApi.getAll()
    // Сортируем по дате начала
    const list = data.results ?? data
    workouts.value = list.sort((a, b) => new Date(a.workout_start) - new Date(b.workout_start))
  } catch (e) {
    console.error("Ошибка загрузки расписания", e)
  }
}

// Получаем месяц (Янв, Фев...)
function getMonth(date) {
  const months = ['Янв', 'Фев', 'Мар', 'Апр', 'Май', 'Июн', 'Июл', 'Авг', 'Сен', 'Окт', 'Ноя', 'Дек']
  return months[date.getMonth()]
}

// Форматируем время (например, 10:30)
function formatTime(dateString) {
  const date = new Date(dateString)
  return date.toLocaleTimeString('ru-RU', { hour: '2-digit', minute: '2-digit' })
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
.info h3 { margin: 0 0 5px 0; color: #1a1a2e; font-size: 18px;}
.info p { margin: 0; color: #666; font-size: 14px; }
.time { color: #e94560; font-weight: bold; margin-top: 5px !important; }
.status { padding: 5px 10px; border-radius: 20px; font-size: 12px; font-weight: bold; background: #e3f2fd; color: #1976d2; }
</style>