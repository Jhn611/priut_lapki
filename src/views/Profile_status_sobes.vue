<script>
import { get_interview_status, post_interview } from "@/API";
import CatCard from "../components/CatCard.vue";
export default {
  data() {
    return {
      // тут переменные которые будут изменяться или использоваться для отображения или для изменения состояния(видно или не видно блок например)
      token: "",
      name: "",
      last_name: "",
      login: false,
      status: null,
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
    logout() {
      this.token = "";
      this.name = "";
      this.last_name = "";
      localStorage.setItem("token", "");
      localStorage.setItem("name", "");
      localStorage.setItem("last_name", "");
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
      const json = await get_interview_status(this.token);
      if (json == 401 || typeof json == "undefined") {
        localStorage.setItem("token", "");
        this.login = false;
      } else {
        this.status = json["status"];
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
      <div class="loader" v-if="load">
        <img src="../assets/imgs/Loader.svg" alt="" />
      </div>
      <div class="status_sobes" v-if="!load"><p>Статус собеседования</p></div>
      <!-- <div
        class="status_sobes"
        @click="changePageToSobes"
        style="cursor: pointer"
      >
        <p>Статус собеседования</p>
      </div> -->

      <!-- когда собеседование не пройдено -->
      <div class="bgr_status_sobes" v-if="this.status == 'None'">
        <div class="complete_sobes"><p>Собеседование не пройдено</p></div>
        <div
          class="pass_an_sobes"
          @click="changePageToSobes"
          style="cursor: pointer"
        >
          <p>Пройти собеседование</p>
        </div>
      </div>
      <!-- когда собеседование пройдено успешно -->
      <!-- <div class="status_sobes"> <p> Статус собеседования </p> </div> -->
      <div class="bgr_status_sobes" v-if="this.status == 'passed'">
        <div class="complete_sobes_sucsess">
          <p>Собеседование пройдено успешно!</p>
        </div>
        <div class="pass_an_sobes_sucsess">
          <p class="pass_text">
            Ждем вас в рабочее время приюта на стойке администратора в рабочее
            время (10:00-20:00) <br />
            Администратор проведет с вами личную беседу, познакомит с будущем
            питомцем и, в случае взаимной симпатии, оформит нужные документы.
          </p>
        </div>
      </div>
      <!-- когда собеседование пройдено с фейлом -->

      <div class="bgr_status_sobes" v-if="this.status == 'failed'">
        <div class="complete_sobes_fail"><p>Собеседование провалено</p></div>
        <div class="pass_an_sobes_fail">
          <p class="pass_text">
            К сожалению, вы не будете хорошим хозяином для кошки и мы не сможем
            отдать в ваши руки животное. <br />
            <br />
            Повторная попытка будет доступна date
          </p>
        </div>
      </div>
    </div>
</template>

<style src="../styles/style.css"></style>
