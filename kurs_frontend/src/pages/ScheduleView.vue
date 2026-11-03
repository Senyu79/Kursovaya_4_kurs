<template>
  <div>
    <div class="schedule-header">
      <h1>Расписание тренировок</h1>
      <p>Будь в форме — следи за своим графиком</p>
    </div>
    
    <!-- Скелетоны -->
    <div v-if="loading" class="schedule-list">
      <div v-for="i in 3" :key="i" class="schedule-item skeleton-item"></div>
    </div>

    <!-- Пусто -->
    <div v-else-if="workouts.length === 0" class="empty-state">
      <div class="empty-icon">📅</div>
      <h3>Пока нет запланированных тренировок</h3>
      <p>Запишитесь на абонемент, и мы составим для вас график.</p>
    </div>

    <!-- Список -->
    <div v-else class="schedule-list">
      <div v-for="w in workouts" :key="w.id" class="schedule-item">
        
        <div class="date-box">
          <div class="day">{{ new Date(w.workout_start).getDate() }}</div>
          <div class="month">{{ getMonth(new Date(w.workout_start)) }}</div>
        </div>
        
        <div class="info">
          <div class="trainer">
            <span class="label">Тренер</span>
            <h3>{{ w.trainer_name }}</h3>
          </div>
          <div class="client">
            <span class="label">Клиент</span>
            <p>{{ w.client_name }}</p>
          </div>
        </div>
        
        <div class="time-box">
          <div class="time">
            {{ formatTime(w.workout_start) }} <span>—</span> {{ formatTime(w.workout_end) }}
          </div>
          <div class="status">Запланирована</div>
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
  const months = ['Янв', 'Фев', 'Мар', 'Апр', 'Май', 'Июн', 'Июл', 'Авг', 'Сен', 'Окт', 'Ноя', 'Дек']
  return months[date.getMonth()]
}

function formatTime(dateString) {
  const date = new Date(dateString)
  return date.toLocaleTimeString('ru-RU', { hour: '2-digit', minute: '2-digit' })
}

onMounted(load)
</script>

<style scoped>
.schedule-header { text-align: center; margin-bottom: 50px; }
.schedule-header h1 { font-size: 42px; color: #0f172a; font-weight: 800; margin-bottom: 10px; }
.schedule-header p { color: #64748b; font-size: 18px; }

.schedule-list { display: flex; flex-direction: column; gap: 20px; max-width: 900px; margin: 0 auto; }

.schedule-item { 
  background: white; padding: 25px 30px; border-radius: 16px; display: flex; align-items: center; 
  box-shadow: 0 4px 15px rgba(0,0,0,0.03); border-left: 6px solid #ef4444; transition: transform 0.3s;
}
.schedule-item:hover { transform: translateX(10px); box-shadow: 0 8px 25px rgba(0,0,0,0.08); }

.date-box { 
  background: #0f172a; color: white; padding: 15px; border-radius: 12px; 
  text-align: center; margin-right: 30px; min-width: 80px; 
  box-shadow: 0 4px 10px rgba(15,23,42,0.2);
}
.day { font-size: 28px; font-weight: 800; line-height: 1; }
.month { font-size: 12px; text-transform: uppercase; color: #cbd5e1; margin-top: 5px; letter-spacing: 1px; }

.info { flex: 1; display: flex; gap: 40px; align-items: center; }
.label { font-size: 11px; text-transform: uppercase; color: #94a3b8; font-weight: 700; letter-spacing: 1px; margin-bottom: 4px; display: block; }
.info h3 { margin: 0; color: #0f172a; font-size: 18px; font-weight: 700; }
.info p { margin: 0; color: #475569; font-size: 16px; }

.time-box { text-align: right; display: flex; flex-direction: column; align-items: flex-end; gap: 8px; }
.time { font-size: 20px; font-weight: 800; color: #0f172a; }
.time span { color: #cbd5e1; font-weight: 400; margin: 0 5px; }
.status { 
  padding: 6px 14px; border-radius: 20px; font-size: 12px; font-weight: 700; 
  background: #dcfce7; color: #166534; letter-spacing: 0.5px;
}

/* Пустое состояние */
.empty-state { text-align: center; padding: 80px 20px; background: white; border-radius: 20px; border: 2px dashed #cbd5e1; }
.empty-icon { font-size: 60px; margin-bottom: 20px; }
.empty-state h3 { font-size: 24px; color: #0f172a; margin-bottom: 10px; }
.empty-state p { color: #64748b; }

/* Скелетон */
.skeleton-item { height: 100px; background: #e2e8f0; animation: pulse 1.5s infinite; border-left-color: #cbd5e1; }
@keyframes pulse { 0% { opacity: 1; } 50% { opacity: 0.5; } 100% { opacity: 1; } }
</style>