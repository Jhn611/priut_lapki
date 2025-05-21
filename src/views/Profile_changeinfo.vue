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
    changePageToProfile(){
      this.$router.push('/profile');
    },
    changePageToProfile_changeinfo(){
      this.$router.push('/profile_changeinfo');
    },
    changePageToProfile_cats(){
      this.$router.push('/profile_cats');
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
  },

  unmounted() {
    // то что происходит когда страница закрывается/происходит переход на другу страницу
  },
};
</script>

<template>
  <div class="profile_right_container"> 
    <div class="status_sobes" v-if="!load"> <p> Изменение информации профиля </p> </div>
    <div class="bgr_status_sobes" v-if="!load"> 
      <p> Имя </p>
      <label class="input">
            <input
              v-model="name"
              class="input__field"
              type="text"
              placeholder=" "
            />
            <span class="input__label">Например: Иван</span>
      </label>
    
      <p> Фамилия </p>
      <label class="input">
            <input
              v-model="last_name"
              class="input__field"
              type="text"
              placeholder=" "
            />
            <span class="input__label">Например: Иванов</span>
      </label>
      
      <p> Номер телефона </p>
      <label class="input">
            <input
              v-model="phone"
              class="input__field"
              type="text"
              placeholder=" "
            />
            <span class="input__label">Например: +79321112723</span>
      </label>

      <div @click="sendChanges" class="btn">
        <p>Изменить</p>
      </div>
    </div>
    <div class="loader" v-if="load">
        <img src="../assets/imgs/Loader.svg" alt="" />
    </div>   
  </div>
</template>

<style src="../styles/style.css"></style>
