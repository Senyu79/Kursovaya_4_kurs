<template>
  <div class="container trainers-page">
    
    <div class="page-header">
      <div class="header-left">
        <h1 class="main-title">КОМАНДА</h1>
        <p class="subtitle">Профессионалы, которые приведут вас к результату</p>
      </div>
      
      <div class="header-right">
        <div class="filter-group">
          <label>Специализация:</label>
          <select v-model="selectedPosition" class="custom-select">
            <option value="">Все тренеры</option>
            <option v-for="pos in positions" :key="pos" :value="pos">
              {{ pos }}
            </option>
          </select>
        </div>
      </div>
    </div>

    <div v-if="loading" class="loading">Загрузка...</div>
    <div v-else-if="filteredTrainers.length === 0" class="empty-state">
      <p>По вашему запросу тренеров не найдено</p>
    </div>

    <div v-else class="trainers-grid">
      <div v-for="t in filteredTrainers" :key="t.id" class="trainer-card">
        
        <div class="card-image-wrapper">
          <img 
            v-if="t.photo" 
            :src="t.photo" 
            :alt="t.last_name" 
            class="card-image"
          />
          <div v-else class="card-image-placeholder">
            {{ t.first_name[0] }}{{ t.last_name[0] }}
          </div>
          
          <div class="position-badge">
            {{ t.position_name }}
          </div>
        </div>

        <div class="card-content">
          <h2 class="trainer-name">{{ t.first_name }} {{ t.last_name }}</h2>
          <p class="trainer-fathername">{{ t.middle_name || ' ' }}</p>
          
          <div class="contact-info">
            <div class="contact-row">
              <span class="contact-label">Тел:</span>
              <span>{{ t.phone || 'Скрыт' }}</span>
            </div>
            <div class="contact-row" v-if="t.email">
              <span class="contact-label">Email:</span>
              <span>{{ t.email }}</span>
            </div>
          </div>
        </div>

      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { trainersApi } from '../api/index.js'

const trainers = ref([])
const loading = ref(true)
const selectedPosition = ref('')

const positions = computed(() => {
  const allPositions = trainers.value.map(t => t.position_name)
  return [...new Set(allPositions)]
})

const filteredTrainers = computed(() => {
  if (!selectedPosition.value) return trainers.value
  return trainers.value.filter(t => t.position_name === selectedPosition.value)
})

async function loadTrainers() {
  try {
    const { data } = await trainersApi.getAll()
    trainers.value = data.results ?? data
  } catch (e) {
    console.error("Ошибка загрузки тренеров", e)
  } finally {
    loading.value = false
  }
}

onMounted(loadTrainers)
</script>

<style scoped>
/* ДОБАВИЛИ ОТСТУП ВНИЗУ, ТАК КАК ПОДВАЛА БОЛЬШЕ НЕТ */
.trainers-page {
  padding-top: 40px;
  padding-bottom: 100px; 
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  margin-bottom: 50px;
  padding-bottom: 20px;
  border-bottom: 2px solid #E8EAED;
}

.main-title {
  font-size: 44px;
  font-weight: 800;
  letter-spacing: -1px;
  color: #202439;
  margin-bottom: 8px;
  line-height: 1;
}

.subtitle {
  font-size: 16px;
  color: #666;
  font-weight: 400;
}

.filter-group {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 8px;
}

.filter-group label {
  font-size: 13px;
  text-transform: uppercase;
  letter-spacing: 1px;
  color: #888;
  font-weight: 600;
}

.custom-select {
  padding: 10px 16px;
  font-size: 15px;
  font-family: inherit;
  font-weight: 500;
  color: #202439;
  background-color: #F3F4F7;
  border: 2px solid transparent;
  border-radius: 8px;
  cursor: pointer;
  outline: none;
  transition: all 0.3s;
  min-width: 200px;
  appearance: none;
  background-image: url("data:image/svg+xml;charset=US-ASCII,%3Csvg%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%20width%3D%22292.4%22%20height%3D%22292.4%22%3E%3Cpath%20fill%3D%22%23202439%22%20d%3D%22M287%2069.4a17.6%2017.6%200%200%200-13-5.4H18.4c-5%200-9.3%201.8-12.9%205.4A17.6%2017.6%200%200%200%200%2082.2c0%205%201.8%209.3%205.4%2012.9l128%20127.9c3.6%203.6%207.8%205.4%2012.8%205.4s9.2-1.8%2012.8-5.4L287%2095c3.5-3.5%205.4-7.8%205.4-12.8%200-5-1.9-9.2-5.5-12.8z%22%2F%3E%3C%2Fsvg%3E");
  background-repeat: no-repeat;
  background-position: right 15px top 50%;
  background-size: 10px auto;
}

.custom-select:focus, .custom-select:hover {
  border-color: #B7C0F9;
  background-color: #fff;
  box-shadow: 0 4px 15px rgba(183, 192, 249, 0.2);
}

.trainers-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 30px;
}

.trainer-card {
  background: #fff;
  border-radius: 20px;
  overflow: hidden;
  transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  border: 1px solid #E8EAED;
  display: flex;
  flex-direction: column;
}

.trainer-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.08);
  border-color: #B7C0F9;
}

.card-image-wrapper {
  position: relative;
  height: 320px;
  background-color: #E8EAED;
  overflow: hidden;
}

.card-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.5s ease;
}

.trainer-card:hover .card-image {
  transform: scale(1.05);
}

.card-image-placeholder {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 56px;
  font-weight: 800;
  color: #fff;
  background: linear-gradient(135deg, #B7C0F9 0%, #8E9AF4 100%);
}

.position-badge {
  position: absolute;
  bottom: 15px;
  left: 15px;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(5px);
  color: #202439;
  font-size: 12px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  padding: 6px 14px;
  border-radius: 30px;
  box-shadow: 0 4px 10px rgba(0,0,0,0.1);
}

.card-content {
  padding: 25px;
  display: flex;
  flex-direction: column;
  flex-grow: 1;
}

.trainer-name {
  font-size: 22px;
  font-weight: 800;
  color: #202439;
  margin-bottom: 5px;
  line-height: 1.2;
}

.trainer-fathername {
  font-size: 15px;
  color: #888;
  margin-bottom: 20px;
  font-weight: 500;
  min-height: 22px;
}

.contact-info {
  margin-top: auto;
  display: flex;
  flex-direction: column;
  gap: 10px;
  padding-top: 15px;
  border-top: 1px solid #E8EAED;
}

.contact-row {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
  color: #444;
  font-weight: 500;
}

.contact-label {
  color: #999;
  font-weight: 600;
  font-size: 13px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  min-width: 45px;
}

.loading, .empty-state {
  text-align: center;
  padding: 80px 0;
  font-size: 18px;
  color: #666;
}

@media (max-width: 900px) {
  .page-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 20px;
  }
  .main-title { font-size: 36px; }
  .custom-select { width: 100%; }
}
</style>