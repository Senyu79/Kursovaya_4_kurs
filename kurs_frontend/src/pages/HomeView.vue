<template>
  <div>
    <div class="hero">
      <h1>Начни свой путь к идеальному телу</h1>
      <p>Выбери подходящий абонемент и запишись на первую тренировку!</p>
    </div>

    <!-- Карточки абонементов (загружаются из БД) -->
    <div class="cards-container" v-if="types.length > 0">
      <div v-for="t in types" :key="t.id" class="card">
        <h2>{{ t.type }}</h2>
        <div class="price">{{ t.price }} ₽</div>
        <ul>
          <li>Доступ в тренажерный зал</li>
          <li>Безлимитные посещения</li>
        </ul>
        <button class="btn" @click="selectType(t.id)">Выбрать</button>
      </div>
    </div>
    <div v-else style="text-align: center; color: #666;">
      Загрузка абонементов...
    </div>

    <!-- Форма записи -->
    <div class="form-section" id="form-anchor">
      <h2>Оставить заявку</h2>
      <form @submit.prevent="submitForm" class="signup-form">
        <input v-model="form.first_name" placeholder="Ваше имя" required />
        <input v-model="form.last_name" placeholder="Ваша фамилия" required />
        <input v-model="form.phone" placeholder="Телефон (89991234567)" maxlength="12" required />
        <input v-model="form.email" type="email" placeholder="Email (необязательно)" />
        
        <select v-model="form.membership_id" required>
          <option disabled value="">Выберите абонемент</option>
          <option v-for="t in types" :key="t.id" :value="t.id">
            {{ t.type }} ({{ t.price }} ₽)
          </option>
        </select>
        
        <button type="submit" class="btn">Отправить заявку</button>
      </form>
      <p v-if="message" :style="{ color: messageType === 'error' ? 'red' : 'green', textAlign: 'center', marginTop: '15px' }">
        {{ message }}
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { clientsApi, membershipsApi, membershipTypesApi } from '../api/index.js'

const types = ref([])
const form = ref({ first_name: '', last_name: '', phone: '', email: '', membership_id: '' })
const message = ref('')
const messageType = ref('success')

// Загружаем типы абонементов при старте
async function loadTypes() {
  try {
    const { data } = await membershipTypesApi.getAll()
    types.value = data.results ?? data
  } catch (e) {
    console.error("Ошибка загрузки абонементов", e)
  }
}

// Клик по кнопке "Выбрать" на карточке
function selectType(id) {
  form.value.membership_id = id
  document.getElementById('form-anchor').scrollIntoView({ behavior: 'smooth' })
}

// Отправка формы
async function submitForm() {
  message.value = ''
  try {
    // 1. Создаем клиента
    const clientRes = await clientsApi.create({
      first_name: form.value.first_name,
      last_name: form.value.last_name,
      phone: form.value.phone,
      email: form.value.email || null
    })
    const clientId = clientRes.data.id

    // 2. Создаем абонемент (на 1 месяц от сегодняшнего дня)
    const startDate = new Date()
    const endDate = new Date()
    endDate.setMonth(endDate.getMonth() + 1)

    await membershipsApi.create({
      client: clientId,
      membership: form.value.membership_id,
      start_date: startDate.toISOString().split('T')[0],
      end_date: endDate.toISOString().split('T')[0]
    })

    messageType.value = 'success'
    message.value = 'Заявка успешно отправлена! Ждем вас в зале.'
    form.value = { first_name: '', last_name: '', phone: '', email: '', membership_id: '' }
  } catch (e) {
    messageType.value = 'error'
    message.value = 'Ошибка при отправке. Проверьте телефон (возможно, он уже зарегистрирован).'
    console.error(e.response?.data)
  }
}

onMounted(loadTypes)
</script>

<style scoped>
.hero { text-align: center; margin-bottom: 50px; }
.hero h1 { font-size: 36px; margin-bottom: 10px; color: #1a1a2e; }
.hero p { color: #666; font-size: 18px; }

.cards-container { display: flex; gap: 20px; justify-content: center; margin-bottom: 60px; flex-wrap: wrap; }
.card { background: white; border-radius: 10px; padding: 30px; text-align: center; width: 300px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); transition: transform 0.3s; }
.card:hover { transform: translateY(-10px); }
.card h2 { color: #1a1a2e; font-size: 24px; text-transform: capitalize; }
.card .price { font-size: 36px; font-weight: bold; color: #e94560; margin: 20px 0; }
.card ul { list-style: none; padding: 0; margin-bottom: 30px; color: #666; }
.card ul li { padding: 10px 0; border-bottom: 1px solid #eee; }

.form-section { max-width: 500px; margin: 0 auto; background: white; padding: 40px; border-radius: 10px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); }
.form-section h2 { text-align: center; margin-bottom: 20px; }
.signup-form { display: flex; flex-direction: column; gap: 15px; }
.signup-form input, .signup-form select { padding: 12px; border: 1px solid #ccc; border-radius: 5px; font-size: 16px; }
</style>