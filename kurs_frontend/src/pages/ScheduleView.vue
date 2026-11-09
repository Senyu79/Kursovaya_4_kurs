<template>
  <div class="container schedule-page">
    <h1 class="title-schedule">РАСПИСАНИЕ ТРЕНИРОВОК</h1>
    
    <div v-if="loading" class="loading">Загрузка...</div>
    
    <div v-else-if="workouts.length === 0" class="no-results">
      <h2>Пока нет запланированных тренировок</h2>
      <p>Запишитесь на тариф, чтобы составить расписание.</p>
    </div>

    <div v-else class="schedule-list">
      <div v-for="w in workouts" :key="w.id" class="schedule-card">
        <div class="date-block">
          <span class="day">{{ new Date(w.workout_start).getDate() }}</span>
          <span class="month">{{ getMonth(new Date(w.workout_start)) }}</span>
        </div>
        
        <div class="info-block">
          <h3>Тренировка с {{ w.trainer_name }}</h3>
          <p>Клиент: <b>{{ w.client_name }}</b></p>
        </div>
        
        <div class="time-block-schedule">
          <span class="time-text">{{ formatTime(w.workout_start) }} — {{ formatTime(w.workout_end) }}</span>
          <span class="status-badge">Запланирована</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { workoutsApi } from '../api/index.js'

const workouts = ref([])
const loading = ref(true)

async function load() {
  try {
    const { data } = await workoutsApi.getAll()
    const list = data.results ?? data
    workouts.value = list.sort((a, b) => new Date(a.workout_start) - new Date(b.workout_start))
  } catch (e) {
    console.error(e)
  } finally {
    loading.value = false
  }
}

function getMonth(date) {
  const months = ['ЯНВ', 'ФЕВ', 'МАР', 'АПР', 'МАЙ', 'ИЮН', 'ИЮЛ', 'АВГ', 'СЕН', 'ОКТ', 'НОЯ', 'ДЕК']
  return months[date.getMonth()]
}

function formatTime(dateString) {
  return new Date(dateString).toLocaleTimeString('ru-RU', { hour: '2-digit', minute: '2-digit' })
}

onMounted(load)
</script>

<style scoped>
.schedule-page { margin-top: 50px; }
.title-schedule { text-align: center; font-size: 45px; margin-bottom: 50px; font-weight: 700; }
.loading { text-align: center; font-size: 20px; margin: 50px 0; }

.schedule-list { display: flex; flex-direction: column; gap: 20px; max-width: 900px; margin: 0 auto; }
.schedule-card { 
  display: flex; align-items: center; background: #F3F4F7; 
  border-radius: 20px; padding: 20px 30px; gap: 30px; transition: transform 0.3s;
}
.schedule-card:hover { transform: translateX(10px); background: #EBECF0; }

.date-block { 
  background: #B7C0F9; color: #000; padding: 15px 20px; border-radius: 15px; 
  text-align: center; min-width: 90px; display: flex; flex-direction: column;
}
.day { font-size: 32px; font-weight: 700; line-height: 1; }
.month { font-size: 14px; font-weight: 600; text-transform: uppercase; letter-spacing: 1px; margin-top: 5px; }

.info-block { flex: 1; }
.info-block h3 { font-size: 22px; margin-bottom: 5px; color: #202439; }
.info-block p { color: #666; font-size: 16px; margin: 0; }

.time-block-schedule { text-align: right; display: flex; flex-direction: column; align-items: flex-end; gap: 10px; }
.time-text { font-size: 20px; font-weight: 700; color: #0CA1B1; }
.status-badge { background: #202439; color: white; padding: 5px 15px; border-radius: 20px; font-size: 12px; font-weight: 600; }

.no-results { text-align: center; padding: 60px 20px; }
.no-results h2 { color: #666; margin-bottom: 15px; }
</style>