<template>
  <div>
    <!-- Hero-секция -->
    <div class="hero">
      <h1>ТВОЙ ТЕЛО — <br><span>ТВОЙ ПРОЕКТ</span></h1>
      <p>Присоединяйся к лучшему фитнес-клубу. Первая тренировка — бесплатно.</p>
      <button class="btn hero-btn" @click="scrollToForm">Выбрать абонемент</button>
    </div>

    <!-- Карточки абонементов -->
    <div class="section-title">
      <h2>Наши абонементы</h2>
      <div class="line"></div>
    </div>

    <div class="cards-container">
      <!-- Скелетоны (пока грузится) -->
      <div v-if="loading" class="card skeleton" v-for="i in 3" :key="i">
        <div class="sk-title"></div>
        <div class="sk-price"></div>
        <div class="sk-text"></div>
      </div>

      <!-- Реальные карточки -->
      <div v-else v-for="t in types" :key="t.id" class="card" :class="{ 'popular': t.type.toLowerCase().includes('год') }">
        <div class="card-icon">💪</div>
        <h3>{{ t.type }}</h3>
        <div class="price">{{ t.price }} <span>₽</span></div>
        <ul class="features">
          <li>✓ Доступ в зал 24/7</li>
          <li>✓ Раздевалка и душ</li>
          <li v-if="t.type.toLowerCase().includes('год')">✓ 3 персональные тренировки</li>
        </ul>
        <button class="btn card-btn" @click="selectType(t.id)">Выбрать</button>
        <div v-if="t.type.toLowerCase().includes('год')" class="badge">Хит продаж</div>
      </div>
    </div>

    <!-- Форма -->
    <div class="form-wrapper" id="form-anchor">
      <div class="form-info">
        <h2>Готов начать?</h2>
        <p>Оставь заявку, и наш менеджер свяжется с тобой в течение 15 минут для подтверждения.</p>
        <ul>
          <li>📍 г. Москва, ул. Спортивная, 1</li>
          <li>📞 +7 (999) 123-45-67</li>
          <li>🕒 Круглосуточно</li>
        </ul>
      </div>
      
      <form @submit.prevent="submitForm" class="signup-form">
        <h3>Оставить заявку</h3>
        
        <div class="input-group">
          <input v-model="form.first_name" placeholder="Имя" required />
          <input v-model="form.last_name" placeholder="Фамилия" required />
        </div>
        
        <input v-model="form.phone" placeholder="Телефон (89991234567)" maxlength="12" required />
        <input v-model="form.email" type="email" placeholder="Email (необязательно)" />
        
        <select v-model="form.membership_id" required>
          <option disabled value="">Выберите абонемент</option>
          <option v-for="t in types" :key="t.id" :value="t.id">
            {{ t.type }} — {{ t.price }} ₽
          </option>
        </select>
        
        <button type="submit" class="btn" :disabled="isSubmitting">
          {{ isSubmitting ? 'Отправка...' : 'Отправить заявку' }}
        </button>
        
        <p v-if="message" :class="['message', messageType]">{{ message }}</p>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { clientsApi, membershipsApi, membershipTypesApi } from '../api/index.js'

const types = ref([])
const loading = ref(true)
const isSubmitting = ref(false)
const form = ref({ first_name: '', last_name: '', phone: '', email: '', membership_id: '' })
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

function scrollToForm() {
  document.getElementById('form-anchor').scrollIntoView({ behavior: 'smooth' })
}

function selectType(id) {
  form.value.membership_id = id
  scrollToForm()
}

async function submitForm() {
  message.value = ''
  isSubmitting.value = true
  try {
    const clientRes = await clientsApi.create({
      first_name: form.value.first_name,
      last_name: form.value.last_name,
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
    message.value = 'Заявка отправлена! Ждем вас в зале.'
    form.value = { first_name: '', last_name: '', phone: '', email: '', membership_id: '' }
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
/* Hero */
.hero { text-align: center; padding: 40px 0 80px; }
.hero h1 { font-size: 56px; font-weight: 800; color: #0f172a; line-height: 1.1; margin-bottom: 20px; letter-spacing: -1px; }
.hero h1 span { color: #ef4444; }
.hero p { font-size: 18px; color: #64748b; max-width: 500px; margin: 0 auto 30px; }

/* Заголовки секций */
.section-title { text-align: center; margin-bottom: 50px; }
.section-title h2 { font-size: 32px; color: #0f172a; font-weight: 700; margin-bottom: 15px; }
.line { width: 60px; height: 4px; background: #ef4444; margin: 0 auto; border-radius: 2px; }

/* Карточки */
.cards-container { display: flex; gap: 30px; justify-content: center; margin-bottom: 80px; flex-wrap: wrap; }
.card { 
  background: white; border-radius: 16px; padding: 40px 30px; text-align: center; width: 320px; 
  box-shadow: 0 10px 30px rgba(0,0,0,0.05); transition: all 0.3s ease; position: relative;
  border: 1px solid #e2e8f0; display: flex; flex-direction: column;
}
.card:hover { transform: translateY(-10px); box-shadow: 0 20px 40px rgba(0,0,0,0.1); border-color: #ef4444; }
.card-icon { font-size: 40px; margin-bottom: 15px; }
.card h3 { font-size: 22px; color: #0f172a; margin-bottom: 15px; text-transform: capitalize; }
.price { font-size: 42px; font-weight: 800; color: #0f172a; margin-bottom: 25px; }
.price span { font-size: 24px; color: #64748b; font-weight: 500; }
.features { list-style: none; text-align: left; margin-bottom: 30px; flex: 1; }
.features li { padding: 8px 0; color: #475569; font-size: 14px; border-bottom: 1px dashed #e2e8f0; }
.card-btn { width: 100%; margin-top: auto; }

/* Популярный тариф */
.popular { border: 2px solid #ef4444; transform: scale(1.05); }
.popular:hover { transform: scale(1.05) translateY(-10px); }
.badge { 
  position: absolute; top: -15px; left: 50%; transform: translateX(-50%); 
  background: #ef4444; color: white; padding: 6px 16px; border-radius: 20px; 
  font-size: 12px; font-weight: 700; text-transform: uppercase; letter-spacing: 1px;
}

/* Скелетоны */
.skeleton { animation: pulse 1.5s infinite; }
.sk-title, .sk-price, .sk-text { background: #e2e8f0; border-radius: 4px; margin: 0 auto 20px; }
.sk-title { width: 60%; height: 24px; }
.sk-price { width: 40%; height: 40px; }
.sk-text { width: 80%; height: 16px; }
@keyframes pulse { 0% { opacity: 1; } 50% { opacity: 0.5; } 100% { opacity: 1; } }

/* Форма */
.form-wrapper { 
  display: flex; background: #0f172a; border-radius: 20px; overflow: hidden; 
  box-shadow: 0 20px 50px rgba(0,0,0,0.2); max-width: 1000px; margin: 0 auto;
}
.form-info { flex: 1; padding: 60px; background: url('https://images.unsplash.com/photo-1534438327276-14e5300c3a48?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&q=80') center/cover; position: relative; }
.form-info::before { content: ''; position: absolute; inset: 0; background: linear-gradient(to right, rgba(15,23,42,0.9), rgba(15,23,42,0.7)); }
.form-info h2, .form-info p, .form-info ul { position: relative; z-index: 1; color: white; }
.form-info h2 { font-size: 32px; margin-bottom: 20px; }
.form-info p { color: #cbd5e1; margin-bottom: 30px; line-height: 1.6; }
.form-info ul { list-style: none; }
.form-info li { margin-bottom: 15px; color: #e2e8f0; font-size: 15px; }

.signup-form { flex: 1; padding: 60px; background: white; display: flex; flex-direction: column; gap: 20px; }
.signup-form h3 { font-size: 24px; color: #0f172a; margin-bottom: 10px; }
.input-group { display: flex; gap: 15px; }
.signup-form input, .signup-form select { 
  width: 100%; padding: 16px; border: 1px solid #cbd5e1; border-radius: 8px; 
  font-size: 15px; font-family: inherit; transition: all 0.3s; background: #f8fafc;
}
.signup-form input:focus, .signup-form select:focus { 
  outline: none; border-color: #ef4444; box-shadow: 0 0 0 3px rgba(239, 68, 68, 0.1); background: white;
}
.signup-form button { margin-top: 10px; }
.signup-form button:disabled { opacity: 0.7; cursor: not-allowed; }

/* Сообщения */
.message { padding: 12px; border-radius: 8px; text-align: center; font-size: 14px; font-weight: 500; }
.message.success { background: #dcfce7; color: #166534; }
.message.error { background: #fee2e2; color: #991b1b; }
</style>