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
  <div class="howtohelp_all"> 
    <div class="howtohelp_text"> <a> Как помочь приюту </a></div>
    <div class="bgr_howtohelp_cats"> 
        <p> Самая необходимая нужда приюта, как и самый легкий путь помощи - материально поддержать наш проект. <br> Вы можете сделать пожертвование следующими способами  </p>
        <div class="bgr_helps">
          <div class="bgr_help1"> </div>
          <div class="bgr_help2"> </div>
        </div>
    </div>
    
  </div>
</template>

<style src="../styles/style.css"></style>
