<template>
  <div class="container">
    <h2 class="title-trainers">НАШИ ТРЕНЕРЫ</h2>
    
    <div v-if="loading" class="loading">Загрузка тренеров...</div>
    
    <div v-else-if="trainers.length === 0" class="no-results">
      <h3>Пока нет добавленных тренеров</h3>
    </div>

    <div v-else class="trainers-grid">
      <div v-for="t in trainers" :key="t.id" class="trainer-card">
        
        <div class="trainer-photo">
          <img 
            v-if="t.photo" 
            :src="t.photo" 
            :alt="t.last_name" 
            class="trainer-img"
          />
          <div v-else class="trainer-photo-placeholder">
            {{ t.first_name[0] }}{{ t.last_name[0] }}
          </div>
        </div>

        <div class="trainer-info">
          <h3 class="trainer-name">{{ t.last_name }} {{ t.first_name }}</h3>
          <p class="trainer-fathername">{{ t.middle_name }}</p>
          <p class="trainer-position">{{ t.position_name }}</p>
          <p class="trainer-phone">{{ t.phone || 'Телефон не указан' }}</p>
          <p class="trainer-email">{{ t.email || '' }}</p>
        </div>
        
        <button class="trainer-button" @click="selectTrainer(t)">Записаться</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { trainersApi } from '../api/index.js'

const trainers = ref([])
const loading = ref(true)

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

function selectTrainer(t) {
  alert(`Вы записываетесь к тренеру: ${t.last_name} ${t.first_name}`)
}

onMounted(loadTrainers)
</script>

<style scoped>
.title-trainers { font-size: 45px; text-align: center; margin: 50px 0; font-weight: 700; }
.loading { text-align: center; font-size: 20px; margin: 50px 0; color: #666; }
.no-results { text-align: center; padding: 60px 20px; }

.trainers-grid {
  display: grid;
  gap: 30px;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  max-width: 1200px;
  margin: 0 auto 70px;
  justify-items: center;
}

.trainer-card {
  background: #F3F4F7;
  border-radius: 20px;
  padding: 25px;
  text-align: center;
  transition: all 0.3s ease;
  box-shadow: 0 4px 15px rgba(0,0,0,0.05);
  width: 100%;
  max-width: 350px;
  display: flex;
  flex-direction: column;
}

.trainer-card:hover {
  transform: translateY(-10px);
  box-shadow: 0 8px 25px rgba(0,0,0,0.1);
}

.trainer-photo {
  margin-bottom: 20px;
}

.trainer-img {
  width: 150px;
  height: 150px;
  border-radius: 50%;
  object-fit: cover;
  margin: 0 auto;
  border: 4px solid #fff;
  box-shadow: 0 4px 10px rgba(0,0,0,0.1);
  display: block;
}

.trainer-photo-placeholder {
  width: 150px;
  height: 150px;
  border-radius: 50%;
  background: #B7C0F9;
  color: #202439;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 40px;
  font-weight: 700;
  margin: 0 auto;
  border: 4px solid #fff;
}

.trainer-info { margin-bottom: 20px; flex-grow: 1; }
.trainer-name {
  font-size: 22px;
  font-weight: 700;
  margin-bottom: 5px;
  color: #202439;
}
.trainer-fathername {
  color: #666;
  font-size: 16px;
  margin-bottom: 15px;
}
.trainer-position {
  font-size: 16px;
  color: #0CA1B1;
  font-weight: 700;
  margin-bottom: 15px;
  background: #D6F1F0;
  display: inline-block;
  padding: 5px 15px;
  border-radius: 20px;
}
.trainer-phone {
  font-size: 15px;
  color: #444;
  margin-bottom: 5px;
}
.trainer-email {
  font-size: 14px;
  color: #888;
}

.trainer-button {
  display: inline-block;
  padding: 12px 25px;
  background: #0CA1B1;
  color: white;
  text-decoration: none;
  border-radius: 25px;
  font-weight: 600;
  transition: all 0.3s ease;
  border: none;
  cursor: pointer;
  font-size: 16px;
  font-family: inherit;
  width: 100%;
}

.trainer-button:hover {
  transform: scale(1.02);
  background: #098593;
}
</style>