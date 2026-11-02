<template>
  <div>
    <div class="hero">
      <h1>Начни свой путь к идеальному телу</h1>
      <p>Выбери подходящий абонемент и запишись на первую тренировку!</p>
    </div>

    <!-- Карточки абонементов -->
    <div class="cards-container">
      <div class="card">
        <h2>Месяц</h2>
        <div class="price">2 500 ₽</div>
        <ul>
          <li>Доступ в тренажерный зал</li>
          <li>Безлимитные посещения</li>
        </ul>
        <button class="btn" @click="selectType('Месяц')">Выбрать</button>
      </div>

      <div class="card popular">
        <div class="badge">Хит продаж</div>
        <h2>Полгода</h2>
        <div class="price">12 000 ₽</div>
        <ul>
          <li>Доступ в тренажерный зал</li>
          <li>1 персональная тренировка в подарок</li>
        </ul>
        <button class="btn" @click="selectType('Полгода')">Выбрать</button>
      </div>

      <div class="card">
        <h2>Год</h2>
        <div class="price">20 000 ₽</div>
        <ul>
          <li>Доступ в тренажерный зал</li>
          <li>3 персональные тренировки</li>
          <li>Заморозка на 1 месяц</li>
        </ul>
        <button class="btn" @click="selectType('Год')">Выбрать</button>
      </div>
    </div>

    <!-- Форма записи -->
    <div class="form-section" id="form-anchor">
      <h2>Записаться на абонемент</h2>
      <form @submit.prevent="submitForm" class="signup-form">
        <input v-model="form.first_name" placeholder="Ваше имя" required />
        <input v-model="form.last_name" placeholder="Ваша фамилия" required />
        <input v-model="form.phone" placeholder="Телефон (+7...)" maxlength="12" required />
        <input v-model="form.email" type="email" placeholder="Email" />
        <select v-model="form.type" required>
          <option disabled value="">Выберите абонемент</option>
          <option value="Месяц">Месяц</option>
          <option value="Полгода">Полгода</option>
          <option value="Год">Год</option>
        </select>
        <button type="submit" class="btn">Отправить заявку</button>
      </form>
      <p v-if="message" :style="{ color: messageType === 'error' ? 'red' : 'green' }">{{ message }}</p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { clientsApi, membershipsApi } from '../api/index.js'

const form = ref({ first_name: '', last_name: '', phone: '', email: '', type: '' })
const message = ref('')
const messageType = ref('success')

function selectType(type) {
  form.value.type = type
  document.getElementById('form-anchor').scrollIntoView({ behavior: 'smooth' })
}

async function submitForm() {
  message.value = ''
  try {
    // 1. Создаем клиента
    const clientRes = await clientsApi.create({
      first_name: form.value.first_name,
      last_name: form.value.last_name,
      phone: form.value.phone,
      email: form.value.email
    })
    const clientId = clientRes.data.id

    // 2. Создаем абонемент для клиента (даты рассчитываем на лету)
    const startDate = new Date()
    const endDate = new Date()
    if (form.value.type === 'Месяц') endDate.setMonth(endDate.getMonth() + 1)
    if (form.value.type === 'Полгода') endDate.setMonth(endDate.getMonth() + 6)
    if (form.value.type === 'Год') endDate.setFullYear(endDate.getFullYear() + 1)

    const prices = { 'Месяц': 2500, 'Полгода': 12000, 'Год': 20000 }

    await membershipsApi.create({
      client: clientId,
      type: form.value.type,
      start_date: startDate.toISOString().split('T')[0],
      end_date: endDate.toISOString().split('T')[0],
      price: prices[form.value.type]
    })

    messageType.value = 'success'
    message.value = 'Вы успешно записаны! Наш администратор свяжется с вами.'
    form.value = { first_name: '', last_name: '', phone: '', email: '', type: '' }
  } catch (e) {
    messageType.value = 'error'
    message.value = 'Ошибка при записи. Проверьте введенные данные (возможно, такой телефон уже есть).'
    console.error(e)
  }
}
</script>

<style scoped>
.hero { text-align: center; margin-bottom: 50px; }
.hero h1 { font-size: 36px; margin-bottom: 10px; color: #1a1a2e; }
.hero p { color: #666; font-size: 18px; }

.cards-container { display: flex; gap: 20px; justify-content: center; margin-bottom: 60px; }
.card { background: white; border-radius: 10px; padding: 30px; text-align: center; width: 300px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); transition: transform 0.3s; position: relative; }
.card:hover { transform: translateY(-10px); }
.card h2 { color: #1a1a2e; font-size: 24px; }
.card .price { font-size: 36px; font-weight: bold; color: #e94560; margin: 20px 0; }
.card ul { list-style: none; padding: 0; margin-bottom: 30px; color: #666; }
.card ul li { padding: 10px 0; border-bottom: 1px solid #eee; }
.popular { border: 2px solid #e94560; }
.badge { position: absolute; top: -15px; left: 50%; transform: translateX(-50%); background: #e94560; color: white; padding: 5px 15px; border-radius: 20px; font-size: 12px; font-weight: bold; }

.form-section { max-width: 500px; margin: 0 auto; background: white; padding: 40px; border-radius: 10px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); }
.form-section h2 { text-align: center; margin-bottom: 20px; }
.signup-form { display: flex; flex-direction: column; gap: 15px; }
.signup-form input, .signup-form select { padding: 12px; border: 1px solid #ccc; border-radius: 5px; font-size: 16px; }
</style>