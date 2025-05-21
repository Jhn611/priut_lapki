<script>
import { get_priyuts, post_priyuts_status } from "@/API";
import CatCard from "../components/CatCard.vue";

export default {
  data() {
    return {
      token: "",
      name: "",
      last_name: "",
      priyuts: [],
      query: "",
      load: false,
      activeTab: 'all',
      menuVisible: false,
      currentPriyutId: null,
      showRejectDialog: false,
      rejectionReason: "",
      tabs: [
        { id: 'all', label: 'Все приюты' },
        { id: 'moderation', label: 'На модерации' },
        { id: 'approved', label: 'Одобренные' },
        { id: 'rejected', label: 'Отклоненные' }
      ]
    };
  },
  components: {
    CatCard,
  },
  computed: {
    filteredPriyuts() {
      let filtered = this.priyuts;
      
      if (this.activeTab === 'moderation') {
        filtered = filtered.filter(p => p.status === 'pending');
      } else if (this.activeTab === 'approved') {
        filtered = filtered.filter(p => p.status === 'approved');
      } else if (this.activeTab === 'rejected') {
        filtered = filtered.filter(p => p.status === 'rejected');
      }
      
      if (this.query) {
        const q = this.query.toLowerCase();
        filtered = filtered.filter(p => 
          p.name.toLowerCase().includes(q) ||
          p.town.toLowerCase().includes(q) ||
          p.address.toLowerCase().includes(q) ||
          p.phone_number.includes(q)
        );
      }
      
      return filtered;
    }
  },
  methods: {
    async loadPriyuts() {
      this.load = true;
      try {
        const response = await get_priyuts(this.token);
        if (response && Array.isArray(response)) {
          this.priyuts = response;
        }
      } catch (error) {
        console.error('Ошибка загрузки приютов:', error);
      } finally {
        this.load = false;
      }
    },
    changeTab(tab) {
      this.activeTab = tab;
    },
    toggleMenu(priyutId, event) {
      event.stopPropagation();
      this.currentPriyutId = priyutId;
      this.menuVisible = !this.menuVisible;
    },
    async handleOption(option) {
      this.menuVisible = false;
      
      if (option === 'Подтвердить статус') {
        await this.approveShelter();
      } else if (option === 'Отклонить') {
        this.showRejectDialog = true;
      } else {
        console.log(`Действие: ${option} для приюта ID: ${this.currentPriyutId}`);
        // Здесь можно добавить другие действия
      }
    },
    async approveShelter() {
      this.load = true;
      try {
        const response = await post_priyuts_status(
          'approve',
          null,
          this.currentPriyutId,
          this.token
        );
        if (response) {
          await this.loadPriyuts();
        }
      } catch (error) {
        console.error('Ошибка подтверждения приюта:', error);
      } finally {
        this.load = false;
      }
    },
    async rejectShelter() {
      if (!this.rejectionReason) {
        alert('Пожалуйста, укажите причину отказа');
        return;
      }
      
      this.load = true;
      try {
        const response = await post_priyuts_status(
          'reject',
          this.rejectionReason,
          this.currentPriyutId,
          this.token
        );
        if (response) {
          this.showRejectDialog = false;
          this.rejectionReason = "";
          await this.loadPriyuts();
        }
      } catch (error) {
        console.error('Ошибка отклонения приюта:', error);
      } finally {
        this.load = false;
      }
    },
    handleClickOutside() {
      this.menuVisible = false;
    },
    getStatusText(status) {
      switch(status) {
        case 'approved': return 'Подтвержден';
        case 'rejected': return 'Отклонен';
        case 'pending': return 'На модерации';
        default: return status;
      }
    },
    getStatusClass(status) {
      switch(status) {
        case 'approved': return 'status-approved';
        case 'rejected': return 'status-rejected';
        case 'pending': return 'status-pending';
        default: return '';
      }
    },
    formatDate(dateString) {
      const date = new Date(dateString);
      return date.toLocaleDateString('ru-RU');
    }
  },
  async mounted() {
    this.token = localStorage.getItem("token");
    if (this.token && this.token != "") {
      this.name = localStorage.getItem("name");
      this.last_name = localStorage.getItem("last_name");
      await this.loadPriyuts();
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
    <!-- Диалог отклонения приюта -->
    <div v-if="showRejectDialog" class="reject-dialog-overlay">
      <div class="reject-dialog">
        <h3>Укажите причину отказа</h3>
        <textarea v-model="rejectionReason" placeholder="Причина отказа..."></textarea>
        <div class="dialog-buttons">
          <button @click="rejectShelter" class="confirm-btn">Отклонить</button>
          <button @click="showRejectDialog = false" class="cancel-btn">Отмена</button>
        </div>
      </div>
    </div>

    <div class="admin-header">
      <h1>Управление приютами</h1>
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
        placeholder="Поиск по названию, городу или адресу..."
        class="search-input"
      />
    </div>

    <div class="priyuts-list" v-if="!load && filteredPriyuts.length > 0">
      <div class="priyut-card" v-for="priyut in filteredPriyuts" :key="priyut.id">
        <div class="priyut-photo">
          <img 
            :src="`http://26.48.41.80:8000${priyut.photo_url}`"
            :alt="priyut.name"
          />
        </div>
        <div class="priyut-info">
          <h3>{{ priyut.name }}</h3>
          <div class="priyut-meta">
            <span class="priyut-location">
              {{ priyut.town }}, {{ priyut.address }}
            </span>
            <span class="priyut-phone">
              {{ priyut.phone_number }}
            </span>
            <span :class="['priyut-status', getStatusClass(priyut.status)]">
              {{ getStatusText(priyut.status) }}
            </span>
          </div>
          <p class="priyut-description">{{ priyut.description }}</p>
          <div class="priyut-footer">
            <a :href="priyut.link_maps" target="_blank" class="map-link">
              Посмотреть на карте
            </a>
            <span class="priyut-date">
              Создан: {{ formatDate(priyut.created_at) }}
            </span>
          </div>
          <div v-if="priyut.rejection_reason" class="rejection-reason">
            <strong>Причина отказа:</strong> {{ priyut.rejection_reason }}
          </div>
        </div>
        <div class="priyut-actions">
          <div class="lp_wrapper">
            <div class="lp_menu" @click="toggleMenu(priyut.id, $event)">
              <p>...</p>
            </div>
            <div
              class="lp_dropdown"
              v-show="menuVisible && currentPriyutId === priyut.id"
              @click.stop
            >
              <div class="lp_option" @click="handleOption('Удалить приют')">Удалить приют</div>
              <div class="lp_option" @click="handleOption('Заблокировать')">Заблокировать</div>
              <div class="lp_option" @click="handleOption('Разблокировать')">Разблокировать</div>
              <div 
                class="lp_option" 
                @click="handleOption(priyut.status === 'pending' ? 'Подтвердить статус' : 'Отклонить')"
              >
                {{ priyut.status === 'pending' ? 'Подтвердить статус' : 'Отклонить' }}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div v-else-if="!load && filteredPriyuts.length === 0" class="no-results">
      <p>Нет приютов для отображения</p>
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
  display: flex;
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  overflow: hidden;
  position: relative;
}

.priyut-photo {
  width: 250px;
  height: 200px;
  flex-shrink: 0;
}

.priyut-photo img {
  width: 100%;
  height: 100%;
  object-fit: cover;
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
}

.priyut-status {
  padding: 2px 8px;
  border-radius: 4px;
  font-size: 12px;
  font-weight: bold;
}

.status-approved {
  background-color: #E6F7E6;
  color: #2E7D32;
}

.status-rejected {
  background-color: #FFEBEE;
  color: #C62828;
}

.status-pending {
  background-color: #FFF8E1;
  color: #F57F17;
}

.priyut-description {
  margin: 0;
  color: #444;
  font-size: 14px;
}

.priyut-footer {
  display: flex;
  justify-content: space-between;
  margin-top: auto;
  font-size: 13px;
}

.map-link {
  color: #1976d2;
  text-decoration: none;
}

.map-link:hover {
  text-decoration: underline;
}

.priyut-date {
  color: #888;
}

.rejection-reason {
  margin-top: 10px;
  padding: 8px;
  background-color: #ffebee;
  border-radius: 4px;
  font-size: 13px;
  color: #c62828;
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
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  z-index: 10;
  padding: 0;
  display: flex;
  flex-direction: column;
}

.lp_option {
  padding: 8px 20px;
  cursor: pointer;
  transition: background-color 0.2s;
  font-size: 16px;
  margin:0;
}
.lp_option:first-child {
  border-radius: 11px 11px 0 0;
}
.lp_option:last-child {
 border-radius:  0 0 11px 11px;
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

.reject-dialog-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.reject-dialog {
  background-color: white;
  padding: 20px;
  border-radius: 11px;
  width: 400px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
}

.reject-dialog h3 {
  margin-top: 0;
  color: #5A2F10;
}

.reject-dialog textarea {
  width: 100%;
  height: 100px;
  padding: 10px;
  margin: 10px 0;
  border: 1px solid #DFBB9E;
  border-radius: 8px;
  resize: vertical;
}

.dialog-buttons {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}

.confirm-btn {
  background-color: #FF5252;
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 8px;
  cursor: pointer;
}

.cancel-btn {
  background-color: #FFEEE0;
  border: none;
  padding: 8px 16px;
  border-radius: 8px;
  cursor: pointer;
}

.confirm-btn:hover {
  background-color: #FF1744;
}

.cancel-btn:hover {
  background-color: #DFBB9E;
}
</style>