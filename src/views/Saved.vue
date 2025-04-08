<script>
import CatCard from "../components/CatCard.vue";
export default {
  data() {
    return {
      // тут переменные которые будут изменяться или использоваться для отображения или для изменения состояния(видно или не видно блок например)
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
  <div class="saved_all"> 
    <div class="saved_cats"> <a> Котики, которые вам понравились </a></div>
    <div class="bgr_saved_cats"> 
        <div class="saved_cats_cards"> 
            <div class="prizrak"> </div>
            <div class="prizrak"> </div>
            <div class="prizrak"> </div>
            <div class="prizrak"> </div>
        </div>
        
    </div>
    <div class="saved_cats_else"> <a class="sce_text"> Добавляйте котиков не только в избранное, но и в свой дом! </a></div>
  </div>

  
</template>

<style src="../styles/style.css"></style>
