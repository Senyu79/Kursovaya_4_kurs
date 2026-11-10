<template>
  <div class="app-wrapper">
    <header class="header">
      <div class="container header-inner">
        <div class="title">VERITY</div>
        <nav>
          <ul class="nav-list">
            <li class="nav-item"><router-link to="/" class="nav-link">Тарифы</router-link></li>
            <li class="nav-item"><router-link to="/trainers" class="nav-link">Тренеры</router-link></li>
            <li class="nav-item"><router-link to="/schedule" class="nav-link">Расписание</router-link></li>
            <li class="nav-item"><router-link to="/profile" class="nav-link">Кабинет</router-link></li>
          </ul>
        </nav>
      </div>
    </header>

    <main class="main-content">
      <router-view v-slot="{ Component }">
        <transition name="fade" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </main>
  </div>
</template>

<style>
@import url('https://fonts.googleapis.com/css2?family=Instrument+Sans:wght@400;600;700;800&display=swap');

* { box-sizing: border-box; margin: 0; padding: 0; }
body { 
  font-family: "Instrument Sans", sans-serif; 
  background-color: #FFFFFF; 
  color: #000; 
}
ul { padding: 0; list-style: none; }
a { text-decoration: none; }

.container { margin: 0 auto; padding: 0 20px; max-width: 1100px; }
.app-wrapper { display: flex; flex-direction: column; min-height: 100vh; }

/* УВЕЛИЧИЛИ ШАПКУ */
.header { 
  background-color: #B7C0F9; 
  padding: 25px 0; /* Было 15px */
  box-shadow: 0 4px 20px rgba(183, 192, 249, 0.3); /* Легкая тень для объема */
}
.header-inner { display: flex; justify-content: space-between; align-items: center; }
.title { 
  font-size: 36px; /* Было 28px */
  font-weight: 800; 
  letter-spacing: 2px; 
  color: #202439; /* Сделали чуть темнее для контраста */
}
.nav-list { display: flex; gap: 45px; font-size: 18px; }
.nav-item { transition: transform 0.3s ease; }
.nav-item:hover { transform: translateY(-2px); }
.nav-link { color: #202439; font-weight: 700; opacity: 0.8; transition: opacity 0.3s; }
.nav-link:hover, .nav-link.router-link-active { opacity: 1; }

/* УБРАЛИ ПОДВАЛ, ОСТАВИЛИ ТОЛЬКО КОНТЕНТ */
.main-content { 
  flex: 1; 
  padding-top: 20px;
  padding-bottom: 80px; 
}

.fade-enter-active, .fade-leave-active { transition: opacity 0.3s ease; }
.fade-enter-from, .fade-leave-to { opacity: 0; }
</style>