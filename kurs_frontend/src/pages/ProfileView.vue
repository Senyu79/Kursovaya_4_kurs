<template>
  <div class="container profile-page">
    <div class="page-header">
      <div>
        <h1 class="main-title">ЛИЧНЫЙ КАБИНЕТ</h1>
        <p class="subtitle">Управляйте абонементом и записывайтесь на тренировки</p>
      </div>
      <!-- Кнопка выхода -->
      <button v-if="client" @click="logout" class="logout-btn">Выйти</button>
    </div>

    <!-- Экран входа -->
    <div v-if="!client" class="login-box">
      <h2>Вход по номеру телефона</h2>
      <p>Введите номер, который указывали при покупке абонемента</p>
      <form @submit.prevent="login" class="login-form">
        <input v-model="searchPhone" placeholder="Телефон (89991234567)" maxlength="12" required />
        <button type="submit" class="btn">Войти</button>
      </form>
      <p v-if="error" class="error-msg">{{ error }}</p>
    </div>

    <!-- Экран кабинета -->
    <div v-else class="dashboard">
      
      <!-- Левая колонка: Информация об абонементе -->
      <div class="sidebar">
        <div class="user-card">
          <div class="avatar">{{ client.first_name[0] }}{{ client.last_name[0] }}</div>
          <h2>{{ client.last_name }} {{ client.first_name }}</h2>
          <p class="phone">{{ client.phone }}</p>
        </div>

        <div class="membership-card">
          <h3>Ваш абонемент</h3>
          
          <div v-if="activeMembership" class="active-membership">
            <div class="tariff-name">{{ activeMembership.membership_type }}</div>
            <div class="tariff-dates">
              <p>Начало: <b>{{ activeMembership.start_date }}</b></p>
              <p>Конец: <b>{{ activeMembership.end_date }}</b></p>
            </div>
            <div class="status-badge">Активен</div>
          </div>
          
          <div v-else class="no-membership">
            <p>У вас нет активного абонемента.</p>
            <router-link to="/" class="btn-small">Купить абонемент</router-link>
          </div>
        </div>
      </div>

      <!-- Правая колонка: Запись на тренировку -->
      <div class="main-area">
        <h2 class="section-title">Записаться на тренировку</h2>
        
        <!-- Если нет активного абонемента — блокируем форму -->
        <div v-if="!activeMembership" class="warning-box">
          <p>Вы не можете записаться на тренировку, так как у вас нет активного абонемента.</p>
          <router-link to="/" class="btn-small">Перейти к тарифам</router-link>
        </div>

        <form v-else @submit.prevent="bookWorkout" class="booking-form">
          <div class="input-group">
            <label>Выберите тренера</label>
            <select v-model="booking.trainer" required>
              <option disabled value="">-- Выберите тренера --</option>
              <option v-for="t in trainers" :key="t.id" :value="t.id">
                {{ t.last_name }} {{ t.first_name }} ({{ t.position_name }})
              </option>
            </select>
          </div>

          <div class="input-group">
            <label>Дата и время начала</label>
            <input v-model="booking.workout_start" type="datetime-local" required />
          </div>

          <div class="input-group">
            <label>Дата и время окончания</label>
            <input v-model="booking.workout_end" type="datetime-local" required />
          </div>

          <button type="submit" class="btn submit-btn" :disabled="isBooking">
            {{ isBooking ? 'Запись...' : 'Записаться' }}
          </button>
        </form>

        <p v-if="bookMessage" class="book-message">{{ bookMessage }}</p>

        <h2 class="section-title" style="margin-top: 50px;">Мои тренировки</h2>
        <div class="my-workouts">
          <div v-for="w in myWorkouts" :key="w.id" class="workout-item">
            <div class="w-date">{{ formatDate(w.workout_start) }}</div>
            <div class="w-trainer">Тренер: {{ w.trainer_name }}</div>
            <div class="w-time">{{ formatTime(w.workout_start) }} — {{ formatTime(w.workout_end) }}</div>
          </div>
          <p v-if="myWorkouts.length === 0" class="empty-text">У вас пока нет запланированных тренировок.</p>
        </div>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import api, { trainersApi, workoutsApi } from '../api/index.js'

const searchPhone = ref('')
const client = ref(null)
const memberships = ref([])
const trainers = ref([])
const myWorkouts = ref([])
const error = ref('')
const isBooking = ref(false)
const bookMessage = ref('')

const booking = ref({ trainer: '', workout_start: '', workout_end: '' })

// Вычисляем активный абонемент на текущую дату
const activeMembership = computed(() => {
  const today = new Date().toISOString().split('T')[0]
  return memberships.value.find(m => m.start_date <= today && m.end_date >= today)
})

async function login() {
  error.value = ''
  try {
    const res = await api.get(`/clients/?search=${searchPhone.value}`)
    const clients = res.data.results ?? res.data
    
    if (clients.length === 0) {
      error.value = 'Клиент с таким номером не найден.'
      return
    }
    
    client.value = clients[0]
    
    const [mRes, tRes, wRes] = await Promise.all([
      api.get(`/memberships/?client=${client.value.id}`),
      trainersApi.getAll(),
      workoutsApi.getAll()
    ])
    
    memberships.value = mRes.data.results ?? mRes.data
    trainers.value = tRes.data.results ?? tRes.data
    
    const allWorkouts = wRes.data.results ?? wRes.data
    myWorkouts.value = allWorkouts.filter(w => w.client === client.value.id)
    
  } catch (e) {
    error.value = 'Ошибка сервера. Попробуйте позже.'
  }
}

// Функция выхода из кабинета
function logout() {
  client.value = null
  memberships.value = []
  myWorkouts.value = []
  searchPhone.value = ''
  booking.value = { trainer: '', workout_start: '', workout_end: '' }
  bookMessage.value = ''
}

async function bookWorkout() {
  isBooking.value = true
  bookMessage.value = ''
  try {
    await api.post('/workouts/', {
      client: client.value.id,
      trainer: booking.value.trainer,
      workout_start: booking.value.workout_start + ':00Z',
      workout_end: booking.value.workout_end + ':00Z'
    })
    
    bookMessage.value = 'Вы успешно записаны на тренировку!'
    booking.value = { trainer: '', workout_start: '', workout_end: '' }
    
    const wRes = await workoutsApi.getAll()
    const allWorkouts = wRes.data.results ?? wRes.data
    myWorkouts.value = allWorkouts.filter(w => w.client === client.value.id)
    
  } catch (e) {
    bookMessage.value = 'Ошибка записи. Возможно, время занято.'
    console.error(e)
  } finally {
    isBooking.value = false
  }
}

function formatDate(dateStr) {
  return new Date(dateStr).toLocaleDateString('ru-RU')
}
function formatTime(dateStr) {
  return new Date(dateStr).toLocaleTimeString('ru-RU', { hour: '2-digit', minute: '2-digit' })
}
</script>

<style scoped>
.profile-page { padding-top: 40px; padding-bottom: 100px; }
.page-header { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 40px; }
.main-title { font-size: 44px; font-weight: 800; letter-spacing: -1px; color: #202439; margin-bottom: 8px; }
.subtitle { font-size: 16px; color: #666; }

/* Кнопка выхода */
.logout-btn { 
  background: #fff; color: #ef4444; border: 2px solid #ef4444; 
  padding: 10px 20px; border-radius: 50px; font-weight: 700; 
  cursor: pointer; transition: 0.3s; font-family: inherit; font-size: 14px;
}
.logout-btn:hover { background: #ef4444; color: #fff; }

/* Форма входа */
.login-box { max-width: 400px; margin: 80px auto; background: #F3F4F7; padding: 40px; border-radius: 20px; text-align: center; }
.login-box h2 { font-size: 22px; margin-bottom: 10px; color: #202439; }
.login-box p { font-size: 14px; color: #666; margin-bottom: 20px; }
.login-form { display: flex; flex-direction: column; gap: 12px; }
.login-form input { padding: 14px; border: 1px solid #ccc; border-radius: 8px; font-size: 15px; font-family: inherit; }
.btn { background: #0CA1B1; color: white; border: none; padding: 14px; border-radius: 50px; font-size: 16px; font-weight: 700; cursor: pointer; transition: 0.3s; }
.btn:hover { background: #098593; }
.error-msg { color: #ef4444; font-weight: 600; margin-top: 15px; }

/* Дашборд */
.dashboard { display: flex; gap: 40px; align-items: flex-start; }

/* Левая колонка */
.sidebar { width: 320px; flex-shrink: 0; }
.user-card { background: #fff; border: 1px solid #E8EAED; padding: 30px; border-radius: 20px; text-align: center; margin-bottom: 20px; }
.avatar { width: 80px; height: 80px; border-radius: 50%; background: #B7C0F9; color: #202439; display: flex; align-items: center; justify-content: center; font-size: 28px; font-weight: 800; margin: 0 auto 15px; }
.user-card h2 { font-size: 20px; color: #202439; margin-bottom: 5px; }
.phone { color: #666; font-size: 14px; }

.membership-card { background: #202439; color: #fff; padding: 30px; border-radius: 20px; }
.membership-card h3 { font-size: 14px; text-transform: uppercase; letter-spacing: 1px; color: #8E9AF4; margin-bottom: 20px; }
.tariff-name { font-size: 24px; font-weight: 800; margin-bottom: 15px; text-transform: capitalize; }
.tariff-dates p { font-size: 14px; color: #cbd5e1; margin-bottom: 8px; }
.tariff-dates b { color: #fff; }
.status-badge { display: inline-block; background: #10b981; color: white; padding: 6px 14px; border-radius: 20px; font-size: 12px; font-weight: 700; margin-top: 15px; }
.no-membership { text-align: center; }
.no-membership p { color: #cbd5e1; margin-bottom: 15px; }
.btn-small { display: inline-block; background: #B7C0F9; color: #202439; padding: 10px 20px; border-radius: 30px; font-weight: 700; font-size: 14px; transition: 0.3s; }
.btn-small:hover { background: #a5b0f5; }

/* Правая колонка */
.main-area { flex-grow: 1; background: #F3F4F7; padding: 40px; border-radius: 20px; }
.section-title { font-size: 24px; font-weight: 800; color: #202439; margin-bottom: 25px; }

/* Блокировка формы */
.warning-box { background: #fee2e2; border: 2px dashed #ef4444; padding: 30px; border-radius: 16px; text-align: center; }
.warning-box p { color: #b91c1c; font-weight: 600; margin-bottom: 20px; font-size: 16px; }

.booking-form { display: flex; flex-direction: column; gap: 20px; max-width: 500px; }
.input-group { display: flex; flex-direction: column; gap: 8px; }
.input-group label { font-size: 13px; font-weight: 700; color: #666; text-transform: uppercase; letter-spacing: 0.5px; }
.input-group select, .input-group input { padding: 14px; border: 1px solid #ccc; border-radius: 8px; font-size: 15px; font-family: inherit; background: #fff; }
.submit-btn { margin-top: 10px; }
.book-message { margin-top: 20px; font-weight: 700; color: #10b981; }

/* Мои тренировки */
.my-workouts { display: flex; flex-direction: column; gap: 15px; }
.workout-item { background: #fff; padding: 20px; border-radius: 12px; border-left: 4px solid #0CA1B1; display: flex; justify-content: space-between; align-items: center; }
.w-date { font-weight: 800; color: #202439; }
.w-trainer { font-size: 14px; color: #666; }
.w-time { font-weight: 700; color: #0CA1B1; }
.empty-text { color: #666; font-size: 15px; }

@media (max-width: 900px) {
  .dashboard { flex-direction: column; }
  .sidebar { width: 100%; }
  .page-header { flex-direction: column; gap: 20px; }
}
</style>