<script>
import { get_interview_status, update_profile } from "@/API";
import CatCard from "../components/CatCard.vue";
export default {
  data() {
    return {
      // тут переменные которые будут изменяться или использоваться для отображения или для изменения состояния(видно или не видно блок например)
      token: "",
      name: "",
      last_name: "",
      phone: "",
      load: false,
      login: false,
      armored_cats: [{
    "name": "string",
    "age": "string",
    "color": "string",
    "breed": "string",
    "gender": "string",
    "description": "string",
    "photo_url": new URL("../assets/imgs/cat1.jpg", import.meta.url).href,
    "is_sterilized": false,
    "has_rabies_vaccine": false,
    "id": 0,
    "booked_by_user_id": 0,
    "is_favorite": false
  }],
  activeModalId: null,
    };
  },
  components: {
    //тут импортируются компоненты (например карточка)
    CatCard,
  },
  computed: {
    // тут функции которые что-то считают и возвращают что-то (пока можно не использовать, это для оптимизации)
  },
  methods: {
    openModal(catId) {
      this.activeModalId = catId; // Устанавливаем ID кота для модального окна
    },
    closeModal(e) {
      // Закрываем только если клик был не по кнопке меню
      if (!e.target.closest(".menu-modal-btn")) {
        this.activeModalId = null;
      }
    },
    isModalOpen(catId) {
      return this.activeModalId === catId; // Проверяем, для этого ли кота открыто окно
    },
    changeTab() {
      this.$router.push(`/home`);
    },
    fix(str){
      if(str == ""){
        return "";
      }else{
        return str[0];
      }
    },  
    async sendChanges(){
      this.load = true;
      try {
        const reg = await update_profile(this.name, this.last_name, this.phone, this.token);
        if(json != 401 || typeof json != 'undefined'){
          localStorage.setItem("name", this.name);
          localStorage.setItem("last_name", this.last_name);
          localStorage.setItem("phone", this.phone );
        }
        this.load = false;
      } catch {
        this.load = false;
      }
    },
    logout(){
      this.token = '';
      this.name = '';
      this.last_name = '';
      localStorage.setItem('token', '')
      localStorage.setItem('name', '')
      localStorage.setItem('last_name', '')
      this.$router.push("/home");
    },  
    //тут функции которые будем использовать для изменения визуального контента (изменение переменных, добавление стилей, и т. д.) в целом можно все тут писать
  },

  async mounted() {
    // то что происходит когда страница создаётся (то есть запуск анимаций которые должны проиграться при открытии страницы и подобное)
    this.token = localStorage.getItem("token");
    if (this.token && this.token != "") {
      this.name = localStorage.getItem("name");
      this.last_name = localStorage.getItem("last_name");
      this.phone = localStorage.getItem("phone");
      const json = await get_interview_status(this.token);
      if(json == 401 || typeof json == 'undefined'){
        localStorage.setItem("token", '') 
        this.login = false;
      }else{
        this.login = true;
      }
    }
    document.addEventListener("click", this.closeModal.bind(this));
  },

  unmounted() {
    document.removeEventListener("click", this.closeModal.bind(this));
  },
};
</script>

<template>
  <div class="background_profile_right"> 
    <div class="status_sobes" v-if="!load && armored_cats.length != 0"> <p> Мои брони </p> </div>
    <div class="cats_armored" v-if="!load && armored_cats.length != 0">
      <div v-for="cat in armored_cats" :key="cat.id">
        <div class="profile-armored-cat">
          <img :src="cat.photo_url" alt="">
          <div class="profile-armored-cat-right">
            <div class="profile-armored-cat-right-header"><p>{{ cat.name }}</p> <div class="menu-modal-btn" @click="openModal(cat.id)">...</div></div>
            <div class="profile-armored-cat-right-description"><p>Кот за вами забронирован.
Свяжитесь с приютом для уточнения деталей.</p> <button>Связаться</button></div>
          </div>
          <div class="menu-modal" v-if="isModalOpen(cat.id)">
            <p class="menu-modal-option">Перейти к объявлению</p>
            <p class="menu-modal-option">Снять бронь</p>
          </div>
        </div>
      </div> 
    </div>
    <div class="status_sobes" v-if="!load && armored_cats.length == 0" @click="changeTab"> <p> Просмотр объявлений </p> </div>
    <div class="loader" v-if="load">
        <img src="../assets/imgs/Loader.svg" alt="" />
    </div>   
  </div>
</template>

<style src="../styles/style.css"></style>
