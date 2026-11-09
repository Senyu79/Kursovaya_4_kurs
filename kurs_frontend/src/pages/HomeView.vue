<template>
  <div class="container">
    <section class="trafic-main">
      <h2 class="title-trafic">НАШИ ТАРИФЫ</h2>
      
      <div v-if="loading" class="loading">Загрузка тарифов...</div>

      <div v-else class="trafic-list">
        <div 
          v-for="(t, index) in types" 
          :key="t.id" 
          :class="['trafic-card', getCardClass(index)]"
        >
          <div class="trafic-head">
            <h2 class="title-item">{{ t.type.toUpperCase() }}</h2>
            <div :class="['kvadrat', getSquareClass(index)]">
               <span class="atom">⚡</span>
            </div>
          </div>
          
          <div class="information">
            <ul class="information-list">
              <li class="information-item" v-for="feature in getFeatures(index)" :key="feature.text">
                <span :class="['check-icon', feature.included ? 'check' : 'cross']">
                  {{ feature.included ? '✓' : '✕' }}
                </span>
                <p :class="['information-text', { 'text-muted': !feature.included }]">
                  {{ feature.text }}
                </p>
              </li>
            </ul>
          </div>
          
          <div class="card-bottom">
            <h3 class="price-info">{{ t.price }}₽ <span>В месяц</span></h3>
          </div>
        </div>
      </div>

      <div class="form-wrapper" id="form-anchor">
        <h2>Вступить в клуб</h2>
        <form @submit.prevent="submitForm" class="signup-form">
          <div class="input-row">
            <input v-model="form.first_name" placeholder="Имя" required />
            <input v-model="form.last_name" placeholder="Фамилия" required />
          </div>
          
          <input v-model="form.middle_name" placeholder="Отчество (необязательно)" />
          
          <input v-model="form.phone" placeholder="Телефон (89991234567)" maxlength="12" required />
          <input v-model="form.email" type="email" placeholder="Email (необязательно)" />
          
          <select v-model="form.membership_id" required>
            <option disabled value="">Выберите абонемент</option>
            <option v-for="t in types" :key="t.id" :value="t.id">
              {{ t.type }} ({{ t.price }} ₽)
            </option>
          </select>
          
          <button type="submit" class="submit-btn" :disabled="isSubmitting">
            {{ isSubmitting ? 'Отправка...' : 'Вступить в клуб' }}
          </button>
        </form>
        <p v-if="message" :class="['message', messageType]">{{ message }}</p>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { clientsApi, membershipsApi, membershipTypesApi } from '../api/index.js'

const types = ref([])
const loading = ref(true)
const isSubmitting = ref(false)
const form = ref({ 
  first_name: '', 
  last_name: '', 
  middle_name: '', 
  phone: '', 
  email: '', 
  membership_id: '' 
})
const message = ref('')
const messageType = ref('success')

async function loadTypes() {
  try {
    const { data } = await membershipTypesApi.getAll()
    types.value = data.results ?? data
  } catch (e) {
    console.error(e)
  } finally {
    loading.value = false
  }
}

function getCardClass(index) {
  const classes = ['trafic-light', 'trafic-infinity', 'trafic-smart']
  return classes[index % 3]
}
function getSquareClass(index) {
  const classes = ['kvadrat-1', 'kvadrat-2', 'kvadrat-3']
  return classes[index % 3]
}

function getFeatures(index) {
  const base = [
    { text: 'безлимитный доступ в клуб', included: true },
    { text: 'тренажерный зал', included: true },
    { text: 'анализ состава тела InBody', included: true },
    { text: 'мобильное приложение', included: true },
  ]
  const extra = [
    { text: 'групповые занятия', included: index > 0 },
    { text: 'SPA-зона', included: index > 1 },
    { text: 'доступ во все клубы сети', included: index > 1 },
    { text: 'доступ для друзей', included: false },
  ]
  return [...base, ...extra]
}

async function submitForm() {
  message.value = ''
  isSubmitting.value = true
  try {
    const clientRes = await clientsApi.create({
      first_name: form.value.first_name,
      last_name: form.value.last_name,
      middle_name: form.value.middle_name,
      phone: form.value.phone,
      email: form.value.email || null
    })
    
    const startDate = new Date()
    const endDate = new Date()
    endDate.setMonth(endDate.getMonth() + 1)

    await membershipsApi.create({
      client: clientRes.data.id,
      membership: form.value.membership_id,
      start_date: startDate.toISOString().split('T')[0],
      end_date: endDate.toISOString().split('T')[0]
    })

    messageType.value = 'success'
    message.value = 'Заявка отправлена! Мы свяжемся с вами.'
    form.value = { 
      first_name: '', 
      last_name: '', 
      middle_name: '', 
      phone: '', 
      email: '', 
      membership_id: '' 
    }
  } catch (e) {
    messageType.value = 'error'
    message.value = 'Ошибка. Возможно, этот телефон уже зарегистрирован.'
  } finally {
    isSubmitting.value = false
  }
}

onMounted(loadTypes)
</script>

<style scoped>
.title-trafic { font-size: 45px; text-align: center; margin: 50px 0; font-weight: 700; }
.loading { text-align: center; font-size: 20px; margin: 50px 0; color: #666; }

.trafic-list { display: flex; justify-content: space-evenly; gap: 20px; flex-wrap: wrap; }

.trafic-card {
  background-color: #F3F4F7; width: 400px; border-radius: 30px; 
  padding-bottom: 30px; display: flex; flex-direction: column;
}
.trafic-light { min-height: 680px; color: #0CA1B1; }
.trafic-infinity { min-height: 710px; color: #202439; transform: scale(1.02); }
.trafic-smart { min-height: 680px; color: #ED692A; }

.trafic-head { display: flex; justify-content: space-between; align-items: flex-start; }
.title-item { margin: 30px; font-size: 32px; font-weight: 700; }
.kvadrat { width: 100px; height: 100px; border-radius: 20px; margin-right: 30px; position: relative; top: -20px; display: flex; align-items: center; justify-content: center; }
.kvadrat-1 { background-color: #D6F1F0; }
.kvadrat-2 { background-color: #DDE1EF; }
.kvadrat-3 { background-color: #FFEBD6; }
.atom { font-size: 40px; }

.information { margin-bottom: 20px; flex-grow: 1; }
.information-list { padding: 0 30px; }
.information-item { display: flex; font-size: 15px; align-items: flex-start; margin-bottom: 15px; }
.check-icon { font-weight: bold; margin-right: 10px; font-size: 18px; }
.check { color: #10b981; }
.cross { color: #ef4444; }
.information-text { color: #000; margin: 0; }
.text-muted { color: #999; text-decoration: line-through; }

.card-bottom { text-align: center; margin-top: auto; padding-top: 20px; }
.price-info { font-size: 32px; font-weight: 800; margin-bottom: 0; }
.price-info span { font-size: 16px; font-weight: 400; color: #666; }

.form-wrapper { max-width: 600px; margin: 80px auto 0; background: #F3F4F7; padding: 40px; border-radius: 30px; text-align: center; }
.form-wrapper h2 { font-size: 30px; margin-bottom: 30px; }
.signup-form { display: flex; flex-direction: column; gap: 15px; }
.input-row { display: flex; gap: 15px; }
.signup-form input, .signup-form select { 
  padding: 15px; border: 1px solid #ccc; border-radius: 10px; font-size: 16px; font-family: inherit; outline: none; 
}
.signup-form input:focus, .signup-form select:focus { border-color: #0CA1B1; }
.submit-btn { 
  background-color: #0CA1B1; color: white; border: none; padding: 15px; 
  border-radius: 50px; font-size: 18px; cursor: pointer; font-weight: 600; transition: 0.3s;
}
.submit-btn:hover { background-color: #098593; }
.message { margin-top: 20px; font-weight: 600; }
.message.success { color: #10b981; }
.message.error { color: #ef4444; }
</style>