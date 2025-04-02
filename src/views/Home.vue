<script>
import CatCard from "../components/CatCard.vue";
import { get_cats, search_cats } from "../API.js";
export default {
  data() {
    return {
      // тут переменные которые будут изменяться или использоваться для отображения или для изменения состояния(видно или не видно блок например)
      cats: [1, 2],
      load: false,
    };
  },
  props: ["command"],
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
  watch: {
    async command(newCommand) {
      if (newCommand) {
        this.load = true
        try{
          console.log("Получена команда:", newCommand);
          const cats_cards = await search_cats(newCommand);
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
            if(current.length != 0){
              x.push(current);
            }
            this.cats = x;
          }
          console.log(this.cats);
          const height = this.cats.length * 286 + this.cats.length * 50;
          const currentStyles = document.body.style.cssText;
          document.body.style.cssText = currentStyles + `--mainHeight: ${height}px`
          this.load = false
        }
        catch{
          this.load = false
        }
        
      }
    },
  },

  async mounted() {
    this.load = true  
    try{
      const cats_cards = await get_cats();
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
        if(current.length != 0){
          x.push(current);
        }
        this.cats = x;
      }
      console.log(this.cats);

      const height = this.cats.length * 286 + this.cats.length * 50;
      const currentStyles = document.body.style.cssText;
      document.body.style.cssText = currentStyles + `--mainHeight: ${height}px`
      this.load = false 
    }catch{
      this.load = false 
    }
  },

  unmounted() {
    // то что происходит когда страница закрывается/происходит переход на другу страницу
  },
};
</script>

<template>
  <div class="background_card_container" v-if="!load">
    <div class="background_card" v-for="x in cats" :key="x">
      <CatCard v-for="i in x" :key="i" :data="i" />
    </div>
  </div>
  <div class="loader" v-if="load">
    <img src="../assets/imgs/Loader.svg" alt="">
  </div>
  
</template>

<style src="../styles/style.css"></style>
