<script>
import { get_users } from "@/API";
import CatCard from "../components/CatCard.vue";

export default {
  data() {
    return {
      token: "",
      name: "",
      last_name: "",
      users: [],
      query: "",
      load: false,
      activeTab: 'all',
      menuVisible: false,
      currentUserId: null,
      tabs: [
        { id: 'all', label: 'Все пользователи' },
        { id: 'banned', label: 'Заблокированные' },
        { id: 'shelters', label: 'Приюты' },
        { id: 'admins', label: 'Администраторы' }
      ]
    };
  },
  components: {
    CatCard,
  },
  computed: {
    filteredUsers() {
      let filtered = this.users;
      
      if (this.activeTab === 'banned') {
        filtered = filtered.filter(u => u.is_banned || u.is_blocked);
      } else if (this.activeTab === 'shelters') {
        filtered = filtered.filter(u => u.is_shelter);
      } else if (this.activeTab === 'admins') {
        filtered = filtered.filter(u => u.is_admin);
      }
      
      if (this.query) {
        const q = this.query.toLowerCase();
        filtered = filtered.filter(u => 
          u.first_name.toLowerCase().includes(q) ||
          u.last_name.toLowerCase().includes(q) ||
          u.phone_number.includes(q) ||
          (u.shelter_name && u.shelter_name.toLowerCase().includes(q))
        );
      }
      
      return filtered;
    }
  },
  methods: {
    async loadUsers() {
      this.load = true;
      try {
        const response = await get_users(this.token);
        if (response && Array.isArray(response)) {
          this.users = response;
        }
      } catch (error) {
        console.error('Ошибка загрузки пользователей:', error);
      } finally {
        this.load = false;
      }
    },
    changeTab(tab) {
      this.activeTab = tab;
    },
    toggleMenu(userId, event) {
      event.stopPropagation();
      this.currentUserId = userId;
      this.menuVisible = !this.menuVisible;
    },
    handleOption(option) {
      console.log(`Выбрано: ${option} для пользователя ID: ${this.currentUserId}`);
      this.menuVisible = false;
      // Здесь можно добавить логику для каждого действия
    },
    handleClickOutside() {
      this.menuVisible = false;
    },
    getUserStatus(user) {
      if (user.is_banned) return 'Забанен';
      if (user.is_blocked) return 'Заблокирован';
      if (user.is_admin) return 'Администратор';
      if (user.is_shelter) return 'Приют';
      return 'Активен';
    },
    getStatusClass(user) {
      if (user.is_banned) return 'status-banned';
      if (user.is_blocked) return 'status-blocked';
      if (user.is_admin) return 'status-admin';
      if (user.is_shelter) return 'status-shelter';
      return 'status-active';
    },
    formatDate(dateString) {
      if (!dateString) return '';
      const date = new Date(dateString);
      return date.toLocaleDateString('ru-RU');
    },
    formatPhone(phone) {
      if (!phone) return '';
      return phone.replace(/(\d{1})(\d{3})(\d{3})(\d{2})(\d{2})/, '+$1 ($2) $3-$4-$5');
    }
  },
  async mounted() {
    this.token = localStorage.getItem("token");
    if (this.token && this.token != "") {
      this.name = localStorage.getItem("name");
      this.last_name = localStorage.getItem("last_name");
      await this.loadUsers();
    }
    document.addEventListener("click", this.handleClickOutside);
  },
  unmounted() {
    document.removeEventListener("click", this.handleClickOutside);
  }
};
</script>

<template>
  <div class="admin-priyuts-container">
    <div class="admin-header">
      <h1>Управление пользователями</h1>
      <div class="admin-tabs">
        <button 
          v-for="tab in tabs" 
          :key="tab.id"
          :class="{ 'active-tab': activeTab === tab.id }"
          @click="changeTab(tab.id)"
        >
          {{ tab.label }}
        </button>
      </div>
    </div>

    <div class="search-container">
      <input 
        type="text" 
        v-model="query" 
        placeholder="Поиск по имени, телефону или названию приюта..."
        class="search-input"
      />
    </div>

    <div class="priyuts-list" v-if="!load && filteredUsers.length > 0">
      <div class="priyut-card" v-for="user in filteredUsers" :key="user.id">
        <div class="user-photo">
          <div class="avatar-placeholder">
            {{ user.first_name?.charAt(0) || '' }}{{ user.last_name?.charAt(0) || '' }}
          </div>
        </div>
        <div class="priyut-info">
          <h3>
            {{ user.first_name }} {{ user.last_name }}
            <span v-if="user.shelter_name">({{ user.shelter_name }})</span>
          </h3>
          <div class="priyut-meta">
            <span class="priyut-phone">
              {{ formatPhone(user.phone_number) }}
            </span>
            <span :class="['priyut-status', getStatusClass(user)]">
              {{ getUserStatus(user) }}
            </span>
            <span v-if="user.is_banned" class="ban-date">
              До: {{ formatDate(user.ban_until) || 'навсегда' }}
            </span>
          </div>
          <div class="priyut-footer">
            <span class="priyut-date">
              Зарегистрирован: {{ formatDate(user.created_at) }}
            </span>
          </div>
        </div>
        <div class="priyut-actions">
          <div class="lp_wrapper">
            <div class="lp_menu" @click="toggleMenu(user.id, $event)">
              <p>...</p>
            </div>
            <div
              class="lp_dropdown"
              v-show="menuVisible && currentUserId === user.id"
              @click.stop
            >
              <div class="lp_option" @click="handleOption('Разрешить попытку')">Разрешить попытку</div>
              <div class="lp_option" @click="handleOption('Зачесть попытку')">Зачесть попытку</div>
              <div class="lp_option" @click="handleOption('Бан навсегда')">Бан навсегда</div>
              <div class="lp_option" @click="handleOption('Разблокировать')">Разблокировать</div>
              <div class="lp_option" @click="handleOption('Сбросить тест')">Сбросить тест</div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div v-else-if="!load && filteredUsers.length === 0" class="no-results">
      <p>Нет пользователей для отображения</p>
    </div>

    <div v-if="load" class="loader-container">
      <img src="../assets/imgs/Loader.svg" alt="Загрузка..." />
    </div>
  </div>
</template>

<style scoped>
.admin-priyuts-container {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
}

.admin-header {
  margin-bottom: 20px;
  display: flex;
  flex-direction: column;
  gap: 15px;
  color: #5A2F10;
}

.admin-tabs {
  display: flex;
  gap: 10px;
  border-bottom: 1px solid #DFBB9E;
  padding-bottom: 10px;
}

.admin-tabs button {
  padding: 8px 16px;
  background: #FFEEE0;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s;
}

.admin-tabs button.active-tab {
  background: #DFBB9E;
  color: white;
}

.search-container {
  margin-bottom: 20px;
}

.search-input {
  width: 850px;
  padding: 10px 15px;
  border: 1px solid #DFBB9E;
  border-radius: 8px;
  font-size: 16px;
}

.search-input:focus {
  border: 1px solid #DFBB9E;
  outline: none;
}

.priyuts-list {
  display: grid;
  grid-template-columns: 1fr;
  gap: 20px;
}

.priyut-card {
  width: 850px;
  height: 240px;
  display: flex;
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  overflow: hidden;
  position: relative;
}

.user-photo {
  width: 100px;
  height: 100px;
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #FFEEE0;
  margin: 20px;
  border-radius: 50%;
}

.avatar-placeholder {
  font-size: 24px;
  font-weight: bold;
  color: #5A2F10;
}

.priyut-info {
  flex: 1;
  padding: 15px;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.priyut-info h3 {
  margin: 0;
  color: #333;
}

.priyut-meta {
  display: flex;
  gap: 15px;
  font-size: 14px;
  color: #666;
  align-items: center;
}

.priyut-status {
  padding: 2px 8px;
  border-radius: 4px;
  font-size: 12px;
  font-weight: bold;
}

.status-active {
  background-color: #E6F7E6;
  color: #2E7D32;
}

.status-banned {
  background-color: #FFEBEE;
  color: #C62828;
}

.status-blocked {
  background-color: #FFF8E1;
  color: #F57F17;
}

.status-admin {
  background-color: #E3F2FD;
  color: #1565C0;
}

.status-shelter {
  background-color: #E8F5E9;
  color: #2E7D32;
}

.ban-date {
  color: #C62828;
  font-size: 12px;
}

.priyut-footer {
  display: flex;
  justify-content: space-between;
  margin-top: auto;
  font-size: 13px;
}

.priyut-date {
  color: #888;
}

.priyut-actions {
  padding: 15px;
  border-left: 1px solid #eee;
}

.lp_wrapper {
  position: relative;
}

.lp_menu {
  background-color: #FFEAD4;
  border-radius: 11px;
  height: 44px;
  width: 57px;
  font-size: 22px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  user-select: none;
}

.lp_dropdown {
  position: absolute;
  top: 5px;
  right: 70px;
  background-color: #FFEAD4;
  border-radius: 11px;
  width: 261px;
  height: 190px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  z-index: 10;
  padding: 0;
  display: flex;
  flex-direction: column;
}
.lp_option:first-child {
  border-radius: 11px 11px 0 0;
}
.lp_option:last-child {
 border-radius:  0 0 11px 11px;
}
.lp_option {
  padding: 8px 20px;
  cursor: pointer;
  transition: background-color 0.2s;
  font-size: 16px;
}

.lp_option:hover {
  background-color: #DCC5AC;
}

.no-results {
  text-align: center;
  padding: 40px;
  color: #666;
}

.loader-container {
  display: flex;
  justify-content: center;
  padding: 40px;
}
</style>