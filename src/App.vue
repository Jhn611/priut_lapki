<script>
import MainSearch from './components/MainSearch.vue';
export default {
  data() {
    return {
      // тут переменные которые будут изменяться или использоваться для отображения или для изменения состояния(видно или не видно блок например)
      cats: [1, 2],
      command: "",
    }
  },
  components: {
    //тут импортируются компоненты (например карточка)
    MainSearch,
  },
  computed: {
    // тут функции которые что-то считают и возвращают что-то (пока можно не использовать, это для оптимизации)
  },
  methods: {
    //тут функции которые будем использовать для изменения визуального контента (изменение переменных, добавление стилей, и т. д.) в целом можно все тут писать
    changePageToProfile(){
      this.$router.push('/profile');
    },
    changePageToHome(){
      this.$router.push('/home');
    },
    changePageToSaved(){
      this.$router.push('/saved');
    },
    changePageToContacts(){
      this.$router.push('/contacts');
    },
    changePageToHowtohelp(){
      this.$router.push('/howtohelp');
    },
    changePageToSurrenderaCat(){
      this.$router.push('/surrender_a_cat');
    },
  },
  async mounted() {
    // то что происходит когда страница создаётся (то есть запуск анимаций которые должны проиграться при открытии страницы и подобное)
    this.$router.push('/home');
  },

  unmounted() {
    // то что происходит когда страница закрывается/происходит переход на другу страницу
  },
}
</script>

<template>
  <header>
    <div class="background_find"> 
      <div class="bg_upper">
        <img class="logo_find" src="./assets/imgs/logo.svg" @click="changePageToHome" style="cursor: pointer;" />
        <MainSearch v-model="command"/>
        <div class="header_icons">
          <img class="icon_home" src="./assets/imgs/Home.svg" @click="changePageToHome" style="cursor: pointer;"/>
          <img class="icon_heart" src="./assets/imgs/Heart.svg" @click="changePageToSaved" style="cursor: pointer;"/>
          <img class="icon_user" src="./assets/imgs/User.svg" @click="changePageToProfile" style="cursor: pointer;"/>
        </div>
      </div>
      <div class="header_text">
        <div class="header_text1">
          <a @click="changePageToHowtohelp" style="cursor: pointer;"> Как помочь </a>
          <a> Нужды приюта </a>
          <a> Полезные статьи </a>
          <a @click="changePageToSurrenderaCat" style="cursor: pointer;"> Сдать кошку в приют </a>
          <a @click="changePageToContacts" style="cursor: pointer;"> Контакты </a> 
        </div>

        <div class="header_text2">
          <a> Москва Ул. Софьи Ковалевской 228 </a>
        </div>
      </div>
    </div>
  </header>

  <main id="main">
    <RouterView :command="command"/>
  </main>
</template>

<style src="./styles/style.css"> </style>
