<template>
  <div class="app-wrapper">
    <header class="header">
      <div class="logo"><span>VERITY</span></div>
      <nav class="nav">
        <router-link to="/">Абонементы</router-link>
        <router-link to="/schedule">Расписание</router-link>
      </nav>
    </header>

    <main class="main-content">
      <router-view v-slot="{ Component }">
        <transition name="fade" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </main>

    <footer class="footer">
      <div class="footer-content">
        <div class="footer-logo">VERITY</div>
        <p>Даже демоны занимаются у нас.</p>
        <p class="copyright">© 2026 VERITY. Все права защищены.</p>
      </div>
    </footer>
  </div>
</template>

<style>
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;700;800&display=swap');

* { box-sizing: border-box; margin: 0; padding: 0; }

body { 
  font-family: 'Montserrat', sans-serif; 
  background-color: #0f172a; 
  color: #334155; 
}

.app-wrapper { 
  display: flex; 
  flex-direction: column; 
  min-height: 100vh; 
  background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
}

.header { 
  background: rgba(15, 23, 42, 0.95); 
  backdrop-filter: blur(10px);
  color: white; 
  padding: 20px 50px; 
  display: flex; 
  justify-content: space-between; 
  align-items: center; 
  position: sticky; 
  top: 0; 
  z-index: 100; 
  box-shadow: 0 4px 20px rgba(0,0,0,0.1);
}

.logo { 
  font-size: 26px; 
  font-weight: 800; 
  color: white; 
  letter-spacing: 1px; 
}
.logo span { color: #ef4444; /* Красный акцент */ }

.nav a { 
  color: #cbd5e1; 
  text-decoration: none; 
  margin-left: 30px; 
  font-size: 15px; 
  font-weight: 500;
  transition: color 0.3s; 
  position: relative;
}
.nav a:hover, .nav a.router-link-active { color: white; }
.nav a::after {
  content: ''; position: absolute; bottom: -5px; left: 0; width: 0; height: 2px;
  background: #ef4444; transition: width 0.3s;
}
.nav a:hover::after, .nav a.router-link-active::after { width: 100%; }

.main-content { 
  flex: 1; 
  max-width: 1200px; 
  margin: 0 auto; 
  width: 100%; 
  padding: 60px 20px; 
}

.footer { 
  background: #0f172a; 
  color: #94a3b8; 
  padding: 50px 20px 30px; 
  text-align: center; 
}
.footer-logo { font-size: 24px; font-weight: 800; color: white; margin-bottom: 10px; }
.footer p { margin-bottom: 10px; font-size: 14px; }
.copyright { margin-top: 30px; font-size: 12px; color: #64748b; }

.fade-enter-active, .fade-leave-active { transition: opacity 0.3s ease, transform 0.3s ease; }
.fade-enter-from, .fade-leave-to { opacity: 0; transform: translateY(10px); }

.btn { 
  background-color: #ef4444; 
  color: white; 
  border: none; 
  padding: 14px 28px; 
  border-radius: 8px; 
  font-size: 16px; 
  cursor: pointer; 
  transition: all 0.3s ease; 
  font-weight: 700; 
  font-family: inherit;
  box-shadow: 0 4px 12px rgba(239, 68, 68, 0.3);
}
.btn:hover { 
  background-color: #dc2626; 
  transform: translateY(-2px);
  box-shadow: 0 6px 15px rgba(239, 68, 68, 0.4);
}
</style>