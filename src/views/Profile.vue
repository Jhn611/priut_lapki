<script>
import { get_interview_status } from "@/API";
import CatCard from "../components/CatCard.vue";
// Импортируем изображения напрямую
import RadioButtonOn from "../assets/imgs/Radio_button_on.svg";
import RadioButtonOff from "../assets/imgs/Radio_button_off.svg";

export default {
  data() {
    return {
      token: "",
      name: "",
      last_name: "",
      phone: "",
      load: false,
      login: false,
      activeTab: 'status',
      tabs: [
        { id: 'edit', label: 'Изменить профиль' },
        { id: 'status', label: 'Статус собеседования' },
        { id: 'armor', label: 'Мои бронирования' },
        { id: 'ad', label: 'Мои объявления' },
        { id: 'priyut', label: 'Мой приют' },
      ],
      // Добавляем пути к изображениям в data
      radioButtonOn: RadioButtonOn,
      radioButtonOff: RadioButtonOff
    };
  },
  components: {
    CatCard,
  },
  watch: {
    '$route.path'(newPath) {
      this.updateActiveTab(newPath);
    }
  },
  methods: {
    updateActiveTab(path) {
      const tab = path.split('/profile/')[1] || '/profile/status';
      this.activeTab = tab;
    },
    changeTab(tab) {
      this.activeTab = tab;
      this.$router.push(`/profile/${tab}`);
    },
    fix(str) {
      return str ? str[0] : "";
    },  
    async sendChanges() {
      this.load = true;
      try {
        const reg = await update_profile(this.name, this.last_name, this.phone, this.token);
        if(reg != 401 && typeof reg != 'undefined'){
          localStorage.setItem("name", this.name);
          localStorage.setItem("last_name", this.last_name);
          localStorage.setItem("phone", this.phone);
        }
        this.load = false;
      } catch {
        this.load = false;
      }
    },
    logout() {
      this.token = '';
      this.name = '';
      this.last_name = '';
      localStorage.setItem('token', '');
      localStorage.setItem('name', '');
      localStorage.setItem('last_name', '');
      this.$router.push("/home");
    }
  },
  async mounted() {
    this.token = localStorage.getItem("token");
    if (this.token && this.token != "") {
      this.name = localStorage.getItem("name");
      this.last_name = localStorage.getItem("last_name");
      const json = await get_interview_status(this.token);
      if(json == 401 || typeof json == 'undefined'){
        localStorage.setItem("token", ''); 
        this.login = false;
      } else {
        this.login = true;
      }
    }
    this.updateActiveTab(this.$route.path);
  }
};
</script>

<template>
  <div class="background_profile"> 
    <div class="background_profile_left">
      <div class="profile_setup">
        <div class="bgr_avatarka">
          <div class="p_NS">
            <p>{{ fix(name) + fix(last_name) }}</p>
          </div>
        </div>
        <div class="Name_Subname">
          <p class="Name">{{ name }}</p>
          <p class="Subname">{{ last_name }}</p>
        </div>
      </div>

      <div class="meaning">
        <img src="../assets/imgs/Rectangle.svg" alt="decoration">
        <p class="text_mean">Любитель котиков, который может подарить счастливую жизнь и любимый дом коту.</p>
      </div>

      <div class="pr_setup_all">
        <div 
          v-for="tab in tabs" 
          :key="tab.id"
          class="bgr_ch_pr_with_rb" 
          @click="changeTab(tab.id)" 
          :class="{ 'active-tab': activeTab === tab.id }"
        >
          <img 
            :src="activeTab === tab.id ? radioButtonOn : radioButtonOff" 
            class="rad_but"
            :alt="tab.label"
          >
          <div class="bgr_change_pr">
            <a>{{ tab.label }}</a>
          </div>
        </div>
      </div>
      
      <div v-if="login" class="btn" @click="logout">
        <p>Выйти</p>
      </div>
    </div>

    <div class="background_profile_right"> 
      <router-view></router-view>
    </div>
  </div>
</template>

<style src="../styles/style.css"></style>
