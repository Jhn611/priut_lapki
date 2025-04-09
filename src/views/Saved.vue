<script>
import { get_favorite } from "../API.js";
import CatCard from "../components/CatCard.vue";
export default {
  data() {
    return {
      // тут переменные которые будут изменяться или использоваться для отображения или для изменения состояния(видно или не видно блок например)
      load: false,
      cats: [],
      token: "",
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
    changePageToProfile() {
      this.$router.push("/profile");
    },
    changePageToHome() {
      this.$router.push("/home");
    },
    changePageToSaved() {
      this.$router.push("/saved");
    },
    changePageToContacts() {
      this.$router.push("/contacts");
    },
    changePageToHowtohelp() {
      this.$router.push("/howtohelp");
    },
    //тут функции которые будем использовать для изменения визуального контента (изменение переменных, добавление стилей, и т. д.) в целом можно все тут писать
  },

  async mounted() {
    // то что происходит когда страница создаётся (то есть запуск анимаций которые должны проиграться при открытии страницы и подобное)
    this.token = localStorage.getItem("token");
    if (this.token && this.token != "") {
      this.load = true;
      try {
        const cats_cards = await get_favorite(this.token);
        console.log("карточки: ", cats_cards);
        if (cats_cards) {
          let x = [];
          let current = [];
          for (let i = 0; i < cats_cards.length; i++) {
            current.push(cats_cards[i]);
            if (current.length % 4 == 0) {
              x.push(current);
              current = [];
            }
          }
          if (current.length != 0) {
            x.push(current);
          }
          this.cats = x;
        }
        console.log(this.cats);

        const height = this.cats.length * 286 + this.cats.length * 30;
        const currentStyles = document.body.style.cssText;
        document.body.style.cssText =
          currentStyles + `--mainHeight: ${height}px`;
        this.load = false;
      } catch {
        this.load = false;
      }
    }
  },

  unmounted() {
    // то что происходит когда страница закрывается/происходит переход на другу страницу
  },
};
</script>

<template>
  <div class="saved_all">
    <div class="saved_cats"><a> Котики, которые вам понравились </a></div>
    <div class="background_card_container" v-if="!load">
      <div class="background_card" v-for="x in cats" :key="x">
        <CatCard v-for="i in x" :key="i" :data="i" />
      </div>
    </div>
    <div class="saved_cats_if" v-if="cats.length == 0 && !load">
      <a class="sce_text">
        Здесь пока ничего нет, надеемся вы найдете любимчиков!
      </a>
    </div>
    <div class="loader" v-if="load">
      <img src="../assets/imgs/Loader.svg" alt="" />
    </div>
    <div class="saved_cats_else" v-if="!load">
      <a class="sce_text">
        Добавляйте котиков не только в избранное, но и в свой дом!
      </a>
    </div>
  </div>
</template>

<style src="../styles/style.css"></style>
