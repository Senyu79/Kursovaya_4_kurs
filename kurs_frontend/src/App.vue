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

    <footer class="footer">
      <div class="footer-inner">
        <p class="copyright">© 2026 VERITY. Все права защищены.</p>
      </div>
    </footer>
  </div>
</template>

<style>
@import url('https://fonts.googleapis.com/css2?family=Instrument+Sans:wght@400;600;700&display=swap');

* { box-sizing: border-box; margin: 0; padding: 0; }
body { 
  font-family: "Instrument Sans", sans-serif; 
  background-color: #FFFFFF; 
  color: #000; 
}
ul { padding: 0; list-style: none; }
a { text-decoration: none; }

.container { margin: 0 auto; padding: 0 20px; max-width: 1400px; }
.app-wrapper { display: flex; flex-direction: column; min-height: 100vh; }

/* Шапка */
.header { background-color: #B7C0F9; padding: 20px 0; }
.header-inner { display: flex; justify-content: space-between; align-items: center; }
.title { font-size: 35px; font-weight: 700; letter-spacing: 2px; }
.nav-list { display: flex; gap: 45px; font-size: 20px; }
.nav-item { transition: transform 0.3s ease; }
.nav-item:hover { transform: translateY(-2px); }
.nav-link { color: #000; font-weight: 600; }

/* Контент */
.main-content { flex: 1; padding-bottom: 70px; }

/* Подвал */
.footer { background-color: #B7C0F9; height: 150px; margin-top: 70px; }
.footer-inner { display: flex; justify-content: center; align-items: center; height: 100%; }
.copyright { color: #000; font-size: 16px; }

/* Анимация */
.fade-enter-active, .fade-leave-active { transition: opacity 0.3s ease; }
.fade-enter-from, .fade-leave-to { opacity: 0; }
</style>