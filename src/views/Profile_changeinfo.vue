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
  <div class="background_profile"> 
  <div class="background_profile_left">
    <div class="profile_setup">
        <div class="bgr_avatarka">
          <div class="p_NS">
            <p>{{ name[0] + last_name[0] }}</p>
          </div>
        </div>
        <div class="Name_Subname">
          <p class="Name">{{ name }}</p>
          <p class="Subname">{{ last_name }}</p>
        </div>
      </div>

    <div class="meaning">
      <img src="../assets/imgs/Rectangle.svg" />
      <p class="text_mean"> Любитель котиков, который может подарить счастливую жизнь и любимый дом
        коту. </p>
        <p class="text_mean_gpt">(Сгенерированно GigaChat)</p>
    </div>

    <div class="pr_setup_all"> 

      <div class="bgr_ch_pr_with_rb" @click="changePageToProfile_changeinfo" style="cursor: pointer;"> 
        <img src="../assets/imgs/Radio_button_on.svg" class="rad_but">
        <div class="bgr_change_pr"> <a> Изменить профиль </a></div>
      </div>

      <div class="bgr_ch_pr_with_rb" @click="changePageToProfile" style="cursor: pointer;"> 
        <img src="../assets/imgs/Radio_button_off.svg" class="rad_but">
        <div class="bgr_sobes"> <a> Статус собеседования </a></div>
      </div>

      <div class="bgr_ch_pr_with_rb" @click="changePageToProfile_cats" style="cursor: pointer;">
        <img src="../assets/imgs/Radio_button_off.svg" class="rad_but3">
        <div class="bgr_catstopriyut"> <a> Коты, сданные в приют </a> </div>
      </div>

    </div>
  </div>

  <div class="background_profile_right"> 
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
  </div>
</template>

<style src="../styles/style.css"></style>
