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
    //header
    changePageToPriyut() {
      this.$router.push("/hellopage");
    },
    changePageToPriyut() {
      this.$router.push("/saved");
    },
    changePageToProfile() {
      this.$router.push("/profile_changeinfo");
    },
        changePageToPriyut() {
      this.$router.push("/announcements");
    },
    changePageToSaved() {
      this.$router.push("/post_an_ad");
    },
    changePageToHowtohelp() {
      this.$router.push("/sobesevodanie");
    },
    //other
    changePageToHome() {
      this.$router.push("/priyut");
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
    <div class="hp_all_all">
        <div class="hp_all">
        <div class="hellopage_all">
        <div class="hp_left">
            <div class="text_hp1"> 
                <img src="../assets/imgs/texthp1.svg">
            </div>
            <div class="text_hp2"> 
                <img src="../assets/imgs/texthp2.svg">
            </div>
            <div class="button_want_a_cat">
                <img src="../assets/imgs/buttonhp.svg">
            </div>
            </div>
        <div class="image_cat_hp">
            <img src="../assets/imgs/Cat_hp.svg">
        </div>
        </div>  
    </div>
    <div class="cuties"> 
        <div class="marquee">
            <div class="track">
            <div class="repeat">
                <span class="word">Лапочки</span>
                <span class="word">Лапочки</span>
                <span class="word">Лапочки</span>
                <span class="word">Лапочки</span>
                <span class="word">Лапочки</span>
                <span class="word">Лапочки</span>
                <span class="word">Лапочки</span>
                <span class="word">Лапочки</span>
                <span class="word">Лапочки</span>
                <span class="word">Лапочки</span>
            </div>
            <!-- Копия для бесшовности -->
            <div class="repeat">
                <span class="word">Лапочки</span>
                <span class="word">Лапочки</span>
                <span class="word">Лапочки</span>
                <span class="word">Лапочки</span>
                <span class="word">Лапочки</span>
                <span class="word">Лапочки</span>
                <span class="word">Лапочки</span>
                <span class="word">Лапочки</span>
                <span class="word">Лапочки</span>
                <span class="word">Лапочки</span>
            </div>
            </div>
        </div>
    </div>
    <div class="steps">
        <img src="../assets/imgs/step1.svg">
        <img src="../assets/imgs/step2.svg">
        <img src="../assets/imgs/step3.svg">
    </div>
    </div>
  
</template>

<style src="../styles/style.css"></style>
