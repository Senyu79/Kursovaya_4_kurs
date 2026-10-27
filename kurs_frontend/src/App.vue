<template>
  <div class="app-wrapper">
    <header class="header">
      <div class="logo">🏋️ GYM PRO</div>
      <nav class="nav">
        <router-link to="/">Абонементы</router-link>
        <router-link to="/schedule">Расписание</router-link>
      </nav>
    </header>

    <main class="main-content">
      <router-view />
    </main>

    <footer class="footer">
      <p>© 2026 GYM PRO. Все права защищены.</p>
    </footer>
  </div>
</template>

<style>
/* Базовые стили */
* { box-sizing: border-box; }
body { margin: 0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f5f7fa; color: #333; }
.app-wrapper { display: flex; flex-direction: column; min-height: 100vh; }

/* Шапка */
.header { background-color: #1a1a2e; color: white; padding: 15px 50px; display: flex; justify-content: space-between; align-items: center; }
.logo { font-size: 24px; font-weight: bold; color: #e94560; letter-spacing: 1px; }
.nav a { color: white; text-decoration: none; margin-left: 20px; font-size: 16px; transition: 0.3s; }
.nav a:hover, .nav a.router-link-active { color: #e94560; }

/* Контент */
.main-content { flex: 1; max-width: 1200px; margin: 0 auto; width: 100%; padding: 40px 20px; }

/* Подвал */
.footer { background-color: #1a1a2e; color: #888; text-align: center; padding: 20px; font-size: 14px; }

/* Общие стили для форм и кнопок */
.btn { background-color: #e94560; color: white; border: none; padding: 12px 24px; border-radius: 5px; font-size: 16px; cursor: pointer; transition: 0.3s; font-weight: bold; }
.btn:hover { background-color: #d13d56; }
</style>