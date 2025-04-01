<script>
import CatCard from "../components/CatCard.vue";
export default {
  data() {
    return {
      // тут переменные которые будут изменяться или использоваться для отображения или для изменения состояния(видно или не видно блок например)
        login: true
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
    changePageToProfile_changeinfo(){
      this.$router.push('/profile_changeinfo');
    },
    changePageToProfile_cats(){
      this.$router.push('/profile_cats');
    },
    //тут функции которые будем использовать для изменения визуального контента (изменение переменных, добавление стилей, и т. д.) в целом можно все тут писать
  },

  async mounted() {
    // то что происходит когда страница создаётся (то есть запуск анимаций которые должны проиграться при открытии страницы и подобное)
  },

  unmounted() {
    // то что происходит когда страница закрывается/происходит переход на другу страницу
  },
};
</script>

<template>
  <div class="logRegIn-block"> 
    
  </div>
</template>

<style src="../styles/style.css"></style>
